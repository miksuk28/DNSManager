"""Initial schema

Revision ID: 31e69414c410
Revises: 
Create Date: 2025-06-27 17:58:29.905671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31e69414c410'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.DDL(
        """
        CREATE TABLE domains (
            domainId            SERIAL      PRIMARY KEY,
            domainName          TEXT        NOT NULL UNIQUE
        );

        CREATE TABLE dhcpScopes (
            dhcpScopeId         SERIAL      PRIMARY KEY,
            dhcpScopeName       TEXT        NOT NULL UNIQUE,
            dhcpStartAddress    INET        NOT NULL UNIQUE,
            dhcpEndAddress      INET        NOT NULL UNIQUE,
            dhcpNetmask         INTEGER     NOT NULL
        );

        CREATE TABLE hosts (
            hostId              SERIAL      PRIMARY KEY,
            hostname            TEXT        NOT NULL,
            domainId            INTEGER     NOT NULL,
            ipAddress           INET        NOT NULL UNIQUE,
            ipAddressInt        INTEGER,
            managedDhcp         BOOLEAN     NOT NULL,
            dhcpScopeId         INTEGER,
            macAddress          MACADDR     UNIQUE,

            UNIQUE(hostname, domainId),
            FOREIGN KEY (domainId) REFERENCES domains (domainId) ON DELETE RESTRICT,
            FOREIGN KEY (dhcpScopeId) REFERENCES dhcpScopes (dhcpScopeId) ON DELETE RESTRICT
        );

        CREATE TABLE services (
            serviceId           SERIAL      PRIMARY KEY,
            targetHostId        INTEGER     NOT NULL,
            serviceName         TEXT        NOT NULL,
            domainId            INTEGER     NOT NULL,
            description         TEXT,

            UNIQUE(serviceName, domainId),
            FOREIGN KEY (domainId)     REFERENCES domains (domainId) ON DELETE RESTRICT,
            FOREIGN KEY (targetHostId) REFERENCES hosts (hostId) ON DELETE RESTRICT
        );


        CREATE TABLE technitiumServers (
            serverId            SERIAL      PRIMARY KEY,
            serverHostname      TEXT        NOT NULL UNIQUE,
            serverPort          INTEGER,
            useHttps            BOOLEAN     NOT NULL,
            serverToken         TEXT        NOT NULL
        );
        """
    ))


def downgrade() -> None:
    """Downgrade schema."""
    pass
