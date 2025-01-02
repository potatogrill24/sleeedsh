from dotenv import load_dotenv
import os


class Config:
    def __init__(self,
                 postgres_port: str,
                 postgres_db: str,
                 postgres_user: str,
                 postgres_password: str,
                 kafka_port: str,
                 redis_port: str,
                 jwt_secret_key: str,
                 session_time_in_secs: int,
                 authorization_port: str,
                 profile_port: str,
                 gateway_port: str,
                 order_management_port: str,
                 review_management_port: str,
                 search_port: str,
                 recommendation_system_port: str):
        self.POSTGRES_PORT = postgres_port
        self.POSTGRES_DB = postgres_db
        self.POSTGRES_USER = postgres_user
        self.POSTGRES_PASSWORD = postgres_password
        self.KAFKA_PORT = kafka_port
        self.REDIS_PORT = redis_port
        self.JWT_SECRET_KEY = jwt_secret_key
        self.SESSION_TIME_IN_SECS = session_time_in_secs
        self.AUTHORIZATION_PORT = authorization_port
        self.PROFILE_PORT = profile_port
        self.GATEWAY_PORT = gateway_port
        self.ORDER_MANAGEMENT_PORT = order_management_port
        self.REVIEW_MANAGEMENT_PORT = review_management_port
        self.SEARCH_PORT = search_port
        self.RECOMMENDATION_SYSTEM_PORT = recommendation_system_port


def load_config() -> Config:
    load_dotenv()
    return Config(postgres_port=os.getenv("POSTGRES_PORT"),
                  postgres_db=os.getenv("POSTGRES_DB"),
                  postgres_user=os.getenv("POSTGRES_USER"),
                  postgres_password=os.getenv("POSTGRES_PASSWORD"),
                  kafka_port=os.getenv("KAFKA_PORT"),
                  redis_port=os.getenv("REDIS_PORT"),
                  jwt_secret_key=os.getenv("JWT_SECRET_KEY"),
                  session_time_in_secs=int(os.getenv("SESSION_TIME_IN_SECS")),
                  authorization_port=os.getenv("AUTHORIZATION_PORT"),
                  profile_port=os.getenv("PROFILE_PORT"),
                  gateway_port=os.getenv("GATEWAY_PORT"),
                  order_management_port=os.getenv("ORDER_MANAGEMENT_PORT"),
                  review_management_port=os.getenv("REVIEW_MANAGEMENT_PORT"),
                  search_port=os.getenv("SEARCH_PORT"),
                  recommendation_system_port=os.getenv("RECOMMENDATION_SYSTEM_PORT"))
