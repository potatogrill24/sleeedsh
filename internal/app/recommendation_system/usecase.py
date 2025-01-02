from internal.app.recommendation_system.repository import *
from ml.recommendation_system.model import RecommendationSystem


class RecommendationSystemUseCase:
    def __init__(self, recommendation_system: RecommendationSystem, repo: RecommendationSystemRepository):
        self.__recommendation_system = recommendation_system
        # self.__optimal_price = optimal_price
        self.__repo = repo

    def recommend_products(self, user_id: int, count: int):
        if user_id == 0:
            return self.__repo.get_most_popular(count)

        reviewed = self.__repo.get_user_products_reviewed(user_id)
        if not reviewed:
            return self.__repo.get_most_popular(count)

        ids = self.__recommendation_system.recommend_items(user_id, reviewed, count)
        return [item.__dict__ for item in self.__repo.get_products_by_ids(ids)]

    # def get_optimal_prices(self, shop_id: int):
    #     products = self.__repo.get_shop_products(shop_id)
    #     return self.__optimal_price.predict_optimal_price(products)
