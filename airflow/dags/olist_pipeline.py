from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

def run_ingestion():
    import subprocess
    result = subprocess.run(
        ['python', '/opt/ingestion/staging_script.py'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"Ingestion failed:\n{result.stderr}")
    print(result.stdout)

with DAG(
    dag_id='olist_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule= '@daily' ,    
    catchup=False,
    tags=['olist', 'snowflake', 'dbt']
) as dag:

    wait_for_s3 = S3KeySensor(
        task_id='wait_for_s3_files',
        bucket_name='olistdbbucket',
        bucket_key=[
            'raw/olist_customers_dataset.csv',
            'raw/olist_geolocation_dataset.csv',
            'raw/olist_order_items_dataset.csv',
            'raw/olist_order_payments_dataset.csv',
            'raw/olist_order_reviews_dataset.csv',
            'raw/olist_orders_dataset.csv',
            'raw/olist_products_dataset.csv',
            'raw/olist_sellers_dataset.csv',
            'raw/olist_product_category_translation_dataset.csv',
        ],
        aws_conn_id='aws_default',
        poke_interval=30,
        timeout=300,
        mode='reschedule'
    )
    

    ingestion = PythonOperator(
        task_id='run_ingestion',
        python_callable=run_ingestion
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/dbt && dbt run --profiles-dir /opt/dbt'
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/dbt && dbt test --profiles-dir /opt/dbt'
    )

    wait_for_s3 >> ingestion >> dbt_run >> dbt_test