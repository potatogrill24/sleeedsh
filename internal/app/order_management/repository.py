from internal.domain.repository import ShoppingCartRepository


class OrderManagementRepository:
    def __init__(self, shopping_carts: ShoppingCartRepository):
        self.__shopping_carts = shopping_carts

    def add_to_cart(self, user_id: int, product_id: int):
        self.__shopping_carts.add_product_to_cart(user_id, product_id)

    def delete_from_cart(self, user_id: int, product_id: int):
        self.__shopping_carts.drop_product_from_users_cart(user_id, product_id)
