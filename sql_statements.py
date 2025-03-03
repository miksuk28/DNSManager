GET_DOMAIN_BY_ID="SELECT domainName FROM domains WHERE domainId=?"
GET_DOMAIN_ID="SELECT domainId FROM domains WHERE domainName=?"
ADD_DOMAIN="INSERT INTO domains (domainName) VALUES (?)"
GET_DOMAINS="SELECT domainId, domainName FROM domains"
DELETE_DOMAIN="DELETE FROM domains WHERE domainId=?"
ADD_HOST='''INSERT INTO hosts (hostname, domainId, ipAddress, ipAddressInt, managedDhcp, dhcpScopeId, macAddress)
            VALUES (:hostname, :domainId, :ipAddress, :ipAddressInt, :managedDhcp, :dhcpScopeId, :macAddress)'''
GET_DHCP_SCOPE_ID="SELECT dhcpScopeId FROM dhcpScopes WHERE dhcpScopeName=?"
GET_DHCP_SCOPE='''
SELECT *
FROM dhcpScopes
WHERE dhcpScopeId=?
'''
GET_DHCP_SCOPE_BY_NAME='''
SELECT *
FROM dhcpScopes
WHERE dhcpScopeName=?
'''
ADD_DHCP_SCOPE='''
INSERT INTO dhcpScopes (dhcpScopeName, dhcpStartAddress, dhcpEndAddress, dhcpNetmask)
VALUES (:dhcpScopeName, :dhcpStartAddress, :dhcpEndAddress, :dhcpNetmask)
'''
ADD_SERVICE='''INSERT INTO services (targetHostId, serviceName, domainId, description)
               VALUES (:targetHostId, :serviceName, :domainId, :description)'''
GET_HOST_DOMAIN='''SELECT hostname || '.' || domainName
                   FROM hosts h LEFT JOIN domains d ON h.domainId=d.domainId
                   WHERE h.hostId=?'''
GET_SERVICE_DOMAIN='''SELECT serviceName || '.' || domainName
                      FROM services s LEFT JOIN domains d ON s.domainId=d.domainId
                      WHERE s.serviceId=?'''
REMOVE_SERVICE="DELETE FROM services WHERE serviceId=?"
REMOVE_HOST="DELETE FROM hosts WHERE hostId=?"
GET_HOST='''SELECT h.hostId, hostname, d.domainName, d.domainId, ipAddress, UPPER(macAddress) as macAddress, managedDhcp, h.dhcpScopeId, s.dhcpScopeName FROM hosts h
            LEFT JOIN domains d ON h.domainId=d.domainId
            LEFT JOIN dhcpScopes s ON h.dhcpScopeId=s.dhcpScopeId
            WHERE h.hostId=?'''
GET_HOSTS='''SELECT h.hostname || '.' || d.domainName AS hostname, h.hostId, hostname, d.domainName, d.domainId, ipAddress, UPPER(macAddress) AS macAddress, managedDhcp, h.dhcpScopeId, s.dhcpScopeName FROM hosts h
            LEFT JOIN domains d ON h.domainId=d.domainId
            LEFT JOIN dhcpScopes s ON h.dhcpScopeId=s.dhcpScopeId
            ORDER BY hostname ASC'''
GET_HOST_INFO='''
SELECT
    h.hostId,
    h.hostname || '.' || d.domainName AS hostname,
    d.domainName,
    d.domainId,
    h.ipAddress,
    UPPER(h.macAddress) as macAddress,
    dc.dhcpScopeId,
    dc.dhcpScopeName,
    dc.dhcpNetmask
FROM hosts h
LEFT JOIN domains d ON h.domainId=d.domainId
LEFT JOIN dhcpScopes dc ON h.dhcpScopeId=dc.dhcpScopeId
WHERE h.hostId=?
'''
GET_USED_DHCP_ADDRESSES='''
SELECT
    ipAddress,
    ipAddressInt
FROM hosts
WHERE dhcpScopeId=?
ORDER BY ipAddressInt ASC
'''
GET_SERVICES='''
SELECT
	s.serviceId,
	s.serviceName || '.' || d.domainName AS domainName,
	s.targetHostId,
	h.hostname || '.' || (SELECT domainName FROM domains WHERE domainID=h.domainId) AS target,
	d.domainName AS baseDomain,
	d.domainId,
    s.description
FROM services s
LEFT JOIN domains d ON s.domainId=d.domainId
LEFT JOIN hosts h 	ON s.targetHostId=h.hostId
ORDER BY domainName ASC
'''
GET_SERVICES_FOR_HOST='''
SELECT
	s.serviceId,
	s.serviceName || '.' || d.domainName AS domainName,
	s.targetHostId,
	h.hostname || '.' || (SELECT domainName FROM domains WHERE domainID=h.domainId) AS target,
	d.domainName AS baseDomain,
	d.domainId,
    s.description
FROM services s
LEFT JOIN domains d ON s.domainId=d.domainId
LEFT JOIN hosts h 	ON s.targetHostId=h.hostId
WHERE s.targetHostId=?
ORDER BY domainName ASC
'''