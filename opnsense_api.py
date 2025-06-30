import requests
import configparser
from requests.auth import HTTPBasicAuth


config = configparser.ConfigParser()
config.read("manager.conf")

class OPNsenseException(Exception):
    def __init__(self, message, code=500):
        self.message =  message
        self.code =     code
        # Do logging stuff here
        # Call the base class constructor with the parameters it needs
        super().__init__(message, code)


class OPNsenseAPI:
    def __init__(self):
        # initiate db connection
        self.URL =      config["FIREWALL"]["OPNSENSE_URL"]
        self._KEY =     config["FIREWALL"]["OPNSENSE_API_KEY"]
        self._SECRET =  config["FIREWALL"]["OPNSENSE_API_SECRET"]
        self.auth =     HTTPBasicAuth(self._KEY, self._SECRET)
        self._HOST_CHAR_REPLACE = [
            (".", "_"),
            ("-", "_")
        ]


    def _request(self, path, params={}, json=None, method="GET"):
        r = requests.request(
            method,
            url=f"{config['FIREWALL']['OPNSENSE_URL']}/api{path}",
            params=params,
            json=json,
            auth=self.auth
        )
        data = r.json()
        if r.status_code > 299 or data.get("result") == "failed":
            raise OPNsenseException(
                message=data.get("message", (data.get("result") or data.get("errorMessage"))),
                code=r.status_code
            )

        print(r.status_code, r.text)

        return data


    def _hostname_to_alias_compat(self, hostname):
        '''transforms hostname to OPNsense compatible alias name'''
        for oldchar, newchar in self._HOST_CHAR_REPLACE:
            hostname = hostname.replace(oldchar, newchar)

        return hostname


    def create_alias(self, alias, target):
        alias = self._hostname_to_alias_compat(alias)
        r = self._request(
            "/firewall/alias/addItem",
            method="POST",
            json={
                "alias": {
                    "type":         "host",
                    "categories":   config.get("FIREWALL", "DEFAULT_ALIAS_CATEGORY_ID", fallback=""),
                    "name":         alias,
                    "content":      target
                }
            }
        )

        return r.get("uuid")


    def _get_alias_by_id(self, alias_id):
        data = self._request("/firewall/alias/export")
        aliases = data["aliases"].get("alias")

        try:
            return aliases[alias_id]
        except KeyError:
            raise OPNsenseException(f"Alias with id {alias_id} does not exist", code=404)


    def get_alias_id(self, alias):
        alias = self._hostname_to_alias_compat(alias)
        data = self._request(f"/firewall/alias/getAliasUUID/{alias}")

        if not data:
            raise OPNsenseException(message=f"Alias with name {alias} does not exist", code=404)
        
        return data["uuid"]


    def get_categories(self):
        data = self._request("/firewall/alias/list_categories")

        return data.get("rows")


    def list_aliases(self):
        data = self._request("/firewall/alias/list_network_aliases")
        
        return data


    def _set_alias(self, alias_id, alias, alias_content):
        r = self._request(
            f"/firewall/alias/setItem/{alias_id}",
            method="POST",
            json={
                "alias": {
                    "categories":       alias.get("categories"),
                    "content":          alias_content,
                    "description":      alias.get("description"),
                    "enabled":          alias.get("enabled"),
                    "interface":        alias.get("interface"),
                    "name":             alias.get("name"),
                    "type":             alias.get("type")
                }
            }
        )

    def add_to_alias(self, alias_id, host):
        alias = self._get_alias_by_id(alias_id)
        alias_content = alias.get("content") + f"\n{host}"

        self._set_alias(alias_id, alias, alias_content)

    def remove_from_alias(self, alias_id, host):
        alias = self._get_alias_by_id(alias_id)
        alias_content = alias.get("content").split("\n")

        if host not in alias_content:
            raise OPNsenseException(
                message=f"Host '{host}' not in alias {alias.get('name')}",
                code=400
            )

        delimiter = "\n"

        alias_content.remove(host)
        alias_content = delimiter.join(alias_content)

        self._set_alias(alias_id, alias, alias_content)
        

    
if __name__ == "__main__":
    print("'api' object exposed for debugging")
    api = OPNsenseAPI()