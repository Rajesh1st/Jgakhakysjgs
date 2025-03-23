from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import string
import os
from database import save_file, get_file
from config import API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID

bot = Client("file_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Generate a unique file ID
def generate_file_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Start command
@bot.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply("Hello! I am a file provider bot. Send me a file request.")

# Handle random text messages
@bot.on_message(filters.text)
async def handle_random_text(bot, message):
    await message.reply("I am just a file provider. Please do not send messages directly.")

# Handle media and add inline button
@bot.on_message(filters.media)
async def handle_media(bot, message):
    file_id = generate_file_id()
    username = (await bot.get_me()).username

    forwarded_message = await bot.send_message(
        chat_id=CHANNEL_ID,
        text=message.caption or "",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📂 Get File", url=f"https://telegram.me/{username}?start=getfile-{file_id}")]]
        )
    )

    # Save file mapping
    save_file(file_id, forwarded_message.message_id)

# Handle button click and send file in DM
@bot.on_message(filters.command("start") & filters.regex(r"getfile-(\w+)"))
async def send_file(bot, message):
    file_id = message.text.split("getfile-")[1]
    message_id = get_file(file_id)

    if message_id:
        await bot.forward_messages(message.chat.id, CHANNEL_ID, message_id)
        await message.reply("✅ File successfully sent in DM!")
    else:
        await message.reply("⚠️ File not found!")

# Start bot with port support
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    bot.run()
