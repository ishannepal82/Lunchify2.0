from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, JSON
from decimal import Decimal

# Helpers
from app.helpers.convert_date_to_str import convert_datetime_to_str


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

    user: Optional["User"] = Relationship(back_populates="order_history")

    user_snapshot: Dict[str, Any] = Field(
        sa_column=Column(JSON, nullable=False)
    )
    
    restaurant_id: int = Field(foreign_key="restaurant.restaurant_id")

    restaurant: Optional["Restaurant"] = Relationship(back_populates="orders")

    restaurant_snapshot: Dict[str, Any] = Field(
        sa_column=Column(JSON, nullable=False)
    )

    created_at: str = Field(default=convert_datetime_to_str(datetime.utcnow()), index=True)
