import multiprocessing as mp
import requests
import pandas as pd
from transform.data_transformer import DataTransformer
from load.postgres_loader import bulk_insert_data
from utils.redis_cache import cache_data, get_cached_data

def extract_data(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

def transform_data(data):
    transformer = DataTransformer()
    cleaned_data = transformer.clean_data(data)
    filtered_data = transformer.filter_data(cleaned_data, "column_name > 0")
    enriched_data = transformer.enrich_data(filtered_data)
    return enriched_data

def parallel_process(func, data, num_processes):
    pool = mp.Pool(num_processes)
    result = pool.map(func, data)
    pool.close()
    pool.join()
    return result

def etl_pipeline(api_urls):
    # Extract data in parallel
    extracted_data = parallel_process(extract_data, api_urls, num_processes=mp.cpu_count())

    # Transform data in parallel
    transformed_data = parallel_process(transform_data, extracted_data, num_processes=mp.cpu_count())

    # Load data into the database
    for data in transformed_data:
        bulk_insert_data(data)

if __name__ == "__main__":
    api_urls = ["https://api.example.com/data1", "https://api.example.com/data2"]
    etl_pipeline(api_urls)