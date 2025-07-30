#!/usr/bin/env python3
"""
Start the twikit-rss web service
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "twikit_rss.app:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
