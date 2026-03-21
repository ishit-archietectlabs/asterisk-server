from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

DATA_FILE = "/data/endpoints.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    os.makedirs("/data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def generate_pjsip(endpoints):
    os.makedirs("/etc/asterisk", exist_ok=True)
    config = """
[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0
"""

    for ep in endpoints:
        ext = ep["extension"]
        user = ep["username"]
        pwd = ep["password"]

        config += f"""

[{ext}]
type=endpoint
context=default
disallow=all
allow=ulaw
auth={ext}
aors={ext}

[{ext}]
type=auth
auth_type=userpass
username={user}
password={pwd}

[{ext}]
type=aor
max_contacts=1
"""

    with open("/etc/asterisk/pjsip.conf", "w") as f:
        f.write(config)

@app.route("/")
def index():
    return send_from_directory("/app/public", "index.html")

@app.route("/api/endpoints", methods=["GET"])
def get_endpoints():
    return jsonify(load_data())

@app.route("/api/endpoints", methods=["POST"])
def save_endpoints():
    data = request.json
    if not isinstance(data, list):
        return jsonify({"success": False, "error": "Invalid format"})
    
    save_data(data)
    generate_pjsip(data)
    
    # Reload Asterisk PJSIP
    os.system("asterisk -rx 'pjsip reload'")
    
    return jsonify({"success": True})

# IMPORTANT: static file handler
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("/app/public", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
