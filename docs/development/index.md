# Development

## Development Objectives

- keep public surfaces thin,
- keep implementation logic in source modules,
- keep docstrings parseable and semantically useful,
- keep API docs source-driven,
- keep domain grouping explicit and testable.

## Change Areas

| Change | Primary File |
|---|---|
| new provider-backed retrieval | `fetchers.py` |
| new ingestion path | `loaders.py` |
| new HTML extraction behavior | `scrapers.py` |
| new public export | `fonky.py` |
| new domain grouping | `tools.py` |
| new schema/helper type | `models.py` or `processors.py` |
| new config hook | `config.py` |
