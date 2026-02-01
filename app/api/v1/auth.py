from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

# Services 
from app.services.auth.login_service import LoginService
from app.services.auth.registration_service import RegistrationService

# Schemas
from app.schemas.user_schemas import UserCreateSchema, UserResponseSchema

# Sessions
from app.db.sessions import get_session

auth_router = APIRouter()

@auth_router.post('/login')
def login(db = Depends(get_session)):
    pass

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