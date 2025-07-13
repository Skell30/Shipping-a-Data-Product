import os
import json
import time
import logging
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors import FloodWaitError
from telethon.tl.types import MessageMediaPhoto
from pathlib import Path
from datetime import datetime

# --- Load .env credentials ---
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# --- Channel setup ---
channels = [
    'tikvahpharma', 'lobelia4cosmetics', 'CheMed123'
]
image_channels = {'lobelia4cosmetics', 'CheMed123'}  # Only download images from these

# --- Directory config ---
RAW_MSG_DIR = Path("data/raw/telegram_messages")
RAW_IMG_DIR = Path("data/raw/images")

# --- Setup logging ---
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Telegram client ---
client = TelegramClient("session_name", api_id, api_hash)

def save_messages_as_json(channel_name, messages):
    date_str = datetime.now().strftime("%Y-%m-%d")
    save_path = RAW_MSG_DIR / date_str
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
            message_data = {
                "channel": channel_username,
                "id": msg.id,
                "date": str(msg.date),
                "sender": getattr(msg.from_id, 'user_id', None) if msg.from_id else None,
                "message": msg.message,
                "views": msg.views if hasattr(msg, 'views') else None,
                "image_path": None
            }

            # 📸 Image download logic (only for selected channels)
            if channel_username in image_channels and isinstance(msg.media, MessageMediaPhoto):
                img_date = datetime.now().strftime("%Y-%m-%d")
                image_folder = RAW_IMG_DIR / img_date / channel_username
                image_folder.mkdir(parents=True, exist_ok=True)

                try:
                    filename = f"{msg.id}.jpg"
                    filepath = image_folder / filename
                    client.download_media(msg, file=filepath)
                    message_data["image_path"] = str(filepath)
                except Exception as e:
                    logging.warning(f"Couldn't download image from {channel_username} (msg ID {msg.id}): {e}")

            messages.append(message_data)

        save_messages_as_json(channel_username, messages)
        print(f"✅ Scraped {len(messages)} messages from {channel_username}")
        logging.info(f"Scraped {len(messages)} messages from {channel_username}")

    except FloodWaitError as e:
        print(f"⏳ Rate limited. Sleeping for {e.seconds} seconds...")
        logging.warning(f"Flood wait: sleeping for {e.seconds} seconds")
        time.sleep(e.seconds)
        scrape_channel(channel_username)
    except Exception as e:
        print(f"❌ Failed to scrape {channel_username}: {e}")
        logging.error(f"Error scraping {channel_username}: {e}")

if __name__ == "__main__":
    with client:
        for username in channels:
            scrape_channel(username)
