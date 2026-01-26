from sqlmodel import SQLModel, Field, Column, JSON
from enum import Enum
from typing import Optional, Dict, List
from pydantic import model_validator
from datetime import datetime

# Helpers
from app.helpers.convert_date_to_str import convert_datetime_to_str

class RestaurantSchema(SQLModel):
    restaurant_id: str
    name: str
    address: str
    phone: str

class UserSchema(SQLModel):
    user_id: str
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
    order_id: str | None = Field(default=None, primary_key=True)
    user: Dict[str, UserSchema] = Field(sa_column=Column(JSON))
    restaurant: Dict[str,RestaurantSchema] = Field(sa_column=Column(JSON))
    order: List[OrderItemSchema] = Field(sa_column=Column(JSON))
    otp: Optional[str] = Field(default=None, nullable=True) 
    total_price: float 
    is_approved_by_restaurant: bool = Field(default=False)
    approved_at: Optional[str] = Field(default=None, nullable=True)
    order_status: Optional[OrderStatusEnum] = Field(default=None, nullable=True)

    @model_validator(mode="after")
    def validate_order_state(self):
        # Approval validation
        if self.is_approved_by_restaurant:
            if not self.otp:
                raise ValueError("otp must be set when order is approved")
            if self.approved_at is None:
                self.approved_at = convert_datetime_to_str(datetime.utcnow())
        else:
            self.otp = None
            self.approved_at = None

        # Restaurant approval controls order status
        if self.is_approved_by_restaurant:
            if self.order_status is None:
                self.order_status = OrderStatusEnum.COOKING
        else:
            self.order_status = None

        return self

