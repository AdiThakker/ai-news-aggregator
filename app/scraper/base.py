import feedparser


class Scraper:
    def fetch_feed(self, url, **kwargs):
        """
        Fetch and parse an RSS/Atom feed.
        Accepts extra keyword arguments for feedparser.parse (e.g., request_headers).
        """
        return feedparser.parse(url, **kwargs)
