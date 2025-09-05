from app.utils.config_loader import load_channels
from app.services.vod_service import fetch_vods, insert_vods

def fetch_all_vods(max_per_channel: int):
    channels = load_channels()
    for channel in channels:
        print(f"Fetching VODs for {channel['name']}...")
        entries = fetch_vods(channel['url'], max_per_channel)
        insert_vods(entries)

if __name__ == "__main__":
    fetch_all_vods(50)