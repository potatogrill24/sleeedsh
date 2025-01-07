from fastapi import FastAPI
import uvicorn

from internal.config import load_config
from internal.infrastructure.postgres import Database
from internal.app.search.repository import SearchRepository
from internal.app.search.usecase import SearchUseCase
from internal.app.search.handler import SearchHandler

app = FastAPI()

if __name__ == "__main__":
    config = load_config()

    db = Database(
        f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@postgres:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
    )

    repository = SearchRepository(db)
    use_case = SearchUseCase(repository)
    handler = SearchHandler(use_case)

    app.include_router(handler.router)

    uvicorn.run(app, host="0.0.0.0", port=int(config.SEARCH_PORT))