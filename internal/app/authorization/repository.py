from internal.domain.model import Shop, User
from internal.domain.repository import ShopRepository, UserRepository
from internal.infrastructure.redis import RedisClient


class AuthorizationRepository:
    def __init__(self, shop_repository: ShopRepository, user_repository: UserRepository, redis: RedisClient):
        self.__shop_repository = shop_repository
        self.__user_repository = user_repository
        self.__redis = redis

    def authenticate_shop(self, login: str) -> tuple[int, str]:
        return self.__shop_repository.authorize_shop(login)

    def authenticate_user(self, login: str) -> tuple[int, str]:
        return self.__user_repository.authorize_user(login)

    def add_jwt_to_redis(self, jwt: str, expiration_time):
        return self.__redis.set(jwt, '', expiration_time)

    def check_jwt_in_redis(self, jwt: str):
        return self.__redis.get(jwt) is not None

    def delete_jwt_from_redis(self, jwt: str):
        return self.__redis.delete([jwt])

    def register_user(self, name: str, login: str, password_hash: str):
        return self.__user_repository.register(name, login, password_hash)

    def check_registered_user(self, login: str) -> bool:
        return self.__user_repository.check_registered(login)
