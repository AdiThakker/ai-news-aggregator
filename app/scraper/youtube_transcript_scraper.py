from app.scraper.base import Scraper
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)
from urllib.parse import urlparse, parse_qs


class YouTubeTranscriptScraper(Scraper):
    """
    Scraper for YouTube channel transcripts via RSS feed and youtube-transcript-api.
    """

    def __init__(self, channel_id):
        """Initialize with a YouTube channel ID."""
        self.channel_id = channel_id
        self.feed_url = (
            f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        )

    def get_video_id_from_url(self, url):
        """Extract the video ID from a YouTube URL."""
        parsed_url = urlparse(url)
        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            return parse_qs(parsed_url.query).get("v", [None])[0]
        elif parsed_url.hostname == "youtu.be":
            return parsed_url.path[1:]
        return None

    def fetch_transcript(self, video_id):
        """Fetch the transcript for a given video ID."""
        try:
            transcript = YouTubeTranscriptApi.fetch(video_id)
            return " ".join([entry["text"] for entry in transcript])
        except (TranscriptsDisabled, NoTranscriptFound):
            return None
        except Exception as e:
            print(f"Error fetching transcript for {video_id}: {e}")
            return None

    def scrape(self):
        """Scrape the channel's RSS feed and return video info and transcripts."""
        feed = self.fetch_feed(self.feed_url)
        results = []
        for entry in feed.entries:
            video_id = self.get_video_id_from_url(entry.link)
            if not video_id:
                print(f"Skipping entry with invalid video_id: {entry.link}")
                continue
            transcript = self.fetch_transcript(video_id)
            results.append(
                {
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published,
                    "video_id": video_id,
                    "transcript": transcript,
                }
            )
        return results


# Module-level function for interactive/CLI use
def scrape_youtube_channel(channel_id):
    """
    Scrape a YouTube channel's RSS feed and return a list of dicts with video info and transcripts.
    """
    scraper = YouTubeTranscriptScraper(channel_id)
    return scraper.scrape()


if __name__ == "__main__":
    # For VS Code Interactive Window support
    try:
        from IPython import get_ipython

        if get_ipython():
            print(
                "You are running in an interactive environment. Use the scrape_youtube_channel(channel_id) function directly."
            )
            print("Example: scrape_youtube_channel('UC_x5XG1OV2P6uZZ5FSM9Ttw')")
    except ImportError:
        pass
    # Fallback to CLI mode
    channel_ids = [
        "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Example: Google Developers
    ]
    for cid in channel_ids:
        print(f"Scraping channel: {cid}")
        videos = scrape_youtube_channel(cid)
        for video in videos:
            print(f"Title: {video['title']}")
            print(f"Link: {video['link']}")
            print(f"Published: {video['published']}")
            transcript = video["transcript"]
            if transcript:
                print(f"Transcript: {transcript[:200]}...\n")
            else:
                print("Transcript: None\n")
