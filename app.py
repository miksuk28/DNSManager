from flask import Flask, jsonify, request, make_response
from manager import ManagerException
from waitress import serve
from datetime import datetime
import configparser
import manager


config = configparser.ConfigParser()
config.read("manager.conf")


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
manager = manager.Manager(
    token=config["TECHNITIUM"]["TOKEN"],
    address=config["TECHNITIUM"]["HOST"]
)


@app.route("/header", methods=["GET"])
def get_title():
    try:
        return make_response(config["MANAGER"]["HEADER_TITLE"])
    except:
        return make_response("Manager")


@app.route("/hosts/list", methods=["GET"])
def list_hosts():
    hosts = manager.get_hosts()

    return jsonify(hosts)

@app.route("/hosts/<int:host_id>")
def get_host_info(host_id):
    host = manager.get_host_info(host_id)

    return jsonify(host)
    

@app.route("/hosts", methods=["POST"])
def create_host():
    request_body = request.get_json()

    if not bool(request_body["managedDhcp"]) and not request_body.get("ipAddress"):
        raise ManagerException("error", "Bad request. ipAddress is required when managedDhcp is false", code=400)
    elif request_body["managedDhcp"] and not request_body.get("macAddress"):
        raise ManagerException("error", "Bad request. macAddress is required when managedDhcp is true", code=400)

    manager.add_host(
        hostname=       request_body["hostname"],
        domain=         request_body["domain"],
        managed_dhcp=   bool(request_body["managedDhcp"]),
        address=        request_body.get("ipAddress"),
        mac_address=    request_body.get("macAddress"),
        dhcp_scope=     request_body["dhcpScope"],
        overwrite=      request_body.get("overwrite"),
        create_alias=   request_body.get("createAlias")
    )

    return jsonify({"status": "ok", "message": "Host created"}), 201


@app.route("/hosts/<int:host_id>", methods=["DELETE"])
def delete_host(host_id):
    manager.remove_host(host_id)

    return jsonify({
        "status": "ok",
        "message": f"Deleted host with id {host_id}"
    })


@app.route("/hosts/<int:host_id>/ping", methods=["GET"])
def ping_host(host_id):
    return jsonify(manager.ping_host(host_id))


@app.route("/domains/list", methods=["GET"])
def get_domains():
    domains = manager.get_domains()

    return jsonify(domains)


@app.route("/domains", methods=["POST"])
def create_domain():
    request_body = request.get_json()

    manager.add_domain(request_body["domainName"])

    return jsonify({
        "status":       "ok",
        "message":      f"Domain {request_body['domainName']} created"
    }), 201


@app.route("/domains/<int:domain_id>", methods=["DELETE"])
def delete_domain(domain_id):
    manager.remove_domain(domain_id)

    return jsonify({
        "status":       "ok",
        "message":      f"Domain with id {domain_id} deleted"
    })


@app.route("/services", methods=["POST"])
def create_service():
    request_body = request.get_json()

    manager.add_service(
        service_name=       request_body["serviceName"],
        domain=             request_body["domain"],
        host_id=            request_body["hostId"],
        description=        request_body.get("description") 
    )

    return jsonify({"status": "ok", "message": "Service created"}), 201


@app.route("/services/<int:service_id>", methods=["DELETE"])
def delete_service(service_id):
    manager.remove_service(service_id)
    
    return jsonify({
        "status": "ok",
        "message": f"Deleted service with id {service_id}"
    })



@app.route("/services/list", methods=["GET"])
def list_services():
    on_host_id = request.args.get("hostId")
    services = []

    if on_host_id:
        services = manager.get_services_for_host(on_host_id)
        return jsonify(services)

    services = manager.get_services()
    return jsonify(services)


@app.route("/dhcpscopes/list", methods=["GET"])
def list_dhcp_scopes():
    dhcp_scopes = manager.get_dhcp_scopes()

    return jsonify(dhcp_scopes)


#### FLASK HANDLERS ####
@app.errorhandler(Exception)
def exception_handler(error):
    #if config.getboolean("MANAGER", "USE_DEBUG_SERVER"):
    #    raise error

    message = str(error)
    exception_type = type(error).__name__
    status_code = getattr(error, "code", 500)

    if exception_type in ("IntegrityError"):
        status_code = 400

    return jsonify({"error": message, "exception": exception_type}), status_code


@app.after_request
def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"

    # Waitress specific logging
    if not config.getboolean("MANAGER", "USE_DEBUG_SERVER", fallback=False):
        timestamp = datetime.now().strftime('[%Y-%b-%d %H:%M]')
        print(f"{timestamp} {request.remote_addr} {request.method} {request.scheme} {request.full_path} {response.status}")

    return response


if __name__ == "__main__":
    if config.getboolean("MANAGER", "USE_DEBUG_SERVER", fallback=False):
        app.run(host=config["MANAGER"]["BIND_HOST"],
                port=config["MANAGER"]["BIND_PORT"],
                debug=config.getboolean("MANAGER", "USE_DEBUG_SERVER", fallback=False))
    else:
        serve(
            app,
            host=config["MANAGER"]["BIND_HOST"],
            port=config["MANAGER"]["BIND_PORT"],
            threads=config.getint("MANAGER", "WAITRESS_THREADS", fallback=100)
        )