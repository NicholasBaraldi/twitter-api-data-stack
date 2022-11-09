# twitter-api-data-stack

This project was made with the intention to learn and get a hand on a real-world data challenge and at the same time try to develop engineering best practices about the most used Data Eng stack such as Apache Airflow and AWS S3, and for that, we decided to create a pipeline to consume data from Twitter API and analyze them.

![Data Infra Diagram](https://cdn.discordapp.com/attachments/1023624440350785706/1040030229533569074/Diagrama_sem_nome.drawio.png)

<br />

## First Steps
<br />

The first thing to do is to run the command
```  
make requirements  
``` 
This command install all the necessary libraries for the project.
After that type
```
make up
```
It will run the docker compose containers for Airflow.

For all this to work correctly we had to set up a AWS S3 credentials.  
On Airflow UI, go to Admin > Connections  
Create a new connection with the following attributes:  
Conn Id: my_conn_S3  
Conn Type: S3  
Extra: `{"aws_access_key_id":"_your_aws_access_keyid", "aws_secret_access_key": "_your_aws_secret_accesskey"}`  
Leave all the other fields (Host, Schema, Login) blank.

<br />

## DAGs
<br />

The next step was to create the Pipelines using Airflow DAGs.  
The first DAG\`s Task instanciate the class `Twitter` and runs the method `make_req` to ingest the tweets with the chosen parans like hashtag, in this case #HouseOfTheDragon, number of tweets per request and number of requests
``` Python
t = Twitter(bearer_token)
params = {"query": "#HouseOfTheDragon", "ntweets": 100, "nreq": 200}
tweets, users = t.make_req(params["query"], params["ntweets"], params["nreq"])
```

We used Spark to process the data and ingest it into the lake
``` Python
tweets = spark.read.json(
    f"s3a://{bucket_name}/Raw/{date.today()}/{file_name_tweets}/"
)

tweets.write.json(f"s3a://{bucket_name}/Trusted/{file_name_tweets}")
```

In the second DAG, which is in s3_to_postgres_dw.py, Pandas were used, with SQL Alchemy, to create a Postgres database acting as a warehouse.
``` Python
engine = create_engine(
    "postgresql://username:password@host.docker.internal:5432/dbt_db"
)
final_df.to_sql("tweets", engine, if_exists = 'replace')
```

<br />

## Analytics Engineering
<br />

The next step in this flow was to model the data in a way to facilitate data consumption. For that we chose DBT, a powerful tool for data wrangling and Analytics Engineering, to make the transformations, to struct data, and to create data lineage.

We structured the models in intermediate and datamart, so you can use
```
dbt run
```
This command creates all the views.

<br />

## Data Visualization
<br />

Our last step was data visualization itself. For that a dashboard using Streamlit was the choice, consuming data directly from our Postgres “Data Warehouse”.  
The dashboards can be seen here: [Dashboards](https://github.com/NicholasBaraldi/hotd-tweets-analysis)