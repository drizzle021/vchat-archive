from fastapi import APIRouter, Query
from app.db.session import SessionLocal
from app.models.video import Video
router = APIRouter()

@router.get("/videos")
def get_videos(channel: str = Query(default=None)):
    db = SessionLocal()

    query = db.query(Video)
    if channel:
        query = query.filter(Video.channel == channel)

    videos = query.all()
    db.close()

    return [{"id": v.video_id, "title": v.title, "channel": v.channel} for v in videos]
