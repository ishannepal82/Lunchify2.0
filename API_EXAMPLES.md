# API Examples and Usage Guide

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, no authentication is required. In production, add JWT bearer token to all requests:

```
Authorization: Bearer <token>
```

## Common Headers

```
Content-Type: application/json
Accept: application/json
```

---

## Order Endpoints

### 1. Create Order

**Endpoint**: `POST /orders`

**Request**:
```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "restaurant_id": "550e8400-e29b-41d4-a716-446655440001",
    "items": [
      {
        "item_id": "PIZZA_001",
        "name": "Margherita Pizza",
        "price": 12.99,
        "quantity": 2,
        "notes": "Extra cheese"
      },
      {
        "item_id": "DRINK_001",
        "name": "Coca Cola",
        "price": 2.99,
        "quantity": 1
      }
    ],
    "total_price": 31.97,
    "delivery_address": "123 Main Street, New York, NY 10001",
    "special_instructions": "Ring doorbell twice"
  }'
```

**Response** (201 Created):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "restaurant_id": "550e8400-e29b-41d4-a716-446655440001",
  "items": [
    {
      "item_id": "PIZZA_001",
      "name": "Margherita Pizza",
      "price": 12.99,
      "quantity": 2,
      "notes": "Extra cheese"
    },
    {
      "item_id": "DRINK_001",
      "name": "Coca Cola",
      "price": 2.99,
      "quantity": 1
    }
  ],
  "status": "pending",
  "total_price": 31.97,
  "delivery_address": "123 Main Street, New York, NY 10001",
  "special_instructions": "Ring doorbell twice",
  "created_at": "2024-01-19T10:30:00",
  "updated_at": "2024-01-19T10:30:00"
}
```

**Error Response** (422 Unprocessable Entity):
```json
{
  "code": "VALIDATION_ERROR",
  "message": "Total price must be positive",
  "status_code": 422
}
```

---

### 2. Get Order

**Endpoint**: `GET /orders/{order_id}`

**Request**:
```bash
curl http://localhost:8000/api/v1/orders/123e4567-e89b-12d3-a456-426614174000
```

**Response** (200 OK):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "restaurant_id": "550e8400-e29b-41d4-a716-446655440001",
  "items": [...],
  "status": "pending",
  "total_price": 31.97,
  "delivery_address": "123 Main Street, New York, NY 10001",
  "special_instructions": "Ring doorbell twice",
  "created_at": "2024-01-19T10:30:00",
  "updated_at": "2024-01-19T10:30:00"
}
```

**Error Response** (404 Not Found):
```json
{
  "code": "ORDER_NOT_FOUND",
  "message": "Order with ID 123e4567-e89b-12d3-a456-426614174000 not found",
  "status_code": 404
}
```

---

### 3. Update Order

**Endpoint**: `PUT /orders/{order_id}`

**Request**:
```bash
curl -X PUT http://localhost:8000/api/v1/orders/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "item_id": "PIZZA_002",
        "name": "Pepperoni Pizza",
        "price": 14.99,
        "quantity": 1
      }
    ],
    "special_instructions": "No onions, extra spicy"
  }'
```

**Response** (200 OK):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "restaurant_id": "550e8400-e29b-41d4-a716-446655440001",
  "items": [
    {
      "item_id": "PIZZA_002",
      "name": "Pepperoni Pizza",
      "price": 14.99,
      "quantity": 1
    }
  ],
  "status": "pending",
  "total_price": 31.97,
  "delivery_address": "123 Main Street, New York, NY 10001",
  "special_instructions": "No onions, extra spicy",
  "created_at": "2024-01-19T10:30:00",
  "updated_at": "2024-01-19T10:35:00"
}
```

---

### 4. Confirm Order

**Endpoint**: `POST /orders/{order_id}/confirm`

**Request**:
```bash
curl -X POST http://localhost:8000/api/v1/orders/123e4567-e89b-12d3-a456-426614174000/confirm \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response** (200 OK):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "restaurant_id": "550e8400-e29b-41d4-a716-446655440001",
  "items": [...],
  "status": "confirmed",
  "total_price": 31.97,
  "delivery_address": "123 Main Street, New York, NY 10001",
  "special_instructions": "Ring doorbell twice",
  "created_at": "2024-01-19T10:30:00",
  "updated_at": "2024-01-19T10:35:00"
}
```

**Error Response** (422 - Cannot confirm non-pending order):
```json
{
  "code": "INVALID_ORDER_STATUS",
  "message": "Only pending orders can be confirmed",
  "status_code": 422
}
```

---

### 5. Cancel Order

**Endpoint**: `POST /orders/{order_id}/cancel`

**Request**:
```bash
curl -X POST http://localhost:8000/api/v1/orders/123e4567-e89b-12d3-a456-426614174000/cancel \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response** (200 OK):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "restaurant_id": "550e8400-e29b-41d4-a716-446655440001",
  "items": [...],
  "status": "cancelled",
  "total_price": 31.97,
  "delivery_address": "123 Main Street, New York, NY 10001",
  "special_instructions": "Ring doorbell twice",
  "created_at": "2024-01-19T10:30:00",
  "updated_at": "2024-01-19T10:35:00"
}
```

---

### 6. Delete Order

**Endpoint**: `DELETE /orders/{order_id}`

**Request**:
```bash
curl -X DELETE http://localhost:8000/api/v1/orders/123e4567-e89b-12d3-a456-426614174000
```

**Response** (204 No Content):
```
(empty body)
```

**Error Response** (404 Not Found):
```json
{
  "code": "ORDER_NOT_FOUND",
  "message": "Order with ID 123e4567-e89b-12d3-a456-426614174000 not found",
  "status_code": 404
}
```

---

### 7. Get User Orders

**Endpoint**: `GET /orders/user/{user_id}/orders?limit=10&offset=0`

**Request**:
```bash
curl "http://localhost:8000/api/v1/orders/user/550e8400-e29b-41d4-a716-446655440000/orders?limit=20&offset=0"
```

**Response** (200 OK):
```json
{
  "orders": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "restaurant_id": "550e8400-e29b-41d4-a716-446655440001",
      "items": [...],
      "status": "confirmed",
      "total_price": 31.97,
      "delivery_address": "123 Main Street, New York, NY 10001",
      "special_instructions": "Ring doorbell twice",
      "created_at": "2024-01-19T10:30:00",
      "updated_at": "2024-01-19T10:35:00"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

---

### 8. Get Restaurant Orders

**Endpoint**: `GET /orders/restaurant/{restaurant_id}/orders?limit=10&offset=0`

**Request**:
```bash
curl "http://localhost:8000/api/v1/orders/restaurant/550e8400-e29b-41d4-a716-446655440001/orders?limit=20&offset=0"
```

**Response** (200 OK):
```json
{
  "orders": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "restaurant_id": "550e8400-e29b-41d4-a716-446655440001",
      "items": [...],
      "status": "confirmed",
      "total_price": 31.97,
      "delivery_address": "123 Main Street, New York, NY 10001",
      "special_instructions": "Ring doorbell twice",
      "created_at": "2024-01-19T10:30:00",
      "updated_at": "2024-01-19T10:35:00"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

---

### 9. Health Check

**Endpoint**: `GET /health`

**Request**:
```bash
curl http://localhost:8000/health
```

**Response** (200 OK):
```json
{
  "status": "healthy"
}
```

---

## Status Codes

| Code | Meaning | Scenarios |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT, POST (confirm/cancel) |
| 201 | Created | Order created successfully |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid request format |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation error or invalid state transition |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

---

## Order Status Flow

```
┌─────────┐
│ PENDING │
└────┬────┘
     │
     ├──────────────────────────────┐
     │                              │
     ▼                              ▼
┌───────────┐                  ┌──────────┐
│ CONFIRMED │                  │ CANCELLED│
└─────┬─────┘                  └──────────┘
      │
      ▼
 ┌──────────┐
 │PREPARING │
 └─────┬────┘
       │
       ▼
  ┌──────┐
  │READY │
  └──┬───┘
     │
     ▼
┌───────────┐
│ COMPLETED │
└───────────┘
```

---

## Using Python Requests Library

```python
import requests
import json
from uuid import uuid4

BASE_URL = "http://localhost:8000/api/v1"

# Create order
order_data = {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "restaurant_id": "550e8400-e29b-41d4-a716-446655440001",
    "items": [
        {
            "item_id": "PIZZA_001",
            "name": "Margherita Pizza",
            "price": 12.99,
            "quantity": 2
        }
    ],
    "total_price": 25.98,
    "delivery_address": "123 Main Street"
}

response = requests.post(f"{BASE_URL}/orders", json=order_data)
order = response.json()
order_id = order["id"]

# Get order
response = requests.get(f"{BASE_URL}/orders/{order_id}")
print(response.json())

# Confirm order
response = requests.post(f"{BASE_URL}/orders/{order_id}/confirm", json={})
print(response.json())

# Get user orders
response = requests.get(f"{BASE_URL}/orders/user/550e8400-e29b-41d4-a716-446655440000/orders")
print(response.json())
```

---

## Using JavaScript/Fetch

```javascript
const BASE_URL = "http://localhost:8000/api/v1";

// Create order
async function createOrder() {
  const orderData = {
    user_id: "550e8400-e29b-41d4-a716-446655440000",
    restaurant_id: "550e8400-e29b-41d4-a716-446655440001",
    items: [
      {
        item_id: "PIZZA_001",
        name: "Margherita Pizza",
        price: 12.99,
        quantity: 2
      }
    ],
    total_price: 25.98,
    delivery_address: "123 Main Street"
  };

  const response = await fetch(`${BASE_URL}/orders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(orderData)
  });

  return await response.json();
}

// Get order
async function getOrder(orderId) {
  const response = await fetch(`${BASE_URL}/orders/${orderId}`);
  return await response.json();
}

// Confirm order
async function confirmOrder(orderId) {
  const response = await fetch(`${BASE_URL}/orders/${orderId}/confirm`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({})
  });
  return await response.json();
}
```

---

## Rate Limiting

Rate limiting is enforced on order creation to prevent abuse:

**Configuration**:
```env
RATE_LIMIT_ENABLED=True
```

**Response when exceeded** (429 Too Many Requests):
```json
{
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded",
  "status_code": 429
}
```

---

## Error Handling

All errors follow a consistent format:

```json
{
  "code": "ERROR_CODE",
  "message": "Human-readable error message",
  "status_code": 400
}
```

**Common Error Codes**:
- `VALIDATION_ERROR`: Input validation failed
- `ORDER_NOT_FOUND`: Order doesn't exist
- `INVALID_ORDER_STATUS`: Invalid status transition
- `ORDER_CREATION_ERROR`: Order creation failed
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error

---

## Testing Workflow

```bash
# 1. Create multiple orders
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/v1/orders \
    -H "Content-Type: application/json" \
    -d '{
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "restaurant_id": "550e8400-e29b-41d4-a716-446655440001",
      "items": [{"item_id": "PIZZA_001", "name": "Pizza", "price": 12.99, "quantity": 1}],
      "total_price": 12.99,
      "delivery_address": "123 Main Street"
    }'
done

# 2. List user orders
curl http://localhost:8000/api/v1/orders/user/550e8400-e29b-41d4-a716-446655440000/orders

# 3. Confirm first order
# (Use order ID from creation response)
curl -X POST http://localhost:8000/api/v1/orders/{order_id}/confirm -H "Content-Type: application/json" -d '{}'

# 4. Check updated status
curl http://localhost:8000/api/v1/orders/{order_id}

# 5. Cancel order
curl -X POST http://localhost:8000/api/v1/orders/{order_id}/cancel -H "Content-Type: application/json" -d '{}'
```

---

## Performance Notes

- **Caching**: Order details are cached for 1 hour in Redis
- **Database**: Indexes on `user_id`, `restaurant_id`, and `status` for fast queries
- **Pagination**: Use `limit` and `offset` for large result sets
- **Connection Pool**: 20 connections with 0 overflow
