from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import string
from database import add_channel, remove_channel, get_channels
from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID

bot = Client("file_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Store file mappings
bot.files = {}

# Generate a unique file ID
def generate_file_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Start command
@bot.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply("Hello! I am a file provider bot. Send me a file request.")

# Handle random text messages
@bot.on_message(filters.text & ~filters.command(["add_channel", "remove_channel"]))
async def handle_random_text(bot, message):
    await message.reply("I am just a file provider. Please do not send messages directly.")

# Handle media and add inline button
@bot.on_message(filters.media)
async def handle_media(bot, message):
    allowed_channels = get_channels()
    
    if not allowed_channels:
        await message.reply("❌ No channels are configured yet.")
        return
    
    file_id = generate_file_id()
    username = (await bot.get_me()).username
    channel_id = allowed_channels[0]

    forwarded_message = await bot.send_message(
        chat_id=channel_id,
        text=message.caption or "",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📂 Get File", url=f"https://telegram.me/{username}?start=getfile-{file_id}")]]
        )
    )

    bot.files[file_id] = (channel_id, forwarded_message.message_id)

# Handle button click and send file in DM
@bot.on_message(filters.command("start") & filters.regex(r"getfile-(\w+)"))
async def send_file(bot, message):
    file_id = message.text.split("getfile-")[1]
    
    if file_id in bot.files:
        channel_id, message_id = bot.files[file_id]
        
        await bot.forward_messages(message.chat.id, channel_id, message_id)
        await message.reply("✅ File successfully sent in DM!")
    else:
        await message.reply("⚠️ File not found!")

# Admin command: Add channel
@bot.on_message(filters.command("add_channel") & filters.user(ADMIN_ID))
async def add_channel_command(bot, message):
    if len(message.command) < 2:
        await message.reply("Usage: `/add_channel <channel_id>`")
        return

    channel_id = message.command[1]
    if add_channel(channel_id):
        await message.reply(f"✅ Channel `{channel_id}` added!")
    else:
        await message.reply("⚠️ Channel is already added.")

# Admin command: Remove channel
@bot.on_message(filters.command("remove_channel") & filters.user(ADMIN_ID))
async def remove_channel_command(bot, message):
    if len(message.command) < 2:
        await message.reply("Usage: `/remove_channel <channel_id>`")
        return

    channel_id = message.command[1]
    if remove_channel(channel_id):
        await message.reply(f"✅ Channel `{channel_id}` removed!")
    else:
        await message.reply("⚠️ Channel not found.")

bot.run()
