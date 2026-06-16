import os
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFICATION_TOKEN = os.environ.get("VERIFICATION_TOKEN", "abcdef1234567890abcdef1234567890")
ENDPOINT_URL = os.environ.get("ENDPOINT_URL", "")

@app.route("/ebay-webhook", methods=["GET", "POST"])
def ebay_webhook():

    # eBay verification challenge
    if request.method == "GET":
        challenge_code = request.args.get("challenge_code", "")
        if challenge_code:
            combined = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
            hash_value = hashlib.sha256(combined.encode("utf-8")).hexdigest()
            return jsonify({"challengeResponse": hash_value}), 200

    # Account deletion notifications
    if request.method == "POST":
        print("eBay notification received:", request.json)
        return jsonify({"status": "ok"}), 200

    return jsonify({"status": "ok"}), 200

@app.route("/")
def home():
    return "eBay Webhook is running.", 200

if __name__ == "__main__":
    app.run(debug=False)
