from fastapi import FastAPI
import uvicorn

from internal.config import *
from internal.infrastructure.postgres import Database
from internal.domain.repository import UserRepository, ShopRepository, ShoppingCartRepository, PaycheckRepository, \
    ProductRepository, ReviewRepository

from internal.app.profile.repository import ProfileRepository
from internal.app.profile.usecase import ProfileUseCase
from internal.app.profile.handler import ProfileHandler

app = FastAPI()

if __name__ == '__main__':
    config = load_config()

    db = Database(
        f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@postgres:{config.POSTGRES_PORT}/{config.POSTGRES_DB}")

    shop_repository = ShopRepository(db)
    user_repository = UserRepository(db)
    cart_repository = ShoppingCartRepository(db)
    paycheck_repository = PaycheckRepository(db)
    product_repository = ProductRepository(db)
    review_repository = ReviewRepository(db)

    repo = ProfileRepository(
        user_repository=user_repository,
        shop_repository=shop_repository,
        cart_repository=cart_repository,
        paycheck_repository=paycheck_repository,
        product_repository=product_repository,
        review_repository=review_repository)
    use_case = ProfileUseCase(repository=repo)
    handler = ProfileHandler(use_case=use_case)

    app.include_router(handler.router)
    uvicorn.run(app, port=int(config.PROFILE_PORT), host="0.0.0.0")
