from typing import Any

from twikit import Client
from twikit.user import User

from twikit_rss.logger import setup_logger


class TwitterClient:
    def __init__(self, proxy: str | None = None) -> None:
        self.client = Client("en-US", proxy=proxy)
        self.authenticated = False
        self.logger = setup_logger("twitter_client")
        if proxy:
            self.logger.info(f"Using proxy: {proxy}")

    async def login(self, username: str, email: str, password: str) -> bool:
        """Login to Twitter using credentials"""
        try:
            self.logger.info(f"Attempting login for user: {username}")
            await self.client.login(
                auth_info_1=username, auth_info_2=email, password=password
            )
            self.authenticated = True
            self.logger.info("Login successful")
            return True
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            return False

    async def login_with_cookies(self, cookies_file: str) -> bool:
        """Login using saved cookies"""
        try:
            self.logger.info(f"Loading cookies from: {cookies_file}")
            self.client.load_cookies(cookies_file)
            self.authenticated = True
            self.logger.info("Cookie login successful")
            return True
        except Exception as e:
            self.logger.error(f"Cookie login failed: {e}")
            return False

    def save_cookies(self, cookies_file: str) -> None:
        """Save authentication cookies"""
        if self.authenticated:
            self.logger.info(f"Saving cookies to: {cookies_file}")
            self.client.save_cookies(cookies_file)
        else:
            self.logger.warning("Cannot save cookies: not authenticated")

    async def get_user_timeline(self, username: str, count: int = 20) -> list[Any]:
        """Fetch tweets from a user's timeline"""
        if not self.authenticated:
            self.logger.error("Not authenticated")
            raise Exception("Not authenticated")

        try:
            self.logger.info(f"Fetching timeline for user: {username} (count: {count})")
            user = await self.client.get_user_by_screen_name(username)
            tweets = await user.get_tweets("Tweets", count=count)
            self.logger.info(f"Retrieved {len(tweets)} tweets for {username}")
            return tweets
        except Exception as e:
            self.logger.error(f"Error fetching user timeline for {username}: {e}")
            return []

    async def get_list_timeline(self, list_id: str, count: int = 20) -> list[Any]:
        """Fetch tweets from a Twitter list"""
        if not self.authenticated:
            self.logger.error("Not authenticated")
            raise Exception("Not authenticated")

        try:
            self.logger.info(f"Fetching timeline for list: {list_id} (count: {count})")
            tweets = await self.client.get_list_tweets(list_id, count=count)
            self.logger.info(f"Retrieved {len(tweets)} tweets for list {list_id}")
            return tweets
        except Exception as e:
            self.logger.error(f"Error fetching list timeline for {list_id}: {e}")
            return []

    async def search_user(self, username: str) -> User | None:
        """Search for a user by username"""
        if not self.authenticated:
            self.logger.error("Not authenticated")
            raise Exception("Not authenticated")

        try:
            self.logger.info(f"Searching for user: {username}")
            user = await self.client.get_user_by_screen_name(username)
            self.logger.info(f"Found user: {username}")
            return user
        except Exception as e:
            self.logger.error(f"Error searching for user {username}: {e}")
            return None
