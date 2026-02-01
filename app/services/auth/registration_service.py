
# Helpers
from app.helpers.internal.hash_password import hash_password
from app.helpers.convert_date_to_str import convert_datetime_to_str

# Repos
from app.repos.users.users import User
from sqlmodel import select 
from datetime import datetime
from uuid import uuid4


class RegistrationService():
    def __init__(self, db):
        self.db = db

    def create_user(self, user):
        try:
            existing_user = self.db.exec(
            select(User).where(
                User.contact["email"].as_string() == user.contacts.email
            )
        ).first()

            if existing_user:
                raise ValueError("User with this email already exists.")
            
            user_db = User(
                name=user.name,
                contact=user.contacts.model_dump(),
                address=user.address.model_dump(),
                hashed_password=hash_password(user.password)
            )

            self.db.add(user_db)
            self.db.commit()
            self.db.refresh(user_db)

        except Exception as e:
            raise e
        
        return user