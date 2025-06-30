"""Alias table

Revision ID: b9b7cc809ae8
Revises: 31e69414c410
Create Date: 2025-06-29 17:28:18.929218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9b7cc809ae8'
down_revision: Union[str, Sequence[str], None] = '31e69414c410'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.DDL(
        """
        CREATE TABLE opnsense_aliases (
            alias_id            UUID    NOT NULL UNIQUE,
            is_host_alias       BOOLEAN NOT NULL,
            alias_name          TEXT    NOT NULL UNIQUE,
            category_id         TEXT,
            alias_description   TEXT,
            alias_display_name  TEXT
        );
        """
    ))


def downgrade() -> None:
    op.execute(sa.DDL(
        '''
        DROP TABLE opnsense_aliases;
        '''
    ))
    pass
