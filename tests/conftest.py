"""Test configuration and fixtures."""

import asyncio
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.cache.redis_cache import RedisCache
from app.db.session import Base
from app.domain.order.entity import Order, OrderStatus
from app.infrastructure.repositories.order.sqlalchemy_repository import (
    SQLAlchemyOrderRepository,
)
from app.services.order.service import OrderService


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session.
    
    Uses in-memory SQLite for fast tests.
    """
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        future=True,
    )

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def mock_cache() -> RedisCache:
    """Create mock Redis cache."""
    cache = RedisCache()
    cache.redis_client = AsyncMock()
    return cache


@pytest_asyncio.fixture
async def order_repository(test_db_session: AsyncSession) -> SQLAlchemyOrderRepository:
    """Create order repository with test session."""
    return SQLAlchemyOrderRepository(test_db_session)


@pytest_asyncio.fixture
async def order_service(
    order_repository: SQLAlchemyOrderRepository, mock_cache: RedisCache
) -> OrderService:
    """Create order service with mock dependencies."""
    return OrderService(order_repository, mock_cache)


@pytest.fixture
def sample_order_data() -> dict:
    """Create sample order data for tests."""
    return {
        "user_id": uuid4(),
        "restaurant_id": uuid4(),
        "items": [{"item_id": "1", "name": "Pizza", "price": 10.0, "quantity": 1}],
        "total_price": 10.0,
        "delivery_address": "123 Main St",
        "special_instructions": "Extra cheese",
    }


@pytest.fixture
def sample_order(sample_order_data: dict) -> Order:
    """Create sample order entity for tests."""
    return Order(**sample_order_data)


@pytest_asyncio.fixture
async def persisted_order(
    sample_order_data: dict, order_service: OrderService
) -> Order:
    """Create and persist a sample order."""
    return await order_service.create_order(**sample_order_data)
