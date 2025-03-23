import os

API_ID = int(os.getenv("API_ID", "YOUR_API_ID"))
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")  # Fixed this line
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1002339454272"))  # Fixed the syntax
MONGO_URI = os.getenv("MONGO_URI", "YOUR_MONGODB_CONNECTION_STRING")
