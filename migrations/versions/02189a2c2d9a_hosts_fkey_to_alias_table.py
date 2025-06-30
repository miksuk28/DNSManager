"""hosts fkey to alias_table

Revision ID: 02189a2c2d9a
Revises: 08051b9a9106
Create Date: 2025-06-30 15:23:27.352725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02189a2c2d9a'
down_revision: Union[str, Sequence[str], None] = '08051b9a9106'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.DDL(
        """
        ALTER TABLE hosts ADD COLUMN host_alias_id UUID
        CONSTRAINT fkey_host_alias_id REFERENCES opnsense_aliases (alias_id)
        ON DELETE SET NULL;
        """
    ))
    pass


def downgrade() -> None:
    op.execute(sa.DDL(
        """
        ALTER TABLE hosts DROP CONSTRAINT   fkey_host_alias_id;
        ALTER TABLE hosts DROP COLUMN       host_alias_id;
        """
    ))
