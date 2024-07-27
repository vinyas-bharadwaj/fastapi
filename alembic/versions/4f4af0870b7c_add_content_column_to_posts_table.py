"""add content column to posts table

Revision ID: 4f4af0870b7c
Revises: 62884ea3c788
Create Date: 2024-07-27 19:20:03.076853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f4af0870b7c'
down_revision: Union[str, None] = '62884ea3c788'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
