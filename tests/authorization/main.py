import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from internal.app.authorization.usecase import AuthorizationUseCase
import jwt
import bcrypt
import base64

# Фикстура для настроек
@pytest.fixture
def jwt_secret_key():
    return "test_secret"

@pytest.fixture
def session_time_in_secs():
    return 3600

@pytest.fixture
def repository():
    return MagicMock()

@pytest.fixture
def use_case(repository, jwt_secret_key, session_time_in_secs):
    return AuthorizationUseCase(repository, jwt_secret_key, session_time_in_secs)

# Тесты для authenticate_entity
def test_authenticate_entity_success(repository, use_case, jwt_secret_key):
    b64 = "user:test_login:test_password"
    hashed_password = bcrypt.hashpw("test_password".encode(), bcrypt.gensalt()).decode()

    repository.authenticate_user.return_value = (1, hashed_password)
    repository.add_jwt_to_redis.return_value = True

    jwt_token = use_case.authenticate_entity(b64.encode())
    decoded = jwt.decode(jwt_token, key=jwt_secret_key, algorithms=["HS256"])

    assert decoded["id"] == 1
    assert decoded["type"] == "user"


def test_authenticate_entity_invalid_base64(use_case):
    with pytest.raises(HTTPException) as exc_info:
        use_case.authenticate_entity("invalid_base64")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'invalid base64 format'


def test_authenticate_entity_invalid_entity_type(repository, use_case):
    b64 = base64.b64encode("invalid:test_login:test_password".encode()).decode()

    with pytest.raises(HTTPException) as exc_info:
        use_case.authenticate_entity(b64.encode())

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'invalid entity type'


def test_authenticate_entity_password_mismatch(repository, use_case):
    b64 = base64.b64encode("user:test_login:test_password".encode()).decode()

    # Создаем корректный, но не соответствующий паролю хеш
    wrong_hash = bcrypt.hashpw("another_password".encode(), bcrypt.gensalt()).decode()

    repository.authenticate_user.return_value = (1, wrong_hash)

    with pytest.raises(HTTPException) as exc_info:
        use_case.authenticate_entity(b64.encode())

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'password mismatch'

# Тесты для authorize_entity
def test_authenticate_entity_success(repository, use_case, jwt_secret_key):
    b64 = base64.b64encode("user:test_login:test_password".encode()).decode()
    hashed_password = bcrypt.hashpw("test_password".encode(), bcrypt.gensalt()).decode()

    repository.authenticate_user.return_value = (1, hashed_password)
    repository.add_jwt_to_redis.return_value = True

    jwt_token = use_case.authenticate_entity(b64.encode())
    decoded = jwt.decode(jwt_token, key=jwt_secret_key, algorithms=["HS256"])

    assert decoded["id"] == 1
    assert decoded["type"] == "user"


def test_authorize_entity_jwt_not_found(repository, use_case):
    repository.check_jwt_in_redis.return_value = False

    with pytest.raises(HTTPException) as exc_info:
        use_case.authorize_entity("invalid_token")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'could not find jwt'

# Тесты для logout_entity
def test_logout_entity_success(repository, use_case):
    repository.delete_jwt_from_redis.return_value = 1

    try:
        use_case.logout_entity("valid_token")
    except HTTPException:
        pytest.fail("Logout raised an exception unexpectedly!")


def test_logout_entity_jwt_not_found(repository, use_case):
    repository.delete_jwt_from_redis.return_value = 0

    with pytest.raises(HTTPException) as exc_info:
        use_case.logout_entity("invalid_token")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'could not find jwt'
