
# Check-In API

A Flask-based REST API that processes location-based check-ins from iOS shortcuts, performs reverse geocoding, fetches weather data, and logs everything to Airtable.

## Features

- **Location Processing**: Accepts GPS coordinates and converts them to ZIP codes and city names
- **Weather Integration**: Fetches current weather data based on location
- **Airtable Logging**: Stores all check-in data in an Airtable database
- **API Authentication**: Secured with token-based authentication
- **Diagnostic Tools**: Built-in endpoint to test Airtable connectivity

## API Endpoints

### POST `/checkin`
Main endpoint for processing check-ins from iOS shortcuts.

**Headers:**
- `X-API-Token`: Your API authentication token

**Request Body:**
```json
{
  "status": "Working",
  "location": {
    "lat": 39.01788646683369,
    "lon": -104.7904912403113
  }
}
```

**Response:**
```json
{
  "status": "Working",
  "timestamp": "2025-08-06T00:17:42.892430",
  "zip": "80921",
  "city": "Colorado Springs",
  "temperature": 90.0,
  "weather": "Partly cloudy"
}
```

### GET `/airtable-test`
Diagnostic endpoint to test Airtable connectivity.

## Environment Variables

Set up the following environment variables in your Replit Secrets:

- `API_TOKEN`: Authentication token for the API
- `GEOCODE_API_KEY`: PositionStack API key for reverse geocoding
- `WEATHER_API_KEY`: WeatherAPI key for weather data
- `AIRTABLE_TOKEN`: Airtable personal access token
- `AIRTABLE_BASE_ID`: Your Airtable base ID
- `AIRTABLE_TABLE_NAME`: Name of your Airtable table

## External Services

### PositionStack
Used for reverse geocoding (converting lat/lon to ZIP and city).
- Website: https://positionstack.com/
- Free tier available

### WeatherAPI
Provides current weather data based on ZIP code.
- Website: https://weatherapi.com/
- Free tier available

### Airtable
Database for storing check-in logs.
- Website: https://airtable.com/
- Required fields in your table:
  - Status (Single line text)
  - Timestamp (Single line text)
  - Zip Code (Single line text)
  - City (Single line text)
  - Temperature (Number)
  - Weather Description (Single line text)

## Deployment

This app is configured to run on Replit with automatic deployment to Cloud Run.

- **Development**: Runs on port 81 locally
- **Production**: Deployed via Replit's deployment feature

## iOS Shortcut Integration

This API is designed to work with iOS Shortcuts that:
1. Get current location
2. Send status and coordinates to the `/checkin` endpoint
3. Include the API token in headers for authentication

## Error Handling

The API includes comprehensive error handling for:
- Invalid API tokens (401)
- Malformed requests (400)
- Missing coordinates (400)
- External API failures (500)
- Airtable logging failures (500)

## Development

To run locally:
1. Set up environment variables in Replit Secrets
2. Click the Run button or use `python main.py`
3. The server will start on `http://0.0.0.0:81`

## Dependencies

- Flask 3.1.0
- Requests 2.32.3
- Python-dotenv 1.0.1
