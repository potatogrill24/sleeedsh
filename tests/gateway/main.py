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
        review_management_port="8004"
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


# def test_add_to_cart_success(use_case):
#     with patch.object(use_case, "_GatewayUseCase__authorization", return_value={"type": "user", "id": 1}):
#         with patch("grpc.insecure_channel") as mock_channel:
#             mock_stub = MagicMock(spec=OrderManagementStub)
#             mock_channel.return_value.__enter__.return_value = mock_stub

#             mock_stub.add_product = MagicMock(return_value=None)

#             result = use_case.add_to_cart("Bearer mock_token", 42)

#             assert result == "success"
#             mock_stub.add_product.assert_called_once_with(
#                 OrderOperationRequest(user_id=1, product_id=42)
#             )


def test_create_review_invalid_rate(use_case):
    with pytest.raises(HTTPException) as exc_info:
        use_case.create_review("Bearer mock_token", 42, 6.0, "Great product")
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "rate must be between 1 and 5"


# def test_create_review_success(use_case):
#     with patch.object(use_case, "_GatewayUseCase__authorization", return_value={"type": "user", "id": 1}):
#         with patch("grpc.insecure_channel") as mock_channel:
#             mock_stub = MagicMock()
#             mock_channel.return_value.__enter__.return_value = mock_stub

#             mock_stub.create_review = MagicMock(return_value=None)

#             result = use_case.create_review("Bearer mock_token", 42, 4.5, "Great product")
#             assert result == "success"
#             mock_stub.create_review.assert_called_once_with(
#                 CreateReviewRequest(user_id=1, product_id=42, rate=4.5, text="Great product")
#             )


def test_delete_review_shop_fail(use_case):
    with patch.object(use_case, "_GatewayUseCase__authorization", return_value={"type": "shop", "id": 1}):
        with pytest.raises(HTTPException) as exc_info:
            use_case.delete_review("Bearer mock_token", 42)
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "shops cant delete review"


# def test_delete_review_success(use_case):
#     with patch.object(use_case, "_GatewayUseCase__authorization", return_value={"type": "user", "id": 1}):
#         with patch("grpc.insecure_channel") as mock_channel:
#             mock_stub = MagicMock()
#             mock_channel.return_value.__enter__.return_value = mock_stub

#             mock_stub.delete_review = MagicMock(return_value=None)

#             result = use_case.delete_review("Bearer mock_token", 42)
#             assert result == "success"
#             mock_stub.delete_review.assert_called_once_with(
#                 DeleteReviewRequest(user_id=1, product_id=42)
#             )
