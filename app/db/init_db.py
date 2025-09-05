from app.db.base import Base
from app.db.session import engine
from app.models.video import Video
from app.models.message import Message

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
