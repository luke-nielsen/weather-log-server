import requests
import logging
from app.config import Config

def get_weather(zip_code: str) -> tuple[str, str]:
    url = f"http://api.weatherapi.com/v1/current.json?key={Config.WEATHER_API_KEY}&q={zip_code}"
    logging.info(f"Weather URL: {url}")

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        temp = data.get("current", {}).get("temp_f", "N/A")
        desc = data.get("current", {}).get("condition", {}).get("text", "N/A")
        return temp, desc
    except Exception as e:
        logging.error(f"Weather fetch failed: {e}")
        return "N/A", "N/A"
