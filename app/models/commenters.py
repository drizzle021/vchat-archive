from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Commenters(Base):
    __tablename__ = "commenters"

    author = Column(String, primary_key=True)
    video_id = Column(String, primary_key=True)
