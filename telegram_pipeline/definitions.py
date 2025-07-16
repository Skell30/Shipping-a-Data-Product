from dagster import Definitions
from .assets import telegram_pipeline_job

defs = Definitions(
    jobs=[telegram_pipeline_job]
)

