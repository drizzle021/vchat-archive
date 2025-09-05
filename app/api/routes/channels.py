from fastapi import APIRouter
from app.db.session import SessionLocal
from app.models.video import Video

router = APIRouter()

@router.get("/channels")
def get_channels():
    db = SessionLocal()
    return [
        row[0]
        for row in db.query(Video.channel).distinct().all()
    ]

