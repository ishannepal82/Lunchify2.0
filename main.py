import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import create_all_db_tables
from app.api.v1.menu import menu_router
from app.api.v1.order import order_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_all_db_tables()
    print("✓ Database tables created successfully")
    yield
    # Shutdown
    print("✓ App shutting down")


app = FastAPI(
    title="Lunchify_2.0",
    summary="A Food Delivery app, Mainly a practice app",
    version="v1",
    lifespan=lifespan
)

app.include_router(
    prefix="/api/v1/menus", 
    router=menu_router
)

app.include_router(
    prefix="/api/v1/orders",
    router=order_router
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    ) 


