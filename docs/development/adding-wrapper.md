# Adding a `fonky.py` Wrapper

The wrapper is an ergonomic surface, not a new implementation layer.

```python
def scrape_tables( uri: str ):
    scraper = WebExtractor( )
    return scraper.scrape_tables(
        uri=uri
    )
```

## Requirements

- explicit typed parameters;
- no duplicated provider logic;
- local implementation instance;
- direct call to the intended method;
- result returned without unnecessary transformation;
- exported through `__all__`;
- route test verifies class, method, argument names, and result propagation.
