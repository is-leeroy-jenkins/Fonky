# Web Retrieval & Scraping

The Web domain covers four distinct jobs: **HTTP retrieval**, **content extraction**, **crawling/web
loading**, and **focused structural scraping**.

## Choose the Right Operation

| Need | Function |
|---|---|
| Raw/general page retrieval | `fetch_web_page()` |
| Convert known HTML to text | `convert_html_to_text()` / `scraper_html_to_text()` |
| Extract title/links/structured data from known HTML | `extract_web_title()`, `extract_web_links()`, `extract_web_structured_data()` |
| Crawl multiple pages | `crawl_web()` |
| Render one page, optionally with Playwright | `render_web_page()` |
| Load web content as documents | `load_web()`, `load_web_recursive()`, `load_web_pages()` |
| Load repository content | `load_github()` |
| Extract page structures directly | `scrape_paragraphs()`, `scrape_lists()`, `scrape_tables()`, etc. |

## Workflow — Fetch Once, Extract Several Structures

```python
from fonky import fonky

html = fonky.fetch_web_page(
    url='https://example.com',
    time=10
)

text = fonky.convert_html_to_text(html)
title = fonky.extract_web_title(html)
links = fonky.extract_web_links(
    base_url='https://example.com',
    html=html
)
```

This avoids issuing a separate HTTP request for each extraction when you already have the HTML.

## Workflow — Focused Table Extraction

```python
from fonky import fonky

cells = fonky.scrape_tables(
    uri='https://example.com/report'
)

for value in cells or []:
    print(value)
```

The focused scraper performs its own request and returns flattened readable table-cell text.

## Workflow — Bounded Crawl

```python
from fonky import fonky

pages = fonky.crawl_web(
    seed_url='https://example.com',
    include_title=True,
    include_basic_text=True,
    include_raw_html=False,
    recursive=True,
    max_depth=2,
    max_pages=25,
    same_domain_only=True,
    request_timeout=10,
    delay_seconds=0.5,
    max_bytes=1_000_000,
    use_playwright=False
)
```

Bound `max_depth`, `max_pages`, and `max_bytes`. Crawling without explicit limits can become expensive
or impolite to the target site.

## When to Use Playwright

Set `use_playwright=True` when meaningful content is produced by client-side JavaScript and ordinary
HTTP retrieval does not contain the expected page content. Install Chromium separately with:

```powershell
python -m playwright install chromium
```

## Failure Interpretation

A scraper exception is different from an empty extraction result. An empty list can mean the page
contains no matching structures; an exception can indicate URI validation, network, timeout, HTTP,
or parser failure.
