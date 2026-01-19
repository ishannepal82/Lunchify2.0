"""Unit tests for OrderService."""

import pytest
from uuid import uuid4

from app.domain.order.entity import OrderStatus
from app.domain.order.exceptions import InvalidOrderStatusError, OrderNotFoundError
from app.services.order.service import OrderService


@pytest.mark.asyncio
class TestOrderService:
    """Test cases for OrderService."""

    async def test_create_order_success(
        self, order_service: OrderService, sample_order_data: dict
    ) -> None:
        """Test successful order creation."""
        order = await order_service.create_order(**sample_order_data)

        assert order.id is not None
        assert order.user_id == sample_order_data["user_id"]
        assert order.restaurant_id == sample_order_data["restaurant_id"]
        assert order.status == OrderStatus.PENDING
        assert order.total_price == sample_order_data["total_price"]

    async def test_create_order_with_invalid_price(
        self, order_service: OrderService, sample_order_data: dict
    ) -> None:
        """Test order creation fails with invalid price."""
        sample_order_data["total_price"] = -10.0

        with pytest.raises(ValueError):
            await order_service.create_order(**sample_order_data)

    async def test_get_order_success(
        self, order_service: OrderService, persisted_order
    ) -> None:
        """Test successful order retrieval."""
        retrieved_order = await order_service.get_order(persisted_order.id)

        assert retrieved_order.id == persisted_order.id
        assert retrieved_order.user_id == persisted_order.user_id
        assert retrieved_order.status == OrderStatus.PENDING

    async def test_get_order_not_found(self, order_service: OrderService) -> None:
        """Test order retrieval fails for non-existent order."""
        with pytest.raises(OrderNotFoundError):
            await order_service.get_order(uuid4())

    async def test_confirm_order_success(
        self, order_service: OrderService, persisted_order
    ) -> None:
        """Test successful order confirmation."""
        confirmed_order = await order_service.confirm_order(persisted_order.id)

        assert confirmed_order.status == OrderStatus.CONFIRMED

    async def test_confirm_order_invalid_status(
        self, order_service: OrderService, persisted_order
    ) -> None:
        """Test confirmation fails when order is not pending."""
        await order_service.confirm_order(persisted_order.id)

        with pytest.raises(InvalidOrderStatusError):
            await order_service.confirm_order(persisted_order.id)

    async def test_cancel_order_success(
        self, order_service: OrderService, persisted_order
    ) -> None:
        """Test successful order cancellation."""
        cancelled_order = await order_service.cancel_order(persisted_order.id)

        assert cancelled_order.status == OrderStatus.CANCELLED

    async def test_cancel_confirmed_order(
        self, order_service: OrderService, persisted_order
    ) -> None:
        """Test confirmed order can be cancelled."""
        await order_service.confirm_order(persisted_order.id)
        cancelled_order = await order_service.cancel_order(persisted_order.id)

        assert cancelled_order.status == OrderStatus.CANCELLED

    async def test_cancel_completed_order_fails(
        self, order_service: OrderService, persisted_order
    ) -> None:
        """Test completed order cannot be cancelled."""
        # Manually set status to completed
        persisted_order.status = OrderStatus.COMPLETED
        await order_service.repository.update(persisted_order)

        with pytest.raises(InvalidOrderStatusError):
            await order_service.cancel_order(persisted_order.id)

    async def test_update_order_success(
        self, order_service: OrderService, persisted_order
    ) -> None:
        """Test successful order update."""
        new_items = [{"item_id": "2", "name": "Pasta", "price": 12.0, "quantity": 2}]
        new_instructions = "No onions"

        updated_order = await order_service.update_order(
            persisted_order.id,
            items=new_items,
            special_instructions=new_instructions,
        )

        assert updated_order.items == new_items
        assert updated_order.special_instructions == new_instructions

    async def test_update_non_existent_order(self, order_service: OrderService) -> None:
        """Test update fails for non-existent order."""
        with pytest.raises(OrderNotFoundError):
            await order_service.update_order(uuid4())

    async def test_delete_order_success(
        self, order_service: OrderService, persisted_order
    ) -> None:
        """Test successful order deletion."""
        result = await order_service.delete_order(persisted_order.id)

        assert result is True

        with pytest.raises(OrderNotFoundError):
            await order_service.get_order(persisted_order.id)

    async def test_delete_non_existent_order(self, order_service: OrderService) -> None:
        """Test delete returns False for non-existent order."""
        result = await order_service.delete_order(uuid4())

        assert result is False

    async def test_get_user_orders(
        self, order_service: OrderService, sample_order_data: dict
    ) -> None:
        """Test retrieving user's orders."""
        user_id = uuid4()
        sample_order_data["user_id"] = user_id

        order1 = await order_service.create_order(**sample_order_data)
        order2 = await order_service.create_order(**sample_order_data)

        orders = await order_service.get_user_orders(user_id)

        assert len(orders) >= 2

    async def test_get_restaurant_orders(
        self, order_service: OrderService, sample_order_data: dict
    ) -> None:
        """Test retrieving restaurant's orders."""
        restaurant_id = uuid4()
        sample_order_data["restaurant_id"] = restaurant_id

        order1 = await order_service.create_order(**sample_order_data)
        order2 = await order_service.create_order(**sample_order_data)

        orders = await order_service.get_restaurant_orders(restaurant_id)

        assert len(orders) >= 2

    async def test_cache_invalidation_on_update(
        self, order_service: OrderService, persisted_order
    ) -> None:
        """Test cache is invalidated on order update."""
        cache_key = order_service._get_cache_key(persisted_order.id)

        # Get order to populate cache
        await order_service.get_order(persisted_order.id)
        order_service.cache.redis_client.get.assert_called()

        # Update order
        await order_service.update_order(persisted_order.id, special_instructions="Updated")

        # Verify cache was deleted
        order_service.cache.redis_client.delete.assert_called_with(cache_key)
