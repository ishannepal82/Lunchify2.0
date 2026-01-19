"""Order repository interface defining contract for order persistence."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.order.entity import Order


class IOrderRepository(ABC):
    """Interface for order repository operations.
    
    Defines the contract for order persistence operations without
    exposing implementation details.
    """

    @abstractmethod
    async def create(self, order: Order) -> Order:
        """Create a new order.
        
        Args:
            order: Order entity to persist.
            
        Returns:
            Order: Created order with generated ID.
            
        Raises:
            OrderCreationError: If creation fails.
        """
        pass

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        """Retrieve order by ID.
        
        Args:
            order_id: The order identifier.
            
        Returns:
            Optional[Order]: Order if found, None otherwise.
        """
        pass

    @abstractmethod
    async def update(self, order: Order) -> Order:
        """Update an existing order.
        
        Args:
            order: Order entity with updated data.
            
        Returns:
            Order: Updated order.
            
        Raises:
            OrderNotFoundError: If order does not exist.
        """
        pass

    @abstractmethod
    async def delete(self, order_id: UUID) -> bool:
        """Delete an order by ID.
        
        Args:
            order_id: The order identifier.
            
        Returns:
            bool: True if deleted, False if not found.
        """
        pass

    @abstractmethod
    async def list_by_user(self, user_id: UUID, limit: int = 10, offset: int = 0) -> list[Order]:
        """List orders for a specific user.
        
        Args:
            user_id: The user identifier.
            limit: Maximum number of results.
            offset: Number of results to skip.
            
        Returns:
            list[Order]: List of user's orders.
        """
        pass

    @abstractmethod
    async def list_by_restaurant(
        self, restaurant_id: UUID, limit: int = 10, offset: int = 0
    ) -> list[Order]:
        """List orders for a specific restaurant.
        
        Args:
            restaurant_id: The restaurant identifier.
            limit: Maximum number of results.
            offset: Number of results to skip.
            
        Returns:
            list[Order]: List of restaurant's orders.
        """
        pass
