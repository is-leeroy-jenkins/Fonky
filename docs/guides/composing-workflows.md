# Composing Workflows

## Common Compositions

| Composition                              | Pattern                                                                |
|------------------------------------------|------------------------------------------------------------------------|
| retrieval → load → summarize             | fetch source metadata, materialize content, summarize/index downstream |
| recursive web load → scrape tables/links | capture a site section, then extract specific page structures          |
| environmental fetch → geocode → map      | retrieve events/measurements, enrich with spatial context              |
| research + public data                   | combine archive sources with government or demographic datasets        |
| document load → chunk → index            | produce `Document` objects, split, and send to vector storage          |

## Example

```python
from funkytown.fonky import fetch_google_search
from funkytown.fonky import load_web

search_hits = fetch_google_search.invoke(
    {
        'question': 'federal data governance policy',
        'max_documents': 3,
        'full_documents': False,
        'include_metadata': True
    }
)

page = load_web.invoke(
    {
        'url': 'https://example.gov/policy',
        'depth': 0,
        'preserve_links': True
    }
)
```

## Composition Rule

Keep each step narrow and typed. Fetch for discovery, load for document construction, scrape for structure, and process/index downstream.
