# Adding a Functional Wrapper

```python
def scrape_tables( uri: str ):
    scraper = WebExtractor( )
    return scraper.scrape_tables( uri=uri )
```

Keep wrappers thin: explicit parameters, local implementation instance, direct method call, no duplicated provider logic.
