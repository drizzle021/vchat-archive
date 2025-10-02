from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.db.base import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String, ForeignKey("videos.video_id"), nullable=False)
    timestamp = Column(String, nullable=False)
    timestamp_seconds = Column(Integer, nullable=True)
    author = Column(String, nullable=False)
    message = Column(Text, nullable=False)
