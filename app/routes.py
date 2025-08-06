from flask import Flask, request, jsonify
from datetime import datetime
from .config import Config
from .services.airtable import log_to_airtable
from .services.geocode import get_zip_and_city
from .services.weather import get_weather
from .utils.exceptions import InvalidPayloadError, UnauthorizedError

def register_routes(app: Flask):

    @app.route("/airtable-test", methods=["GET"])
    def airtable_test():
        import requests
        url = f"https://api.airtable.com/v0/{Config.AIRTABLE_BASE_ID}/{Config.AIRTABLE_TABLE_NAME}"
        headers = {"Authorization": f"Bearer {Config.AIRTABLE_TOKEN}"}
        try:
            r = requests.get(url, headers=headers)
            return jsonify({"status_code": r.status_code, "response": r.text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/checkin", methods=["POST"])
    def checkin():
        try:
            if request.headers.get("X-API-Token") != Config.API_TOKEN:
                raise UnauthorizedError("Invalid API token")

            data = request.get_json()
            if not data or "status" not in data or "location" not in data:
                raise InvalidPayloadError("Missing required fields")

            lat = data["location"].get("lat")
            lon = data["location"].get("lon")
            if lat is None or lon is None:
                raise InvalidPayloadError("Missing coordinates")

            zip_code, city = get_zip_and_city(lat, lon)
            temp, desc = get_weather(zip_code)
            timestamp = datetime.utcnow().isoformat()

            success = log_to_airtable(data['status'], timestamp, zip_code, city, temp, desc)
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

        except UnauthorizedError as ue:
            return jsonify({"error": str(ue)}), 401
        except InvalidPayloadError as pe:
            return jsonify({"error": str(pe)}), 400
        except Exception as e:
            return jsonify({"error": f"Unhandled exception: {str(e)}"}), 500
