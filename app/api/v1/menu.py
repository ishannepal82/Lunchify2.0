from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

# Services
from app.services.menu_service import MenuService

# Dependencies
from app.db.sessions import get_session

# Schemas
from app.schemas.menu_schemas import MenuBaseSchema, MenuCreateSchema, MenuResponseSchma
from typing import List 

menu_router = APIRouter()

@menu_router.get("/menus")
async def get_all_menus(db = Depends(get_session)):
    """
    Info: Get all Menus
    Returns: List of Menus 
    Return Type: list of MenuBaseSchema
    Errors: Raises HTTPException 500 if database query fails
    """
    try:
        service = MenuService(db)
        menus: List[MenuBaseSchema] = service.get_all_menus()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(content={"menus": menus}, status_code=200)

@menu_router.post("/create/menu")
async def create_menu(db = Depends(get_session)):
    try: 
        service = MenuService(db)
        resp: MenuResponseSchema = service.create_menu()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(content={"menu": resp}, status_code=201)


