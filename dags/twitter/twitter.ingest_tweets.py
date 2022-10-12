from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, date
from twitter_api.twitter_client.twitter_search import Twitter
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from airflow.models import Variable
# from airflow.providers.amazon.aws.operators.redshift import RedshiftSQLOperator
import logging
import os

# os.environ['PYSPARK_SUBMIT_ARGS'] = "--master spark://localhost:8888"

AWS_ACCESS_KEY_ID = Variable.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = Variable.get("AWS_SECRET_ACCESS_KEY")
bearer_token = Variable.get("Bearer Token")

logger = logging.getLogger("write_twitter_df")



def create_spark_session():
    spark_session = SparkSession.builder.config(
        "spark.jars.packages",
        "org.apache.hadoop:hadoop-common:3.3.3,org.apache.hadoop:hadoop-client:3.3.3,org.apache.hadoop:hadoop-aws:3.3.3",
    ).master("local[*]").getOrCreate()
    return spark_session


def write_twitter_df():
    print(os.environ['JAVA_HOME'])
    logger.info("JAVA_HOME")
    spark = create_spark_session()
    bucket_name = "databoys"
    file_name_tweet = "tweets_json.json"
    file_name_user = "tweets_json.json"
    t = Twitter(bearer_token)
    query = "#HouseOfTheDragon"
    ntweet = 100
    nreq = 2
    tweets, users = t.make_req(query, ntweet, nreq)
    logger.info("msg=API Returned")
    print(tweets)
    print(users)
    schema_tweets=StructType([
    StructField('author_id', StringType(), True),
    StructField('created_at',StringType(), True),
    StructField('edit_history_tweet_ids',StringType(), True),
    StructField('id',StringType(), True),
    StructField('text',StringType(), True)

])
    spark_tweets_df = spark.createDataFrame(data=tweets, schema=schema_tweets)
    logger.info("msg=spark_tweets_df Created")
    # schema_users="description str, id int, name str, username str"
    # spark_users_df = spark.createDataFrame(data=users, schema=schema_users)
    # logger.info("msg=spark_users_df Created")
    spark.sparkContext._jsc.hadoopConfiguration().set(
        "fs.s3a.access.key", AWS_ACCESS_KEY_ID
    )
    spark.sparkContext._jsc.hadoopConfiguration().set(
        "fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY
    )
    logger.info("msg=AWS Keys Set")
    spark_tweets_df.write.json(
        f"s3a://{bucket_name}/Raw/{date.today()}/{file_name_tweet}"
    )
    logger.info("msg=spark_tweets_df Written")
    # spark_users_df.write.json(
    #     f"s3a://{bucket_name}/Raw/{date.today()}/{file_name_user}"
    # )
    # logger.info("msg=spark_users_df Written")
    logger.info("msg=task Successful")
    if spark_tweets_df: #and spark_users_df:
        return 1
    return 0


# def raw_to_trusted():
#     file_name_tweet = "tweets_json.json"
#     file_name_user = "tweets_json.json"
#     # success = ti.xcom_pull(task_ids="write_twitter_df")
#     if success == 1:
#         spark = SparkSession.builder.config(
#         "spark.jars.packages",
#         "org.apache.hadoop:hadoop-common:3.3.3,org.apache.hadoop:hadoop-client:3.3.3,org.apache.hadoop:hadoop-aws:3.3.3",
#         ).master("local[*]").getOrCreate()
#         bucket_name = "databoys"
#         spark.sparkContext._jsc.hadoopConfiguration().set(
#             "fs.s3a.access.key", AWS_ACCESS_KEY_ID
#         )
#         spark.sparkContext._jsc.hadoopConfiguration().set(
#             "fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY
#         )
#         tweet = spark.read.json(
#             f"s3a://{bucket_name}/Raw/{date.today()}/{file_name_tweet}"
#         )
#         users = spark.read.json(
#             f"s3a://{bucket_name}/Raw/{date.today()}/{file_name_user}"
#         )
#         try:
#             x = spark.read.json(f"s3a://{bucket_name}/Trusted/{file_name_tweet}")
#             y = spark.read.json(f"s3a://{bucket_name}/Trusted/{file_name_user}")
#         except:
#             x = 0
#             y = 0
#         if x == 0 and y == 0:
#             tweet.write.mode("append").json(
#                 f"s3a://{bucket_name}/Trusted/{file_name_tweet}"
#             )
#             users.write.mode("append").json(
#                 f"s3a://{bucket_name}/Trusted/{file_name_user}"
#             )
#         else:
#             tweet.write.json(f"s3a://{bucket_name}/Trusted/{file_name_tweet}")
#             users.write.json(f"s3a://{bucket_name}/Trusted/{file_name_user}")
#     else:
#         logger.info("msg=Error")
#     return


with DAG(
    "ingest_twitter",
    start_date=datetime(2022, 9, 30),
    schedule_interval="0 21 * * 0",
    catchup=False,
) as dag:

    write_twitter_df = PythonOperator(
        task_id="write_twitter_df", python_callable=write_twitter_df
    )
    # raw_to_trusted = PythonOperator(
    #     task_id="raw_to_trusted", python_callable=raw_to_trusted
    # )

write_twitter_df # >> raw_to_trusted
