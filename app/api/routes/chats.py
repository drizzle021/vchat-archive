from fastapi import APIRouter, Query
from app.db.session import SessionLocal
from app.models.message import Message
from app.models.video import Video
from fastapi import HTTPException

router = APIRouter()

@router.get("/chats/{video_id}")
def get_chats(
    video_id: str,
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
):
    db = SessionLocal()

    total = db.query(Message).filter_by(video_id=video_id).count()

    if total == 0:
        video = db.query(Video).filter_by(video_id=video_id).first()
        if not video:
            raise HTTPException(status_code=404, detail=f"Video '{video_id}' does not exist.")
        raise HTTPException(status_code=404, detail="No messages found for this video.")

    messages = (
        db.query(Message)
        .filter_by(video_id=video_id)
        .order_by(Message.timestamp)
        .offset(offset)
        .limit(limit)
        .all()
    )

    db.close()

    return {
        "video_id": video_id,
        "total": total,
        "limit": limit,
        "offset": offset,
        "messages": [
            {
                "id":m.id,
                "author": m.author,
                "message": m.message,
                "timestamp": m.timestamp
            }
            for m in messages
        ]
    }
