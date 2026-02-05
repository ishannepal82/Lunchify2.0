from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class OrderStatusEnum(str, Enum):
    COOKING = "COOKING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class OrderItemSchema(BaseModel):
    item_name: str
    item_quantity: int
    item_price: float
    item_discount: Optional[float] = 0.0


class UserSnapshotSchema(BaseModel):
    name: str
    phone: str
    address: str


class RestaurantSnapshotSchema(BaseModel):
    name: str
    address: str
    phone: str


class OrderBaseSchema(BaseModel):
    order_id: str
    total_price: float
    is_approved_by_restaurant: bool = False
    approved_at: Optional[str] = None
    status: Optional[OrderStatusEnum] = None
    order_items: List[OrderItemSchema]
    user_snapshot: UserSnapshotSchema
    restaurant_snapshot: RestaurantSnapshotSchema
    approval_otp: Optional[str] = None


class OrderCreateSchema(BaseModel):
    order_items: List[OrderItemSchema]
    user_snapshot: UserSnapshotSchema
    restaurant_snapshot: RestaurantSnapshotSchema
