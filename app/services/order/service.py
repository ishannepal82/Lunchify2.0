"""Order service with business logic."""

from typing import Optional
from uuid import UUID

from app.cache.redis_cache import RedisCache
from app.core.logging import get_logger
from app.domain.order.entity import Order, OrderStatus
from app.domain.order.exceptions import InvalidOrderStatusError, OrderNotFoundError
from app.repositories.order.interface import IOrderRepository

logger = get_logger(__name__)


class OrderService:
    """Order service containing business logic.
    
    Handles all order-related operations with proper validation,
    caching, and business rule enforcement.
    """

    CACHE_TTL = 3600  # 1 hour

    def __init__(self, repository: IOrderRepository, cache: RedisCache) -> None:
        """Initialize order service.
        
        Args:
            repository: Order repository implementation.
            cache: Cache implementation.
        """
        self.repository = repository
        self.cache = cache
        self.logger = get_logger(__name__)

    def _get_cache_key(self, order_id: UUID) -> str:
        """Generate cache key for order.
        
        Args:
            order_id: Order identifier.
            
        Returns:
            str: Cache key.
        """
        return f"order:{order_id}"

    async def create_order(
        self,
        user_id: UUID,
        restaurant_id: UUID,
        items: list[dict],
        total_price: float,
        delivery_address: str,
        special_instructions: Optional[str] = None,
    ) -> Order:
        """Create a new order.
        
        Args:
            user_id: User who is placing the order.
            restaurant_id: Restaurant fulfilling the order.
            items: List of items in the order.
            total_price: Total price of the order.
            delivery_address: Delivery address for the order.
            special_instructions: Optional special instructions.
            
        Returns:
            Order: Created order entity.
            
        Raises:
            OrderCreationError: If order creation fails validation.
        """
        order = Order(
            user_id=user_id,
            restaurant_id=restaurant_id,
            items=items,
            status=OrderStatus.PENDING,
            total_price=total_price,
            delivery_address=delivery_address,
            special_instructions=special_instructions,
        )

        created_order = await self.repository.create(order)
        await self.cache.set(self._get_cache_key(created_order.id), created_order.model_dump())

        self.logger.info("Order created successfully", order_id=str(created_order.id))
        return created_order

    async def get_order(self, order_id: UUID) -> Order:
        """Retrieve order by ID with caching.
        
        Args:
            order_id: Order identifier.
            
        Returns:
            Order: Order entity.
            
        Raises:
            OrderNotFoundError: If order not found.
        """
        # Try cache first
        cache_key = self._get_cache_key(order_id)
        cached_data = await self.cache.get(cache_key)

        if cached_data:
            self.logger.debug("Order retrieved from cache", order_id=str(order_id))
            return Order(**cached_data)

        # Fetch from repository
        order = await self.repository.get_by_id(order_id)
        if not order:
            self.logger.warning("Order not found", order_id=str(order_id))
            raise OrderNotFoundError(str(order_id))

        # Cache for future requests
        await self.cache.set(cache_key, order.model_dump(), self.CACHE_TTL)

        self.logger.info("Order retrieved from database", order_id=str(order_id))
        return order

    async def update_order(
        self,
        order_id: UUID,
        items: Optional[list[dict]] = None,
        special_instructions: Optional[str] = None,
    ) -> Order:
        """Update order details.
        
        Args:
            order_id: Order identifier.
            items: Updated items list.
            special_instructions: Updated special instructions.
            
        Returns:
            Order: Updated order entity.
            
        Raises:
            OrderNotFoundError: If order not found.
        """
        order = await self.get_order(order_id)

        if items is not None:
            order.items = items

        if special_instructions is not None:
            order.special_instructions = special_instructions

        updated_order = await self.repository.update(order)

        # Invalidate cache
        await self.cache.delete(self._get_cache_key(order_id))

        self.logger.info("Order updated", order_id=str(order_id))
        return updated_order

    async def confirm_order(self, order_id: UUID) -> Order:
        """Confirm a pending order.
        
        Args:
            order_id: Order identifier.
            
        Returns:
            Order: Confirmed order.
            
        Raises:
            OrderNotFoundError: If order not found.
            InvalidOrderStatusError: If order cannot be confirmed.
        """
        order = await self.get_order(order_id)

        try:
            order.mark_as_confirmed()
        except ValueError as e:
            self.logger.error("Cannot confirm order", order_id=str(order_id), error=str(e))
            raise InvalidOrderStatusError(str(e))

        confirmed_order = await self.repository.update(order)
        await self.cache.delete(self._get_cache_key(order_id))

        self.logger.info("Order confirmed", order_id=str(order_id))
        return confirmed_order

    async def cancel_order(self, order_id: UUID) -> Order:
        """Cancel an order.
        
        Args:
            order_id: Order identifier.
            
        Returns:
            Order: Cancelled order.
            
        Raises:
            OrderNotFoundError: If order not found.
            InvalidOrderStatusError: If order cannot be cancelled.
        """
        order = await self.get_order(order_id)

        try:
            order.mark_as_cancelled()
        except ValueError as e:
            self.logger.error("Cannot cancel order", order_id=str(order_id), error=str(e))
            raise InvalidOrderStatusError(str(e))

        cancelled_order = await self.repository.update(order)
        await self.cache.delete(self._get_cache_key(order_id))

        self.logger.info("Order cancelled", order_id=str(order_id))
        return cancelled_order

    async def delete_order(self, order_id: UUID) -> bool:
        """Delete an order.
        
        Args:
            order_id: Order identifier.
            
        Returns:
            bool: True if deleted, False if not found.
        """
        deleted = await self.repository.delete(order_id)
        if deleted:
            await self.cache.delete(self._get_cache_key(order_id))
            self.logger.info("Order deleted", order_id=str(order_id))
        return deleted

    async def get_user_orders(
        self, user_id: UUID, limit: int = 10, offset: int = 0
    ) -> list[Order]:
        """Get all orders for a user.
        
        Args:
            user_id: User identifier.
            limit: Maximum number of results.
            offset: Number of results to skip.
            
        Returns:
            list[Order]: List of user's orders.
        """
        orders = await self.repository.list_by_user(user_id, limit, offset)
        self.logger.info("Retrieved user orders", user_id=str(user_id), count=len(orders))
        return orders

    async def get_restaurant_orders(
        self, restaurant_id: UUID, limit: int = 10, offset: int = 0
    ) -> list[Order]:
        """Get all orders for a restaurant.
        
        Args:
            restaurant_id: Restaurant identifier.
            limit: Maximum number of results.
            offset: Number of results to skip.
            
        Returns:
            list[Order]: List of restaurant's orders.
        """
        orders = await self.repository.list_by_restaurant(restaurant_id, limit, offset)
        self.logger.info(
            "Retrieved restaurant orders", restaurant_id=str(restaurant_id), count=len(orders)
        )
        return orders
