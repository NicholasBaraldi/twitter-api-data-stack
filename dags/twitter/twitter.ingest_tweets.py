from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from twitter_api.twitter_client.twitter_search import Twitter
from pyspark.sql import SparkSession


def create_spark_session():
    spark_session = SparkSession.builder.config(
        "spark.jars.packages", "com.amazonaws:aws-java-sdk-bundle:1.12.314"
    ).getOrCreate()
    return spark_session


def write_twitter_df():
    spark = create_spark_session()
    bucket_name = "databoys"
    file_name = "tweets_json.json"
    t = Twitter()
    query = "#HouseOfTheDragon"
    ntweet = 100
    nreq = 200
    tweets, users = t.make_req(query, ntweet, nreq)
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
    write_twitter_df = PythonOperator(
        task_id="write_twitter_df", python_callable=write_twitter_df
    )

write_twitter_df
