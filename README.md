# twikit-rss

[![uv](https://img.shields.io/badge/uv-dependency_manager-blue)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![isort](https://img.shields.io/badge/isort-imports_sorted-yellow)](https://github.com/PyCQA/isort)
[![mypy](https://img.shields.io/badge/mypy-checked-blue)](https://github.com/python/mypy)

A FastAPI web service that generates RSS feeds from Twitter user timelines and lists using [twikit](https://github.com/d60/twikit).

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd twikit-rss

# Install using uv
uv sync

# Install pre-commit hooks (optional but recommended)
pre-commit install
```

## Configuration

Create a `.env` file in the project root with your Twitter credentials:

```env
TWITTER_USERNAME=your_username
TWITTER_EMAIL=your_email@example.com
TWITTER_PASSWORD=your_password

# Optional proxy support
TWITTER_PROXY=http://proxy.example.com:8080
```

## Usage

### Starting the Service

```bash
# Start the web service
python start_server.py

# Or directly with uvicorn
uvicorn twikit_rss.app:app --host 0.0.0.0 --port 8000 --reload
```

The service will be available at `http://localhost:8000`

### API Endpoints

#### Get API Information
```http
GET /
```

#### Generate RSS feed for user timeline
```http
GET /user/{username}/rss?count=20&title=Custom+Title&description=Custom+Description
```

Example:
```bash
curl "http://localhost:8000/user/elonmusk/rss?count=10"
```

#### Generate RSS feed for Twitter list
```http
GET /list/{list_id}/rss?count=20&title=Custom+Title&description=Custom+Description
```

Example:
```bash
curl "http://localhost:8000/list/123456789/rss?count=15"
```

#### Health Check
```http
GET /health
```

### Query Parameters

All RSS endpoints support the following optional query parameters:

- `count` (int): Number of tweets to fetch (default: 20)
- `title` (string): Custom RSS feed title
- `description` (string): Custom RSS feed description

## Features

- ✅ **FastAPI Web Service** - Modern async web framework
- ✅ **RSS Feed Generation** - Standards-compliant RSS 2.0 XML
- ✅ **User Timeline Feeds** - Get RSS feeds from any public Twitter user
- ✅ **Twitter List Feeds** - Get RSS feeds from Twitter lists
- ✅ **Persistent Authentication** - Automatic cookie-based session management
- ✅ **Proxy Support** - Optional HTTP proxy configuration for network restrictions
- ✅ **Environment Configuration** - Secure credential management via `.env`
- ✅ **Configurable Parameters** - Custom titles, descriptions, and tweet counts
- ✅ **Rich Content** - Includes tweet text, author info, and engagement metrics
- ✅ **Comprehensive Logging** - Detailed logging for debugging and monitoring
- ✅ **Type Safety** - Full type annotations with mypy checking
- ✅ **Code Quality** - Pre-commit hooks with ruff linting and formatting

## Authentication

The service uses [twikit](https://github.com/d60/twikit) for Twitter authentication. It supports:

1. **Environment Variables**: Loads credentials from `.env` file
2. **Cookie Persistence**: Automatically saves and reuses authentication cookies
3. **Automatic Re-authentication**: Falls back to credentials if cookies expire

Authentication cookies are stored at: `~/.twikit-rss/cookies.json`

## Development

### Code Quality

```bash
# Run all quality checks
pre-commit run --all-files

# Individual tools
ruff check .          # Linting
ruff format .         # Formatting
mypy .               # Type checking
uv lock --check      # Dependency checks
```

## Dependencies

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework
- **[twikit](https://github.com/d60/twikit)** - Twitter API client
- **[feedgen](https://feedgen.kiesow.be/)** - RSS/Atom feed generation
- **[uvicorn](https://www.uvicorn.org/)** - ASGI server
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment variable management

### Development Dependencies

- **[ruff](https://github.com/astral-sh/ruff)** - Fast Python linter and formatter
- **[isort](https://github.com/PyCQA/isort)** - Python import sorting
- **[mypy](https://mypy.readthedocs.io/)** - Static type checker
- **[pre-commit](https://pre-commit.com/)** - Git hooks framework

## API Response Format

The RSS endpoints return valid RSS 2.0 XML with proper content-type headers:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<rss version="2.0">
  <channel>
    <title>Twitter Timeline: @username</title>
    <link>https://twitter.com/username</link>
    <description>Recent tweets from @username</description>
    <item>
      <title>@username: Tweet content...</title>
      <link>https://twitter.com/username/status/123456789</link>
      <description>Full tweet with engagement metrics</description>
      <pubDate>Wed, 30 Jul 2025 12:34:56 +0000</pubDate>
      <author>username@twitter.com (@username)</author>
    </item>
  </channel>
</rss>
```

## License

MIT License
