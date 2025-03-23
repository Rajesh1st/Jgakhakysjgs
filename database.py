import json

DB_FILE = "files.json"

# Load existing file mappings
def load_files():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save file mappings
def save_files(files):
    with open(DB_FILE, "w") as f:
        json.dump(files, f)

# Save a new file ID with message ID
def save_file(file_id, message_id):
    files = load_files()
    files[file_id] = message_id
    save_files(files)

# Retrieve message ID by file ID
def get_file(file_id):
    files = load_files()
    return files.get(file_id, None)
