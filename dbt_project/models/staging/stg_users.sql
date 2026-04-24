with source as (
    select * from {{ source('product_analytics', 'raw_users') }}
),

staged as (
    select
        user_id,
        date(signup_date) as signup_date,
        platform,
        country,
        plan
    from source
)

select * from staged