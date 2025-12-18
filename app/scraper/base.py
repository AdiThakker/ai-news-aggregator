import feedparser


class Scraper:
    def fetch_feed(self, url):
        return feedparser.parse(url)
