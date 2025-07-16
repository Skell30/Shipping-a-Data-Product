from dagster import Definitions
from .assets import telegram_scrape_job

defs = Definitions(
    jobs=[telegram_scrape_job]
)

