with user_cohorts as (
    select
        u.user_id,
        date_trunc(u.signup_date, week) as cohort_week,
        date_trunc(e.event_date, week) as activity_week
    from {{ ref('stg_users') }} u
    join {{ ref('stg_events') }} e
        on u.user_id = e.user_id
),

cohort_sizes as (
    select
        cohort_week,
        count(distinct user_id) as cohort_size
    from user_cohorts
    group by cohort_week
),

retention as (
    select
        uc.cohort_week,
        uc.activity_week,
        date_diff(uc.activity_week, uc.cohort_week, week) as weeks_since_signup,
        count(distinct uc.user_id) as active_users
    from user_cohorts uc
    group by 1, 2, 3
)

select
    r.cohort_week,
    r.weeks_since_signup,
    r.active_users,
    cs.cohort_size,
    round(r.active_users / cs.cohort_size * 100, 2) as retention_rate
from retention r
left join cohort_sizes cs
    on r.cohort_week = cs.cohort_week
order by cohort_week, weeks_since_signup