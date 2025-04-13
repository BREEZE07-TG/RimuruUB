from UB import app
from config import admin
from pyrogram import filters
import time

afk_status = {
    "afkTime" : 0,
    "reason" : "None",
    "status" : False
}

@app.on_message(filters.command("afk",prefixes=".") & filters.user(admin))
async def afk(client,message):

    afk_status["afkTime"] = time.time()

    try: 
        afk_status["reason"] = message.text.split(" ", 1)[1]
    except:
        reason = "None"

    afk_status["status"] = True

    user = message.from_user

    await message.reply(f"{user.mention} is away from keyboard..\n\nReason:\n{afk_status['reason']}")

@app.on_message((filters.group | filters.private) & ~filters.me)
async def afk_msg(client,message):
    try:
        if afk_status["status"] ==  True:
            if message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.id == admin:
                current_time = time.time()
                last_scene = afk_status["afkTime"]
                afk_time = current_time - last_scene
                hours, remainder = divmod(int(afk_time), 3600)
                mins, secs = divmod(remainder, 60)
                time_str = f"{hours:02}:{mins:02}:{secs:02}"

                await message.reply(
                    f"I'm currently offline since {time_str}.\nPlease contact me later.\nReason: {afk_status.get('reason', 'None')}"
                )
    except Exception as e:
        await message.reply(e)

@app.on_message(filters.me & filters.create(lambda _, __, m: afk_status["status"] == True))
async def alive(client,message):
    current_time = time.time()
    last_scene = afk_status["afkTime"]
    afk_time = current_time - last_scene
    hours , remainder = divmod(int(afk_time),3600)
    min , sec = divmod(remainder,60)
    time_str = f"{hours:02}:{min:02}:{sec:02}"
    afk_status["status"] = False

    await message.reply(f"Welcome Back!\nYou were offline since {time_str}")

