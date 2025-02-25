GET_DOMAIN_BY_ID="SELECT domainName FROM domains WHERE domainId=?"
GET_DOMAIN_ID="SELECT domainId FROM domains WHERE domainName=?"
ADD_HOST='''INSERT INTO hosts (hostname, domainId, ipAddress, managedDhcp, dhcpScopeId, macAddress)
            VALUES (:hostname, :domainId, :ipAddress, :managedDhcp, :dhcpScopeId, :macAddress)'''
GET_DHCP_SCOPE_ID="SELECT dhcpScopeId FROM dhcpScopes WHERE dhcpScopeName=?"
ADD_SERVICE='''INSERT INTO services (targetHostId, serviceName, domainId)
               VALUES (:targetHostId, :serviceName, :domainId)'''
GET_HOST_DOMAIN='''SELECT hostname || '.' || domainName
                   FROM hosts h LEFT JOIN domains d ON h.domainId=d.domainId
                   WHERE h.hostId=?'''
GET_SERVICE_DOMAIN='''SELECT serviceName || '.' || domainName
                      FROM services s LEFT JOIN domains d ON s.domainId=d.domainId
                      WHERE s.serviceId=?'''
REMOVE_SERVICE="DELETE FROM services WHERE serviceId=?"
REMOVE_HOST="DELETE FROM hosts WHERE hostId=?"
GET_HOST='''SELECT h.hostId, hostname, d.domainName, d.domainId, ipAddress, macAddress, managedDhcp, h.dhcpScopeId, s.dhcpScopeName FROM hosts h
            LEFT JOIN domains d ON h.domainId=d.domainId
            LEFT JOIN dhcpScopes s ON h.dhcpScopeId=s.dhcpScopeId
            WHERE h.hostId=?'''
