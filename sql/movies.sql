
CREATE OR REPLACE TABLE movies (
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

CREATE OR REPLACE TABLE movies (id serial PRIMARY KEY,id_movie VARCHAR ( 50 ) UNIQUE NOT NULL,title VARCHAR ( 255 ) NOT NULL,type VARCHAR ( 50 ),description VARCHAR(50000),release_year FLOAT,age_certification VARCHAR(255),runtime FLOAT,genres VARCHAR (1000),production_country VARCHAR(55),seasons FLOAT,imdb_id VARCHAR ( 50 ),imdb_score FLOAT,imdb_votes FLOAT,tmdb_popularity FLOAT,tmdb_score FLOAT,genres_transformed VARCHAR ( 255 ),production_country_transformed VARCHAR ( 50 ));
-- \copy movies (id,id_movie,title,type,description,release_year,age_certification,runtime,genres,production_country,seasons,imdb_id,imdb_score,imdb_votes,tmdb_popularity,tmdb_score,genres_transformed,production_country_transformed) from '/home/joao_victor/twitter-api-data-stack/data/df_titles.csv' WITH DELIMITER ',' CSV HEADER;

df.write.jdbc(url=url, table="movies", mode="append", properties=properties)
     spark = (
      SparkSession.builder.config(
          "spark.jars.packages",
          "org.apache.hadoop:hadoop-common:3.3.3,org.apache.hadoop:hadoop-client:3.3.3,org.apache.hadoop:hadoop-aws:3.3.3,org.apache.hive:hive-jdbc:3.1.3, org.apache.curator:curator-framework:3.1.0",
      )
      .master("local[*]")
      .getOrCreate()
  )
   properties = {
          "user": "admin",
          "password": ""
      }
      url = "jdbc:hive2://localhost:10000"