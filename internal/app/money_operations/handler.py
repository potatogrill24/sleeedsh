import json

from internal.app.money_operations.usecase import *
from internal.infrastructure.kafka import Consumer, consume_messages


class MoneyOperationsHandler:
    def __init__(self, use_case: MoneyOperationsUseCase, consumer: Consumer):
        self.__use_case = use_case
        self.__consumer = consumer

    def deposit(self, data: dict):
        if 'userID' not in data or 'diff' not in data:
            return
        self.__use_case.add_money_to_user(
            user_id=data['userID'], to_add=data['diff'])

    def buy(self, data: dict):
        if 'userID' not in data:
            return

        self.__use_case.buy_cart(user_id=data['userID'])

    def fork_messages(self, msg: str):
        data = json.loads(msg)
        if 'type' not in data:
            return

        if data['type'] == 'deposit':
            self.deposit(data)
        elif data['type'] == 'buy':
            self.buy(data)

    def consume(self):
        consume_messages(self.__consumer, self.fork_messages, print, print)
