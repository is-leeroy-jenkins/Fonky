# Environmental & Climate

![Environmental & Climate](../images/fonky-enviro-geo-climate.png)

### Scope

Environmental workflows unify weather, air quality, seismic, hydrologic, climate, UV, fire, and environmental observation sources.

### Key Operations

| Operation                                          | Primary Use                                     |
|----------------------------------------------------|-------------------------------------------------|
| `fetch_google_weather_current`                     | current weather retrieval                       |
| `fetch_google_weather_hourly_forecast`             | hourly forecast retrieval                       |
| `fetch_google_weather_daily_forecast`              | daily forecast retrieval                        |
| `fetch_historical_weather`                         | historical weather archive retrieval            |
| `fetch_usgs_earthquakes`                           | earthquake feed retrieval                       |
| `fetch_usgs_water_data`                            | hydrologic / water data retrieval               |
| `fetch_air_now / fetch_open_aq / fetch_purple_air` | air-quality retrieval across providers          |
| `fetch_envirofacts / fetch_eonet / fetch_firms`    | environmental incidents and related public data |

### Workflow Patterns

- monitor current conditions
- compare history and forecast
- enrich with location context
- feed alerts, dashboards, or geospatial analysis

### Notes

Use environmental tools when the primary data shape is measurement-, event-, or observation-oriented and tied to environment or climate.
