
# Helpers
from app.helpers.hash_password import hash_password
from app.helpers.convert_date_to_str import convert_datetime_to_str

# Repos
from app.repos.restaurants.restaurants import Restaurant
from sqlmodel import select 
from datetime import datetime
from uuid import uuid4


class RegistrationService():
    def __init__(self, db):
        self.db = db

    def create_restaurant(self, restaurant):
        try:
            existing_restaurant = self.db.exec(
            select(Restaurant).where(
                Restaurant.contact["email"].as_string() == restaurant.contacts.email
            )
        ).first()

            if existing_restaurant:
                raise ValueError("Restaurant with this email already exists.")
            
            restaurant_db = Restaurant(
                name=restaurant.name,
                contact=restaurant.contacts.model_dump(),
                address=restaurant.address.model_dump(),
                hashed_password=hash_password(restaurant.password)
            )

            self.db.add(restaurant_db)
            self.db.commit()
            self.db.refresh(restaurant_db)

        except Exception as e:
            raise e
        
        return restaurant