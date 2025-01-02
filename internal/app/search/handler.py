from fastapi import APIRouter
from pydantic import BaseModel

from internal.app.search.usecase import *


class SearchRequest(BaseModel):
    query: str


class SearchHandler:
    def __init__(self, use_case: SearchUseCase):
        self.router = APIRouter()
        self.use_case = use_case

        self.router.add_api_route("/search", self.search, methods=["POST"])

    async def search(self, request: SearchRequest):
        return self.use_case.search(request.query)
