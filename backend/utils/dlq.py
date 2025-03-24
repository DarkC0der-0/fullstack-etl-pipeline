import redis
from utils.config import REDIS_URL

redis_client = redis.StrictRedis.from_url(REDIS_URL)

def add_to_dlq(record, reason):
    redis_client.rpush('dlq', {'record': record, 'reason': reason})

def get_dlq():
    return [redis_client.lindex('dlq', i) for i in range(redis_client.llen('dlq'))]