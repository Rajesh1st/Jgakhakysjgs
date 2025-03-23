from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["file_provider_bot"]
channels_col = db["channels"]

# Add a channel
def add_channel(channel_id):
    if not channels_col.find_one({"channel_id": channel_id}):
        channels_col.insert_one({"channel_id": channel_id})
        return True
    return False

# Remove a channel
def remove_channel(channel_id):
    channels_col.delete_one({"channel_id": channel_id})
    return True

# Get all channels
def get_channels():
    return [doc["channel_id"] for doc in channels_col.find()]
