import os, uuid
from api.queue import get_job
from worker.downloader import download_scribd
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(BOT_TOKEN)

print("Worker started...")

while True:
    job = get_job()
    if not job:
        continue

    user_id = job["user_id"]
    msg_id = job["msg_id"]
    url = job["url"]
    filename = f"{uuid.uuid4()}.pdf"

    def progress(p):
        bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=f"⏳ Downloading... {p}%")

    try:
        download_scribd(url, filename, progress)
        bot.send_document(user_id, open(filename, "rb"))

    except Exception as e:
        bot.send_message(user_id, f"❌ Error: {e}")

    if os.path.exists(filename):
        os.remove(filename)
