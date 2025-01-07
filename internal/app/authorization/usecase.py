import jwt
import base64
import bcrypt

from internal.app.authorization.repository import AuthorizationRepository
from fastapi import HTTPException, status


class AuthorizationUseCase:
    def __init__(self, repository: AuthorizationRepository, jwt_secret_key: str, session_time_in_secs: int):
        self.__repository = repository
        self.__jwt_secret_key = jwt_secret_key
        self.__session_time_in_secs = session_time_in_secs

    def authenticate_entity(self, b64: str) -> str:
        try:
            decoded = base64.b64decode(b64, validate=True)
            decoded = decoded.decode()
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='invalid base64 format')

        tokens = decoded.split(':')
        if len(tokens) != 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='invalid base64 format')

        entity_type = tokens[0]
        login = tokens[1]
        password = tokens[2]

        if entity_type == "shop":
            entity_id, password_hash = self.__repository.authenticate_shop(
                login)
        elif entity_type == "user":
            entity_id, password_hash = self.__repository.authenticate_user(
                login)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='invalid entity type')

        if not bcrypt.checkpw(password.encode(), password_hash.encode()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='password mismatch')

        entity = {
            'id': entity_id,
            'type': entity_type
        }

        json_web_token = jwt.encode(
            entity, self.__jwt_secret_key, algorithm='HS256')

        if self.__repository.add_jwt_to_redis(json_web_token, self.__session_time_in_secs) is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unable to push jwt to redis')

        return json_web_token

    def authorize_entity(self, json_web_token: str) -> tuple[int, str]:
        if not self.__repository.check_jwt_in_redis(json_web_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='could not find jwt')

        decoded = jwt.decode(
            json_web_token, key=self.__jwt_secret_key, algorithms=["HS256"])
        return decoded['id'], decoded['type']

    def logout_entity(self, json_web_token: str):
        if not self.__repository.delete_jwt_from_redis(json_web_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='could not find jwt')

    def register_user(self, reg: str):
        try:
            decoded = base64.b64decode(reg, validate=True)
            decoded = decoded.decode()
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='invalid base64 format')
        tokens = decoded.split(':')
        if len(tokens) != 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='invalid regform format')
        name = tokens[0]
        login = tokens[1]
        password = tokens[2]
        if self.__repository.check_registered_user(login):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='user already registered')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(
            password.encode('utf-8'), salt).decode('utf-8')
        self.__repository.register_user(name, login, password_hash)
