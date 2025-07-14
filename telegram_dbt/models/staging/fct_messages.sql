-- models/staging/fct_messages.sql

select
    id as message_id,
    channel,
    message_time,
    sender,
    message,
    views,
    image_path
from {{ ref('stg_telegram_messages') }}
