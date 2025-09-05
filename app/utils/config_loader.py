import json

def load_channels(path="config/channels.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
