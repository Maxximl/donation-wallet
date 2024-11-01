from app.endpoints.auth import api_router as auth_router
from app.endpoints.health_check import api_router as application_health_router


list_of_routes = [
    application_health_router,
    auth_router,
]

__all__ = [
    "list_of_routes",
]