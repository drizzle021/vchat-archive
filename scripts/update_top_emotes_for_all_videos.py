from app.db.session import SessionLocal
from app.models.video import Video
from app.models.message import Message
from collections import Counter
import re

EMOTE_REGEX = r':\_[^:]+:'

def extract_top_emotes(messages):
    emotes = []
    for msg in messages:
        emotes += re.findall(EMOTE_REGEX, msg.message)
    return Counter(emotes).most_common(3)

def update_all_videos_top_emotes():
    db = SessionLocal()
    videos = db.query(Video).all()

    for video in videos:
        messages = db.query(Message).filter_by(video_id=video.video_id).all()
        top_emotes = extract_top_emotes(messages)

        video.top_emotes = [
            {"emote": emote, "count": count}
            for emote, count in top_emotes
        ]

        print(f"Updated {video.video_id} with top emotes: {video.top_emotes}")

    db.commit()
    db.close()
    print("✅ All videos updated with top emotes.")

if __name__ == "__main__":
    update_all_videos_top_emotes()
