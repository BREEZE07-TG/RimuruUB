import aiohttp
from pyrogram import filters
from config import admin
from UB import app

async def fetch_data(query, message):
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json"
        }
        url = "https://api.binjie.fun/api/generateStream"
        data = {
            "prompt": query,
            "userId": f"#/chat/{message.from_user.id}",
            "network": True,
            "stream": False,
            "system": {
                "userId": "#/chat/1722576084617",
                "withoutContext": False
            }
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                return await response.text()
    except Exception as e:
        return f"An error occurred: {str(e)}"

instruct = "Note the length of out should be short under length 512 and the should tone rimuru from anime the time i got reancarnated as a slime a helpful ai"

@app.on_message(filters.command("ai", prefixes=".") & filters.user(admin))
async def get_query(_, message):
        if len(message.command) < 2:
            return await message.reply("Please provide a query!")
        query = message.text.split(" ", 1)[1] + instruct

        msg = await message.reply("Please wait genrating your responce")

        result =  await fetch_data(query, message)

        await msg.edit(f"<b>Your genrated result</b>\n\n>{result}")

