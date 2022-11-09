# twitter-api-data-stack

This project was made with the intention to learn and get a hand on a real-world data challenge and at the same time try to develop engineering best practices about  
the most used Data Eng stack such as Apache Airflow and AWS S3, and for that, we decided to create a pipeline to consume data from Twitter API and analyze them.

![Data Infra Diagram](https://cdn.discordapp.com/attachments/1023624440350785706/1040030229533569074/Diagrama_sem_nome.drawio.png)

The first thing to do is to run the command
 `make requirements` 
that install all the necessary libraries for the pipeline.
after that type the make up command to run the dockercompose containers for Airflow.
For all this to work correctly we had to set up a AWS S3 credentials

The next step was to create the DAGs.
The first one is responsible for taking the tweets with the chosen hashtag, in this case #HouseOfTheDragon, and putting them in the "Raw" S3 lake.

The second DAG transfer all the date from the "Raw" to the "Trusted" lake 
