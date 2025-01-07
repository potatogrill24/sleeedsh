from internal.config import *
from internal.infrastructure.postgres import Database

from internal.app.money_operations.handler import *


if __name__ == '__main__':
    # try:
    config = load_config()

    db = Database(
        f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@postgres:{config.POSTGRES_PORT}/{config.POSTGRES_DB}")

    user_repository = UserRepository(db)
    shopping_cart_repository = ShoppingCartRepository(db)
    repository = MoneyOperationsRepository(
        user_repository, shopping_cart_repository)
    use_case = MoneyOperationsUseCase(repository)

    consumer = Consumer(f"kafka:{config.KAFKA_PORT}", 'group')
    consumer.subscribe(['money_operations'])
    handler = MoneyOperationsHandler(use_case=use_case, consumer=consumer)

    handler.consume()

    # except Exception as e:
    #     print('error: unable to establish the server: ', str(e))
