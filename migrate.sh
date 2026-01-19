#!/bin/bash
# Run database migrations

set -e

echo "🗄️  Running database migrations..."

docker-compose exec -T app alembic upgrade head

echo ""
echo "✅ Migrations completed!"
