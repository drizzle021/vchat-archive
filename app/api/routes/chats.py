from fastapi import APIRouter, Query
from app.db.session import SessionLocal
from app.models.message import Message

router = APIRouter()

@router.get("/chats/{video_id}")
def get_chats(
    video_id: str,
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
):
    db = SessionLocal()

    total = db.query(Message).filter_by(video_id=video_id).count()

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
                "author": m.author,
                "message": m.message,
                "timestamp": m.timestamp
            }
            for m in messages
        ]
    }
