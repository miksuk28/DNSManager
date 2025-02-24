import requests
import config
import sql_statements as sql
from db_manager import DatabaseConnection

class TechnitiumException(Exception):
    def __init__(self, status, error, stacktrace=None):
        # Do logging stuff here
        print("STACKTRACE WOULD BE HERE")
        # Call the base class constructor with the parameters it needs
        super().__init__(error)


class ManagerException(Exception):
    def __init__(self, status, error):
        # Do logging stuff here
        print("Inside ManagerException wooo")
        super().__init__(error)


class Manager(DatabaseConnection):
    def __init__(self, token, address, port="5380", schema="http"):
        super().__init__()
        self.URL = f"{schema}://{address}:{port}/api"
        self.comment = config.MANAGER_DEFAULT_COMMENT
        self.token = token

    
    def _request(self, path, params={}, method="GET"):
        r = requests.request(
            method,
            url=f"{self.URL}{path}",
            params={"token": self.token} | params,
        )
        data = r.json()

        if data["status"] != "ok":
            raise TechnitiumException(data["status"], data["errorMessage"], data.get("stackTrace"))

        return data["response"]


    def get_dhcp_scopes(self):
        return self._request("/dhcp/scopes/list")

    
    def get_static_dhcp_leases(self, scope):
        r = self._request("/dhcp/scopes/get", params={"name": scope})

        return r["reservedLeases"]


    def add_static_dhcp_lease(self, scope, hardware_address, ip_address, hostname, comments=""):
        r = self._request(
            "/dhcp/scopes/addReservedLease",
            params={
                "name": scope,
                "hardwareAddress": hardware_address,
                "ipAddress": ip_address,
                "hostName": hostname,
                "comments": comments
            }
        )

    def remove_static_dhcp_lease(self, scope, hardware_address):
        r = self._request(
            "/dhcp/scopes/removeReservedLease",
            params={
                "name": scope,
                "hardwareAddress": hardware_address
            }
        )
        

    def get_dns_zones(self):
        r = self._request("/zones/list")
        return r["zones"]


    def flush_dns_cache(self):
        r = self._request("/cache/flush")


    def get_dns_records(self, domain, zone=None, list_zone=True):
        r = self._request(
            "/zones/records/get",
            params={
                "domain": domain,
                "zone": zone,
                "listZone": list_zone
            }
        )

        return r["records"]


    def add_dns_record(self, domain, type, target, zone="", overwrite=False, comments=""):
        params={
            "domain": domain,
            "zone": zone,
            "type": type,
            #"ipAddress": address,
            "overwrite": str(overwrite),
            "comments": comments
        }

        if type.upper() == "A":
            params = params | {"ipAddress": target}
        elif type.upper() == "CNAME":
            params = params | {"cname": target}
        else:
            raise TechnitiumException("error", "Only A and CNAME records are supported")

        r = self._request(
            "/zones/records/add",
            params=params
        )


    def _get_domain_by_id(self, domain_id):
        with self.cur() as cur:
            cur.execute(sql.GET_DOMAIN_BY_ID, (domain_id,))
            domain = cur.fetchone()

            if not domain:
                raise ManagerException("error", f"Domain with id {domain_id} does not exist")

            return domain[0]


    def _get_domain_id(self, domain):
        with self.cur() as cur:
            cur.execute(sql.GET_DOMAIN_ID, (domain,))
            domain_id = cur.fetchone()

            if not domain:
                raise ManagerException("error", f"Domain {domain} does not exist")

            return domain_id[0]


    def _get_dhcp_scope_id(self, dhcp_scope):
        with self.cur() as cur:
            cur.execute(sql.GET_DHCP_SCOPE_ID, (dhcp_scope,))
            dhcp_scope_id = cur.fetchone()

            if not dhcp_scope_id:
                raise ManagerException("error", f"DHCP Scope {dhcp_scope} does not exist")

            return dhcp_scope_id[0]


    def add_host(self, hostname, domain, address, managed_dhcp, mac_address=None, dhcp_scope=None, overwrite=False, comments=""):     
        domain_id = self._get_domain_id(domain)
        dhcp_scope_id = None
        if dhcp_scope is not None:
            dhcp_scope_id = self._get_dhcp_scope_id(dhcp_scope)

        with self.cur() as cur:
            # Add to database
            cur.execute(sql.ADD_HOST, {
                "hostname":     hostname,
                "domainId":     domain_id,
                "ipAddress":    address,
                "managedDhcp":  managed_dhcp,
                "dhcpScopeId":  dhcp_scope_id,
                "macAddress":   mac_address
            })
            # Add DNS record
            r = self._request(
                "/zones/records/add",
                params={
                    "domain": f"{hostname}.{domain}",
                    #"zone": zone,
                    "type": "A",
                    "ipAddress": address,
                    "overwrite": True,
                    "comments": self.comment
                }
            )
            # Add DHCP reservation if applicable
            if managed_dhcp:
                self.add_static_dhcp_lease(
                    scope=dhcp_scope,
                    hardware_address=mac_address,
                    ip_address=address,
                    hostname=f"{hostname}.{domain}",
                    comments=self.comment
                )


    def add_dns_cname_record(self, domain, target, zone=None):
        r = self._request(
            "/zones/records/add",
             params={
                "domain": domain,
                "zone": zone,
                "type": "CNAME",
                "cname": target,
                "overwrite": True,
                "comments": self.comment
            }
        )


    def remove_dns_record(self, domain, type, target=None, zone=None):
        '''Deletes the specified A or CNAME record. For A, ipAddress needs to be passed as target'''
        params={
            "domain": domain,
            "type": type,
            "zone": zone
        }
        
        if type == "A":
            params = params | {"ipAddress": target}

        r = self._request(
            "/zones/records/delete",
            params=params
        )



# for testing
api = Manager(
    token=config.TECHNITIUM_TOKEN,
    address=config.TECHNITIUM_ADDRESS
)