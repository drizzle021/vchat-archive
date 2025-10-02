from sqlalchemy import Column, String
from app.db.base import Base

class Commenters(Base):
    __tablename__ = "commenters"

    author = Column(String, primary_key=True)
    video_id = Column(String, primary_key=True)
