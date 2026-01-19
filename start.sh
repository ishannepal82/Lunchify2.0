#!/bin/bash
# Startup script for development environment

set -e

echo "🚀 Starting Lunchify Backend..."

# Check if Docker is running
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    exit 1
fi

echo "📦 Building and starting containers..."
docker-compose up --build

echo "✅ Application started!"
echo ""
echo "🌐 Access the application:"
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo "   ReDoc: http://localhost:8000/redoc"
echo "   Health: http://localhost:8000/health"
echo ""
echo "🗄️  Database:"
echo "   Host: localhost:5432"
echo "   User: postgres"
echo "   Password: postgres"
echo "   Database: lunchify"
echo ""
echo "💾 Redis:"
echo "   Host: localhost:6379"
