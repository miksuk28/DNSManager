"""hosts to alias table

Revision ID: 08051b9a9106
Revises: b9b7cc809ae8
Create Date: 2025-06-30 14:47:25.777720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08051b9a9106'
down_revision: Union[str, Sequence[str], None] = 'b9b7cc809ae8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.DDL(
        """
        -- function to set pending_delete on delete

        CREATE FUNCTION set_pending_delete_on_host()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE hosts_to_alias
            SET pending_delete = TRUE
            WHERE host_id = OLD.hostId;

            RETURN OLD;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TABLE hosts_to_alias (
            host_id              INTEGER NOT NULL,
            alias_id             UUID    NOT NULL,
            pending_delete       BOOLEAN NOT NULL DEFAULT FALSE,

            FOREIGN KEY (host_id)  REFERENCES hosts (hostId),
            FOREIGN KEY (alias_id) REFERENCES opnsense_aliases (alias_id) ON DELETE CASCADE
        );

        -- trigger to override host delete

        CREATE TRIGGER host_delete_trigger
        BEFORE DELETE ON hosts
        FOR EACH ROW
        EXECUTE FUNCTION set_pending_delete_on_host();
        """
    ))
    pass


def downgrade() -> None:
    op.execute(sa.DDL(
        """
        DROP TRIGGER  host_delete_trigger ON hosts;
        DROP FUNCTION set_pending_delete_on_host();
        DROP TABLE    hosts_to_alias; 
        """
    ))
    pass
