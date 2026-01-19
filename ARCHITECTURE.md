# Architecture Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            API Layer (v1/orders)                     │   │
│  │  - POST   /orders                 (create)           │   │
│  │  - GET    /orders/{id}            (retrieve)         │   │
│  │  - PUT    /orders/{id}            (update)           │   │
│  │  - DELETE /orders/{id}            (delete)           │   │
│  │  - POST   /orders/{id}/confirm    (confirm)          │   │
│  │  - POST   /orders/{id}/cancel     (cancel)           │   │
│  │  - GET    /orders/user/{id}       (list by user)     │   │
│  │  - GET    /orders/restaurant/{id} (list by rest)     │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Service Layer (OrderService)               │   │
│  │  - create_order()                                    │   │
│  │  - get_order()        (with caching)                │   │
│  │  - update_order()     (cache invalidation)          │   │
│  │  - confirm_order()                                   │   │
│  │  - cancel_order()                                    │   │
│  │  - delete_order()                                    │   │
│  │  - get_user_orders()                                 │   │
│  │  - get_restaurant_orders()                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│                ┌──────────┴──────────┐                      │
│                │                     │                      │
│                ▼                     ▼                      │
│  ┌────────────────────────┐  ┌──────────────────────────┐  │
│  │ Repository Pattern     │  │  Redis Cache             │  │
│  │ (IOrderRepository)     │  │  - get()                 │  │
│  │ - create()             │  │  - set() with TTL        │  │
│  │ - get_by_id()          │  │  - delete()              │  │
│  │ - update()             │  │  - get_or_set()          │  │
│  │ - delete()             │  │  - clear()               │  │
│  │ - list_by_user()       │  │                          │  │
│  │ - list_by_restaurant() │  └──────────────────────────┘  │
│  └────────────────────────┘                                 │
│                │                                             │
│                ▼                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │    SQLAlchemy Repository Implementation              │   │
│  │    - Async database operations                       │   │
│  │    - ORM model mapping                               │   │
│  │    - Query building                                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                │                                             │
│                ▼                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Domain Layer                                │   │
│  │  Order Entity:                                       │   │
│  │  - id: UUID                                          │   │
│  │  - user_id: UUID                                     │   │
│  │  - restaurant_id: UUID                               │   │
│  │  - items: list                                       │   │
│  │  - status: OrderStatus (enum)                        │   │
│  │  - total_price: float                                │   │
│  │  - delivery_address: str                             │   │
│  │  - special_instructions: str (optional)              │   │
│  │                                                       │   │
│  │  Value Objects:                                      │   │
│  │  - OrderItem                                         │   │
│  │  - OrderSummary                                      │   │
│  │                                                       │   │
│  │  Exceptions:                                         │   │
│  │  - OrderNotFoundError                                │   │
│  │  - InvalidOrderStatusError                           │   │
│  │  - OrderCreationError                                │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
    ┌──────────────────┐      ┌──────────────────┐
    │   PostgreSQL     │      │      Redis       │
    │   Database       │      │      Cache       │
    │   - orders table │      │   (1hr TTL)      │
    │   - 3 indexes    │      │                  │
    │   - asyncpg      │      │  (Async Python)  │
    │   - pooling (20) │      │                  │
    └──────────────────┘      └──────────────────┘
```

---

## Request Flow Diagram

```
HTTP Request
    │
    ▼
FastAPI Router (/api/v1/orders/{path})
    │
    ├─ Validate request with Pydantic schema
    ├─ Extract path/query parameters
    │
    ▼
Dependency Injection (Depends)
    │
    ├─ Get AsyncSession (database connection)
    ├─ Create SQLAlchemy repository
    ├─ Create OrderService
    │
    ▼
Service Layer (OrderService)
    │
    ├─ Check cache (Redis)
    │   ├─ HIT  → Return cached data
    │   └─ MISS → Continue to repository
    │
    ├─ Call repository method
    │   ├─ create()         → Create ORM model → Flush → Return
    │   ├─ get_by_id()      → Query → Map to domain entity
    │   ├─ update()         → Query → Update fields → Flush
    │   ├─ delete()         → Query → Delete → Flush
    │   ├─ list_by_user()   → Query with filter → Map list
    │
    ├─ Cache result (if applicable)
    ├─ Log operation
    │
    ▼
API Response
    │
    ├─ Serialize with Pydantic response schema
    ├─ Set HTTP status code
    ├─ Return JSON response
    │
    ▼
HTTP Response
```

---

## Data Persistence Layer

```
┌─────────────────────────────────────────────────────────┐
│            Application Domain Layer                     │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Order(BaseModel)                               │    │
│  │  - Pydantic validation                          │    │
│  │  - Business logic methods                       │    │
│  │  - Status transitions                           │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                        │
                        │ to_domain() / from_domain()
                        │
┌─────────────────────────────────────────────────────────┐
│       Infrastructure Mapping Layer                      │
│  ┌─────────────────────────────────────────────────┐    │
│  │  OrderORM (SQLAlchemy declarative)              │    │
│  │  - ORM column mappings                          │    │
│  │  - Table/Index definitions                      │    │
│  │  - Conversion methods                           │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                        │
                        │ SQLAlchemy ORM
                        │
┌─────────────────────────────────────────────────────────┐
│                  Database Layer                        │
│                                                         │
│  PostgreSQL Table: orders                              │
│  ├─ id (UUID, PK)                                      │
│  ├─ user_id (UUID, indexed)                            │
│  ├─ restaurant_id (UUID, indexed)                      │
│  ├─ items (JSON)                                       │
│  ├─ status (VARCHAR, indexed)                          │
│  ├─ total_price (FLOAT)                                │
│  ├─ delivery_address (VARCHAR)                         │
│  ├─ special_instructions (VARCHAR, nullable)           │
│  ├─ created_at (TIMESTAMP)                             │
│  └─ updated_at (TIMESTAMP)                             │
└─────────────────────────────────────────────────────────┘
```

---

## Order Status State Machine

```
┌─────────┐
│ PENDING │ ◄─────────────────────────────────────────┐
└────┬────┘                                            │
     │                                                  │
     │ confirm_order()                                 │
     ▼                                                  │
┌───────────┐                                          │
│ CONFIRMED │                                          │
└─────┬─────┘                                          │
      │                                                 │
      │ (automatic progression)                        │
      ▼                                                 │
┌──────────┐                                           │
│ PREPARING│                                           │
└─────┬────┘                                           │
      │                                                 │
      │ (automatic progression)                        │
      ▼                                                 │
 ┌──────┐                                              │
 │READY │                                              │
 └──┬───┘                                              │
    │                                                   │
    │ (automatic progression)                          │
    ▼                                                   │
┌───────────┐                                          │
│ COMPLETED │                                          │
└───────────┘                                          │
                                                        │
  cancel_order() available from:                       │
  - PENDING ──────────────────────────────────────────┘
  - CONFIRMED ────────────────────────────────────────┐
                                                      │
                                                      ▼
                                              ┌──────────────┐
                                              │  CANCELLED   │
                                              └──────────────┘
```

---

## Caching Strategy

```
Request for Order
    │
    ▼
Is order in cache?
    │
    ├─ YES (cache hit)
    │   │
    │   ├─ Increment cache hit counter
    │   ├─ Log cache hit
    │   │
    │   ▼
    │   Return cached Order from memory (instant)
    │
    └─ NO (cache miss)
        │
        ├─ Query database
        ├─ Parse SQL result to Order entity
        ├─ Store in cache with TTL=3600 seconds
        ├─ Log cache miss
        │
        ▼
        Return Order from database

On Update/Delete:
    │
    ├─ Invalidate cache key
    ├─ Update/delete in database
    ├─ Log cache invalidation
    │
    ▼
    Success
```

---

## Error Handling Flow

```
API Request
    │
    ▼
Validate Input (Pydantic)
    │
    ├─ Validation Failed
    │   │
    │   ▼
    │   ValidationError (422)
    │   {
    │     "code": "VALIDATION_ERROR",
    │     "message": "...",
    │     "status_code": 422
    │   }
    │
    └─ Validation Passed
        │
        ▼
    Execute Service Method
        │
        ├─ Order Not Found
        │   │
        │   ▼
        │   OrderNotFoundError (404)
        │   {
        │     "code": "ORDER_NOT_FOUND",
        │     "message": "Order with ID ... not found",
        │     "status_code": 404
        │   }
        │
        ├─ Invalid Status Transition
        │   │
        │   ▼
        │   InvalidOrderStatusError (422)
        │   {
        │     "code": "INVALID_ORDER_STATUS",
        │     "message": "Cannot confirm non-pending order",
        │     "status_code": 422
        │   }
        │
        ├─ Database Error
        │   │
        │   ▼
        │   ApplicationException (500)
        │   {
        │     "code": "INTERNAL_ERROR",
        │     "message": "Internal server error",
        │     "status_code": 500
        │   }
        │
        └─ Success
            │
            ▼
            Serialize Response
            Return 200/201
```

---

## Dependency Injection Flow

```
HTTP Request
    │
    ▼
FastAPI Router receives request
    │
    ▼
Extract dependencies from function signature
    │
    ├─ session: AsyncSession = Depends(get_session)
    │   │
    │   ▼
    │   Call get_session()
    │   │
    │   ▼
    │   Create async context manager
    │   │
    │   ▼
    │   Return AsyncSession
    │
    ├─ service: OrderService = Depends(get_order_service)
    │   │
    │   ▼
    │   Call get_order_service(session)
    │   │
    │   ▼
    │   Create SQLAlchemyOrderRepository(session)
    │   │
    │   ▼
    │   Create OrderService(repository, cache)
    │   │
    │   ▼
    │   Return service instance
    │
    ▼
Call route handler with resolved dependencies
    │
    ▼
Handler can now use:
    - session: database connection
    - service: fully initialized service
    
    ▼
Route handler executes
    │
    ▼
Clean up: close session
```

---

## Docker Compose Services

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Network                         │
│                  (lunchify-network)                        │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            FastAPI Application                       │  │
│  │            (Port: 8000 → 8000)                       │  │
│  │                                                       │  │
│  │  - Environment variables configured                 │  │
│  │  - Volumes: source code mounted                     │  │
│  │  - Depends on: postgres, redis                      │  │
│  │  - Health check: /health endpoint                   │  │
│  │  - Command: uvicorn with reload                     │  │
│  └──────────────────────────────────────────────────────┘  │
│         │                              │                   │
│         │ tcp://postgres:5432          │ tcp://redis:6379  │
│         │                              │                   │
│  ┌──────┴──────────────────────┐  ┌────┴──────────────┐   │
│  │     PostgreSQL 16           │  │   Redis 7        │   │
│  │   (Port: 5432 → 5432)       │  │ (Port: 6379 →    │   │
│  │                              │  │       6379)      │   │
│  │ - Image: postgres:16-alpine │  │                  │   │
│  │ - Volume: postgres_data     │  │ - Image:         │   │
│  │ - Env: user/password/db     │  │   redis:7-alpine │   │
│  │ - Health check: pg_isready  │  │ - Volume:        │   │
│  │                              │  │   redis_data     │   │
│  │                              │  │ - Health check:  │   │
│  │                              │  │   redis-cli ping │   │
│  └──────────────────────────────┘  └──────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Internet                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Load Balancer│
                  │  (Optional)  │
                  └──────┬───────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌─────────┐      ┌─────────┐     ┌─────────┐
   │Container│      │Container│     │Container│
   │Instance1│      │Instance2│ ... │InstanceN│
   │(App)    │      │(App)    │     │(App)    │
   └────┬────┘      └────┬────┘     └────┬────┘
        │                │                │
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
            ┌─────────────────────────┐
            │  Managed Services       │
            │                         │
            │  ┌──────────────────┐   │
            │  │ RDS PostgreSQL   │   │
            │  │ (Multi-AZ)       │   │
            │  └──────────────────┘   │
            │                         │
            │  ┌──────────────────┐   │
            │  │ ElastiCache      │   │
            │  │ Redis (Replicas) │   │
            │  └──────────────────┘   │
            │                         │
            └─────────────────────────┘
```

---

## Development vs Production

```
┌──────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  docker-compose up                                           │
│  ├─ PostgreSQL (localhost:5432)                             │
│  ├─ Redis (localhost:6379)                                  │
│  └─ FastAPI (localhost:8000, reload enabled)                │
│                                                               │
│  Environment:                                                │
│  ├─ DEBUG=True                                              │
│  ├─ LOG_LEVEL=INFO                                          │
│  ├─ DATABASE_ECHO=True                                      │
│  └─ Logging: Pretty console output                          │
│                                                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    PRODUCTION                                │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Kubernetes / Docker Container                              │
│  ├─ PostgreSQL (Managed RDS)                                │
│  ├─ Redis (Managed ElastiCache)                             │
│  └─ FastAPI (No reload, gunicorn/uvicorn)                   │
│                                                               │
│  Environment:                                                │
│  ├─ ENVIRONMENT=production                                  │
│  ├─ DEBUG=False                                             │
│  ├─ LOG_LEVEL=WARNING                                       │
│  ├─ DATABASE_ECHO=False                                     │
│  └─ Logging: JSON for aggregation                           │
│                                                               │
│  Infrastructure:                                             │
│  ├─ Auto-scaling based on load                              │
│  ├─ Load balancer for distribution                          │
│  ├─ Health checks and monitoring                            │
│  ├─ Database backups and replication                        │
│  ├─ Redis replication and failover                          │
│  └─ Certificate management (HTTPS)                          │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Class Diagram (Simplified)

```
┌──────────────────────────────────────┐
│          Order (Domain)              │
├──────────────────────────────────────┤
│ - id: UUID                           │
│ - user_id: UUID                      │
│ - restaurant_id: UUID                │
│ - items: list[dict]                  │
│ - status: OrderStatus                │
│ - total_price: float                 │
│ - delivery_address: str              │
│ - special_instructions: str?         │
│ - created_at: datetime               │
│ - updated_at: datetime               │
├──────────────────────────────────────┤
│ + mark_as_confirmed()                │
│ + mark_as_cancelled()                │
│ + is_completed(): bool               │
└──────────────────────────────────────┘
           △                    △
           │ implements         │ maps to
           │                    │
┌──────────┴─────────────────┐  │
│ IOrderRepository           │  │
├────────────────────────────┤  │
│ + create(Order): Order     │  │
│ + get_by_id(UUID): Order?  │  │
│ + update(Order): Order     │  │
│ + delete(UUID): bool       │  │
│ + list_by_user(...): List  │  │
│ + list_by_restaurant(...)  │  │
└────────────────────────────┘  │
           △                     │
           │ implements          │
           │                     │
┌──────────┴────────────────────────┐
│ SQLAlchemyOrderRepository           │
├─────────────────────────────────────┤
│ - session: AsyncSession             │
├─────────────────────────────────────┤
│ + create(Order): Order              │
│ + get_by_id(UUID): Order?           │
│ + update(Order): Order              │
│ + delete(UUID): bool                │
│ + list_by_user(...): List[Order]    │
│ + list_by_restaurant(...): List     │
└─────────────────────────────────────┘
           │
           │ uses
           ▼
┌──────────────────────────────────────┐
│          OrderORM (SQLAlchemy)       │
├──────────────────────────────────────┤
│ __tablename__ = "orders"             │
│ - id: Column(UUID)                   │
│ - user_id: Column(UUID)              │
│ - restaurant_id: Column(UUID)        │
│ - items: Column(JSON)                │
│ - status: Column(String)             │
│ - total_price: Column(Float)         │
│ - delivery_address: Column(String)   │
│ - special_instructions: Column(...)  │
│ - created_at: Column(DateTime)       │
│ - updated_at: Column(DateTime)       │
├──────────────────────────────────────┤
│ + to_domain(): Order                 │
└──────────────────────────────────────┘
           │
           │ persists to
           ▼
┌──────────────────────────────────────┐
│      PostgreSQL Database             │
│        (orders table)                │
└──────────────────────────────────────┘
```

---

## Service Composition

```
┌─────────────────────────────────────┐
│       OrderService                  │
├─────────────────────────────────────┤
│                                     │
│  __init__(                          │
│    repository: IOrderRepository,    │
│    cache: RedisCache                │
│  )                                  │
│                                     │
├─────────────────────────────────────┤
│                                     │
│  + create_order(...): Order         │
│  + get_order(id): Order             │
│  + update_order(id, ...): Order     │
│  + delete_order(id): bool           │
│  + confirm_order(id): Order         │
│  + cancel_order(id): Order          │
│  + get_user_orders(...): List       │
│  + get_restaurant_orders(...): List │
│                                     │
├─────────────────────────────────────┤
│  Private Methods:                   │
│  - _get_cache_key(id): str          │
│                                     │
└─────────────────────────────────────┘
        │                  │
        │ uses             │ uses
        ▼                  ▼
   ┌──────────────┐  ┌───────────────┐
   │IOrderRepos   │  │ RedisCache    │
   │itory        │  │               │
   │              │  │ + get()       │
   │ + create()   │  │ + set()       │
   │ + get_by_id()│  │ + delete()    │
   │ + update()   │  │ + clear()     │
   │ + delete()   │  │ + get_or_set()│
   │ + list...()  │  │               │
   └──────────────┘  └───────────────┘
```

This completes the architectural documentation! All diagrams show how the components interact and work together.
