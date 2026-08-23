# Health Data

Fonky exposes HealthData/Socrata-style public-health data, global-health indicators, CDC WONDER, and
PubMed document search.

## Workflow — HealthData Rows

```python
from fonky import fonky

rows = fonky.fetch_health_data(
    mode='rows',
    domain='healthdata.gov',
    dataset_id='dataset-id',
    select='*',
    where='',
    order='',
    limit=25,
    offset=0
)
```

Dataset IDs and fields are source-specific. Discover and validate the target dataset before building a
complex query.

## Workflow — Global Health Indicator Registry

```python
indicators = fonky.fetch_global_health_data(
    mode='indicator_registry',
    fmt='json'
)
```

Use registry/discovery output before constructing provider-specific query paths.

## Workflow — CDC WONDER

```python
from fonky import fonky

template = fonky.fetch_wonder(
    mode='metadata_template',
    dataset_id='D76'
)
```

The WONDER implementation supports metadata/template and query submission modes. Build request XML
against the dataset contract rather than guessing field names.

## Workflow — PubMed

```python
papers = fonky.load_pubmed(
    query='machine learning environmental health',
    max_docs=10
)
```

PubMed loading is useful when the next workflow expects document objects rather than raw provider
records.

## Data Responsibility

Public-health and medical datasets can contain complex definitions, revisions, suppression rules,
provisional observations, and population denominators. Fonky retrieves data; it does not replace
source methodology or subject-matter interpretation.
