import os
import time
from api.queue import pop_job
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(BOT_TOKEN)

print("🚀 Worker started")

while True:
    print("⏳ Waiting for job...")
    job = pop_job()

    if not job:
        continue

    print("📥 Job received:", job)

    user_id = job["user_id"]

    bot.send_message(user_id, "✅ Worker received your job!")

    time.sleep(3)

    bot.send_message(user_id, "🎉 Job finished successfully!")
