import os
import time
import uuid
from api.queue import get_job
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(BOT_TOKEN)

print("🚀 Worker started and waiting for jobs...")

while True:
    job = get_job()

    if not job:
        time.sleep(2)
        continue

    user_id = job["user_id"]
    url = job["url"]

    print("📥 Processing job:", job)

    try:
        bot.send_message(user_id, "⏳ Processing your document...")

        # TEMP test download
        for i in range(1, 6):
            time.sleep(1)
            bot.send_message(user_id, f"Progress: {i*20}%")

        filename = f"{uuid.uuid4()}.pdf"
        with open(filename, "w") as f:
            f.write("Test PDF")

        bot.send_document(user_id, open(filename, "rb"))

    except Exception as e:
        bot.send_message(user_id, f"❌ Error: {e}")

    finally:
        if os.path.exists(filename):
            os.remove(filename)
