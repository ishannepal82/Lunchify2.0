# FastAPI Backend Service

A high-performance backend service built with **FastAPI**, featuring a PostgreSQL database, Redis-based caching and rate limiting, and a robust automated testing setup using **pytest**.

---

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

