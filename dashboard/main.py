"""FastAPI application for the dashboard service.

This module initialises a FastAPI server configured with Jinja2 templates
and loads required API keys from environment variables. A simple root route
renders a template to verify that the server is running correctly.
"""

from pathlib import Path
import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI(title="Dashboard")

# Set up the Jinja2 templates directory relative to this file
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Load API keys from environment variables
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
MAKE_API_KEY = os.getenv("MAKE_API_KEY")
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request) -> HTMLResponse:
    """Render the dashboard index page."""
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

