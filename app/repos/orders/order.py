from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, JSON
from decimal import Decimal


class OrderStatusEnum(str, Enum):
    COOKING = "COOKING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    order_id: str = Field(primary_key=True, index=True)

    total_price: Decimal

    is_approved_by_restaurant: bool = Field(default=False)
    approved_at: Optional[datetime] = None
    status: Optional[OrderStatusEnum] = None
    approval_otp: Optional[str] = None

    order_items: List[Dict[str, Any]] = Field(
        sa_column=Column(JSON, nullable=False)
    )

    user_id: int = Field(foreign_key="user.user_id")

    user_snapshot: Dict[str, Any] = Field(
        sa_column=Column(JSON, nullable=False)
    )

    restaurant_id: int = Field(foreign_key="restaurant.restaurant_id")

    restaurant_snapshot: Dict[str, Any] = Field(
        sa_column=Column(JSON, nullable=False)
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)
