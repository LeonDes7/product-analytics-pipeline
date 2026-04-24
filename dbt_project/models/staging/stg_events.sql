with source as (
    select * from {{ source('product_analytics', 'raw_events') }}
),

staged as (
    select
        event_id,
        user_id,
        event_type,
        timestamp(event_timestamp) as event_timestamp,
        platform,
        page,
        session_id,
        country,
        date(event_timestamp) as event_date
    from source
)

select * from staged