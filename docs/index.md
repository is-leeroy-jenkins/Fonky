![](images/fonky-project.png)

___

Fonky is a modular external-data framework organized around three execution modules:

- `fetchers.py` for provider-backed retrieval,
- `loaders.py` for source ingestion and document construction,
- `scrapers.py` for synchronous HTML extraction.

The public surface is split into two layers:

1. `fonky.py` — 110 literal `@tool(...)` exports.
2. `tools.py` — domain grouping and discovery helpers for the exported tools.

![Fonky Overview](images/fonky_project.png)

---

## Public Domains

| Domain          | Operations | Examples                                                                                                                                           |
|-----------------|-----------:|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `archives`      |         11 | `fetch_arxiv, fetch_google_drive, fetch_wikipedia, fetch_news ...`                                                                                 |
| `astronomical`  |         10 | `fetch_naval_observatory, fetch_satellite_center, fetch_nearby_objects, fetch_open_science ...`                                                    |
| `cloud`         |          8 | `load_google_drive_file, load_google_drive_folder, load_onedrive, load_google_cloud_file ...`                                                      |
| `demographic`   |          5 | `fetch_census_data, fetch_socrata, fetch_united_nations, fetch_world_population ...`                                                               |
| `documents`     |         18 | `load_text, load_csv, read_pdf, load_pdf ...`                                                                                                      |
| `environmental` |         19 | `fetch_google_weather_current, fetch_google_weather_hourly_forecast, fetch_google_weather_daily_forecast, fetch_google_weather_hourly_history ...` |
| `geospatial`    |         10 | `geocode_location, geocode_coordinates, validate_address, request_directions ...`                                                                  |
| `health`        |          4 | `fetch_health_data, fetch_global_health_data, fetch_wonder, load_pubmed`                                                                           |
| `web`           |         25 | `fetch_web_page, convert_html_to_text, extract_web_title, extract_web_links ...`                                                                   |

## Core Surfaces

| Surface                 | Role                     | Primary Use                                                    |
|-------------------------|--------------------------|----------------------------------------------------------------|
| `fonky.py`              | Public tool exports      | Direct `.invoke(...)` execution or agent-ready tool imports    |
| `tools.py`              | Tool discovery           | `get_domains()`, `get_tools(domain)`, `get_tool_names(domain)` |
| `fetchers.py`           | Retrieval implementation | APIs, remote services, public data, search, weather, maps      |
| `loaders.py`            | Ingestion implementation | Files, notebooks, cloud sources, recursive web loading         |
| `scrapers.py`           | Structured extraction    | Headings, paragraphs, links, tables, images, sections          |
| `models.py`             | Data contracts           | shared schemas and tool definition helpers                     |
| `processors.py`         | Transformation utilities | text cleanup, parsing, chunking support                        |
| `core.py` / `config.py` | Support infrastructure   | errors, configuration, runtime utilities                       |

## Representative Paths

```python
from fonky.fonky import fetch_arxiv

result = fetch_arxiv.invoke(
    {
        'question': 'retrieval augmented generation',
        'max_documents': 5,
        'full_documents': False,
        'include_metadata': True
    }
)
```

```python
from fonky.tools import get_tools

environmental_tools = get_tools( domain='environmental' )
```

## Documentation Map

- **Getting Started** — install, validate, execute first tool.
- **User Guide** — task-oriented usage patterns.
- **Guides** — domain-specific operation references.
- **API Reference** — module and source-level API docs via `mkdocstrings`.
- **Development** — extension standards, tests, contribution rules.
