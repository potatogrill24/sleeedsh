from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


class DatabaseError(Exception):
    pass


class NotFoundError(Exception):
    pass


class MultipleResultsFoundError(Exception):
    pass


class Database:
    def __init__(self, db_url: str, pool_size: int = 5, max_overflow: int = 10, pool_timeout: int = 30):
        self.engine: Engine = create_engine(
            db_url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout
        )

    def query(self, query: str, params: dict = None) -> list:
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params)
                return [row._asdict() for row in result]
        except SQLAlchemyError:
            raise DatabaseError

    def query_row(self, query: str, params: dict = None) -> dict:
        result = self.query(query, params)
        if len(result) == 0:
            raise NotFoundError("No row was found.")
        elif len(result) > 1:
            raise MultipleResultsFoundError("Multiple rows were found.")
        return result[0]

    def execute(self, query: str, params: dict = None):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params)
                connection.commit()
                return result.rowcount
        except SQLAlchemyError:
            raise DatabaseError

    def transaction(self, queries: list, level: str = None):
        try:
            with self.engine.connect() as connection:
                if level:
                    connection.execution_options(isolation_level=level)

                with connection.begin():
                    for query, params in queries:
                        connection.execute(text(query), params)
        except SQLAlchemyError:
            raise DatabaseError("Transaction failed.")

    def close(self):
        self.engine.dispose()

    def __del__(self):
        self.engine.dispose()
