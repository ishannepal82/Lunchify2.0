# Lunchify Backend - Project Index

## 📋 Start Here

### For Immediate Use
1. **[QUICKSTART.md](QUICKSTART.md)** - Get running in 2 minutes
2. Run `docker-compose up --build`
3. Access API at `http://localhost:8000/docs`

### For Understanding the Project
1. **[README.md](README.md)** - Complete overview
2. **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development guide
3. **[API_EXAMPLES.md](API_EXAMPLES.md)** - API usage

---

## 📁 Project Structure

```
Lunchify2.0/
├── app/                              # Main application
│   ├── api/v1/orders/               # API endpoints
│   │   ├── router.py                # FastAPI router
│   │   └── schemas.py               # Pydantic models
│   ├── services/order/              # Business logic
│   │   └── service.py               # OrderService
│   ├── domain/order/                # Domain models
│   │   ├── entity.py                # Order entity
│   │   ├── exceptions.py            # Domain exceptions
│   │   └── value_objects.py         # Value objects
│   ├── repositories/order/          # Repository interface
│   │   └── interface.py             # IOrderRepository
│   ├── infrastructure/repositories/order/  # Implementation
│   │   └── sqlalchemy_repository.py # SQLAlchemy impl
│   ├── cache/                       # Caching layer
│   │   └── redis_cache.py          # Redis implementation
│   ├── core/                        # Configuration
│   │   ├── config.py               # Settings
│   │   ├── logging.py              # Logging setup
│   │   └── exceptions.py           # App exceptions
│   ├── db/                          # Database
│   │   ├── session.py              # Session management
│   │   └── models.py               # ORM models
│   └── main.py                      # Application factory
├── tests/                           # Test suite
│   ├── test_order_service.py       # Service tests
│   ├── test_order_api.py           # API tests
│   └── conftest.py                 # Fixtures
├── alembic/                         # Migrations
│   ├── versions/                    # Migration files
│   │   └── 001_initial_orders.py   # Initial migration
│   ├── env.py                       # Alembic config
│   └── alembic.ini                 # INI config
├── docker-compose.yml               # Local stack
├── Dockerfile                       # Production image
├── pyproject.toml                   # Dependencies
└── .env.example                     # Environment template
```

---

## 📚 Documentation Guide

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [QUICKSTART.md](QUICKSTART.md) | Get started quickly | 5 min |
| [README.md](README.md) | Complete overview | 15 min |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Development guide | 30 min |
| [API_EXAMPLES.md](API_EXAMPLES.md) | API usage | 20 min |
| [GENERATION_SUMMARY.md](GENERATION_SUMMARY.md) | What was generated | 10 min |
| [PROJECT_CHECKLIST.md](PROJECT_CHECKLIST.md) | Complete checklist | 5 min |

---

## 🚀 Quick Commands

### Start Application
```bash
docker-compose up --build
```

### Run Tests
```bash
pytest
pytest --cov=app --cov-report=html
```

### Check Code Quality
```bash
black app tests
mypy app
ruff check app tests
```

### View API Docs
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Health Check
```bash
curl http://localhost:8000/health
```

---

## 🏗️ Architecture Overview

### Layered Architecture
```
Request
  ↓
FastAPI Router (API Layer)
  ↓
OrderService (Service Layer)
  ↓
Repository (Repository Layer)
  ↓
SQLAlchemy ORM (Infrastructure)
  ↓
PostgreSQL Database
```

### Key Design Patterns
- ✅ **Repository Pattern** - Abstract data access
- ✅ **Service Layer** - Centralize business logic
- ✅ **Dependency Injection** - Loose coupling
- ✅ **Domain-Driven Design** - Rich domain models
- ✅ **Value Objects** - Immutable data
- ✅ **Exception Hierarchy** - Structured errors

---

## 🔌 API Endpoints

### Order Management (9 endpoints)
```
POST   /api/v1/orders                 # Create
GET    /api/v1/orders/{id}           # Get
PUT    /api/v1/orders/{id}           # Update
DELETE /api/v1/orders/{id}           # Delete
POST   /api/v1/orders/{id}/confirm   # Confirm
POST   /api/v1/orders/{id}/cancel    # Cancel
GET    /api/v1/orders/user/{id}      # User orders
GET    /api/v1/orders/restaurant/{id}# Restaurant orders
GET    /health                        # Health
```

---

## 🗂️ Key Files Reference

### Configuration
- `app/core/config.py` - Environment settings
- `.env.example` - Environment template
- `pyproject.toml` - Dependencies

### Domain Models
- `app/domain/order/entity.py` - Order entity
- `app/domain/order/exceptions.py` - Domain exceptions
- `app/domain/order/value_objects.py` - Value objects

### API Layer
- `app/api/v1/orders/router.py` - Endpoints
- `app/api/v1/orders/schemas.py` - Request/response

### Business Logic
- `app/services/order/service.py` - OrderService
- `app/repositories/order/interface.py` - Repository contract
- `app/infrastructure/repositories/order/sqlalchemy_repository.py` - Implementation

### Data Access
- `app/db/session.py` - Database session
- `app/db/models.py` - ORM models
- `alembic/versions/` - Migrations

### Testing
- `tests/conftest.py` - Fixtures
- `tests/test_order_service.py` - Service tests
- `tests/test_order_api.py` - API tests

---

## 💻 Development Workflow

### 1. Local Development
```bash
# Install dependencies
pip install -e ".[dev]"

# Start services
docker-compose up postgres redis

# Run app with reload
uvicorn app.main:app --reload
```

### 2. Adding Features
1. Create domain entity
2. Create repository interface
3. Implement repository
4. Create service
5. Create API endpoints
6. Write tests

### 3. Database Changes
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

### 4. Testing
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_order_service.py::TestOrderService::test_create_order_success

# With coverage
pytest --cov=app
```

---

## 🔍 Code Examples

### Create Order (Python)
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/orders",
    json={
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "restaurant_id": "550e8400-e29b-41d4-a716-446655440001",
        "items": [{"item_id": "1", "name": "Pizza", "price": 12.99, "quantity": 1}],
        "total_price": 12.99,
        "delivery_address": "123 Main St"
    }
)
order = response.json()
```

### Service Usage
```python
from app.services.order.service import OrderService
from app.infrastructure.repositories.order.sqlalchemy_repository import SQLAlchemyOrderRepository

service = OrderService(repository, cache)
order = await service.create_order(
    user_id=user_id,
    restaurant_id=restaurant_id,
    items=items,
    total_price=total_price,
    delivery_address=address
)
```

---

## 📊 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | FastAPI | 0.109.0 |
| Server | Uvicorn | 0.27.0 |
| Validation | Pydantic | 2.5.2 |
| Database | PostgreSQL | 16 |
| ORM | SQLAlchemy | 2.0.24 |
| Async Driver | asyncpg | 0.29.0 |
| Cache | Redis | 7 |
| Migrations | Alembic | 1.13.1 |
| Testing | pytest | 7.4.3 |
| Logging | structlog | 24.1.0 |

---

## ✅ Feature Checklist

- ✅ Complete CRUD operations
- ✅ Order status management
- ✅ User order history
- ✅ Restaurant order history
- ✅ Redis caching
- ✅ Async database operations
- ✅ Comprehensive error handling
- ✅ Structured logging
- ✅ Type hints everywhere
- ✅ Full test coverage
- ✅ Docker support
- ✅ Database migrations
- ✅ API documentation
- ✅ Production-ready code

---

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check if ports are in use
lsof -i :8000
lsof -i :5432
lsof -i :6379

# Restart specific service
docker-compose restart postgres
docker-compose restart redis
docker-compose restart app
```

### Tests Failing
```bash
# Ensure services are running
docker-compose up

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_order_service.py -v
```

### Import Errors
```bash
# Reinstall dependencies
pip install -e ".[dev]"

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

## 📖 Learning Path

1. **Day 1**: Read QUICKSTART.md, start application
2. **Day 2**: Read README.md, explore API with Swagger
3. **Day 3**: Read DEVELOPMENT.md, understand architecture
4. **Day 4**: Read API_EXAMPLES.md, test all endpoints
5. **Day 5**: Review code starting with app/main.py
6. **Day 6**: Run and understand tests
7. **Day 7**: Add a new feature following the pattern

---

## 🤝 Contributing

### Code Standards
- All functions have type hints
- All public methods have docstrings
- No business logic in routers
- Use repository pattern
- Write tests for new features
- Follow PEP 8

### Before Committing
```bash
# Format code
black app tests

# Type check
mypy app

# Lint
ruff check app tests

# Test
pytest
```

---

## 📞 Support

### Issues
- Check [QUICKSTART.md](QUICKSTART.md) troubleshooting
- Check [DEVELOPMENT.md](DEVELOPMENT.md) guide
- Review relevant code comments
- Check test examples

### Resources
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Redis Docs](https://redis.io/docs/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

## 📝 License

MIT License - See LICENSE file

---

## 🎯 Summary

This is a **production-ready FastAPI backend** featuring:
- Clean layered architecture
- Comprehensive testing
- Full Docker support
- Complete API documentation
- Async throughout
- Type-safe code
- Structured logging
- Redis caching

**Ready to use immediately** with `docker-compose up --build`

---

*Generated: January 2024*
*Python 3.11+ | FastAPI 0.109.0 | PostgreSQL 16 | Redis 7*
