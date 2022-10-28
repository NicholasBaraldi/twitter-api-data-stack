select  
    tweets.id as tweets_id
    , users.id as username_id
    , users.username as username
    , users.name as name
    , users.description as description
    , tweets.text as tweet
    , tweets.created_at
from {{source("public","tweets")}} as tweets
left join 
    {{source("public","users")}} as users on users.id = tweets.author_id