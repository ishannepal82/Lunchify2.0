from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from datetime import datetime
from typing import List
from uuid import uuid4

# Helpers
from app.helpers.convert_date_to_str import convert_datetime_to_str

# Schemas
class ContactsSchema(SQLModel):
    phone: str
    email: str

class AddressSchema(SQLModel):
    city: str 
    state: str 
    street: str


class User(SQLModel, table=True):
    user_id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True
    )

    name: str = Field(index=True)

    contact: ContactsSchema = Field(sa_column=Column(JSON))
    address: AddressSchema = Field(sa_column=Column(JSON))

    hashed_password: str = Field(nullable=False)

    order_history: List[dict] = Field(
        default_factory=list,
        sa_column=Column(JSON)
    )

    created_at: str = Field(
        default_factory=lambda: convert_datetime_to_str(datetime.utcnow()),
        index=True
    )

    updated_at: str = Field(
        default_factory=lambda: convert_datetime_to_str(datetime.utcnow()),
        index=True
    )
