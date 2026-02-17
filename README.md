# Weather MCP Server

An MCP (Model Context Protocol) server that provides real-time weather alerts and forecasts using the National Weather Service API.

## Features

- **Weather Alerts**: Get current weather alerts for US locations (by city, state, or zip code)
- **Weather Forecast**: Get weather forecasts for the next N days for any US location
- Async/await support for efficient API calls
- Proper error handling and user-agent headers for NWS API compliance

## Requirements

- Python 3.12+
- httpx (async HTTP client)
- mcp (Model Context Protocol)

## Installation

1. Clone the repository
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   uv add "mcp[cli]" httpx
   ```

## Available Tools

### get_alerts(location: str) -> dict

Get current weather alerts for a US location.

**Parameters:**

- `location` (str): Location in format "city,state" or ZIP code

**Returns:**

- Dictionary with alerts array containing event, headline, description, severity, and expiry information

### get_forecast(location: str, days: int = 3) -> dict

Get weather forecast for a US location.

**Parameters:**

- `location` (str): Location in format "city,state" or ZIP code
- `days` (int): Number of days to forecast (default: 3)

**Returns:**

- Dictionary with forecast array containing time, name, temperature, wind speed, short forecast, and detailed forecast for each period

## Running the Server

```bash
python weather.py
```

The server runs on stdio transport, making it compatible with MCP clients using local stdio pipes.

## API Source

This server uses the [National Weather Service API](https://www.weather.gov/documentation/services-web-api), which provides free weather data for US locations.

## Author

jeetparmar33@gmail.com
