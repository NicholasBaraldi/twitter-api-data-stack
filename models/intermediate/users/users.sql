with aux as (
select  
    id,
    name,
    username,
    description,
    row_number() over(partition by id) as rank
from {{source("public","users")}}
)
select     
    id,
    name,
    username,
    description
from aux 
where rank = 1