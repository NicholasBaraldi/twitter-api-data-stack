
  create view "dbt_db"."dbt_schema"."test__dbt_tmp" as (
    select * from "dbt_db"."pg_catalog"."pg_aggregate"
  );