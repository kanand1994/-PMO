#!/usr/bin/env python3
"""
Root level app.py for Render deployment
This imports and runs the actual app from the backend directory
"""

import sys
import os

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Change working directory to backend
os.chdir(backend_path)

# Import the actual Flask app
from app import app, socketio

if __name__ == '__main__':
    # For development
    socketio.run(app, debug=True, port=5000)
else:
    # For production (gunicorn will use this)
    application = app