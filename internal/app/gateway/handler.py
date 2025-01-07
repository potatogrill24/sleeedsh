from fastapi import Header, Body, HTTPException, APIRouter, status
from pydantic import BaseModel

from internal.app.gateway.usecase import GatewayUseCase
from internal.app.search.handler import SearchRequest


class DepositRequest(BaseModel):
    money: int


class ReviewCreateRequest(BaseModel):
    product_id: int
    rate: float
    text: str


class ReviewDeleteRequest(BaseModel):
    product_id: int


class GatewayHandler:
    def __init__(self, use_case: GatewayUseCase):
        self.__use_case = use_case
        self.router = APIRouter()

        self.router.add_api_route("/api/login", self.login, methods=["GET"])
        self.router.add_api_route("/api/logout", self.logout, methods=["POST"])
        self.router.add_api_route(
            "/api/register", self.register, methods=["POST"])

        self.router.add_api_route(
            "/api/deposit", self.deposit, methods=["POST"])
        self.router.add_api_route("/api/buy", self.buy, methods=["POST"])

        self.router.add_api_route(
            "/api/profile/{entity_type}/{entity_id}", self.profile_other, methods=["GET"])
        self.router.add_api_route(
            "/api/profile/self", self.profile_self, methods=["GET"])

        self.router.add_api_route(
            "/api/cart/add/{product_id}", self.add_to_cart, methods=["POST"])
        self.router.add_api_route(
            "/api/cart/delete/{product_id}", self.delete_from_cart, methods=["DELETE"])

        self.router.add_api_route(
            "/api/review/create", self.create_review, methods=["POST"])
        self.router.add_api_route(
            "/api/review/delete", self.delete_review, methods=["DELETE"])

        self.router.add_api_route(
            "/api/search", self.search, methods=["POST"])

        self.router.add_api_route(
            "/api/recommendations/{count}", self.recommendations, methods=["GET"])
        # self.router.add_api_route("/api/optimal_price", self.optimal_price, methods=["GET"])

    async def login(self, authorization: str = Header(None)):
        code, data = self.__use_case.authentication(authorization)
        if code != status.HTTP_200_OK:
            raise HTTPException(status_code=code, detail=data['detail'])
        return {'jwt': data['jwt']}

    async def logout(self, authorization: str = Header(None)):
        code, body = self.__use_case.logout(authorization)
        if code != status.HTTP_200_OK:
            raise HTTPException(status_code=code, detail=body['detail'])
        return 'success'

    async def register(self, authorization: str = Header(None)):
        code, body = self.__use_case.register(authorization)
        if code != status.HTTP_200_OK:
            raise HTTPException(status_code=code, detail=body['detail'])
        return 'success'

    async def deposit(self, body: DepositRequest, authorization: str = Header(None)):
        if body.money <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='unable to deposit non positive amount of money')

        return self.__use_case.deposit(
            body.money, auth_header=authorization)

    async def buy(self, authorization: str = Header(None)):
        return self.__use_case.buy(authorization)

    async def profile_self(self, authorization: str = Header(None)):
        return self.__use_case.profile_self(auth_header=authorization)

    async def profile_other(self, entity_type: str, entity_id: int):
        return self.__use_case.profile_other(entity_type, entity_id)

    async def add_to_cart(self, product_id: int, authorization: str = Header(None)):
        return self.__use_case.add_to_cart(
            auth_header=authorization, product_id=product_id)

    async def delete_from_cart(self, product_id: int, authorization: str = Header(None)):
        return self.__use_case.delete_from_cart(
            auth_header=authorization, product_id=product_id)

    async def create_review(self, body: ReviewCreateRequest, authorization: str = Header(None)):
        return self.__use_case.create_review(authorization, body.product_id, body.rate, body.text)

    async def delete_review(self, body: ReviewDeleteRequest, authorization: str = Header(None)):
        return self.__use_case.delete_review(authorization, body.product_id)

    async def search(self, body: SearchRequest):
        code, result = self.__use_case.search(body.__dict__)
        if code != status.HTTP_200_OK:
            raise HTTPException(status_code=code, detail=result['detail'])
        return result

    async def recommendations(self, count: int, authorization: str = Header(None)):
        return self.__use_case.recommend(authorization, count)

    # async def optimal_price(self, authorization: str = Header(None)):
    #     return self.__use_case.optimal_price(authorization)
