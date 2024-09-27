"""add phone number

Revision ID: 61c6b0a6e839
Revises: f82c02b13a64
Create Date: 2024-09-24 01:57:19.271399

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61c6b0a6e839'
down_revision: Union[str, None] = 'f82c02b13a64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
