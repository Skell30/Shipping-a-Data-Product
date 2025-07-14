-- models/staging/dim_channels.sql

with distinct_channels as (
    select distinct
        channel
    from {{ ref('stg_telegram_messages') }}
)

select
    md5(channel) as channel_id,  -- Optional hashed ID
    channel
from distinct_channels
