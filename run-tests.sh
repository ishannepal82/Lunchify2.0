#!/bin/bash
# Run tests with coverage

set -e

echo "🧪 Running tests..."

docker-compose exec -T app pytest --cov=app --cov-report=html --cov-report=term-missing

echo ""
echo "✅ Tests completed!"
echo "📊 Coverage report generated in htmlcov/index.html"
