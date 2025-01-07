from internal.app.search.repository import *


class SearchUseCase:
    def __init__(self, repository: SearchRepository):
        self.repository = repository

    def search(self, query: str) -> dict:
        if not query:
            return {}

        query_like = query.strip().replace(" ", "%")

        return self.repository.search(query_like)
    
    def get_all_products(self) -> dict:
        return self.repository.get_all_products()