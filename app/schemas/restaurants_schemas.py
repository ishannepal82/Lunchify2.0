from pydantic import BaseModel
from typing import Optional

class ContactSchema(BaseModel):
    phone: str
    email: str

class AddressSchema(BaseModel):
    street: str
    city: str
    state: str 
    zip_code: str

class DeliveryHistoryItemSchema(BaseModel):
    order_id: str
    order_date: str
    total_price: float

class RestraurantCreateSchema(BaseModel):
    contacts: ContactSchema
    address: AddressSchema
    categories: list 
    name: str
    password: str

class RestaurantBaseSchema(BaseModel):
    contacts: ContactSchema
    address: AddressSchema
    name: str
    delivery_history: Optional[list[DeliveryHistoryItemSchema]] = []

class RestaurantLoginRequestSchema(BaseModel):
    contact: ContactSchema
    password: str 


