"""mock

Revision ID: 96002d01913b
Revises: e56380c002c9
Create Date: 2024-11-26 14:42:40.539387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96002d01913b'
down_revision: Union[str, None] = 'd8d68afa78ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
