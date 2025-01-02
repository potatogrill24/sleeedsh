from internal.app.review_management.repository import ReviewManagementRepository
from internal.app.review_management.usecase import ReviewManagementUseCase
from internal.config import load_config
from internal.domain.repository import ReviewRepository, PaycheckRepository
from internal.infrastructure.postgres import Database
from internal.app.review_management.handler import serve

if __name__ == '__main__':
    config = load_config()

    db = Database(
        f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@postgres:{config.POSTGRES_PORT}/{config.POSTGRES_DB}")

    reviews = ReviewRepository(db)
    paychecks = PaycheckRepository(db)

    repo = ReviewManagementRepository(reviews, paychecks)
    use_case = ReviewManagementUseCase(repo)
    serve(use_case, config.REVIEW_MANAGEMENT_PORT)
