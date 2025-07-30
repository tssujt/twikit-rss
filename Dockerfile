# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Create directory for twikit cookies
RUN mkdir -p /root/.twikit-rss

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8000

# Run the application
CMD ["uv", "run", "uvicorn", "twikit_rss.app:app", "--host", "0.0.0.0", "--port", "8000"]
