import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.db.db import SessionLocal
from app.db.crud import delete_all_openai_blog_posts, delete_all_youtube_transcripts

if __name__ == "__main__":
    db = SessionLocal()
    delete_all_openai_blog_posts(db)
    delete_all_youtube_transcripts(db)
    db.close()
    print("All records deleted from OpenAI blog posts and YouTube transcripts tables.")
