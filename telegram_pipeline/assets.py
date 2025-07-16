from dagster import op, job
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "src/scraper.py"], check=True)

@job
def telegram_scrape_job():
    scrape_telegram_data()
    load_raw_to_postgres()

@op
def load_raw_to_postgres():
    import subprocess
    subprocess.run(["python", "src/load_raw_data_to_postgres.py"], check=True)
