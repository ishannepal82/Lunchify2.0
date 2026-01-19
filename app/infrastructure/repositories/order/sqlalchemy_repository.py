"""SQLAlchemy implementation of order repository."""

from typing import Optional
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.models import OrderORM
from app.domain.order.entity import Order
from app.domain.order.exceptions import OrderNotFoundError
from app.repositories.order.interface import IOrderRepository

logger = get_logger(__name__)


class SQLAlchemyOrderRepository(IOrderRepository):
    """SQLAlchemy implementation of order repository.
    
    Handles all persistence operations for orders using SQLAlchemy
    with async/await pattern.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session.
        
        Args:
            session: AsyncSession for database operations.
        """
        self.session = session
        self.logger = get_logger(__name__)

    async def create(self, order: Order) -> Order:
        """Create a new order in the database.
        
        Args:
            order: Order entity to persist.
            
        Returns:
            Order: Created order.
        """
        model = OrderORM(
            id=order.id,
            user_id=order.user_id,
            restaurant_id=order.restaurant_id,
            items=order.items,
            status=order.status.value if hasattr(order.status, "value") else order.status,
            total_price=order.total_price,
            delivery_address=order.delivery_address,
            special_instructions=order.special_instructions,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
        self.session.add(model)
        await self.session.flush()
        self.logger.info("Order created", order_id=str(order.id))
        return order

    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        """Retrieve order by ID.
        
        Args:
            order_id: The order identifier.
            
        Returns:
            Optional[Order]: Order if found, None otherwise.
        """
        stmt = select(OrderORM).where(OrderORM.id == order_id)
        result = await self.session.execute(stmt)
        model = result.scalars().first()
        if not model:
            self.logger.warning("Order not found", order_id=str(order_id))
            return None
        return model.to_domain()

    async def update(self, order: Order) -> Order:
        """Update an existing order.
        
        Args:
            order: Order entity with updated data.
            
        Returns:
            Order: Updated order.
            
        Raises:
            OrderNotFoundError: If order does not exist.
        """
        existing = await self.get_by_id(order.id)
        if not existing:
            raise OrderNotFoundError(str(order.id))

        stmt = select(OrderORM).where(OrderORM.id == order.id)
        result = await self.session.execute(stmt)
        model = result.scalars().first()

        if model:
            model.status = order.status.value if hasattr(order.status, "value") else order.status
            model.items = order.items
            model.total_price = order.total_price
            model.delivery_address = order.delivery_address
            model.special_instructions = order.special_instructions
            model.updated_at = order.updated_at

            await self.session.flush()
            self.logger.info("Order updated", order_id=str(order.id))

        return order

    async def delete(self, order_id: UUID) -> bool:
        """Delete an order by ID.
        
        Args:
            order_id: The order identifier.
            
        Returns:
            bool: True if deleted, False if not found.
        """
        stmt = select(OrderORM).where(OrderORM.id == order_id)
        result = await self.session.execute(stmt)
        model = result.scalars().first()

        if not model:
            self.logger.warning("Order not found for deletion", order_id=str(order_id))
            return False

        await self.session.delete(model)
        await self.session.flush()
        self.logger.info("Order deleted", order_id=str(order_id))
        return True

    async def list_by_user(self, user_id: UUID, limit: int = 10, offset: int = 0) -> list[Order]:
        """List orders for a specific user.
        
        Args:
            user_id: The user identifier.
            limit: Maximum number of results.
            offset: Number of results to skip.
            
        Returns:
            list[Order]: List of user's orders.
        """
        stmt = select(OrderORM).where(OrderORM.user_id == user_id).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        self.logger.info("Orders retrieved for user", user_id=str(user_id), count=len(models))
        return [model.to_domain() for model in models]

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
        stmt = (
            select(OrderORM)
            .where(OrderORM.restaurant_id == restaurant_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        self.logger.info(
            "Orders retrieved for restaurant", restaurant_id=str(restaurant_id), count=len(models)
        )
        return [model.to_domain() for model in models]
