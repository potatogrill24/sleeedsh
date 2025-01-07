from fastapi import FastAPI
import uvicorn

from internal.config import load_config
from internal.infrastructure.kafka import Producer

from internal.app.gateway.usecase import GatewayUseCase
from internal.app.gateway.handler import GatewayHandler

app = FastAPI()

if __name__ == '__main__':
    config = load_config()

    producer = Producer(f"kafka:{config.KAFKA_PORT}", 'producer', "all", 5)

    use_case = GatewayUseCase(
        producer, config.AUTHORIZATION_PORT, config.PROFILE_PORT, config.ORDER_MANAGEMENT_PORT, config.REVIEW_MANAGEMENT_PORT, config.SEARCH_PORT, config.RECOMMENDATION_SYSTEM_PORT)
    handler = GatewayHandler(use_case)

    app.include_router(handler.router)
    uvicorn.run(app, port=int(config.GATEWAY_PORT), host="0.0.0.0")
