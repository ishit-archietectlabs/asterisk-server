from flask import Flask, request, jsonify, send_from_directory
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

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
    import os
    os.makedirs("/etc/asterisk", exist_ok=True)

    config = """
[global]
type=global
user_agent=HA-Asterisk
endpoint_identifier_order=auth_username,username,ip

[transport-ws]
type=transport
protocol=ws
bind=0.0.0.0:8088

[transport-wss]
type=transport
protocol=wss
bind=0.0.0.0:8089

[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0:5060

[default]
type=endpoint
context=default
disallow=all
allow=ulaw
"""

    for ep in endpoints:
        ext = str(ep.get("extension") or "")
        user = str(ep.get("username") or "")
        pwd = str(ep.get("password") or "")

        if not user or not ext:
            logging.error(f"Skipping invalid endpoint: {ep}")
            continue

        config += f"""
[{user}]
type=endpoint
context=default
disallow=all
allow=ulaw
webrtc=yes
dtls_auto_generate_cert=yes
ice_support=yes
media_encryption=dtls
dtls_verify=fingerprint
dtls_setup=actpass
auth={user}-auth
aors={user}-aor
transport=transport-ws
identify_by=auth_username

[{user}-auth]
type=auth
auth_type=userpass
username={user}
password={pwd}

[{user}-aor]
type=aor
max_contacts=1
"""

    with open("/etc/asterisk/pjsip.conf", "w") as f:
        f.write(config)

    logging.info("Generated pjsip.conf:")
    logging.info(config)

def generate_extensions():
    os.makedirs("/etc/asterisk", exist_ok=True)
    with open("/etc/asterisk/extensions.conf", "w") as f:
        f.write("""
[default]
exten => _X.,1,Answer()
 same => n,Playback(hello-world)
 same => n,Hangup()
""")
    logging.info("Generated extensions.conf")

@app.route("/")
def index():
    return send_from_directory("/app/public", "index.html")

@app.route("/api/endpoints", methods=["GET"])
def get_endpoints():
    return jsonify(load_data())

@app.route("/api/endpoints", methods=["POST"])
def save_endpoints():
    try:
        data = request.get_json(force=True)

        logging.info(f"Received endpoints: {data}")

        if not isinstance(data, list):
            return jsonify({"success": False, "error": "Invalid format"})

        # Save JSON
        save_data(data)

        # Generate configs
        generate_pjsip(data)
        generate_extensions()

        # RELOAD ASTERISK PROPERLY
        os.system("asterisk -rx 'module reload res_pjsip.so'")
        os.system("asterisk -rx 'pjsip reload'")

        logging.info("Asterisk reloaded successfully")

        return jsonify({"success": True})

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)})

# IMPORTANT: static file handler
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("/app/public", path)

if __name__ == "__main__":
    # Ensure baseline configs exist on startup
    endpoints = load_data()
    generate_pjsip(endpoints)
    generate_extensions()
    
    app.run(host="0.0.0.0", port=8090)
