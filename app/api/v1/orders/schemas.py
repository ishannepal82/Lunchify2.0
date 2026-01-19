"""Pydantic schemas for order API."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


class OrderItemSchema(BaseModel):
    """Schema for order item."""

    item_id: str
    name: str
    price: float
    quantity: int
    notes: Optional[str] = None

    @validator("price", "quantity")
    @classmethod
    def validate_positive(cls, v: float | int) -> float | int:
        """Validate positive values."""
        if v <= 0:
            raise ValueError("Price and quantity must be positive")
        return v


class CreateOrderRequest(BaseModel):
    """Schema for creating a new order."""

    user_id: UUID
    restaurant_id: UUID
    items: list[OrderItemSchema]
    total_price: float
    delivery_address: str
    special_instructions: Optional[str] = None

    @validator("total_price")
    @classmethod
    def validate_total_price(cls, v: float) -> float:
        """Validate total price is positive."""
        if v <= 0:
            raise ValueError("Total price must be positive")
        return v

    @validator("items")
    @classmethod
    def validate_items(cls, v: list) -> list:
        """Validate items list is not empty."""
        if not v or len(v) == 0:
            raise ValueError("Order must contain at least one item")
        return v


class UpdateOrderRequest(BaseModel):
    """Schema for updating an order."""

    items: Optional[list[OrderItemSchema]] = None
    special_instructions: Optional[str] = None


class ConfirmOrderRequest(BaseModel):
    """Schema for confirming an order."""

    pass


class CancelOrderRequest(BaseModel):
    """Schema for cancelling an order."""

    pass


class OrderResponse(BaseModel):
    """Schema for order response."""

    id: UUID
    user_id: UUID
    restaurant_id: UUID
    items: list[dict]
    status: str
    total_price: float
    delivery_address: str
    special_instructions: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class OrderListResponse(BaseModel):
    """Schema for order list response."""

    orders: list[OrderResponse]
    total: int
    limit: int
    offset: int


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    code: str
    message: str
    status_code: int = Field(default=400)
