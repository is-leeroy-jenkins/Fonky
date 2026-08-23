# Fonky

Fonky is a Python framework for retrieving, loading, extracting, and preparing information from local files, web pages, public APIs, scientific services, cloud platforms, government datasets, research repositories, and structured data providers.

The framework exposes two complementary interfaces: a flat functional API in `fonky.py` and direct implementation classes in `fetchers.py`, `loaders.py`, and `scrapers.py`.

## What Fonky Can Do

| Domain | Operations | Representative Functions |
|---|---:|---|
| Archives | 11 | `fetch_arxiv()`, `fetch_google_drive()`, `fetch_wikipedia()`, `fetch_news()` |
| Astronomical | 10 | `fetch_naval_observatory()`, `fetch_satellite_center()`, `fetch_nearby_objects()`, `fetch_open_science()` |
| Cloud | 8 | `load_google_drive_file()`, `load_google_drive_folder()`, `load_onedrive()`, `load_google_cloud_file()` |
| Demographic | 5 | `fetch_census_data()`, `fetch_socrata()`, `fetch_united_nations()`, `fetch_world_population()` |
| Documents | 18 | `load_text()`, `load_csv()`, `read_pdf()`, `load_pdf()` |
| Environmental | 19 | `fetch_google_weather_current()`, `fetch_google_weather_hourly_forecast()`, `fetch_google_weather_daily_forecast()`, `fetch_google_weather_hourly_history()` |
| Geospatial | 10 | `geocode_location()`, `geocode_coordinates()`, `validate_address()`, `request_directions()` |
| Health | 4 | `fetch_health_data()`, `fetch_global_health_data()`, `fetch_wonder()`, `load_pubmed()` |
| Web | 25 | `fetch_web_page()`, `convert_html_to_text()`, `extract_web_title()`, `extract_web_links()` |

## Start Here

- [Getting Started](getting-started.md) — install, configure, and run first calls.
- [User Guide](user-guide.md) — task-oriented workflows across every domain.
- [Architecture](architecture.md) — execution, state, validation, results, and error boundaries.
- [Troubleshooting](troubleshooting.md) — dependency, provider, file, network, and validation failures.
- [Functional API](api/fonky.md) — exhaustive reference for every wrapper.
- [Development](development/index.md) — extending fetchers, loaders, scrapers, and wrappers.

## Core Capability Families

### Document ingestion

The loader layer centralizes ingestion into LangChain `Document` objects for local files, Office documents, structured data, notebooks, email, cloud storage, repositories, public research sources, and web content. Loaded documents can be split into smaller chunks for retrieval and embedding workflows.

### Web extraction

`WebExtractor` supports whole-page retrieval plus structural extraction for paragraphs, lists, tables, articles, headings, divisions, sections, blockquotes, hyperlinks, and image references.

### Remote/public data

Fetchers cover archives, government data, search, weather, climate, environmental monitoring, geospatial services, astronomy, aviation, demographics, public health, and research sources.
