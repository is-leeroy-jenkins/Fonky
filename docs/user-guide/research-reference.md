# Research & Reference

**Tools:** 11

Examples use the Google ADK callable wrapper surface so each example is directly executable as ordinary Python.

## Tool Index

| Tool |
|---|
| [`fetch_arxiv`](#fetch_arxiv) |
| [`fetch_google_drive`](#fetch_google_drive) |
| [`fetch_wikipedia`](#fetch_wikipedia) |
| [`fetch_news`](#fetch_news) |
| [`fetch_cse_search`](#fetch_cse_search) |
| [`fetch_gov_data`](#fetch_gov_data) |
| [`fetch_congress`](#fetch_congress) |
| [`fetch_internet_archive`](#fetch_internet_archive) |
| [`fetch_grokipedia`](#fetch_grokipedia) |
| [`load_arxiv`](#load_arxiv) |
| [`load_wikipedia`](#load_wikipedia) |

---

## `fetch_arxiv`

Retrieve ArXiv research documents.

### Signature

```python
def fetch_arxiv( question: str, max_documents: int | None=None, full_documents: bool | None=None, include_metadata: bool | None=None ) -> Any
```

### Purpose

Retrieve ArXiv research documents through ArXiv. The query text determines the records or documents matched by the provider. Result-count arguments bound the amount of data requested. Boolean options control retrieval depth or supplemental content.

### Example

```python
from fonky.gemini.tools import fetch_arxiv

result = fetch_arxiv(
    question='retrieval augmented generation' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `question` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `max_documents` | `int | None` | Maximum number of documents to retrieve. |
| `full_documents` | `bool | None` | Whether to retrieve full document content instead of abbreviated search results. |
| `include_metadata` | `bool | None` | Whether provider metadata should be included with retrieved content. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_google_drive`

Retrieve Google Drive documents.

### Signature

```python
def fetch_google_drive( question: str, folder_id: str='root', results: int=10, template: str='gdrive-query', mime_type: str | None=None, mode: str='documents' ) -> Any
```

### Purpose

Retrieve Google Drive documents through Google Drive. The query text determines the records or documents matched by the provider. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_google_drive

result = fetch_google_drive(
    question='retrieval augmented generation' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `question` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `folder_id` | `str` | Provider folder identifier that scopes the operation. |
| `results` | `int` | Maximum number of search results to request. |
| `template` | `str` | Provider query template used to construct the request. |
| `mime_type` | `str | None` | Optional MIME type used to restrict matching files. |
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_wikipedia`

Retrieve Wikipedia documents.

### Signature

```python
def fetch_wikipedia( question: str, language: str | None=None, max_documents: int | None=None, include_metadata: bool | None=None ) -> Any
```

### Purpose

Retrieve Wikipedia documents through Wikipedia. The query text determines the records or documents matched by the provider. Result-count arguments bound the amount of data requested. Boolean options control retrieval depth or supplemental content.

### Example

```python
from fonky.gemini.tools import fetch_wikipedia

result = fetch_wikipedia(
    question='retrieval augmented generation' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `question` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `language` | `str | None` | Language code used for provider results or parsing. |
| `max_documents` | `int | None` | Maximum number of documents to retrieve. |
| `include_metadata` | `bool | None` | Whether provider metadata should be included with retrieved content. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_news`

Retrieve The News API article.

### Signature

```python
def fetch_news( endpoint: str='all', query: str='', language: str='en', categories: str='', exclude_categories: str='', locale: str='', domains: str='', exclude_domains: str='', source_ids: str='', exclude_source_ids: str='', published_after: str='', published_before: str='', published_on: str='', sort: str='published_at', limit: int=10, page: int=1, include_similar: bool=True, headlines_per_category: int=6, time: int=10, api_key: str | None=None ) -> Any
```

### Purpose

Retrieve The News API article through The News API. The query text determines the records or documents matched by the provider. Date and time arguments constrain the requested interval when supplied. Result-count arguments bound the amount of data requested. Boolean options control retrieval depth or supplemental content. When supplied, ``api_key`` overrides the configured provider credential for this request.

### Example

```python
from fonky.gemini.tools import fetch_news

result = fetch_news( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `endpoint` | `str` | Provider endpoint or endpoint family to request. |
| `query` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `language` | `str` | Language code used for provider results or parsing. |
| `categories` | `str` | Comma-separated news categories used to include matching articles. |
| `exclude_categories` | `str` | Filter value used to exclude categories from provider results. |
| `locale` | `str` | Locale filter applied to news results. |
| `domains` | `str` | Comma-separated source domains used to include matching news articles. |
| `exclude_domains` | `str` | Filter value used to exclude domains from provider results. |
| `source_ids` | `str` | Provider identifiers for the selected source. |
| `exclude_source_ids` | `str` | Filter value used to exclude source ids from provider results. |
| `published_after` | `str` | Earliest publication timestamp accepted by the news query. |
| `published_before` | `str` | Latest publication timestamp accepted by the news query. |
| `published_on` | `str` | Specific publication date used to restrict news results. |
| `sort` | `str` | Provider-supported result ordering expression. |
| `limit` | `int` | Maximum number of records or items to return. |
| `page` | `int` | One-based result page to request. |
| `include_similar` | `bool` | Whether to include similar in the result. |
| `headlines_per_category` | `int` | Maximum number of headlines returned for each category in headline mode. |
| `time` | `int` | Request timeout in seconds. |
| `api_key` | `str | None` | Optional credential override used for the active request. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_cse_search`

Retrieve Google Programmable Search Engine results.

### Signature

```python
def fetch_cse_search( keywords: str, results: int=10, start: int=1, exact_terms: str='', exclude_terms: str='', file_type: str='', date_restrict: str='', gl: str='', lr: str='', safe: str='off', search_type: str='', site_search: str='', site_search_filter: str='', sort: str='', img_size: str='', img_type: str='', img_color_type: str='', img_dominant_color: str='', time: int=10, api_key: str | None=None, cse_id: str | None=None ) -> Any
```

### Purpose

Retrieve results through Google Programmable Search Engine (Custom Search JSON API). The query text determines the records or documents matched by the provider. Result-count arguments bound the amount of data requested. When supplied, ``api_key`` overrides the configured provider credential for this request.

### Example

```python
from fonky.gemini.tools import fetch_cse_search

result = fetch_cse_search(
    keywords='retrieval augmented generation' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `keywords` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `results` | `int` | Maximum number of search results to request. |
| `start` | `int` | Starting result position used for pagination. |
| `exact_terms` | `str` | Phrase that must appear exactly in Google Custom Search results. |
| `exclude_terms` | `str` | Terms that must not appear in Google Custom Search results. |
| `file_type` | `str` | File-extension filter applied to Google Custom Search results. |
| `date_restrict` | `str` | Google Custom Search date restriction expression. |
| `gl` | `str` | Google country-code boost applied to search results. |
| `lr` | `str` | Google language restriction expression. |
| `safe` | `str` | Google SafeSearch setting. |
| `search_type` | `str` | Google Custom Search result type; use the provider-supported image-search value when requesting images. |
| `site_search` | `str` | Domain or site used to restrict Google Custom Search results. |
| `site_search_filter` | `str` | Whether ``site_search`` is included or excluded by Google Custom Search. |
| `sort` | `str` | Provider-supported result ordering expression. |
| `img_size` | `str` | Image-size filter used for Google image search. |
| `img_type` | `str` | Google image type filter. |
| `img_color_type` | `str` | Google image color-type filter. |
| `img_dominant_color` | `str` | Dominant-color filter used for Google image search. |
| `time` | `int` | Request timeout in seconds. |
| `api_key` | `str | None` | Optional credential override used for the active request. |
| `cse_id` | `str | None` | Google Programmable Search Engine identifier. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_gov_data`

Retrieve Data.gov package and collection.

### Signature

```python
def fetch_gov_data( mode: str='search', query: str='', page_size: int=10, offset_mark: str='*', sort_field: str='score', sort_order: str='DESC', package_id: str='', collection: str='', start_date: str='', time: int=20 ) -> Any
```

### Purpose

Retrieve Data.gov package and collection through Data.gov. Use ``mode`` to select among ``collection``, ``package_summary``, ``search``. The query text determines the records or documents matched by the provider. Date and time arguments constrain the requested interval when supplied. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_gov_data

result = fetch_gov_data( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``collection``, ``package_summary``, ``search``. |
| `query` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `page_size` | `int` | Maximum number of records requested per page. |
| `offset_mark` | `str` | Provider continuation marker used for paginated Data.gov search results. |
| `sort_field` | `str` | Provider field used to order search results. |
| `sort_order` | `str` | Sort direction applied to the provider search. |
| `package_id` | `str` | Provider identifier for the selected package. |
| `collection` | `str` | Provider collection identifier used to restrict results. |
| `start_date` | `str` | Inclusive start date for the requested time range, in the provider-supported format. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_congress`

Retrieve Congress.gov legislative data.

### Signature

```python
def fetch_congress( mode: str='congresses', congress: int=0, bill_type: str='', bill_number: int=0, law_type: str='', law_number: int=0, report_type: str='', report_number: int=0, offset: int=0, limit: int=20, sort: str='updateDate+desc', from_date_time: str='', to_date_time: str='', conference: bool=False, time: int=20 ) -> Any
```

### Purpose

Retrieve Congress.gov legislative data through Congress.gov. Use ``mode`` to select among ``bill_detail``, ``bills``, ``congresses``, ``law_detail``, ``laws``, ``report_detail``, ``reports``. Date and time arguments constrain the requested interval when supplied. Result- count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_congress

result = fetch_congress( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation selector. Supported values detected in the implementation include ``bill_detail``, ``bills``, ``congresses``, ``law_detail``, ``laws``, ``report_detail``, ``reports``. |
| `congress` | `int` | Congress number used to scope legislative records. |
| `bill_type` | `str` | Provider type selector for bill. |
| `bill_number` | `int` | Legislative bill number used with the selected Congress and bill type. |
| `law_type` | `str` | Provider type selector for law. |
| `law_number` | `int` | Public or private law number used with the selected law type. |
| `report_type` | `str` | Provider type selector for report. |
| `report_number` | `int` | Committee report number used with the selected Congress and report type. |
| `offset` | `int` | Zero-based result offset used for pagination. |
| `limit` | `int` | Maximum number of records or items to return. |
| `sort` | `str` | Provider-supported result ordering expression. |
| `from_date_time` | `str` | Earliest provider update timestamp to include. |
| `to_date_time` | `str` | Latest provider update timestamp to include. |
| `conference` | `bool` | Whether to restrict committee reports to conference reports. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_internet_archive`

Retrieve Internet Archive search and metadata.

### Signature

```python
def fetch_internet_archive( keywords: str, fields: List[str] | None=None, rows: int=10, page: int=1, sort: str='downloads desc', media_type: str='', collection: str='', time: int=20 ) -> Any
```

### Purpose

Retrieve Internet Archive search and metadata through Internet Archive. The query text determines the records or documents matched by the provider. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_internet_archive

result = fetch_internet_archive(
    keywords='retrieval augmented generation' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `keywords` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `fields` | `List[str] | None` | Comma-separated or provider-specific field selection. |
| `rows` | `int` | Maximum number of rows to request. |
| `page` | `int` | One-based result page to request. |
| `sort` | `str` | Provider-supported result ordering expression. |
| `media_type` | `str` | Provider type selector for media. |
| `collection` | `str` | Provider collection identifier used to restrict results. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `fetch_grokipedia`

Retrieve Grokipedia search and page.

### Signature

```python
def fetch_grokipedia( mode: str='search', query: str='', page: str='', limit: int=12, offset: int=0, include_content: bool=True ) -> Any
```

### Purpose

Retrieve Grokipedia search and page through Grokipedia. The query text determines the records or documents matched by the provider. Result-count arguments bound the amount of data requested.

### Example

```python
from fonky.gemini.tools import fetch_grokipedia

result = fetch_grokipedia( )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `query` | `str` | Search text, lookup value, or provider query submitted by the caller. |
| `page` | `str` | One-based result page to request. |
| `limit` | `int` | Maximum number of records or items to return. |
| `offset` | `int` | Zero-based result offset used for pagination. |
| `include_content` | `bool` | Whether to include content in the result. |

### Returns

Any: Structured mapping produced by the operation.

### Raises

ValueError: If a required value is missing, blank, or outside the supported range. Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_arxiv`

Load ArXiv research documents.

### Signature

```python
def load_arxiv( question: str ) -> Any
```

### Purpose

Load ArXiv research documents using the ArXiv loader. The query text determines the records or documents matched by the provider.

### Example

```python
from fonky.gemini.tools import load_arxiv

result = load_arxiv(
    question='retrieval augmented generation' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `question` | `str` | Search query or prompt submitted to the backing loader. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_wikipedia`

Load Wikipedia articles.

### Signature

```python
def load_wikipedia( question: str ) -> Any
```

### Purpose

Load Wikipedia articles using the Wikipedia loader. The query text determines the records or documents matched by the provider.

### Example

```python
from fonky.gemini.tools import load_wikipedia

result = load_wikipedia(
    question='retrieval augmented generation' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `question` | `str` | Search query or prompt submitted to the backing loader. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---
