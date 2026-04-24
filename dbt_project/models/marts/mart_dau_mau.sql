with daily_active as (
    select
        event_date,
        count(distinct user_id) as dau
    from {{ ref('stg_events') }}
    group by event_date
),

monthly_active as (
    select
        date_trunc(event_date, month) as month,
        count(distinct user_id) as mau
    from {{ ref('stg_events') }}
    group by date_trunc(event_date, month)
)

select
    d.event_date,
    d.dau,
    m.mau,
    round(d.dau / m.mau * 100, 2) as dau_mau_ratio
from daily_active d
left join monthly_active m
    on date_trunc(d.event_date, month) = m.month
order by event_date