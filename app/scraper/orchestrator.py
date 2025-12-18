from datetime import datetime, timedelta, timezone
from typing import List
from dateutil import parser as date_parser
from app.scraper.youtube_transcript_scraper import YouTubeTranscriptScraper
from app.scraper.openai_blog_scraper import OpenAIBlogScraper
from app.scraper.scraper_config import SCRAPER_CONFIG


class ScraperOrchestrator:
    """
    Orchestrates multiple scrapers and aggregates results within a time window.
    """

    def __init__(self, scrapers: List, hours: int = 24):
        self.scrapers = scrapers
        self.since = datetime.now(timezone.utc) - timedelta(hours=hours)

    def run(self):
        all_docs = []
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
