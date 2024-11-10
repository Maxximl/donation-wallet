from sqlalchemy.ext.asyncio import AsyncSession

from app.services.mock_api_schemas import mock_transactions
from app.services.mock_api_schemas import mock_accounts
from app.schemas import Account
from app.db.models import User


# async def create(session: AsyncSession, transaction: Transaction) -> Transaction | None:
#     # idx = len(mock_accounts)
#     # if t.id in mock_accounts:
#     #     return None
#     mock_transactions[transaction.id] = transaction
#     return transaction


async def get_all(session: AsyncSession, user: User) -> list[Account]:
    return list(filter(lambda x: x.owner_id == user.id, mock_accounts.values()))


async def get_by_id(session: AsyncSession, id: int) -> Account | None:
    if id not in mock_accounts:
        return None
    return mock_accounts[id]
