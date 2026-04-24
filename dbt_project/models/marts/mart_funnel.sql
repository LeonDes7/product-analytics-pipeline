with events as (
    select * from {{ ref('stg_events') }}
),

funnel as (
    select
        'signup' as step,
        1 as step_order,
        count(distinct user_id) as users
    from events where event_type = 'signup'

    union all

    select
        'login' as step,
        2 as step_order,
        count(distinct user_id) as users
    from events where event_type = 'login'

    union all

    select
        'click_feature' as step,
        3 as step_order,
        count(distinct user_id) as users
    from events where event_type = 'click_feature'

    union all

    select
        'upgrade_plan' as step,
        4 as step_order,
        count(distinct user_id) as users
    from events where event_type = 'upgrade_plan'
)

select
    step,
    step_order,
    users,
    round(users / first_value(users) over (order by step_order) * 100, 2) as conversion_rate
from funnel
order by step_order