"""user pwd length change

Revision ID: 237d460c97ac
Revises: 9788228a591b
Create Date: 2026-08-31 16:11:55.695360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '237d460c97ac'
down_revision: Union[str, Sequence[str], None] = '9788228a591b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("user", "pwd", type_=sa.String(length=255), nullable=False)
    op.alter_column("user", "name", type_=sa.String(length=50), nullable=False)
    op.alter_column("user", "email", type_=sa.String(length=50), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("user", "pwd", type_=sa.String(), nullable=False)
    op.alter_column("user", "name", type_=sa.String(), nullable=False)
    op.alter_column("user", "email", type_=sa.String(), nullable=False)
