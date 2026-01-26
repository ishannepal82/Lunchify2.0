from sqlmodel import SQLModel, Field
from sqlalchemy import JSON
from datetime import datetime
from typing import List, Optional

# Helpers
from app.helpers.convert_date_to_str import convert_datetime_to_str

class DishBaseSchema(SQLModel):
    dish_name: str
    dish_description: str
    dish_price: float 
    dish_discount: Optional[float]= 0.0
    dish_category: List[str] = []

class Menu(SQLModel, table=True):
    """
    Schema for Menu: 

    menu_id: str
    menu_title: str
    restaurant_id: str
    menu_description: Optional[str] = Field(default="", max_length=500)
    created_at: str = convert_datetime_to_str(datetime.utcnow())
    dishes: List[DishBaseSchema] 

    """
    menu_id: str = Field(primary_key=True, index=True)
    menu_title: str
    menu_description: str = Field(min_length=0, max_length=500)
    restaurant_id: str 
    created_at: str = Field(default=convert_datetime_to_str(datetime.utcnow()), index=True)
    updated_at: Optional[str] = Field(default=None, index=True)
    dishes: List[DishBaseSchema] = Field(default_factory=list, sa_type=JSON)
    created_at: str = Field(default=convert_datetime_to_str(datetime.utcnow()), index=True)



