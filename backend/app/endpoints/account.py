from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas import Account
from app.db.connection import get_session
from app.services.mock_data import mock_accounts

api_router = APIRouter(
    prefix="",
    tags=["Accounts"],
)


@api_router.get(
    "/accounts",
    response_model=list[Account],
    status_code=status.HTTP_200_OK,
)
async def accounts(
        session: AsyncSession = Depends(get_session)):
    # По хорошему надо передать user_id или organization_id и брать только их счета

    return mock_accounts


@api_router.post(
    "/accounts",
    status_code=status.HTTP_200_OK,
)
async def accounts(
        account: Account = Body(...),
        session: AsyncSession = Depends(get_session)):
    # По хорошему надо передать user_id или organization_id и брать только их счета
    print(account)
    return mock_accounts


@api_router.get(
    "/accounts/{account_id}",
    response_model=Account,
    status_code=status.HTTP_200_OK,
)
async def accounts(
        account_id: int,
        session: AsyncSession = Depends(get_session)):
    print(account_id)
    return mock_accounts[0]
