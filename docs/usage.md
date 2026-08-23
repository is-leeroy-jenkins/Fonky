# Usage

This page provides practical examples across the current functional domains. Provider calls require the dependencies, credentials, and network access expected by their implementations.

## Archives

```python
from fonky import fonky

papers = fonky.fetch_arxiv(
    question='retrieval augmented generation',
    max_documents=5,
    full_documents=False,
    include_metadata=True
)
```

```python
results = fonky.fetch_google_search(
    question='USGS earthquake data',
    exact_terms='', exclude_terms='', file_type='', date_restrict='',
    site_search='usgs.gov', site_search_filter='i', image_search=False,
    country='', language='lang_en', safe='off', max_results=10
)
```

## Astronomical

![Astronomy and Space](images/fonky-astro-space.png)

Use the astronomical wrappers for Naval Observatory, satellite, near-Earth object, NASA Open Science, space-weather, catalog, query, map, and chart operations. Their exact signatures are documented in [API Reference: `fonky.py`](api/fonky.md).

## Cloud

Cloud loaders may require SDK credentials, project identifiers, bucket/container identifiers, or authentication files. Use the wrapper signature and underlying loader reference together when configuring a cloud integration.

## Demographic

```python
from fonky import fonky

data = fonky.fetch_census_data(
    mode='data', dataset='acs/acs5', year=2024,
    get='NAME,B01001_001E', predicates='for=state:*', api_key=''
)
```

## Documents

```python
from fonky import fonky

documents = fonky.load_text(
    path='sample.txt', encoding='utf-8', size=1000, overlap=100, chunk=False
)
```

```python
documents = fonky.load_pdf(
    path='sample.pdf', mode='single', extract='plain', include=False,
    format='markdown-img', size=1000, overlap=150, has_tables=True
)
```

## Environmental

![Environmental and Geospatial](images/fonky-enviro-geo-climate.png)

```python
from fonky import fonky

current = fonky.fetch_google_weather_current(
    address='Arlington, VA', units_system='METRIC', language_code='en', time=10
)
```

```python
earthquakes = fonky.fetch_usgs_earthquakes(
    mode='feed', feed='all_day.geojson', min_magnitude=1.0, limit=25
)
```

## Geospatial

```python
from fonky import fonky

location = fonky.geocode_location(
    address='1600 Pennsylvania Avenue NW, Washington, DC'
)
```

## Health

![Government, Demographic, and Health](images/fonky-gov-demo-health.png)

Health wrappers cover HealthData, global health, CDC WONDER, and PubMed-backed loading. Consult the functional API for exact current signatures.

## Web

```python
from fonky import fonky

page = fonky.fetch_web_page(url='https://example.com', time=10)
tables = fonky.scrape_tables(uri='https://example.com')
links = fonky.scrape_hyperlinks(uri='https://example.com')
```

## Direct Class Usage

```python
from fonky.fetchers import GoogleWeather

weather = GoogleWeather( )
result = weather.fetch_current(
    address='Arlington, VA', units_system='METRIC', language_code='en', time=10
)
```

## Results

Wrappers return underlying implementation results directly. Common shapes include dictionaries, lists, strings, document collections, tabular structures, and provider-native payloads. There is no universal wrapper envelope.

## Errors

Use normal Python exception handling around operations that depend on files, networks, credentials, or external services.
