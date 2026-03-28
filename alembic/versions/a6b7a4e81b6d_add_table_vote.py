"""add table vote

Revision ID: a6b7a4e81b6d
Revises: 762b9414b65b
Create Date: 2026-03-28 19:41:16.580142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6b7a4e81b6d'
down_revision: Union[str, Sequence[str], None] = '762b9414b65b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        "created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(table_name='posts', column_name='published')
    op.drop_column(table_name='posts', column_name="created_at")
    pass


