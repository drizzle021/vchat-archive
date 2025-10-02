from app.db.base import Base
from app.db.session import engine
from app.models.video import Video
from app.models.commenters import Commenters

def init_db():
    tables_to_create = [Video.__table__, Commenters.__table__]  # Add other non-partitioned models here
    Base.metadata.create_all(bind=engine, tables=tables_to_create)

if __name__ == "__main__":
    init_db()
