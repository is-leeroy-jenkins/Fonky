# Demographic & Public Data

This domain covers U.S. Census, Socrata, United Nations data, world-population catalog assets, and
municipal/open-city datasets.

## Workflow — Census Variables and Data

Discover variables first when you do not know field names:

```python
from fonky import fonky

variables = fonky.fetch_census_data(
    mode='variables',
    year='2022',
    dataset='acs/acs5'
)
```

Then request data with explicit fields and geography:

```python
records = fonky.fetch_census_data(
    mode='data',
    year='2022',
    dataset='acs/acs5',
    fields='NAME,B01001_001E',
    geography_for='state:*'
)
```

## Workflow — Socrata Query

```python
from fonky import fonky

rows = fonky.fetch_socrata(
    mode='rows',
    domain='data.cdc.gov',
    dataset_id='dataset-id',
    select='state,count(*) as total',
    where="year >= 2024",
    group='state',
    order='total DESC',
    limit=100
)
```

Socrata query clauses are provider syntax. Validate queries against the target dataset's schema rather
than assuming fields are portable between datasets.

## Workflow — United Nations Dataset Discovery

```python
from fonky import fonky

datasets = fonky.fetch_united_nations(
    mode='datasets'
)
```

Use the returned dataset metadata to construct the provider-specific `query_path` for subsequent
requests.

## Operational Notes

- Public-data datasets change independently of Fonky.
- Schema discovery is often the first step for Census/Socrata/UN workflows.
- Pagination/limits should be intentional; avoid requesting an entire large dataset when a filtered
  query will do.
