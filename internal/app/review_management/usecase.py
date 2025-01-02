from internal.app.review_management.repository import *


class ReviewManagementUseCase:
    def __init__(self, repo: ReviewManagementRepository):
        self.__repo = repo

    async def create_review(self, user_id: int, product_id: int, rate: float, text: str):
        if not self.__repo.check_if_review_is_valid(user_id, product_id):
            return

        self.__repo.create_review(user_id, product_id, rate, text)

    async def delete_review(self, user_id: int, product_id: int):
        self.__repo.delete_review(user_id, product_id)
