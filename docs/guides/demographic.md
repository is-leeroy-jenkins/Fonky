# Demographic

Census, Socrata, United Nations, population, and municipal/open-data retrieval.

## Functional Operations

| Function | Signature | Purpose |
|---|---|---|
| `fetch_census_data()` | `fetch_census_data( mode: str = 'variables', year: str = '2022', dataset: str = 'acs/acs5', fields: str = 'NAME,B01001_001E', geography_for: str = 'state:*', geography_in: str = '', predicates: str = '', time: int = 20 ) -> Any` | Fetch U.S. Census dataset and variable retrieval. Provides direct module-level access to ``CensusData.fetch`` using a fresh ``CensusData`` instance. Any: Value returned by ``CensusData.fetch``. |
| `fetch_socrata()` | `fetch_socrata( mode: str = 'rows', domain: str = 'data.cdc.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any` | Fetch Socrata dataset metadata and row retrieval. Provides direct module-level access to ``Socrata.fetch`` using a fresh ``Socrata`` instance. Any: Value returned by ``Socrata.fetch``. |
| `fetch_united_nations()` | `fetch_united_nations( mode: str = 'datasets', query_path: str = '', time: int = 20 ) -> Any` | Fetch United Nations SDMX dataset and query retrieval. Provides direct module-level access to ``UnitedNations.fetch`` using a fresh ``UnitedNations`` instance. Any: Value returned by ``UnitedNations.fetch``. |
| `fetch_world_population()` | `fetch_world_population( mode: str = 'catalog', query: str = '', asset_path: str = '', page: int = 1, page_size: int = 25, time: int = 20 ) -> Any` | Fetch WorldPop catalog and raster metadata retrieval. Provides direct module-level access to ``WorldPopulation.fetch`` using a fresh ``WorldPopulation`` instance. Any: Value returned by ``WorldPopulation.fetch``. |
| `load_open_city()` | `load_open_city( city_id: str, dataset_id: str, limit: int = 100 ) -> Any` | Load source content. Provides direct module-level access to ``OpenCityLoader.load`` using a fresh ``OpenCityLoader`` instance. Any: Value returned by ``OpenCityLoader.load``. |

## How to choose

Use the functional wrapper when one call completes the task. Use the implementation class when you need retained state, helper methods, or direct provider debugging.

## Operational considerations

- Remote providers require network access.
- Rate limits, timeouts, service availability, and response-shape changes remain operational concerns.
- Provider-specific argument validation is enforced by the implementation class.

## Representative Functions

### `fetch_census_data()`

```python
# fetch_census_data( mode: str = 'variables', year: str = '2022', dataset: str = 'acs/acs5', fields: str = 'NAME,B01001_001E', geography_for: str = 'state:*', geography_in: str = '', predicates: str = '', time: int = 20 ) -> Any
```

Fetch U.S. Census dataset and variable retrieval. Provides direct module-level access to ``CensusData.fetch`` using a fresh ``CensusData`` instance. Any: Value returned by ``CensusData.fetch``.

### `fetch_socrata()`

```python
# fetch_socrata( mode: str = 'rows', domain: str = 'data.cdc.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

Fetch Socrata dataset metadata and row retrieval. Provides direct module-level access to ``Socrata.fetch`` using a fresh ``Socrata`` instance. Any: Value returned by ``Socrata.fetch``.

### `fetch_united_nations()`

```python
# fetch_united_nations( mode: str = 'datasets', query_path: str = '', time: int = 20 ) -> Any
```

Fetch United Nations SDMX dataset and query retrieval. Provides direct module-level access to ``UnitedNations.fetch`` using a fresh ``UnitedNations`` instance. Any: Value returned by ``UnitedNations.fetch``.

### `fetch_world_population()`

```python
# fetch_world_population( mode: str = 'catalog', query: str = '', asset_path: str = '', page: int = 1, page_size: int = 25, time: int = 20 ) -> Any
```

Fetch WorldPop catalog and raster metadata retrieval. Provides direct module-level access to ``WorldPopulation.fetch`` using a fresh ``WorldPopulation`` instance. Any: Value returned by ``WorldPopulation.fetch``.

### `load_open_city()`

```python
# load_open_city( city_id: str, dataset_id: str, limit: int = 100 ) -> Any
```

Load source content. Provides direct module-level access to ``OpenCityLoader.load`` using a fresh ``OpenCityLoader`` instance. Any: Value returned by ``OpenCityLoader.load``.


See [Functional API](../api/fonky.md) for all signatures.
