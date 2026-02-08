from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from app.core.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    """
    JWT Authentication Middleware
    """

    async def dispatch(self, request: Request, call_next):
        PUBLIC_PATHS = (
            "/docs",
            "/openapi.json",
            "/health",
            "/api/v1/auth",
        )

        path = request.url.path

        # Skip auth for public routes
        if path.startswith(PUBLIC_PATHS):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid Authorization header"},
            )

        token = auth_header.split(" ", 1)[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            sub = payload.get("sub")
            role = payload.get("role")

            if not sub or not role:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid token payload"},
                )

            # Attach authenticated user to request
            request.state.actor = {
                "id": sub,
                "role": role,
            }

        except ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token expired"},
            )
        except JWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"},
            )

        return await call_next(request)
