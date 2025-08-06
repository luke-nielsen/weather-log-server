import os


class Config:
    API_TOKEN = os.environ.get("API_TOKEN")
    GEOCODE_API_KEY = os.environ.get("GEOCODE_API_KEY")
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
    AIRTABLE_TOKEN = os.environ.get("AIRTABLE_TOKEN")
    AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
    AIRTABLE_TABLE_NAME = os.environ.get("AIRTABLE_TABLE_NAME")
