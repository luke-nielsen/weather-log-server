import requests
import json
import logging
from app.config import Config

def log_to_airtable(status: str, timestamp: str, zip_code: str, city: str,
                    temperature: str, weather_desc: str) -> bool:
    url = f"https://api.airtable.com/v0/{Config.AIRTABLE_BASE_ID}/{Config.AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {Config.AIRTABLE_TOKEN}",
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

    logging.info(f"Airtable POST URL: {url}")
    logging.debug(f"Airtable Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, headers=headers, json=payload)
        logging.info(f"Airtable response code: {response.status_code}")
        return response.status_code in (200, 201)
    except requests.RequestException as e:
        logging.error(f"Airtable request failed: {e}")
        return False
