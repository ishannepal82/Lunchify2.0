from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

# Schemas 
from app.schemas.order_schemas import OrderBaseSchema, OrderCreateSchema
from sqlmodel import Session

# Database Dependencies 
from app.db.sessions import get_session

# Services 
from app.services.order_service import OrderService


order_router = APIRouter()
@order_router.get("/orders")
def get_all_orders(db: Session = Depends(get_session)):
    """
    Docstring for get_all_orders
    """
    pass

@order_router.post("/create/order")
def create_order(): 
    """
    Docstring for create_order
    """
    pass