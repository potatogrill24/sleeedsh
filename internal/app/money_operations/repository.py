from internal.domain.repository import UserRepository, ShoppingCartRepository


class MoneyOperationsRepository:
    def __init__(self, user_repository: UserRepository, shopping_cart_repository: ShoppingCartRepository):
        self.__user_repository = user_repository
        # self.__paycheck_repository = paycheck_repository
        self.__shopping_cart_repository = shopping_cart_repository
        # self.__product_repository = product_repository

    def deposit(self, user_id: int, to_add: int):
        self.__user_repository.change_balance(user_id, to_add)

    def buy_cart(self, user_id: int):
        if not self.__shopping_cart_repository.get_shopping_cart_size(user_id):
            return
        self.__shopping_cart_repository.buy_cart(user_id)

    # def buy_shopping_cart(self, user: User):
    #     # todo: transaction
    #     user_id = self.__user_repository.get_id_by_login(user.id)
    #     product_ids = self.__shopping_cart_repository.get_users_products(
    #         user_id)
    #     cart_price = self.__product_repository.get_products_price_sum(
    #         product_ids)

    #     if cart_price > user.balance:
    #         raise ValueError("not enough money on balance")

    #     self.__paycheck_repository.add_paycheck_for_user(user_id, product_ids)
