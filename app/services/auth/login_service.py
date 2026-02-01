from uuid import uuid4
from datetime import datetime
from sqlmodel import select

# Repos: 
from app.repos.users.users import User

# Helpers 
from app.helpers.hash_password import check_password
from app.helpers.access_token_creator import create_access_token

class LoginService():
    def __init__(self, db):
        self.db = db

    def login_user(self, data):
        try: 
            user = self.db.exec(
            select(User).where(User.contact['email'].as_string()  == data.contact.email)
            ).first()
            print(user)
            """
            Check wether the password that user has entred is correct or not 
            and also check if the user exists or not 
            """
            if not user or not check_password(data.password, user.hashed_password):
                raise ValueError("Invalid email or password.")
            
            access_token = create_access_token(
                data={"sub": str(user.user_id)}
            )
            
        except Exception as e:
            raise e
        
        return access_token
        

    def logout_user(self, user):
        pass