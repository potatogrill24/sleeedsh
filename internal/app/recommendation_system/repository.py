from internal.domain.repository import ProductRepository, ReviewRepository
from internal.domain.model import Product


class RecommendationSystemRepository:
    def __init__(self, product_repository: ProductRepository, review_repository: ReviewRepository):
        self.__product_repository = product_repository
        self.__review_repository = review_repository

    def get_most_popular(self, n: int) -> list[Product]:
        return self.__product_repository.select_n_most_popular(n)

    def get_user_products_reviewed(self, user_id: int) -> list[int]:
        return [item.product_id for item in self.__review_repository.get_user_reviews(user_id)]

    def get_products_by_ids(self, ids: list[int]) -> list[Product]:
        return self.__product_repository.get_products_by_ids(ids)

    def get_shop_products(self, shop_id: int) -> list[Product]:
        return self.__product_repository.get_shop_products(shop_id)
