from flask import Flask, request
import requests
import os

app = Flask(__name__)

# These should reference ENV VAR names, not the actual ID/secret directly
GA4_MEASUREMENT_ID = os.getenv("GA4_MEASUREMENT_ID")
GA4_API_SECRET = os.getenv("GA4_API_SECRET")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    client_id = data.get("client_id")

    if not client_id:
        return "Missing client_id", 400

    payload = {
        "client_id": client_id,
        "events": [{
            "name": "purchase",
            "params": {
                "currency": "USD",
                "value": 157.00,
                "source": "kajabi_webhook"
            }
        }]
    }
import logging
logging.basicConfig(level=logging.INFO)

# Add this:
print("Sending payload to GA4:", payload)
    response = requests.post(
        f"https://www.google-analytics.com/mp/collect?measurement_id={GA4_MEASUREMENT_ID}&api_secret={GA4_API_SECRET}",
        json=payload
    )

    if response.status_code == 204:
        return ("ok", 200)
    else:
        print(response.text)
        return ("error", 500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
