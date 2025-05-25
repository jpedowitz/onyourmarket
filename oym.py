from flask import Flask, request
import requests
import os

app = Flask(__name__)

GA4_MEASUREMENT_ID = os.getenv("G-V7FGE844JG")
GA4_API_SECRET = os.getenv("t3nnofJ3Stm57KAu-DUlgg")

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
                "value": 157.00
            }
        }]
    }

    response = requests.post(
        f"https://www.google-analytics.com/mp/collect?measurement_id={GA4_MEASUREMENT_ID}&api_secret={GA4_API_SECRET}",
        json=payload
    )

    return ("ok", 200) if response.status_code == 204 else ("error", 500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
