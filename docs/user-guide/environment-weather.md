# Environment & Weather

**Tools:** 19

Examples use the Google ADK callable wrapper surface so each example is directly executable as ordinary Python.

## Tool Index

| Tool |
|---|
| [`fetch_google_weather_current`](#fetch_google_weather_current) |
| [`fetch_google_weather_hourly_forecast`](#fetch_google_weather_hourly_forecast) |
| [`fetch_google_weather_daily_forecast`](#fetch_google_weather_daily_forecast) |
| [`fetch_google_weather_hourly_history`](#fetch_google_weather_hourly_history) |
| [`fetch_google_weather_alerts`](#fetch_google_weather_alerts) |
| [`fetch_earth_observatory`](#fetch_earth_observatory) |
| [`fetch_open_weather`](#fetch_open_weather) |
| [`fetch_historical_weather`](#fetch_historical_weather) |
| [`fetch_usgs_earthquakes`](#fetch_usgs_earthquakes) |
| [`fetch_usgs_water_data`](#fetch_usgs_water_data) |
| [`fetch_air_now`](#fetch_air_now) |
| [`fetch_climate_data`](#fetch_climate_data) |
| [`fetch_eonet`](#fetch_eonet) |
| [`fetch_envirofacts`](#fetch_envirofacts) |
| [`fetch_tides_and_currents`](#fetch_tides_and_currents) |
| [`fetch_uv_index`](#fetch_uv_index) |
| [`fetch_purple_air`](#fetch_purple_air) |
| [`fetch_open_aq`](#fetch_open_aq) |
| [`fetch_firms`](#fetch_firms) |

---

## `fetch_google_weather_current`

Retrieve google weather current data.

### Signature

```python
def fetch_google_weather_current( address: str, units_system: str='METRIC', language_code: str='en', time: int=10 ) -> Any
```

### Purpose

Retrieve google weather current data through Google Weather.

### Example

```python
from fonky.gemini.tools import fetch_google_weather_current

result = fetch_google_weather_current(
    address='1600 Pennsylvania Avenue NW, Washington, DC' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `address` | `str` | Street address or place description used for geocoding, validation, or routing. |
| `units_system` | `str` | Measurement unit system requested from the provider. |
| `language_code` | `str` | BCP-47-style language code used for provider results. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_google_weather_hourly_forecast`

Retrieve hourly forecast.

### Signature

```python
def fetch_google_weather_hourly_forecast( address: str, hours: int=24, units_system: str='METRIC', language_code: str='en', time: int=10 ) -> Any
```

### Purpose

Retrieve hourly forecast through Google Weather.

### Example

```python
from fonky.gemini.tools import fetch_google_weather_hourly_forecast

result = fetch_google_weather_hourly_forecast(
    address='1600 Pennsylvania Avenue NW, Washington, DC' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `address` | `str` | Street address or place description used for geocoding, validation, or routing. |
| `hours` | `int` | Number of hourly observations or forecast periods to request. |
| `units_system` | `str` | Measurement unit system requested from the provider. |
| `language_code` | `str` | BCP-47-style language code used for provider results. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_google_weather_daily_forecast`

Retrieve daily forecast.

### Signature

```python
def fetch_google_weather_daily_forecast( address: str, days: int=5, units_system: str='METRIC', language_code: str='en', time: int=10 ) -> Any
```

### Purpose

Retrieve daily forecast through Google Weather.

### Example

```python
from fonky.gemini.tools import fetch_google_weather_daily_forecast

result = fetch_google_weather_daily_forecast(
    address='1600 Pennsylvania Avenue NW, Washington, DC' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `address` | `str` | Street address or place description used for geocoding, validation, or routing. |
| `days` | `int` | Number of calendar days included in the requested interval. |
| `units_system` | `str` | Measurement unit system requested from the provider. |
| `language_code` | `str` | BCP-47-style language code used for provider results. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_google_weather_hourly_history`

Retrieve hourly history.

### Signature

```python
def fetch_google_weather_hourly_history( address: str, hours: int=24, units_system: str='METRIC', language_code: str='en', time: int=10 ) -> Any
```

### Purpose

Retrieve hourly history through Google Weather.

### Example

```python
from fonky.gemini.tools import fetch_google_weather_hourly_history

result = fetch_google_weather_hourly_history(
    address='1600 Pennsylvania Avenue NW, Washington, DC' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `address` | `str` | Street address or place description used for geocoding, validation, or routing. |
| `hours` | `int` | Number of hourly observations or forecast periods to request. |
| `units_system` | `str` | Measurement unit system requested from the provider. |
| `language_code` | `str` | BCP-47-style language code used for provider results. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_google_weather_alerts`

Retrieve google weather alerts data.

### Signature

```python
def fetch_google_weather_alerts( address: str, language_code: str='en', time: int=10 ) -> Any
```

### Purpose

Retrieve google weather alerts data through Google Weather.

### Example

```python
from fonky.gemini.tools import fetch_google_weather_alerts

result = fetch_google_weather_alerts(
    address='1600 Pennsylvania Avenue NW, Washington, DC' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `address` | `str` | Street address or place description used for geocoding, validation, or routing. |
| `language_code` | `str` | BCP-47-style language code used for provider results. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_earth_observatory`

Retrieve NASA EONET events, categories, sources, and layers.

### Signature

```python
def fetch_earth_observatory( mode: str='events', status: str='open', category: str='', source: str='', limit: int=20, days: int=30, start_date: str='', end_date: str='', time: int=20 ) -> Any
```

### Purpose

Retrieve NASA EONET events, categories, sources, and layers through NASA EONET. Date and time arguments constrain the requested interval when supplied. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_earth_observatory

result = fetch_earth_observatory( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `status` | `str` | Provider status filter applied to returned records. |
| `category` | `str` | Optional logical category retained in tool metadata. |
| `source` | `str` | Provider source identifier used to restrict or classify results. |
| `limit` | `int` | Maximum number of records or items to return. |
| `days` | `int` | Number of calendar days included in the requested interval. |
| `start_date` | `str` | Inclusive start date for the requested time range, in the provider-supported format. |
| `end_date` | `str` | Inclusive end date for the requested time range, in the provider-supported format. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_open_weather`

Retrieve Open-Meteo current and forecast weather.

### Signature

```python
def fetch_open_weather( location: str, mode: str='current', zone: str='auto', forecast_days: int=7, past_days: int=0, count: int=10 ) -> Any
```

### Purpose

Retrieve Open-Meteo current and forecast weather through Open-Meteo.

### Example

```python
from fonky.gemini.tools import fetch_open_weather

result = fetch_open_weather(
    location='Washington, DC' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `location` | `str` | Place name, address, or location description resolved by the provider. |
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `zone` | `str` | Timezone identifier or automatic timezone-selection mode. |
| `forecast_days` | `int` | Number of forecast days to request. |
| `past_days` | `int` | Number of historical days to include with the weather request. |
| `count` | `int` | Maximum number of matching locations or records to consider. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_historical_weather`

Retrieve historical weather archive.

### Signature

```python
def fetch_historical_weather( location: str, date: dt.date, zone: str='auto', count: int=10 ) -> Any
```

### Purpose

Retrieve historical weather archive through Open-Meteo Archive.

### Example

```python
from fonky.gemini.tools import fetch_historical_weather

result = fetch_historical_weather(
    location='Washington, DC',
    date='2026-08-01' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `location` | `str` | Place name, address, or location description resolved by the provider. |
| `date` | `dt.date` | Date used by the provider or processing operation. |
| `zone` | `str` | Timezone identifier or automatic timezone-selection mode. |
| `count` | `int` | Maximum number of matching locations or records to consider. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_usgs_earthquakes`

Retrieve USGS earthquake feed and query.

### Signature

```python
def fetch_usgs_earthquakes( mode: str='feed', feed: str='all_day.geojson', start_date: str='', end_date: str='', min_magnitude: float=1.0, max_magnitude: float=10.0, limit: int=25, order_by: str='time', event_type: str='earthquake', latitude: float | None=None, longitude: float | None=None, max_radius_km: float | None=None, time: int=20 ) -> Any
```

### Purpose

Retrieve USGS earthquake feed and query through USGS Earthquake Hazards Program. Use ``mode`` to select among ``feed``, ``search``. Date and time arguments constrain the requested interval when supplied. Coordinate and bounding arguments constrain geographic scope when supported. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_usgs_earthquakes

result = fetch_usgs_earthquakes( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``feed``, ``search``. |
| `feed` | `str` | Predefined USGS earthquake feed name used when feed mode is selected. |
| `start_date` | `str` | Inclusive start date for the requested time range, in the provider-supported format. |
| `end_date` | `str` | Inclusive end date for the requested time range, in the provider-supported format. |
| `min_magnitude` | `float` | Minimum earthquake magnitude to include in the result set. |
| `max_magnitude` | `float` | Maximum earthquake magnitude to include in the result set. |
| `limit` | `int` | Maximum number of records or items to return. |
| `order_by` | `str` | Provider-supported field used to order results. |
| `event_type` | `str` | USGS event type to include; ``earthquake`` is the default. |
| `latitude` | `float | None` | Latitude in decimal degrees. |
| `longitude` | `float | None` | Longitude in decimal degrees. |
| `max_radius_km` | `float | None` | Maximum geographic search radius in kilometers. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_usgs_water_data`

Retrieve USGS water services records.

### Signature

```python
def fetch_usgs_water_data( mode: str='monitoring-locations', monitoring_location_id: str='', state_code: str='', county_code: str='', site_type: str='', parameter_code: str='', limit: int=25, time: int=20 ) -> Any
```

### Purpose

Retrieve USGS water services records through USGS Water Data. Use ``mode`` to select among ``latest-continuous``, ``latest-daily``, ``monitoring-locations``, ``time-series-metadata``. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_usgs_water_data

result = fetch_usgs_water_data( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``latest- continuous``, ``latest-daily``, ``monitoring-locations``, ``time-series-metadata``. |
| `monitoring_location_id` | `str` | USGS monitoring-location identifier used to target a specific site. |
| `state_code` | `str` | State code used to restrict provider records. |
| `county_code` | `str` | County code used to restrict provider records. |
| `site_type` | `str` | USGS site-type code used to restrict monitoring locations. |
| `parameter_code` | `str` | USGS parameter code identifying the measured property. |
| `limit` | `int` | Maximum number of records or items to return. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_air_now`

Retrieve AirNow current and forecast air quality data.

### Signature

```python
def fetch_air_now( mode: str='current-zip', zip_code: str='', latitude: float | None=None, longitude: float | None=None, date: str='', distance: int=25, time: int=20 ) -> Any
```

### Purpose

Retrieve AirNow current and forecast air quality data through AirNow. Use ``mode`` to select among ``current-latlon``, ``current-zip``, ``forecast-latlon``, ``forecast-zip``. Coordinate and bounding arguments constrain geographic scope when supported.

### Example

```python
from fonky.gemini.tools import fetch_air_now

result = fetch_air_now( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``current- latlon``, ``current-zip``, ``forecast-latlon``, ``forecast-zip``. |
| `zip_code` | `str` | Provider code identifying or filtering zip. |
| `latitude` | `float | None` | Latitude in decimal degrees. |
| `longitude` | `float | None` | Longitude in decimal degrees. |
| `date` | `str` | Date used by the provider or processing operation. |
| `distance` | `int` | Maximum provider search distance, using the units defined by that service. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_climate_data`

Retrieve NOAA climate dataset and data records.

### Signature

```python
def fetch_climate_data( mode: str='datasets', keyword: str='', dataset: str='', start_date: str='', end_date: str='', stations: str='', data_types: str='', limit: int=25, offset: int=0, time: int=20 ) -> Any
```

### Purpose

Retrieve NOAA climate dataset and data records through NOAA climate services. Use ``mode`` to select among ``data``, ``datasets``. Date and time arguments constrain the requested interval when supplied. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_climate_data

result = fetch_climate_data( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``data``, ``datasets``. |
| `keyword` | `str` | Keyword used to filter provider records. |
| `dataset` | `str` | Provider dataset name or identifier. |
| `start_date` | `str` | Inclusive start date for the requested time range, in the provider-supported format. |
| `end_date` | `str` | Inclusive end date for the requested time range, in the provider-supported format. |
| `stations` | `str` | Station identifiers used to restrict climate observations. |
| `data_types` | `str` | Climate data-type identifiers requested from the provider. |
| `limit` | `int` | Maximum number of records or items to return. |
| `offset` | `int` | Zero-based result offset used for pagination. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_eonet`

Retrieve NASA EONET environmental event data.

### Signature

```python
def fetch_eonet( mode: str='events', source: str='', category: str='', status: str='open', limit: int=25, days: int=30, start_date: str='', end_date: str='', bbox: str='', time: int=20 ) -> Any
```

### Purpose

Retrieve NASA EONET environmental event data through NASA EONET. Use ``mode`` to select among ``categories``, ``events``. Date and time arguments constrain the requested interval when supplied. Coordinate and bounding arguments constrain geographic scope when supported. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_eonet

result = fetch_eonet( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``categories``, ``events``. |
| `source` | `str` | Provider source identifier used to restrict or classify results. |
| `category` | `str` | Optional logical category retained in tool metadata. |
| `status` | `str` | Provider status filter applied to returned records. |
| `limit` | `int` | Maximum number of records or items to return. |
| `days` | `int` | Number of calendar days included in the requested interval. |
| `start_date` | `str` | Inclusive start date for the requested time range, in the provider-supported format. |
| `end_date` | `str` | Inclusive end date for the requested time range, in the provider-supported format. |
| `bbox` | `str` | Bounding box defining the geographic extent of the request. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_envirofacts`

Retrieve EPA Envirofacts table and facility records.

### Signature

```python
def fetch_envirofacts( table_name: str='TRI_FACILITY', state_code: str='', facility_name: str='', limit: int=25, time: int=20 ) -> Any
```

### Purpose

Retrieve EPA Envirofacts table and facility records through EPA Envirofacts. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_envirofacts

result = fetch_envirofacts( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `table_name` | `str` | Envirofacts table or resource name to query. |
| `state_code` | `str` | State code used to restrict provider records. |
| `facility_name` | `str` | Facility-name filter applied to Envirofacts records. |
| `limit` | `int` | Maximum number of records or items to return. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_tides_and_currents`

Retrieve NOAA tides, currents, and station data.

### Signature

```python
def fetch_tides_and_currents( mode: str='water-level', station_id: str='', begin_date: str='', end_date: str='', datum: str='MLLW', units: str='metric', time_zone: str='gmt', interval: str='hilo', time: int=20 ) -> Any
```

### Purpose

Retrieve NOAA tides, currents, and station data through NOAA Tides & Currents. Use ``mode`` to select among ``station``, ``tide-predictions``, ``water-level``. Date and time arguments constrain the requested interval when supplied.

### Example

```python
from fonky.gemini.tools import fetch_tides_and_currents

result = fetch_tides_and_currents( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``station``, ``tide-predictions``, ``water-level``. |
| `station_id` | `str` | Provider identifier for the selected station. |
| `begin_date` | `str` | Beginning date for the requested interval, in the provider-supported format. |
| `end_date` | `str` | Inclusive end date for the requested time range, in the provider-supported format. |
| `datum` | `str` | Vertical datum used for tide or water-level measurements. |
| `units` | `str` | Unit system used for returned measurements. |
| `time_zone` | `str` | Timezone used for returned tide or current timestamps. |
| `interval` | `str` | Provider sampling or reporting interval. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_uv_index`

Retrieve EPA UV Index current and forecast data.

### Signature

```python
def fetch_uv_index( mode: str='daily-zip', zip_code: str='', city: str='', state: str='', time: int=20 ) -> Any
```

### Purpose

Retrieve EPA UV Index current and forecast data through EPA UV Index. Use ``mode`` to select among ``daily-city-state``, ``daily-zip``, ``hourly-city-state``, ``hourly-zip``.

### Example

```python
from fonky.gemini.tools import fetch_uv_index

result = fetch_uv_index( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``daily- city-state``, ``daily-zip``, ``hourly-city-state``, ``hourly-zip``. |
| `zip_code` | `str` | Provider code identifying or filtering zip. |
| `city` | `str` | City name used to locate or filter provider records. |
| `state` | `str` | State name or abbreviation used to locate or filter provider records. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_purple_air`

Retrieve PurpleAir sensor and air quality records.

### Signature

```python
def fetch_purple_air( mode: str='sensors', sensor_index: int | None=None, nwlng: float | None=None, nwlat: float | None=None, selng: float | None=None, selat: float | None=None, location_type: int=0, max_age: int=0, modified_since: int=0, fields: str='', time: int=20 ) -> Any
```

### Purpose

Retrieve PurpleAir sensor and air quality records through PurpleAir. Use ``mode`` to select among ``sensor``, ``sensors``. Coordinate and bounding arguments constrain geographic scope when supported.

### Example

```python
from fonky.gemini.tools import fetch_purple_air

result = fetch_purple_air( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``sensor``, ``sensors``. |
| `sensor_index` | `int | None` | PurpleAir sensor identifier. |
| `nwlng` | `float | None` | Northwest bounding-box longitude in decimal degrees. |
| `nwlat` | `float | None` | Northwest bounding-box latitude in decimal degrees. |
| `selng` | `float | None` | Southeast bounding-box longitude in decimal degrees. |
| `selat` | `float | None` | Southeast bounding-box latitude in decimal degrees. |
| `location_type` | `int` | Provider type selector for location. |
| `max_age` | `int` | Maximum age permitted by the operation. |
| `modified_since` | `int` | Unix timestamp used to return PurpleAir sensors modified after the specified time. |
| `fields` | `str` | Comma-separated or provider-specific field selection. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_open_aq`

Retrieve OpenAQ location, measurement, and air-quality records.

### Signature

```python
def fetch_open_aq( mode: str='locations', location_id: int | None=None, parameter_id: int | None=None, country_id: int | None=None, coordinates: str='', radius: int=25000, providers_id: str='', parameters_id: str='', limit: int=25, page: int=1, time: int=20 ) -> Any
```

### Purpose

Retrieve OpenAQ location, measurement, and air-quality records through OpenAQ. Use ``mode`` to select among ``countries``, ``latest``, ``locations``, ``parameter_latest``, ``parameters``, ``providers``. Coordinate and bounding arguments constrain geographic scope when supported. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_open_aq

result = fetch_open_aq( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``countries``, ``latest``, ``locations``, ``parameter_latest``, ``parameters``, ``providers``. |
| `location_id` | `int | None` | Provider identifier for the selected location. |
| `parameter_id` | `int | None` | Provider identifier for the selected parameter. |
| `country_id` | `int | None` | Provider identifier for the selected country. |
| `coordinates` | `str` | Latitude/longitude coordinate string used by the provider. |
| `radius` | `int` | Search radius in the units specified by the operation. |
| `providers_id` | `str` | Provider identifier for the selected providers. |
| `parameters_id` | `str` | Provider identifier for the selected parameters. |
| `limit` | `int` | Maximum number of records or items to return. |
| `page` | `int` | One-based result page to request. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_firms`

Retrieve NASA FIRMS active fire data.

### Signature

```python
def fetch_firms( mode: str='area', source: str='VIIRS_SNPP_NRT', area_coordinates: str='world', day_range: int=1, date: str='', sensor: str='ALL', time: int=20 ) -> Any
```

### Purpose

Retrieve NASA FIRMS active fire data through NASA FIRMS. Use ``mode`` to select among ``area``, ``data-availability``.

### Example

```python
from fonky.gemini.tools import fetch_firms

result = fetch_firms( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``area``, ``data-availability``. |
| `source` | `str` | Provider source identifier used to restrict or classify results. |
| `area_coordinates` | `str` | FIRMS area-of-interest coordinates or ``world`` selector. |
| `day_range` | `int` | Number of days included in the FIRMS active-fire request. |
| `date` | `str` | Date used by the provider or processing operation. |
| `sensor` | `str` | Sensor or instrument filter applied to provider results. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---
