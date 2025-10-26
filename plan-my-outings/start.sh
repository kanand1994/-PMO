#!/bin/bash
echo "🚀 Starting Plan My Outings..."
echo "Current directory: $(pwd)"
echo "PORT: $PORT"

# Start the application using the root-level app.py
gunicorn app:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120