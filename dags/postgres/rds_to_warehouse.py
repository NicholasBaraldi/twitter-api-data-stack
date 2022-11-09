import re
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pyspark.sql.types import *
from airflow.models import Variable
from datetime import timedelta
import boto3
import logging
import pandas as pd
from sqlalchemy import create_engine


AWS_ACCESS_KEY_ID = Variable.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = Variable.get("AWS_SECRET_ACCESS_KEY")

logger = logging.getLogger("write_twitter_df")
bucket_name = "databoys"
region = "us-east-1"

default_args = {
    "owner": "Joao Victor, Nicholas Baraldi",
    "retries": 5,
    "retryu_delay": timedelta(minutes=10),
}


def rds_to_warehouse():
    file_name = "Trusted/Postgresql/movies_2022-10-09.csv"
    logger.info("First task Initialized")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=region,
    )
    logger.info("msg=client created")
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    logger.info("msg=object obtained")
    initial_df = pd.read_csv(obj["Body"])
    logger.info("msg=Dataframe Created")
    engine = create_engine(
        "postgresql://username:password@host.docker.internal:5432/postgres"
    )
    initial_df.to_sql("movies", engine)

with DAG(
    "s3_to_warehouse",
    default_args=default_args,
    start_date=datetime(2022, 9, 30),
    schedule_interval="0 21 * * 0",
    catchup=False,
) as dag:

    rds_to_warehouse = PythonOperator(
        task_id="rds_to_warehouse", python_callable=rds_to_warehouse
    )