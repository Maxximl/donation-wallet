from fastapi import APIRouter, Depends, HTTPException, Request, Body, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas import Account
from app.db.connection import get_session
# from app.services.mock_api_schemas import mock_accounts
import app.services.account_manager.business_logic as account_manager
from app.schemas import User
from app.services.user_manager import get_current_user

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
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user),
):
    accounts = await account_manager.get_all(session, current_user)
    return accounts


# @api_router.post(
#     "/accounts",
#     status_code=status.HTTP_200_OK,
# )
# async def create(
#         account: Account = Body(...),
#         session: AsyncSession = Depends(get_session),
#         current_user: User = Depends(get_current_user),
# ):
#     # По хорошему надо передать user_id или organization_id и брать только их счета
#     account.owner_id = current_user.id
#     resp = await account_manager.create(session, account)
#     if resp is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="account with id already exist")
#     return account


@api_router.get(
    "/accounts/{account_id}",
    response_model=Account,
    status_code=status.HTTP_200_OK,

)
async def get_by_id(
        account_id: int = Path(...),
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user),
):
    account = await account_manager.get_by_id(session, account_id)

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found")

    if account.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="not owner")
    return account
