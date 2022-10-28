import pandas as pd
from datetime import datetime, timezone

def model(dbt, session):
    dbt.config(materialized="table")
    tweets_users_df = dbt.source("public", "users")
    final_df = tweets_users_df["username_id"].apply(lambda x: x/10000)
    return final_df