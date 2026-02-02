# Middlewares 
from starlette.middleware.base import BaseHTTPMiddleware

# FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request

# JWT 
from jose import jwt 

# CORE 
from app.core.config import settings

class AuthMiddlware(BaseHTTPMiddleware):
    """
    Docstring for AuthMiddlware

    :param BaseHTTPMiddleware:
    :info: Authentication for users
    """
    def dispatch(self, request, call_next):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing token"})
        
        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            
            # Add actor to request 
            request.state.actor = {
                "id": payload["sub"],
                "role": payload["role"],
            }

        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token expired"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})
        
        return call_next(request)