import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

from twikit_rss.logger import setup_logger
from twikit_rss.rss_generator import RSSGenerator
from twikit_rss.twitter_client import TwitterClient

# Load environment variables
load_dotenv()

app = FastAPI(
    title="twikit-rss",
    description="Generate RSS feeds from Twitter user timelines and lists",
    version="0.1.0",
)

logger = setup_logger("web_service")

# Global Twitter client
twitter_client = None


async def get_twitter_client() -> TwitterClient:
    """Get authenticated Twitter client"""
    global twitter_client

    if twitter_client is None or not twitter_client.authenticated:
        # Get proxy setting from environment
        proxy = os.getenv("TWITTER_PROXY")
        twitter_client = TwitterClient(proxy=proxy)

        # Try to load from cookies first
        cookies_file = str(Path.home() / ".twikit-rss" / "cookies.json")
        if Path(cookies_file).exists():
            logger.info("Loading existing cookies")
            if await twitter_client.login_with_cookies(cookies_file):
                return twitter_client

        # If cookies don't work, try environment credentials
        username = os.getenv("TWITTER_USERNAME")
        email = os.getenv("TWITTER_EMAIL")
        password = os.getenv("TWITTER_PASSWORD")

        if username and email and password:
            logger.info("Attempting login with environment credentials")
            if await twitter_client.login(username, email, password):
                # Save cookies for future use
                Path(cookies_file).parent.mkdir(parents=True, exist_ok=True)
                twitter_client.save_cookies(cookies_file)
                return twitter_client

        logger.error("Failed to authenticate Twitter client")
        raise HTTPException(status_code=500, detail="Twitter authentication failed")

    return twitter_client


@app.get("/")
async def root() -> dict:
    """Root endpoint with API information"""
    return {
        "name": "twikit-rss",
        "description": "Generate RSS feeds from Twitter timelines",
        "endpoints": {
            "user_timeline": "/user/{username}/rss",
            "list_timeline": "/list/{list_id}/rss",
        },
    }


@app.get("/user/{username}/rss", response_class=PlainTextResponse)
async def get_user_rss(
    username: str,
    count: int = 20,
    title: str | None = None,
    description: str | None = None,
) -> PlainTextResponse:
    """Generate RSS feed for a user's timeline"""
    try:
        logger.info(f"Generating RSS for user: {username} (count: {count})")

        client = await get_twitter_client()
        tweets = await client.get_user_timeline(username, count)

        if not tweets:
            raise HTTPException(
                status_code=404, detail=f"No tweets found for user: {username}"
            )

        # Generate RSS
        feed_title = title or f"Twitter Timeline: @{username}"
        feed_description = description or f"Recent tweets from @{username}"
        feed_url = f"https://twitter.com/{username}"

        rss_gen = RSSGenerator(feed_title, feed_description, feed_url)
        rss_gen.add_tweets(tweets)

        rss_content = rss_gen.generate_rss()

        # Set proper content type for RSS
        response = PlainTextResponse(
            content=rss_content, media_type="application/rss+xml; charset=utf-8"
        )

        logger.info(
            f"Successfully generated RSS for {username} with {len(tweets)} tweets"
        )
        return response

    except Exception as e:
        logger.error(f"Error generating RSS for user {username}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/list/{list_id}/rss", response_class=PlainTextResponse)
async def get_list_rss(
    list_id: str,
    count: int = 20,
    title: str | None = None,
    description: str | None = None,
) -> PlainTextResponse:
    """Generate RSS feed for a Twitter list"""
    try:
        logger.info(f"Generating RSS for list: {list_id} (count: {count})")

        client = await get_twitter_client()
        tweets = await client.get_list_timeline(list_id, count)

        if not tweets:
            raise HTTPException(
                status_code=404, detail=f"No tweets found for list: {list_id}"
            )

        # Generate RSS
        feed_title = title or f"Twitter List: {list_id}"
        feed_description = description or f"Recent tweets from Twitter list {list_id}"
        feed_url = f"https://twitter.com/i/lists/{list_id}"

        rss_gen = RSSGenerator(feed_title, feed_description, feed_url)
        rss_gen.add_tweets(tweets)

        rss_content = rss_gen.generate_rss()

        # Set proper content type for RSS
        response = PlainTextResponse(
            content=rss_content, media_type="application/rss+xml; charset=utf-8"
        )

        logger.info(
            f"Successfully generated RSS for list {list_id} with {len(tweets)} tweets"
        )
        return response

    except Exception as e:
        logger.error(f"Error generating RSS for list {list_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint"""
    return {"status": "healthy", "service": "twikit-rss"}
