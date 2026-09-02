# Astronomy & Space

**Tools:** 10

Examples use the Google ADK callable wrapper surface so each example is directly executable as ordinary Python.

## Tool Index

| Tool |
|---|
| [`fetch_naval_observatory`](#fetch_naval_observatory) |
| [`fetch_satellite_center`](#fetch_satellite_center) |
| [`fetch_nearby_objects`](#fetch_nearby_objects) |
| [`fetch_open_science`](#fetch_open_science) |
| [`fetch_space_weather`](#fetch_space_weather) |
| [`fetch_astro_catalog`](#fetch_astro_catalog) |
| [`fetch_astro_query`](#fetch_astro_query) |
| [`fetch_star_map`](#fetch_star_map) |
| [`fetch_star_chart`](#fetch_star_chart) |
| [`fetch_open_sky`](#fetch_open_sky) |

---

## `fetch_naval_observatory`

Retrieve U.S. Naval Observatory celestial-navigation data.

### Signature

```python
def fetch_naval_observatory( mode: str='celnav', date_value: str='', time_value: str='', latitude: float=0.0, longitude: float=0.0, location_label: str='', time: int=20 ) -> Any
```

### Purpose

Retrieve U.S. Naval Observatory celestial-navigation data through U.S. Naval Observatory. Coordinate and bounding arguments constrain geographic scope when supported.

### Example

```python
from fonky.gemini.tools import fetch_naval_observatory

result = fetch_naval_observatory( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `date_value` | `str` | Calendar date used by the selected provider operation. |
| `time_value` | `str` | Clock time or timestamp used by the selected provider operation. |
| `latitude` | `float` | Latitude in decimal degrees. |
| `longitude` | `float` | Longitude in decimal degrees. |
| `location_label` | `str` | Human-readable label associated with the supplied coordinates. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_satellite_center`

Retrieve SSC satellite observatory, ground-station, and location data.

### Signature

```python
def fetch_satellite_center( mode: str='observatories', query: str='', start_time: str='', end_time: str='', coordinate_systems: str='gse', resolution_factor: int=1, time: int=20 ) -> Any
```

### Purpose

Retrieve SSC satellite observatory, ground-station, and location data through NASA Satellite Situation Center. The query text determines the records or documents matched by the provider.

### Example

```python
from fonky.gemini.tools import fetch_satellite_center

result = fetch_satellite_center( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `query` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `start_time` | `str` | Beginning timestamp for the requested provider interval. |
| `end_time` | `str` | Ending timestamp for the requested provider interval. |
| `coordinate_systems` | `str` | Coordinate system or comma-separated coordinate systems requested from the satellite service. |
| `resolution_factor` | `int` | Sampling resolution factor applied to returned satellite location data. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_nearby_objects`

Retrieve JPL SSD and CNEOS near-Earth object data.

### Signature

```python
def fetch_nearby_objects( mode: str='close_approaches', start_date: str='', end_date: str='', query: str='', query_type: str='sstr', dist_max: str='10LD', body: str='Earth', sort: str='date', limit: int=20, dv: float=6.0, dur: int=360, stay: int=8, launch: str='2020-2045', h: float=26.0, occ: int=7, include_physical: bool=True, include_close_approaches: bool=True, ca_body: str='Earth', include_discovery: bool=True, time: int=20 ) -> Any
```

### Purpose

Retrieve JPL SSD and CNEOS near-Earth object data through NASA/JPL near-Earth object services. The query text determines the records or documents matched by the provider. Date and time arguments constrain the requested interval when supplied. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_nearby_objects

result = fetch_nearby_objects( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `start_date` | `str` | Inclusive start date for the requested time range, in the provider-supported format. |
| `end_date` | `str` | Inclusive end date for the requested time range, in the provider-supported format. |
| `query` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `query_type` | `str` | Provider type selector for query. |
| `dist_max` | `str` | Maximum close-approach distance expression accepted by the JPL service. |
| `body` | `str` | Solar-system body used as the reference object. |
| `sort` | `str` | Provider-supported result ordering expression. |
| `limit` | `int` | Maximum number of records or items to return. |
| `dv` | `float` | Delta-v threshold or mission constraint used by the near-Earth object query. |
| `dur` | `int` | Mission duration constraint, in days, used by the near-Earth object query. |
| `stay` | `int` | Target stay-duration constraint, in days, used by the near-Earth object query. |
| `launch` | `str` | Launch-year or launch-window expression used by the near-Earth object query. |
| `h` | `float` | Absolute-magnitude threshold used by the near-Earth object query. |
| `occ` | `int` | Opportunity-count or occurrence constraint used by the mission query. |
| `include_physical` | `bool` | Whether to include physical in the result. |
| `include_close_approaches` | `bool` | Whether to include close approaches in the result. |
| `ca_body` | `str` | Reference body used for close-approach data. |
| `include_discovery` | `bool` | Whether to include discovery in the result. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_open_science`

Retrieve NASA Open Science Data Repository resources.

### Signature

```python
def fetch_open_science( mode: str='dataset', query: str='', accession: str='', format_value: str='json', time: int=20 ) -> Any
```

### Purpose

Retrieve NASA Open Science Data Repository resources through NASA Open Science Data Repository. The query text determines the records or documents matched by the provider.

### Example

```python
from fonky.gemini.tools import fetch_open_science

result = fetch_open_science( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `query` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `accession` | `str` | Dataset accession identifier used to retrieve a specific Open Science resource. |
| `format_value` | `str` | Provider output format. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_space_weather`

Retrieve NASA DONKI space weather endpoints.

### Signature

```python
def fetch_space_weather( mode: str='cme', start_date: str='', end_date: str='', time: int=20, location: str='ALL', catalog: str='ALL', notification_type: str='all', most_accurate_only: bool=True, complete_entry_only: bool=True, speed: int=0, half_angle: int=0, keyword: str='', api_key: str | None=None ) -> Any
```

### Purpose

Retrieve NASA DONKI space weather endpoints through NASA DONKI. Date and time arguments constrain the requested interval when supplied. When supplied, ``api_key`` overrides the configured provider credential for this request.

### Example

```python
from fonky.gemini.tools import fetch_space_weather

result = fetch_space_weather( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `start_date` | `str` | Inclusive start date for the requested time range, in the provider-supported format. |
| `end_date` | `str` | Inclusive end date for the requested time range, in the provider-supported format. |
| `time` | `int` | Request timeout in seconds. |
| `location` | `str` | Place name, address, or location description resolved by the provider. |
| `catalog` | `str` | Provider catalog filter. |
| `notification_type` | `str` | Provider type selector for notification. |
| `most_accurate_only` | `bool` | Whether to restrict results to the provider-designated most accurate analyses. |
| `complete_entry_only` | `bool` | Whether to restrict results to complete provider entries. |
| `speed` | `int` | Minimum or target speed constraint used by the space-weather query. |
| `half_angle` | `int` | Half-angle constraint used by the space-weather query. |
| `keyword` | `str` | Keyword used to filter provider records. |
| `api_key` | `str | None` | Optional credential override used for the active request. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_astro_catalog`

Retrieve Open Astronomy Catalog queries.

### Signature

```python
def fetch_astro_catalog( mode: str='object_query', query: str='', quantity: str='', attributes: str='', arguments: str='', ra: str='', dec: str='', radius: int=2, data_format: str='json', time: int=20 ) -> Any
```

### Purpose

Retrieve Open Astronomy Catalog queries through Open Astronomy Catalog. The query text determines the records or documents matched by the provider.

### Example

```python
from fonky.gemini.tools import fetch_astro_catalog

result = fetch_astro_catalog( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `query` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `quantity` | `str` | Provider quantity or field requested from the catalog. |
| `attributes` | `str` | Provider attributes requested for matching catalog records. |
| `arguments` | `str` | Keyword arguments passed to the bound callable. |
| `ra` | `str` | Right ascension value. |
| `dec` | `str` | Declination value. |
| `radius` | `int` | Search radius in the units specified by the operation. |
| `data_format` | `str` | Provider output data format. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Provider-specific structured data produced by the retrieval operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_astro_query`

Retrieve Simbad and astronomy object search operations.

### Signature

```python
def fetch_astro_query( mode: str='object_search', query: str='', ra: str='', dec: str='', radius: float=0.5, radius_unit: str='deg', row_limit: int=100 ) -> Any
```

### Purpose

Retrieve Simbad and astronomy object search operations through Astroquery/SIMBAD. The query text determines the records or documents matched by the provider. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_astro_query

result = fetch_astro_query( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `query` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `ra` | `str` | Right ascension value. |
| `dec` | `str` | Declination value. |
| `radius` | `float` | Search radius in the units specified by the operation. |
| `radius_unit` | `str` | Unit applied to the search radius. |
| `row_limit` | `int` | Maximum number of rows returned by the astronomy query. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_star_map`

Retrieve astronomical object map links and imagery.

### Signature

```python
def fetch_star_map( mode: str='object_link', query: str='', ra: float=0.0, dec: float=0.0, zoom: int=5, image_source: str='DSS2', box_color: str='yellow', show_box: bool=True, show_grid: bool=True, show_lines: bool=True, show_boundaries: bool=True, show_const_names: bool=False, time: int=20 ) -> Any
```

### Purpose

Retrieve astronomical object map links and imagery through astronomical map service. The query text determines the records or documents matched by the provider.

### Example

```python
from fonky.gemini.tools import fetch_star_map

result = fetch_star_map( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `query` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `ra` | `float` | Right ascension value. |
| `dec` | `float` | Declination value. |
| `zoom` | `int` | Map or chart zoom level. |
| `image_source` | `str` | Imagery or survey source used to render the map or chart. |
| `box_color` | `str` | Color used to draw the target box on generated map or chart output. |
| `show_box` | `bool` | Whether to display box in generated output. |
| `show_grid` | `bool` | Whether to display grid in generated output. |
| `show_lines` | `bool` | Whether to display lines in generated output. |
| `show_boundaries` | `bool` | Whether to display boundaries in generated output. |
| `show_const_names` | `bool` | Whether to display const names in generated output. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_star_chart`

Retrieve static star chart and coordinate chart generation.

### Signature

```python
def fetch_star_chart( mode: str='object_chart', query: str='', ra: float=0.0, dec: float=0.0, zoom: int=5, image_source: str='DSS2', box_color: str='yellow', show_box: bool=True, show_grid: bool=True, show_lines: bool=True, show_boundaries: bool=True, show_const_names: bool=False, width: int=900, height: int=450, magnitude: float=7.5, time: int=20 ) -> Any
```

### Purpose

Retrieve static star chart and coordinate chart generation through astronomical chart service. The query text determines the records or documents matched by the provider.

### Example

```python
from fonky.gemini.tools import fetch_star_chart

result = fetch_star_chart( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `query` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `ra` | `float` | Right ascension value. |
| `dec` | `float` | Declination value. |
| `zoom` | `int` | Map or chart zoom level. |
| `image_source` | `str` | Imagery or survey source used to render the map or chart. |
| `box_color` | `str` | Color used to draw the target box on generated map or chart output. |
| `show_box` | `bool` | Whether to display box in generated output. |
| `show_grid` | `bool` | Whether to display grid in generated output. |
| `show_lines` | `bool` | Whether to display lines in generated output. |
| `show_boundaries` | `bool` | Whether to display boundaries in generated output. |
| `show_const_names` | `bool` | Whether to display const names in generated output. |
| `width` | `int` | Output image or chart width in pixels. |
| `height` | `int` | Output image or chart height in pixels. |
| `magnitude` | `float` | Limiting stellar magnitude used when rendering a chart. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_open_sky`

Retrieve OpenSky Network aircraft, airport, and state-vector data.

### Signature

```python
def fetch_open_sky( mode: str='states_bbox', icao24: str='', airport: str='', begin: int | None=None, end: int | None=None, time_value: int | None=None, lamin: float | None=None, lomin: float | None=None, lamax: float | None=None, lomax: float | None=None, extended: bool=False, client_id: str=None, client_secret: str=None, time: int=20 ) -> Any
```

### Purpose

Retrieve OpenSky Network aircraft, airport, and state-vector data through OpenSky Network. Use ``mode`` to select among ``arrivals_airport``, ``departures_airport``, ``flights_aircraft``, ``states_bbox``, ``track_aircraft``.

### Example

```python
from fonky.gemini.tools import fetch_open_sky

result = fetch_open_sky( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``arrivals_airport``, ``departures_airport``, ``flights_aircraft``, ``states_bbox``, ``track_aircraft``. |
| `icao24` | `str` | 24-bit ICAO aircraft transponder address. |
| `airport` | `str` | ICAO airport identifier used to query arrivals or departures. |
| `begin` | `int | None` | Beginning Unix timestamp for the requested aviation interval. |
| `end` | `int | None` | Ending Unix timestamp for the requested aviation interval. |
| `time_value` | `int | None` | Clock time or timestamp used by the selected provider operation. |
| `lamin` | `float | None` | Bounding-box minimum latitude in decimal degrees. |
| `lomin` | `float | None` | Bounding-box minimum longitude in decimal degrees. |
| `lamax` | `float | None` | Bounding-box maximum latitude in decimal degrees. |
| `lomax` | `float | None` | Bounding-box maximum longitude in decimal degrees. |
| `extended` | `bool` | Whether extended OpenSky state-vector fields should be requested. |
| `client_id` | `str` | Optional credential override used for the active request. |
| `client_secret` | `str` | Optional credential override used for the active request. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---
