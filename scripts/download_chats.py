import os
import json
import time
import random
from chat_downloader import ChatDownloader
from app.db.session import SessionLocal
from app.models.video import Video
from config.settings import RAW_CHAT_DIR
from config.settings import CHAT_DOWNLOADER_TIMEOUT
from app.utils.logging import logger


def preprocess_message(msg):
    return {
        'message': msg.get('message'),
        'author': msg.get('author', {}).get('name'),
        'time': msg.get('time_text')
    }

def download_all_chats():
    os.makedirs(RAW_CHAT_DIR, exist_ok=True)
    db = SessionLocal()
    videos = db.query(Video).all()
    downloader = ChatDownloader()

    for video in videos:
        output_path = os.path.join(RAW_CHAT_DIR, f"{video.video_id}.json")
        if os.path.exists(output_path):
            continue

        url = f"https://www.youtube.com/watch?v={video.video_id}"
        print(f"Downloading chat for {video.title}...")
        logger.info(f"Started downloading chat for {video.title} ({video.video_id})")
        success = False
        for attempt in range(3):
            try:
                chat = downloader.get_chat(url, message_types=["text_message"], max_messages=200000)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write("[\n")
                    first = True
                    for message in chat:
                        cleaned = preprocess_message(message)
                        if not first:
                            f.write(",\n")
                        json.dump(cleaned, f, ensure_ascii=False)
                        first = False
                    f.write("\n]")
                success = True
                logger.info(f"Successfully downloaded chat for {video.title}")
                break
            except Exception as e:
                print(f"Failed to download chat for {video.title}: {e} - Attempt #{attempt+1}")
                logger.error(f"Failed to download chat for {video.title}: {e} - Attempt #{attempt+1}")
                time.sleep(5)

        if not success: 
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump([{
                    "error": "live chat missing",
                    "video_id": video.video_id,
                    "title": video.title,
                }], f, ensure_ascii=False)
            logger.error(f"Chat for {video.title} was not downloaded. Error .json written to {video.video_id}.json")
        time.sleep(random.randint(2, 5))

if __name__ == "__main__":
    download_all_chats()
