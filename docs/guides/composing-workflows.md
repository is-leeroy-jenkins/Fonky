# Combining Capabilities

Fonky's domains can be composed because the wrapper layer exposes ordinary Python functions.
Composition should nevertheless preserve each provider's data semantics.

## Example — Geocode Then Query Nearby Environmental Data

```python
from fonky import fonky

location = fonky.geocode_location(
    address='Arlington, VA'
)

# Extract the coordinates according to the geocoder's returned structure,
# then use them with providers that accept latitude/longitude filters.
```

## Example — Search, Fetch, Then Extract

```python
from fonky import fonky

results = fonky.fetch_google_search(
    keywords='site:usgs.gov water data',
    results=5
)

# Select a result URL from the returned provider structure.
# Then retrieve and extract the selected page.
```

## Example — Load Documents for Downstream Retrieval

```python
from fonky import fonky

documents = fonky.load_pdf(
    path='report.pdf',
    mode='single',
    extract='plain',
    include=False,
    format='markdown-img',
    size=1000,
    overlap=150,
    has_tables=True
)

# Pass `documents` to the embedding/vector/retrieval layer used by your application.
```

## Composition Rule

Do not assume two providers use the same units, coordinate ordering, date semantics, metadata keys, or
quality controls merely because their results are both Python dictionaries.
