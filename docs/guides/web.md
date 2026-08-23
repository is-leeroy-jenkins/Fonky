# Web

General web fetching, crawling, HTML conversion, link/title extraction, structured extraction, loading, and targeted scraping.

## Functional Operations

| Function | Signature | Purpose |
|---|---|---|
| `fetch_web_page()` | `fetch_web_page( url: str, time: int = 10 ) -> Any` | Fetch HTTP web page retrieval and HTML extraction. Provides direct module-level access to ``WebFetcher.fetch`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.fetch``. |
| `convert_html_to_text()` | `convert_html_to_text( html: str ) -> Any` | HTML to text. Provides direct module-level access to ``WebFetcher.html_to_text`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.html_to_text``. |
| `extract_web_title()` | `extract_web_title( html: str ) -> Any` | Extract title. Provides direct module-level access to ``WebFetcher.extract_title`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_title``. |
| `extract_web_links()` | `extract_web_links( base_url: str, html: str ) -> Any` | Extract links. Provides direct module-level access to ``WebFetcher.extract_links`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_links``. |
| `extract_web_structured_data()` | `extract_web_structured_data( url: str, html: str, selected_methods: Optional[List[str]] = None ) -> Any` | Extract structured data. Provides direct module-level access to ``WebFetcher.extract_structured_data`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_structured_data``. |
| `crawl_web()` | `crawl_web( seed_url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, recursive: bool = False, max_depth: int = 1, max_pages: int = 10, same_domain_only: bool = True, request_timeout: int = 10, delay_seconds: float = 0.25, max_bytes: int = 1000000, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any` | Crawl. Provides direct module-level access to ``WebCrawler.crawl`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.crawl``. |
| `scrape_crawler_page()` | `scrape_crawler_page( url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, request_timeout: int = 10, max_bytes: int = 1000000, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any` | Scrape page. Provides direct module-level access to ``WebCrawler.scrape_page`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.scrape_page``. |
| `render_web_page()` | `render_web_page( url: str, timeout: int = 15, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any` | Render with playwright. Provides direct module-level access to ``WebCrawler.render_with_playwright`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.render_with_playwright``. |
| `load_web()` | `load_web( urls: str \| List[str], recursive: bool = False, max_depth: int = 2, prevent_outside: bool = True, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> Any` | Load source content. Provides direct module-level access to ``WebLoader.load`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load``. |
| `load_web_recursive()` | `load_web_recursive( url: str, depth: int = 2, max_time: int = 10, ignore: bool = True ) -> Any` | Load web documents recursively. Provides direct module-level access to ``WebLoader.load_recursive`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load_recursive``. |
| `load_web_pages()` | `load_web_pages( urls: List[str], depth: int = 2, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> Any` | Load static web pages. Provides direct module-level access to ``WebLoader.load_pages`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load_pages``. |
| `load_github()` | `load_github( url: str, repo: str, branch: str, filetype: str = '.md' ) -> Any` | Load source content. Provides direct module-level access to ``GithubLoader.load`` using a fresh ``GithubLoader`` instance. Any: Value returned by ``GithubLoader.load``. |
| `scrape_web_page()` | `scrape_web_page( url: str, time: int = 10 ) -> Any` | Fetch a web page. Provides direct module-level access to ``WebExtractor.scrape`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape``. |
| `scraper_html_to_text()` | `scraper_html_to_text( html: str ) -> Any` | Convert HTML to plain text. Provides direct module-level access to ``WebExtractor.html_to_text`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.html_to_text``. |
| `scrape_paragraphs()` | `scrape_paragraphs( uri: str ) -> Any` | Extract paragraph text. Provides direct module-level access to ``WebExtractor.scrape_paragraphs`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_paragraphs``. |
| `scrape_lists()` | `scrape_lists( uri: str ) -> Any` | Extract list item text. Provides direct module-level access to ``WebExtractor.scrape_lists`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_lists``. |
| `scrape_tables()` | `scrape_tables( uri: str ) -> Any` | Extract table cell text. Provides direct module-level access to ``WebExtractor.scrape_tables`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_tables``. |
| `scrape_articles()` | `scrape_articles( uri: str ) -> Any` | Extract article text. Provides direct module-level access to ``WebExtractor.scrape_articles`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_articles``. |
| `scrape_headings()` | `scrape_headings( uri: str ) -> Any` | Extract heading text. Provides direct module-level access to ``WebExtractor.scrape_headings`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_headings``. |
| `scrape_divisions()` | `scrape_divisions( uri: str ) -> Any` | Extract division text. Provides direct module-level access to ``WebExtractor.scrape_divisions`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_divisions``. |
| `scrape_sections()` | `scrape_sections( uri: str ) -> Any` | Extract section text. Provides direct module-level access to ``WebExtractor.scrape_sections`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_sections``. |
| `scrape_blockquotes()` | `scrape_blockquotes( uri: str ) -> Any` | Extract blockquote text. Provides direct module-level access to ``WebExtractor.scrape_blockquotes`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_blockquotes``. |
| `scrape_hyperlinks()` | `scrape_hyperlinks( uri: str ) -> Any` | Extract hyperlinks. Provides direct module-level access to ``WebExtractor.scrape_hyperlinks`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_hyperlinks``. |
| `scrape_images()` | `scrape_images( uri: str ) -> Any` | Extract image references. Provides direct module-level access to ``WebExtractor.scrape_images`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_images``. |
| `encode_image()` | `encode_image( path: str ) -> str` | Encode an image as Base64 text. Provides direct module-level access to ``fetchers.encode_image``. str: Base64-encoded image data. |

## How to choose

Use the functional wrapper when one call completes the task. Use the implementation class when you need retained state, helper methods, or direct provider debugging.

## Operational considerations

- Remote providers require network access.
- Rate limits, timeouts, service availability, and response-shape changes remain operational concerns.
- Provider-specific argument validation is enforced by the implementation class.

## Representative Functions

### `fetch_web_page()`

```python
# fetch_web_page( url: str, time: int = 10 ) -> Any
```

Fetch HTTP web page retrieval and HTML extraction. Provides direct module-level access to ``WebFetcher.fetch`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.fetch``.

### `convert_html_to_text()`

```python
# convert_html_to_text( html: str ) -> Any
```

HTML to text. Provides direct module-level access to ``WebFetcher.html_to_text`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.html_to_text``.

### `extract_web_title()`

```python
# extract_web_title( html: str ) -> Any
```

Extract title. Provides direct module-level access to ``WebFetcher.extract_title`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_title``.

### `extract_web_links()`

```python
# extract_web_links( base_url: str, html: str ) -> Any
```

Extract links. Provides direct module-level access to ``WebFetcher.extract_links`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_links``.

### `extract_web_structured_data()`

```python
# extract_web_structured_data( url: str, html: str, selected_methods: Optional[List[str]] = None ) -> Any
```

Extract structured data. Provides direct module-level access to ``WebFetcher.extract_structured_data`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_structured_data``.

### `crawl_web()`

```python
# crawl_web( seed_url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, recursive: bool = False, max_depth: int = 1, max_pages: int = 10, same_domain_only: bool = True, request_timeout: int = 10, delay_seconds: float = 0.25, max_bytes: int = 1000000, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any
```

Crawl. Provides direct module-level access to ``WebCrawler.crawl`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.crawl``.

### `scrape_crawler_page()`

```python
# scrape_crawler_page( url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, request_timeout: int = 10, max_bytes: int = 1000000, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any
```

Scrape page. Provides direct module-level access to ``WebCrawler.scrape_page`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.scrape_page``.

### `render_web_page()`

```python
# render_web_page( url: str, timeout: int = 15, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any
```

Render with playwright. Provides direct module-level access to ``WebCrawler.render_with_playwright`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.render_with_playwright``.


See [Functional API](../api/fonky.md) for all signatures.
