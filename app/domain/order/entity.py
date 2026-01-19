"""Order domain entity."""

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


class OrderStatus(str, Enum):
    """Order status enumeration."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(BaseModel):
    """Order domain entity.
    
    Represents the core business entity for an order with validation
    and business rule enforcement.
    """

    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    restaurant_id: UUID
    items: list[dict] = Field(default_factory=list)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    total_price: float
    delivery_address: str
    special_instructions: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("total_price")
    @classmethod
    def validate_total_price(cls, v: float) -> float:
        """Validate that total price is positive.
        
        Args:
            v: Price value to validate.
            
        Returns:
            float: Validated price.
            
        Raises:
            ValueError: If price is not positive.
        """
        if v <= 0:
            raise ValueError("Total price must be positive")
        return v

    @validator("items")
    @classmethod
    def validate_items(cls, v: list[dict]) -> list[dict]:
        """Validate that items list is not empty.
        
        Args:
            v: Items list to validate.
            
        Returns:
            list[dict]: Validated items list.
            
        Raises:
            ValueError: If items list is empty.
        """
        if not v or len(v) == 0:
            raise ValueError("Order must contain at least one item")
        return v

    @validator("delivery_address")
    @classmethod
    def validate_delivery_address(cls, v: str) -> str:
        """Validate delivery address is not empty.
        
        Args:
            v: Address string to validate.
            
        Returns:
            str: Validated address.
            
        Raises:
            ValueError: If address is empty.
        """
        if not v or len(v.strip()) == 0:
            raise ValueError("Delivery address cannot be empty")
        return v.strip()

    class Config:
        """Pydantic configuration."""

        use_enum_values = True

    def mark_as_confirmed(self) -> None:
        """Mark order as confirmed.
        
        Raises:
            ValueError: If order is not in pending status.
        """
        if self.status != OrderStatus.PENDING:
            raise ValueError("Only pending orders can be confirmed")
        self.status = OrderStatus.CONFIRMED
        self.updated_at = datetime.utcnow()

    def mark_as_cancelled(self) -> None:
        """Mark order as cancelled.
        
        Raises:
            ValueError: If order cannot be cancelled in current status.
        """
        cancellable_statuses = {OrderStatus.PENDING, OrderStatus.CONFIRMED}
        if self.status not in cancellable_statuses:
            raise ValueError(f"Cannot cancel order in {self.status} status")
        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.utcnow()

    def is_completed(self) -> bool:
        """Check if order is completed.
        
        Returns:
            bool: True if order status is completed.
        """
        return self.status == OrderStatus.COMPLETED
