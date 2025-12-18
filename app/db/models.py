# SQLAlchemy models for scraped documents
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Table for OpenAI blog posts
class OpenAIBlogPost(Base):
    __tablename__ = "openai_blog_posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    link = Column(String(1024), nullable=False)
    published = Column(DateTime, nullable=False)
    text = Column(Text, nullable=False)
    # Add more fields as needed


# Table for YouTube transcripts
class YouTubeTranscript(Base):
    __tablename__ = "youtube_transcripts"
    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    link = Column(String(1024), nullable=False)
    published = Column(DateTime, nullable=False)
    text = Column(Text, nullable=False)
    video_id = Column(String(64), nullable=False)
    # Add more fields as needed
