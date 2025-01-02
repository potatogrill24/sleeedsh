import jwt

from internal.app.money_operations.repository import *


class MoneyOperationsUseCase:
    def __init__(self, repository: MoneyOperationsRepository):
        self.__repository = repository

    def add_money_to_user(self, user_id: int, to_add: int):
        self.__repository.deposit(user_id, to_add)

    def buy_cart(self, user_id: int):
        self.__repository.buy_cart(user_id)
