from datetime import UTC, datetime
from typing import Any

from dateutil import parser
from feedgen.feed import FeedGenerator

from twikit_rss.logger import setup_logger


class RSSGenerator:
    def __init__(self, title: str, description: str, link: str, language: str = "en"):
        self.fg = FeedGenerator()
        self.fg.title(title)
        self.fg.description(description)
        self.fg.link(href=link, rel="alternate")
        self.fg.language(language)
        self.fg.id(link)
        self.fg.generator("twikit-rss")
        self.logger = setup_logger("rss_generator")

    def add_tweets(
        self, tweets: list[Any], base_url: str = "https://twitter.com"
    ) -> None:
        """Add tweets as RSS feed entries"""
        self.logger.info(f"Adding {len(tweets)} tweets to RSS feed")
        for tweet in tweets:
            entry = self.fg.add_entry()

            # Tweet ID and URL
            tweet_url = f"{base_url}/{tweet.user.screen_name}/status/{tweet.id}"
            entry.id(tweet_url)
            entry.link(href=tweet_url)

            # Title (first 100 chars of tweet text or full text if shorter)
            title = tweet.text[:100] + "..." if len(tweet.text) > 100 else tweet.text
            entry.title(f"@{tweet.user.screen_name}: {title}")

            # Description (full tweet text)
            description = self._format_tweet_description(tweet)
            entry.description(description)

            # Publication date
            if hasattr(tweet, "created_at") and tweet.created_at:
                try:
                    if isinstance(tweet.created_at, str):
                        pub_date = parser.parse(tweet.created_at)
                    else:
                        pub_date = tweet.created_at

                    # Ensure timezone info exists
                    if pub_date.tzinfo is None:
                        pub_date = pub_date.replace(tzinfo=UTC)

                    entry.pubDate(pub_date)
                except Exception as e:
                    self.logger.warning(f"Error parsing date for tweet {tweet.id}: {e}")
                    entry.pubDate(datetime.now(UTC))
            else:
                entry.pubDate(datetime.now(UTC))

            # Author
            entry.author(
                name=f"@{tweet.user.screen_name}",
                email=f"{tweet.user.screen_name}@twitter.com",
            )

    def _format_tweet_description(self, tweet: Any) -> str:
        """Format tweet content for RSS description"""
        description = f"<p>{tweet.text}</p>"

        # Add media information if available
        if hasattr(tweet, "media") and tweet.media:
            description += "<p><strong>Media:</strong></p><ul>"
            for media in tweet.media:
                if hasattr(media, "type") and hasattr(media, "url"):
                    description += (
                        f"<li>{media.type}: <a href='{media.url}'>{media.url}</a></li>"
                    )
            description += "</ul>"

        # Add user information
        description += f"<p><strong>Author:</strong> @{tweet.user.screen_name}"
        if hasattr(tweet.user, "name"):
            description += f" ({tweet.user.name})"
        description += "</p>"

        # Add engagement metrics if available
        if hasattr(tweet, "favorite_count") and tweet.favorite_count is not None:
            description += f"<p><strong>Likes:</strong> {tweet.favorite_count}"
        if hasattr(tweet, "retweet_count") and tweet.retweet_count is not None:
            description += f" | <strong>Retweets:</strong> {tweet.retweet_count}"
        if hasattr(tweet, "reply_count") and tweet.reply_count is not None:
            description += f" | <strong>Replies:</strong> {tweet.reply_count}"
        description += "</p>"

        return description

    def generate_rss(self) -> str:
        """Generate RSS XML string"""
        return self.fg.rss_str(pretty=True).decode("utf-8")

    def save_rss(self, filename: str) -> None:
        """Save RSS feed to file"""
        self.fg.rss_file(filename)

    def generate_atom(self) -> str:
        """Generate Atom XML string"""
        return self.fg.atom_str(pretty=True).decode("utf-8")

    def save_atom(self, filename: str) -> None:
        """Save Atom feed to file"""
        self.fg.atom_file(filename)
