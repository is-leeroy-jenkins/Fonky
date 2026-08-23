# Health

HealthData, global health data, CDC WONDER, PubMed, and related public health retrieval.

## Functional Operations

| Function | Signature | Purpose |
|---|---|---|
| `fetch_health_data()` | `fetch_health_data( mode: str = 'rows', domain: str = 'healthdata.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any` | Fetch HealthData.gov Socrata metadata and rows. Provides direct module-level access to ``HealthData.fetch`` using a fresh ``HealthData`` instance. Any: Value returned by ``HealthData.fetch``. |
| `fetch_global_health_data()` | `fetch_global_health_data( mode: str = 'indicator_registry', query_path: str = '', fmt: str = 'json', time: int = 20 ) -> Any` | Fetch WHO global health indicator and Athena data. Provides direct module-level access to ``GlobalHealthData.fetch`` using a fresh ``GlobalHealthData`` instance. Any: Value returned by ``GlobalHealthData.fetch``. |
| `fetch_wonder()` | `fetch_wonder( mode: str = 'metadata_template', dataset_id: str = 'D76', request_xml: str = '', time: int = 20 ) -> Any` | Fetch CDC WONDER template and query submission. Provides direct module-level access to ``Wonder.fetch`` using a fresh ``Wonder`` instance. Any: Value returned by ``Wonder.fetch``. |
| `load_pubmed()` | `load_pubmed( query: str, max_docs: int = 5 ) -> Any` | Load source content. Provides direct module-level access to ``PubMedSearchLoader.load`` using a fresh ``PubMedSearchLoader`` instance. Any: Value returned by ``PubMedSearchLoader.load``. |

## How to choose

Use the functional wrapper when one call completes the task. Use the implementation class when you need retained state, helper methods, or direct provider debugging.

## Operational considerations

- Remote providers require network access.
- Rate limits, timeouts, service availability, and response-shape changes remain operational concerns.
- Provider-specific argument validation is enforced by the implementation class.

## Representative Functions

### `fetch_health_data()`

```python
# fetch_health_data( mode: str = 'rows', domain: str = 'healthdata.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

Fetch HealthData.gov Socrata metadata and rows. Provides direct module-level access to ``HealthData.fetch`` using a fresh ``HealthData`` instance. Any: Value returned by ``HealthData.fetch``.

### `fetch_global_health_data()`

```python
# fetch_global_health_data( mode: str = 'indicator_registry', query_path: str = '', fmt: str = 'json', time: int = 20 ) -> Any
```

Fetch WHO global health indicator and Athena data. Provides direct module-level access to ``GlobalHealthData.fetch`` using a fresh ``GlobalHealthData`` instance. Any: Value returned by ``GlobalHealthData.fetch``.

### `fetch_wonder()`

```python
# fetch_wonder( mode: str = 'metadata_template', dataset_id: str = 'D76', request_xml: str = '', time: int = 20 ) -> Any
```

Fetch CDC WONDER template and query submission. Provides direct module-level access to ``Wonder.fetch`` using a fresh ``Wonder`` instance. Any: Value returned by ``Wonder.fetch``.

### `load_pubmed()`

```python
# load_pubmed( query: str, max_docs: int = 5 ) -> Any
```

Load source content. Provides direct module-level access to ``PubMedSearchLoader.load`` using a fresh ``PubMedSearchLoader`` instance. Any: Value returned by ``PubMedSearchLoader.load``.


See [Functional API](../api/fonky.md) for all signatures.
