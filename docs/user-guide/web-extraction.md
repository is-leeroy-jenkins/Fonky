# Web Extraction

## Fetch a page

```python
from fonky.gemini.tools import fetch_web_page

page = fetch_web_page(
    uri='https://example.com' )

print( page )
```

## Extract paragraphs

```python
from fonky.gemini.tools import scrape_paragraphs

paragraphs = scrape_paragraphs(
    uri='https://example.com' )

print( paragraphs )
```

## Extract tables

```python
from fonky.gemini.tools import scrape_tables

tables = scrape_tables(
    uri='https://example.com' )

print( tables )
```

## Extract hyperlinks

```python
from fonky.gemini.tools import scrape_hyperlinks

links = scrape_hyperlinks(
    uri='https://example.com' )

print( links )
```

## Crawl a site

```python
from fonky.gemini.tools import crawl_web

pages = crawl_web(
    seed_url='https://example.com',
    recursive=True,
    max_depth=1,
    max_pages=10 )

print( pages )
```
