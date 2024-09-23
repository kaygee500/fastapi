""" add content to posts table

Revision ID: ed6ef3b2ac52
Revises: 984f68041599
Create Date: 2024-09-21 21:26:25.102374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed6ef3b2ac52'
down_revision: Union[str, None] = '984f68041599'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
