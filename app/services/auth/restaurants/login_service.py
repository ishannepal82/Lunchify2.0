from uuid import uuid4
from datetime import datetime
from sqlmodel import select

# Repos: 
from app.repos.restaurants.restaurants import Restaurant

# Helpers 
from app.helpers.hash_password import check_password
from app.helpers.access_token_creator import create_access_token

class LoginService():
    def __init__(self, db):
        self.db = db

    def login_restaurant(self, data):
        try: 
            restaurant = self.db.exec(
            select(Restaurant).where(Restaurant.contact['email'].as_string()  == data.contact.email)
            ).first()
            """
            Check wether the password that restaurant has entred is correct or not 
            and also check if the restaurant exists or not 
            """
            if not restaurant or not check_password(data.password, restaurant.hashed_password):
                raise ValueError("Invalid email or password.")
            
            access_token = create_access_token( data={"sub": str(restaurant.restaurant_id), 
                      "role": "restaurant"
                      })
          
        except Exception as e:
            raise e
        
        return access_token
        

    def logout_user(self, user):
        pass