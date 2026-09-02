# Demographics & Public Data

**Tools:** 5

Examples use the Google ADK callable wrapper surface so each example is directly executable as ordinary Python.

## Tool Index

| Tool |
|---|
| [`fetch_census_data`](#fetch_census_data) |
| [`fetch_socrata`](#fetch_socrata) |
| [`fetch_united_nations`](#fetch_united_nations) |
| [`fetch_world_population`](#fetch_world_population) |
| [`load_open_city`](#load_open_city) |

---

## `fetch_census_data`

Retrieve U.S. Census dataset and variable.

### Signature

```python
def fetch_census_data( mode: str='variables', year: str='2022', dataset: str='acs/acs5', fields: str='NAME,B01001_001E', geography_for: str='state:*', geography_in: str='', predicates: str='', time: int=20 ) -> Any
```

### Purpose

Retrieve U.S. Census dataset and variable through U.S. Census API. Use ``mode`` to select among ``data``, ``variables``.

### Example

```python
from fonky.gemini.tools import fetch_census_data

result = fetch_census_data( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``data``, ``variables``. |
| `year` | `str` | Dataset or observation year requested from the provider. |
| `dataset` | `str` | Provider dataset name or identifier. |
| `fields` | `str` | Comma-separated or provider-specific field selection. |
| `geography_for` | `str` | Census ``for`` geography clause defining the requested geography. |
| `geography_in` | `str` | Optional Census ``in`` geography clause constraining the request. |
| `predicates` | `str` | Additional Census query predicates appended to the request. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_socrata`

Retrieve Socrata dataset metadata and row.

### Signature

```python
def fetch_socrata( mode: str='rows', domain: str='data.cdc.gov', dataset_id: str='', select: str='', where: str='', order: str='', group: str='', limit: int=25, offset: int=0, time: int=20 ) -> Any
```

### Purpose

Retrieve Socrata dataset metadata and row through Socrata. Use ``mode`` to select among ``metadata``, ``rows``. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_socrata

result = fetch_socrata( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``metadata``, ``rows``. |
| `domain` | `str` | Provider domain or host containing the requested dataset. |
| `dataset_id` | `str` | Provider dataset identifier. |
| `select` | `str` | Socrata ``$select`` expression defining returned columns or calculations. |
| `where` | `str` | Socrata ``$where`` filter expression. |
| `order` | `str` | Provider-supported result ordering expression. |
| `group` | `str` | Socrata ``$group`` expression used to aggregate rows. |
| `limit` | `int` | Maximum number of records or items to return. |
| `offset` | `int` | Zero-based result offset used for pagination. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_united_nations`

Retrieve United Nations SDMX dataset and query.

### Signature

```python
def fetch_united_nations( mode: str='datasets', query_path: str='', time: int=20 ) -> Any
```

### Purpose

Retrieve United Nations SDMX dataset and query through United Nations SDMX service. Use ``mode`` to select among ``datasets``, ``sdmx_query``.

### Example

```python
from fonky.gemini.tools import fetch_united_nations

result = fetch_united_nations( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``datasets``, ``sdmx_query``. |
| `query_path` | `str` | Path identifying the query resource. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_world_population`

Retrieve WorldPop catalog and raster metadata.

### Signature

```python
def fetch_world_population( mode: str='catalog', query: str='', asset_path: str='', page: int=1, page_size: int=25, time: int=20 ) -> Any
```

### Purpose

Retrieve WorldPop catalog and raster metadata through WorldPop. Use ``mode`` to select among ``catalog``, ``raster_metadata``, ``search``. The query text determines the records or documents matched by the provider. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_world_population

result = fetch_world_population( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``catalog``, ``raster_metadata``, ``search``. |
| `query` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `asset_path` | `str` | Path identifying the asset resource. |
| `page` | `int` | One-based result page to request. |
| `page_size` | `int` | Maximum number of records requested per page. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_open_city`

Load an Open City dataset.

### Signature

```python
def load_open_city( city_id: str, dataset_id: str, limit: int=100 ) -> Any
```

### Purpose

Load an Open City dataset using the Open City Data loader. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import load_open_city

result = load_open_city(
    city_id='washington-dc',
    dataset_id='example-dataset' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `city_id` | `str` | Provider identifier for the selected city. |
| `dataset_id` | `str` | Provider dataset identifier. |
| `limit` | `int` | Maximum number of records requested from the backing source. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

ValueError: Raised when a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---
