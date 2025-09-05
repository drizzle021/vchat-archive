from sqlalchemy import Column, String
from app.db.base import Base

class Video(Base):
    __tablename__ = "videos"

    video_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    chat_status=Column(String, default="PENDING")
