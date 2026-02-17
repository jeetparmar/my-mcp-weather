from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server with a name
mcp = FastMCP("weather")

# Constants for the National Weather Service API
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "my-mcp-weather/1.0 (jeetparmar33@gmail.com)"  # NWS requires contact info


@mcp.tool()
async def get_alerts(location: str) -> dict[str, Any]:
    """Get current weather alerts for a US location (city,state or zip)."""
    try:
        # Step 1: Get grid points for the location
        async with httpx.AsyncClient(headers={"User-Agent": USER_AGENT}) as client:
            point_resp = await client.get(f"{NWS_API_BASE}/points/{location}")
            point_resp.raise_for_status()
            point_data = point_resp.json()

            grid_id = point_data["properties"]["gridId"]
            grid_x = point_data["properties"]["gridX"]
            grid_y = point_data["properties"]["gridY"]

            # Step 2: Get alerts for that grid
            alerts_resp = await client.get(
                f"{NWS_API_BASE}/alerts/active?point={point_data['properties']['relativeLocation']['properties']['city']},{point_data['properties']['relativeLocation']['properties']['state']}"
            )
            alerts_resp.raise_for_status()
            alerts = alerts_resp.json()

            return {
                "alerts": [
                    {
                        "event": a["properties"]["event"],
                        "headline": a["properties"]["headline"],
                        "description": a["properties"]["description"],
                        "severity": a["properties"]["severity"],
                        "expires": a["properties"]["expires"],
                    }
                    for a in alerts.get("features", [])
                ]
            }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_forecast(location: str, days: int = 3) -> dict[str, Any]:
    """Get weather forecast for a US location (city,state or zip) for the next N days."""
    try:
        async with httpx.AsyncClient(headers={"User-Agent": USER_AGENT}) as client:
            point_resp = await client.get(f"{NWS_API_BASE}/points/{location}")
            point_resp.raise_for_status()
            point_data = point_resp.json()

            forecast_url = point_data["properties"]["forecast"]

            forecast_resp = await client.get(forecast_url)
            forecast_resp.raise_for_status()
            periods = forecast_resp.json()["properties"]["periods"]

            forecast = []
            for period in periods[: days * 2]:  # roughly 2 periods per day
                forecast.append(
                    {
                        "time": period["startTime"],
                        "name": period["name"],
                        "temp": period["temperature"],
                        "wind": period["windSpeed"],
                        "short_forecast": period["shortForecast"],
                        "detailed": period["detailedForecast"],
                    }
                )

            return {"forecast": forecast}
    except Exception as e:
        return {"error": str(e)}


def main():
    # Run the server (stdio transport = local stdio pipe, most common for desktop)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
