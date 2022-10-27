from queue import Empty
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
from pandas.io import sql


AWS_ACCESS_KEY_ID = Variable.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = Variable.get("AWS_SECRET_ACCESS_KEY")

logger = logging.getLogger("write_twitter_df")
bucket_name = "databoys"
region = "us-east-1"

default_args = {
    "owner": "Joao Victor, Nicholas Baraldi",
    "retries": 5,
    "return_delay": timedelta(minutes=10),
}

def drop_table():
    engine = create_engine(
        "postgresql://username:password@host.docker.internal:5432/dbt_db"
    )
    sql.execute('DROP TABLE IF EXISTS tweets CASCADE', engine)
    sql.execute('DROP TABLE IF EXISTS users CASCADE', engine)

def tweets_to_warehouse():
    df_list = []
    logger.info("Second task Initialized")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=region,
    )
    logger.info("msg=client created")
    paginator = s3.get_paginator('list_objects_v2')
    result = paginator.paginate(Bucket='databoys', StartAfter = "Trusted/tweets_json.json/")
    for page in result:
        if "Contents" in page:
            for key in page["Contents"]:
                keyString = key["Key"]
                if "tweets_json.json" in keyString:
                    obj = s3.get_object(Bucket=bucket_name, Key=keyString)
                    initial_df = pd.read_json(obj["Body"], lines=True)
                    df_list.append(initial_df)
    final_df = pd.concat(df_list)
    logger.info("msg=Dataframe Created")
    engine = create_engine(
        "postgresql://username:password@host.docker.internal:5432/dbt_db"
    )
    final_df.to_sql("tweets", engine, if_exists = 'replace')

def users_to_warehouse():
    df_list = []
    logger.info("Second task Initialized")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=region,
    )
    logger.info("msg=client created")
    paginator = s3.get_paginator('list_objects_v2')
    result = paginator.paginate(Bucket='databoys', StartAfter = "Trusted/users_json.json/")
    for page in result:
        if "Contents" in page:
            for key in page["Contents"]:
                keyString = key["Key"]
                if "users_json.json" in keyString:
                    print(keyString)
                    obj = s3.get_object(Bucket=bucket_name, Key=keyString)
                    initial_df = pd.read_json(obj["Body"], lines=True)
                    df_list.append(initial_df)
    final_df = pd.concat(df_list)
    logger.info("msg=Dataframe Created")
    print(final_df)
    engine = create_engine(
        "postgresql://username:password@host.docker.internal:5432/dbt_db"
    )
    final_df.to_sql("users", engine, if_exists = 'replace')


with DAG(
    "s3_to_postgres_dw",
    default_args=default_args,
    start_date=datetime(2022, 9, 30),
    schedule_interval="0 21 * * 0",
    catchup=False,
) as dag:

    tweets_to_warehouse = PythonOperator(
        task_id="tweets_to_warehouse", python_callable=tweets_to_warehouse
    )    

    users_to_warehouse = PythonOperator(
        task_id="users_to_warehouse", python_callable=users_to_warehouse
    ) 

    drop_table = PythonOperator(
       task_id="drop_table", python_callable=drop_table 
    )   

drop_table >> [tweets_to_warehouse, users_to_warehouse]