# API Reference: `scrapers.py`

`scrapers.py` contains the HTML extraction layer. `WebExtractor` provides page extraction and independent structural scraping operations.

## Module Inventory

- **Classes:** 2
- **Top-level functions:** 1

## Module-Level Functions

| Function | Signature | Purpose |
|---|---|---|
| `throw_if()` | `throw_if( name: str, value: object ) -> None` | Throw if. |

## Classes

| Class | Constructor | Public Methods | Functional Wrappers |
|---|---|---:|---:|
| [`Extractor`](#extractor) | `Extractor( self: Any ) -> Any` | 0 | 0 |
| [`WebExtractor`](#webextractor) | `WebExtractor( self: Any ) -> None` | 13 | 12 |

## `Extractor`

Provide shared state for HTML extraction classes.

```python
Extractor( self: Any ) -> Any
```

**Source:** `scrapers.py`, line 87

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `WebExtractor`

Fetch and extract selected structures from HTML pages.

```python
WebExtractor( self: Any ) -> None
```

**Source:** `scrapers.py`, line 128

**Functional wrappers:** `fonky.scrape_web_page()`, `fonky.scraper_html_to_text()`, `fonky.scrape_paragraphs()`, `fonky.scrape_lists()`, `fonky.scrape_tables()`, `fonky.scrape_articles()`, `fonky.scrape_headings()`, `fonky.scrape_divisions()`, `fonky.scrape_sections()`, `fonky.scrape_blockquotes()`, `fonky.scrape_hyperlinks()`, `fonky.scrape_images()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `scrape()` | `scrape( self: Any, url: str, time: int = 10 ) -> Result \| None` | Fetch a web page. |
| `html_to_text()` | `html_to_text( self: Any, html: str ) -> str` | Convert HTML to plain text. |
| `scrape_paragraphs()` | `scrape_paragraphs( self: Any, uri: str ) -> List[str] \| None` | Extract paragraph text. |
| `scrape_lists()` | `scrape_lists( self: Any, uri: str ) -> List[str] \| None` | Extract list item text. |
| `scrape_tables()` | `scrape_tables( self: Any, uri: str ) -> List[str] \| None` | Extract table cell text. |
| `scrape_articles()` | `scrape_articles( self: Any, uri: str ) -> List[str] \| None` | Extract article text. |
| `scrape_headings()` | `scrape_headings( self: Any, uri: str ) -> List[str] \| None` | Extract heading text. |
| `scrape_divisions()` | `scrape_divisions( self: Any, uri: str ) -> List[str] \| None` | Extract division text. |
| `scrape_sections()` | `scrape_sections( self: Any, uri: str ) -> List[str] \| None` | Extract section text. |
| `scrape_blockquotes()` | `scrape_blockquotes( self: Any, uri: str ) -> List[str] \| None` | Extract blockquote text. |
| `scrape_hyperlinks()` | `scrape_hyperlinks( self: Any, uri: str ) -> List[str] \| None` | Extract hyperlinks. |
| `scrape_images()` | `scrape_images( self: Any, uri: str ) -> List[str] \| None` | Extract image references. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create a dynamic tool schema. |
