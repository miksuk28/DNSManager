GET_DOMAIN_BY_ID="SELECT domainName FROM domains WHERE domainId=?"
GET_DOMAIN_ID="SELECT domainId FROM domains WHERE domainName=?"
ADD_HOST='''INSERT INTO hosts (hostname, domainId, ipAddress, managedDhcp, dhcpScopeId, macAddress)
            VALUES (:hostname, :domainId, :ipAddress, :managedDhcp, :dhcpScopeId, :macAddress)'''
GET_DHCP_SCOPE_ID="SELECT dhcpScopeId FROM dhcpScopes WHERE dhcpScopeName=?"