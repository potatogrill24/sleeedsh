from internal.config import load_config

from internal.app.order_management.handler import serve
from internal.app.order_management.usecase import OrderManagementUseCase
from internal.app.order_management.repository import OrderManagementRepository
from internal.domain.repository import ShoppingCartRepository
from internal.infrastructure.postgres import Database

if __name__ == '__main__':
    config = load_config()

    db = Database(
        f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@postgres:{config.POSTGRES_PORT}/{config.POSTGRES_DB}")

    carts = ShoppingCartRepository(db)
    repo = OrderManagementRepository(carts)
    use_case = OrderManagementUseCase(repo)
    serve(use_case, config.ORDER_MANAGEMENT_PORT)
