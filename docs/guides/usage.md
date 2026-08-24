# Usage Patterns

## Representative Recipes

### Retrieval-first

```python
from fonky.fonky import fetch_gov_data

result = fetch_gov_data.invoke(
    {
        'query': 'budget execution',
        'max_documents': 5,
        'full_documents': False,
        'include_metadata': True
    }
)
```

### Loader-first

```python
from fonky.fonky import load_markdown

docs = load_markdown.invoke(
    {
        'file_path': 'README.md'
    }
)
```

### Scraper-first

```python
from fonky.fonky import scrape_tables

tables = scrape_tables.invoke(
    {
        'uri': 'https://example.com/report'
    }
)
```
