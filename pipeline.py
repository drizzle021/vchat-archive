from scripts.fetch_all_vods import fetch_all_vods
from scripts.download_chats import download_all_chats
from scripts.import_chats import run_import

def run_pipeline():
    fetch_all_vods(20)
    download_all_chats()
    run_import()

if __name__ == "__main__":
    run_pipeline()
