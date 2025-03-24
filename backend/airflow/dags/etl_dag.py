from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from extract.data_extractor import DataExtractor
from transform.data_transformer import DataTransformer
from load.postgres_loader import bulk_insert_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='An ETL pipeline for extracting, transforming, and loading data',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    tags=['etl'],
)

def extract_data(**kwargs):
    extractor = DataExtractor()
    api_data = extractor.extract_from_api("https://api.example.com/data")
    csv_data = extractor.extract_from_csv("/path/to/local/file.csv")
    s3_data = extractor.extract_from_s3("bucket-name", "path/to/s3/file.csv")
    return api_data, csv_data, s3_data

def transform_data(**kwargs):
    ti = kwargs['ti']
    api_data, csv_data, s3_data = ti.xcom_pull(task_ids='extract_data')
    transformer = DataTransformer(reference_data_path="/path/to/reference.csv", reference_api_url="https://api.example.com/data")
    transformed_data = []
    for data in [api_data, csv_data, s3_data]:
        if data is not None:
            cleaned_data = transformer.clean_data(data)
            filtered_data = transformer.filter_data(cleaned_data, "column_name > 0")
            enriched_data = transformer.enrich_data(filtered_data)
            transformed_data.append(enriched_data)
    return transformed_data

def load_data(**kwargs):
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(task_ids='transform_data')
    for data in transformed_data:
        if data is not None:
            bulk_insert_data(data)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

extract_task >> transform_task >> load_task