import redis as rd


class RedisClient:
    def __init__(self, host: str, port: int, db: int):
        self.__redis = rd.Redis(host=host, port=port, db=db)

    def set(self, name, value, expiration_time):
        return self.__redis.set(name=name, value=value, ex=expiration_time)

    def get(self, name):
        return self.__redis.get(name=name)

    def delete(self, names):
        return self.__redis.delete(*names)

    def __del__(self):
        return self.__redis.close()
