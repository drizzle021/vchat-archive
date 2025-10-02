from app.db.session import SessionLocal
from app.models.video import Video
from app.models.message import Message
import re

def parse_timestamp_to_seconds(ts: str) -> int:
    negative = ts.startswith('-')
    ts = ts.lstrip('-')
    parts = list(map(int, ts.split(':')))
    if len(parts) == 3:
        h, m, s = parts
    elif len(parts) == 2:
        h, m, s = 0, *parts
    else:
        h, m, s = 0, 0, parts[0]
    total = h * 3600 + m * 60 + s
    return -total if negative else total

def update_timestamps_by_video():
    db = SessionLocal()
    videos = db.query(Video.video_id).all()

    for (video_id,) in videos:
        messages = db.query(Message).filter_by(video_id=video_id).yield_per(1000)
        for msg in messages:
            if msg.timestamp:
                msg.timestamp_seconds = parse_timestamp_to_seconds(msg.timestamp)
        db.commit()
        print(f"Updated timestamps for video {video_id}")

    db.close()
    print("All videos processed.")

if __name__ == "__main__":
    update_timestamps_by_video()
