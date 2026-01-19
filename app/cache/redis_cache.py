"""Redis cache implementation."""

import json
from typing import Any, Optional

import redis.asyncio as redis

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class RedisCache:
    """Redis cache wrapper for async operations.
    
    Handles all caching operations with proper serialization
    and error handling.
    """

    def __init__(self) -> None:
        """Initialize Redis cache connection."""
        self.redis_client: Optional[redis.Redis] = None

    async def connect(self) -> None:
        """Establish Redis connection."""
        try:
            self.redis_client = await redis.from_url(settings.redis_url, decode_responses=True)
            await self.redis_client.ping()
            logger.info("Connected to Redis")
        except Exception as e:
            logger.error("Failed to connect to Redis", error=str(e))
            raise

    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Disconnected from Redis")

    async def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache.
        
        Args:
            key: Cache key.
            
        Returns:
            Optional[Any]: Cached value if exists, None otherwise.
        """
        if not self.redis_client:
            logger.warning("Redis client not initialized")
            return None

        try:
            value = await self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning("Cache get failed", key=key, error=str(e))
            return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Store value in cache.
        
        Args:
            key: Cache key.
            value: Value to cache.
            ttl: Time to live in seconds.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.redis_client:
            logger.warning("Redis client not initialized")
            return False

        try:
            await self.redis_client.setex(key, ttl, json.dumps(value))
            logger.debug("Value cached", key=key, ttl=ttl)
            return True
        except Exception as e:
            logger.warning("Cache set failed", key=key, error=str(e))
            return False

    async def delete(self, key: str) -> bool:
        """Delete value from cache.
        
        Args:
            key: Cache key.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.redis_client:
            logger.warning("Redis client not initialized")
            return False

        try:
            await self.redis_client.delete(key)
            logger.debug("Cache key deleted", key=key)
            return True
        except Exception as e:
            logger.warning("Cache delete failed", key=key, error=str(e))
            return False

    async def clear(self) -> bool:
        """Clear all cache.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.redis_client:
            logger.warning("Redis client not initialized")
            return False

        try:
            await self.redis_client.flushdb()
            logger.info("Cache cleared")
            return True
        except Exception as e:
            logger.warning("Cache clear failed", error=str(e))
            return False

    async def get_or_set(
        self, key: str, factory, ttl: int = 3600
    ) -> Any:  # noqa: ANN001
        """Get value from cache or compute and cache it.
        
        Args:
            key: Cache key.
            factory: Async callable that generates value if not cached.
            ttl: Time to live in seconds.
            
        Returns:
            Any: Cached or computed value.
        """
        cached = await self.get(key)
        if cached is not None:
            logger.debug("Cache hit", key=key)
            return cached

        logger.debug("Cache miss", key=key)
        value = await factory()
        await self.set(key, value, ttl)
        return value


# Global cache instance
cache = RedisCache()
