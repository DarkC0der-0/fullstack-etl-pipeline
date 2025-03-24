import pandas as pd
from utils.redis_cache import cache_data

def extract_from_csv(file_path):
    data = pd.read_csv(file_path)
    cache_data('csv_data', data.to_dict())
    return data