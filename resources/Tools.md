# 🧰 Fonky Tools

## 📊 Inventory

| Property | Value |
|---|---:|
| OpenAI Agents SDK `FunctionTool` objects | 150 |
| Retrieval, loading, and scraping tools | 110 |
| Preprocessing and NLTK tools | 40 |

## 📥 Import Pattern

```python
from fonky.tools import fetch_arxiv
from fonky.tools import load_pdf
from fonky.tools import preprocess_normalize_text
from fonky.tools import scrape_tables
```

## 🤖 Agent Pattern

```python
from agents import Agent, Runner

from fonky.tools import fetch_arxiv

agent = Agent(
    name='Research Assistant',
    tools=[
        fetch_arxiv,
    ] )

result = Runner.run_sync(
    agent,
    'Research retrieval augmented generation.' )

print( result.final_output )
```

## 📚 Tool Index

| # | Tool |
|---:|---|
| 1 | [`convert_html_to_text()`](#convert_html_to_text) |
| 2 | [`crawl_web()`](#crawl_web) |
| 3 | [`encode_image()`](#encode_image) |
| 4 | [`extract_web_links()`](#extract_web_links) |
| 5 | [`extract_web_structured_data()`](#extract_web_structured_data) |
| 6 | [`extract_web_title()`](#extract_web_title) |
| 7 | [`fetch_air_now()`](#fetch_air_now) |
| 8 | [`fetch_arxiv()`](#fetch_arxiv) |
| 9 | [`fetch_astro_catalog()`](#fetch_astro_catalog) |
| 10 | [`fetch_astro_query()`](#fetch_astro_query) |
| 11 | [`fetch_census_data()`](#fetch_census_data) |
| 12 | [`fetch_climate_data()`](#fetch_climate_data) |
| 13 | [`fetch_congress()`](#fetch_congress) |
| 14 | [`fetch_earth_observatory()`](#fetch_earth_observatory) |
| 15 | [`fetch_envirofacts()`](#fetch_envirofacts) |
| 16 | [`fetch_eonet()`](#fetch_eonet) |
| 17 | [`fetch_firms()`](#fetch_firms) |
| 18 | [`fetch_global_health_data()`](#fetch_global_health_data) |
| 19 | [`fetch_global_imagery_map_services()`](#fetch_global_imagery_map_services) |
| 20 | [`fetch_global_imagery_mercator_map()`](#fetch_global_imagery_mercator_map) |
| 21 | [`fetch_global_imagery_wms_map()`](#fetch_global_imagery_wms_map) |
| 22 | [`fetch_google_drive()`](#fetch_google_drive) |
| 23 | [`fetch_google_geocoding()`](#fetch_google_geocoding) |
| 24 | [`fetch_google_search()`](#fetch_google_search) |
| 25 | [`fetch_google_weather_alerts()`](#fetch_google_weather_alerts) |
| 26 | [`fetch_google_weather_current()`](#fetch_google_weather_current) |
| 27 | [`fetch_google_weather_daily_forecast()`](#fetch_google_weather_daily_forecast) |
| 28 | [`fetch_google_weather_hourly_forecast()`](#fetch_google_weather_hourly_forecast) |
| 29 | [`fetch_google_weather_hourly_history()`](#fetch_google_weather_hourly_history) |
| 30 | [`fetch_gov_data()`](#fetch_gov_data) |
| 31 | [`fetch_grokipedia()`](#fetch_grokipedia) |
| 32 | [`fetch_health_data()`](#fetch_health_data) |
| 33 | [`fetch_historical_weather()`](#fetch_historical_weather) |
| 34 | [`fetch_internet_archive()`](#fetch_internet_archive) |
| 35 | [`fetch_naval_observatory()`](#fetch_naval_observatory) |
| 36 | [`fetch_nearby_objects()`](#fetch_nearby_objects) |
| 37 | [`fetch_news()`](#fetch_news) |
| 38 | [`fetch_open_aq()`](#fetch_open_aq) |
| 39 | [`fetch_open_science()`](#fetch_open_science) |
| 40 | [`fetch_open_sky()`](#fetch_open_sky) |
| 41 | [`fetch_open_weather()`](#fetch_open_weather) |
| 42 | [`fetch_purple_air()`](#fetch_purple_air) |
| 43 | [`fetch_satellite_center()`](#fetch_satellite_center) |
| 44 | [`fetch_socrata()`](#fetch_socrata) |
| 45 | [`fetch_space_weather()`](#fetch_space_weather) |
| 46 | [`fetch_star_chart()`](#fetch_star_chart) |
| 47 | [`fetch_star_map()`](#fetch_star_map) |
| 48 | [`fetch_tides_and_currents()`](#fetch_tides_and_currents) |
| 49 | [`fetch_united_nations()`](#fetch_united_nations) |
| 50 | [`fetch_usgs_earthquakes()`](#fetch_usgs_earthquakes) |
| 51 | [`fetch_usgs_national_map()`](#fetch_usgs_national_map) |
| 52 | [`fetch_usgs_sciencebase()`](#fetch_usgs_sciencebase) |
| 53 | [`fetch_usgs_water_data()`](#fetch_usgs_water_data) |
| 54 | [`fetch_uv_index()`](#fetch_uv_index) |
| 55 | [`fetch_web_page()`](#fetch_web_page) |
| 56 | [`fetch_wikipedia()`](#fetch_wikipedia) |
| 57 | [`fetch_wonder()`](#fetch_wonder) |
| 58 | [`fetch_world_population()`](#fetch_world_population) |
| 59 | [`geocode_coordinates()`](#geocode_coordinates) |
| 60 | [`geocode_location()`](#geocode_location) |
| 61 | [`load_arxiv()`](#load_arxiv) |
| 62 | [`load_aws_bucket()`](#load_aws_bucket) |
| 63 | [`load_aws_file()`](#load_aws_file) |
| 64 | [`load_csv()`](#load_csv) |
| 65 | [`load_email()`](#load_email) |
| 66 | [`load_excel()`](#load_excel) |
| 67 | [`load_github()`](#load_github) |
| 68 | [`load_google_bucket()`](#load_google_bucket) |
| 69 | [`load_google_cloud_file()`](#load_google_cloud_file) |
| 70 | [`load_google_drive_file()`](#load_google_drive_file) |
| 71 | [`load_google_drive_folder()`](#load_google_drive_folder) |
| 72 | [`load_google_speech_to_text()`](#load_google_speech_to_text) |
| 73 | [`load_html()`](#load_html) |
| 74 | [`load_json()`](#load_json) |
| 75 | [`load_jupyter_notebook()`](#load_jupyter_notebook) |
| 76 | [`load_markdown()`](#load_markdown) |
| 77 | [`load_onedrive()`](#load_onedrive) |
| 78 | [`load_open_city()`](#load_open_city) |
| 79 | [`load_outlook()`](#load_outlook) |
| 80 | [`load_pdf()`](#load_pdf) |
| 81 | [`load_powerpoint()`](#load_powerpoint) |
| 82 | [`load_powerpoint_multiple()`](#load_powerpoint_multiple) |
| 83 | [`load_pubmed()`](#load_pubmed) |
| 84 | [`load_spfx()`](#load_spfx) |
| 85 | [`load_spfx_folder()`](#load_spfx_folder) |
| 86 | [`load_text()`](#load_text) |
| 87 | [`load_web()`](#load_web) |
| 88 | [`load_web_pages()`](#load_web_pages) |
| 89 | [`load_web_recursive()`](#load_web_recursive) |
| 90 | [`load_wikipedia()`](#load_wikipedia) |
| 91 | [`load_word()`](#load_word) |
| 92 | [`load_xml()`](#load_xml) |
| 93 | [`load_xml_tree()`](#load_xml_tree) |
| 94 | [`nltk_chunk_sentences()`](#nltk_chunk_sentences) |
| 95 | [`nltk_chunk_words()`](#nltk_chunk_words) |
| 96 | [`nltk_named_entity_recognition()`](#nltk_named_entity_recognition) |
| 97 | [`nltk_pos_tagger()`](#nltk_pos_tagger) |
| 98 | [`nltk_sentence_tokenizer()`](#nltk_sentence_tokenizer) |
| 99 | [`nltk_word_lemmatizer()`](#nltk_word_lemmatizer) |
| 100 | [`nltk_word_stemmer()`](#nltk_word_stemmer) |
| 101 | [`nltk_word_tokenizer()`](#nltk_word_tokenizer) |
| 102 | [`preprocess_chunk_data()`](#preprocess_chunk_data) |
| 103 | [`preprocess_chunk_datasets()`](#preprocess_chunk_datasets) |
| 104 | [`preprocess_chunk_files()`](#preprocess_chunk_files) |
| 105 | [`preprocess_clean_file()`](#preprocess_clean_file) |
| 106 | [`preprocess_clean_files()`](#preprocess_clean_files) |
| 107 | [`preprocess_collapse_whitespace()`](#preprocess_collapse_whitespace) |
| 108 | [`preprocess_convert_jsonl()`](#preprocess_convert_jsonl) |
| 109 | [`preprocess_create_frequency_distribution()`](#preprocess_create_frequency_distribution) |
| 110 | [`preprocess_create_vectors()`](#preprocess_create_vectors) |
| 111 | [`preprocess_create_vocabulary()`](#preprocess_create_vocabulary) |
| 112 | [`preprocess_create_wordbag()`](#preprocess_create_wordbag) |
| 113 | [`preprocess_encode_sentences()`](#preprocess_encode_sentences) |
| 114 | [`preprocess_load_text()`](#preprocess_load_text) |
| 115 | [`preprocess_normalize_text()`](#preprocess_normalize_text) |
| 116 | [`preprocess_remove_encodings()`](#preprocess_remove_encodings) |
| 117 | [`preprocess_remove_errors()`](#preprocess_remove_errors) |
| 118 | [`preprocess_remove_fragments()`](#preprocess_remove_fragments) |
| 119 | [`preprocess_remove_headers()`](#preprocess_remove_headers) |
| 120 | [`preprocess_remove_html()`](#preprocess_remove_html) |
| 121 | [`preprocess_remove_images()`](#preprocess_remove_images) |
| 122 | [`preprocess_remove_markdown()`](#preprocess_remove_markdown) |
| 123 | [`preprocess_remove_numbers()`](#preprocess_remove_numbers) |
| 124 | [`preprocess_remove_numerals()`](#preprocess_remove_numerals) |
| 125 | [`preprocess_remove_punctuation()`](#preprocess_remove_punctuation) |
| 126 | [`preprocess_remove_stopwords()`](#preprocess_remove_stopwords) |
| 127 | [`preprocess_remove_symbols()`](#preprocess_remove_symbols) |
| 128 | [`preprocess_remove_xml()`](#preprocess_remove_xml) |
| 129 | [`preprocess_semantic_search()`](#preprocess_semantic_search) |
| 130 | [`preprocess_split_pages()`](#preprocess_split_pages) |
| 131 | [`preprocess_split_paragraphs()`](#preprocess_split_paragraphs) |
| 132 | [`preprocess_split_sentences()`](#preprocess_split_sentences) |
| 133 | [`preprocess_tiktokenize()`](#preprocess_tiktokenize) |
| 134 | [`read_pdf()`](#read_pdf) |
| 135 | [`render_web_page()`](#render_web_page) |
| 136 | [`request_directions()`](#request_directions) |
| 137 | [`scrape_articles()`](#scrape_articles) |
| 138 | [`scrape_blockquotes()`](#scrape_blockquotes) |
| 139 | [`scrape_crawler_page()`](#scrape_crawler_page) |
| 140 | [`scrape_divisions()`](#scrape_divisions) |
| 141 | [`scrape_headings()`](#scrape_headings) |
| 142 | [`scrape_hyperlinks()`](#scrape_hyperlinks) |
| 143 | [`scrape_images()`](#scrape_images) |
| 144 | [`scrape_lists()`](#scrape_lists) |
| 145 | [`scrape_paragraphs()`](#scrape_paragraphs) |
| 146 | [`scrape_sections()`](#scrape_sections) |
| 147 | [`scrape_tables()`](#scrape_tables) |
| 148 | [`scrape_web_page()`](#scrape_web_page) |
| 149 | [`scraper_html_to_text()`](#scraper_html_to_text) |
| 150 | [`validate_address()`](#validate_address) |

## 🧩 API Reference

### 🔧 convert_html_to_text

**Index:** 1

```python
def convert_html_to_text( html: str ) -> Any
```

Convert HTML to plain text.

#### 🎯 Purpose

Convert HTML to plain text using Fonky's web fetcher implementation.

#### 📥 Arguments

- `html`
  - Raw HTML content to parse or transform.

#### 📤 Returns

str: Text produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 crawl_web

**Index:** 2

```python
def crawl_web( seed_url: str, include_title: bool=True, include_basic_text: bool=True, include_raw_html: bool=False, selected_methods: Optional[List[str]]=None, recursive: bool=False, max_depth: int=1, max_pages: int=10, same_domain_only: bool=True, request_timeout: int=10, delay_seconds: float=0.25, max_bytes: int=1000000, headers: Optional[Dict[str, str]]=None, use_playwright: bool=False ) -> Any
```

Crawl web pages from a seed URL.

#### 🎯 Purpose

Crawl web pages from a seed URL. Boolean options control retrieval depth or supplemental
    content.

#### 📥 Arguments

- `seed_url`
  - Starting URL for the crawl.
- `include_title`
  - Whether to include title in the result.
- `include_basic_text`
  - Whether to include basic text in the result.
- `include_raw_html`
  - Whether to include raw html in the result.
- `selected_methods`
  - Extraction method names to execute against the supplied HTML.
- `recursive`
  - Whether nested folders, links, or provider resources should be traversed.
- `max_depth`
  - Maximum recursion depth.
- `max_pages`
  - Maximum pages permitted by the operation.
- `same_domain_only`
  - Whether crawl traversal should remain on the seed URL domain.
- `request_timeout`
  - Request timeout in seconds.
- `delay_seconds`
  - Delay in seconds inserted between crawl requests.
- `max_bytes`
  - Maximum bytes permitted by the operation.
- `headers`
  - Optional HTTP headers applied to web requests.
- `use_playwright`
  - Whether browser-backed rendering should be used for dynamic pages.

#### 📤 Returns

Dict[str, Any]: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 encode_image

**Index:** 3

```python
def encode_image( path: str ) -> str
```

Encode a local image as Base64 text.

#### 🎯 Purpose

Encode a local image as Base64 text using Fonky's provider implementation.

#### 📥 Arguments

- `path`
  - Local image path to encode.

#### 📤 Returns

str: Text produced by the operation.

#### ⚠️ Raises

Exception: If the delegated implementation raises an operational failure.

---

### 🔧 extract_web_links

**Index:** 4

```python
def extract_web_links( base_url: str, html: str ) -> Any
```

Extract web links from the supplied content.

#### 🎯 Purpose

Extract web links from the supplied content using Fonky's web fetcher implementation.

#### 📥 Arguments

- `base_url`
  - URL or URI value used as the request or parsing source.
- `html`
  - Raw HTML content to parse or transform.

#### 📤 Returns

List[str]: Hyperlink values produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 extract_web_structured_data

**Index:** 5

```python
def extract_web_structured_data( url: str, html: str, selected_methods: Optional[List[str]]=None ) -> Any
```

Extract structured data.

#### 🎯 Purpose

Extract structured data using Fonky's web fetcher implementation.

#### 📥 Arguments

- `url`
  - URL or URI value used as the request or parsing source.
- `html`
  - Raw HTML content to parse or transform.
- `selected_methods`
  - Extraction method names to execute against the supplied HTML.

#### 📤 Returns

Dict[str, List[str]]: Text or identifier values produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 extract_web_title

**Index:** 6

```python
def extract_web_title( html: str ) -> Any
```

Extract web title from the supplied content.

#### 🎯 Purpose

Extract web title from the supplied content using Fonky's web fetcher implementation.

#### 📥 Arguments

- `html`
  - Raw HTML content to parse or transform.

#### 📤 Returns

str: Text produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_air_now

**Index:** 7

```python
def fetch_air_now( mode: str='current-zip', zip_code: str='', latitude: float | None=None, longitude: float | None=None, date: str='', distance: int=25, time: int=20 ) -> Any
```

Retrieve AirNow current and forecast air quality data.

#### 🎯 Purpose

Retrieve AirNow current and forecast air quality data through AirNow. Use ``mode`` to select
    among ``current-latlon``, ``current-zip``, ``forecast-latlon``, ``forecast-zip``. Coordinate
    and bounding arguments constrain geographic scope when supported.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``current- latlon``, ``current-zip``, ``forecast-latlon``, ``forecast-zip``.
- `zip_code`
  - Provider code identifying or filtering zip.
- `latitude`
  - Latitude in decimal degrees.
- `longitude`
  - Longitude in decimal degrees.
- `date`
  - Date used by the provider or processing operation.
- `distance`
  - Maximum provider search distance, using the units defined by that service.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_arxiv

**Index:** 8

```python
def fetch_arxiv( question: str, max_documents: int | None=None, full_documents: bool | None=None, include_metadata: bool | None=None ) -> Any
```

Retrieve ArXiv research documents.

#### 🎯 Purpose

Retrieve ArXiv research documents through ArXiv. The query text determines the records or
    documents matched by the provider. Result-count arguments bound the amount of data
    requested. Boolean options control retrieval depth or supplemental content.

#### 📥 Arguments

- `question`
  - Search text, lookup value, or provider query submitted by the caller.
- `max_documents`
  - Maximum number of documents to retrieve.
- `full_documents`
  - Whether to retrieve full document content instead of abbreviated search results.
- `include_metadata`
  - Whether provider metadata should be included with retrieved content.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_astro_catalog

**Index:** 9

```python
def fetch_astro_catalog( mode: str='object_query', query: str='', quantity: str='', attributes: str='', arguments: str='', ra: str='', dec: str='', radius: int=2, data_format: str='json', time: int=20 ) -> Any
```

Retrieve Open Astronomy Catalog queries.

#### 🎯 Purpose

Retrieve Open Astronomy Catalog queries through Open Astronomy Catalog. The query text
    determines the records or documents matched by the provider.

#### 📥 Arguments

- `mode`
  - Operation mode used to select the provider or processing workflow.
- `query`
  - Search text, lookup value, or provider query submitted by the caller.
- `quantity`
  - Provider quantity or field requested from the catalog.
- `attributes`
  - Provider attributes requested for matching catalog records.
- `arguments`
  - Keyword arguments passed to the bound callable.
- `ra`
  - Right ascension value.
- `dec`
  - Declination value.
- `radius`
  - Search radius in the units specified by the operation.
- `data_format`
  - Provider output data format.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Any: Provider-specific structured data produced by the retrieval operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_astro_query

**Index:** 10

```python
def fetch_astro_query( mode: str='object_search', query: str='', ra: str='', dec: str='', radius: float=0.5, radius_unit: str='deg', row_limit: int=100 ) -> Any
```

Retrieve Simbad and astronomy object search operations.

#### 🎯 Purpose

Retrieve Simbad and astronomy object search operations through Astroquery/SIMBAD. The query
    text determines the records or documents matched by the provider. Result-count arguments
    bound the amount of data requested.

#### 📥 Arguments

- `mode`
  - Operation mode used to select the provider or processing workflow.
- `query`
  - Search text, lookup value, or provider query submitted by the caller.
- `ra`
  - Right ascension value.
- `dec`
  - Declination value.
- `radius`
  - Search radius in the units specified by the operation.
- `radius_unit`
  - Unit applied to the search radius.
- `row_limit`
  - Maximum number of rows returned by the astronomy query.

#### 📤 Returns

Dict[str, Any]: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_census_data

**Index:** 11

```python
def fetch_census_data( mode: str='variables', year: str='2022', dataset: str='acs/acs5', fields: str='NAME,B01001_001E', geography_for: str='state:*', geography_in: str='', predicates: str='', time: int=20 ) -> Any
```

Retrieve U.S. Census dataset and variable.

#### 🎯 Purpose

Retrieve U.S. Census dataset and variable through U.S. Census API. Use ``mode`` to select
    among ``data``, ``variables``.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``data``, ``variables``.
- `year`
  - Dataset or observation year requested from the provider.
- `dataset`
  - Provider dataset name or identifier.
- `fields`
  - Comma-separated or provider-specific field selection.
- `geography_for`
  - Census ``for`` geography clause defining the requested geography.
- `geography_in`
  - Optional Census ``in`` geography clause constraining the request.
- `predicates`
  - Additional Census query predicates appended to the request.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_climate_data

**Index:** 12

```python
def fetch_climate_data( mode: str='datasets', keyword: str='', dataset: str='', start_date: str='', end_date: str='', stations: str='', data_types: str='', limit: int=25, offset: int=0, time: int=20 ) -> Any
```

Retrieve NOAA climate dataset and data records.

#### 🎯 Purpose

Retrieve NOAA climate dataset and data records through NOAA climate services. Use ``mode``
    to select among ``data``, ``datasets``. Date and time arguments constrain the requested
    interval when supplied. Result-count arguments bound the amount of data requested.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``data``, ``datasets``.
- `keyword`
  - Keyword used to filter provider records.
- `dataset`
  - Provider dataset name or identifier.
- `start_date`
  - Inclusive start date for the requested time range, in the provider-supported format.
- `end_date`
  - Inclusive end date for the requested time range, in the provider-supported format.
- `stations`
  - Station identifiers used to restrict climate observations.
- `data_types`
  - Climate data-type identifiers requested from the provider.
- `limit`
  - Maximum number of records or items to return.
- `offset`
  - Zero-based result offset used for pagination.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_congress

**Index:** 13

```python
def fetch_congress( mode: str='congresses', congress: int=0, bill_type: str='', bill_number: int=0, law_type: str='', law_number: int=0, report_type: str='', report_number: int=0, offset: int=0, limit: int=20, sort: str='updateDate+desc', from_date_time: str='', to_date_time: str='', conference: bool=False, time: int=20 ) -> Any
```

Retrieve Congress.gov legislative data.

#### 🎯 Purpose

Retrieve Congress.gov legislative data through Congress.gov. Use ``mode`` to select among
    ``bill_detail``, ``bills``, ``congresses``, ``law_detail``, ``laws``, ``report_detail``,
    ``reports``. Date and time arguments constrain the requested interval when supplied. Result-
    count arguments bound the amount of data requested.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``bill_detail``, ``bills``, ``congresses``, ``law_detail``, ``laws``, ``report_detail``, ``reports``.
- `congress`
  - Congress number used to scope legislative records.
- `bill_type`
  - Provider type selector for bill.
- `bill_number`
  - Legislative bill number used with the selected Congress and bill type.
- `law_type`
  - Provider type selector for law.
- `law_number`
  - Public or private law number used with the selected law type.
- `report_type`
  - Provider type selector for report.
- `report_number`
  - Committee report number used with the selected Congress and report type.
- `offset`
  - Zero-based result offset used for pagination.
- `limit`
  - Maximum number of records or items to return.
- `sort`
  - Provider-supported result ordering expression.
- `from_date_time`
  - Earliest provider update timestamp to include.
- `to_date_time`
  - Latest provider update timestamp to include.
- `conference`
  - Whether to restrict committee reports to conference reports.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_earth_observatory

**Index:** 14

```python
def fetch_earth_observatory( mode: str='events', status: str='open', category: str='', source: str='', limit: int=20, days: int=30, start_date: str='', end_date: str='', time: int=20 ) -> Any
```

Retrieve NASA EONET events, categories, sources, and layers.

#### 🎯 Purpose

Retrieve NASA EONET events, categories, sources, and layers through NASA EONET. Date and
    time arguments constrain the requested interval when supplied. Result-count arguments bound
    the amount of data requested.

#### 📥 Arguments

- `mode`
  - Operation mode used to select the provider or processing workflow.
- `status`
  - Provider status filter applied to returned records.
- `category`
  - Optional logical category retained in tool metadata.
- `source`
  - Provider source identifier used to restrict or classify results.
- `limit`
  - Maximum number of records or items to return.
- `days`
  - Number of calendar days included in the requested interval.
- `start_date`
  - Inclusive start date for the requested time range, in the provider-supported format.
- `end_date`
  - Inclusive end date for the requested time range, in the provider-supported format.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any]: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_envirofacts

**Index:** 15

```python
def fetch_envirofacts( table_name: str='TRI_FACILITY', state_code: str='', facility_name: str='', limit: int=25, time: int=20 ) -> Any
```

Retrieve EPA Envirofacts table and facility records.

#### 🎯 Purpose

Retrieve EPA Envirofacts table and facility records through EPA Envirofacts. Result-count
    arguments bound the amount of data requested.

#### 📥 Arguments

- `table_name`
  - Envirofacts table or resource name to query.
- `state_code`
  - State code used to restrict provider records.
- `facility_name`
  - Facility-name filter applied to Envirofacts records.
- `limit`
  - Maximum number of records or items to return.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_eonet

**Index:** 16

```python
def fetch_eonet( mode: str='events', source: str='', category: str='', status: str='open', limit: int=25, days: int=30, start_date: str='', end_date: str='', bbox: str='', time: int=20 ) -> Any
```

Retrieve NASA EONET environmental event data.

#### 🎯 Purpose

Retrieve NASA EONET environmental event data through NASA EONET. Use ``mode`` to select
    among ``categories``, ``events``. Date and time arguments constrain the requested interval
    when supplied. Coordinate and bounding arguments constrain geographic scope when supported.
    Result-count arguments bound the amount of data requested.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``categories``, ``events``.
- `source`
  - Provider source identifier used to restrict or classify results.
- `category`
  - Optional logical category retained in tool metadata.
- `status`
  - Provider status filter applied to returned records.
- `limit`
  - Maximum number of records or items to return.
- `days`
  - Number of calendar days included in the requested interval.
- `start_date`
  - Inclusive start date for the requested time range, in the provider-supported format.
- `end_date`
  - Inclusive end date for the requested time range, in the provider-supported format.
- `bbox`
  - Bounding box defining the geographic extent of the request.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_firms

**Index:** 17

```python
def fetch_firms( mode: str='area', source: str='VIIRS_SNPP_NRT', area_coordinates: str='world', day_range: int=1, date: str='', sensor: str='ALL', time: int=20 ) -> Any
```

Retrieve NASA FIRMS active fire data.

#### 🎯 Purpose

Retrieve NASA FIRMS active fire data through NASA FIRMS. Use ``mode`` to select among
    ``area``, ``data-availability``.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``area``, ``data-availability``.
- `source`
  - Provider source identifier used to restrict or classify results.
- `area_coordinates`
  - FIRMS area-of-interest coordinates or ``world`` selector.
- `day_range`
  - Number of days included in the FIRMS active-fire request.
- `date`
  - Date used by the provider or processing operation.
- `sensor`
  - Sensor or instrument filter applied to provider results.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_global_health_data

**Index:** 18

```python
def fetch_global_health_data( mode: str='indicator_registry', query_path: str='', fmt: str='json', time: int=20 ) -> Any
```

Retrieve WHO global health indicator and Athena data.

#### 🎯 Purpose

Retrieve WHO global health indicator and Athena data through WHO Global Health. Use ``mode``
    to select among ``athena``, ``indicator_registry``.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``athena``, ``indicator_registry``.
- `query_path`
  - Path identifying the query resource.
- `fmt`
  - Provider response format, such as JSON or XML when supported.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_global_imagery_map_services

**Index:** 19

```python
def fetch_global_imagery_map_services(  ) -> Any
```

Retrieve available imagery map services.

#### 🎯 Purpose

Retrieve available imagery map services through NASA Global Imagery Browse Services.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_global_imagery_mercator_map

**Index:** 20

```python
def fetch_global_imagery_mercator_map( ccrs: Any | None=None ) -> Any
```

Render a Mercator imagery map.

#### 🎯 Purpose

Render a Mercator imagery map through NASA Global Imagery Browse Services.

#### 📥 Arguments

- `ccrs`
  - Optional Cartopy coordinate reference system used to construct the map.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_global_imagery_wms_map

**Index:** 21

```python
def fetch_global_imagery_wms_map( layer: str, image_date: str, bbox: Tuple[float, float, float, float], width: int=1200, height: int=600, projection: str='epsg4326', quality: str='best', image_format: str='image/png', transparent: bool=True, output_dir: str='python-examples', output_name: str='', time: int=20 ) -> Any
```

Retrieve a WMS imagery map.

#### 🎯 Purpose

Retrieve a WMS imagery map through NASA Global Imagery Browse Services. Coordinate and
    bounding arguments constrain geographic scope when supported.

#### 📥 Arguments

- `layer`
  - Map or imagery layer identifier.
- `image_date`
  - Observation date used to select imagery.
- `bbox`
  - Bounding box defining the geographic extent of the request.
- `width`
  - Output image or chart width in pixels.
- `height`
  - Output image or chart height in pixels.
- `projection`
  - Coordinate reference system used for rendered imagery.
- `quality`
  - Imagery quality level requested from the mapping service.
- `image_format`
  - Output format requested for image.
- `transparent`
  - Whether the generated map image should use a transparent background.
- `output_dir`
  - Local directory where generated imagery is written.
- `output_name`
  - Optional filename for generated imagery.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_google_drive

**Index:** 22

```python
def fetch_google_drive( question: str, folder_id: str='root', results: int=10, template: str='gdrive-query', mime_type: str | None=None, mode: str='documents' ) -> Any
```

Retrieve Google Drive documents.

#### 🎯 Purpose

Retrieve Google Drive documents through Google Drive. The query text determines the records
    or documents matched by the provider. Result-count arguments bound the amount of data
    requested.

#### 📥 Arguments

- `question`
  - Search text, lookup value, or provider query submitted by the caller.
- `folder_id`
  - Provider folder identifier that scopes the operation.
- `results`
  - Maximum number of search results to request.
- `template`
  - Provider query template used to construct the request.
- `mime_type`
  - Optional MIME type used to restrict matching files.
- `mode`
  - Operation mode used to select the provider or processing workflow.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_google_geocoding

**Index:** 23

```python
def fetch_google_geocoding( mode: str='forward', query: str='', latitude: float=0.0, longitude: float=0.0, place_id: str='', language: str='en', region: str='', result_type: str='', location_type: str='', time: int=10, api_key: Optional[str]=None ) -> Any
```

Retrieve Google forward, reverse, and place geocoding.

#### 🎯 Purpose

Retrieve Google forward, reverse, and place geocoding through Google Geocoding. Use ``mode``
    to select among ``forward``, ``place``, ``reverse``. The query text determines the records
    or documents matched by the provider. Coordinate and bounding arguments constrain geographic
    scope when supported. When supplied, ``api_key`` overrides the configured provider
    credential for this request.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``forward``, ``place``, ``reverse``.
- `query`
  - Search text, lookup value, or provider query submitted by the caller.
- `latitude`
  - Latitude in decimal degrees.
- `longitude`
  - Longitude in decimal degrees.
- `place_id`
  - Provider identifier for the selected place.
- `language`
  - Language code used for provider results or parsing.
- `region`
  - Provider region filter or regional bias value.
- `result_type`
  - Provider type selector for result.
- `location_type`
  - Provider type selector for location.
- `time`
  - Request timeout in seconds.
- `api_key`
  - Optional credential override used for the active request.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_google_search

**Index:** 24

```python
def fetch_google_search( keywords: str, results: int=10, start: int=1, exact_terms: str='', exclude_terms: str='', file_type: str='', date_restrict: str='', gl: str='', lr: str='', safe: str='off', search_type: str='', site_search: str='', site_search_filter: str='', sort: str='', img_size: str='', img_type: str='', img_color_type: str='', img_dominant_color: str='', time: int=10, api_key: str | None=None, cse_id: str | None=None ) -> Any
```

Retrieve Google Custom Search.

#### 🎯 Purpose

Retrieve Google Custom Search through Google Custom Search. The query text determines the
    records or documents matched by the provider. Result-count arguments bound the amount of
    data requested. When supplied, ``api_key`` overrides the configured provider credential for
    this request.

#### 📥 Arguments

- `keywords`
  - Search text, lookup value, or provider query submitted by the caller.
- `results`
  - Maximum number of search results to request.
- `start`
  - Starting result position used for pagination.
- `exact_terms`
  - Phrase that must appear exactly in Google Custom Search results.
- `exclude_terms`
  - Terms that must not appear in Google Custom Search results.
- `file_type`
  - File-extension filter applied to Google Custom Search results.
- `date_restrict`
  - Google Custom Search date restriction expression.
- `gl`
  - Google country-code boost applied to search results.
- `lr`
  - Google language restriction expression.
- `safe`
  - Google SafeSearch setting.
- `search_type`
  - Google Custom Search result type; use the provider-supported image-search value when requesting images.
- `site_search`
  - Domain or site used to restrict Google Custom Search results.
- `site_search_filter`
  - Whether ``site_search`` is included or excluded by Google Custom Search.
- `sort`
  - Provider-supported result ordering expression.
- `img_size`
  - Image-size filter used for Google image search.
- `img_type`
  - Google image type filter.
- `img_color_type`
  - Google image color-type filter.
- `img_dominant_color`
  - Dominant-color filter used for Google image search.
- `time`
  - Request timeout in seconds.
- `api_key`
  - Optional credential override used for the active request.
- `cse_id`
  - Google Programmable Search Engine identifier.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_google_weather_alerts

**Index:** 25

```python
def fetch_google_weather_alerts( address: str, language_code: str='en', time: int=10 ) -> Any
```

Retrieve google weather alerts data.

#### 🎯 Purpose

Retrieve google weather alerts data through Google Weather.

#### 📥 Arguments

- `address`
  - Street address or place description used for geocoding, validation, or routing.
- `language_code`
  - BCP-47-style language code used for provider results.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_google_weather_current

**Index:** 26

```python
def fetch_google_weather_current( address: str, units_system: str='METRIC', language_code: str='en', time: int=10 ) -> Any
```

Retrieve google weather current data.

#### 🎯 Purpose

Retrieve google weather current data through Google Weather.

#### 📥 Arguments

- `address`
  - Street address or place description used for geocoding, validation, or routing.
- `units_system`
  - Measurement unit system requested from the provider.
- `language_code`
  - BCP-47-style language code used for provider results.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_google_weather_daily_forecast

**Index:** 27

```python
def fetch_google_weather_daily_forecast( address: str, days: int=5, units_system: str='METRIC', language_code: str='en', time: int=10 ) -> Any
```

Retrieve daily forecast.

#### 🎯 Purpose

Retrieve daily forecast through Google Weather.

#### 📥 Arguments

- `address`
  - Street address or place description used for geocoding, validation, or routing.
- `days`
  - Number of calendar days included in the requested interval.
- `units_system`
  - Measurement unit system requested from the provider.
- `language_code`
  - BCP-47-style language code used for provider results.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_google_weather_hourly_forecast

**Index:** 28

```python
def fetch_google_weather_hourly_forecast( address: str, hours: int=24, units_system: str='METRIC', language_code: str='en', time: int=10 ) -> Any
```

Retrieve hourly forecast.

#### 🎯 Purpose

Retrieve hourly forecast through Google Weather.

#### 📥 Arguments

- `address`
  - Street address or place description used for geocoding, validation, or routing.
- `hours`
  - Number of hourly observations or forecast periods to request.
- `units_system`
  - Measurement unit system requested from the provider.
- `language_code`
  - BCP-47-style language code used for provider results.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_google_weather_hourly_history

**Index:** 29

```python
def fetch_google_weather_hourly_history( address: str, hours: int=24, units_system: str='METRIC', language_code: str='en', time: int=10 ) -> Any
```

Retrieve hourly history.

#### 🎯 Purpose

Retrieve hourly history through Google Weather.

#### 📥 Arguments

- `address`
  - Street address or place description used for geocoding, validation, or routing.
- `hours`
  - Number of hourly observations or forecast periods to request.
- `units_system`
  - Measurement unit system requested from the provider.
- `language_code`
  - BCP-47-style language code used for provider results.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_gov_data

**Index:** 30

```python
def fetch_gov_data( mode: str='search', query: str='', page_size: int=10, offset_mark: str='*', sort_field: str='score', sort_order: str='DESC', package_id: str='', collection: str='', start_date: str='', time: int=20 ) -> Any
```

Retrieve Data.gov package and collection.

#### 🎯 Purpose

Retrieve Data.gov package and collection through Data.gov. Use ``mode`` to select among
    ``collection``, ``package_summary``, ``search``. The query text determines the records or
    documents matched by the provider. Date and time arguments constrain the requested interval
    when supplied. Result-count arguments bound the amount of data requested.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``collection``, ``package_summary``, ``search``.
- `query`
  - Search text, lookup value, or provider query submitted by the caller.
- `page_size`
  - Maximum number of records requested per page.
- `offset_mark`
  - Provider continuation marker used for paginated Data.gov search results.
- `sort_field`
  - Provider field used to order search results.
- `sort_order`
  - Sort direction applied to the provider search.
- `package_id`
  - Provider identifier for the selected package.
- `collection`
  - Provider collection identifier used to restrict results.
- `start_date`
  - Inclusive start date for the requested time range, in the provider-supported format.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_grokipedia

**Index:** 31

```python
def fetch_grokipedia( mode: str='search', query: str='', page: str='', limit: int=12, offset: int=0, include_content: bool=True ) -> Any
```

Retrieve Grokipedia search and page.

#### 🎯 Purpose

Retrieve Grokipedia search and page through Grokipedia. The query text determines the
    records or documents matched by the provider. Result-count arguments bound the amount of
    data requested.

#### 📥 Arguments

- `mode`
  - Operation mode used to select the provider or processing workflow.
- `query`
  - Search text, lookup value, or provider query submitted by the caller.
- `page`
  - One-based result page to request.
- `limit`
  - Maximum number of records or items to return.
- `offset`
  - Zero-based result offset used for pagination.
- `include_content`
  - Whether to include content in the result.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_health_data

**Index:** 32

```python
def fetch_health_data( mode: str='rows', domain: str='healthdata.gov', dataset_id: str='', select: str='', where: str='', order: str='', group: str='', limit: int=25, offset: int=0, time: int=20 ) -> Any
```

Retrieve HealthData.gov Socrata metadata and rows.

#### 🎯 Purpose

Retrieve HealthData.gov Socrata metadata and rows through HealthData.gov. Use ``mode`` to
    select among ``metadata``, ``rows``. Result-count arguments bound the amount of data
    requested.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``metadata``, ``rows``.
- `domain`
  - Provider domain or host containing the requested dataset.
- `dataset_id`
  - Provider dataset identifier.
- `select`
  - Socrata ``$select`` expression defining returned columns or calculations.
- `where`
  - Socrata ``$where`` filter expression.
- `order`
  - Provider-supported result ordering expression.
- `group`
  - Socrata ``$group`` expression used to aggregate rows.
- `limit`
  - Maximum number of records or items to return.
- `offset`
  - Zero-based result offset used for pagination.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_historical_weather

**Index:** 33

```python
def fetch_historical_weather( location: str, date: dt.date, zone: str='auto', count: int=10 ) -> Any
```

Retrieve historical weather archive.

#### 🎯 Purpose

Retrieve historical weather archive through Open-Meteo Archive.

#### 📥 Arguments

- `location`
  - Place name, address, or location description resolved by the provider.
- `date`
  - Date used by the provider or processing operation.
- `zone`
  - Timezone identifier or automatic timezone-selection mode.
- `count`
  - Maximum number of matching locations or records to consider.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_internet_archive

**Index:** 34

```python
def fetch_internet_archive( keywords: str, fields: List[str] | None=None, rows: int=10, page: int=1, sort: str='downloads desc', media_type: str='', collection: str='', time: int=20 ) -> Any
```

Retrieve Internet Archive search and metadata.

#### 🎯 Purpose

Retrieve Internet Archive search and metadata through Internet Archive. The query text
    determines the records or documents matched by the provider. Result-count arguments bound
    the amount of data requested.

#### 📥 Arguments

- `keywords`
  - Search text, lookup value, or provider query submitted by the caller.
- `fields`
  - Comma-separated or provider-specific field selection.
- `rows`
  - Maximum number of rows to request.
- `page`
  - One-based result page to request.
- `sort`
  - Provider-supported result ordering expression.
- `media_type`
  - Provider type selector for media.
- `collection`
  - Provider collection identifier used to restrict results.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_naval_observatory

**Index:** 35

```python
def fetch_naval_observatory( mode: str='celnav', date_value: str='', time_value: str='', latitude: float=0.0, longitude: float=0.0, location_label: str='', time: int=20 ) -> Any
```

Retrieve U.S. Naval Observatory celestial-navigation data.

#### 🎯 Purpose

Retrieve U.S. Naval Observatory celestial-navigation data through U.S. Naval Observatory.
    Coordinate and bounding arguments constrain geographic scope when supported.

#### 📥 Arguments

- `mode`
  - Operation mode used to select the provider or processing workflow.
- `date_value`
  - Calendar date used by the selected provider operation.
- `time_value`
  - Clock time or timestamp used by the selected provider operation.
- `latitude`
  - Latitude in decimal degrees.
- `longitude`
  - Longitude in decimal degrees.
- `location_label`
  - Human-readable label associated with the supplied coordinates.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_nearby_objects

**Index:** 36

```python
def fetch_nearby_objects( mode: str='close_approaches', start_date: str='', end_date: str='', query: str='', query_type: str='sstr', dist_max: str='10LD', body: str='Earth', sort: str='date', limit: int=20, dv: float=6.0, dur: int=360, stay: int=8, launch: str='2020-2045', h: float=26.0, occ: int=7, include_physical: bool=True, include_close_approaches: bool=True, ca_body: str='Earth', include_discovery: bool=True, time: int=20 ) -> Any
```

Retrieve JPL SSD and CNEOS near-Earth object data.

#### 🎯 Purpose

Retrieve JPL SSD and CNEOS near-Earth object data through NASA/JPL near-Earth object
    services. The query text determines the records or documents matched by the provider. Date
    and time arguments constrain the requested interval when supplied. Result-count arguments
    bound the amount of data requested.

#### 📥 Arguments

- `mode`
  - Operation mode used to select the provider or processing workflow.
- `start_date`
  - Inclusive start date for the requested time range, in the provider-supported format.
- `end_date`
  - Inclusive end date for the requested time range, in the provider-supported format.
- `query`
  - Search text, lookup value, or provider query submitted by the caller.
- `query_type`
  - Provider type selector for query.
- `dist_max`
  - Maximum close-approach distance expression accepted by the JPL service.
- `body`
  - Solar-system body used as the reference object.
- `sort`
  - Provider-supported result ordering expression.
- `limit`
  - Maximum number of records or items to return.
- `dv`
  - Delta-v threshold or mission constraint used by the near-Earth object query.
- `dur`
  - Mission duration constraint, in days, used by the near-Earth object query.
- `stay`
  - Target stay-duration constraint, in days, used by the near-Earth object query.
- `launch`
  - Launch-year or launch-window expression used by the near-Earth object query.
- `h`
  - Absolute-magnitude threshold used by the near-Earth object query.
- `occ`
  - Opportunity-count or occurrence constraint used by the mission query.
- `include_physical`
  - Whether to include physical in the result.
- `include_close_approaches`
  - Whether to include close approaches in the result.
- `ca_body`
  - Reference body used for close-approach data.
- `include_discovery`
  - Whether to include discovery in the result.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_news

**Index:** 37

```python
def fetch_news( endpoint: str='all', query: str='', language: str='en', categories: str='', exclude_categories: str='', locale: str='', domains: str='', exclude_domains: str='', source_ids: str='', exclude_source_ids: str='', published_after: str='', published_before: str='', published_on: str='', sort: str='published_at', limit: int=10, page: int=1, include_similar: bool=True, headlines_per_category: int=6, time: int=10, api_key: str | None=None ) -> Any
```

Retrieve The News API article.

#### 🎯 Purpose

Retrieve The News API article through The News API. The query text determines the records or
    documents matched by the provider. Date and time arguments constrain the requested interval
    when supplied. Result-count arguments bound the amount of data requested. Boolean options
    control retrieval depth or supplemental content. When supplied, ``api_key`` overrides the
    configured provider credential for this request.

#### 📥 Arguments

- `endpoint`
  - Provider endpoint or endpoint family to request.
- `query`
  - Search text, lookup value, or provider query submitted by the caller.
- `language`
  - Language code used for provider results or parsing.
- `categories`
  - Comma-separated news categories used to include matching articles.
- `exclude_categories`
  - Filter value used to exclude categories from provider results.
- `locale`
  - Locale filter applied to news results.
- `domains`
  - Comma-separated source domains used to include matching news articles.
- `exclude_domains`
  - Filter value used to exclude domains from provider results.
- `source_ids`
  - Provider identifiers for the selected source.
- `exclude_source_ids`
  - Filter value used to exclude source ids from provider results.
- `published_after`
  - Earliest publication timestamp accepted by the news query.
- `published_before`
  - Latest publication timestamp accepted by the news query.
- `published_on`
  - Specific publication date used to restrict news results.
- `sort`
  - Provider-supported result ordering expression.
- `limit`
  - Maximum number of records or items to return.
- `page`
  - One-based result page to request.
- `include_similar`
  - Whether to include similar in the result.
- `headlines_per_category`
  - Maximum number of headlines returned for each category in headline mode.
- `time`
  - Request timeout in seconds.
- `api_key`
  - Optional credential override used for the active request.

#### 📤 Returns

Dict[str, Any]: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_open_aq

**Index:** 38

```python
def fetch_open_aq( mode: str='locations', location_id: int | None=None, parameter_id: int | None=None, country_id: int | None=None, coordinates: str='', radius: int=25000, providers_id: str='', parameters_id: str='', limit: int=25, page: int=1, time: int=20 ) -> Any
```

Retrieve OpenAQ location, measurement, and air-quality records.

#### 🎯 Purpose

Retrieve OpenAQ location, measurement, and air-quality records through OpenAQ. Use ``mode``
    to select among ``countries``, ``latest``, ``locations``, ``parameter_latest``,
    ``parameters``, ``providers``. Coordinate and bounding arguments constrain geographic scope
    when supported. Result-count arguments bound the amount of data requested.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``countries``, ``latest``, ``locations``, ``parameter_latest``, ``parameters``, ``providers``.
- `location_id`
  - Provider identifier for the selected location.
- `parameter_id`
  - Provider identifier for the selected parameter.
- `country_id`
  - Provider identifier for the selected country.
- `coordinates`
  - Latitude/longitude coordinate string used by the provider.
- `radius`
  - Search radius in the units specified by the operation.
- `providers_id`
  - Provider identifier for the selected providers.
- `parameters_id`
  - Provider identifier for the selected parameters.
- `limit`
  - Maximum number of records or items to return.
- `page`
  - One-based result page to request.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_open_science

**Index:** 39

```python
def fetch_open_science( mode: str='dataset', query: str='', accession: str='', format_value: str='json', time: int=20 ) -> Any
```

Retrieve NASA Open Science Data Repository resources.

#### 🎯 Purpose

Retrieve NASA Open Science Data Repository resources through NASA Open Science Data
    Repository. The query text determines the records or documents matched by the provider.

#### 📥 Arguments

- `mode`
  - Operation mode used to select the provider or processing workflow.
- `query`
  - Search text, lookup value, or provider query submitted by the caller.
- `accession`
  - Dataset accession identifier used to retrieve a specific Open Science resource.
- `format_value`
  - Provider output format.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_open_sky

**Index:** 40

```python
def fetch_open_sky( mode: str='states_bbox', icao24: str='', airport: str='', begin: int | None=None, end: int | None=None, time_value: int | None=None, lamin: float | None=None, lomin: float | None=None, lamax: float | None=None, lomax: float | None=None, extended: bool=False, client_id: str | None=None, client_secret: str | None=None, time: int=20 ) -> Any
```

Retrieve OpenSky Network aircraft, airport, and state-vector data.

#### 🎯 Purpose

Retrieve OpenSky Network aircraft, airport, and state-vector data through OpenSky Network.
    Use ``mode`` to select among ``arrivals_airport``, ``departures_airport``,
    ``flights_aircraft``, ``states_bbox``, ``track_aircraft``.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``arrivals_airport``, ``departures_airport``, ``flights_aircraft``, ``states_bbox``, ``track_aircraft``.
- `icao24`
  - 24-bit ICAO aircraft transponder address.
- `airport`
  - ICAO airport identifier used to query arrivals or departures.
- `begin`
  - Beginning Unix timestamp for the requested aviation interval.
- `end`
  - Ending Unix timestamp for the requested aviation interval.
- `time_value`
  - Clock time or timestamp used by the selected provider operation.
- `lamin`
  - Bounding-box minimum latitude in decimal degrees.
- `lomin`
  - Bounding-box minimum longitude in decimal degrees.
- `lamax`
  - Bounding-box maximum latitude in decimal degrees.
- `lomax`
  - Bounding-box maximum longitude in decimal degrees.
- `extended`
  - Whether extended OpenSky state-vector fields should be requested.
- `client_id`
  - Optional credential override used for the active request.
- `client_secret`
  - Optional credential override used for the active request.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_open_weather

**Index:** 41

```python
def fetch_open_weather( location: str, mode: str='current', zone: str='auto', forecast_days: int=7, past_days: int=0, count: int=10 ) -> Any
```

Retrieve Open-Meteo current and forecast weather.

#### 🎯 Purpose

Retrieve Open-Meteo current and forecast weather through Open-Meteo.

#### 📥 Arguments

- `location`
  - Place name, address, or location description resolved by the provider.
- `mode`
  - Operation mode used to select the provider or processing workflow.
- `zone`
  - Timezone identifier or automatic timezone-selection mode.
- `forecast_days`
  - Number of forecast days to request.
- `past_days`
  - Number of historical days to include with the weather request.
- `count`
  - Maximum number of matching locations or records to consider.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_purple_air

**Index:** 42

```python
def fetch_purple_air( mode: str='sensors', sensor_index: int | None=None, nwlng: float | None=None, nwlat: float | None=None, selng: float | None=None, selat: float | None=None, location_type: int=0, max_age: int=0, modified_since: int=0, fields: str='', time: int=20 ) -> Any
```

Retrieve PurpleAir sensor and air quality records.

#### 🎯 Purpose

Retrieve PurpleAir sensor and air quality records through PurpleAir. Use ``mode`` to select
    among ``sensor``, ``sensors``. Coordinate and bounding arguments constrain geographic scope
    when supported.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``sensor``, ``sensors``.
- `sensor_index`
  - PurpleAir sensor identifier.
- `nwlng`
  - Northwest bounding-box longitude in decimal degrees.
- `nwlat`
  - Northwest bounding-box latitude in decimal degrees.
- `selng`
  - Southeast bounding-box longitude in decimal degrees.
- `selat`
  - Southeast bounding-box latitude in decimal degrees.
- `location_type`
  - Provider type selector for location.
- `max_age`
  - Maximum age permitted by the operation.
- `modified_since`
  - Unix timestamp used to return PurpleAir sensors modified after the specified time.
- `fields`
  - Comma-separated or provider-specific field selection.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_satellite_center

**Index:** 43

```python
def fetch_satellite_center( mode: str='observatories', query: str='', start_time: str='', end_time: str='', coordinate_systems: str='gse', resolution_factor: int=1, time: int=20 ) -> Any
```

Retrieve SSC satellite observatory, ground-station, and location data.

#### 🎯 Purpose

Retrieve SSC satellite observatory, ground-station, and location data through NASA Satellite
    Situation Center. The query text determines the records or documents matched by the
    provider.

#### 📥 Arguments

- `mode`
  - Operation mode used to select the provider or processing workflow.
- `query`
  - Search text, lookup value, or provider query submitted by the caller.
- `start_time`
  - Beginning timestamp for the requested provider interval.
- `end_time`
  - Ending timestamp for the requested provider interval.
- `coordinate_systems`
  - Coordinate system or comma-separated coordinate systems requested from the satellite service.
- `resolution_factor`
  - Sampling resolution factor applied to returned satellite location data.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_socrata

**Index:** 44

```python
def fetch_socrata( mode: str='rows', domain: str='data.cdc.gov', dataset_id: str='', select: str='', where: str='', order: str='', group: str='', limit: int=25, offset: int=0, time: int=20 ) -> Any
```

Retrieve Socrata dataset metadata and row.

#### 🎯 Purpose

Retrieve Socrata dataset metadata and row through Socrata. Use ``mode`` to select among
    ``metadata``, ``rows``. Result-count arguments bound the amount of data requested.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``metadata``, ``rows``.
- `domain`
  - Provider domain or host containing the requested dataset.
- `dataset_id`
  - Provider dataset identifier.
- `select`
  - Socrata ``$select`` expression defining returned columns or calculations.
- `where`
  - Socrata ``$where`` filter expression.
- `order`
  - Provider-supported result ordering expression.
- `group`
  - Socrata ``$group`` expression used to aggregate rows.
- `limit`
  - Maximum number of records or items to return.
- `offset`
  - Zero-based result offset used for pagination.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_space_weather

**Index:** 45

```python
def fetch_space_weather( mode: str='cme', start_date: str='', end_date: str='', time: int=20, location: str='ALL', catalog: str='ALL', notification_type: str='all', most_accurate_only: bool=True, complete_entry_only: bool=True, speed: int=0, half_angle: int=0, keyword: str='', api_key: str | None=None ) -> Any
```

Retrieve NASA DONKI space weather endpoints.

#### 🎯 Purpose

Retrieve NASA DONKI space weather endpoints through NASA DONKI. Date and time arguments
    constrain the requested interval when supplied. When supplied, ``api_key`` overrides the
    configured provider credential for this request.

#### 📥 Arguments

- `mode`
  - Operation mode used to select the provider or processing workflow.
- `start_date`
  - Inclusive start date for the requested time range, in the provider-supported format.
- `end_date`
  - Inclusive end date for the requested time range, in the provider-supported format.
- `time`
  - Request timeout in seconds.
- `location`
  - Place name, address, or location description resolved by the provider.
- `catalog`
  - Provider catalog filter.
- `notification_type`
  - Provider type selector for notification.
- `most_accurate_only`
  - Whether to restrict results to the provider-designated most accurate analyses.
- `complete_entry_only`
  - Whether to restrict results to complete provider entries.
- `speed`
  - Minimum or target speed constraint used by the space-weather query.
- `half_angle`
  - Half-angle constraint used by the space-weather query.
- `keyword`
  - Keyword used to filter provider records.
- `api_key`
  - Optional credential override used for the active request.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_star_chart

**Index:** 46

```python
def fetch_star_chart( mode: str='object_chart', query: str='', ra: float=0.0, dec: float=0.0, zoom: int=5, image_source: str='DSS2', box_color: str='yellow', show_box: bool=True, show_grid: bool=True, show_lines: bool=True, show_boundaries: bool=True, show_const_names: bool=False, width: int=900, height: int=450, magnitude: float=7.5, time: int=20 ) -> Any
```

Retrieve static star chart and coordinate chart generation.

#### 🎯 Purpose

Retrieve static star chart and coordinate chart generation through astronomical chart
    service. The query text determines the records or documents matched by the provider.

#### 📥 Arguments

- `mode`
  - Operation mode used to select the provider or processing workflow.
- `query`
  - Search text, lookup value, or provider query submitted by the caller.
- `ra`
  - Right ascension value.
- `dec`
  - Declination value.
- `zoom`
  - Map or chart zoom level.
- `image_source`
  - Imagery or survey source used to render the map or chart.
- `box_color`
  - Color used to draw the target box on generated map or chart output.
- `show_box`
  - Whether to display box in generated output.
- `show_grid`
  - Whether to display grid in generated output.
- `show_lines`
  - Whether to display lines in generated output.
- `show_boundaries`
  - Whether to display boundaries in generated output.
- `show_const_names`
  - Whether to display const names in generated output.
- `width`
  - Output image or chart width in pixels.
- `height`
  - Output image or chart height in pixels.
- `magnitude`
  - Limiting stellar magnitude used when rendering a chart.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_star_map

**Index:** 47

```python
def fetch_star_map( mode: str='object_link', query: str='', ra: float=0.0, dec: float=0.0, zoom: int=5, image_source: str='DSS2', box_color: str='yellow', show_box: bool=True, show_grid: bool=True, show_lines: bool=True, show_boundaries: bool=True, show_const_names: bool=False, time: int=20 ) -> Any
```

Retrieve astronomical object map links and imagery.

#### 🎯 Purpose

Retrieve astronomical object map links and imagery through astronomical map service. The
    query text determines the records or documents matched by the provider.

#### 📥 Arguments

- `mode`
  - Operation mode used to select the provider or processing workflow.
- `query`
  - Search text, lookup value, or provider query submitted by the caller.
- `ra`
  - Right ascension value.
- `dec`
  - Declination value.
- `zoom`
  - Map or chart zoom level.
- `image_source`
  - Imagery or survey source used to render the map or chart.
- `box_color`
  - Color used to draw the target box on generated map or chart output.
- `show_box`
  - Whether to display box in generated output.
- `show_grid`
  - Whether to display grid in generated output.
- `show_lines`
  - Whether to display lines in generated output.
- `show_boundaries`
  - Whether to display boundaries in generated output.
- `show_const_names`
  - Whether to display const names in generated output.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_tides_and_currents

**Index:** 48

```python
def fetch_tides_and_currents( mode: str='water-level', station_id: str='', begin_date: str='', end_date: str='', datum: str='MLLW', units: str='metric', time_zone: str='gmt', interval: str='hilo', time: int=20 ) -> Any
```

Retrieve NOAA tides, currents, and station data.

#### 🎯 Purpose

Retrieve NOAA tides, currents, and station data through NOAA Tides & Currents. Use ``mode``
    to select among ``station``, ``tide-predictions``, ``water-level``. Date and time arguments
    constrain the requested interval when supplied.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``station``, ``tide-predictions``, ``water-level``.
- `station_id`
  - Provider identifier for the selected station.
- `begin_date`
  - Beginning date for the requested interval, in the provider-supported format.
- `end_date`
  - Inclusive end date for the requested time range, in the provider-supported format.
- `datum`
  - Vertical datum used for tide or water-level measurements.
- `units`
  - Unit system used for returned measurements.
- `time_zone`
  - Timezone used for returned tide or current timestamps.
- `interval`
  - Provider sampling or reporting interval.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_united_nations

**Index:** 49

```python
def fetch_united_nations( mode: str='datasets', query_path: str='', time: int=20 ) -> Any
```

Retrieve United Nations SDMX dataset and query.

#### 🎯 Purpose

Retrieve United Nations SDMX dataset and query through United Nations SDMX service. Use
    ``mode`` to select among ``datasets``, ``sdmx_query``.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``datasets``, ``sdmx_query``.
- `query_path`
  - Path identifying the query resource.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_usgs_earthquakes

**Index:** 50

```python
def fetch_usgs_earthquakes( mode: str='feed', feed: str='all_day.geojson', start_date: str='', end_date: str='', min_magnitude: float=1.0, max_magnitude: float=10.0, limit: int=25, order_by: str='time', event_type: str='earthquake', latitude: float | None=None, longitude: float | None=None, max_radius_km: float | None=None, time: int=20 ) -> Any
```

Retrieve USGS earthquake feed and query.

#### 🎯 Purpose

Retrieve USGS earthquake feed and query through USGS Earthquake Hazards Program. Use
    ``mode`` to select among ``feed``, ``search``. Date and time arguments constrain the
    requested interval when supplied. Coordinate and bounding arguments constrain geographic
    scope when supported. Result-count arguments bound the amount of data requested.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``feed``, ``search``.
- `feed`
  - Predefined USGS earthquake feed name used when feed mode is selected.
- `start_date`
  - Inclusive start date for the requested time range, in the provider-supported format.
- `end_date`
  - Inclusive end date for the requested time range, in the provider-supported format.
- `min_magnitude`
  - Minimum earthquake magnitude to include in the result set.
- `max_magnitude`
  - Maximum earthquake magnitude to include in the result set.
- `limit`
  - Maximum number of records or items to return.
- `order_by`
  - Provider-supported field used to order results.
- `event_type`
  - USGS event type to include; ``earthquake`` is the default.
- `latitude`
  - Latitude in decimal degrees.
- `longitude`
  - Longitude in decimal degrees.
- `max_radius_km`
  - Maximum geographic search radius in kilometers.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_usgs_national_map

**Index:** 51

```python
def fetch_usgs_national_map( mode: str='products', dataset: str='', q: str='', bbox: str='', prod_formats: str='', max_items: int=25, offset: int=0, time: int=20 ) -> Any
```

Retrieve USGS National Map datasets and products.

#### 🎯 Purpose

Retrieve USGS National Map datasets and products through USGS The National Map. Use ``mode``
    to select among ``datasets``, ``products``. The query text determines the records or
    documents matched by the provider. Coordinate and bounding arguments constrain geographic
    scope when supported. Result-count arguments bound the amount of data requested.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``datasets``, ``products``.
- `dataset`
  - Provider dataset name or identifier.
- `q`
  - Free-text provider query used to search matching records.
- `bbox`
  - Bounding box defining the geographic extent of the request.
- `prod_formats`
  - Product-format filter applied to National Map results.
- `max_items`
  - Maximum number of records or items to return.
- `offset`
  - Zero-based result offset used for pagination.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_usgs_sciencebase

**Index:** 52

```python
def fetch_usgs_sciencebase( mode: str='items', q: str='', item_id: str='', max_items: int=25, offset: int=0, fields: str='', time: int=20 ) -> Any
```

Retrieve USGS ScienceBase items and catalog records.

#### 🎯 Purpose

Retrieve USGS ScienceBase items and catalog records through USGS ScienceBase. Use ``mode``
    to select among ``item``, ``items``. The query text determines the records or documents
    matched by the provider. Result-count arguments bound the amount of data requested.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``item``, ``items``.
- `q`
  - Free-text provider query used to search matching records.
- `item_id`
  - Provider identifier for the selected item.
- `max_items`
  - Maximum number of records or items to return.
- `offset`
  - Zero-based result offset used for pagination.
- `fields`
  - Comma-separated or provider-specific field selection.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_usgs_water_data

**Index:** 53

```python
def fetch_usgs_water_data( mode: str='monitoring-locations', monitoring_location_id: str='', state_code: str='', county_code: str='', site_type: str='', parameter_code: str='', limit: int=25, time: int=20 ) -> Any
```

Retrieve USGS water services records.

#### 🎯 Purpose

Retrieve USGS water services records through USGS Water Data. Use ``mode`` to select among
    ``latest-continuous``, ``latest-daily``, ``monitoring-locations``, ``time-series-metadata``.
    Result-count arguments bound the amount of data requested.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``latest- continuous``, ``latest-daily``, ``monitoring-locations``, ``time-series-metadata``.
- `monitoring_location_id`
  - USGS monitoring-location identifier used to target a specific site.
- `state_code`
  - State code used to restrict provider records.
- `county_code`
  - County code used to restrict provider records.
- `site_type`
  - USGS site-type code used to restrict monitoring locations.
- `parameter_code`
  - USGS parameter code identifying the measured property.
- `limit`
  - Maximum number of records or items to return.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_uv_index

**Index:** 54

```python
def fetch_uv_index( mode: str='daily-zip', zip_code: str='', city: str='', state: str='', time: int=20 ) -> Any
```

Retrieve EPA UV Index current and forecast data.

#### 🎯 Purpose

Retrieve EPA UV Index current and forecast data through EPA UV Index. Use ``mode`` to select
    among ``daily-city-state``, ``daily-zip``, ``hourly-city-state``, ``hourly-zip``.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``daily- city-state``, ``daily-zip``, ``hourly-city-state``, ``hourly-zip``.
- `zip_code`
  - Provider code identifying or filtering zip.
- `city`
  - City name used to locate or filter provider records.
- `state`
  - State name or abbreviation used to locate or filter provider records.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_web_page

**Index:** 55

```python
def fetch_web_page( url: str, time: int=10 ) -> Any
```

Retrieve HTTP web page retrieval and HTML extraction.

#### 🎯 Purpose

Retrieve HTTP web page retrieval and HTML extraction through web fetcher.

#### 📥 Arguments

- `url`
  - URL or URI value used as the request or parsing source.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Result | None: Fonky result wrapper containing the provider or HTTP response.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_wikipedia

**Index:** 56

```python
def fetch_wikipedia( question: str, language: str | None=None, max_documents: int | None=None, include_metadata: bool | None=None ) -> Any
```

Retrieve Wikipedia documents.

#### 🎯 Purpose

Retrieve Wikipedia documents through Wikipedia. The query text determines the records or
    documents matched by the provider. Result-count arguments bound the amount of data
    requested. Boolean options control retrieval depth or supplemental content.

#### 📥 Arguments

- `question`
  - Search text, lookup value, or provider query submitted by the caller.
- `language`
  - Language code used for provider results or parsing.
- `max_documents`
  - Maximum number of documents to retrieve.
- `include_metadata`
  - Whether provider metadata should be included with retrieved content.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_wonder

**Index:** 57

```python
def fetch_wonder( mode: str='metadata_template', dataset_id: str='D76', request_xml: str='', time: int=20 ) -> Any
```

Retrieve CDC WONDER template and query submission.

#### 🎯 Purpose

Retrieve CDC WONDER template and query submission through CDC WONDER. Use ``mode`` to select
    among ``metadata_template``, ``query_xml``.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``metadata_template``, ``query_xml``.
- `dataset_id`
  - Provider dataset identifier.
- `request_xml`
  - CDC WONDER XML request document submitted for query execution.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 fetch_world_population

**Index:** 58

```python
def fetch_world_population( mode: str='catalog', query: str='', asset_path: str='', page: int=1, page_size: int=25, time: int=20 ) -> Any
```

Retrieve WorldPop catalog and raster metadata.

#### 🎯 Purpose

Retrieve WorldPop catalog and raster metadata through WorldPop. Use ``mode`` to select among
    ``catalog``, ``raster_metadata``, ``search``. The query text determines the records or
    documents matched by the provider. Result-count arguments bound the amount of data
    requested.

#### 📥 Arguments

- `mode`
  - Operation selector. Supported values detected in the implementation include ``catalog``, ``raster_metadata``, ``search``.
- `query`
  - Search text, lookup value, or provider query submitted by the caller.
- `asset_path`
  - Path identifying the asset resource.
- `page`
  - One-based result page to request.
- `page_size`
  - Maximum number of records requested per page.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 geocode_coordinates

**Index:** 59

```python
def geocode_coordinates( lat: float, long: float ) -> Any
```

Geocode coordinates.

#### 🎯 Purpose

Geocode coordinates using Google Maps. Coordinate and bounding arguments constrain
    geographic scope when supported.

#### 📥 Arguments

- `lat`
  - Latitude in decimal degrees.
- `long`
  - Longitude in decimal degrees.

#### 📤 Returns

str | None: Text produced by the operation.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 geocode_location

**Index:** 60

```python
def geocode_location( address: str ) -> Any
```

Geocode location.

#### 🎯 Purpose

Geocode location using Google Maps.

#### 📥 Arguments

- `address`
  - Street address or place description used for geocoding, validation, or routing.

#### 📤 Returns

Tuple[float, float]: Latitude and longitude coordinate pair.

#### ⚠️ Raises

ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_arxiv

**Index:** 61

```python
def load_arxiv( question: str ) -> Any
```

Load ArXiv research documents.

#### 🎯 Purpose

Load ArXiv research documents using the ArXiv loader. The query text determines the records
    or documents matched by the provider.

#### 📥 Arguments

- `question`
  - Search query or prompt submitted to the backing loader.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_aws_bucket

**Index:** 62

```python
def load_aws_bucket( bucket: str, prefix: Optional[str]=None, aws_access_key_id: Optional[str]=None, aws_secret_access_key: Optional[str]=None, aws_session_token: Optional[str]=None, region_name: Optional[str]=None, endpoint_url: Optional[str]=None ) -> Any
```

Load documents from an Amazon S3 bucket.

#### 🎯 Purpose

Load documents from an Amazon S3 bucket using the Amazon S3 bucket loader.

#### 📥 Arguments

- `bucket`
  - Storage bucket name.
- `prefix`
  - Optional object-name prefix used to restrict cloud storage results.
- `aws_access_key_id`
  - Provider identifier for the selected aws access key.
- `aws_secret_access_key`
  - AWS credential or configuration value for secret access key.
- `aws_session_token`
  - AWS credential or configuration value for session token.
- `region_name`
  - Cloud region name used to configure the storage client.
- `endpoint_url`
  - Optional alternate service endpoint URL.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_aws_file

**Index:** 63

```python
def load_aws_file( bucket: str, key: str, aws_access_key_id: Optional[str]=None, aws_secret_access_key: Optional[str]=None, aws_session_token: Optional[str]=None, region_name: Optional[str]=None ) -> Any
```

Load an Amazon S3 object.

#### 🎯 Purpose

Load an Amazon S3 object using the Amazon S3 file loader.

#### 📥 Arguments

- `bucket`
  - Storage bucket name.
- `key`
  - Amazon S3 object key.
- `aws_access_key_id`
  - Provider identifier for the selected aws access key.
- `aws_secret_access_key`
  - AWS credential or configuration value for secret access key.
- `aws_session_token`
  - AWS credential or configuration value for session token.
- `region_name`
  - Cloud region name used to configure the storage client.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_csv

**Index:** 64

```python
def load_csv( path: str, encoding: Optional[str]='utf-8', source_column: Optional[str]=None, delimiter: str=',', quotechar: str='"' ) -> Any
```

Load a CSV file.

#### 🎯 Purpose

Load a CSV file using the CSV loader.

#### 📥 Arguments

- `path`
  - Local file path used by the loader.
- `encoding`
  - Optional file encoding passed to the backing loader.
- `source_column`
  - Optional CSV column whose value is stored as the document source.
- `delimiter`
  - Field delimiter used to parse delimited text.
- `quotechar`
  - Quote character used to parse delimited text.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_email

**Index:** 65

```python
def load_email( path: str, mode: str='single', attachments: bool=True ) -> Any
```

Load an email message.

#### 🎯 Purpose

Load an email message using the email loader.

#### 📥 Arguments

- `path`
  - Local file path used by the loader.
- `mode`
  - Operation mode used to select the provider or processing workflow.
- `attachments`
  - Whether email attachments should be included when supported.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_excel

**Index:** 66

```python
def load_excel( path: str, mode: str='elements', has_headers: bool=True ) -> Any
```

Load an Excel workbook.

#### 🎯 Purpose

Load an Excel workbook using the Excel loader.

#### 📥 Arguments

- `path`
  - Local file path used by the loader.
- `mode`
  - Operation mode used to select the provider or processing workflow.
- `has_headers`
  - Whether the first spreadsheet row should be treated as column headers.

#### 📤 Returns

List[Document]: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_github

**Index:** 67

```python
def load_github( url: str, repo: str, branch: str, filetype: str='.md' ) -> Any
```

Load files from a GitHub repository.

#### 🎯 Purpose

Load files from a GitHub repository using the GitHub loader.

#### 📥 Arguments

- `url`
  - URL used by the web or repository loader.
- `repo`
  - GitHub repository name or owner/repository path.
- `branch`
  - Repository branch to inspect.
- `filetype`
  - File suffix filter used when loading repository files.

#### 📤 Returns

List[Document]: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_google_bucket

**Index:** 68

```python
def load_google_bucket( project_name: str, bucket: str, prefix: Optional[str]=None, continue_on_failure: bool=False ) -> Any
```

Load documents from a Google Cloud Storage bucket.

#### 🎯 Purpose

Load documents from a Google Cloud Storage bucket using the Google Cloud Storage bucket
    loader.

#### 📥 Arguments

- `project_name`
  - Google Cloud project name used by the storage loader.
- `bucket`
  - Storage bucket name.
- `prefix`
  - Optional object-name prefix used to restrict cloud storage results.
- `continue_on_failure`
  - Whether loading should continue when an individual object fails.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_google_cloud_file

**Index:** 69

```python
def load_google_cloud_file( project_name: str, bucket: str, blob: str ) -> Any
```

Load a Google Cloud Storage object.

#### 🎯 Purpose

Load a Google Cloud Storage object using the Google Cloud Storage loader.

#### 📥 Arguments

- `project_name`
  - Google Cloud project name used by the storage loader.
- `bucket`
  - Storage bucket name.
- `blob`
  - Cloud storage object name.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_google_drive_file

**Index:** 70

```python
def load_google_drive_file( file_id: str, recursive: bool=False ) -> Any
```

Load a Google Drive file.

#### 🎯 Purpose

Load a Google Drive file using the Google Drive loader. Boolean options control retrieval
    depth or supplemental content.

#### 📥 Arguments

- `file_id`
  - Provider file identifier used to load a single file.
- `recursive`
  - Whether the loader should traverse nested provider or URL resources.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_google_drive_folder

**Index:** 71

```python
def load_google_drive_folder( folder_id: str, recursive: bool=False ) -> Any
```

Load documents from a Google Drive folder.

#### 🎯 Purpose

Load documents from a Google Drive folder using the Google Drive loader. Boolean options
    control retrieval depth or supplemental content.

#### 📥 Arguments

- `folder_id`
  - Provider folder identifier used to load folder contents.
- `recursive`
  - Whether the loader should traverse nested provider or URL resources.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_google_speech_to_text

**Index:** 72

```python
def load_google_speech_to_text( project_id: str, file_path: str, config: Optional[Dict[str, Any]]=None ) -> Any
```

Transcribe audio with Google Speech-to-Text.

#### 🎯 Purpose

Transcribe audio with Google Speech-to-Text using the Google Speech-to-Text loader.

#### 📥 Arguments

- `project_id`
  - Google Cloud project identifier used by the speech loader.
- `file_path`
  - Local filesystem path to the source file.
- `config`
  - Optional provider configuration mapping.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_html

**Index:** 73

```python
def load_html( path: str ) -> Any
```

Load an HTML document.

#### 🎯 Purpose

Load an HTML document using the HTML loader.

#### 📥 Arguments

- `path`
  - Local file path used by the loader.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_json

**Index:** 74

```python
def load_json( filepath: str, is_text: bool=True, is_lines: bool=False ) -> Any
```

Load JSON content.

#### 🎯 Purpose

Load JSON content using the JSON loader.

#### 📥 Arguments

- `filepath`
  - Local file path used by the loader.
- `is_text`
  - Whether JSON values should be treated as text content.
- `is_lines`
  - Whether the JSON source uses JSON Lines format.

#### 📤 Returns

List[Document]: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_jupyter_notebook

**Index:** 75

```python
def load_jupyter_notebook( path: str, include_outputs: bool=False, max_output_length: int=10, remove_newline: bool=False, traceback: bool=False ) -> Any
```

Load a Jupyter notebook.

#### 🎯 Purpose

Load a Jupyter notebook using the Jupyter notebook loader. Boolean options control retrieval
    depth or supplemental content.

#### 📥 Arguments

- `path`
  - Local file path used by the loader.
- `include_outputs`
  - Whether notebook cell outputs should be included.
- `max_output_length`
  - Maximum notebook cell output length to retain.
- `remove_newline`
  - Whether newline characters should be removed from notebook output.
- `traceback`
  - Whether notebook traceback output should be included.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_markdown

**Index:** 76

```python
def load_markdown( path: str ) -> Any
```

Load a Markdown document.

#### 🎯 Purpose

Load a Markdown document using the Markdown loader.

#### 📥 Arguments

- `path`
  - Local file path used by the loader.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_onedrive

**Index:** 77

```python
def load_onedrive( drive_id: str, folder_path: Optional[str]=None, object_ids: Optional[List[str]]=None, auth_with_token: bool=True ) -> Any
```

Load documents from OneDrive.

#### 🎯 Purpose

Load documents from OneDrive using the OneDrive loader.

#### 📥 Arguments

- `drive_id`
  - OneDrive drive identifier.
- `folder_path`
  - Optional folder path within the selected drive.
- `object_ids`
  - Optional provider object identifiers to load.
- `auth_with_token`
  - Whether token-based authentication should be used.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_open_city

**Index:** 78

```python
def load_open_city( city_id: str, dataset_id: str, limit: int=100 ) -> Any
```

Load an Open City dataset.

#### 🎯 Purpose

Load an Open City dataset using the Open City Data loader. Result-count arguments bound the
    amount of data requested.

#### 📥 Arguments

- `city_id`
  - Provider identifier for the selected city.
- `dataset_id`
  - Provider dataset identifier.
- `limit`
  - Maximum number of records requested from the backing source.

#### 📤 Returns

List[Document]: LangChain documents loaded from the requested source.

#### ⚠️ Raises

ValueError: Raised when a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_outlook

**Index:** 79

```python
def load_outlook( path: str ) -> Any
```

Load an Outlook message.

#### 🎯 Purpose

Load an Outlook message using the Outlook message loader.

#### 📥 Arguments

- `path`
  - Local file path used by the loader.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_pdf

**Index:** 80

```python
def load_pdf( path: str, mode: str='single', extract: str='plain', include: bool=False, format: str='markdown-img', size: int=1000, overlap: int=150, has_tables: bool=True ) -> Any
```

Load and extract a PDF file.

#### 🎯 Purpose

Load and extract a PDF file using the PDF loader.

#### 📥 Arguments

- `path`
  - Local file path used by the loader.
- `mode`
  - Operation mode used to select the provider or processing workflow.
- `extract`
  - PDF text-extraction strategy used by the underlying parser.
- `include`
  - Whether optional embedded content should be included.
- `format`
  - Output or embedded-image format requested from the loader.
- `size`
  - Maximum chunk size used for document splitting.
- `overlap`
  - Number of characters or tokens repeated between adjacent chunks.
- `has_tables`
  - Whether table-aware parsing or extraction should be enabled.

#### 📤 Returns

List[Document]: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_powerpoint

**Index:** 81

```python
def load_powerpoint( path: str, mode: str='single' ) -> Any
```

Load a PowerPoint presentation.

#### 🎯 Purpose

Load a PowerPoint presentation using the PowerPoint loader.

#### 📥 Arguments

- `path`
  - Local file path used by the loader.
- `mode`
  - Operation mode used to select the provider or processing workflow.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_powerpoint_multiple

**Index:** 82

```python
def load_powerpoint_multiple( path: str ) -> Any
```

Load multiple PowerPoint presentation elements.

#### 🎯 Purpose

Load multiple PowerPoint presentation elements using the PowerPoint loader.

#### 📥 Arguments

- `path`
  - Local file path used by the loader.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_pubmed

**Index:** 83

```python
def load_pubmed( query: str, max_docs: int=5 ) -> Any
```

Load PubMed research documents.

#### 🎯 Purpose

Load PubMed research documents using the PubMed loader. The query text determines the
    records or documents matched by the provider. Result-count arguments bound the amount of
    data requested.

#### 📥 Arguments

- `query`
  - Search query submitted to the backing loader.
- `max_docs`
  - Maximum number of documents requested from the backing service.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_spfx

**Index:** 84

```python
def load_spfx( library_id: str ) -> Any
```

Load a SharePoint document library.

#### 🎯 Purpose

Load a SharePoint document library using the SharePoint loader.

#### 📥 Arguments

- `library_id`
  - SharePoint document-library identifier.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_spfx_folder

**Index:** 85

```python
def load_spfx_folder( library_id: str, folder_id: str ) -> Any
```

Load a SharePoint folder.

#### 🎯 Purpose

Load a SharePoint folder using the SharePoint loader.

#### 📥 Arguments

- `library_id`
  - SharePoint document-library identifier.
- `folder_id`
  - Provider folder identifier used to load folder contents.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_text

**Index:** 86

```python
def load_text( path: str, encoding: Optional[str]=None ) -> Any
```

Load a plain-text file.

#### 🎯 Purpose

Load a plain-text file using the text loader.

#### 📥 Arguments

- `path`
  - Local file path used by the loader.
- `encoding`
  - Optional file encoding passed to the backing loader.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_web

**Index:** 87

```python
def load_web( urls: str | List[str], recursive: bool=False, max_depth: int=2, prevent_outside: bool=True, timeout: int=10, ignore: bool=True, progress: bool=True ) -> Any
```

Load web documents.

#### 🎯 Purpose

Load web documents using the web loader. Boolean options control retrieval depth or
    supplemental content.

#### 📥 Arguments

- `urls`
  - URL string or URL list used as web-loader input.
- `recursive`
  - Whether nested folders, links, or provider resources should be traversed.
- `max_depth`
  - Maximum recursion depth.
- `prevent_outside`
  - Whether recursive web loading should exclude pages outside the seed domain.
- `timeout`
  - Maximum time in seconds to wait for the operation.
- `ignore`
  - Whether individual loading failures should be skipped when supported.
- `progress`
  - Whether the underlying loader should report progress.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

ValueError: Raised when a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_web_pages

**Index:** 88

```python
def load_web_pages( urls: List[str], depth: int=2, timeout: int=10, ignore: bool=True, progress: bool=True ) -> Any
```

Load static web pages.

#### 🎯 Purpose

Load static web pages using the web loader.

#### 📥 Arguments

- `urls`
  - URL string or URL list used as web-loader input.
- `depth`
  - Maximum recursion depth.
- `timeout`
  - Maximum time in seconds to wait for the operation.
- `ignore`
  - Whether individual loading failures should be skipped when supported.
- `progress`
  - Whether the underlying loader should report progress.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_web_recursive

**Index:** 89

```python
def load_web_recursive( url: str, depth: int=2, max_time: int=10, ignore: bool=True ) -> Any
```

Recursively load web documents.

#### 🎯 Purpose

Recursively load web documents using the web loader.

#### 📥 Arguments

- `url`
  - URL used by the web or repository loader.
- `depth`
  - Maximum recursion depth.
- `max_time`
  - Maximum request or crawl time in seconds.
- `ignore`
  - Whether individual loading failures should be skipped when supported.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_wikipedia

**Index:** 90

```python
def load_wikipedia( question: str ) -> Any
```

Load Wikipedia articles.

#### 🎯 Purpose

Load Wikipedia articles using the Wikipedia loader. The query text determines the records or
    documents matched by the provider.

#### 📥 Arguments

- `question`
  - Search query or prompt submitted to the backing loader.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_word

**Index:** 91

```python
def load_word( path: str ) -> Any
```

Load a Word document.

#### 🎯 Purpose

Load a Word document using the Word loader.

#### 📥 Arguments

- `path`
  - Local file path used by the loader.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_xml

**Index:** 92

```python
def load_xml( filepath: str ) -> Any
```

Load an XML document.

#### 🎯 Purpose

Load an XML document using the XML loader.

#### 📥 Arguments

- `filepath`
  - Local file path used by the loader.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 load_xml_tree

**Index:** 93

```python
def load_xml_tree( filepath: str ) -> Any
```

Parse an XML document tree.

#### 🎯 Purpose

Parse an XML document tree using the XML loader.

#### 📥 Arguments

- `filepath`
  - Local file path used by the loader.

#### 📤 Returns

etree._ElementTree | None: XML elements matching the requested XPath expression.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 nltk_chunk_sentences

**Index:** 94

```python
def nltk_chunk_sentences( text: str, size: int=15 ) -> DataFrame | None
```

Group sentence tokens into fixed-size chunks and return them as tabular data.

#### 🎯 Purpose

Tokenizes lowercase text into sentences, groups the sentences into fixed-size chunks, and
    returns a DataFrame of chunk strings. This provides a sentence-level chunking utility for
    review or dataset preparation.

#### 📥 Arguments

- `text`
  - Text value to process.
- `size`
  - Maximum number of tokens or sentences grouped into each chunk.

#### 📤 Returns

DataFrame | None: Pandas DataFrame containing the processed output when the operation
    succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 nltk_chunk_words

**Index:** 95

```python
def nltk_chunk_words( text: str, size: int=5 ) -> DataFrame | None
```

Group word tokens into fixed-size chunks and return them as tabular data.

#### 🎯 Purpose

Tokenizes lowercase text into words, groups the tokens into fixed-size chunks, and returns a
    DataFrame of chunk strings. This provides a simple word-level chunking utility for downstream
    vector or dataset generation.

#### 📥 Arguments

- `text`
  - Text value to process.
- `size`
  - Maximum number of tokens or sentences grouped into each chunk.

#### 📤 Returns

DataFrame | None: Pandas DataFrame containing the processed output when the operation
    succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 nltk_named_entity_recognition

**Index:** 96

```python
def nltk_named_entity_recognition( text: str ) -> List[Tuple[str, str]] | None
```

Extract named-entity text and entity labels from tagged tokens.

#### 🎯 Purpose

Lowercases text, tokenizes and tags it, then applies NLTK named-entity chunking. Entity text
    and labels are collected into tuples for downstream review or extraction workflows.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

List[ Tuple[ str, str ] ] | None: List of text and label tuples when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 nltk_pos_tagger

**Index:** 97

```python
def nltk_pos_tagger( text: str ) -> List[Tuple[str, str]] | None
```

Assign part-of-speech tags to lowercased word tokens.

#### 🎯 Purpose

Lowercases and tokenizes text, then assigns NLTK part-of-speech tags to each token. The tagged
    sequence is stored on the instance and returned for syntactic analysis.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

List[ Tuple[ str, str ] ] | None: List of text and label tuples when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 nltk_sentence_tokenizer

**Index:** 98

```python
def nltk_sentence_tokenizer( text: str ) -> List[str] | None
```

Tokenize text into lowercased sentence strings.

#### 🎯 Purpose

Lowercases text and tokenizes it into sentence strings with NLTK. The resulting sentences are
    stored on the parser instance and returned to the caller.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

List[ str ] | None: List of processed text values when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 nltk_word_lemmatizer

**Index:** 99

```python
def nltk_word_lemmatizer( text: str ) -> List[str] | None
```

Lemmatize lowercased word tokens with the configured WordNet lemmatizer.

#### 🎯 Purpose

Lowercases text, tokenizes it, and applies WordNet lemmatization to each non-empty token. This
    produces normalized lexical forms suitable for downstream analysis.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

List[ str ] | None: List of processed text values when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 nltk_word_stemmer

**Index:** 100

```python
def nltk_word_stemmer( text: str ) -> List[str] | None
```

Stem lowercased word tokens with the configured Porter stemmer.

#### 🎯 Purpose

Lowercases text, tokenizes it, and applies Porter stemming to each non-empty token. This
    produces stemmed tokens for lexical normalization workflows.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

List[ str ] | None: List of processed text values when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 nltk_word_tokenizer

**Index:** 101

```python
def nltk_word_tokenizer( text: str ) -> List[str] | None
```

Tokenize text into lowercased word tokens.

#### 🎯 Purpose

Lowercases text and tokenizes it into word tokens with NLTK. The resulting list is also stored
    on the parser instance for reuse by later NLTK operations.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

List[ str ] | None: List of processed text values when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_chunk_data

**Index:** 102

```python
def preprocess_chunk_data( filepath: str, size: int=10 ) -> DataFrame | None
```

Chunk a single text file into fixed-size word groups represented as tabular data.

#### 🎯 Purpose

Reads a single text file, filters recognized English alphabetic tokens, groups them into
    fixed-size chunks, and returns the chunk rows as a DataFrame. This provides a compact dataset-
    ready representation of token groups.

#### 📥 Arguments

- `filepath`
  - Path to the local source file.
- `size`
  - Maximum number of tokens or sentences grouped into each chunk.

#### 📤 Returns

DataFrame | None: Pandas DataFrame containing the processed output when the operation
    succeeds.

#### ⚠️ Raises

FileNotFoundError: If a required local file or matched path does not exist.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_chunk_datasets

**Index:** 103

```python
def preprocess_chunk_datasets( source: str, destination: str, size: int=10 ) -> DataFrame
```

Clean and chunk a directory of text files into spreadsheet datasets.

#### 🎯 Purpose

Processes all text files in a directory through cleaning, tokenization, fixed-size chunking,
    and Excel export. This creates spreadsheet datasets suitable for review, labeling, or later
    ingestion.

#### 📥 Arguments

- `source`
  - Directory containing source text files.
- `destination`
  - Directory where generated output files are written.
- `size`
  - Maximum number of tokens or sentences grouped into each chunk.

#### 📤 Returns

DataFrame: Pandas DataFrame containing the processed output.

#### ⚠️ Raises

FileNotFoundError: If a required local file or matched path does not exist.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_chunk_files

**Index:** 104

```python
def preprocess_chunk_files( source: str, destination: str ) -> None
```

Split text files into sentence chunks and write chunked output files.

#### 🎯 Purpose

Reads each file in a source directory, splits text into sentences, and writes the resulting
    sentence sequence to matching output files. This prepares cleaned corpora for chunk-based
    downstream workflows.

#### 📥 Arguments

- `source`
  - Directory containing source text files.
- `destination`
  - Directory where generated output files are written.

#### 📤 Returns

None: The operation completes without producing a return value.

#### ⚠️ Raises

FileNotFoundError: If a required local file or matched path does not exist.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_clean_file

**Index:** 105

```python
def preprocess_clean_file( filepath: str ) -> str | None
```

Apply the standard Fonky text-cleaning pipeline to a single file.

#### 🎯 Purpose

Runs a single file through the parser cleaning pipeline, including whitespace normalization,
    encoding cleanup, symbol removal, fragment filtering, lemmatization, and stop-word removal.
    The method returns the cleaned text instead of writing a file.

#### 📥 Arguments

- `filepath`
  - Path to the local source file.

#### 📤 Returns

str | None: Processed text value when the operation succeeds.

#### ⚠️ Raises

FileNotFoundError: If a required local file or matched path does not exist.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_clean_files

**Index:** 106

```python
def preprocess_clean_files( source: str, destination: str ) -> None
```

Apply the standard Fonky text-cleaning pipeline to every file in a directory.

#### 🎯 Purpose

Processes every file in a source directory through the standard cleaning pipeline and writes
    cleaned text to a destination directory. This supports batch preparation of corpora before
    chunking or dataset creation.

#### 📥 Arguments

- `source`
  - Directory containing source text files.
- `destination`
  - Directory where generated output files are written.

#### 📤 Returns

None: The operation completes without producing a return value.

#### ⚠️ Raises

FileNotFoundError: If a required local file or matched path does not exist.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_collapse_whitespace

**Index:** 107

```python
def preprocess_collapse_whitespace( text: str ) -> str | None
```

Normalize spacing by lowercasing text and collapsing repeated whitespace.

#### 🎯 Purpose

Creates a compact lowercase representation of text by splitting on whitespace and joining
    tokens with single spaces. This prepares raw text for deterministic comparison, cleaning, and
    tokenization steps.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str | None: Processed text value when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_convert_jsonl

**Index:** 108

```python
def preprocess_convert_jsonl( source: str, destination: str, size: int=10 ) -> None
```

Convert text files into line-oriented JSON-like chunk output.

#### 🎯 Purpose

Splits text files into fixed-size token groups and writes each group using a JSON-like line-
    oriented representation. This supports quick conversion of raw text corpora into chunked
    training or testing artifacts.

#### 📥 Arguments

- `source`
  - Directory containing source text files.
- `destination`
  - Directory where generated output files are written.
- `size`
  - Maximum number of tokens or sentences grouped into each chunk.

#### 📤 Returns

None: The operation completes without producing a return value.

#### ⚠️ Raises

FileNotFoundError: If a required local file or matched path does not exist.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_create_frequency_distribution

**Index:** 109

```python
def preprocess_create_frequency_distribution( tokens: List[str] ) -> DataFrame | None
```

Build a word-frequency table from a token sequence.

#### 🎯 Purpose

Counts token occurrences with NLTK frequency distribution support and returns a labeled pandas
    DataFrame. The output provides a simple word-frequency table for analysis and reporting.

#### 📥 Arguments

- `tokens`
  - Token sequence used by the processing operation.

#### 📤 Returns

DataFrame | None: Pandas DataFrame containing the processed output when the operation
    succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_create_vectors

**Index:** 110

```python
def preprocess_create_vectors( tokens: List[str] ) -> DataFrame | None
```

Create TF-IDF vectors for token values.

#### 🎯 Purpose

Builds one-token documents, fits a TF-IDF vectorizer, and maps each token to its vector
    representation. This supplies lightweight vector features for lexical comparison workflows.

#### 📥 Arguments

- `tokens`
  - Token sequence used by the processing operation.

#### 📤 Returns

DataFrame | None: Pandas DataFrame containing the processed output when the operation
    succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_create_vocabulary

**Index:** 111

```python
def preprocess_create_vocabulary( tokens: List[str] ) -> Series | None
```

Extract the vocabulary column from a token-frequency table.

#### 🎯 Purpose

Counts token occurrences and returns the unique token column as a pandas Series. This gives
    downstream routines a vocabulary list derived from the active token stream.

#### 📥 Arguments

- `tokens`
  - Token sequence used by the processing operation.

#### 📤 Returns

Series | None: Pandas Series containing the processed output when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_create_wordbag

**Index:** 112

```python
def preprocess_create_wordbag( tokens: List[str] ) -> DataFrame | None
```

Build a bag-of-words table from a token sequence.

#### 🎯 Purpose

Builds a bag-of-words representation by extracting unique terms from the token frequency
    distribution. The returned DataFrame supports simple vocabulary inspection and feature
    preparation.

#### 📥 Arguments

- `tokens`
  - Token sequence used by the processing operation.

#### 📤 Returns

DataFrame | None: Pandas DataFrame containing the processed output when the operation
    succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_encode_sentences

**Index:** 113

```python
def preprocess_encode_sentences( tokens: List[str], model: str='all-MiniLM-L6-v2' ) -> Tuple[List[str], np.ndarray]
```

Generate sentence-transformer embeddings for normalized token values.

#### 🎯 Purpose

Lemmatizes token values and encodes them with a SentenceTransformer model. The returned tuple
    pairs token text with a NumPy embedding matrix for semantic-search workflows.

#### 📥 Arguments

- `tokens`
  - Token sequence used by the processing operation.
- `model`
  - Sentence-transformer model used to encode the query or token sequence.

#### 📤 Returns

Tuple[ List[ str ], np.ndarray ]: Token values paired with the generated embedding matrix.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_load_text

**Index:** 114

```python
def preprocess_load_text( filepath: str ) -> str | None
```

Read UTF-8 text from a local file and return the raw string.

#### 🎯 Purpose

Loads a local text file using UTF-8 with ignored decode errors so downstream cleaning routines
    can operate on a plain string. The method records the active file path and raises a project
    Error when the file cannot be read.

#### 📥 Arguments

- `filepath`
  - Path to the local source file.

#### 📤 Returns

str | None: Processed text value when the operation succeeds.

#### ⚠️ Raises

FileNotFoundError: If a required local file or matched path does not exist.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_normalize_text

**Index:** 115

```python
def preprocess_normalize_text( text: str ) -> str | None
```

Convert text to lowercase for stable downstream comparison and tokenization.

#### 🎯 Purpose

Converts text to lowercase without otherwise changing content. This provides a simple
    normalization stage for workflows that need case-insensitive matching or tokenization.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str | None: Processed text value when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_remove_encodings

**Index:** 116

```python
def preprocess_remove_encodings( text: str ) -> str | None
```

Resolve HTML entities, normalize Unicode characters, and remove control characters.

#### 🎯 Purpose

Decodes common escaped sequences when possible, resolves HTML entities, normalizes Unicode to
    compatibility form, and strips control characters. This reduces text artifacts from scraped,
    copied, or encoded sources.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str | None: Processed text value when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_remove_errors

**Index:** 117

```python
def preprocess_remove_errors( text: str ) -> str
```

Filter tokens against the NLTK English words corpus.

#### 🎯 Purpose

Uses the NLTK English words corpus as a vocabulary filter and keeps only tokens recognized by
    that corpus. This reduces obvious OCR, spelling, and parsing artifacts before later analysis.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str: Processed text value produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_remove_fragments

**Index:** 118

```python
def preprocess_remove_fragments( text: str ) -> str | None
```

Remove very short token fragments from normalized text.

#### 🎯 Purpose

Removes short text fragments that are unlikely to be useful lexical units. This helps reduce
    noise produced by OCR, markup stripping, punctuation removal, and aggressive token cleanup.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str | None: Processed text value when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_remove_headers

**Index:** 119

```python
def preprocess_remove_headers( filepath: str, lines: int=50, headers: int=3, footers: int=3 ) -> str | None
```

Detect and remove repeated page headers and footers from a text file.

#### 🎯 Purpose

Splits a text file into page-sized blocks and identifies repeated leading and trailing line
    groups. Matching header and footer blocks are removed to produce cleaner body text for
    analysis.

#### 📥 Arguments

- `filepath`
  - Path to the local source file.
- `lines`
  - Number of lines treated as one page during header and footer detection.
- `headers`
  - Number of leading lines considered as a repeated page header.
- `footers`
  - Number of trailing lines considered as a repeated page footer.

#### 📤 Returns

str | None: Processed text value when the operation succeeds.

#### ⚠️ Raises

FileNotFoundError: If a required local file or matched path does not exist.
    ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_remove_html

**Index:** 120

```python
def preprocess_remove_html( text: str ) -> str | None
```

Extract visible text from HTML markup.

#### 🎯 Purpose

Parses HTML input with BeautifulSoup and extracts visible text content. This allows raw HTML
    fragments or pages to enter the same cleaning pipeline used for plain text.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str | None: Processed text value when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_remove_images

**Index:** 121

```python
def preprocess_remove_images( text: str ) -> str
```

Remove Markdown image references, HTML image elements, and direct image URLs.

#### 🎯 Purpose

Removes Markdown image syntax, HTML image tags, and direct image URLs from text. This keeps
    descriptive text while excluding image-only references that do not support text processing.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str: Processed text value produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_remove_markdown

**Index:** 122

```python
def preprocess_remove_markdown( text: str ) -> str | None
```

Remove common Markdown links, image syntax, and formatting markers.

#### 🎯 Purpose

Removes common Markdown link, image, and inline-formatting syntax from lowercase text. This
    converts README-style or documentation-style content into cleaner text for downstream
    analysis.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str | None: Processed text value when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_remove_numbers

**Index:** 123

```python
def preprocess_remove_numbers( text: str ) -> str | None
```

Remove decimal digits from text.

#### 🎯 Purpose

Removes digit sequences from lowercase text. This supports workflows that need lexical content
    without numeric values.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str | None: Processed text value when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_remove_numerals

**Index:** 124

```python
def preprocess_remove_numerals( text: str ) -> str | None
```

Remove Roman-numeral patterns from text.

#### 🎯 Purpose

Applies the configured Roman-numeral expression to lowercase text and replaces matching
    numeral tokens with spaces. This reduces numbering artifacts in outlines, headings, and
    document sections.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str | None: Processed text value when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_remove_punctuation

**Index:** 125

```python
def preprocess_remove_punctuation( text: str ) -> str
```

Strip punctuation from tokenized text while preserving word and spacing content.

#### 🎯 Purpose

Tokenizes lowercase text and removes punctuation marks from each token. The method preserves
    alphanumeric token content while returning a whitespace-joined string for later cleaning
    stages.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str: Processed text value produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_remove_stopwords

**Index:** 126

```python
def preprocess_remove_stopwords( text: str ) -> str | None
```

Remove English stop words from tokenized text.

#### 🎯 Purpose

Tokenizes lowercase text and removes standard English stop words. This leaves a reduced token
    stream better suited for frequency analysis, vocabulary extraction, and embedding preparation.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str | None: Processed text value when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_remove_symbols

**Index:** 127

```python
def preprocess_remove_symbols( text: str ) -> str | None
```

Remove configured symbol characters from normalized text.

#### 🎯 Purpose

Removes characters listed in the parser symbol set from lowercase text. This produces cleaner
    text for tokenization, word-frequency generation, and embedding workflows.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str | None: Processed text value when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_remove_xml

**Index:** 128

```python
def preprocess_remove_xml( text: str ) -> str
```

Extract inner text from XML-like markup while recovering malformed fragments when possible.

#### 🎯 Purpose

Wraps XML-like text in a temporary root node, parses it with recovery enabled, and
    concatenates element text and tail content. This retains readable content while discarding
    markup structure.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

str: Processed text value produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_semantic_search

**Index:** 129

```python
def preprocess_semantic_search( query: str, tokens: List[str], model: str='all-MiniLM-L6-v2', top: int=5 ) -> List[Tuple[str, float]]
```

Search token content by semantic similarity.

#### 🎯 Purpose

Creates sentence embeddings internally and returns the highest-scoring token matches for
    the supplied query. The wrapper keeps NumPy arrays and SentenceTransformer instances out
    of the agent-facing JSON schema.

#### 📥 Arguments

- `query`
  - Natural-language query used for semantic matching.
- `tokens`
  - Text values searched for semantic similarity.
- `model`
  - Sentence-transformer model name used to create embeddings.
- `top`
  - Maximum number of matches to return.

#### 📤 Returns

List[Tuple[str, float]]: Highest-scoring text values and similarity scores.

---

### 🔧 preprocess_split_pages

**Index:** 130

```python
def preprocess_split_pages( filepath: str, num: int=50 ) -> List[str] | None
```

Split a text file into page-sized text blocks.

#### 🎯 Purpose

Reads a plain-text file and splits it into page-sized blocks using form-feed characters when
    available or fixed line counts otherwise. The resulting list can be used for page- level
    cleaning and analysis.

#### 📥 Arguments

- `filepath`
  - Path to the local source file.
- `num`
  - Number of lines used as the fallback page boundary.

#### 📤 Returns

List[ str ] | None: List of processed text values when the operation succeeds.

#### ⚠️ Raises

FileNotFoundError: If a required local file or matched path does not exist.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_split_paragraphs

**Index:** 131

```python
def preprocess_split_paragraphs( filepath: str ) -> DataFrame | None
```

Read a text file and return paragraph-like text blocks as tabular data.

#### 🎯 Purpose

Reads a text file and converts separated text blocks into a pandas DataFrame. The fallback
    Latin-1 branch preserves the ability to process files that fail UTF-8 decoding.

#### 📥 Arguments

- `filepath`
  - Path to the local source file.

#### 📤 Returns

DataFrame | None: Pandas DataFrame containing the processed output when the operation
    succeeds.

#### ⚠️ Raises

FileNotFoundError: If a required local file or matched path does not exist.

---

### 🔧 preprocess_split_sentences

**Index:** 132

```python
def preprocess_split_sentences( text: str ) -> List[str] | None
```

Split text into sentence strings using NLTK sentence tokenization.

#### 🎯 Purpose

Applies NLTK sentence tokenization to lowercase text and returns the resulting sentence list.
    This provides sentence boundaries for chunking, cleaning, and dataset generation workflows.

#### 📥 Arguments

- `text`
  - Text value to process.

#### 📤 Returns

List[ str ] | None: List of processed text values when the operation succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 preprocess_tiktokenize

**Index:** 133

```python
def preprocess_tiktokenize( text: str, encoding: str='cl100k_base' ) -> DataFrame | None
```

Encode text with a tiktoken tokenizer and return token identifiers as tabular data.

#### 🎯 Purpose

Encodes lowercase text using the requested tiktoken encoding and returns token identifiers in
    a pandas DataFrame. This supports token inspection and model-facing preprocessing workflows.

#### 📥 Arguments

- `text`
  - Text value to process.
- `encoding`
  - Tiktoken encoding name used for tokenization.

#### 📤 Returns

DataFrame | None: Pandas DataFrame containing the processed output when the operation
    succeeds.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
        project error type.

---

### 🔧 read_pdf

**Index:** 134

```python
def read_pdf( path: str, mode: str='single' ) -> Any
```

Read a PDF file.

#### 🎯 Purpose

Read a PDF file using the PDF reader.

#### 📥 Arguments

- `path`
  - Local file path used by the loader.
- `mode`
  - Operation mode used to select the provider or processing workflow.

#### 📤 Returns

List[Document] | None: LangChain documents loaded from the requested source.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 render_web_page

**Index:** 135

```python
def render_web_page( url: str, timeout: int=15, headers: Optional[Dict[str, str]]=None, use_playwright: bool=False ) -> Any
```

Render a dynamic web page with Playwright.

#### 🎯 Purpose

Render a dynamic web page with Playwright.

#### 📥 Arguments

- `url`
  - URL or URI value used as the request or parsing source.
- `timeout`
  - Request timeout in seconds.
- `headers`
  - Optional HTTP headers applied to web requests.
- `use_playwright`
  - Whether browser-backed rendering should be used for dynamic pages.

#### 📤 Returns

str: Text produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 request_directions

**Index:** 136

```python
def request_directions( origin: str, destination: str, mode: str='driving' ) -> Any
```

Request directions.

#### 🎯 Purpose

Request directions using Google Maps.

#### 📥 Arguments

- `origin`
  - Starting address or place for a routing request.
- `destination`
  - Destination address or place for a routing request.
- `mode`
  - Operation mode used to select the provider or processing workflow.

#### 📤 Returns

Dict[str, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 scrape_articles

**Index:** 137

```python
def scrape_articles( uri: str ) -> Any
```

Extract article text.

#### 🎯 Purpose

Extract article text using Fonky's web extractor implementation.

#### 📥 Arguments

- `uri`
  - Fully qualified URI of the target HTML page.

#### 📤 Returns

List[str] | None: Text or identifier values produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 scrape_blockquotes

**Index:** 138

```python
def scrape_blockquotes( uri: str ) -> Any
```

Extract blockquote text.

#### 🎯 Purpose

Extract blockquote text using Fonky's web extractor implementation.

#### 📥 Arguments

- `uri`
  - Fully qualified URI of the target HTML document.

#### 📤 Returns

List[str] | None: Text or identifier values produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 scrape_crawler_page

**Index:** 139

```python
def scrape_crawler_page( url: str, include_title: bool=True, include_basic_text: bool=True, include_raw_html: bool=False, selected_methods: Optional[List[str]]=None, request_timeout: int=10, max_bytes: int=1000000, headers: Optional[Dict[str, str]]=None, use_playwright: bool=False ) -> Any
```

Extract crawler page from an HTML page.

#### 🎯 Purpose

Extract crawler page from an HTML page using Fonky's web crawler implementation.

#### 📥 Arguments

- `url`
  - URL or URI value used as the request or parsing source.
- `include_title`
  - Whether to include title in the result.
- `include_basic_text`
  - Whether to include basic text in the result.
- `include_raw_html`
  - Whether to include raw html in the result.
- `selected_methods`
  - Extraction method names to execute against the supplied HTML.
- `request_timeout`
  - Request timeout in seconds.
- `max_bytes`
  - Maximum bytes permitted by the operation.
- `headers`
  - Optional HTTP headers applied to web requests.
- `use_playwright`
  - Whether browser-backed rendering should be used for dynamic pages.

#### 📤 Returns

Dict[str, Any]: Structured mapping produced by the operation.

#### ⚠️ Raises

Exception: If the delegated implementation raises an operational failure.

---

### 🔧 scrape_divisions

**Index:** 140

```python
def scrape_divisions( uri: str ) -> Any
```

Extract division text.

#### 🎯 Purpose

Extract division text using Fonky's web extractor implementation.

#### 📥 Arguments

- `uri`
  - Fully qualified URI of the target HTML document.

#### 📤 Returns

List[str] | None: Text or identifier values produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 scrape_headings

**Index:** 141

```python
def scrape_headings( uri: str ) -> Any
```

Extract heading text.

#### 🎯 Purpose

Extract heading text using Fonky's web extractor implementation.

#### 📥 Arguments

- `uri`
  - Fully qualified URI of the target HTML document.

#### 📤 Returns

List[str] | None: Heading text values produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 scrape_hyperlinks

**Index:** 142

```python
def scrape_hyperlinks( uri: str ) -> Any
```

Extract hyperlinks from an HTML page.

#### 🎯 Purpose

Extract hyperlinks from an HTML page using Fonky's web extractor implementation.

#### 📥 Arguments

- `uri`
  - Fully qualified URI of the target HTML page.

#### 📤 Returns

List[str] | None: Hyperlink values produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 scrape_images

**Index:** 143

```python
def scrape_images( uri: str ) -> Any
```

Extract image references.

#### 🎯 Purpose

Extract image references using Fonky's web extractor implementation.

#### 📥 Arguments

- `uri`
  - Fully qualified URI of the target HTML page.

#### 📤 Returns

List[str] | None: Image references produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 scrape_lists

**Index:** 144

```python
def scrape_lists( uri: str ) -> Any
```

Extract list item text.

#### 🎯 Purpose

Extract list item text using Fonky's web extractor implementation.

#### 📥 Arguments

- `uri`
  - Fully qualified URI of the target HTML page.

#### 📤 Returns

List[str] | None: Text or identifier values produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 scrape_paragraphs

**Index:** 145

```python
def scrape_paragraphs( uri: str ) -> Any
```

Extract paragraph text.

#### 🎯 Purpose

Extract paragraph text using Fonky's web extractor implementation.

#### 📥 Arguments

- `uri`
  - Fully qualified URI of the target HTML document.

#### 📤 Returns

List[str] | None: Paragraph text values produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 scrape_sections

**Index:** 146

```python
def scrape_sections( uri: str ) -> Any
```

Extract section text.

#### 🎯 Purpose

Extract section text using Fonky's web extractor implementation.

#### 📥 Arguments

- `uri`
  - Fully qualified URI of the target HTML document.

#### 📤 Returns

List[str] | None: Text or identifier values produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 scrape_tables

**Index:** 147

```python
def scrape_tables( uri: str ) -> Any
```

Extract table cell text.

#### 🎯 Purpose

Extract table cell text using Fonky's web extractor implementation.

#### 📥 Arguments

- `uri`
  - Fully qualified URI of the target HTML document.

#### 📤 Returns

List[str] | None: Table cell text values produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 scrape_web_page

**Index:** 148

```python
def scrape_web_page( url: str, time: int=10 ) -> Any
```

Fetch a web page for extraction.

#### 🎯 Purpose

Fetch a web page for extraction using Fonky's web extractor implementation.

#### 📥 Arguments

- `url`
  - Absolute URL to fetch.
- `time`
  - Request timeout in seconds.

#### 📤 Returns

Result | None: Fonky result wrapper containing the provider or HTTP response.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 scraper_html_to_text

**Index:** 149

```python
def scraper_html_to_text( html: str ) -> Any
```

Convert HTML to plain text.

#### 🎯 Purpose

Convert HTML to plain text.

#### 📥 Arguments

- `html`
  - Raw HTML string to convert.

#### 📤 Returns

str: Text produced by the operation.

#### ⚠️ Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---

### 🔧 validate_address

**Index:** 150

```python
def validate_address( address: List[str] ) -> Any
```

Validate address.

#### 🎯 Purpose

Validate address using Google Maps.

#### 📥 Arguments

- `address`
  - Street address or place description used for geocoding, validation, or routing.

#### 📤 Returns

Dict[Any, Any] | None: Structured mapping produced by the operation.

#### ⚠️ Raises

TypeError: If a supplied value has an unsupported type.
    ValueError: If a required value is missing, blank, or outside the supported range.
    Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
        the project error type.

---
