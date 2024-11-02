from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas import Account
from app.db.connection import get_session
from app.services.mock_api_schemas import mock_accounts

api_router = APIRouter(
    prefix="",
    tags=["Accounts"],
)


@api_router.get(
    "/accounts",
    response_model=list[Account],
    status_code=status.HTTP_200_OK,
)
async def get_all(
        session: AsyncSession = Depends(get_session)):
    # По хорошему надо передать user_id или organization_id и брать только их счета

    return mock_accounts.values()


@api_router.post(
    "/accounts",
    status_code=status.HTTP_200_OK,
)
async def create(
        account: Account = Body(...),
        session: AsyncSession = Depends(get_session)):
    # По хорошему надо передать user_id или organization_id и брать только их счета
    print(account)
    return {"msg": "OK"}


@api_router.get(
    "/accounts/{id}",
    response_model=Account,
    status_code=status.HTTP_200_OK,
)
async def get(
        id: int,
        session: AsyncSession = Depends(get_session)):
    if id not in mock_accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found")
    return mock_accounts[id]
