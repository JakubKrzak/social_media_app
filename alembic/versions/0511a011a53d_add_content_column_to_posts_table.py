"""add content column to posts table

Revision ID: 0511a011a53d
Revises: 5a4bb140e54b
Create Date: 2026-03-28 18:53:05.467745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0511a011a53d'
down_revision: Union[str, Sequence[str], None] = '5a4bb140e54b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
