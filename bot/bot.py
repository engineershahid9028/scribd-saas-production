import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from api.queue import add_job

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Scribd SaaS Bot is online.\nUse /download <scribd_url>")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /download <scribd_url>")

    url = context.args[0]
    msg = await update.message.reply_text("📥 Added to queue...")

    add_job({
        "user_id": update.effective_user.id,
        "msg_id": msg.message_id,
        "url": url
    })

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("download", download))

app.run_polling()
