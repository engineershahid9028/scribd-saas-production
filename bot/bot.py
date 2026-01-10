import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from api.queue import add_job

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /download <scribd_url>")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /download <url>")

    url = context.args[0]
    msg = await update.message.reply_text("📥 Added to queue...")

    add_job({
        "user_id": update.effective_user.id,
        "url": url,
        "msg_id": msg.message_id
    })

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("download", download))

app.run_polling()
