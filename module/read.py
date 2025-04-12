from config import admin
from UB import app
from pyrogram import filters
import math
import os

@app.on_message(filters.command("read", prefixes=".") & filters.user(admin))
async def read(_, msg):
    message = await msg.reply_text("`Processing...`")
    file = await msg.reply_to_message.download()
    with open(file, "r") as f:
        content = f.read() 
    text = f"**Content**:\n\n{content}"
    if len(text) > 4096:
        total_size = math.ceil(len(text)/4096)
        await message.edit(text[:4096])
        for i in range(1, total_size):
            await message.reply_text(text[i*4096:(i+1)*4096])
    if os.path.exists(file):
        os.remove(file)