# Quick Start Guide

## TL;DR - Get Running in 2 Minutes

### Prerequisites
- Docker & Docker Compose installed
- Git installed

### Start Application

```bash
# 1. Clone/navigate to project
cd Lunchify2.0

# 2. Copy environment file
cp .env.example .env

# 3. Start everything
docker-compose up --build

# 4. Health check (in another terminal)
curl http://localhost:8000/health
```

### Access Points

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Database**: localhost:5432 (postgres/postgres)
- **Redis**: localhost:6379

---

## Common Tasks

### Run Tests

```bash
pytest
```

### View Logs

```bash
docker-compose logs -f app
```

### Create Order

```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "restaurant_id": "550e8400-e29b-41d4-a716-446655440001",
    "items": [{"item_id": "1", "name": "Pizza", "price": 12.99, "quantity": 1}],
    "total_price": 12.99,
    "delivery_address": "123 Main St"
  }'
```

### Get Order

```bash
curl http://localhost:8000/api/v1/orders/{order_id}
```

### Stop Services

```bash
docker-compose down
```

### Clean Up Everything

```bash
docker-compose down -v
```

---

## File Locations

| Task | File |
|------|------|
| Main App | `app/main.py` |
| Configuration | `app/core/config.py` |
| Database Models | `app/db/models.py` |
| Order Service | `app/services/order/service.py` |
| Order API | `app/api/v1/orders/router.py` |
| Tests | `tests/test_order_*.py` |
| Migrations | `alembic/versions/` |
| Environment | `.env.example` |
| Docker | `docker-compose.yml` |

---

## Architecture

```
API Request
    ↓
FastAPI Router (app/api/v1/orders/router.py)
    ↓
Service (app/services/order/service.py)
    ↓
Repository (app/infrastructure/repositories/order/sqlalchemy_repository.py)
    ↓
Database (PostgreSQL)
```

---

## For Developers

### Local Setup (Without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -e ".[dev]"

# Start services in Docker
docker-compose up postgres redis

# Run app
uvicorn app.main:app --reload
```

### Code Quality Checks

```bash
# Format code
black app tests

# Type check
mypy app

# Lint
ruff check app tests
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

---

## Troubleshooting

### Port 8000 Already in Use

```bash
lsof -i :8000
kill -9 <PID>
```

### Database Connection Error

```bash
docker-compose restart postgres
docker-compose logs postgres
```

### Tests Failing

```bash
# Ensure services are up
docker-compose up

# Run tests in verbose mode
pytest -v
```

### Python Import Errors

```bash
# Reinstall
pip install -e ".[dev]"

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

## Key Concepts

### Repository Pattern
- Interface in `app/repositories/order/interface.py`
- Implementation in `app/infrastructure/repositories/order/sqlalchemy_repository.py`
- Allows swapping implementations without changing services

### Service Layer
- Business logic in `app/services/order/service.py`
- No business logic in routers
- All services injectable via FastAPI `Depends()`

### Domain Entities
- `Order` entity in `app/domain/order/entity.py`
- Validation in Pydantic models
- Business rules enforced

### Caching
- Redis cache in `app/cache/redis_cache.py`
- Automatic cache invalidation on updates
- 1-hour TTL by default

---

## Next Steps

1. **Read full documentation**: See `DEVELOPMENT.md` and `API_EXAMPLES.md`
2. **Explore code**: Start with `app/main.py`, then `app/api/v1/orders/`
3. **Run tests**: `pytest -v` to understand the system
4. **Add features**: Follow the pattern for orders in other domains
5. **Deploy**: Use `Dockerfile` for production deployments

---

## Support Files

- **README.md**: Full project documentation
- **DEVELOPMENT.md**: Detailed development guide
- **API_EXAMPLES.md**: API usage examples
- **pyproject.toml**: Dependencies and configuration
- **.env.example**: Environment template

---

## Production Checklist

- [ ] Change database URL to managed service (AWS RDS, etc.)
- [ ] Change Redis URL to managed service (AWS ElastiCache, etc.)
- [ ] Set `ENVIRONMENT=production` and `DEBUG=False`
- [ ] Configure authentication (JWT, OAuth)
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting appropriately
- [ ] Set up CI/CD pipeline
- [ ] Run security scanning
- [ ] Set up database backups
- [ ] Configure health checks
