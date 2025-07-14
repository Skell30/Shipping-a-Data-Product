with source as (
    select
        id,
        channel,
        cast(date as timestamp) as message_time,
        sender,
        message,
        views,
        image_path
    from raw.telegram_messages
)

select * from source
