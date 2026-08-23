# Environmental

Weather, climate, air quality, fires, natural events, tides, earthquakes, water, UV, and environmental records.

## Functional Operations

| Function | Signature | Purpose |
|---|---|---|
| `fetch_google_weather_current()` | `fetch_google_weather_current( address: str, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any` | Fetch current. Provides direct module-level access to ``GoogleWeather.fetch_current`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_current``. |
| `fetch_google_weather_hourly_forecast()` | `fetch_google_weather_hourly_forecast( address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any` | Fetch hourly forecast. Provides direct module-level access to ``GoogleWeather.fetch_hourly_forecast`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_hourly_forecast``. |
| `fetch_google_weather_daily_forecast()` | `fetch_google_weather_daily_forecast( address: str, days: int = 5, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any` | Fetch daily forecast. Provides direct module-level access to ``GoogleWeather.fetch_daily_forecast`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_daily_forecast``. |
| `fetch_google_weather_hourly_history()` | `fetch_google_weather_hourly_history( address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any` | Fetch hourly history. Provides direct module-level access to ``GoogleWeather.fetch_hourly_history`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_hourly_history``. |
| `fetch_google_weather_alerts()` | `fetch_google_weather_alerts( address: str, language_code: str = 'en', time: int = 10 ) -> Any` | Fetch alerts. Provides direct module-level access to ``GoogleWeather.fetch_alerts`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_alerts``. |
| `fetch_earth_observatory()` | `fetch_earth_observatory( mode: str = 'events', status: str = 'open', category: str = '', source: str = '', limit: int = 20, days: int = 30, start_date: str = '', end_date: str = '', time: int = 20 ) -> Any` | Fetch NASA EONET events, categories, sources, and layers. Provides direct module-level access to ``EarthObservatory.fetch`` using a fresh ``EarthObservatory`` instance. Any: Value returned by ``EarthObservatory.fetch``. |
| `fetch_open_weather()` | `fetch_open_weather( location: str, mode: str = 'current', zone: str = 'auto', forecast_days: int = 7, past_days: int = 0, count: int = 10 ) -> Any` | Fetch Open-Meteo current and forecast weather retrieval. Provides direct module-level access to ``OpenWeather.fetch`` using a fresh ``OpenWeather`` instance. Any: Value returned by ``OpenWeather.fetch``. |
| `fetch_historical_weather()` | `fetch_historical_weather( location: str, date: dt.date, zone: str = 'auto', count: int = 10 ) -> Any` | Fetch historical weather archive retrieval. Provides direct module-level access to ``HistoricalWeather.fetch`` using a fresh ``HistoricalWeather`` instance. Any: Value returned by ``HistoricalWeather.fetch``. |
| `fetch_usgs_earthquakes()` | `fetch_usgs_earthquakes( mode: str = 'feed', feed: str = 'all_day.geojson', start_date: str = '', end_date: str = '', min_magnitude: float = 1.0, max_magnitude: float = 10.0, limit: int = 25, order_by: str = 'time', event_type: str = 'earthquake', latitude: float \| None = None, longitude: float \| None = None, max_radius_km: float \| None = None, time: int = 20 ) -> Any` | Fetch USGS earthquake feed and query retrieval. Provides direct module-level access to ``USGSEarthquakes.fetch`` using a fresh ``USGSEarthquakes`` instance. Any: Value returned by ``USGSEarthquakes.fetch``. |
| `fetch_usgs_water_data()` | `fetch_usgs_water_data( mode: str = 'monitoring-locations', monitoring_location_id: str = '', state_code: str = '', county_code: str = '', site_type: str = '', parameter_code: str = '', limit: int = 25, time: int = 20 ) -> Any` | Fetch USGS water services records. Provides direct module-level access to ``USGSWaterData.fetch`` using a fresh ``USGSWaterData`` instance. Any: Value returned by ``USGSWaterData.fetch``. |
| `fetch_air_now()` | `fetch_air_now( mode: str = 'current-zip', zip_code: str = '', latitude: float \| None = None, longitude: float \| None = None, date: str = '', distance: int = 25, time: int = 20 ) -> Any` | Fetch AirNow current and forecast air quality data. Provides direct module-level access to ``AirNow.fetch`` using a fresh ``AirNow`` instance. Any: Value returned by ``AirNow.fetch``. |
| `fetch_climate_data()` | `fetch_climate_data( mode: str = 'datasets', keyword: str = '', dataset: str = '', start_date: str = '', end_date: str = '', stations: str = '', data_types: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any` | Fetch NOAA climate dataset and data records. Provides direct module-level access to ``ClimateData.fetch`` using a fresh ``ClimateData`` instance. Any: Value returned by ``ClimateData.fetch``. |
| `fetch_eonet()` | `fetch_eonet( mode: str = 'events', source: str = '', category: str = '', status: str = 'open', limit: int = 25, days: int = 30, start_date: str = '', end_date: str = '', bbox: str = '', time: int = 20 ) -> Any` | Fetch NASA EONET environmental event data. Provides direct module-level access to ``EoNet.fetch`` using a fresh ``EoNet`` instance. Any: Value returned by ``EoNet.fetch``. |
| `fetch_envirofacts()` | `fetch_envirofacts( table_name: str = 'TRI_FACILITY', state_code: str = '', facility_name: str = '', limit: int = 25, time: int = 20 ) -> Any` | Fetch EPA Envirofacts table and facility records. Provides direct module-level access to ``EnviroFacts.fetch`` using a fresh ``EnviroFacts`` instance. Any: Value returned by ``EnviroFacts.fetch``. |
| `fetch_tides_and_currents()` | `fetch_tides_and_currents( mode: str = 'water-level', station_id: str = '', begin_date: str = '', end_date: str = '', datum: str = 'MLLW', units: str = 'metric', time_zone: str = 'gmt', interval: str = 'hilo', time: int = 20 ) -> Any` | Fetch NOAA tides, currents, and station data. Provides direct module-level access to ``TidesAndCurrents.fetch`` using a fresh ``TidesAndCurrents`` instance. Any: Value returned by ``TidesAndCurrents.fetch``. |
| `fetch_uv_index()` | `fetch_uv_index( mode: str = 'daily-zip', zip_code: str = '', city: str = '', state: str = '', time: int = 20 ) -> Any` | Fetch EPA UV Index current and forecast data. Provides direct module-level access to ``UvIndex.fetch`` using a fresh ``UvIndex`` instance. Any: Value returned by ``UvIndex.fetch``. |
| `fetch_purple_air()` | `fetch_purple_air( mode: str = 'sensors', sensor_index: int = None, nwlng: float \| None = None, nwlat: float \| None = None, selng: float \| None = None, selat: float \| None = None, location_type: int = 0, max_age: int = 0, modified_since: int = 0, fields: str = '', time: int = 20 ) -> Any` | Fetch PurpleAir sensor and air quality records. Provides direct module-level access to ``PurpleAir.fetch`` using a fresh ``PurpleAir`` instance. Any: Value returned by ``PurpleAir.fetch``. |
| `fetch_open_aq()` | `fetch_open_aq( mode: str = 'locations', location_id: int = None, parameter_id: int = None, country_id: int = None, coordinates: str = '', radius: int = 25000, providers_id: str = '', parameters_id: str = '', limit: int = 25, page: int = 1, time: int = 20 ) -> Any` | Fetch OpenAQ location, measurement, and air-quality records. Provides direct module-level access to ``OpenAQ.fetch`` using a fresh ``OpenAQ`` instance. Any: Value returned by ``OpenAQ.fetch``. |
| `fetch_firms()` | `fetch_firms( mode: str = 'area', source: str = 'VIIRS_SNPP_NRT', area_coordinates: str = 'world', day_range: int = 1, date: str = '', sensor: str = 'ALL', time: int = 20 ) -> Any` | Fetch NASA FIRMS active fire data. Provides direct module-level access to ``Firms.fetch`` using a fresh ``Firms`` instance. Any: Value returned by ``Firms.fetch``. |

## How to choose

Use the functional wrapper when one call completes the task. Use the implementation class when you need retained state, helper methods, or direct provider debugging.

## Operational considerations

- Remote providers require network access.
- Rate limits, timeouts, service availability, and response-shape changes remain operational concerns.
- Provider-specific argument validation is enforced by the implementation class.

## Representative Functions

### `fetch_google_weather_current()`

```python
# fetch_google_weather_current( address: str, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

Fetch current. Provides direct module-level access to ``GoogleWeather.fetch_current`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_current``.

### `fetch_google_weather_hourly_forecast()`

```python
# fetch_google_weather_hourly_forecast( address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

Fetch hourly forecast. Provides direct module-level access to ``GoogleWeather.fetch_hourly_forecast`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_hourly_forecast``.

### `fetch_google_weather_daily_forecast()`

```python
# fetch_google_weather_daily_forecast( address: str, days: int = 5, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

Fetch daily forecast. Provides direct module-level access to ``GoogleWeather.fetch_daily_forecast`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_daily_forecast``.

### `fetch_google_weather_hourly_history()`

```python
# fetch_google_weather_hourly_history( address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

Fetch hourly history. Provides direct module-level access to ``GoogleWeather.fetch_hourly_history`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_hourly_history``.

### `fetch_google_weather_alerts()`

```python
# fetch_google_weather_alerts( address: str, language_code: str = 'en', time: int = 10 ) -> Any
```

Fetch alerts. Provides direct module-level access to ``GoogleWeather.fetch_alerts`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_alerts``.

### `fetch_earth_observatory()`

```python
# fetch_earth_observatory( mode: str = 'events', status: str = 'open', category: str = '', source: str = '', limit: int = 20, days: int = 30, start_date: str = '', end_date: str = '', time: int = 20 ) -> Any
```

Fetch NASA EONET events, categories, sources, and layers. Provides direct module-level access to ``EarthObservatory.fetch`` using a fresh ``EarthObservatory`` instance. Any: Value returned by ``EarthObservatory.fetch``.

### `fetch_open_weather()`

```python
# fetch_open_weather( location: str, mode: str = 'current', zone: str = 'auto', forecast_days: int = 7, past_days: int = 0, count: int = 10 ) -> Any
```

Fetch Open-Meteo current and forecast weather retrieval. Provides direct module-level access to ``OpenWeather.fetch`` using a fresh ``OpenWeather`` instance. Any: Value returned by ``OpenWeather.fetch``.

### `fetch_historical_weather()`

```python
# fetch_historical_weather( location: str, date: dt.date, zone: str = 'auto', count: int = 10 ) -> Any
```

Fetch historical weather archive retrieval. Provides direct module-level access to ``HistoricalWeather.fetch`` using a fresh ``HistoricalWeather`` instance. Any: Value returned by ``HistoricalWeather.fetch``.


See [Functional API](../api/fonky.md) for all signatures.
