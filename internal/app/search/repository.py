from internal.domain.repository import *


class SearchRepository:
    def __init__(self, db: Database):
        self.__shop_repo = ShopRepository(db)
        self.__product_repo = ProductRepository(db)

    def search(self, query: str) -> dict:
        shops = self.__shop_repo.search_shops(query)
        products = self.__product_repo.search_products(query)
        return {
            "shops": [item.__dict__ for item in shops],
            "products": [item.__dict__ for item in products]
        }
