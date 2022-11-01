with tweets_per_10_minute as (
    select
        date_trunc('minute', created_at) - (CAST(EXTRACT(MINUTE from created_at) as integer) % 10) * interval '1 minute' as trunc_10_minute,
        count(*) as count_tweets,
        count(distinct username_id) as count_users
    from {{ref("tweets_users")}}
    group by trunc_10_minute
    order by trunc_10_minute
)

select *,
    sum(count_tweets) over (order by trunc_10_minute asc rows between unbounded preceding and current row) as csum_tweets,
    sum(count_users) over (order by trunc_10_minute asc rows between unbounded preceding and current row) as csum_users
from tweets_per_10_minute
order by tweets_per_10_minute asc
