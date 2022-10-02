from airflow import DAG
from airflow.operatr.python import PythonOperator
from datetime import datetime
from twitter_api.twitter_client.twitter_search import Twitter
from pyspark.sql import SparkSession


def create_spark_session():
    spark_session = SparkSession.builder.getOrCreate()
    return spark_session


def read_twitter_df():
    spark = create_spark_session()
    bucket_name = "databoys"
    file_name = "tweets_json"
    t = Twitter()
    query = "#HouseOfTheDragon"
    ntweet = 100
    nreq = 200
    tweets = t.make_req(query, ntweet, nreq)
    spark_tweets_df = spark.createDataFrame(data=tweets)
    spark_tweets_df.write.json(f"s3a://{bucket_name}/Raw/{file_name}")
    if tweets:
        return 1
    return 0


with DAG(
    "ingest_twitter",
    start_date=datetime(2022, 9, 30),
    schedule_interval="0 21 * * 0",
    catchup=False,
) as dag:
    pass
