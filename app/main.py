"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.orders.router import router as orders_router
from app.cache.redis_cache import cache
from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.db.session import close_db, init_db

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Manage application lifecycle events.
    
    Handles startup and shutdown of application resources.
    """
    # Startup
    logger.info("Starting application", environment=settings.environment)
    await init_db()
    await cache.connect()

    yield

    # Shutdown
    logger.info("Shutting down application")
    await cache.disconnect()
    await close_db()


def create_app() -> FastAPI:
    """Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured application instance.
    """
    configure_logging()

    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description="Production-ready order service API",
        lifespan=lifespan,
    )

    # Exception handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):  # noqa: ARG001
        """Handle validation errors."""
        return JSONResponse(
            status_code=422,
            content={
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "errors": exc.errors(),
            },
        )

    # Include routers
    app.include_router(orders_router, prefix="/api/v1")

    # Health check endpoint
    @app.get("/health")
    async def health_check() -> dict:
        """Health check endpoint.
        
        Returns:
            dict: Health status.
        """
        return {"status": "healthy"}

    logger.info("Application created successfully")
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
