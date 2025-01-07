import grpc
import requests
import json

from fastapi import status, HTTPException

from internal.protos.review_management.review_management_pb2 import CreateReviewRequest, DeleteReviewRequest
from internal.infrastructure.kafka import Producer
from internal.protos.order_management.order_management_pb2_grpc import OrderManagementStub
from internal.protos.order_management.order_management_pb2 import OrderOperationRequest
from internal.protos.review_management.review_management_pb2_grpc import ReviewManagementStub


class GatewayUseCase:
    def __init__(self, producer: Producer, authorization_port: str, profile_port: str, order_management_port: str, review_management_port: str, search_port: str, recommendation_system_port: str):
        self.__producer = producer
        self.__authorization_port = authorization_port
        self.__profile_port = profile_port
        self.__order_management_port = order_management_port
        self.__review_management_port = review_management_port
        self.__search_port = search_port
        self.__recommendation_system_port = recommendation_system_port

    @staticmethod
    def __fetch_get(url, headers=None):
        response = requests.get(url, headers=headers)
        response_data = response.json()
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=response.status_code,
                                detail=response_data['detail'])
        return response_data

    def __authorization(self, auth_header: str) -> dict:
        return self.__fetch_get(f"http://authorization:{self.__authorization_port}/authorization", headers={'Authorization': auth_header})

    def authentication(self, auth_header: str):
        response = requests.get(
            f"http://authorization:{self.__authorization_port}/authentication", headers={'Authorization': auth_header})
        return response.status_code, response.json()

    def logout(self, auth_header: str):
        response = requests.post(
            f"http://authorization:{self.__authorization_port}/logout", headers={'Authorization': auth_header})
        return response.status_code, response.json()

    def register(self, auth_header: str):
        response = requests.post(
            f"http://authorization:{self.__authorization_port}/register", headers={'Authorization': auth_header})
        return response.status_code, response.json()

    def deposit(self, money: int, auth_header: str):
        response_data = self.__authorization(auth_header)

        if response_data['type'] != 'user':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='shops cant deposit any money')

        msg = {
            'type': 'deposit',
            'userID': response_data['id'],
            'diff': money
        }

        self.__producer.produce('money_operations', json.dumps(msg))
        return 'success'

    def buy(self, auth_header: str):
        response_data = self.__authorization(auth_header)

        if response_data['type'] != 'user':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='shops cant buy anything')

        profile = self.__fetch_get(
            f"http://profile:{self.__profile_port}/user/{response_data['id']}")
        if profile['data']['balance'] < profile['total_cart_price']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='not enough money on balance')

        msg = {
            'type': 'buy',
            'userID': response_data['id']
        }

        self.__producer.produce('money_operations', json.dumps(msg))
        return 'success'

    def profile_self(self, auth_header: str):
        response_data = self.__authorization(auth_header)
        return self.__fetch_get(f"http://profile:{self.__profile_port}/{response_data['type']}/{response_data['id']}")

    def profile_other(self, entity_type: str, entity_id: int):
        return self.__fetch_get(f"http://profile:{self.__profile_port}/{entity_type}/{entity_id}?is_public=True")

    def add_to_cart(self, auth_header: str, product_id: int):
        self.__cart_operation(
            to_add=True, auth_header=auth_header, product_id=product_id)
        return 'success'

    def delete_from_cart(self, auth_header: str, product_id: int):
        self.__cart_operation(
            to_add=False, auth_header=auth_header, product_id=product_id)
        return 'success'

    def __cart_operation(self, to_add: bool, auth_header: str, product_id: int):
        response_data = self.__authorization(auth_header)

        if response_data['type'] != 'user':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='shops cant manage carts')

        with grpc.insecure_channel(f"order_management:{self.__order_management_port}") as channel:
            stub = OrderManagementStub(channel)

            if to_add is True:
                stub.add_product(OrderOperationRequest(
                    user_id=response_data['id'], product_id=product_id))
            else:
                stub.delete_product(OrderOperationRequest(
                    user_id=response_data['id'], product_id=product_id))

    def create_review(self, auth_header: str, product_id: int, rate: float, text: str):
        if rate > 5.0 or rate < 1.0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='rate must be between 1 and 5')

        response_data = self.__authorization(auth_header)

        if response_data['type'] != 'user':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='shops cant create reviews')

        with grpc.insecure_channel(f"review_management:{self.__review_management_port}") as channel:
            stub = ReviewManagementStub(channel)
            stub.create_review(CreateReviewRequest(
                user_id=response_data['id'], product_id=product_id, rate=rate, text=text))

        return 'success'

    def delete_review(self, auth_header: str, product_id: int):
        response_data = self.__authorization(auth_header)

        if response_data['type'] != 'user':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='shops cant delete review')

        with grpc.insecure_channel(f"review_management:{self.__review_management_port}") as channel:
            stub = ReviewManagementStub(channel)
            stub.create_review(DeleteReviewRequest(
                user_id=response_data['id'], product_id=product_id))

        return 'success'

    def search(self, payload: dict):
        response = requests.post(
            f"http://search:{self.__search_port}/search", json=payload)
        return response.status_code, response.json()

    def recommend(self, auth_header: str, count: int):
        if not auth_header:
            return self.__fetch_get(
                f"http://recommendation_system:{self.__recommendation_system_port}/predict/0?count={count}")

        auth_data = self.__authorization(auth_header)
        if auth_data['type'] != 'user':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='cant recommend anything for shops')

        return self.__fetch_get(f"http://recommendation_system:{self.__recommendation_system_port}/recommend/{auth_data['id']}?count={count}")

    # def optimal_price(self, auth_header: str):
    #     auth_data = self.__authorization(auth_header)
    #     if auth_data['type'] != 'shop':
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='only shops can do that')
    #
    #     return self.__fetch_get(f"http://recommendation_system:{self.__recommendation_system_port}/optimal_price/{auth_data['id']}")
