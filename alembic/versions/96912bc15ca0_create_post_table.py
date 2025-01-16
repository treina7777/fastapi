"""create post table

Revision ID: 96912bc15ca0
Revises: 
Create Date: 2025-01-16 11:20:48.874508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96912bc15ca0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True)),
    sa.Column('title', sa.String(),nullable=False)
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table('posts')
    pass
    # ### end Alembic commands ###
