import os
import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

# Load DB credentials
load_dotenv()
DB_NAME = os.getenv("DB_NAME", "telegram_data")
DB_USER = os.getenv("DB_USER", "postgres")  # use 'myuser' if created
DB_PASSWORD = os.getenv("DB_PASSWORD", "4124")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    id INTEGER,
    channel TEXT,
    date TIMESTAMP,
    sender BIGINT,
    message TEXT,
    views INTEGER,
    image_path TEXT
);
""")
conn.commit()

# Load JSON files
data_path = Path("data/raw/telegram_messages")
for day_folder in data_path.glob("*"):
    for json_file in day_folder.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            messages = json.load(f)
            for msg in messages:
                cur.execute("""
                    INSERT INTO raw.telegram_messages (id, channel, date, sender, message, views, image_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (
                    msg.get("id"),
                    msg.get("channel"),
                    msg.get("date"),
                    msg.get("sender"),
                    msg.get("message"),
                    msg.get("views"),
                    msg.get("image_path")
                ))

# Save changes and close
conn.commit()
cur.close()
conn.close()
print("✅ Loaded all JSON messages into raw.telegram_messages")
