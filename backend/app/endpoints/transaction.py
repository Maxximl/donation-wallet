from fastapi import APIRouter, Depends, HTTPException, Request, Body, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas import Transaction
from app.db.connection import get_session
import app.services.transaction_manager.business_logic as transaction_manager

# from app.services.mock_api_schemas import mock_transactions

api_router = APIRouter(
    prefix="/accounts",
    tags=["Transactions"],
)


@api_router.get(
    "/{account_id}/transactions",
    response_model=list[Transaction],
    status_code=status.HTTP_200_OK,
)
async def get_all(
        account_id: int = Path(...),
        session: AsyncSession = Depends(get_session)):
    transactions = await transaction_manager.get_all(session, account_id)
    return transactions


@api_router.post(
    "/{account_id}/transactions",
    status_code=status.HTTP_200_OK,
)
async def create(
        transaction: Transaction = Body(...),
        session: AsyncSession = Depends(get_session)):
    # По хорошему надо передать user_id или organization_id и брать только их счета
    print(transaction)
    res = await transaction_manager.create(session, transaction)
    if res:
        return {"msg": "OK"}
    return {"msg": "BAD"}


@api_router.get(
    "/{account_id}/transactions/{transaction_id}",
    response_model=Transaction,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "not found",
        },
    },
)
async def get(
        account_id: int = Path(...),
        transaction_id: int = Path(...),
        session: AsyncSession = Depends(get_session)):

    transaction = await transaction_manager.get_by_id(session, transaction_id)
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found")
    return transaction
