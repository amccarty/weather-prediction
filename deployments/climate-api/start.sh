#!/bin/bash
# Startup script for Climate API deployment
uvicorn app:app --host 0.0.0.0 --port 8080
