from logging import getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from uvicorn import run

from app.settings import get_settings
from app.endpoints import list_of_routes
from app.db.connection import SessionManager
# logger = getLogger(__name__)
from app.db import Base

settings = get_settings()


def bind_routes(application: FastAPI) -> None:
    """
    Bind all routes to application.
    """

    for route in list_of_routes:
        application.include_router(route, prefix=settings.PATH_PREFIX)

    for route in application.routes:
        print(f"Path: {route.path}, Method: {route.methods}")


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    application = FastAPI(
        title="Very top cool best api",
        description="...",
        version="1.0.0",
    )
    bind_routes(application)
    origins = [
        "http://localhost:5173",
        "http://localhost:8000",
        "http://localhost:4173",
        "http://localhost",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # engine = create_engine(get_settings().database_uri_sync, echo=True, future=True)
    # Base.metadata.create_all(engine)

    return application


app = get_app()

if __name__ == "__main__":  # pragma: no cover
    run(
        "app.__main__:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        reload_dirs=["."],
        log_level="debug",
        proxy_headers=True,
    )
