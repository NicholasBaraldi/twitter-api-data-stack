select  
    tweets.id as tweets_id
    , tweets.text as tweet
    , tweets.created_at
    , users.id as username_id
    , users.username as username
from {{source("public","tweets")}} as tweets
left join 
    {{source("public","users")}} as users on users.id = tweets.author_id