from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, date
from twitter_api.twitter_client.twitter_search import Twitter
from pyspark.sql import SparkSession
import os
import logging


logger = logging.getLogger("write_twitter_df")
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark_session = SparkSession.builder.config(
        "spark.jars.packages", "org.apache.hadoop:hadoop-common:3.3.3,org.apache.hadoop:hadoop-client:3.3.3,org.apache.hadoop:hadoop-aws:3.3.3"
    ).getOrCreate()
    return spark_session


def write_twitter_df():
    spark = create_spark_session()
    bucket_name = "databoys"
    file_name_tweet = "tweets_json.json"
    file_name_user = "tweets_json.json"
    t = Twitter()
    query = "#HouseOfTheDragon"
    ntweet = 100
    nreq = 200
    tweets, users = t.make_req(query, ntweet, nreq)
    spark_tweets_df = spark.createDataFrame(data=tweets)
    spark_users_df = spark.createDataFrame(data=users)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", AWS_ACCESS_KEY_ID)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
    spark_tweets_df.write.json(f"s3a://{bucket_name}/Raw/{date.today()}/{file_name_tweet}")
    spark_tweets_df.write.json(f"s3a://{bucket_name}/Raw/{date.today()}/{file_name_user}")
    logger.info("msg=DataFrame Written")
    if spark_tweets_df:
        return 1
    return 0

def raw_to_trusted():
    success = 
    if success == 1:
        spark = create_spark_session()
        bucket_name = "databoys"
        file_name = "tweets_json.json"
        spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", AWS_ACCESS_KEY_ID)
        spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
        tweet = spark.read.json(f"s3a://{bucket_name}/Raw/{date.today()}/{file_name}")
        tweet.write.mode('append').parquet(f"s3a://{bucket_name}/Trusted/{date.today()}/{file_name}")
    else:
        logger.info("msg=Error")


with DAG(
    "ingest_twitter",
    start_date=datetime(2022, 9, 30),
    schedule_interval="0 21 * * 0",
    catchup=False,
) as dag:
    write_twitter_df = PythonOperator(
        task_id="write_twitter_df", python_callable=write_twitter_df
    )
    raw_to_trusted = PythonOperator(
        task_id="raw_to_trusted", python_callable=raw_to_trusted
    )

write_twitter_df > raw_to_trusted