from airflow import DAG
from airflow.operatir.python import PythonOperator 
from datetime import datetime
from twitter_api.twitter_client.twitter_search import Twitter

def create_spark_client:


def read_twitter_df:


    
with DAG(
    'ingest_twitter', 
    start_date = datetime(2022,9,30), 
    schedule_interval = '0 21 * * 0', 
    catchup = False) as dag:

create_spark_client = PythonOperator(
    task_id = 'create_spark_client'

)

read_twitter_df = PythonOperator(
    task_id = 'read_twitter_df'

)