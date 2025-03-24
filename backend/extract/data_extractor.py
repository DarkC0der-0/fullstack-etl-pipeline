import requests
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from utils.redis_cache import cache_data

class DataExtractor:
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def extract_from_api(self, api_url, params=None, headers=None):
        try:
            response = requests.get(api_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            cache_data('api_data', data)
            return data
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None

    def extract_from_csv(self, file_path):
        try:
            data = pd.read_csv(file_path, chunksize=10000)
            for chunk in data:
                cache_data('csv_data_chunk', chunk.to_dict())
            return data
        except FileNotFoundError as e:
            print(f"CSV file not found: {e}")
            return None

    def extract_from_s3(self, bucket_name, file_key):
        try:
            obj = self.s3_client.get_object(Bucket=bucket_name, Key=file_key)
            data = pd.read_csv(obj['Body'], chunksize=10000)
            for chunk in data:
                cache_data('s3_csv_data_chunk', chunk.to_dict())
            return data
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"S3 credentials error: {e}")
            return None
        except self.s3_client.exceptions.NoSuchKey as e:
            print(f"S3 file not found: {e}")
            return None

# Example usage
if __name__ == "__main__":
    extractor = DataExtractor()

    # Extract from API
    api_data = extractor.extract_from_api("https://api.example.com/data")
    if api_data:
        print("API Data Extracted Successfully")

    # Extract from local CSV
    csv_data = extractor.extract_from_csv("path/to/local/file.csv")
    if csv_data:
        print("Local CSV Data Extracted Successfully")

    # Extract from S3
    s3_data = extractor.extract_from_s3("bucket-name", "path/to/s3/file.csv")
    if s3_data:
        print("S3 CSV Data Extracted Successfully")