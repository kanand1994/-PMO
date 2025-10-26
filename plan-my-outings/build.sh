#!/bin/bash
set -e

echo "🏗️ Building Plan My Outings..."
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# Build frontend
echo "📦 Building frontend..."
if [ -d "frontend" ]; then
    cd frontend
    npm install
    npm run build
    cd ..
    echo "✅ Frontend build complete!"
else
    echo "❌ Frontend directory not found!"
    exit 1
fi

# Install backend dependencies
echo "🐍 Installing backend dependencies..."
if [ -d "backend" ]; then
    pip install -r backend/requirements.txt
    echo "✅ Backend dependencies installed!"
else
    echo "❌ Backend directory not found!"
    exit 1
fi

echo "✅ Build complete!"