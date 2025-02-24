import requests

class TechnitiumException(Exception):
    def __init__(self, status, error):            
        # Call the base class constructor with the parameters it needs
        super().__init__(error)



class Manager:
    def __init__(self, token, address, port="5380", schema="http"):
        self.URL = f"{schema}://{address}:{port}/api"
        self.token = token

    
    def _request(self, path, params={}, method="GET"):
        r = requests.request(
            method,
            url=f"{self.URL}{path}",
            params={"token": self.token} | params,
        )
        data = r.json()

        if data["status"] != "ok":
            raise TechnitiumException(data["status"], data["errorMessage"])

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


    def add_dns_a_record(self, domain, address, zone="", overwrite=False, comments=""):     
        r = self._request(
            "/zones/records/add",
            params={
                "domain": domain,
                "zone": zone,
                "type": "A",
                "ipAddress": address,
                "overwrite": str(overwrite),
                "comments": comments
            }
        )


    def add_dns_cname_record(self, domain, target, zone=None, overwrite=False, comments=""):
        r = self._request(
            "/zones/records/add",
             params={
                "domain": domain,
                "zone": zone,
                "type": "CNAME",
                "cname": target,
                "overwrite": str(overwrite),
                "comments": comments
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
