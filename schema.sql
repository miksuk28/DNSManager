CREATE TABLE hosts (
    hostId              INTEGER     PRIMARY KEY AUTOINCREMENT,
    hostname            TEXT        NOT NULL UNIQUE,
    domainId            INTEGER     NOT NULL,
    ipAddress           TEXT(15)    NOT NULL UNIQUE,
    managedDhcp         BOOLEAN     NOT NULL,
    dhcpScopeId         INTEGER,
    macAddress          TEXT(17)    UNIQUE,

    FOREIGN KEY (domainId) REFERENCES domains (domainId),
    FOREIGN KEY (dhcpScopeId) REFERENCES dhcpScopes (dhcpScopeId)
);


CREATE TABLE domains (
    domainId            INTEGER PRIMARY KEY AUTOINCREMENT,
    domainName          TEXT NOT NULL UNIQUE
);


CREATE TABLE dhcpScopes (
    dhcpScopeId         INTEGER     PRIMARY KEY AUTOINCREMENT,
    dhcpScopeName       TEXT        NOT NULL UNIQUE,
    dhcpStartAddress    TEXT(15)    NOT NULL UNIQUE,
    dhcpEndAddress      TEXT(15)    NOT NULL UNIQUE,
    dhcpNetmask         INTEGER     NOT NULL
);


CREATE TABLE services (
    serviceId           INTEGER     PRIMARY KEY AUTOINCREMENT,
    targetHostId        INTEGER     NOT NULL,
    serviceName         TEXT        NOT NULL,
    domainId            INTEGER     NOT NULL,

    UNIQUE(serviceName, domainId),
    FOREIGN KEY (targetHostId) REFERENCES hosts (hostId)
);


CREATE TABLE technitiumServers (
    serverId            INTEGER     PRIMARY KEY AUTOINCREMENT,
    serverHostname      TEXT        NOT NULL UNIQUE,
    serverPort          INTEGER,
    useHttps            BOOLEAN     NOT NULL,
    serverToken         TEXT        NOT NULL
);