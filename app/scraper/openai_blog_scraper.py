from app.scraper.base import Scraper


class OpenAIBlogScraper(Scraper):
    """
    Scraper for the OpenAI blog RSS feed.
    Inherits from Scraper and sets a custom User-Agent header.
    """

    def __init__(self, feed_url="https://openai.com/news/rss.xml"):
        """Initialize with a feed URL (default: OpenAI RSS)."""
        self.feed_url = feed_url

    def fetch_feed(self, url):
        """Fetch the RSS feed with a custom User-Agent header."""
        return super().fetch_feed(url, request_headers={"User-Agent": "Mozilla/5.0"})

    def scrape(self):
        """Parse the feed and return a list of blog post dicts."""
        feed = self.fetch_feed(self.feed_url)
        results = []
        for entry in feed.entries:
            results.append(
                {
                    "title": entry.get("title"),
                    "link": entry.get("link"),
                    "published": entry.get("published"),
                    "summary": entry.get("summary"),
                }
            )
        return results


if __name__ == "__main__":
    scraper = OpenAIBlogScraper()
    results = scraper.scrape()
    for post in results[:3]:
        print(post)
