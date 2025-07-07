GET_DOMAIN_BY_ID="SELECT domainName FROM domains WHERE domainId=%s"
GET_DOMAIN_ID="SELECT domainId FROM domains WHERE domainName=%s"
ADD_DOMAIN="INSERT INTO domains (domainName) VALUES (%s)"
GET_DOMAINS='SELECT domainId AS "domainId", domainName AS "domainName" FROM domains'
DELETE_DOMAIN="DELETE FROM domains WHERE domainId=%s"
ADD_HOST='''
INSERT INTO hosts (hostname, domainId, ipAddress, ipAddressInt, managedDhcp, dhcpScopeId, macAddress)
VALUES (%(hostname)s, %(domainId)s, %(ipAddress)s, %(ipAddressInt)s, %(managedDhcp)s, %(dhcpScopeId)s, %(macAddress)s)
RETURNING hostId
'''
GET_DHCP_SCOPE_ID="SELECT dhcpScopeId FROM dhcpScopes WHERE dhcpScopeName=%s"
GET_DHCP_SCOPE='''
SELECT
    dhcpScopeId,
    dhcpScopeName,
    dhcpStartAddress,
    dhcpStartAddress,
    dhcpEndAddress,
    dhcpNetmask
FROM dhcpScopes
WHERE dhcpScopeId=%s
'''
GET_DHCP_SCOPE_BY_NAME='''
SELECT *
FROM dhcpScopes
WHERE dhcpScopeName=%s
'''
ADD_DHCP_SCOPE='''
INSERT INTO dhcpScopes (dhcpScopeName, dhcpStartAddress, dhcpEndAddress, dhcpNetmask)
VALUES (%(dhcpScopeName)s, %(dhcpStartAddress)s, %(dhcpEndAddress)s, %(dhcpNetmask)s)
'''
ADD_SERVICE='''INSERT INTO services (targetHostId, serviceName, domainId, description)
               VALUES (%(targetHostId)s, %(serviceName)s, %(domainId)s, %(description)s)'''
GET_HOST_DOMAIN='''SELECT hostname || '.' || domainName
                   FROM hosts h LEFT JOIN domains d ON h.domainId=d.domainId
                   WHERE h.hostId=%s'''
GET_SERVICE_DOMAIN='''SELECT serviceName || '.' || domainName
                      FROM services s LEFT JOIN domains d ON s.domainId=d.domainId
                      WHERE s.serviceId=%s'''
REMOVE_SERVICE="DELETE FROM services WHERE serviceId=%s"
REMOVE_HOST="DELETE FROM hosts WHERE hostId=%s"
GET_HOST='''SELECT h.hostId, hostname, d.domainName, d.domainId, ipAddress, macAddress, managedDhcp, h.dhcpScopeId, s.dhcpScopeName FROM hosts h
            LEFT JOIN domains d ON h.domainId=d.domainId
            LEFT JOIN dhcpScopes s ON h.dhcpScopeId=s.dhcpScopeId
            WHERE h.hostId=%s'''
GET_HOSTS='''
SELECT
    h.hostname || '.' || d.domainName AS hostname,
    h.hostId AS "hostId",
    d.domainName AS "domainName",
    d.domainId AS "domainId",
    ipAddress AS "ipAddress",
    macAddress AS "macAddress",
    managedDhcp AS "managedDhcp",
    h.dhcpScopeId AS "dhcpScopeId",
    s.dhcpScopeName AS "dhcpScopeName"
FROM hosts h
LEFT JOIN domains d ON h.domainId=d.domainId
LEFT JOIN dhcpScopes s ON h.dhcpScopeId=s.dhcpScopeId
ORDER BY h.hostname ASC
'''
GET_HOST_INFO='''
SELECT
    h.hostId AS "hostId",
    h.hostname || '.' || d.domainName AS hostname,
    d.domainName AS "domainName",
    d.domainId AS "domainId",
    h.ipAddress AS "ipAddress",
    macAddress AS "macAddress",
    dc.dhcpScopeId AS "dhcpScopeId",
    dc.dhcpScopeName AS "dhcpScopeName",
    dc.dhcpNetmask AS "dhcpNetmask"
FROM hosts h
LEFT JOIN domains d ON h.domainId=d.domainId
LEFT JOIN dhcpScopes dc ON h.dhcpScopeId=dc.dhcpScopeId
WHERE h.hostId=%s
'''
GET_USED_DHCP_ADDRESSES='''
SELECT
    ipAddress,
    ipAddressInt
FROM hosts
WHERE dhcpScopeId=%s
ORDER BY ipAddressInt ASC
'''
GET_SERVICES='''
SELECT
	s.serviceId AS "serviceId",
	s.serviceName || '.' || d.domainName AS "domainName",
	s.targetHostId AS "targetHostId",
	h.hostname || '.' || (SELECT domainName FROM domains WHERE domainID=h.domainId) AS target,
	d.domainName AS "baseDomain",
	d.domainId AS "domainId",
    s.description
FROM services s
LEFT JOIN domains d ON s.domainId=d.domainId
LEFT JOIN hosts h 	ON s.targetHostId=h.hostId
ORDER BY domainName ASC
'''
GET_SERVICES_FOR_HOST='''
SELECT
	s.serviceId AS "serviceId",
	s.serviceName || '.' || d.domainName AS "domainName",
	s.targetHostId AS "targetHostId",
	h.hostname || '.' || (SELECT domainName FROM domains WHERE domainID=h.domainId) AS target,
	d.domainName AS "baseDomain",
	d.domainId AS "domainId",
    s.description
FROM services s
LEFT JOIN domains d ON s.domainId=d.domainId
LEFT JOIN hosts h 	ON s.targetHostId=h.hostId
WHERE s.targetHostId=%s
ORDER BY domainName ASC
'''
ADD_HOST_ALIAS='''
INSERT INTO opnsense_aliases (alias_id, is_host_alias, alias_name, alias_display_name)
VALUES (%(alias_id)s, TRUE, %(alias_name)s, %(alias_display_name)s)
'''
SET_HOST_ALIAS='''
UPDATE hosts
SET host_alias_id = %(host_alias_id)s
'''
REGISTER_ALIAS_GROUP='''
INSERT INTO opnsense_aliases (alias_id, is_host_alias, alias_name, category_id, alias_description, alias_display_name)
VALUES (%(alias_id)s, %(is_host_alias)s, %(alias_name)s, %(category_id)s, %(alias_description)s, %(alias_display_name)s)
'''
GET_ALIAS_GROUPS='''
SELECT
    alias_id                AS "aliasId",
    alias_name              AS "aliasName",
    category_id             AS "categoryId",
    alias_description       AS "aliasDescription",
    alias_display_name      AS "aliasDisplayName"
FROM opnsense_aliases
WHERE is_host_alias = FALSE
'''