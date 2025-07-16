"""dhcpscopes to aliases

Revision ID: b4b4712c96b8
Revises: 02189a2c2d9a
Create Date: 2025-07-07 15:22:15.411168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4b4712c96b8'
down_revision: Union[str, Sequence[str], None] = '02189a2c2d9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.DDL(
        """
        ALTER TABLE opnsense_aliases
        ADD COLUMN  allowed_for_all_scopes BOOLEAN NOT NULL DEFAULT TRUE;

        CREATE TABLE scopes_to_aliases (
            dhcpscope_id    INTEGER     NOT NULL,
            alias_id        UUID        NOT NULL,
            UNIQUE(dhcpscope_id, alias_id),

            CONSTRAINT fkey_scopes_to_aliases_dhcpscope_id
                FOREIGN KEY (dhcpscope_id) REFERENCES dhcpscopes (dhcpscopeid),

            CONSTRAINT fkey_scopes_to_aliases_alias_id
                FOREIGN KEY (alias_id)     REFERENCES opnsense_aliases (alias_id)
        );
        """
    ))


def downgrade() -> None:
    op.execute(sa.DDL(
        """
        ALTER TABLE opnsense_aliases    DROP COLUMN allowed_for_all_scopes;
        ALTER TABLE scopes_to_aliases   DROP CONSTRAINT fkey_scopes_to_aliases_dhcpscope_id;
        ALTER TABLE scopes_to_aliases   DROP CONSTRAINT fkey_scopes_to_aliases_alias_id;
        DROP TABLE scopes_to_aliases;
        """
    ))