from sqlmodel import SQLModel, Field, Column, JSON
from enum import Enum
from typing import Optional, List
from pydantic import model_validator
from datetime import datetime

# Helpers
from app.helpers.convert_date_to_str import convert_datetime_to_str
from app.helpers.random_otp_generator import generate_otp


class RestaurantSnapshotSchema(SQLModel):
    name: str
    address: str
    phone: str


class UserSnapshotSchema(SQLModel):
    name: str
    phone: str
    address: str


class OrderItemSchema(SQLModel):
    item_name: str
    item_quantity: int
    item_price: float
    item_discount: Optional[float] = 0.0


class OrderStatusEnum(str, Enum):
    COOKING = "COOKING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Order(SQLModel, table=True):
    order_id: Optional[str] = Field(default=None, primary_key=True)

    user_snapshot: UserSnapshotSchema = Field(
        sa_column=Column(JSON)
    )
    user_id: str = Field(foreign_key="users.user_id", index=True)

    restaurant_snapshot: RestaurantSnapshotSchema = Field(
        sa_column=Column(JSON)
    )
    restaurant_id: str = Field(foreign_key="restaurants.restaurant_id", index=True)

    order_items: List[OrderItemSchema] = Field(
        sa_column=Column(JSON)
    )

    approval_otp: Optional[str] = Field(default=None, nullable=True)
    total_price: float
    is_approved_by_restaurant: bool = Field(default=False)
    approved_at: Optional[str] = Field(default=None, nullable=True)
    status: Optional[OrderStatusEnum] = Field(default=None, nullable=True)

    @model_validator(mode="after")
    def validate_order_state(self):
        # Approval validation
        if self.is_approved_by_restaurant:
            if not self.approval_otp:
                raise ValueError("approval_otp must be set when order is approved")
            if self.approved_at_utc is None:
                self.approved_at_utc = convert_datetime_to_str(datetime.utcnow())
        else:
            self.approval_otp = None
            self.approved_at_utc = None

        # Restaurant approval controls order status
        if self.is_approved_by_restaurant:
            if self.status is None:
                self.status = OrderStatusEnum.COOKING
                self.approval_otp: str = generate_otp()
        else:
            self.status = None

        return self
