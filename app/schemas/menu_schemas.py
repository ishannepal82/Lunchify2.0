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
     
    pass

class MenuResponseSchma(MenuBaseSchema):
    pass
    


