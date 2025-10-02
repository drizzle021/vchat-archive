import json
from app.db.session import SessionLocal
from app.models.video import Video
from app.models.message import Message
from app.models.commenters import Commenters
from app.utils.logging import logger
from app.utils.timestamp_to_seconds import parse_timestamp_to_seconds
from collections import Counter
import re

EMOTE_REGEX = r':\_[^:]+:'


def insert_messages(messages, video_id):
    db = SessionLocal()
    video = db.query(Video).filter_by(video_id=video_id).first()

    if not video:
        return
    
    emotes = []
    
    for msg in messages:
        timestamp_str = msg['time']
        timestamp_seconds = parse_timestamp_to_seconds(timestamp_str)

        db.add(Message(
            video_id = video_id,
            timestamp=msg['time'],
            timestamp_seconds=timestamp_seconds,
            author=msg['author'],
            message=msg['message']
        ))

        db.merge(Commenters(
            author=msg['author'],
            video_id=video_id
        ))
        emotes += re.findall(EMOTE_REGEX, msg['message'])

    top_emotes = Counter(emotes).most_common(3)
    video.top_emotes = [
        {"emote": emote, "count": count}
        for emote, count in top_emotes
    ]
    db.commit()
    db.close()
    print(f"Inserted {len(messages)} messages for video {video_id}")
    logger.info(f"Imported {len(messages)} messages for {video_id}")


def import_from_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        messages = json.load(f)

    return messages