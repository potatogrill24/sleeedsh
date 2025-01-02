from internal.app.order_management.repository import OrderManagementRepository


class OrderManagementUseCase:
    def __init__(self, repo: OrderManagementRepository):
        self.__repo = repo

    async def add_to_cart(self, user_id: int, product_id: int):
        self.__repo.add_to_cart(user_id, product_id)

    async def delete_from_cart(self, user_id: int, product_id: int):
        self.__repo.delete_from_cart(user_id, product_id)
