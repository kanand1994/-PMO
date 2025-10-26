#!/bin/bash
set -e

echo "🏗️ Building Plan My Outings..."

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Install backend dependencies
echo "🐍 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

echo "✅ Build complete!"