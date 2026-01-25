from datetime import datetime
from uuid import uuid4
from app.repos.menus import menu
from app.repos.menus.menu import Menu
from sqlmodel import select

# Exceptions 
class MenuNotFoundException(Exception):
    def __init__(self, menu_id: str):
        self.menu_id = menu_id
        super().__init__(f"Menu with ID '{menu_id}' not found.")

# Schemas 
from app.schemas.menu_schemas import MenuBaseSchema
from typing import List

class MenuService(): 
    def __init__(self, db):
        self.db = db
    
    def get_all_menus(self):
        """
        Docstring for get_all_menus
        
        :Returns: List of MenuBaseSchema
        :rtype: list of MenuBaseSchema
        :errors: Raises Exception of datbase query fails
        """
        try:
            menus = self.db.exec(select(Menu)).all()
            menus_dict = [menu.model_dump() for menu in menus] 
        except Exception as e:
            raise e
        return menus_dict
    
    def create_menu(self, menu):
        """
        Docstring for create_menu

        :param menu: MenuBaseSchema
        :returns: Created Menu as dict 
        :rtype: dict 
        :errors: Raises Exception if database operation fails
        """
        try:
            db_menu = Menu(
                menu_id=str(uuid4()),
                created_at=datetime.utcnow(),
                **menu.dict())
            self.db.add(db_menu)
            self.db.commit()
            self.db.refresh(db_menu)
        except Exception as e:
            raise e
        return db_menu.model_dump()
    
    def delete_menu(self, menu_id: str):
        """
        Docstring for delete_menu

        :param menu_id: str
        :returns: None
        :rtype: None
        :errors: Raises Exception if database operation fails
        """
        try:
            menu = self.db.get(Menu, menu_id)
            if not menu:
                raise MenuNotFoundException(menu_id=menu_id)
            self.db.delete(menu)
            self.db.commit()
        except Exception as e:
            raise e
        
    def update_menu(self, menu_id, update_data):
        """
        Update a menu by menu_id with new data.

        :param menu_id: str - ID of the menu to update
        :param update_data: dict - fields to update with new values
        :returns: Updated Menu object
        :raises MenuNotFoundException: if menu not found
        :raises Exception: for other DB errors
        """
        try:
            menu = self.db.get(Menu, menu_id)
            
            if not menu:
                raise MenuNotFoundException(menu_id=menu_id)

            for key, value in update_data.items():
                setattr(menu, key, value)

            self.db.add(menu)
            self.db.commit()
            self.db.refresh(menu)

        except Exception as e:
            raise e
    
        return menu.model_dump()
            