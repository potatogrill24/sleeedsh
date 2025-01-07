from internal.domain.repository import ReviewRepository, PaycheckRepository


class ReviewManagementRepository:
    def __init__(self, review_repository: ReviewRepository, paycheck_repository: PaycheckRepository):
        self.__review_repository = review_repository
        self.__paycheck_repository = paycheck_repository

    def create_review(self, user_id: int, product_id: int, rate: float, text: str):
        self.__review_repository.create_review(user_id, product_id, rate, text)

    def check_if_review_is_valid(self, user_id: int, product_id: int):
        return self.__paycheck_repository.check_if_bought(user_id, product_id) and not self.__review_repository.check_if_reviewed(user_id, product_id)

    def delete_review(self, user_id: int, product_id: int):
        self.__review_repository.delete_review(user_id, product_id)
