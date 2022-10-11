from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import date, datetime, timedelta
from pyspark.sql import SparkSession
from airflow.models import Variable
from airflow.providers.amazon.aws.operators.redshift import RedshiftSQLOperator
import logging
import csv

default_args = {
    'owner': 'Joao Victor',
    'retries': 5,
    'retryu_delay': timedelta(minutes=10)
}
AWS_ACCESS_KEY_ID = Variable.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = Variable.get("AWS_SECRET_ACCESS_KEY")

logger = logging.getLogger("write_twitter_df")


def postgres_to_s3():
    psql_hook = PostgresHook(postgres_conn_id = "RDS")
    psql_conn = psql_hook.get_conn()
    cursor = psql_conn.cursor()
    cursor.execute("select * from movies")
    with open(f"dags/data/movies_{date.today()}.csv", "w") as f:
        csv_wirter = csv.writer(f)
        csv_wirter.writerow([i[0] for i in cursor.description])
        csv_wirter.writerows(cursor)
    cursor.close()
    psql_conn.close()
    logging.info("Saved table movies in DB")
    s3_hook = S3Hook(aws_conn_id="my_conn_S3") 
    s3_hook.load_file(
        filename= f"dags/data/movies_{date.today()}.csv",
        key=f"Raw/Postgresql/movies_{date.today()}.csv",
        bucket_name="databoys",
        replace = True
    )
    logging.info("Saved csv on S3")
     
def raw_to_trusted():
    s3_hook = S3Hook(aws_conn_id="my_conn_S3")
    logging.info("Connection Successful")
    s3_hook.copy_object(
        source_bucket_key=f"s3://databoys/Raw/Postgresql/movies_{date.today()}.csv",
        dest_bucket_key=f"s3://databoys/Trusted/Postgresql/movies_{date.today()}.csv",
    )
    logging.info("Saved csv on Trusted")


with DAG(
    "postgres_to_s3",
    default_args=default_args,
    start_date=datetime(2022, 9, 30),
    schedule_interval="0 21 * * 0",
    catchup=False,
) as dag:

    postgres_to_s3 = PythonOperator(
        task_id="postgres_to_s3", python_callable=postgres_to_s3
    )
    
    raw_to_trusted = PythonOperator(
        task_id="raw_to_trusted", python_callable=raw_to_trusted
    )
    
    setup__task_create_table = RedshiftSQLOperator(
        task_id='setup__create_table',
        redshift_conn_id = 'jfc',
        sql="""
            CREATE TABLE IF NOT EXISTS movies (
            id serial PRIMARY KEY,
            id_movie VARCHAR ( 50 ) UNIQUE NOT NULL,
            title VARCHAR ( 255 ) NOT NULL,
            type VARCHAR ( 50 ),
            description VARCHAR(50000),
            release_year FLOAT,
            age_certification VARCHAR(255),
            runtime FLOAT,
            genres VARCHAR (1000),
            production_country VARCHAR(55),
            seasons FLOAT,
            imdb_id VARCHAR ( 50 ),
            imdb_score FLOAT,
            imdb_votes FLOAT,
            tmdb_popularity FLOAT,
            tmdb_score FLOAT,
            genres_transformed VARCHAR ( 255 ),
            production_country_transformed VARCHAR ( 50 )
        );
        """

        transfer_s3_to_redshift = S3ToRedshiftOperator(
            task_id='transfer_s3_to_redshift',
            redshift_conn_id=conn_id_name,
            s3_bucket=bucket_name,
            s3_key=S3_KEY_2,
            schema='PUBLIC',
            table=REDSHIFT_TABLE,
            copy_options=['csv']
        )
    )

postgres_to_s3 >> raw_to_trusted 
