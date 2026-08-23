# Environmental & Climate

Use this domain for current/historical weather, air quality, climate records, natural hazards,
environmental facilities, tides, water, UV exposure, fires, and earthquake data.

## Capability Map

| Task | Functions |
|---|---|
| Google weather | `fetch_google_weather_current()`, `fetch_google_weather_hourly_forecast()`, `fetch_google_weather_daily_forecast()`, `fetch_google_weather_hourly_history()`, `fetch_google_weather_alerts()` |
| General weather | `fetch_open_weather()`, `fetch_historical_weather()` |
| Earth/natural events | `fetch_earth_observatory()`, `fetch_eonet()` |
| Earthquakes | `fetch_usgs_earthquakes()` |
| Water | `fetch_usgs_water_data()`, `fetch_tides_and_currents()` |
| Air quality | `fetch_air_now()`, `fetch_purple_air()`, `fetch_open_aq()` |
| Climate | `fetch_climate_data()` |
| EPA data | `fetch_envirofacts()` |
| UV | `fetch_uv_index()` |
| Fire/hotspots | `fetch_firms()` |

## Workflow — Current Weather and Forecast

```python
from fonky import fonky

current = fonky.fetch_google_weather_current(
    address='Arlington, VA',
    units_system='METRIC',
    language_code='en'
)

forecast = fonky.fetch_google_weather_daily_forecast(
    address='Arlington, VA',
    days=7,
    units_system='METRIC',
    language_code='en'
)
```

## Workflow — Earthquakes Near a Point

```python
from fonky import fonky

events = fonky.fetch_usgs_earthquakes(
    mode='query',
    start_date='2026-08-01',
    end_date='2026-08-23',
    min_magnitude=3.0,
    latitude=37.8,
    longitude=-122.4,
    max_radius_km=500,
    limit=100,
    order_by='time'
)
```

Use feed mode for standard USGS feed products; use query mode when you need date, magnitude, location,
or radius constraints.

## Workflow — Air Quality Comparison

```python
from fonky import fonky

aqi = fonky.fetch_air_now(
    mode='current-zip',
    zip_code='22201',
    distance=25
)

open_aq = fonky.fetch_open_aq(
    mode='locations',
    coordinates='38.88,-77.10',
    radius=25000,
    limit=25
)
```

These providers do not necessarily use identical pollutant metrics, averaging periods, station
semantics, or quality controls. Compare normalized fields deliberately.

## Workflow — Fire Hotspots

```python
fires = fonky.fetch_firms(
    mode='area',
    source='VIIRS_SNPP_NRT',
    area_coordinates='-125,24,-66,50',
    day_range=1,
    sensor='ALL'
)
```

## Operational Notes

- Weather/history APIs can use different date/time zones and units.
- Environmental measurements can be provisional and provider-specific.
- Air-quality providers differ in sensor networks and data-quality practices.
- Geographic filters should be checked for provider coordinate-order conventions.
