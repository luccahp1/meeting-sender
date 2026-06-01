"""
Meeting Sender — work laptop side.
Serves a drag-and-drop UI and proxies VTT files to the receiver.
"""

from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

RECEIVER_URL = os.getenv("RECEIVER_URL", "http://192.168.1.100:5002")
AUTH_TOKEN   = os.getenv("AUTH_TOKEN", "changeme")
PORT         = int(os.getenv("PORT", 5001))


@app.route("/")
def index():
    return render_template("index.html", receiver_url=RECEIVER_URL)


@app.route("/send", methods=["POST"])
def send():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    f = request.files["file"]
    if not f.filename.lower().endswith(".vtt"):
        return jsonify({"error": "Only .vtt files are supported"}), 400

    try:
        resp = requests.post(
            f"{RECEIVER_URL}/upload",
            files={"file": (f.filename, f.stream, "text/vtt")},
            headers={"X-Auth-Token": AUTH_TOKEN},
            timeout=30,
        )
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Cannot reach receiver at {RECEIVER_URL}. Is it running?"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "Receiver timed out"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print(f"\n  Meeting Sender running → http://localhost:{PORT}\n")
    app.run(host="0.0.0.0", port=PORT, debug=False)
