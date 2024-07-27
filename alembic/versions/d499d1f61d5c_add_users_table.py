"""add users table

Revision ID: d499d1f61d5c
Revises: 4f4af0870b7c
Create Date: 2024-07-27 19:24:59.502633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd499d1f61d5c'
down_revision: Union[str, None] = '4f4af0870b7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', 
                  sa.Column('id', sa.Integer(), nullable=False),
                  sa.Column('email', sa.String(), nullable=False),
                  sa.Column('password', sa.String(), nullable=False),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),
                  sa.PrimaryKeyConstraint('id'),
                  sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')
