from pydantic import BaseModel
from typing import List, Optional, Dict 

class OrderItemSchema(BaseModel):
    item_name: str
    item_quantity: int 
    item_price: float 
    item_discount: Optional[float] = 0.0

class RestaurantSchema(BaseModel):
    restaurant_id: str
    name: str
    address: str
    phone: str

class UserSchema(BaseModel):
    user_id: str
    name: str
    phone: str
    address: str

class OrderStatusEnum(BaseModel):
    IN_PROGRESS: str = "IN_PROGRESS"
    COOKING: str = "COOKING"
    COMPLETED: str = "COMPLETED"

class OrderBaseSchema(BaseModel):
    order_id: str 
    total_price: float 
    is_approved_by_restaurant: bool
    approved_at: Optional[str] = None
    order_status: Optional[OrderStatusEnum] = None
    orders: List[OrderItemSchema]
    restaurant: RestaurantSchema
    user: UserSchema

class OrderCreateSchema(BaseModel):
    orders: List[OrderItemSchema]
    restaurant: RestaurantSchema
    user: UserSchema
    