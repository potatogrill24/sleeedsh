from fastapi import APIRouter

from internal.app.recommendation_system.usecase import RecommendationSystemUseCase


class RecommendationSystemHandler:
    def __init__(self, use_case: RecommendationSystemUseCase):
        self.__use_case = use_case
        self.router = APIRouter()

        self.router.add_api_route(
            "/recommend/{user_id}", self.recommend, methods=["GET"])
        # self.router.add_api_route(
        #     "/optimal_price/{shop_id}", self.optimal_price, methods=["GET"])

    async def recommend(self, user_id: int, count: str = None):
        count = int(count) if count is not None else 10
        return self.__use_case.recommend_products(user_id, count)

    # async def optimal_price(self, shop_id: int):
    #     return self.__use_case.get_optimal_prices(shop_id)
