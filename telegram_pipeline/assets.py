from dagster import op, job
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "src/scraper.py"], check=True)

@op
def load_raw_to_postgres():
    subprocess.run(["python", "src/load_raw_data_to_postgres.py"], check=True)

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run", "--project-dir", "telegram_dbt"], check=True)

@op
def run_yolo_enrichment():
    subprocess.run(["python", "src/load_yolo_json_to_postgres.py"], check=True)

from dagster import op, job, In

@job
def telegram_pipeline_job():
    step_1 = scrape_telegram_data()
    step_2 = load_raw_to_postgres()
    step_3 = run_dbt_transformations()
    step_4 = run_yolo_enrichment()
