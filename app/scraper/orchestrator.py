from datetime import datetime, timedelta, timezone
from typing import List
from dateutil import parser as date_parser
from app.scraper.youtube_transcript_scraper import YouTubeTranscriptScraper
from app.scraper.openai_blog_scraper import OpenAIBlogScraper
from app.scraper.scraper_config import SCRAPER_CONFIG
from app.db.db import SessionLocal
from app.db.crud import insert_openai_blog_post, insert_youtube_transcript


class ScraperOrchestrator:
    """
    Orchestrates multiple scrapers and aggregates results within a time window.
    """

    def __init__(self, scrapers: List, hours: int = 24):
        self.scrapers = scrapers
        self.since = datetime.now(timezone.utc) - timedelta(hours=hours)

    def run(self):
        all_docs = []
        db = SessionLocal()
        for scraper in self.scrapers:
            docs = scraper.scrape()
            for doc in docs:
                pub_str = getattr(doc, "published", None) or doc.get("published", None)
                pub_dt = None
                if pub_str:
                    try:
                        pub_dt = date_parser.parse(pub_str)
                    except Exception:
                        pass
                if pub_dt and pub_dt > self.since:
                    all_docs.append(doc)
                    # Insert into DB based on type
                    if "video_id" in doc and doc.get("video_id"):
                        transcript_text = doc.get("text") or doc.get("transcript")
                        if transcript_text:
                            insert_youtube_transcript(
                                db,
                                title=doc.get("title"),
                                link=doc.get("link"),
                                published=pub_dt,
                                text=transcript_text,
                                video_id=doc.get("video_id"),
                            )
                        else:
                            print(
                                f"Skipping YouTube video with missing transcript: {doc.get('title')} ({doc.get('link')})"
                            )
                    else:
                        insert_openai_blog_post(
                            db,
                            title=doc.get("title"),
                            link=doc.get("link"),
                            published=pub_dt,
                            text=doc.get("text") or doc.get("summary"),
                        )
        db.close()
        return all_docs


# Example usage
if __name__ == "__main__":
    scrapers = []
    for channel_id in SCRAPER_CONFIG["youtube_channels"]:
        scrapers.append(YouTubeTranscriptScraper(channel_id=channel_id))
    for feed_url in SCRAPER_CONFIG["blogs"]:
        scrapers.append(OpenAIBlogScraper(feed_url=feed_url))
    orchestrator = ScraperOrchestrator(scrapers, hours=24)
    recent_docs = orchestrator.run()
    print(f"Found {len(recent_docs)} documents in the last 24 hours.")
    for doc in recent_docs[:3]:
        print(doc)
