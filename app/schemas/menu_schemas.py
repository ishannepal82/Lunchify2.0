from pydantic import BaseModel
from typing import List, Optional

class DishesBaseSchema(BaseModel):
    dish_name: str
    dish_description: str
    dish_price: float
    dish_discount: Optional[float] = 0.0
    dish_category: List[str] = []
    dish_image_url: Optional[str] = None

class MenuBaseSchema(BaseModel):
    menu_id: str
    menu_title: str
    menu_description: str 
    dishes: List[DishesBaseSchema] = []
    restaurant_id: str # TODO: Change to UUID in future
    created_at:str

class MenuCreateSchema(BaseModel):
    menu_title: str
    menu_description: str
    dishes: List[DishesBaseSchema] = []
    restaurant_id: str # TODO: Change to UUID in future

class MenuResponseSchma(MenuBaseSchema):
    pass

class DishUpdateSchema(BaseModel):
    dish_name: Optional[str] = None
    dish_description: Optional[str] = None
    dish_price: Optional[float] = None
    dish_discount: Optional[float] = None
    dish_category: Optional[List[str]] = None
    dish_image_url: Optional[str] = None

class MenuUpdateSchema(BaseModel):
    menu_title: Optional[str] = None
    menu_description: Optional[str] = None
    dishes: Optional[list[DishUpdateSchema]] = None
    updated_at: Optional[str] = None
    


