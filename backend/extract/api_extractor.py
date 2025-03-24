import requests
from utils.redis_cache import cache_data

def extract_from_api(api_url):
    response = requests.get(api_url)
    data = response.json()
    cache_data('api_data', data)
    return data