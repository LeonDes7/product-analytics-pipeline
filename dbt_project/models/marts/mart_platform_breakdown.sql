select
    platform,
    event_type,
    count(*) as event_count,
    count(distinct user_id) as unique_users,
    count(distinct event_date) as active_days
from {{ ref('stg_events') }}
group by platform, event_type
order by platform, event_count desc