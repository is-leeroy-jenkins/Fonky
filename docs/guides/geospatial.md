# Geospatial

Geocoding, reverse geocoding, address validation, directions, imagery, ScienceBase, National Map, and related spatial workflows.

## Functional Operations

| Function | Signature | Purpose |
|---|---|---|
| `geocode_location()` | `geocode_location( address: str ) -> Any` | Geocode location. Provides direct module-level access to ``GoogleMaps.geocode_location`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.geocode_location``. |
| `geocode_coordinates()` | `geocode_coordinates( lat: float, long: float ) -> Any` | Geocode coordinates. Provides direct module-level access to ``GoogleMaps.geocode_coordinates`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.geocode_coordinates``. |
| `validate_address()` | `validate_address( address: List[str] ) -> Any` | Validate address. Provides direct module-level access to ``GoogleMaps.validate_address`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.validate_address``. |
| `request_directions()` | `request_directions( origin: str, destination: str, mode: str = 'driving' ) -> Any` | Request directions. Provides direct module-level access to ``GoogleMaps.request_directions`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.request_directions``. |
| `fetch_global_imagery_wms_map()` | `fetch_global_imagery_wms_map( layer: str, image_date: str, bbox: Tuple[float, float, float, float], width: int = 1200, height: int = 600, projection: str = 'epsg4326', quality: str = 'best', image_format: str = 'image/png', transparent: bool = True, output_dir: str = 'python-examples', output_name: str = '', time: int = 20 ) -> Any` | Fetch wms map. Provides direct module-level access to ``GlobalImagery.fetch_wms_map`` using a fresh ``GlobalImagery`` instance. Any: Value returned by ``GlobalImagery.fetch_wms_map``. |
| `fetch_global_imagery_map_services()` | `fetch_global_imagery_map_services(  ) -> Any` | Fetch map services. Provides direct module-level access to ``GlobalImagery.fetch_map_services`` using a fresh ``GlobalImagery`` instance. None. Any: Value returned by ``GlobalImagery.fetch_map_services``. |
| `fetch_global_imagery_mercator_map()` | `fetch_global_imagery_mercator_map( ccrs: Any = None ) -> Any` | Fetch mercator map. Provides direct module-level access to ``GlobalImagery.fetch_mercator_map`` using a fresh ``GlobalImagery`` instance. Any: Value returned by ``GlobalImagery.fetch_mercator_map``. |
| `fetch_google_geocoding()` | `fetch_google_geocoding( mode: str = 'forward', query: str = '', latitude: float = 0.0, longitude: float = 0.0, place_id: str = '', language: str = 'en', region: str = '', result_type: str = '', location_type: str = '', time: int = 10, api_key: Optional[str] = None ) -> Any` | Fetch Google forward, reverse, and place geocoding. Provides direct module-level access to ``GoogleGeocoding.fetch`` using a fresh ``GoogleGeocoding`` instance. Any: Value returned by ``GoogleGeocoding.fetch``. |
| `fetch_usgs_national_map()` | `fetch_usgs_national_map( mode: str = 'products', dataset: str = '', q: str = '', bbox: str = '', prod_formats: str = '', max_items: int = 25, offset: int = 0, time: int = 20 ) -> Any` | Fetch USGS National Map datasets and products. Provides direct module-level access to ``USGSTheNationalMap.fetch`` using a fresh ``USGSTheNationalMap`` instance. Any: Value returned by ``USGSTheNationalMap.fetch``. |
| `fetch_usgs_sciencebase()` | `fetch_usgs_sciencebase( mode: str = 'items', q: str = '', item_id: str = '', max_items: int = 25, offset: int = 0, fields: str = '', time: int = 20 ) -> Any` | Fetch USGS ScienceBase items and catalog records. Provides direct module-level access to ``USGSScienceBase.fetch`` using a fresh ``USGSScienceBase`` instance. Any: Value returned by ``USGSScienceBase.fetch``. |

## How to choose

Use the functional wrapper when one call completes the task. Use the implementation class when you need retained state, helper methods, or direct provider debugging.

## Operational considerations

- Remote providers require network access.
- Rate limits, timeouts, service availability, and response-shape changes remain operational concerns.
- Provider-specific argument validation is enforced by the implementation class.

## Representative Functions

### `geocode_location()`

```python
# geocode_location( address: str ) -> Any
```

Geocode location. Provides direct module-level access to ``GoogleMaps.geocode_location`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.geocode_location``.

### `geocode_coordinates()`

```python
# geocode_coordinates( lat: float, long: float ) -> Any
```

Geocode coordinates. Provides direct module-level access to ``GoogleMaps.geocode_coordinates`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.geocode_coordinates``.

### `validate_address()`

```python
# validate_address( address: List[str] ) -> Any
```

Validate address. Provides direct module-level access to ``GoogleMaps.validate_address`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.validate_address``.

### `request_directions()`

```python
# request_directions( origin: str, destination: str, mode: str = 'driving' ) -> Any
```

Request directions. Provides direct module-level access to ``GoogleMaps.request_directions`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.request_directions``.

### `fetch_global_imagery_wms_map()`

```python
# fetch_global_imagery_wms_map( layer: str, image_date: str, bbox: Tuple[float, float, float, float], width: int = 1200, height: int = 600, projection: str = 'epsg4326', quality: str = 'best', image_format: str = 'image/png', transparent: bool = True, output_dir: str = 'python-examples', output_name: str = '', time: int = 20 ) -> Any
```

Fetch wms map. Provides direct module-level access to ``GlobalImagery.fetch_wms_map`` using a fresh ``GlobalImagery`` instance. Any: Value returned by ``GlobalImagery.fetch_wms_map``.

### `fetch_global_imagery_map_services()`

```python
# fetch_global_imagery_map_services(  ) -> Any
```

Fetch map services. Provides direct module-level access to ``GlobalImagery.fetch_map_services`` using a fresh ``GlobalImagery`` instance. None. Any: Value returned by ``GlobalImagery.fetch_map_services``.

### `fetch_global_imagery_mercator_map()`

```python
# fetch_global_imagery_mercator_map( ccrs: Any = None ) -> Any
```

Fetch mercator map. Provides direct module-level access to ``GlobalImagery.fetch_mercator_map`` using a fresh ``GlobalImagery`` instance. Any: Value returned by ``GlobalImagery.fetch_mercator_map``.

### `fetch_google_geocoding()`

```python
# fetch_google_geocoding( mode: str = 'forward', query: str = '', latitude: float = 0.0, longitude: float = 0.0, place_id: str = '', language: str = 'en', region: str = '', result_type: str = '', location_type: str = '', time: int = 10, api_key: Optional[str] = None ) -> Any
```

Fetch Google forward, reverse, and place geocoding. Provides direct module-level access to ``GoogleGeocoding.fetch`` using a fresh ``GoogleGeocoding`` instance. Any: Value returned by ``GoogleGeocoding.fetch``.


See [Functional API](../api/fonky.md) for all signatures.
