import json

DB_FILE = "channels.json"

# Load existing channels
def load_channels():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save channels
def save_channels(channels):
    with open(DB_FILE, "w") as f:
        json.dump(channels, f)

# Add a channel
def add_channel(channel_id):
    channels = load_channels()
    if channel_id not in channels:
        channels.append(channel_id)
        save_channels(channels)
        return True
    return False

# Remove a channel
def remove_channel(channel_id):
    channels = load_channels()
    if channel_id in channels:
        channels.remove(channel_id)
        save_channels(channels)
        return True
    return False

# Get list of channels
def get_channels():
    return load_channels()
