from pyrogram import filters
from UB import app
from config import admin

@app.on_message(filters.command("start",prefixes=".") & filters.user(admin))
async def start(client,message):
    await message.reply("started")
