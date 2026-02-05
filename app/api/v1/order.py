from fastapi import APIRouter, Depends, HTTPException, Request, Query
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
def create_order(
    order: OrderCreateSchema,
    db: Session = Depends(get_session))-> JSONResponse: 
    """
    Docstring for create_order
    """
    try: 
        service = OrderService(db)
        resp: OrderBaseSchema = service.create_order(order)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content={"order": resp}, status_code=201)

@order_router.put("/approve/order")
def approve_order(
    order_id = Query(None, alias="order_id"),
    db: Session = Depends(get_session))-> JSONResponse: 
    """
    Docstring for approve_order
    - user sends a query parameter 
    - the query parameter is sent to the service (approve_order) method 
    - the order is searched through the DB 
    - if the order exsists then the bool is set true and if not then it returns the 400 bad request 
    """
    try: 
        service = OrderService(db)
        resp: OrderBaseSchema = service.approve_order(order_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content={"order": resp}, status_code=201)