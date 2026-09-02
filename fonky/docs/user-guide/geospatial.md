# Geospatial

**Tools:** 10

Examples use the Google ADK callable wrapper surface so each example is directly executable as ordinary Python.

## Tool Index

| Tool |
|---|
| [`geocode_location`](#geocode_location) |
| [`geocode_coordinates`](#geocode_coordinates) |
| [`validate_address`](#validate_address) |
| [`request_directions`](#request_directions) |
| [`fetch_global_imagery_wms_map`](#fetch_global_imagery_wms_map) |
| [`fetch_global_imagery_map_services`](#fetch_global_imagery_map_services) |
| [`fetch_global_imagery_mercator_map`](#fetch_global_imagery_mercator_map) |
| [`fetch_google_geocoding`](#fetch_google_geocoding) |
| [`fetch_usgs_national_map`](#fetch_usgs_national_map) |
| [`fetch_usgs_sciencebase`](#fetch_usgs_sciencebase) |

---

## `geocode_location`

Geocode location.

### Signature

```python
def geocode_location( address: str ) -> Any
```

### Purpose

Geocode location using Google Maps.

### Example

```python
from fonky.gemini.tools import geocode_location

result = geocode_location(
    address='1600 Pennsylvania Avenue NW, Washington, DC' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `address` | `str` | Street address or place description used for geocoding, validation, or routing. |

### Returns

Any: Latitude and longitude coordinate pair.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `geocode_coordinates`

Geocode coordinates.

### Signature

```python
def geocode_coordinates( lat: float, long: float ) -> Any
```

### Purpose

Geocode coordinates using Google Maps. Coordinate and bounding arguments constrain geographic scope when supported.

### Example

```python
from fonky.gemini.tools import geocode_coordinates

result = geocode_coordinates(
    lat=38.8977,
    long=-77.0365 )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `lat` | `float` | Latitude in decimal degrees. |
| `long` | `float` | Longitude in decimal degrees. |

### Returns

Any: Text produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `validate_address`

Validate address.

### Signature

```python
def validate_address( address: List[str] ) -> Any
```

### Purpose

Validate address using Google Maps.

### Example

```python
from fonky.gemini.tools import validate_address

result = validate_address(
    address='1600 Pennsylvania Avenue NW, Washington, DC' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `address` | `List[str]` | Street address or place description used for geocoding, validation, or routing. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

TypeError: If a supplied value has an unsupported type. ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `request_directions`

Request directions.

### Signature

```python
def request_directions( origin: str, destination: str, mode: str='driving' ) -> Any
```

### Purpose

Request directions using Google Maps.

### Example

```python
from fonky.gemini.tools import request_directions

result = request_directions(
    origin='Washington, DC',
    destination='output/' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `origin` | `str` | Starting address or place for a routing request. |
| `destination` | `str` | Destination address or place for a routing request. |
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_global_imagery_wms_map`

Retrieve a WMS imagery map.

### Signature

```python
def fetch_global_imagery_wms_map( layer: str, image_date: str, bbox: Tuple[float, float, float, float], width: int=1200, height: int=600, projection: str='epsg4326', quality: str='best', image_format: str='image/png', transparent: bool=True, output_dir: str='python-examples', output_name: str='', time: int=20 ) -> Any
```

### Purpose

Retrieve a WMS imagery map through NASA Global Imagery Browse Services. Coordinate and bounding arguments constrain geographic scope when supported.

### Example

```python
from fonky.gemini.tools import fetch_global_imagery_wms_map

result = fetch_global_imagery_wms_map(
    layer='MODIS_Terra_CorrectedReflectance_TrueColor',
    image_date='2026-08-01',
    bbox='-77.2,38.7,-76.8,39.1' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `layer` | `str` | Map or imagery layer identifier. |
| `image_date` | `str` | Observation date used to select imagery. |
| `bbox` | `Tuple[float, float, float, float]` | Bounding box defining the geographic extent of the request. |
| `width` | `int` | Output image or chart width in pixels. |
| `height` | `int` | Output image or chart height in pixels. |
| `projection` | `str` | Coordinate reference system used for rendered imagery. |
| `quality` | `str` | Imagery quality level requested from the mapping service. |
| `image_format` | `str` | Output format requested for image. |
| `transparent` | `bool` | Whether the generated map image should use a transparent background. |
| `output_dir` | `str` | Local directory where generated imagery is written. |
| `output_name` | `str` | Optional filename for generated imagery. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_global_imagery_map_services`

Retrieve available imagery map services.

### Signature

```python
def fetch_global_imagery_map_services(  ) -> Any
```

### Purpose

Retrieve available imagery map services through NASA Global Imagery Browse Services.

### Example

```python
from fonky.gemini.tools import fetch_global_imagery_map_services

result = fetch_global_imagery_map_services( )

print( result )
```

### Returns

Any: Structured mapping produced by the operation.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_global_imagery_mercator_map`

Render a Mercator imagery map.

### Signature

```python
def fetch_global_imagery_mercator_map( ccrs: Any | None=None ) -> Any
```

### Purpose

Render a Mercator imagery map through NASA Global Imagery Browse Services.

### Example

```python
from fonky.gemini.tools import fetch_global_imagery_mercator_map

result = fetch_global_imagery_mercator_map( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `ccrs` | `Any | None` | Optional Cartopy coordinate reference system used to construct the map. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_google_geocoding`

Retrieve Google forward, reverse, and place geocoding.

### Signature

```python
def fetch_google_geocoding( mode: str='forward', query: str='', latitude: float=0.0, longitude: float=0.0, place_id: str='', language: str='en', region: str='', result_type: str='', location_type: str='', time: int=10, api_key: Optional[str]=None ) -> Any
```

### Purpose

Retrieve Google forward, reverse, and place geocoding through Google Geocoding. Use ``mode`` to select among ``forward``, ``place``, ``reverse``. The query text determines the records or documents matched by the provider. Coordinate and bounding arguments constrain geographic scope when supported. When supplied, ``api_key`` overrides the configured provider credential for this request.

### Example

```python
from fonky.gemini.tools import fetch_google_geocoding

result = fetch_google_geocoding( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``forward``, ``place``, ``reverse``. |
| `query` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `latitude` | `float` | Latitude in decimal degrees. |
| `longitude` | `float` | Longitude in decimal degrees. |
| `place_id` | `str` | Provider identifier for the selected place. |
| `language` | `str` | Language code used for provider results or parsing. |
| `region` | `str` | Provider region filter or regional bias value. |
| `result_type` | `str` | Provider type selector for result. |
| `location_type` | `str` | Provider type selector for location. |
| `time` | `int` | Request timeout in seconds. |
| `api_key` | `Optional[str]` | Optional credential override used for the active request. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_usgs_national_map`

Retrieve USGS National Map datasets and products.

### Signature

```python
def fetch_usgs_national_map( mode: str='products', dataset: str='', q: str='', bbox: str='', prod_formats: str='', max_items: int=25, offset: int=0, time: int=20 ) -> Any
```

### Purpose

Retrieve USGS National Map datasets and products through USGS The National Map. Use ``mode`` to select among ``datasets``, ``products``. The query text determines the records or documents matched by the provider. Coordinate and bounding arguments constrain geographic scope when supported. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_usgs_national_map

result = fetch_usgs_national_map( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``datasets``, ``products``. |
| `dataset` | `str` | Provider dataset name or identifier. |
| `q` | `str` | Free-text provider query used to search matching records. |
| `bbox` | `str` | Bounding box defining the geographic extent of the request. |
| `prod_formats` | `str` | Product-format filter applied to National Map results. |
| `max_items` | `int` | Maximum number of records or items to return. |
| `offset` | `int` | Zero-based result offset used for pagination. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_usgs_sciencebase`

Retrieve USGS ScienceBase items and catalog records.

### Signature

```python
def fetch_usgs_sciencebase( mode: str='items', q: str='', item_id: str='', max_items: int=25, offset: int=0, fields: str='', time: int=20 ) -> Any
```

### Purpose

Retrieve USGS ScienceBase items and catalog records through USGS ScienceBase. Use ``mode`` to select among ``item``, ``items``. The query text determines the records or documents matched by the provider. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_usgs_sciencebase

result = fetch_usgs_sciencebase( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``item``, ``items``. |
| `q` | `str` | Free-text provider query used to search matching records. |
| `item_id` | `str` | Provider identifier for the selected item. |
| `max_items` | `int` | Maximum number of records or items to return. |
| `offset` | `int` | Zero-based result offset used for pagination. |
| `fields` | `str` | Comma-separated or provider-specific field selection. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---
