"""Order domain value objects."""

from typing import Any

from pydantic import BaseModel, Field, validator


class OrderItem(BaseModel):
    """Order item value object."""

    item_id: str
    name: str
    price: float
    quantity: int
    notes: str | None = None

    @validator("price", "quantity")
    @classmethod
    def validate_positive(cls, v: float | int) -> float | int:
        """Validate that price and quantity are positive."""
        if v <= 0:
            raise ValueError("Price and quantity must be positive")
        return v


class OrderSummary(BaseModel):
    """Order summary value object."""

    order_id: str
    status: str
    total_items: int
    total_price: float
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        """Convert summary to dictionary.
        
        Returns:
            dict: Dictionary representation of order summary.
        """
        return self.model_dump()
