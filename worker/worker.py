print("🚀 Worker booting...")
import os
import sys
import uuid
from dotenv import load_dotenv

# Make sure we can import local files and project root
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from telegram import Bot
bot = Bot(token=BOT_TOKEN)
from api.queue import get_job
from downloader import download_scribd

# Load env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN is not set")

bot = Bot(token=BOT_TOKEN)

print("✅ Worker started and waiting for jobs...")

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

    def progress(p):
        try:
            bot.edit_message_text(
                chat_id=user_id,
                message_id=msg_id,
                text=f"⏳ Downloading... {p}%"
            )
        except Exception as e:
            print("Progress update failed:", e)

    try:
        print("📥 Processing:", url)
        download_scribd(url, filename, progress)

        with open(filename, "rb") as f:
            bot.send_document(chat_id=user_id, document=f)

        print("✅ Sent PDF to", user_id)

    except Exception as e:
    import requests
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": user_id, "text": f"❌ Error: {e}"}
    )
        except:
            pass

    finally:
        if os.path.exists(filename):
            os.remove(filename)
