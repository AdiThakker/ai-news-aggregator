from app.scraper.base import Scraper


class OpenAIBlogScraper(Scraper):
    def __init__(self):
        self.feed_url = "https://openai.com/news/rss.xml"

    def scrape(self):
        feed = self.fetch_feed(self.feed_url)
        results = []
        for entry in feed.entries:
            results.append(
                {
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published,
                    "summary": entry.summary,
                }
            )
        return results
