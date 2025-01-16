"""add user table

Revision ID: b0bb983df936
Revises: 6a5252bd12a6
Create Date: 2025-01-16 11:47:16.583836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0bb983df936'
down_revision: Union[str, None] = '6a5252bd12a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
