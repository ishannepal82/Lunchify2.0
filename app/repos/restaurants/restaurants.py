from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from typing import List
from datetime import datetime

# Helpers
from app.helpers.convert_date_to_str import convert_datetime_to_str

# Schemas
class ContactsSchema(SQLModel):
    phone: str 
    email: str 

class AddressSchema(SQLModel): 
    street: str
    city: str
    state: str 
    zip_code: str

class Restaurant(SQLModel, table=True):
    restaurant_id: str = Field(primary_key=True, index=True)
    name: str = Field(index=True)
    contact: ContactsSchema = Field(sa_column=Column(JSON))
    address: AddressSchema = Field(sa_column=Column(JSON))
    category: List[str] = Field(sa_column=Column(JSON))
    orders: List["Order"] = Relationship(back_populates="restaurant")
    created_at: str = Field(default=convert_datetime_to_str(datetime.utcnow()), index=True)

