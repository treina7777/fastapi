"""add content column to posts table

Revision ID: 6a5252bd12a6
Revises: 96912bc15ca0
Create Date: 2025-01-16 11:37:04.877020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a5252bd12a6'
down_revision: Union[str, None] = '96912bc15ca0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
