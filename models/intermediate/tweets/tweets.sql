
select distinct
    id,
     author_id,
     created_at,
     text
from {{source("public","tweets")}}