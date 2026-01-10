from pyrogram import Client, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = Client("bot", bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("Scribd SaaS Bot is running.")

app.run()
