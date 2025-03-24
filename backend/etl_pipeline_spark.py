from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from transform.data_transformer import DataTransformer
from load.postgres_loader import bulk_insert_data

spark = SparkSession.builder.appName("ETL Pipeline").getOrCreate()

def extract_data(api_url):
    df = spark.read.json(api_url)
    return df

def transform_data(df):
    transformer = DataTransformer()
    cleaned_df = transformer.clean_data(df)
    filtered_df = transformer.filter_data(cleaned_df, col("column_name") > 0)
    enriched_df = transformer.enrich_data(filtered_df)
    return enriched_df

def etl_pipeline(api_urls):
    for api_url in api_urls:
        df = extract_data(api_url)
        transformed_df = transform_data(df)
        transformed_data = transformed_df.collect()
        bulk_insert_data(transformed_data)

if __name__ == "__main__":
    api_urls = ["https://api.example.com/data1", "https://api.example.com/data2"]
    etl_pipeline(api_urls)