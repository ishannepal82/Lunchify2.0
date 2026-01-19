"""FastAPI router for order endpoints."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.orders.schemas import (
    CancelOrderRequest,
    ConfirmOrderRequest,
    CreateOrderRequest,
    ErrorResponse,
    OrderListResponse,
    OrderResponse,
    UpdateOrderRequest,
)
from app.cache.redis_cache import cache
from app.core.exceptions import ApplicationException
from app.core.logging import get_logger
from app.db.session import get_session
from app.domain.order.exceptions import OrderNotFoundError
from app.infrastructure.repositories.order.sqlalchemy_repository import (
    SQLAlchemyOrderRepository,
)
from app.services.order.service import OrderService

logger = get_logger(__name__)

router = APIRouter(prefix="/orders", tags=["orders"])


async def get_order_service(session: AsyncSession = Depends(get_session)) -> OrderService:
    """Dependency to get order service instance.
    
    Args:
        session: Database session.
        
    Returns:
        OrderService: Service instance.
    """
    repository = SQLAlchemyOrderRepository(session)
    return OrderService(repository, cache)


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        422: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
    },
)
async def create_order(
    request: CreateOrderRequest,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    """Create a new order.
    
    Args:
        request: Order creation request.
        service: Order service.
        
    Returns:
        OrderResponse: Created order.
        
    Raises:
        HTTPException: If creation fails.
    """
    try:
        items = [item.model_dump() for item in request.items]
        order = await service.create_order(
            user_id=request.user_id,
            restaurant_id=request.restaurant_id,
            items=items,
            total_price=request.total_price,
            delivery_address=request.delivery_address,
            special_instructions=request.special_instructions,
        )
        logger.info("Order created via API", order_id=str(order.id))
        return OrderResponse(**order.model_dump())
    except ApplicationException as e:
        logger.error("Order creation failed", error=str(e))
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error("Unexpected error creating order", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    responses={
        404: {"model": ErrorResponse},
    },
)
async def get_order(
    order_id: UUID,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    """Retrieve an order by ID.
    
    Args:
        order_id: Order identifier.
        service: Order service.
        
    Returns:
        OrderResponse: Order details.
        
    Raises:
        HTTPException: If order not found.
    """
    try:
        order = await service.get_order(order_id)
        logger.info("Order retrieved via API", order_id=str(order_id))
        return OrderResponse(**order.model_dump())
    except OrderNotFoundError as e:
        logger.warning("Order not found", order_id=str(order_id))
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        logger.error("Error retrieving order", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put(
    "/{order_id}",
    response_model=OrderResponse,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def update_order(
    order_id: UUID,
    request: UpdateOrderRequest,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    """Update an order.
    
    Args:
        order_id: Order identifier.
        request: Update request.
        service: Order service.
        
    Returns:
        OrderResponse: Updated order.
        
    Raises:
        HTTPException: If update fails.
    """
    try:
        items = None
        if request.items:
            items = [item.model_dump() for item in request.items]

        order = await service.update_order(
            order_id=order_id,
            items=items,
            special_instructions=request.special_instructions,
        )
        logger.info("Order updated via API", order_id=str(order_id))
        return OrderResponse(**order.model_dump())
    except OrderNotFoundError as e:
        logger.warning("Order not found for update", order_id=str(order_id))
        raise HTTPException(status_code=404, detail=e.message)
    except ApplicationException as e:
        logger.error("Order update failed", error=str(e))
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error("Error updating order", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{order_id}/confirm",
    response_model=OrderResponse,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def confirm_order(
    order_id: UUID,
    request: ConfirmOrderRequest,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    """Confirm a pending order.
    
    Args:
        order_id: Order identifier.
        request: Confirm request.
        service: Order service.
        
    Returns:
        OrderResponse: Confirmed order.
        
    Raises:
        HTTPException: If confirmation fails.
    """
    try:
        order = await service.confirm_order(order_id)
        logger.info("Order confirmed via API", order_id=str(order_id))
        return OrderResponse(**order.model_dump())
    except OrderNotFoundError as e:
        logger.warning("Order not found for confirmation", order_id=str(order_id))
        raise HTTPException(status_code=404, detail=e.message)
    except ApplicationException as e:
        logger.error("Order confirmation failed", error=str(e))
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error("Error confirming order", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{order_id}/cancel",
    response_model=OrderResponse,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def cancel_order(
    order_id: UUID,
    request: CancelOrderRequest,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    """Cancel an order.
    
    Args:
        order_id: Order identifier.
        request: Cancel request.
        service: Order service.
        
    Returns:
        OrderResponse: Cancelled order.
        
    Raises:
        HTTPException: If cancellation fails.
    """
    try:
        order = await service.cancel_order(order_id)
        logger.info("Order cancelled via API", order_id=str(order_id))
        return OrderResponse(**order.model_dump())
    except OrderNotFoundError as e:
        logger.warning("Order not found for cancellation", order_id=str(order_id))
        raise HTTPException(status_code=404, detail=e.message)
    except ApplicationException as e:
        logger.error("Order cancellation failed", error=str(e))
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error("Error cancelling order", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse},
    },
)
async def delete_order(
    order_id: UUID,
    service: OrderService = Depends(get_order_service),
) -> None:
    """Delete an order.
    
    Args:
        order_id: Order identifier.
        service: Order service.
        
    Raises:
        HTTPException: If order not found.
    """
    try:
        deleted = await service.delete_order(order_id)
        if not deleted:
            logger.warning("Order not found for deletion", order_id=str(order_id))
            raise HTTPException(status_code=404, detail="Order not found")
        logger.info("Order deleted via API", order_id=str(order_id))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error deleting order", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/user/{user_id}/orders",
    response_model=OrderListResponse,
)
async def get_user_orders(
    user_id: UUID,
    limit: int = 10,
    offset: int = 0,
    service: OrderService = Depends(get_order_service),
) -> OrderListResponse:
    """Get all orders for a user.
    
    Args:
        user_id: User identifier.
        limit: Maximum number of results.
        offset: Number of results to skip.
        service: Order service.
        
    Returns:
        OrderListResponse: List of user's orders.
    """
    try:
        orders = await service.get_user_orders(user_id, limit, offset)
        logger.info("User orders retrieved via API", user_id=str(user_id))
        return OrderListResponse(
            orders=[OrderResponse(**order.model_dump()) for order in orders],
            total=len(orders),
            limit=limit,
            offset=offset,
        )
    except Exception as e:
        logger.error("Error retrieving user orders", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/restaurant/{restaurant_id}/orders",
    response_model=OrderListResponse,
)
async def get_restaurant_orders(
    restaurant_id: UUID,
    limit: int = 10,
    offset: int = 0,
    service: OrderService = Depends(get_order_service),
) -> OrderListResponse:
    """Get all orders for a restaurant.
    
    Args:
        restaurant_id: Restaurant identifier.
        limit: Maximum number of results.
        offset: Number of results to skip.
        service: Order service.
        
    Returns:
        OrderListResponse: List of restaurant's orders.
    """
    try:
        orders = await service.get_restaurant_orders(restaurant_id, limit, offset)
        logger.info("Restaurant orders retrieved via API", restaurant_id=str(restaurant_id))
        return OrderListResponse(
            orders=[OrderResponse(**order.model_dump()) for order in orders],
            total=len(orders),
            limit=limit,
            offset=offset,
        )
    except Exception as e:
        logger.error("Error retrieving restaurant orders", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")
