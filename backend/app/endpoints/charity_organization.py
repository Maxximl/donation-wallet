from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas import CharityOrganization
from app.db.connection import get_session
from app.services.mock_data import mock_charity_organizations

api_router = APIRouter(
    prefix="",
    tags=["Charity Organizations"],
)


@api_router.get(
    "/charity_organizations",
    response_model=list[CharityOrganization],
    status_code=status.HTTP_200_OK,
)
async def get_all(
        session: AsyncSession = Depends(get_session)):
    return mock_charity_organizations


@api_router.post(
    "/charity_organizations",
    status_code=status.HTTP_200_OK,
)
async def create(
        charity_organization: CharityOrganization = Body(...),
        session: AsyncSession = Depends(get_session)):
    # По хорошему надо передать user_id или organization_id и брать только их счета
    print(charity_organization)
    return {"msg": "OK"}


@api_router.get(
    "/charity_organizations/{charity_organization_id}",
    response_model=CharityOrganization,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "charity_organizations with this id and this owner not found",
        },
    },
)
async def get(
        charity_organization_id: int,
        session: AsyncSession = Depends(get_session)):
    if charity_organization_id >= len(mock_charity_organizations):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="charity_organizations with this id and this owner not found")
    return mock_charity_organizations[charity_organization_id - 1]
