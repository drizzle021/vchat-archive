from fastapi import APIRouter
from app.api.routes import videos, chats, channels

router = APIRouter()

router.include_router(videos.router)
router.include_router(chats.router)
router.include_router(channels.router)