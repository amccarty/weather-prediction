#!/usr/bin/env python3
"""
Climate Impact Predictor Web UI

Simple FastAPI server to serve the static dashboard files.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Climate Prediction Dashboard",
    description="Web UI for Climate Impact Predictor",
    version="1.0.0"
)

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount static files directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def read_root():
    """Serve the main dashboard page"""
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "climate-ui",
        "static_dir": STATIC_DIR,
        "static_exists": os.path.exists(STATIC_DIR)
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Climate Prediction Dashboard...")
    logger.info(f"Static files directory: {STATIC_DIR}")
    uvicorn.run(app, host="0.0.0.0", port=8001)
