"""Order domain exceptions."""

from app.core.exceptions import ApplicationException


class OrderNotFoundError(ApplicationException):
    """Raised when an order is not found."""

    def __init__(self, order_id: str) -> None:
        """Initialize order not found error.
        
        Args:
            order_id: The ID of the order that was not found.
        """
        super().__init__(
            message=f"Order with ID {order_id} not found",
            code="ORDER_NOT_FOUND",
            status_code=404,
        )


class InvalidOrderStatusError(ApplicationException):
    """Raised when order status transition is invalid."""

    def __init__(self, message: str) -> None:
        """Initialize invalid order status error.
        
        Args:
            message: Description of the invalid status transition.
        """
        super().__init__(
            message=message,
            code="INVALID_ORDER_STATUS",
            status_code=422,
        )


class OrderCreationError(ApplicationException):
    """Raised when order creation fails."""

    def __init__(self, message: str) -> None:
        """Initialize order creation error.
        
        Args:
            message: Description of the creation error.
        """
        super().__init__(
            message=message,
            code="ORDER_CREATION_ERROR",
            status_code=422,
        )
