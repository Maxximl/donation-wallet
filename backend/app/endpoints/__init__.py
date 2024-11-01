from app.endpoints.auth import api_router as auth_router
from app.endpoints.health_check import api_router as application_health_router
from app.endpoints.account import api_router as account_router
from app.endpoints.charity_organization import api_router as charity_organization_router
from app.endpoints.transaction import api_router as transaction_organization_router

list_of_routes = [
    application_health_router,
    auth_router,
    account_router,
    charity_organization_router,
    transaction_organization_router,
]

__all__ = [
    "list_of_routes",
]
