from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import string
from database import add_channel, remove_channel, get_channels
from config import API_ID, API_HASH, BOT_TOKEN

bot = Client("file_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Generate a unique file ID
def generate_file_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Start command
@bot.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply("Hello! I am a file provider bot. Send me a file request.")

# Handle random messages
@bot.on_message(filters.text)
async def handle_random_text(bot, message):
    await message.reply("I am just a file provider. Please do not send messages directly.")

# Forward media to channel and add button
@bot.on_message(filters.media)
async def handle_media(bot, message):
    allowed_channels = get_channels()
    
    if not allowed_channels:
        await message.reply("No channels are configured yet.")
        return
    
    file_id = generate_file_id()
    temp_username = (await bot.get_me()).username
    
    # Forward media to the first allowed channel
    forwarded_message = await bot.send_message(
        chat_id=allowed_channels[0],
        text=message.caption or "",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Get File", callback_data=f"getfile_{file_id}")]]
        )
    )
    
    # Store the mapping of file_id to the message ID
    bot.files[file_id] = forwarded_message.message_id

# Handle button click
@bot.on_callback_query(filters.regex(r"getfile_(\w+)"))
async def send_file(bot, query):
    file_id = query.data.split("_")[1]
    
    if file_id in bot.files:
        message_id = bot.files[file_id]
        channel_id = get_channels()[0]  
        
        # Forward file to user
        await bot.forward_messages(query.from_user.id, channel_id, message_id)
        
        # Show popup alert
        await query.answer("✅ File successfully sent in DM!", show_alert=True)
    else:
        await query.answer("⚠️ File not found!", show_alert=True)

# Admin command: Add channel
@bot.on_message(filters.command("add_channel") & filters.user("YOUR_ADMIN_ID"))
async def add_channel_command(bot, message):
    if len(message.command) < 2:
        await message.reply("Usage: /add_channel <channel_id>")
        return

    channel_id = message.command[1]
    if add_channel(channel_id):
        await message.reply(f"✅ Channel {channel_id} added!")
    else:
        await message.reply("⚠️ Channel is already added.")

# Admin command: Remove channel
@bot.on_message(filters.command("remove_channel") & filters.user("YOUR_ADMIN_ID"))
async def remove_channel_command(bot, message):
    if len(message.command) < 2:
        await message.reply("Usage: /remove_channel <channel_id>")
        return

    channel_id = message.command[1]
    if remove_channel(channel_id):
        await message.reply(f"✅ Channel {channel_id} removed!")
    else:
        await message.reply("⚠️ Channel not found.")

bot.files = {}  # Store file mappings

bot.run()
