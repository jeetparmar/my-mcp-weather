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
uv run python weather.py
```

The server runs on stdio transport, making it compatible with MCP clients using local stdio pipes.

## Integration with Claude Desktop

To use this weather server with Claude Desktop, add the following configuration to your `claude_desktop_config.json` file (located at `~/.config/Claude/claude_desktop_config.json` on Linux/Mac or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "weather": {
      "command": "/Users/computer-name/.local/bin/uv",
      // find it above path using which uv
      "args": [
        "--directory",
        "/Users/path-to-project/my-mcp-weather",
        // find it this too using "pwd"
        "run",
        "weather.py"
      ]
    }
  }
}
```

Replace the paths with your actual installation paths. Once configured, Claude Desktop will have access to the weather tools for getting alerts and forecasts.

## Example Queries

Here are some example queries you can use with Claude Desktop to interact with the weather MCP server:

### Get Weather Alerts

**Query:** "Using the weather tool, get current alerts for San Francisco,CA"

**Query:** "Check weather alerts in New York,NY"

**Query:** "Are there any weather alerts for 95128 (San Jose zip code)?"

### Get Weather Forecast

**Query:** "Using the weather tool, get a 5-day forecast for Los Angeles,CA"

**Query:** "What's the weather forecast for Chicago,IL for the next 3 days?"

**Query:** "Show me the forecast for 10001 (New York City zip code)"

### Combined Requests

**Query:** "Check current weather alerts for rainfall and give me a 3-day forecast for Portland,OR"

**Query:** "Are there any severe weather alerts for Houston,TX? If not, show me tomorrow's forecast"

These queries will trigger the weather server to fetch real-time data from the National Weather Service API and return formatted weather information directly in Claude Desktop.

## API Source

This server uses the [National Weather Service API](https://www.weather.gov/documentation/services-web-api), which provides free weather data for US locations.

## Author

jeetparmar33@gmail.com
