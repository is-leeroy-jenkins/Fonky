# Health & Science

**Tools:** 4

Examples use the Google ADK callable wrapper surface so each example is directly executable as ordinary Python.

## Tool Index

| Tool |
|---|
| [`fetch_health_data`](#fetch_health_data) |
| [`fetch_global_health_data`](#fetch_global_health_data) |
| [`fetch_wonder`](#fetch_wonder) |
| [`load_pubmed`](#load_pubmed) |

---

## `fetch_health_data`

Retrieve HealthData.gov Socrata metadata and rows.

### Signature

```python
def fetch_health_data( mode: str='rows', domain: str='healthdata.gov', dataset_id: str='', select: str='', where: str='', order: str='', group: str='', limit: int=25, offset: int=0, time: int=20 ) -> Any
```

### Purpose

Retrieve HealthData.gov Socrata metadata and rows through HealthData.gov. Use ``mode`` to select among ``metadata``, ``rows``. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_health_data

result = fetch_health_data( )

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

## `fetch_global_health_data`

Retrieve WHO global health indicator and Athena data.

### Signature

```python
def fetch_global_health_data( mode: str='indicator_registry', query_path: str='', fmt: str='json', time: int=20 ) -> Any
```

### Purpose

Retrieve WHO global health indicator and Athena data through WHO Global Health.

### Example

```python
from fonky.gemini.tools import fetch_global_health_data

result = fetch_global_health_data( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation mode used to select the backing workflow. |
| `query_path` | `str` | Query path value used by the operation. |
| `fmt` | `str` | Fmt value used by the operation. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `fetch_wonder`

Retrieve CDC WONDER template and query submission.

### Signature

```python
def fetch_wonder( mode: str='metadata_template', dataset_id: str='D76', request_xml: str='', time: int=20 ) -> Any
```

### Purpose

Retrieve CDC WONDER template and query submission through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import fetch_wonder

result = fetch_wonder( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation mode used to select the backing workflow. |
| `dataset_id` | `str` | Dataset id value used by the operation. |
| `request_xml` | `str` | Request xml value used by the operation. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `load_pubmed`

Load PubMed research documents.

### Signature

```python
def load_pubmed( query: str, max_docs: int=5 ) -> Any
```

### Purpose

Load PubMed research documents through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import load_pubmed

result = load_pubmed(
    query='federal spending' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `query` | `str` | Search query or natural-language request submitted to the backing operation. |
| `max_docs` | `int` | Max docs value used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---
