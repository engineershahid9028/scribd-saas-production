import os
import sys
import uuid
import json
import requests
from dotenv import load_dotenv

# Paths so imports work on Railway
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from api.queue import get_job
from downloader import download_scribd

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN is not set")

print("🚀 Worker booting...")
print("✅ Worker started and waiting for jobs...")

def tg_edit(chat_id, msg_id, text):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText",
        params={"chat_id": chat_id, "message_id": msg_id, "text": text},
        timeout=30
    )

def tg_send(chat_id, text):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": chat_id, "text": text},
        timeout=30
    )

def tg_send_file(chat_id, filepath):
    with open(filepath, "rb") as f:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
            data={"chat_id": chat_id},
            files={"document": f},
            timeout=120
        )

while True:
    job = get_job()
    if not job:
        continue

    user_id = job.get("user_id")
    msg_id = job.get("msg_id")
    url = job.get("url")

    if not user_id or not msg_id or not url:
        print("❌ Invalid job payload:", job)
        continue

    filename = f"{uuid.uuid4()}.pdf"
    print("📥 Processing:", url)

    def progress(p):
        try:
            tg_edit(user_id, msg_id, f"⏳ Downloading... {p}%")
        except Exception as e:
            print("Progress update failed:", e)

    try:
        download_scribd(url, filename, progress)
        tg_send_file(user_id, filename)
        print("✅ Sent PDF to", user_id)

    except Exception as e:
        print("❌ Download failed:", e)
        try:
            tg_send(user_id, f"❌ Error: {e}")
        except Exception as e2:
            print("❌ Failed to notify user:", e2)

    finally:
        if os.path.exists(filename):
            os.remove(filename)
