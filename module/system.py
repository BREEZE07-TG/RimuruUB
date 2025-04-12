from UB import app
from pyrogram import filters
import subprocess
import os
import asyncio
import sys
from config import admin


@app.on_message(filters.command('logs',prefixes=".") & filters.user(admin))
async def logs(client,message):
    L = subprocess.getoutput("tail -n 20 logs.txt")
    await message.reply(f"<pre>Logs\n{L}</pre>")

@app.on_message(filters.command('restart',prefixes=".") & filters.user(admin))
async def restart(client,message):
    rst_msg= await message.reply("restarting system...")
    await asyncio.sleep(2)
    await rst_msg.edit("system restarted")
    os.execv(sys.executable, ['UB'] + sys.argv)