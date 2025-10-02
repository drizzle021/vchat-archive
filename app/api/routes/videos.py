import re
from fastapi import APIRouter, Query
from app.db.session import SessionLocal
from app.models.video import Video
from app.models.commenters import Commenters
from app.models.message import Message
from app.utils.normalize import normalize
from sqlalchemy import func
from typing import List
from fastapi import HTTPException
from datetime import timedelta

router = APIRouter()

@router.get("/videos")
def get_videos(
    channel: List[str] = Query(default=None, alias="channel[]"),
    keyword: str = Query(default=None),
    title: str = Query(default=None),
    author: str = Query(default=None),
    limit: int = Query(default=25, ge=1, le=25),
    offset: int = Query(default=0, ge=0)
):
    db = SessionLocal()

    query = db.query(Video)
    
    if channel:
        query = query.filter(Video.channel.in_(channel))

    # for use with GIN index
    if title:
        ts_query = func.to_tsquery('simple', ' & '.join(title.strip().split()))
        query = query.filter(
            func.to_tsvector('simple', Video.title).op('@@')(ts_query)
            | Video.title.ilike(f'%{title}%')
    )

    if author:
        query = query.join(Commenters, Video.video_id == Commenters.video_id).filter(Commenters.author.ilike(f'%{author}%'))

    # filter over messages
    if keyword:
        pass

    total = query.count()
    videos = (
        query.offset(offset)
        .limit(limit)
        .all()
    )

    db.close()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "videos": [
            {
                "id": v.video_id,
                "title": v.title,
                "channel": v.channel,
                "chat_status": v.chat_status
            } 
            for v in videos
        ]
    }

@router.get("/videos/top-emotes/{video_id}")
def get_top_emotes(
    video_id: str,
):
    db = SessionLocal()

    return db.query(Video).filter_by(video_id=video_id).first().top_emotes


@router.get("/videos/chatters/{video_id}")
def get_chatters(
    video_id: str,
    limit: int = Query(default=25, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    search: str = Query(default=None)
):
    db = SessionLocal()
    video = db.query(Video).filter_by(video_id=video_id).first()
    if not video:
        db.close()
        return {"chatters": [], "total": 0, "limit": limit, "offset": offset}

    query = db.query(Commenters.author).filter_by(video_id=video_id)

    if search:
        ts_query = func.to_tsquery('simple', ' & '.join(search.strip().split()))
        query = query.filter(
            func.to_tsvector('simple', Commenters.author).op('@@')(ts_query) |
            Commenters.author.ilike(f'%{search}%')
        )
    total = query.count()
    chatters = query.offset(offset).limit(limit).distinct().all()
    db.close()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "chatters": [c[0] for c in chatters]
    }


@router.get("/videos/chat-activity/{video_id}")
def get_chatters(
    video_id: str
):
    db = SessionLocal()

    video = db.query(Video).filter_by(video_id=video_id).first()

    if not video:
        raise HTTPException(status_code=404, detail=f"Video '{video_id}' does not exist.")
    if video.chat_status != 'IMPORTED':
        raise HTTPException(status_code=404, detail="No messages found for this video.")
    
    bucket_expr = Message.timestamp_seconds // 180

    results = (
        db.query(bucket_expr.label("bucket"), func.count().label("message_count"))
        .filter(Message.video_id == video_id)
        .group_by(bucket_expr)
        .order_by(bucket_expr)
        .all()
    )

    db.close()

    return [
        {
            "interval": f"{str(timedelta(seconds=row.bucket * 180))} – {str(timedelta(seconds=(row.bucket * 180 + 180 - 1)))}", 
            "message_count": row.message_count
         }
        for row in results
    ]