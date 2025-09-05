from pathlib import Path
from app.db.session import SessionLocal
from app.models.message import Message
from app.models.video import Video
from app.services.chat_import_service import import_from_file, insert_messages
from config.settings import RAW_CHAT_DIR
from app.utils.logging import logger

path = Path(RAW_CHAT_DIR)

#list of video IDs referenced in Messages table
def get_skipped_video_ids(db):
    return {
        video.video_id
        for video in db.query(Video)
        .filter(Video.chat_status.in_(["IMPORTED", "MISSING"]))
        .all()
    }

def run_import():
    db = SessionLocal()
    skipped_ids = get_skipped_video_ids(db)

    for file in path.glob("*.json"):

        video_id = file.stem  # removes .json
        if video_id in skipped_ids:
            continue
        
        logger.info(f"Importing messages for video_id={video_id}")
        messages = import_from_file(str(file))
        

        video = db.query(Video).filter_by(video_id=video_id).first()
        
        if not video:
            continue
        
        if "error" in messages[0]:
            print(f"Skipping {video_id}: {messages[0]['error']}")
            logger.warning(f"Skipped import for {video_id}: {messages[0]['error']}. Marking as MISSING")
            video.chat_status = "MISSING"
            db.commit()
            continue
        
        insert_messages(messages, video_id)
        video.chat_status = "IMPORTED"
        db.commit()

    db.close()

if __name__ == "__main__":
    run_import()



