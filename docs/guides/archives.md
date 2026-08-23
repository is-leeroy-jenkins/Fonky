# Archives

Research, search, government, legislative, news, and archival retrieval.

## Functional Operations

| Function | Signature | Purpose |
|---|---|---|
| `fetch_arxiv()` | `fetch_arxiv( question: str, max_documents: int = None, full_documents: bool = None, include_metadata: bool = None ) -> Any` | Fetch ArXiv research document retrieval. Provides direct module-level access to ``ArXiv.fetch`` using a fresh ``ArXiv`` instance. Any: Value returned by ``ArXiv.fetch``. |
| `fetch_google_drive()` | `fetch_google_drive( question: str, folder_id: str = 'root', results: int = 10, template: str = 'gdrive-query', mime_type: str = None, mode: str = 'documents' ) -> Any` | Fetch Google Drive document retrieval. Provides direct module-level access to ``GoogleDrive.fetch`` using a fresh ``GoogleDrive`` instance. Any: Value returned by ``GoogleDrive.fetch``. |
| `fetch_wikipedia()` | `fetch_wikipedia( question: str, language: str = None, max_documents: int = None, include_metadata: bool = None ) -> Any` | Fetch Wikipedia document retrieval. Provides direct module-level access to ``Wikipedia.fetch`` using a fresh ``Wikipedia`` instance. Any: Value returned by ``Wikipedia.fetch``. |
| `fetch_news()` | `fetch_news( endpoint: str = 'all', query: str = '', language: str = 'en', categories: str = '', exclude_categories: str = '', locale: str = '', domains: str = '', exclude_domains: str = '', source_ids: str = '', exclude_source_ids: str = '', published_after: str = '', published_before: str = '', published_on: str = '', sort: str = 'published_at', limit: int = 10, page: int = 1, include_similar: bool = True, headlines_per_category: int = 6, time: int = 10, api_key: str = None ) -> Any` | Fetch The News API article retrieval. Provides direct module-level access to ``TheNews.fetch`` using a fresh ``TheNews`` instance. Any: Value returned by ``TheNews.fetch``. |
| `fetch_google_search()` | `fetch_google_search( keywords: str, results: int = 10, start: int = 1, exact_terms: str = '', exclude_terms: str = '', file_type: str = '', date_restrict: str = '', gl: str = '', lr: str = '', safe: str = 'off', search_type: str = '', site_search: str = '', site_search_filter: str = '', sort: str = '', img_size: str = '', img_type: str = '', img_color_type: str = '', img_dominant_color: str = '', time: int = 10, api_key: str = None, cse_id: str = None ) -> Any` | Fetch Google Custom Search retrieval. Provides direct module-level access to ``GoogleSearch.fetch`` using a fresh ``GoogleSearch`` instance. Any: Value returned by ``GoogleSearch.fetch``. |
| `fetch_gov_data()` | `fetch_gov_data( mode: str = 'search', query: str = '', page_size: int = 10, offset_mark: str = '*', sort_field: str = 'score', sort_order: str = 'DESC', package_id: str = '', collection: str = '', start_date: str = '', time: int = 20 ) -> Any` | Fetch Data.gov package and collection retrieval. Provides direct module-level access to ``GovData.fetch`` using a fresh ``GovData`` instance. Any: Value returned by ``GovData.fetch``. |
| `fetch_congress()` | `fetch_congress( mode: str = 'congresses', congress: int = 0, bill_type: str = '', bill_number: int = 0, law_type: str = '', law_number: int = 0, report_type: str = '', report_number: int = 0, offset: int = 0, limit: int = 20, sort: str = 'updateDate+desc', from_date_time: str = '', to_date_time: str = '', conference: bool = False, time: int = 20 ) -> Any` | Fetch Congress.gov legislative data retrieval. Provides direct module-level access to ``Congress.fetch`` using a fresh ``Congress`` instance. Any: Value returned by ``Congress.fetch``. |
| `fetch_internet_archive()` | `fetch_internet_archive( keywords: str, fields: List[str] \| None = None, rows: int = 10, page: int = 1, sort: str = 'downloads desc', media_type: str = '', collection: str = '', time: int = 20 ) -> Any` | Fetch Internet Archive search and metadata retrieval. Provides direct module-level access to ``InternetArchive.fetch`` using a fresh ``InternetArchive`` instance. Any: Value returned by ``InternetArchive.fetch``. |
| `fetch_grokipedia()` | `fetch_grokipedia( mode: str = 'search', query: str = '', page: str = '', limit: int = 12, offset: int = 0, include_content: bool = True ) -> Any` | Fetch Grokipedia search and page retrieval. Provides direct module-level access to ``Grokipedia.fetch`` using a fresh ``Grokipedia`` instance. Any: Value returned by ``Grokipedia.fetch``. |
| `load_arxiv()` | `load_arxiv( question: str ) -> Any` | Load source content. Provides direct module-level access to ``ArXivLoader.load`` using a fresh ``ArXivLoader`` instance. Any: Value returned by ``ArXivLoader.load``. |
| `load_wikipedia()` | `load_wikipedia( question: str ) -> Any` | Load source content. Provides direct module-level access to ``WikiLoader.load`` using a fresh ``WikiLoader`` instance. Any: Value returned by ``WikiLoader.load``. |

## How to choose

Use the functional wrapper when one call completes the task. Use the implementation class when you need retained state, helper methods, or direct provider debugging.

## Operational considerations

- Remote providers require network access.
- Rate limits, timeouts, service availability, and response-shape changes remain operational concerns.
- Provider-specific argument validation is enforced by the implementation class.

## Representative Functions

### `fetch_arxiv()`

```python
# fetch_arxiv( question: str, max_documents: int = None, full_documents: bool = None, include_metadata: bool = None ) -> Any
```

Fetch ArXiv research document retrieval. Provides direct module-level access to ``ArXiv.fetch`` using a fresh ``ArXiv`` instance. Any: Value returned by ``ArXiv.fetch``.

### `fetch_google_drive()`

```python
# fetch_google_drive( question: str, folder_id: str = 'root', results: int = 10, template: str = 'gdrive-query', mime_type: str = None, mode: str = 'documents' ) -> Any
```

Fetch Google Drive document retrieval. Provides direct module-level access to ``GoogleDrive.fetch`` using a fresh ``GoogleDrive`` instance. Any: Value returned by ``GoogleDrive.fetch``.

### `fetch_wikipedia()`

```python
# fetch_wikipedia( question: str, language: str = None, max_documents: int = None, include_metadata: bool = None ) -> Any
```

Fetch Wikipedia document retrieval. Provides direct module-level access to ``Wikipedia.fetch`` using a fresh ``Wikipedia`` instance. Any: Value returned by ``Wikipedia.fetch``.

### `fetch_news()`

```python
# fetch_news( endpoint: str = 'all', query: str = '', language: str = 'en', categories: str = '', exclude_categories: str = '', locale: str = '', domains: str = '', exclude_domains: str = '', source_ids: str = '', exclude_source_ids: str = '', published_after: str = '', published_before: str = '', published_on: str = '', sort: str = 'published_at', limit: int = 10, page: int = 1, include_similar: bool = True, headlines_per_category: int = 6, time: int = 10, api_key: str = None ) -> Any
```

Fetch The News API article retrieval. Provides direct module-level access to ``TheNews.fetch`` using a fresh ``TheNews`` instance. Any: Value returned by ``TheNews.fetch``.

### `fetch_google_search()`

```python
# fetch_google_search( keywords: str, results: int = 10, start: int = 1, exact_terms: str = '', exclude_terms: str = '', file_type: str = '', date_restrict: str = '', gl: str = '', lr: str = '', safe: str = 'off', search_type: str = '', site_search: str = '', site_search_filter: str = '', sort: str = '', img_size: str = '', img_type: str = '', img_color_type: str = '', img_dominant_color: str = '', time: int = 10, api_key: str = None, cse_id: str = None ) -> Any
```

Fetch Google Custom Search retrieval. Provides direct module-level access to ``GoogleSearch.fetch`` using a fresh ``GoogleSearch`` instance. Any: Value returned by ``GoogleSearch.fetch``.

### `fetch_gov_data()`

```python
# fetch_gov_data( mode: str = 'search', query: str = '', page_size: int = 10, offset_mark: str = '*', sort_field: str = 'score', sort_order: str = 'DESC', package_id: str = '', collection: str = '', start_date: str = '', time: int = 20 ) -> Any
```

Fetch Data.gov package and collection retrieval. Provides direct module-level access to ``GovData.fetch`` using a fresh ``GovData`` instance. Any: Value returned by ``GovData.fetch``.

### `fetch_congress()`

```python
# fetch_congress( mode: str = 'congresses', congress: int = 0, bill_type: str = '', bill_number: int = 0, law_type: str = '', law_number: int = 0, report_type: str = '', report_number: int = 0, offset: int = 0, limit: int = 20, sort: str = 'updateDate+desc', from_date_time: str = '', to_date_time: str = '', conference: bool = False, time: int = 20 ) -> Any
```

Fetch Congress.gov legislative data retrieval. Provides direct module-level access to ``Congress.fetch`` using a fresh ``Congress`` instance. Any: Value returned by ``Congress.fetch``.

### `fetch_internet_archive()`

```python
# fetch_internet_archive( keywords: str, fields: List[str] | None = None, rows: int = 10, page: int = 1, sort: str = 'downloads desc', media_type: str = '', collection: str = '', time: int = 20 ) -> Any
```

Fetch Internet Archive search and metadata retrieval. Provides direct module-level access to ``InternetArchive.fetch`` using a fresh ``InternetArchive`` instance. Any: Value returned by ``InternetArchive.fetch``.


See [Functional API](../api/fonky.md) for all signatures.
