from flask import Flask, jsonify, request
import manager
import config


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
manager = manager.Manager(
    token=config.TECHNITIUM_TOKEN,
    address=config.TECHNITIUM_ADDRESS
)


@app.route("/hosts/list", methods=["GET"])
def list_hosts():
    hosts = manager.get_hosts()

    return jsonify(hosts)


@app.route("/services/list", methods=["GET"])
def list_services():
    services = manager.get_services()

    return jsonify(services)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)