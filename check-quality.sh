#!/bin/bash
# Run code quality checks

set -e

echo "📊 Running code quality checks..."

# Type checking
echo "🔍 Type checking with mypy..."
docker-compose exec -T app mypy app

# Formatting check
echo "🎨 Checking code formatting with black..."
docker-compose exec -T app black --check app tests

# Linting
echo "📝 Linting with ruff..."
docker-compose exec -T app ruff check app tests

echo ""
echo "✅ All checks passed!"
