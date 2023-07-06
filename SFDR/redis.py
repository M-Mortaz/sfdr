import redis
from django.conf import settings

from notifier.designe_patterns.singleton import Singleton


class RedisClient(metaclass=Singleton):
    """
    Lazy and singleton Redis client
    """

    def __init__(self):
        self.pool = redis.ConnectionPool.from_url(url=settings.REDIS_URL)

    @property
    def conn(self):
        if not hasattr(self, '_conn'):
            self.get_connection()
        return self._conn

    def get_connection(self):
        self._conn = redis.Redis(connection_pool=self.pool, decode_responses=True)


redis_client = RedisClient()
