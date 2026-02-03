from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

# Services 
from app.services.auth.users.login_service import LoginService
from app.services.auth.users.registration_service import RegistrationService

from app.services.auth.restaurants.login_service import LoginService as LoginRestaurantService
from app.services.auth.restaurants.register_service import RegistrationService as RegistrationRestaurantService

# User Schemas 
from app.schemas.user_schemas import UserCreateSchema, UserResponseSchema, UserLoginRequestSchema

# Restaurant Schemas 
from app.schemas.restaurants_schemas import RestraurantCreateSchema, RestaurantLoginRequestSchema

# Sessions
from app.db.sessions import get_session

auth_router = APIRouter()

@auth_router.post('/login')
def login(data: UserLoginRequestSchema, db = Depends(get_session)):
    try: 
        service = LoginService(db)
        resp = service.login_user(data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    
    return JSONResponse(content={"token": resp}, status_code=201)

@auth_router.post('/logout')
def logout():
    pass

@auth_router.post('/register')
def register(user: UserCreateSchema, db = Depends(get_session)):
    try:
        service = RegistrationService(db)
        resp = service.create_user(user)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    
    return JSONResponse(content={"user": resp.model_dump()}, status_code=201)

@auth_router.post('/restaurants/register')
def register_restaurant(restaurant: RestraurantCreateSchema, db = Depends(get_session)):
    try:
        service = RegistrationRestaurantService(db)
        resp = service.create_user(restaurant)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    
    return JSONResponse(content={"restaurant": resp.model_dump()}, status_code=201)

@auth_router.post('/restaurants/login')
def login_restaurant(restaurant: RestaurantLoginRequestSchema, db = Depends(get_session)):
    try:
        service = LoginRestaurantService(db)
        resp = service.create_user(restaurant)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    
    return JSONResponse(content={"restaurant": resp.model_dump()}, status_code=201)
    

@auth_router.post('/restaurants/logout')
def logout_restaurant():
    pass