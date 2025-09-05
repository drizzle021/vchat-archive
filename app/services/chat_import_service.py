import json
from app.db.session import SessionLocal
from app.models.video import Video
from app.models.message import Message
from app.utils.logging import logger

def insert_messages(messages, video_id):
    db = SessionLocal()
    if not db.query(Video).filter_by(video_id=video_id).first():
        return
    
    
    for msg in messages:
        db.add(Message(
            video_id = video_id,
            timestamp=msg['time'],
            author=msg['author'],
            message=msg['message']
        ))
    db.commit()
    db.close()
    print(f"Inserted {len(messages)} messages for video {video_id}")
    logger.info(f"Imported {len(messages)} messages for {video_id}")


def import_from_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        messages = json.load(f)

    return messages