from UB import app
from pyrogram import filters
from config import admin
from PIL import Image, ImageDraw, ImageFilter
import io

@app.on_message(filters.command("profile", prefixes=".") & filters.user(admin))
async def profile(client, message):

    user = await app.get_chat(message.from_user.id)
    usr = message.from_user
    

    fg = await app.download_media(usr.photo.big_file_id)

    bg = Image.open("bg.jpg").convert("RGBA")

    fg_img = Image.open(fg).convert("RGBA")

    mask = Image.new("L", fg_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + fg_img.size, fill=255)
    
    fg_img.putalpha(mask)

    fg_img = fg_img.resize((1100 , 1100))

    bg.paste(fg_img, (900, 350), fg_img)

    bg = bg.filter(ImageFilter.SMOOTH)

    buffer = io.BytesIO()
    bg.save(buffer, format="PNG")
    buffer.seek(0)

    await client.send_photo(
        message.chat.id,
        buffer,
        f"Name: {usr.mention}\n"
        f"User ID: {user.id}\n"
        f"Bio: {user.bio}",
        reply_to_message_id = message.id
        )
