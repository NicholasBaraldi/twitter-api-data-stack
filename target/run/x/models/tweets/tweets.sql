
  create view "dbt_db"."dbt_schema"."tweets__dbt_tmp" as (
    select * 
from movies
  );