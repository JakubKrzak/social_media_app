"""add user table with all columns

Revision ID: 28ca35d64d80
Revises: c5451b693819
Create Date: 2026-03-28 19:09:43.520681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28ca35d64d80'
down_revision: Union[str, Sequence[str], None] = 'c5451b693819'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
