from UB import app
from pyrogram import idle

async def start_bot():
    await app.start()
    chat = -1002348912075
    await app.send_message(chat, "Bot is online and ready to use!")
    await idle()
    await app.send_message(chat, "I'm going off")


if __name__ == "__main__":
    app.run(start_bot())