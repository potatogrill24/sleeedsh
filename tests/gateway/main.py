import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from internal.app.gateway.usecase import GatewayUseCase
from internal.infrastructure.kafka import Producer
from internal.protos.review_management.review_management_pb2 import CreateReviewRequest, DeleteReviewRequest
from internal.protos.order_management.order_management_pb2 import OrderOperationRequest
from internal.protos.order_management.order_management_pb2_grpc import OrderManagementStub

@pytest.fixture
def mock_producer():
    return MagicMock(spec=Producer)


@pytest.fixture
def use_case(mock_producer):
    return GatewayUseCase(
        producer=mock_producer,
        authorization_port="8001",
        profile_port="8002",
        order_management_port="8003",
        review_management_port="8004",
        search_port="8009"
    )

def test_authentication_success(use_case):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"jwt": "mock_jwt"}
        
        status_code, response = use_case.authentication("Bearer mock_token")
        assert status_code == 200
        assert response["jwt"] == "mock_jwt"


def test_authentication_fail(use_case):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 401
        mock_get.return_value.json.return_value = {"detail": "Unauthorized"}
        
        status_code, response = use_case.authentication("Bearer invalid_token")
        assert status_code == 401
        assert response["detail"] == "Unauthorized"


def test_logout_success(use_case):
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"message": "Logged out"}
        
        status_code, response = use_case.logout("Bearer mock_token")
        assert status_code == 200
        assert response["message"] == "Logged out"


def test_deposit_user_success(use_case, mock_producer):
    with patch.object(use_case, "_GatewayUseCase__authorization", return_value={"type": "user", "id": 1}):
        status_code, message = use_case.deposit(100, "Bearer mock_token")
        
        assert status_code == 200
        assert message == "success"
        mock_producer.produce.assert_called_once()


def test_deposit_shop_fail(use_case):
    with patch.object(use_case, "_GatewayUseCase__authorization", return_value={"type": "shop", "id": 1}):
        with pytest.raises(HTTPException) as exc_info:
            use_case.deposit(100, "Bearer mock_token")
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "shops cant deposit any money"


def test_create_review_invalid_rate(use_case):
    with pytest.raises(HTTPException) as exc_info:
        use_case.create_review("Bearer mock_token", 42, 6.0, "Great product")
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "rate must be between 1 and 5"

def test_search_products_success(use_case):
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"products": [{"id": 1, "name": "Test Product"}]}
        
        status_code, response = use_case.search_products("test")
        assert status_code == 200
        assert response["products"] == [{"id": 1, "name": "Test Product"}]

def test_get_all_products_success(use_case):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"products": [{"id": 1, "name": "Test Product 1"}, {"id": 2, "name": "Test Product 2"}]}

        status_code, response = use_case.get_all_products()
        assert status_code == 200
        assert response["products"] == [{"id": 1, "name": "Test Product 1"}, {"id": 2, "name": "Test Product 2"}]