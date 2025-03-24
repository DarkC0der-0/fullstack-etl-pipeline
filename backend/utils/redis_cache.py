import redis
from utils.config import REDIS_URL

redis_client = redis.StrictRedis.from_url(REDIS_URL)

def cache_data(key, data):
    redis_client.set(key, data)

def get_cached_data(key):
    return redis_client.get(key)

def publish_message(channel, message):
    redis_client.publish(channel, message)