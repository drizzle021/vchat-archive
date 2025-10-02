from scripts.fetch_all_vods import fetch_all_vods
from scripts.download_chats import download_all_chats
from scripts.import_chats import run_import
from app.utils.logging import logger

def run_pipeline():
    VODS_PER_CHANNEL = 120
    logger.info(f"Starting pipeline with {VODS_PER_CHANNEL} VODS/CHANNEL")
    fetch_all_vods(VODS_PER_CHANNEL)
    download_all_chats()
    run_import()

if __name__ == "__main__":
    run_pipeline()
