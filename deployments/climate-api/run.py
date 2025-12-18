#!/usr/bin/env python3
"""
Entry point for Outerbounds deployment.
This imports the FastAPI app and keeps the process alive.
"""
from app import app
import time

if __name__ == "__main__":
    print("Climate API loaded successfully")
    print(f"App available at app:app")
    # Keep process alive
    while True:
        time.sleep(3600)
