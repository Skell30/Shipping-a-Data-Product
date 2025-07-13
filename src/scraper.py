# src/scraper.py

import os
import json
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors import FloodWaitError
from pathlib import Path
from datetime import datetime
import logging
import time

# --- Load secrets from .env ---
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# --- Config ---
channels = [
    'tikvahpharma', 'lobelia4cosmetics', 'CheMed123'
]
RAW_DATA_DIR = Path("data/raw/telegram messages")

# --- Setup logging ---
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Create a Telegram Client session ---
client = TelegramClient("session_name", api_id, api_hash)


def save_messages_as_json(channel_name, messages):
    date_str = datetime.now().strftime("%Y-%m-%d")
    save_path = RAW_DATA_DIR / date_str
    save_path.mkdir(parents=True, exist_ok=True)

    file_path = save_path / f"{channel_name}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def scrape_channel(channel_username):
    try:
        channel = client.get_entity(channel_username)
        history = client(GetHistoryRequest(
            peer=channel,
            limit=500,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        messages = []
        for msg in history.messages:
            messages.append({
                "channel": channel_username,
                "id": msg.id,
                "date": str(msg.date),
                "sender": getattr(msg.from_id, 'user_id', None) if msg.from_id else None,
                "message": msg.message,
                "views": msg.views if hasattr(msg, 'views') else None
                })



        save_messages_as_json(channel_username, messages)
        print(f"✅ Scraped {len(messages)} messages from {channel_username}")
        logging.info(f"Scraped {len(messages)} messages from {channel_username}")

    except FloodWaitError as e:
        print(f"⏳ Rate limited. Sleeping for {e.seconds} seconds...")
        logging.warning(f"Flood wait: sleeping for {e.seconds} seconds")
        time.sleep(e.seconds)
        scrape_channel(channel_username)  # Retry after wait
    except Exception as e:
        print(f"❌ Failed to scrape {channel_username}: {e}")
        logging.error(f"Error scraping {channel_username}: {e}")


if __name__ == "__main__":
    with client:
        for username in channels:
            scrape_channel(username)
