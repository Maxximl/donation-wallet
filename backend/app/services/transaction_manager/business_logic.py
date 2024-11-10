from sqlalchemy.ext.asyncio import AsyncSession

from app.services.mock_api_schemas import mock_transactions
from app.schemas import Transaction, Account
# from app.db.models import Transaction


async def create(session: AsyncSession, transaction: Transaction) -> Transaction | None:
    # idx = len(mock_accounts)
    mock_transactions.append(transaction)
    return transaction


async def get_all(session: AsyncSession, account_id: int) -> list[Transaction]:
    def all_user_transactions(transaction: Transaction) -> bool:
        if account_id in [transaction.receiver_account_id, transaction.sender_account_id]:
            return True
        return False

    return list(filter(all_user_transactions, mock_transactions))


async def get_by_id(session: AsyncSession, id: int) -> Transaction | None:
    if id >= len(mock_transactions):
        return None
    return mock_transactions[id]
