from app.repos.menus.menu import Menu
from sqlmodel import select

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
            menus_dict = [menu.to_dict() for menu in menus] 
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
            db_menu = Menu(**menu.dict())
            self.db.add(db_menu)
            self.db.commit()
            self.db.refresh(db_menu)
        except Exception as e:
            raise e
        return db_menu.to_dict()
        
            