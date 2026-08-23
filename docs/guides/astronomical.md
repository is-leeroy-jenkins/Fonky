# Astronomical

Astronomy catalogs, satellites, near-Earth objects, Open Science, space weather, star maps/charts, and OpenSky.

## Functional Operations

| Function | Signature | Purpose |
|---|---|---|
| `fetch_naval_observatory()` | `fetch_naval_observatory( mode: str = 'celnav', date_value: str = '', time_value: str = '', latitude: float = 0.0, longitude: float = 0.0, location_label: str = '', time: int = 20 ) -> Any` | Fetch U.S. Naval Observatory celestial-navigation data. Provides direct module-level access to ``NavalObservatory.fetch`` using a fresh ``NavalObservatory`` instance. Any: Value returned by ``NavalObservatory.fetch``. |
| `fetch_satellite_center()` | `fetch_satellite_center( mode: str = 'observatories', query: str = '', start_time: str = '', end_time: str = '', coordinate_systems: str = 'gse', resolution_factor: int = 1, time: int = 20 ) -> Any` | Fetch SSC satellite observatory, ground-station, and location data. Provides direct module-level access to ``SatelliteCenter.fetch`` using a fresh ``SatelliteCenter`` instance. Any: Value returned by ``SatelliteCenter.fetch``. |
| `fetch_nearby_objects()` | `fetch_nearby_objects( mode: str = 'close_approaches', start_date: str = '', end_date: str = '', query: str = '', query_type: str = 'sstr', dist_max: str = '10LD', body: str = 'Earth', sort: str = 'date', limit: int = 20, dv: float = 6.0, dur: int = 360, stay: int = 8, launch: str = '2020-2045', h: float = 26.0, occ: int = 7, include_physical: bool = True, include_close_approaches: bool = True, ca_body: str = 'Earth', include_discovery: bool = True, time: int = 20 ) -> Any` | Fetch JPL SSD and CNEOS near-Earth object data. Provides direct module-level access to ``NearbyObjects.fetch`` using a fresh ``NearbyObjects`` instance. Any: Value returned by ``NearbyObjects.fetch``. |
| `fetch_open_science()` | `fetch_open_science( mode: str = 'dataset', query: str = '', accession: str = '', format_value: str = 'json', time: int = 20 ) -> Any` | Fetch NASA Open Science Data Repository resources. Provides direct module-level access to ``OpenScience.fetch`` using a fresh ``OpenScience`` instance. Any: Value returned by ``OpenScience.fetch``. |
| `fetch_space_weather()` | `fetch_space_weather( mode: str = 'cme', start_date: str = '', end_date: str = '', time: int = 20, location: str = 'ALL', catalog: str = 'ALL', notification_type: str = 'all', most_accurate_only: bool = True, complete_entry_only: bool = True, speed: int = 0, half_angle: int = 0, keyword: str = '', api_key: str = None ) -> Any` | Fetch NASA DONKI space weather endpoints. Provides direct module-level access to ``SpaceWeather.fetch`` using a fresh ``SpaceWeather`` instance. Any: Value returned by ``SpaceWeather.fetch``. |
| `fetch_astro_catalog()` | `fetch_astro_catalog( mode: str = 'object_query', query: str = '', quantity: str = '', attributes: str = '', arguments: str = '', ra: str = '', dec: str = '', radius: int = 2, data_format: str = 'json', time: int = 20 ) -> Any` | Fetch Open Astronomy Catalog queries. Provides direct module-level access to ``AstroCatalog.fetch`` using a fresh ``AstroCatalog`` instance. Any: Value returned by ``AstroCatalog.fetch``. |
| `fetch_astro_query()` | `fetch_astro_query( mode: str = 'object_search', query: str = '', ra: str = '', dec: str = '', radius: float = 0.5, radius_unit: str = 'deg', row_limit: int = 100 ) -> Any` | Fetch Simbad and astronomy object search operations. Provides direct module-level access to ``AstroQuery.fetch`` using a fresh ``AstroQuery`` instance. Any: Value returned by ``AstroQuery.fetch``. |
| `fetch_star_map()` | `fetch_star_map( mode: str = 'object_link', query: str = '', ra: float = 0.0, dec: float = 0.0, zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, time: int = 20 ) -> Any` | Fetch astronomical object map links and imagery. Provides direct module-level access to ``StarMap.fetch`` using a fresh ``StarMap`` instance. Any: Value returned by ``StarMap.fetch``. |
| `fetch_star_chart()` | `fetch_star_chart( mode: str = 'object_chart', query: str = '', ra: float = 0.0, dec: float = 0.0, zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, width: int = 900, height: int = 450, magnitude: float = 7.5, time: int = 20 ) -> Any` | Fetch static star chart and coordinate chart generation. Provides direct module-level access to ``StarChart.fetch`` using a fresh ``StarChart`` instance. Any: Value returned by ``StarChart.fetch``. |
| `fetch_open_sky()` | `fetch_open_sky( mode: str = 'states_bbox', icao24: str = '', airport: str = '', begin: int = None, end: int = None, time_value: int = None, lamin: float \| None = None, lomin: float \| None = None, lamax: float \| None = None, lomax: float \| None = None, extended: bool = False, client_id: str = None, client_secret: str = None, time: int = 20 ) -> Any` | Fetch OpenSky Network aircraft, airport, and state-vector data. Provides direct module-level access to ``OpenSky.fetch`` using a fresh ``OpenSky`` instance. Any: Value returned by ``OpenSky.fetch``. |

## How to choose

Use the functional wrapper when one call completes the task. Use the implementation class when you need retained state, helper methods, or direct provider debugging.

## Operational considerations

- Remote providers require network access.
- Rate limits, timeouts, service availability, and response-shape changes remain operational concerns.
- Provider-specific argument validation is enforced by the implementation class.

## Representative Functions

### `fetch_naval_observatory()`

```python
# fetch_naval_observatory( mode: str = 'celnav', date_value: str = '', time_value: str = '', latitude: float = 0.0, longitude: float = 0.0, location_label: str = '', time: int = 20 ) -> Any
```

Fetch U.S. Naval Observatory celestial-navigation data. Provides direct module-level access to ``NavalObservatory.fetch`` using a fresh ``NavalObservatory`` instance. Any: Value returned by ``NavalObservatory.fetch``.

### `fetch_satellite_center()`

```python
# fetch_satellite_center( mode: str = 'observatories', query: str = '', start_time: str = '', end_time: str = '', coordinate_systems: str = 'gse', resolution_factor: int = 1, time: int = 20 ) -> Any
```

Fetch SSC satellite observatory, ground-station, and location data. Provides direct module-level access to ``SatelliteCenter.fetch`` using a fresh ``SatelliteCenter`` instance. Any: Value returned by ``SatelliteCenter.fetch``.

### `fetch_nearby_objects()`

```python
# fetch_nearby_objects( mode: str = 'close_approaches', start_date: str = '', end_date: str = '', query: str = '', query_type: str = 'sstr', dist_max: str = '10LD', body: str = 'Earth', sort: str = 'date', limit: int = 20, dv: float = 6.0, dur: int = 360, stay: int = 8, launch: str = '2020-2045', h: float = 26.0, occ: int = 7, include_physical: bool = True, include_close_approaches: bool = True, ca_body: str = 'Earth', include_discovery: bool = True, time: int = 20 ) -> Any
```

Fetch JPL SSD and CNEOS near-Earth object data. Provides direct module-level access to ``NearbyObjects.fetch`` using a fresh ``NearbyObjects`` instance. Any: Value returned by ``NearbyObjects.fetch``.

### `fetch_open_science()`

```python
# fetch_open_science( mode: str = 'dataset', query: str = '', accession: str = '', format_value: str = 'json', time: int = 20 ) -> Any
```

Fetch NASA Open Science Data Repository resources. Provides direct module-level access to ``OpenScience.fetch`` using a fresh ``OpenScience`` instance. Any: Value returned by ``OpenScience.fetch``.

### `fetch_space_weather()`

```python
# fetch_space_weather( mode: str = 'cme', start_date: str = '', end_date: str = '', time: int = 20, location: str = 'ALL', catalog: str = 'ALL', notification_type: str = 'all', most_accurate_only: bool = True, complete_entry_only: bool = True, speed: int = 0, half_angle: int = 0, keyword: str = '', api_key: str = None ) -> Any
```

Fetch NASA DONKI space weather endpoints. Provides direct module-level access to ``SpaceWeather.fetch`` using a fresh ``SpaceWeather`` instance. Any: Value returned by ``SpaceWeather.fetch``.

### `fetch_astro_catalog()`

```python
# fetch_astro_catalog( mode: str = 'object_query', query: str = '', quantity: str = '', attributes: str = '', arguments: str = '', ra: str = '', dec: str = '', radius: int = 2, data_format: str = 'json', time: int = 20 ) -> Any
```

Fetch Open Astronomy Catalog queries. Provides direct module-level access to ``AstroCatalog.fetch`` using a fresh ``AstroCatalog`` instance. Any: Value returned by ``AstroCatalog.fetch``.

### `fetch_astro_query()`

```python
# fetch_astro_query( mode: str = 'object_search', query: str = '', ra: str = '', dec: str = '', radius: float = 0.5, radius_unit: str = 'deg', row_limit: int = 100 ) -> Any
```

Fetch Simbad and astronomy object search operations. Provides direct module-level access to ``AstroQuery.fetch`` using a fresh ``AstroQuery`` instance. Any: Value returned by ``AstroQuery.fetch``.

### `fetch_star_map()`

```python
# fetch_star_map( mode: str = 'object_link', query: str = '', ra: float = 0.0, dec: float = 0.0, zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, time: int = 20 ) -> Any
```

Fetch astronomical object map links and imagery. Provides direct module-level access to ``StarMap.fetch`` using a fresh ``StarMap`` instance. Any: Value returned by ``StarMap.fetch``.


See [Functional API](../api/fonky.md) for all signatures.
