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

class OrderHistoryItemSchema(BaseModel):
    order_id: str
    order_date: str
    total_price: float

class UserBaseSchema(BaseModel):
    name: str
    hashed_password: str
    contacts: ContactSchema
    address: AddressSchema
    order_history: Optional[list[OrderHistoryItemSchema]] = []
    

class UserCreateSchema(BaseModel):
    contacts: ContactSchema
    address: AddressSchema
    name: str
    password: str

class UserResponseSchema(BaseModel):
    contacts: ContactSchema
    address: AddressSchema
    name: str
    order_history: Optional[list[OrderHistoryItemSchema]] = []

class UserLoginRequestSchema(BaseModel):
    contact: ContactSchema
    password: str 


