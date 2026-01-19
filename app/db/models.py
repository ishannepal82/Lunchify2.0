"""SQLAlchemy ORM models for database tables."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Float, JSON, String, UUID as SQLALCHEMY_UUID, Index
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


class OrderORM(Base):
    """SQLAlchemy ORM model for orders table."""

    __tablename__ = "orders"

    id = Column(SQLALCHEMY_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(SQLALCHEMY_UUID(as_uuid=True), nullable=False, index=True)
    restaurant_id = Column(SQLALCHEMY_UUID(as_uuid=True), nullable=False, index=True)
    items = Column(JSON, nullable=False)
    status = Column(String(50), nullable=False, index=True)
    total_price = Column(Float, nullable=False)
    delivery_address = Column(String(255), nullable=False)
    special_instructions = Column(String(500), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_orders_user_id", "user_id"),
        Index("ix_orders_restaurant_id", "restaurant_id"),
        Index("ix_orders_status", "status"),
    )

    def to_domain(self):
        """Convert ORM model to domain entity."""
        from app.domain.order.entity import Order

        return Order(
            id=self.id,
            user_id=self.user_id,
            restaurant_id=self.restaurant_id,
            items=self.items,
            status=self.status,
            total_price=self.total_price,
            delivery_address=self.delivery_address,
            special_instructions=self.special_instructions,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
