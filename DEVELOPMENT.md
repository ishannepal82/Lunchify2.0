# Lunchify Backend - Development Guide

## Overview

This document provides detailed guidance on developing and deploying the Lunchify backend service.

## Prerequisites

### System Requirements

- **OS**: Linux, macOS, or Windows (with WSL2)
- **Docker**: 20.10+ and Docker Compose 2.0+
- **Python**: 3.11+ (for local development)
- **Git**: 2.20+

### Development Tools

```bash
# macOS with Homebrew
brew install python@3.11 docker docker-compose git

# Ubuntu/Debian
sudo apt-get install python3.11 docker.io docker-compose git

# Windows
# Use Docker Desktop with WSL2 backend
# Use Windows Terminal for best experience
```

## Getting Started

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd Lunchify2.0

# Copy environment file
cp .env.example .env

# Start services
docker-compose up --build
```

The application will be available at `http://localhost:8000`.

### 2. API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### 3. Health Check

```bash
curl http://localhost:8000/health
# Response: {"status": "healthy"}
```

## Development Workflow

### Local Development

```bash
# Install dependencies with dev extras
pip install -e ".[dev]"

# Start database and cache in containers
docker-compose up postgres redis

# In another terminal, run the app with reload
uvicorn app.main:app --reload

# App runs at http://localhost:8000
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_order_service.py

# With coverage
pytest --cov=app --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Code Quality

```bash
# Type checking
mypy app

# Format code
black app tests

# Check formatting
black --check app tests

# Linting
ruff check app tests

# Fix linting issues
ruff check --fix app tests
```

## Architecture

### Layered Architecture

```
┌─────────────────────────────────────┐
│         API Layer (FastAPI)         │
│  - Routers, Schemas, Dependencies   │
├─────────────────────────────────────┤
│       Service Layer (Business)      │
│  - OrderService, Caching Logic      │
├─────────────────────────────────────┤
│       Domain Layer (Entities)       │
│  - Order Entity, Exceptions         │
├─────────────────────────────────────┤
│    Repository Layer (Interface)     │
│  - IOrderRepository                 │
├─────────────────────────────────────┤
│  Infrastructure Layer (Implementation)
│  - SQLAlchemy Repository, Redis     │
└─────────────────────────────────────┘
```

### Data Flow

```
Request
  ↓
FastAPI Router
  ↓
Service Layer (Business Logic)
  ↓
Repository Layer (Data Access)
  ↓
SQLAlchemy ORM
  ↓
PostgreSQL Database
```

## Adding New Features

### 1. Define Domain Entity

Create new entity in `app/domain/<domain>/entity.py`:

```python
from pydantic import BaseModel

class YourEntity(BaseModel):
    id: UUID
    name: str
    # Add fields with validation
    
    class Config:
        use_enum_values = True
```

### 2. Create Repository Interface

Define interface in `app/repositories/<domain>/interface.py`:

```python
from abc import ABC, abstractmethod

class IYourRepository(ABC):
    @abstractmethod
    async def create(self, entity: YourEntity) -> YourEntity:
        pass
```

### 3. Implement Repository

Create implementation in `app/infrastructure/repositories/<domain>/sqlalchemy_repository.py`:

```python
from sqlalchemy.ext.asyncio import AsyncSession

class SQLAlchemyYourRepository(IYourRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, entity: YourEntity) -> YourEntity:
        # Implementation
        pass
```

### 4. Create Service

Define service in `app/services/<domain>/service.py`:

```python
class YourService:
    def __init__(self, repository: IYourRepository, cache: RedisCache):
        self.repository = repository
        self.cache = cache
    
    async def create(self, **kwargs) -> YourEntity:
        # Business logic
        entity = YourEntity(**kwargs)
        return await self.repository.create(entity)
```

### 5. Create API Endpoints

Define router in `app/api/v1/<domain>/router.py`:

```python
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/<domain>", tags=["<domain>"])

@router.post("")
async def create(
    request: CreateRequest,
    service: YourService = Depends(get_your_service),
):
    entity = await service.create(**request.dict())
    return YourResponse(**entity.dict())
```

### 6. Create Tests

```bash
# Unit tests in tests/test_your_service.py
# Integration tests in tests/test_your_api.py
```

## Database Management

### Create Migration

```bash
# Auto-generate migration
alembic revision --autogenerate -m "Add new feature"

# Edit alembic/versions/XXX_add_new_feature.py
```

### Apply Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific number of migrations
alembic upgrade +2

# Rollback
alembic downgrade -1
```

### Reset Database

```bash
# Delete all data and tables
docker-compose exec postgres psql -U postgres -d lunchify -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Recreate tables
alembic upgrade head
```

## Caching

### Cache Keys

Use consistent key format:

```python
def _get_cache_key(self, entity_id: UUID) -> str:
    return f"entity:{entity_id}"
```

### Cache Patterns

```python
# Direct get/set
await cache.get(key)
await cache.set(key, value, ttl=3600)

# Get or compute
value = await cache.get_or_set(key, factory_func, ttl=3600)

# Invalidation
await cache.delete(key)
```

## Error Handling

### Define Exceptions

```python
from app.core.exceptions import ApplicationException

class MyError(ApplicationException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="MY_ERROR",
            status_code=400,
        )
```

### Handle in Router

```python
@router.get("/{id}")
async def get_item(id: UUID):
    try:
        item = await service.get(id)
        return ItemResponse(**item.dict())
    except MyError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
```

## Logging

### Structured Logging

```python
from app.core.logging import get_logger

logger = get_logger(__name__)

# Log events
logger.info("Order created", order_id=str(order.id), user_id=str(order.user_id))
logger.warning("Order not found", order_id=str(order_id))
logger.error("Database error", error=str(e))
```

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially problematic situations
- **ERROR**: Error messages for serious problems
- **CRITICAL**: Critical errors that may stop the application

## Production Deployment

### Environment Variables

```env
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING

# Use managed services
DATABASE_URL=postgresql+asyncpg://user:pass@rds-endpoint:5432/lunchify
REDIS_URL=redis://:password@redis-endpoint:6379/0
```

### Docker Build

```bash
# Build production image
docker build -t lunchify-backend:1.0.0 .

# Push to registry
docker tag lunchify-backend:1.0.0 myregistry.azurecr.io/lunchify-backend:1.0.0
docker push myregistry.azurecr.io/lunchify-backend:1.0.0
```

### Deployment Platforms

**AWS ECS**:
```bash
# Create task definition, service, and load balancer
# Use RDS for PostgreSQL
# Use ElastiCache for Redis
```

**Google Cloud Run**:
```bash
# Deploy container
gcloud run deploy lunchify-backend \
  --image gcr.io/project/lunchify-backend \
  --platform managed
```

**Kubernetes**:
```yaml
# Create deployment, service, configmap, secret
# Use managed PostgreSQL and Redis services
```

## Monitoring and Debugging

### Health Check Endpoint

```bash
curl http://localhost:8000/health
```

### View Application Logs

```bash
# Docker Compose
docker-compose logs -f app

# Docker (production)
docker logs -f container_name
```

### Database Connection Check

```bash
docker-compose exec postgres psql -U postgres -d lunchify -c "SELECT version();"
```

### Redis Connection Check

```bash
docker-compose exec redis redis-cli ping
```

### API Load Testing

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/health

# Using wrk
wrk -t12 -c400 -d30s http://localhost:8000/health
```

## Troubleshooting

### Port Already in Use

```bash
# Find and kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
docker-compose up -e PORT=8001
```

### Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart service
docker-compose restart postgres
```

### Redis Connection Error

```bash
# Check Redis is running
docker-compose ps redis

# Verify connection
docker-compose exec redis redis-cli ping

# Restart service
docker-compose restart redis
```

### Import Errors

```bash
# Verify Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/Lunchify2.0"

# Verify installed packages
pip list

# Reinstall in development mode
pip install -e ".[dev]"
```

## Performance Tuning

### Database Optimization

```python
# Create indexes
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);

# Use EXPLAIN for query analysis
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = '...';
```

### Caching Strategy

```python
# Increase TTL for stable data
cache_ttl = 3600 * 24  # 24 hours

# Use cache tags for bulk invalidation
await cache.set(f"user:{user_id}:orders", orders, ttl=3600)
```

### Connection Pool

```python
# Configured in create_async_engine
pool_size = 20
max_overflow = 0
```

## Contributing

### Code Standards

1. **Type Hints**: All functions must have type hints
2. **Docstrings**: All public methods must have docstrings
3. **Testing**: New features require tests (unit + integration)
4. **No Business Logic in Routers**: Use service layer
5. **Repository Pattern**: All data access through repositories
6. **PEP 8**: Follow style guide

### Pull Request Process

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes with tests
3. Run quality checks: `./check-quality.sh`
4. Commit with descriptive messages
5. Push and create pull request
6. Wait for review and CI/CD checks

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://pydantic-settings.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

## Support

For issues or questions:
1. Check the README.md
2. Review relevant code comments
3. Check similar implementations
4. Open an issue with:
   - Description of problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
