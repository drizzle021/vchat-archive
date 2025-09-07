from fastapi import APIRouter, Query
from app.db.session import SessionLocal
from app.models.video import Video
from app.models.commenters import Commenters
from app.utils.normalize import normalize

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

@router.get("/videos/by-author")
def get_videos_by_author(author: str = Query(...)):
    db = SessionLocal()

    video_ids = db.query(Commenters.video_id).filter(Commenters.author.ilike(f"%{author}%")).all()
    video_ids = [vid[0] for vid in video_ids]

    videos = db.query(Video).filter(Video.video_id.in_(video_ids)).all()
    return videos


@router.get("/videos/by-title")
def get_videos_by_author(q: str = Query(...)):
    db = SessionLocal()

    q = normalize(q)
    
    pattern = f"%{q.lower()}%"

    return db.query(Video).filter(Video.title.ilike(pattern)).all()

