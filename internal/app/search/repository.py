from internal.domain.repository import *


class SearchRepository:
    def __init__(self, db: Database):
        self.__product_repo = ProductRepository(db)

    def search(self, query: str) -> dict:
        products = self.__product_repo.search_products(query)
        return {
            "products": [item.__dict__ for item in products]
        }
    
    def get_all_products(self) -> dict:
        products = self.__product_repo.get_all_products()
        return {
            "products": [item.__dict__ for item in products]
        }