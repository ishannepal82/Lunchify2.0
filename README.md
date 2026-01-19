# Lunchify Backend - Production-Ready FastAPI Service

A production-ready FastAPI backend with clean architecture, proper layering, testing, and infrastructure setup.

## Architecture Overview

This project implements a layered, domain-driven architecture with strict separation of concerns:

- **API Layer**: FastAPI routers and Pydantic schemas
- **Service Layer**: Business logic and orchestration
- **Domain Layer**: Entities, value objects, and domain exceptions
- **Repository Layer**: Interfaces for data access
- **Infrastructure Layer**: SQLAlchemy and Redis implementations
- **Cross-cutting Concerns**: Configuration, logging, caching, rate limiting

## Core Features

### Technology Stack

- **Framework**: FastAPI with Uvicorn
- **Database**: PostgreSQL with SQLAlchemy 2.0 async
- **Caching**: Redis with async-first implementation
- **ORM Migration**: Alembic
- **Testing**: pytest with pytest-asyncio
- **Containerization**: Docker with multi-stage builds

### Order Service Implementation

Complete implementation of an order management service including:

- **Domain Entity**: `Order` with status transitions and validation
- **Repository Pattern**: Interface-based repository with SQLAlchemy implementation
- **Service Layer**: Business logic with caching and error handling
- **API Endpoints**: CRUD operations with rate limiting
- **Redis Caching**: Automatic caching with TTL and invalidation

### API Endpoints

```
POST   /api/v1/orders                 - Create order
GET    /api/v1/orders/{order_id}      - Get order
PUT    /api/v1/orders/{order_id}      - Update order
DELETE /api/v1/orders/{order_id}      - Delete order
POST   /api/v1/orders/{order_id}/confirm - Confirm order
POST   /api/v1/orders/{order_id}/cancel  - Cancel order
GET    /api/v1/orders/user/{user_id}/orders           - Get user orders
GET    /api/v1/orders/restaurant/{restaurant_id}/orders - Get restaurant orders
GET    /health                        - Health check
```

## Project Structure

```
app/
├── api/
│   └── v1/
│       └── orders/
│           ├── router.py
│           ├── schemas.py
│           └── __init__.py
├── services/
│   └── order/
│       ├── service.py
│       └── __init__.py
├── domain/
│   └── order/
│       ├── entity.py
│       ├── exceptions.py
│       ├── value_objects.py
│       └── __init__.py
├── repositories/
│   └── order/
│       ├── interface.py
│       └── __init__.py
├── infrastructure/
│   └── repositories/
│       └── order/
│           ├── sqlalchemy_repository.py
│           └── __init__.py
├── cache/
│   ├── redis_cache.py
│   └── __init__.py
├── core/
│   ├── config.py
│   ├── exceptions.py
│   ├── logging.py
│   └── __init__.py
├── db/
│   ├── session.py
│   └── __init__.py
├── main.py
└── __init__.py

tests/
├── conftest.py
├── test_order_service.py
├── test_order_api.py
└── __init__.py

alembic/
├── env.py
├── alembic.ini
└── versions/

docker-compose.yml
Dockerfile
pyproject.toml
.env.example
README.md
```

## Quick Start

### Prerequisites

- Docker & Docker Compose (recommended)
- Python 3.11+ (for local development)

### Using Docker Compose

```bash
# Start all services
docker-compose up --build

# The API will be available at http://localhost:8000

# Health check
curl http://localhost:8000/health

# API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Local Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Set up environment
cp .env.example .env

# Start PostgreSQL and Redis
docker-compose up postgres redis

# Run migrations
alembic upgrade head

# Start the application
uvicorn app.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html
```

## Configuration

Configuration is managed through environment variables in `.env`:

```env
# Application
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/lunchify
DATABASE_ECHO=True

# Redis
REDIS_URL=redis://localhost:6379/0

# API
API_TITLE=Lunchify Backend
API_VERSION=0.1.0

# Server
HOST=0.0.0.0
PORT=8000
```

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Suite

```bash
pytest tests/test_order_service.py
pytest tests/test_order_api.py
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

## Code Quality

### Type Checking

```bash
mypy app
```

### Code Formatting

```bash
black app tests
```

### Linting

```bash
ruff check app tests
```

## Database Migrations

### Create New Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

## Logging

The application uses structured logging with `structlog`:

- Development: Pretty console output
- Production: JSON output for log aggregation

Configure log level via `LOG_LEVEL` environment variable.

## Design Patterns

### Repository Pattern

All data access is abstracted behind `IOrderRepository` interface, allowing:
- Easy swapping of implementations
- Testability with mock repositories
- Clean separation from domain logic

### Service Layer

Business logic is centralized in `OrderService`:
- No business logic in routers
- Reusable across different API versions
- Testable in isolation

### Dependency Injection

FastAPI's `Depends()` system provides:
- Loose coupling between components
- Easy testing with fixtures
- Automatic dependency resolution

### Value Objects

Immutable value objects ensure data integrity:
- `OrderItem`: Represents individual items
- `OrderSummary`: Provides order summaries

## Error Handling

Structured exception hierarchy:
- `ApplicationException`: Base exception
- `OrderNotFoundError`: Resource not found (404)
- `InvalidOrderStatusError`: Invalid state transition (422)
- `ValidationError`: Input validation failed (422)

## Performance Considerations

### Caching Strategy

- Order details cached in Redis (1 hour TTL)
- Automatic cache invalidation on updates
- `get_or_set` pattern for efficient cache usage

### Database

- Async/await for non-blocking I/O
- Connection pooling with `asyncpg`
- Indexes on frequently queried fields
- Raw SQL available for complex queries

## Production Deployment

### Docker Image

Multi-stage build produces optimized images:
- Minimal runtime dependencies
- Non-root user execution
- Health checks included

### Environment Setup

```bash
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING
```

### Database

Use managed PostgreSQL service (AWS RDS, Google Cloud SQL, etc.)

### Redis

Use managed Redis service (AWS ElastiCache, Upstash, etc.)

### Monitoring

Structured JSON logs integrate with:
- CloudWatch
- ELK Stack
- Datadog
- Any JSON log aggregator

## Security Checklist

- [ ] Use `.env` for secrets (never commit)
- [ ] Enable HTTPS in production
- [ ] Implement authentication (JWT, OAuth)
- [ ] Add rate limiting
- [ ] Validate all inputs
- [ ] Use parameterized queries (SQLAlchemy handles this)
- [ ] Regular dependency updates
- [ ] Security scanning in CI/CD

## Contributing

Follow these guidelines:

1. Type hints on all functions and variables
2. Docstrings for all public methods
3. Tests for new features (unit + integration)
4. No business logic in routers
5. Use repository pattern for data access
6. Follow PEP 8 style guide

## License

MIT License - see LICENSE file

## Support

For issues, questions, or contributions, please open an issue or pull request.

## Tech Stack

### Core Framework
- **FastAPI** – Async Python web framework
- **Uvicorn** – ASGI server

### Database
- **PostgreSQL** – Primary relational database
- **SQLAlchemy 2.0 (async)** – ORM and query builder
- **asyncpg** – High-performance PostgreSQL driver
- **Alembic** – Database migrations

> **Why this stack?**  
> SQLAlchemy (async) + asyncpg is the most widely adopted, production-proven database combination for FastAPI.

### Caching & Rate Limiting
- **Redis** – In-memory data store
- **fastapi-limiter** – Redis-backed rate limiting
- **aioredis** (via `redis-py`) – Async Redis client

### Testing
- **pytest** – Test runner
- **pytest-asyncio** – Async test support
- **httpx** – Async HTTP client for API testing
- **Testcontainers** *(optional)* – Disposable PostgreSQL/Redis containers for tests

---

## Project Structure

