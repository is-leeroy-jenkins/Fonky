# Web Scraping

**Tools:** 14

Examples use the Google ADK callable wrapper surface so each example is directly executable as ordinary Python.

## Tool Index

| Tool |
|---|
| [`scrape_crawler_page`](#scrape_crawler_page) |
| [`scrape_web_page`](#scrape_web_page) |
| [`scraper_html_to_text`](#scraper_html_to_text) |
| [`scrape_paragraphs`](#scrape_paragraphs) |
| [`scrape_lists`](#scrape_lists) |
| [`scrape_tables`](#scrape_tables) |
| [`scrape_articles`](#scrape_articles) |
| [`scrape_headings`](#scrape_headings) |
| [`scrape_divisions`](#scrape_divisions) |
| [`scrape_sections`](#scrape_sections) |
| [`scrape_blockquotes`](#scrape_blockquotes) |
| [`scrape_hyperlinks`](#scrape_hyperlinks) |
| [`scrape_images`](#scrape_images) |
| [`encode_image`](#encode_image) |

---

## `scrape_crawler_page`

Extract a crawler page from an HTML page.

### Signature

```python
def scrape_crawler_page( url: str, include_title: bool=True, include_basic_text: bool=True, include_raw_html: bool=False, selected_methods: Optional[List[str]]=None, request_timeout: int=10, max_bytes: int=1000000, headers: Optional[Dict[str, str]]=None, use_playwright: bool=False ) -> Any
```

### Purpose

Extract a crawler page from an HTML page through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import scrape_crawler_page

result = scrape_crawler_page(
    url='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `url` | `str` | URL used by the operation. |
| `include_title` | `bool` | Include title value used by the operation. |
| `include_basic_text` | `bool` | Include basic text value used by the operation. |
| `include_raw_html` | `bool` | Include raw html value used by the operation. |
| `selected_methods` | `Optional[List[str]]` | Selected methods value used by the operation. |
| `request_timeout` | `int` | Request timeout value used by the operation. |
| `max_bytes` | `int` | Max bytes value used by the operation. |
| `headers` | `Optional[Dict[str, str]]` | Headers value used by the operation. |
| `use_playwright` | `bool` | Use playwright value used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `scrape_web_page`

Fetch a web page for extraction.

### Signature

```python
def scrape_web_page( url: str, time: int=10 ) -> Any
```

### Purpose

Fetch a web page for extraction through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import scrape_web_page

result = scrape_web_page(
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

## `scraper_html_to_text`

Convert scraper HTML to plain text.

### Signature

```python
def scraper_html_to_text( html: str ) -> Any
```

### Purpose

Convert scraper HTML to plain text through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import scraper_html_to_text

result = scraper_html_to_text(
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

## `scrape_paragraphs`

Extract paragraph text from an HTML page.

### Signature

```python
def scrape_paragraphs( uri: str ) -> Any
```

### Purpose

Extract paragraph text from an HTML page through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import scrape_paragraphs

result = scrape_paragraphs(
    uri='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `uri` | `str` | URI used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `scrape_lists`

Extract list-item text from an HTML page.

### Signature

```python
def scrape_lists( uri: str ) -> Any
```

### Purpose

Extract list-item text from an HTML page through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import scrape_lists

result = scrape_lists(
    uri='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `uri` | `str` | URI used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `scrape_tables`

Extract table-cell text from an HTML page.

### Signature

```python
def scrape_tables( uri: str ) -> Any
```

### Purpose

Extract table-cell text from an HTML page through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import scrape_tables

result = scrape_tables(
    uri='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `uri` | `str` | URI used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `scrape_articles`

Extract article text from an HTML page.

### Signature

```python
def scrape_articles( uri: str ) -> Any
```

### Purpose

Extract article text from an HTML page through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import scrape_articles

result = scrape_articles(
    uri='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `uri` | `str` | URI used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `scrape_headings`

Extract heading text from an HTML page.

### Signature

```python
def scrape_headings( uri: str ) -> Any
```

### Purpose

Extract heading text from an HTML page through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import scrape_headings

result = scrape_headings(
    uri='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `uri` | `str` | URI used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `scrape_divisions`

Extract division text from an HTML page.

### Signature

```python
def scrape_divisions( uri: str ) -> Any
```

### Purpose

Extract division text from an HTML page through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import scrape_divisions

result = scrape_divisions(
    uri='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `uri` | `str` | URI used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `scrape_sections`

Extract section text from an HTML page.

### Signature

```python
def scrape_sections( uri: str ) -> Any
```

### Purpose

Extract section text from an HTML page through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import scrape_sections

result = scrape_sections(
    uri='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `uri` | `str` | URI used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `scrape_blockquotes`

Extract blockquote text from an HTML page.

### Signature

```python
def scrape_blockquotes( uri: str ) -> Any
```

### Purpose

Extract blockquote text from an HTML page through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import scrape_blockquotes

result = scrape_blockquotes(
    uri='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `uri` | `str` | URI used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `scrape_hyperlinks`

Extract hyperlinks from an HTML page.

### Signature

```python
def scrape_hyperlinks( uri: str ) -> Any
```

### Purpose

Extract hyperlinks from an HTML page through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import scrape_hyperlinks

result = scrape_hyperlinks(
    uri='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `uri` | `str` | URI used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `scrape_images`

Extract image references from an HTML page.

### Signature

```python
def scrape_images( uri: str ) -> Any
```

### Purpose

Extract image references from an HTML page through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import scrape_images

result = scrape_images(
    uri='https://example.com' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `uri` | `str` | URI used by the operation. |

### Returns

Any: Value produced by the delegated Fonky implementation.

---

## `encode_image`

Encode a local image as Base64 text.

### Signature

```python
def encode_image( path: str ) -> str
```

### Purpose

Encode a local image as Base64 text through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import encode_image

result = encode_image(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local filesystem path used by the operation. |

### Returns

str: Value produced by the delegated Fonky implementation.

---
