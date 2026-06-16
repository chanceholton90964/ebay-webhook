import os
import hmac
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFICATION_TOKEN = os.environ.get("VERIFICATION_TOKEN", "mytoken123")
ENDPOINT_URL = os.environ.get("ENDPOINT_URL", "")

@app.route("/ebay-webhook", methods=["GET", "POST"])
def ebay_webhook():

    # eBay verification challenge (one-time handshake)
    if request.method == "GET":
        challenge_code = request.args.get("challenge_code", "")
        if challenge_code:
            hash_value = hmac.new(
                VERIFICATION_TOKEN.encode("utf-8"),
                (challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL).encode("utf-8"),
                hashlib.sha256
            ).hexdigest()
            return jsonify({"challengeResponse": hash_value}), 200

    # Account deletion notifications — just acknowledge them
    if request.method == "POST":
        print("eBay notification received:", request.json)
        return jsonify({"status": "ok"}), 200

    return jsonify({"status": "ok"}), 200

@app.route("/")
def home():
    return "eBay Webhook is running.", 200

if __name__ == "__main__":
    app.run(debug=False)
