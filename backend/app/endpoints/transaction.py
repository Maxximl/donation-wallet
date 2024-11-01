from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas import Transaction
from app.db.connection import get_session
from app.services.mock_data import mock_transactions

api_router = APIRouter(
    prefix="",
    tags=["Transactions"],
)


@api_router.get(
    "/transactions",
    response_model=list[Transaction],
    status_code=status.HTTP_200_OK,
)
async def get_all(
        session: AsyncSession = Depends(get_session)):
    return mock_transactions


@api_router.post(
    "/transactions",
    status_code=status.HTTP_200_OK,
)
async def create(
        transaction: Transaction = Body(...),
        session: AsyncSession = Depends(get_session)):
    # По хорошему надо передать user_id или organization_id и брать только их счета
    print(transaction)
    return {"msg": "OK"}


@api_router.get(
    "/charity_organizations/{id}",
    response_model=Transaction,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "not found",
        },
    },
)
async def get(
        id: int,
        session: AsyncSession = Depends(get_session)):
    if id >= len(mock_transactions):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found")
    return mock_transactions[id - 1]
