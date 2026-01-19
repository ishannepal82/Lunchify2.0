"""Integration tests for order API endpoints."""

import pytest
from httpx import AsyncClient
from uuid import uuid4

from app.main import app


@pytest.mark.asyncio
class TestOrderAPI:
    """Test cases for order API endpoints."""

    async def test_health_check(self) -> None:
        """Test health check endpoint."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "healthy"}

    async def test_create_order_success(self) -> None:
        """Test successful order creation via API."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            payload = {
                "user_id": str(uuid4()),
                "restaurant_id": str(uuid4()),
                "items": [
                    {
                        "item_id": "1",
                        "name": "Pizza",
                        "price": 10.0,
                        "quantity": 1,
                    }
                ],
                "total_price": 10.0,
                "delivery_address": "123 Main St",
                "special_instructions": "Extra cheese",
            }

            response = await client.post("/api/v1/orders", json=payload)
            assert response.status_code == 201
            data = response.json()
            assert data["status"] == "pending"
            assert data["total_price"] == 10.0

    async def test_create_order_invalid_price(self) -> None:
        """Test order creation fails with invalid price."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            payload = {
                "user_id": str(uuid4()),
                "restaurant_id": str(uuid4()),
                "items": [
                    {
                        "item_id": "1",
                        "name": "Pizza",
                        "price": 10.0,
                        "quantity": 1,
                    }
                ],
                "total_price": -10.0,
                "delivery_address": "123 Main St",
            }

            response = await client.post("/api/v1/orders", json=payload)
            assert response.status_code == 422

    async def test_create_order_missing_items(self) -> None:
        """Test order creation fails with empty items."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            payload = {
                "user_id": str(uuid4()),
                "restaurant_id": str(uuid4()),
                "items": [],
                "total_price": 10.0,
                "delivery_address": "123 Main St",
            }

            response = await client.post("/api/v1/orders", json=payload)
            assert response.status_code == 422

    async def test_get_order_not_found(self) -> None:
        """Test getting non-existent order returns 404."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            order_id = uuid4()
            response = await client.get(f"/api/v1/orders/{order_id}")
            assert response.status_code == 404

    async def test_confirm_order_success(self) -> None:
        """Test successful order confirmation via API."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Create order
            payload = {
                "user_id": str(uuid4()),
                "restaurant_id": str(uuid4()),
                "items": [
                    {
                        "item_id": "1",
                        "name": "Pizza",
                        "price": 10.0,
                        "quantity": 1,
                    }
                ],
                "total_price": 10.0,
                "delivery_address": "123 Main St",
            }

            create_response = await client.post("/api/v1/orders", json=payload)
            order_id = create_response.json()["id"]

            # Confirm order
            confirm_response = await client.post(
                f"/api/v1/orders/{order_id}/confirm", json={}
            )
            assert confirm_response.status_code == 200
            assert confirm_response.json()["status"] == "confirmed"

    async def test_cancel_order_success(self) -> None:
        """Test successful order cancellation via API."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Create order
            payload = {
                "user_id": str(uuid4()),
                "restaurant_id": str(uuid4()),
                "items": [
                    {
                        "item_id": "1",
                        "name": "Pizza",
                        "price": 10.0,
                        "quantity": 1,
                    }
                ],
                "total_price": 10.0,
                "delivery_address": "123 Main St",
            }

            create_response = await client.post("/api/v1/orders", json=payload)
            order_id = create_response.json()["id"]

            # Cancel order
            cancel_response = await client.post(
                f"/api/v1/orders/{order_id}/cancel", json={}
            )
            assert cancel_response.status_code == 200
            assert cancel_response.json()["status"] == "cancelled"

    async def test_delete_order_success(self) -> None:
        """Test successful order deletion via API."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Create order
            payload = {
                "user_id": str(uuid4()),
                "restaurant_id": str(uuid4()),
                "items": [
                    {
                        "item_id": "1",
                        "name": "Pizza",
                        "price": 10.0,
                        "quantity": 1,
                    }
                ],
                "total_price": 10.0,
                "delivery_address": "123 Main St",
            }

            create_response = await client.post("/api/v1/orders", json=payload)
            order_id = create_response.json()["id"]

            # Delete order
            delete_response = await client.delete(f"/api/v1/orders/{order_id}")
            assert delete_response.status_code == 204

            # Verify it's deleted
            get_response = await client.get(f"/api/v1/orders/{order_id}")
            assert get_response.status_code == 404

    async def test_get_user_orders(self) -> None:
        """Test retrieving user's orders via API."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            user_id = uuid4()

            # Create orders for user
            for _ in range(2):
                payload = {
                    "user_id": str(user_id),
                    "restaurant_id": str(uuid4()),
                    "items": [
                        {
                            "item_id": "1",
                            "name": "Pizza",
                            "price": 10.0,
                            "quantity": 1,
                        }
                    ],
                    "total_price": 10.0,
                    "delivery_address": "123 Main St",
                }
                await client.post("/api/v1/orders", json=payload)

            # Get user orders
            response = await client.get(f"/api/v1/orders/user/{user_id}/orders")
            assert response.status_code == 200
            data = response.json()
            assert len(data["orders"]) >= 2

    async def test_get_restaurant_orders(self) -> None:
        """Test retrieving restaurant's orders via API."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            restaurant_id = uuid4()

            # Create orders for restaurant
            for _ in range(2):
                payload = {
                    "user_id": str(uuid4()),
                    "restaurant_id": str(restaurant_id),
                    "items": [
                        {
                            "item_id": "1",
                            "name": "Pizza",
                            "price": 10.0,
                            "quantity": 1,
                        }
                    ],
                    "total_price": 10.0,
                    "delivery_address": "123 Main St",
                }
                await client.post("/api/v1/orders", json=payload)

            # Get restaurant orders
            response = await client.get(f"/api/v1/orders/restaurant/{restaurant_id}/orders")
            assert response.status_code == 200
            data = response.json()
            assert len(data["orders"]) >= 2
