import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# DB connection details
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "telegram_data")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "4124")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=5432
)
cur = conn.cursor()

# Create the table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS raw.yolo_detections (
    image_path TEXT,
    detected_object_class TEXT,
    confidence_score FLOAT
);
""")
conn.commit()

# Load YOLO detections
json_file = Path("data/processed/yolo_detections.json")
with open(json_file, "r", encoding="utf-8") as f:
    detections = json.load(f)

# Insert each detection
for row in detections:
    cur.execute("""
        INSERT INTO raw.yolo_detections (image_path, detected_object_class, confidence_score)
        VALUES (%s, %s, %s);
    """, (
        row["image_path"],
        row["detected_object_class"],
        row["confidence_score"]
    ))

conn.commit()
cur.close()
conn.close()

print("✅ YOLO detections loaded into raw.yolo_detections")
