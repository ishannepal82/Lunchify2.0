from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

# Exceptions 
from app.services.menu_service import MenuNotFoundException
# Services
from app.services.menu_service import MenuService

# Dependencies
from app.db.sessions import get_session

# Helpers
from app.helpers.convert_date_to_str import convert_datetime_to_str
from datetime import datetime 

# Schemas
from app.schemas.menu_schemas import MenuBaseSchema, MenuCreateSchema, MenuResponseSchma, MenuUpdateSchema
from typing import List, Dict
from sqlmodel import Session

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
async def create_menu(req: Request, db = Depends(get_session)):
    try: 
        # Retreive menu data from request body
        menu_data = await req.json()
        menu = MenuCreateSchema(**menu_data)
        service = MenuService(db)
        resp: Dict[MenuResponseSchma] = service.create_menu(menu)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(content={"menu": resp}, status_code=201)

@menu_router.delete("/delete/menu/{menu_id}")
async def delete_menu(menu_id: str, db = Depends(get_session)):
    """
    Info: Delete a Menu by menu_id
    Params: 
        - menu_id: str
    Returns: Success message
    Return Type: dict
    Errors: Raises HTTPException 500 if database operation fails and 404 if menu is not found
    """
    try:
        service = MenuService(db)
        service.delete_menu(menu_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except MenuNotFoundException as mnfe:
        raise HTTPException(status_code=404, detail=str(mnfe))
    
    return JSONResponse(content={"message": "Menu deleted successfully"}, status_code=200)

@menu_router.put("/update/menu/{menu_id}")
async def update_menu(
    req: Request,
    menu_id: str,
    db: Session = Depends(get_session)
):
    """
    Info: Update a Menu by menu_id with provided data.
    Params:
        - menu_id: str
        - menu_update: MenuUpdateSchema (partial update data)
    Returns:
        - Updated menu object
    Errors:
        - 404 if menu not found
        - 500 for DB errors
    """
    try:
        menu_data: MenuUpdateSchema= await req.json()
        
        if menu_data is None:
            raise HTTPException(status_code=400, detail="No update data provided")
        
        updated_menu = MenuUpdateSchema(**menu_data, updated_at=convert_datetime_to_str(datetime.utcnow()))
        
        service = MenuService(db)
        updated_menu = service.update_menu(menu_id, updated_menu.dict())
        return updated_menu

    except MenuNotFoundException as mnfe:
        raise HTTPException(status_code=404, detail=str(mnfe))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))