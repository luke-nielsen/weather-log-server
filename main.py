from flask import Flask, request, jsonify
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)

API_TOKEN = os.environ.get("API_TOKEN")
GEOCODE_API_KEY = os.environ.get("GEOCODE_API_KEY")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

AIRTABLE_TOKEN = os.environ.get("AIRTABLE_TOKEN")
AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.environ.get("AIRTABLE_TABLE_NAME")


def log_to_airtable(status, timestamp, zip_code, city, temperature,
                    weather_desc):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "records": [{
            "fields": {
                "Status": status,
                "Timestamp": timestamp,
                "Zip Code": zip_code,
                "City": city,
                "Temperature": temperature,
                "Weather Description": weather_desc
            }
        }]
    }

    print("\n== Airtable Logging Attempt ==")
    print("URL:", url)
    print("Headers:", headers)
    print("Payload:", json.dumps(payload, indent=2))

    try:
        resp = requests.post(url, headers=headers, json=payload)
        print("Response Code:", resp.status_code)
        print("Response Body:", resp.text)
        return resp.status_code in (200, 201)
    except requests.exceptions.RequestException as e:
        print("Request Exception:", str(e))
        return False


def get_zip_and_city(lat, lon):
    url = f"http://api.positionstack.com/v1/reverse?access_key={GEOCODE_API_KEY}&query={lat},{lon}"
    print(f"Calling PositionStack: {url}")
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json().get("data", [{}])[0]
        print("PositionStack response:", data)
        return data.get("postal_code", "N/A"), data.get("locality", "N/A")
    except Exception as e:
        print("Geocoding failed:", e)
        return "N/A", "N/A"


def get_weather(zip_code):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={zip_code}"
    print(f"Calling WeatherAPI: {url}")
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        print("WeatherAPI response:", data)
        temp = data.get("current", {}).get("temp_f", "N/A")
        desc = data.get("current", {}).get("condition", {}).get("text", "N/A")
        return temp, desc
    except Exception as e:
        print("Weather fetch failed:", e)
        return "N/A", "N/A"


@app.route("/airtable-test", methods=["GET"])
def airtable_test():
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}
    try:
        r = requests.get(url, headers=headers)
        return jsonify({"status_code": r.status_code, "response": r.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/checkin", methods=["POST"])
def checkin():
    print("== Incoming Check-In Request ==")
    incoming_token = request.headers.get("X-API-Token")
    if incoming_token != API_TOKEN:
        print("Invalid API token")
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    print("Payload:", data)

    if not data or "status" not in data or "location" not in data:
        print("Malformed payload")
        return jsonify({"error": "Invalid JSON"}), 400

    lat = data["location"].get("lat")
    lon = data["location"].get("lon")
    if lat is None or lon is None:
        print("Missing coordinates in payload")
        return jsonify({"error": "Missing coordinates"}), 400

    zip_code, city = get_zip_and_city(lat, lon)
    temp, desc = get_weather(zip_code)
    timestamp = datetime.utcnow().isoformat()

    success = log_to_airtable(data['status'], timestamp, zip_code, city, temp,
                              desc)

    if not success:
        return jsonify({"error": "Airtable logging failed"}), 500

    return jsonify({
        "status": data['status'],
        "timestamp": timestamp,
        "zip": zip_code,
        "city": city,
        "temperature": temp,
        "weather": desc
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
