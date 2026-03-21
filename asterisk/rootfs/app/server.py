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
    return jsonify({"success": True})

# IMPORTANT: static file handler
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("/app/public", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
