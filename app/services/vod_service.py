from yt_dlp import YoutubeDL
from app.db.session import SessionLocal
from app.models.video import Video
from app.utils.logging import logger

def fetch_vods(channel_url: str, limit: int = 15):
    NOT_AVAILABLE = ('private', 'premium_only', 'subscriber_only', 'needs_auth', 'unlisted')
    opts = {
        'quiet': True,
        'extract_flat': True,
        'simulate': True,
        'playlistend': limit
    }
    with YoutubeDL(opts) as ydl:
        logger.info(f"Fetching VOD URLs for channel: {channel_url}")
        result = ydl.extract_info(channel_url, download=False)

        videos = [{
                'id': entry['id'],
                'channel_name': result['channel'],
                'title': entry['title'],
                } 
              
              for entry in result.get('entries', []) if entry['live_status'] == 'was_live' and entry['availability'] not in NOT_AVAILABLE]


        return videos

def insert_vods(entries):
    db = SessionLocal()
    num_added = 0
    for entry in entries:
        if not db.query(Video).filter_by(video_id=entry['id']).first():
            db.add(Video(
                video_id=entry['id'],
                title=entry['title'],
                channel=entry['channel_name'],
            ))
            num_added += 1
    db.commit()
    db.close()

    logger.info(f"Added {num_added} new video references to DB")
