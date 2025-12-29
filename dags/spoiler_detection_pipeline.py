from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

# Script klasörünü tanıtalım
sys.path.append('/opt/airflow/scripts')
from data_operations import load_json_to_postgres
from model_inference import run_inference
from simulator import simulate_new_reviews

with DAG(
    'spoiler_detection_pipeline',
    start_date=datetime(2025, 1, 1),
    schedule_interval='*/1 * * * *',
    catchup=False
) as dag:
    
    t0 = PythonOperator(
        task_id='simulate_incoming_data',
        python_callable=simulate_new_reviews
    )
    # 1. Tabloyu oluştur
    t1 = PostgresOperator(
        task_id='alter_table_add_prediction',
        postgres_conn_id='postgres_default',
        sql="ALTER TABLE movie_reviews ADD COLUMN IF NOT EXISTS model_prediction INTEGER;"
    )

    # 2. Veriyi JSON'dan al DB'ye yaz
    t2 = PythonOperator(
        task_id='load_data_to_db',
        python_callable=load_json_to_postgres
    )

    t3 = PythonOperator(
        task_id='predict_spoilers',
        python_callable=run_inference
    )

    # Akış: Önce tablo oluşsun, sonra veri yüklensin
    t0 >> t1 >> t3