from sqlalchemy.orm import Session
from app.db.models import OpenAIBlogPost, YouTubeTranscript
from datetime import datetime


def delete_all_openai_blog_posts(db: Session):
    """Delete all OpenAI blog posts from the database."""
    db.query(OpenAIBlogPost).delete()
    db.commit()


def delete_all_youtube_transcripts(db: Session):
    """Delete all YouTube transcripts from the database."""
    db.query(YouTubeTranscript).delete()
    db.commit()


def insert_openai_blog_post(
    db: Session, title: str, link: str, published: datetime, text: str
):
    post = OpenAIBlogPost(title=title, link=link, published=published, text=text)
    # Prevent duplicate by link
    existing = db.query(OpenAIBlogPost).filter_by(link=link).first()
    if existing:
        return existing
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def insert_youtube_transcript(
    db: Session, title: str, link: str, published: datetime, text: str, video_id: str
):
    transcript = YouTubeTranscript(
        title=title, link=link, published=published, text=text, video_id=video_id
    )
    # Prevent duplicate by video_id
    existing = db.query(YouTubeTranscript).filter_by(video_id=video_id).first()
    if existing:
        return existing
    db.add(transcript)
    db.commit()
    db.refresh(transcript)
    return transcript


def get_openai_blog_posts(db: Session, limit: int = 10):
    return (
        db.query(OpenAIBlogPost)
        .order_by(OpenAIBlogPost.published.desc())
        .limit(limit)
        .all()
    )


def get_youtube_transcripts(db: Session, limit: int = 10):
    return (
        db.query(YouTubeTranscript)
        .order_by(YouTubeTranscript.published.desc())
        .limit(limit)
        .all()
    )
