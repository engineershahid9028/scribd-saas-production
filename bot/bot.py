import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = "https://scribd-saas-production.fly.dev/job"

app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send:\n/download <url>")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /download <url>")

    url = context.args[0]
    msg = await update.message.reply_text("📥 Added to queue...")

    payload = {
        "user_id": update.effective_user.id,
        "msg_id": msg.message_id,
        "url": url
    }

    requests.post(API_URL, json=payload, timeout=30)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("download", download))

app.run_polling()
