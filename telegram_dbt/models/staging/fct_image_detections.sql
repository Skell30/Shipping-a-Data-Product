-- models/staging/fct_image_detections.sql

with detections as (
    select
        -- You must load the JSON into a Postgres table first
        image_path,
        detected_object_class,
        confidence_score
    from raw.yolo_detections
),

linked as (
    select
        fct.message_id,
        d.detected_object_class,
        d.confidence_score
    from detections d
    join staging.fct_messages fct
        on fct.image_path = d.image_path
)

select * from linked
