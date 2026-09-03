# Web Retrieval & Loading

**Tools:** 11

Examples use the Google ADK callable wrapper surface so each example is directly executable as ordinary Python.

## Tool Index

| Tool |
|---|
| [`fetch_web_page`](#fetch_web_page) |
| [`convert_html_to_text`](#convert_html_to_text) |
| [`extract_web_title`](#extract_web_title) |
| [`extract_web_links`](#extract_web_links) |
| [`extract_web_structured_data`](#extract_web_structured_data) |
| [`crawl_web`](#crawl_web) |
| [`render_web_page`](#render_web_page) |
| [`load_web`](#load_web) |
| [`load_web_recursive`](#load_web_recursive) |
| [`load_web_pages`](#load_web_pages) |
| [`load_github`](#load_github) |

---

## `fetch_web_page`

Retrieve HTTP web page content and HTML extraction data.

### Signature

```python
def fetch_web_page( url: str, time: int=10 ) -> Any
```

### Purpose

Retrieve HTTP web page content and HTML extraction data through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import fetch_web_page

result = fetch_web_page(
    url='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `url` | `str` | URL used by the operation. |
| `time` | `int` | Request timeout in seconds. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `convert_html_to_text`

Convert HTML to plain text.

### Signature

```python
def convert_html_to_text( html: str ) -> Any
```

### Purpose

Convert HTML to plain text through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import convert_html_to_text

result = convert_html_to_text(
    html='<html><body><p>Example</p></body></html>' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `html` | `str` | Html value used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `extract_web_title`

Extract a web title from supplied HTML content.

### Signature

```python
def extract_web_title( html: str ) -> Any
```

### Purpose

Extract a web title from supplied HTML content through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import extract_web_title

result = extract_web_title(
    html='<html><body><p>Example</p></body></html>' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `html` | `str` | Html value used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `extract_web_links`

Extract web links from supplied HTML content.

### Signature

```python
def extract_web_links( base_url: str, html: str ) -> Any
```

### Purpose

Extract web links from supplied HTML content through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import extract_web_links

result = extract_web_links(
    base_url='https://example.com',
    html='<html><body><p>Example</p></body></html>' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `base_url` | `str` | Base url value used by the operation. |
| `html` | `str` | Html value used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `extract_web_structured_data`

Extract structured data from supplied HTML content.

### Signature

```python
def extract_web_structured_data( url: str, html: str, selected_methods: Optional[List[str]]=None ) -> Any
```

### Purpose

Extract structured data from supplied HTML content through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import extract_web_structured_data

result = extract_web_structured_data(
    url='https://example.com',
    html='<html><body><p>Example</p></body></html>' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `url` | `str` | URL used by the operation. |
| `html` | `str` | Html value used by the operation. |
| `selected_methods` | `Optional[List[str]]` | Selected methods value used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `crawl_web`

Crawl web pages from a seed URL.

### Signature

```python
def crawl_web( seed_url: str, include_title: bool=True, include_basic_text: bool=True, include_raw_html: bool=False, selected_methods: Optional[List[str]]=None, recursive: bool=False, max_depth: int=1, max_pages: int=10, same_domain_only: bool=True, request_timeout: int=10, delay_seconds: float=0.25, max_bytes: int=1000000, headers: Optional[Dict[str, str]]=None, use_playwright: bool=False ) -> Any
```

### Purpose

Crawl web pages from a seed URL through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import crawl_web

result = crawl_web(
    seed_url='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `seed_url` | `str` | Seed url value used by the operation. |
| `include_title` | `bool` | Include title value used by the operation. |
| `include_basic_text` | `bool` | Include basic text value used by the operation. |
| `include_raw_html` | `bool` | Include raw html value used by the operation. |
| `selected_methods` | `Optional[List[str]]` | Selected methods value used by the operation. |
| `recursive` | `bool` | Whether nested resources should be traversed recursively. |
| `max_depth` | `int` | Max depth value used by the operation. |
| `max_pages` | `int` | Max pages value used by the operation. |
| `same_domain_only` | `bool` | Same domain only value used by the operation. |
| `request_timeout` | `int` | Request timeout value used by the operation. |
| `delay_seconds` | `float` | Delay seconds value used by the operation. |
| `max_bytes` | `int` | Max bytes value used by the operation. |
| `headers` | `Optional[Dict[str, str]]` | Headers value used by the operation. |
| `use_playwright` | `bool` | Use playwright value used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `render_web_page`

Render a dynamic web page with Playwright.

### Signature

```python
def render_web_page( url: str, timeout: int=15, headers: Optional[Dict[str, str]]=None, use_playwright: bool=False ) -> Any
```

### Purpose

Render a dynamic web page with Playwright through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import render_web_page

result = render_web_page(
    url='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `url` | `str` | URL used by the operation. |
| `timeout` | `int` | Maximum time in seconds to wait for the operation. |
| `headers` | `Optional[Dict[str, str]]` | Headers value used by the operation. |
| `use_playwright` | `bool` | Use playwright value used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `load_web`

Load web documents.

### Signature

```python
def load_web( urls: str | List[str], recursive: bool=False, max_depth: int=2, prevent_outside: bool=True, timeout: int=10, ignore: bool=True, progress: bool=True ) -> Any
```

### Purpose

Load web documents through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import load_web

result = load_web(
    urls=['https://example.com'] )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `urls` | `str | List[str]` | Urls value used by the operation. |
| `recursive` | `bool` | Whether nested resources should be traversed recursively. |
| `max_depth` | `int` | Max depth value used by the operation. |
| `prevent_outside` | `bool` | Prevent outside value used by the operation. |
| `timeout` | `int` | Maximum time in seconds to wait for the operation. |
| `ignore` | `bool` | Ignore value used by the operation. |
| `progress` | `bool` | Progress value used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `load_web_recursive`

Recursively load web documents.

### Signature

```python
def load_web_recursive( url: str, depth: int=2, max_time: int=10, ignore: bool=True ) -> Any
```

### Purpose

Recursively load web documents through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import load_web_recursive

result = load_web_recursive(
    url='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `url` | `str` | URL used by the operation. |
| `depth` | `int` | Depth value used by the operation. |
| `max_time` | `int` | Max time value used by the operation. |
| `ignore` | `bool` | Ignore value used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `load_web_pages`

Load static web pages.

### Signature

```python
def load_web_pages( urls: List[str], depth: int=2, timeout: int=10, ignore: bool=True, progress: bool=True ) -> Any
```

### Purpose

Load static web pages through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import load_web_pages

result = load_web_pages(
    urls=['https://example.com'] )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `urls` | `List[str]` | Urls value used by the operation. |
| `depth` | `int` | Depth value used by the operation. |
| `timeout` | `int` | Maximum time in seconds to wait for the operation. |
| `ignore` | `bool` | Ignore value used by the operation. |
| `progress` | `bool` | Progress value used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `load_github`

Load files from a GitHub repository.

### Signature

```python
def load_github( url: str, repo: str, branch: str, filetype: str='.md' ) -> Any
```

### Purpose

Load files from a GitHub repository through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import load_github

result = load_github(
    url='https://example.com',
    repo='is-leeroy-jenkins/Fonky',
    branch='main' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `url` | `str` | URL used by the operation. |
| `repo` | `str` | Repo value used by the operation. |
| `branch` | `str` | Branch value used by the operation. |
| `filetype` | `str` | Filetype value used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---
