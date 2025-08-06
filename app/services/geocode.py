import requests
import logging
from app.config import Config

def get_zip_and_city(lat: float, lon: float) -> tuple[str, str]:
    url = f"http://api.positionstack.com/v1/reverse?access_key={Config.GEOCODE_API_KEY}&query={lat},{lon}"
    logging.info(f"Geocode URL: {url}")

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json().get("data", [{}])[0]
        return data.get("postal_code", "N/A"), data.get("locality", "N/A")
    except Exception as e:
        logging.error(f"Geocoding failed: {e}")
        return "N/A", "N/A"
