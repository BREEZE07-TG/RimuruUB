from pyrogram import Client, filters
import os
import requests
import time
from UB import app
from config import admin


CATBOX_API_URL = "https://catbox.moe/user/api.php"

def upload_to_catbox(file_path):
    
    with open(file_path, "rb") as file:
        files = {"fileToUpload": (file.name, file)}
        data = {"reqtype": "fileupload", "userhash": ""} 
        
        try:
            response = requests.post(CATBOX_API_URL, data=data, files=files)
            if response.status_code == 200:
                return response.text.strip()  
            else:
                print(f"Error from Catbox: {response.text}")
                return None
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None

@app.on_message(filters.command("url",prefixes=".") & filters.reply  & filters.user(admin))
async def url(client: Client, message):
   
    if not message.reply_to_message:
        await message.reply("Reply to a media file.")
        return

    start_time = time.time()
    text = await message.reply("Uploading your media...")

    media = message.reply_to_message.document or message.reply_to_message.photo or message.reply_to_message.video or message.reply_to_message.audio or message.reply_to_message.animation
    if not media:
        await text.edit("Unsupported media type.")
        return
   
    size = media.file_size
    if size > 200*1024*1024:
        await text.edit("Looks like the media you provided have huge size\nSorry I only supports till 200mb")
        return

    file_path = await client.download_media(media.file_id)

    if file_path:
        file_url = await client.loop.run_in_executor(None, upload_to_catbox, file_path)

        if file_url:
            end_time = time.time()
            elapsed_time = end_time - start_time
            await text.edit(
                f"Your media has been uploaded!\n\n"
                f"<a href='{file_url}'>View File</a>\n"
                f"Time taken: {elapsed_time:.3f} seconds\n"
                f"Direct Link: <code>{file_url}</code>", show_above_text = True
            ) 
        else:
            await text.edit("Failed to upload the media to Catbox.")

        os.remove(file_path) if os.path.exists(file_path) else None
    else:
        await text.edit("Failed to download the media.")