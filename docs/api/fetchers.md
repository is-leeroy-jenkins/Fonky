# API Reference: `fetchers.py`

`fetchers.py` contains the remote retrieval implementations for web access, crawling, archives, search, government/public data, weather, environment, geospatial services, astronomy, aviation, health, and demographics.

## Module Inventory

- **Classes:** 49
- **Top-level functions:** 2

## Module-Level Functions

| Function | Signature | Purpose |
|---|---|---|
| `throw_if()` | `throw_if( name: str, value: object ) -> None` | Throw if. |
| `encode_image()` | `encode_image( path: str ) -> str` | Encode image. |

## Classes

| Class | Constructor | Public Methods | Functional Wrappers |
|---|---|---:|---:|
| [`Fetcher`](#fetcher) | `Fetcher( self: Any ) -> None` | 1 | 0 |
| [`WebFetcher`](#webfetcher) | `WebFetcher( self: Any ) -> None` | 20 | 5 |
| [`WebCrawler`](#webcrawler) | `WebCrawler( self: Any, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> None` | 4 | 3 |
| [`ArXiv`](#arxiv) | `ArXiv( self: Any, max_documents: int = 5, full_documents: bool = False, include_metadata: bool = False ) -> None` | 1 | 1 |
| [`GoogleDrive`](#googledrive) | `GoogleDrive( self: Any ) -> None` | 4 | 1 |
| [`Wikipedia`](#wikipedia) | `Wikipedia( self: Any, language: str = 'en', max_documents: int = 5, include_metadata: bool = False ) -> None` | 1 | 1 |
| [`TheNews`](#thenews) | `TheNews( self: Any ) -> None` | 1 | 1 |
| [`GoogleSearch`](#googlesearch) | `GoogleSearch( self: Any ) -> None` | 1 | 1 |
| [`GoogleMaps`](#googlemaps) | `GoogleMaps( self: Any ) -> None` | 5 | 4 |
| [`GoogleWeather`](#googleweather) | `GoogleWeather( self: Any ) -> None` | 8 | 5 |
| [`NavalObservatory`](#navalobservatory) | `NavalObservatory( self: Any ) -> None` | 6 | 1 |
| [`SatelliteCenter`](#satellitecenter) | `SatelliteCenter( self: Any ) -> None` | 4 | 1 |
| [`EarthObservatory`](#earthobservatory) | `EarthObservatory( self: Any ) -> None` | 6 | 1 |
| [`GlobalImagery`](#globalimagery) | `GlobalImagery( self: Any ) -> None` | 6 | 3 |
| [`NearbyObjects`](#nearbyobjects) | `NearbyObjects( self: Any ) -> None` | 7 | 1 |
| [`OpenScience`](#openscience) | `OpenScience( self: Any ) -> None` | 8 | 1 |
| [`SpaceWeather`](#spaceweather) | `SpaceWeather( self: Any ) -> None` | 3 | 1 |
| [`AstroCatalog`](#astrocatalog) | `AstroCatalog( self: Any ) -> Any` | 6 | 1 |
| [`AstroQuery`](#astroquery) | `AstroQuery( self: Any ) -> None` | 5 | 1 |
| [`StarMap`](#starmap) | `StarMap( self: Any ) -> None` | 6 | 1 |
| [`GovData`](#govdata) | `GovData( self: Any ) -> None` | 8 | 1 |
| [`StarChart`](#starchart) | `StarChart( self: Any ) -> None` | 7 | 1 |
| [`Congress`](#congress) | `Congress( self: Any ) -> None` | 16 | 1 |
| [`InternetArchive`](#internetarchive) | `InternetArchive( self: Any ) -> None` | 5 | 1 |
| [`OpenWeather`](#openweather) | `OpenWeather( self: Any ) -> None` | 6 | 1 |
| [`HistoricalWeather`](#historicalweather) | `HistoricalWeather( self: Any ) -> None` | 4 | 1 |
| [`Grokipedia`](#grokipedia) | `Grokipedia( self: Any ) -> None` | 4 | 1 |
| [`GoogleGeocoding`](#googlegeocoding) | `GoogleGeocoding( self: Any ) -> None` | 6 | 1 |
| [`CensusData`](#censusdata) | `CensusData( self: Any ) -> None` | 7 | 1 |
| [`Socrata`](#socrata) | `Socrata( self: Any ) -> None` | 8 | 1 |
| [`HealthData`](#healthdata) | `HealthData( self: Any ) -> None` | 8 | 1 |
| [`GlobalHealthData`](#globalhealthdata) | `GlobalHealthData( self: Any ) -> None` | 5 | 1 |
| [`UnitedNations`](#unitednations) | `UnitedNations( self: Any ) -> None` | 5 | 1 |
| [`WorldPopulation`](#worldpopulation) | `WorldPopulation( self: Any ) -> None` | 8 | 1 |
| [`Wonder`](#wonder) | `Wonder( self: Any ) -> None` | 6 | 1 |
| [`USGSEarthquakes`](#usgsearthquakes) | `USGSEarthquakes( self: Any ) -> None` | 16 | 1 |
| [`USGSWaterData`](#usgswaterdata) | `USGSWaterData( self: Any ) -> None` | 16 | 1 |
| [`USGSTheNationalMap`](#usgsthenationalmap) | `USGSTheNationalMap( self: Any ) -> None` | 14 | 1 |
| [`USGSScienceBase`](#usgssciencebase) | `USGSScienceBase( self: Any ) -> None` | 13 | 1 |
| [`AirNow`](#airnow) | `AirNow( self: Any ) -> None` | 10 | 1 |
| [`ClimateData`](#climatedata) | `ClimateData( self: Any ) -> None` | 13 | 1 |
| [`EoNet`](#eonet) | `EoNet( self: Any ) -> None` | 15 | 1 |
| [`EnviroFacts`](#envirofacts) | `EnviroFacts( self: Any ) -> None` | 11 | 1 |
| [`TidesAndCurrents`](#tidesandcurrents) | `TidesAndCurrents( self: Any ) -> None` | 17 | 1 |
| [`UvIndex`](#uvindex) | `UvIndex( self: Any ) -> None` | 14 | 1 |
| [`PurpleAir`](#purpleair) | `PurpleAir( self: Any ) -> None` | 19 | 1 |
| [`OpenAQ`](#openaq) | `OpenAQ( self: Any ) -> None` | 22 | 1 |
| [`Firms`](#firms) | `Firms( self: Any ) -> None` | 15 | 1 |
| [`OpenSky`](#opensky) | `OpenSky( self: Any ) -> None` | 22 | 1 |

## `Fetcher`

Fetcher fetcher.

```python
Fetcher( self: Any ) -> None
```

**Source:** `fetchers.py`, line 132

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `fetch()` | `fetch( self: Any, query: str, url: str, time: int = 10 ) -> Result \| None` | Fetch base fetcher operations. |

## `WebFetcher`

Web Fetcher fetcher.

```python
WebFetcher( self: Any ) -> None
```

**Source:** `fetchers.py`, line 204

**Functional wrappers:** `fonky.fetch_web_page()`, `fonky.convert_html_to_text()`, `fonky.extract_web_title()`, `fonky.extract_web_links()`, `fonky.extract_web_structured_data()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `fetch()` | `fetch( self: Any, url: str, time: int = 10 ) -> Result \| None` | Fetch HTTP web page retrieval and HTML extraction. |
| `html_to_text()` | `html_to_text( self: Any, html: str ) -> str` | HTML to text. |
| `coerce_items()` | `coerce_items( self: Any, value: Any ) -> List[str]` | Coerce items. |
| `extract_title()` | `extract_title( self: Any, html: str ) -> str` | Extract title. |
| `truncate_text()` | `truncate_text( self: Any, text: str, limit: int = 12000 ) -> str` | Truncate text. |
| `normalize_url()` | `normalize_url( self: Any, base_url: str, href: str ) -> str` | Normalize url. |
| `same_domain()` | `same_domain( self: Any, left_url: str, right_url: str ) -> bool` | Same domain. |
| `extract_links()` | `extract_links( self: Any, base_url: str, html: str ) -> List[str]` | Extract links. |
| `extract_structured_data()` | `extract_structured_data( self: Any, url: str, html: str, selected_methods: Optional[List[str]] = None ) -> Dict[str, List[str]]` | Extract structured data. |
| `scrape_paragraphs()` | `scrape_paragraphs( self: Any, uri: str ) -> List[str] \| None` | Scrape paragraphs. |
| `scrape_lists()` | `scrape_lists( self: Any, uri: str ) -> List[str] \| None` | Scrape lists. |
| `scrape_tables()` | `scrape_tables( self: Any, uri: str ) -> List[str] \| None` | Scrape tables. |
| `scrape_articles()` | `scrape_articles( self: Any, uri: str ) -> List[str] \| None` | Scrape articles. |
| `scrape_headings()` | `scrape_headings( self: Any, uri: str ) -> List[str] \| None` | Scrape headings. |
| `scrape_divisions()` | `scrape_divisions( self: Any, uri: str ) -> List[str] \| None` | Scrape divisions. |
| `scrape_sections()` | `scrape_sections( self: Any, uri: str ) -> List[str] \| None` | Scrape sections. |
| `scrape_blockquotes()` | `scrape_blockquotes( self: Any, uri: str ) -> List[str] \| None` | Scrape blockquotes. |
| `scrape_hyperlinks()` | `scrape_hyperlinks( self: Any, uri: str ) -> List[str] \| None` | Scrape hyperlinks. |
| `scrape_images()` | `scrape_images( self: Any, uri: str ) -> List[str] \| None` | Scrape images. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `WebCrawler`

Web Crawler fetcher.

```python
WebCrawler( self: Any, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> None
```

**Source:** `fetchers.py`, line 1063

**Functional wrappers:** `fonky.crawl_web()`, `fonky.scrape_crawler_page()`, `fonky.render_web_page()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `fetch()` | `fetch( self: Any, url: str, time: int = 10 ) -> Result \| None` | Fetch bounded web crawling and optional browser-rendered scraping. |
| `render_with_playwright()` | `render_with_playwright( self: Any, url: str, timeout: int = 15 ) -> str` | Render with playwright. |
| `scrape_page()` | `scrape_page( self: Any, url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, request_timeout: int = 10, max_bytes: int = 1000000 ) -> Dict[str, Any]` | Scrape page. |
| `crawl()` | `crawl( self: Any, seed_url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, recursive: bool = False, max_depth: int = 1, max_pages: int = 10, same_domain_only: bool = True, request_timeout: int = 10, delay_seconds: float = 0.25, max_bytes: int = 1000000 ) -> Dict[str, Any]` | Crawl. |

## `ArXiv`

Ar Xiv fetcher.

```python
ArXiv( self: Any, max_documents: int = 5, full_documents: bool = False, include_metadata: bool = False ) -> None
```

**Source:** `fetchers.py`, line 1378

**Functional wrappers:** `fonky.fetch_arxiv()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `fetch()` | `fetch( self: Any, question: str, max_documents: int = None, full_documents: bool = None, include_metadata: bool = None ) -> List[Document] \| None` | Fetch ArXiv research document retrieval. |

## `GoogleDrive`

Google Drive fetcher.

```python
GoogleDrive( self: Any ) -> None
```

**Source:** `fetchers.py`, line 1469

**Functional wrappers:** `fonky.fetch_google_drive()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `mime_options()` | `mime_options( self: Any ) -> List[str]` | Mime options. |
| `template_options()` | `template_options( self: Any ) -> List[str]` | Template options. |
| `mode_options()` | `mode_options( self: Any ) -> List[str]` | Mode options. |
| `fetch()` | `fetch( self: Any, question: str, folder_id: str = 'root', results: int = 10, template: str = 'gdrive-query', mime_type: str = None, mode: str = 'documents' ) -> List[Document] \| None` | Fetch Google Drive document retrieval. |

## `Wikipedia`

Wikipedia fetcher.

```python
Wikipedia( self: Any, language: str = 'en', max_documents: int = 5, include_metadata: bool = False ) -> None
```

**Source:** `fetchers.py`, line 1672

**Functional wrappers:** `fonky.fetch_wikipedia()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `fetch()` | `fetch( self: Any, question: str, language: str = None, max_documents: int = None, include_metadata: bool = None ) -> List[Document] \| None` | Fetch Wikipedia document retrieval. |

## `TheNews`

The News fetcher.

```python
TheNews( self: Any ) -> None
```

**Source:** `fetchers.py`, line 1762

**Functional wrappers:** `fonky.fetch_news()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `fetch()` | `fetch( self: Any, endpoint: str = 'all', query: str = '', language: str = 'en', categories: str = '', exclude_categories: str = '', locale: str = '', domains: str = '', exclude_domains: str = '', source_ids: str = '', exclude_source_ids: str = '', published_after: str = '', published_before: str = '', published_on: str = '', sort: str = 'published_at', limit: int = 10, page: int = 1, include_similar: bool = True, headlines_per_category: int = 6, time: int = 10, api_key: str = None ) -> Dict[str, Any]` | Fetch The News API article retrieval. |

## `GoogleSearch`

Google Search fetcher.

```python
GoogleSearch( self: Any ) -> None
```

**Source:** `fetchers.py`, line 1984

**Functional wrappers:** `fonky.fetch_google_search()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `fetch()` | `fetch( self: Any, keywords: str, results: int = 10, start: int = 1, exact_terms: str = '', exclude_terms: str = '', file_type: str = '', date_restrict: str = '', gl: str = '', lr: str = '', safe: str = 'off', search_type: str = '', site_search: str = '', site_search_filter: str = '', sort: str = '', img_size: str = '', img_type: str = '', img_color_type: str = '', img_dominant_color: str = '', time: int = 10, api_key: str = None, cse_id: str = None ) -> Dict[str, Any] \| None` | Fetch Google Custom Search retrieval. |

## `GoogleMaps`

Google Maps fetcher.

```python
GoogleMaps( self: Any ) -> None
```

**Source:** `fetchers.py`, line 2259

**Functional wrappers:** `fonky.geocode_location()`, `fonky.geocode_coordinates()`, `fonky.validate_address()`, `fonky.request_directions()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `geocode_location()` | `geocode_location( self: Any, address: str ) -> Tuple[float, float]` | Geocode location. |
| `geocode_coordinates()` | `geocode_coordinates( self: Any, lat: float, long: float ) -> str \| None` | Geocode coordinates. |
| `validate_address()` | `validate_address( self: Any, address: List[str] ) -> Dict[Any, Any] \| None` | Validate address. |
| `request_directions()` | `request_directions( self: Any, origin: str, destination: str, mode: str = 'driving' ) -> Dict[str, Any] \| None` | Request directions. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `GoogleWeather`

Google Weather fetcher.

```python
GoogleWeather( self: Any ) -> None
```

**Source:** `fetchers.py`, line 2586

**Functional wrappers:** `fonky.fetch_google_weather_current()`, `fonky.fetch_google_weather_hourly_forecast()`, `fonky.fetch_google_weather_daily_forecast()`, `fonky.fetch_google_weather_hourly_history()`, `fonky.fetch_google_weather_alerts()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `resolve_coordinates()` | `resolve_coordinates( self: Any, address: str ) -> Tuple[float, float]` | Resolve coordinates. |
| `request()` | `request( self: Any, path: str, params: Dict[str, Any], time: int = 10 ) -> Dict[str, Any] \| None` | Request Google Weather conditions, forecasts, history, and alerts. |
| `package_response()` | `package_response( self: Any ) -> Dict[str, Any]` | Package response. |
| `fetch_current()` | `fetch_current( self: Any, address: str, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Dict[str, Any] \| None` | Fetch current. |
| `fetch_hourly_forecast()` | `fetch_hourly_forecast( self: Any, address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Dict[str, Any] \| None` | Fetch hourly forecast. |
| `fetch_daily_forecast()` | `fetch_daily_forecast( self: Any, address: str, days: int = 5, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Dict[str, Any] \| None` | Fetch daily forecast. |
| `fetch_hourly_history()` | `fetch_hourly_history( self: Any, address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Dict[str, Any] \| None` | Fetch hourly history. |
| `fetch_alerts()` | `fetch_alerts( self: Any, address: str, language_code: str = 'en', time: int = 10 ) -> Dict[str, Any] \| None` | Fetch alerts. |

## `NavalObservatory`

Naval Observatory fetcher.

```python
NavalObservatory( self: Any ) -> None
```

**Source:** `fetchers.py`, line 3052

**Functional wrappers:** `fonky.fetch_naval_observatory()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_date()` | `validate_date( self: Any, date_value: str ) -> str` | Validate date. |
| `validate_time()` | `validate_time( self: Any, time_value: str ) -> str` | Validate time. |
| `validate_coordinates()` | `validate_coordinates( self: Any, latitude: float, longitude: float ) -> tuple[float, float]` | Validate coordinates. |
| `fetch_celnav()` | `fetch_celnav( self: Any, date_value: str, time_value: str, latitude: float, longitude: float, location_label: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch celnav. |
| `fetch()` | `fetch( self: Any, mode: str = 'celnav', date_value: str = '', time_value: str = '', latitude: float = 0.0, longitude: float = 0.0, location_label: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch U.S. Naval Observatory celestial-navigation data. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `SatelliteCenter`

Satellite Center fetcher.

```python
SatelliteCenter( self: Any ) -> None
```

**Source:** `fetchers.py`, line 3356

**Functional wrappers:** `fonky.fetch_satellite_center()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `fetch_observatories()` | `fetch_observatories( self: Any ) -> Dict[str, Any] \| None` | Fetch observatories. |
| `fetch_ground_stations()` | `fetch_ground_stations( self: Any ) -> Dict[str, Any] \| None` | Fetch ground stations. |
| `fetch_locations()` | `fetch_locations( self: Any, observatories: str, start_time: str, end_time: str, coordinate_systems: str = 'gse', resolution_factor: int = 1, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch locations. |
| `fetch()` | `fetch( self: Any, mode: str = 'observatories', query: str = '', start_time: str = '', end_time: str = '', coordinate_systems: str = 'gse', resolution_factor: int = 1, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch SSC satellite observatory, ground-station, and location data. |

## `EarthObservatory`

Earth Observatory fetcher.

```python
EarthObservatory( self: Any ) -> None
```

**Source:** `fetchers.py`, line 3574

**Functional wrappers:** `fonky.fetch_earth_observatory()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `fetch_events()` | `fetch_events( self: Any, status: str = 'open', category: str = '', source: str = '', limit: int = 20, days: int = 30, start_date: str = '', end_date: str = '', time: int = 20 ) -> Dict[str, Any]` | Fetch events. |
| `fetch_categories()` | `fetch_categories( self: Any, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch categories. |
| `fetch_sources()` | `fetch_sources( self: Any, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch sources. |
| `fetch_layers()` | `fetch_layers( self: Any, category: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch layers. |
| `fetch()` | `fetch( self: Any, mode: str = 'events', status: str = 'open', category: str = '', source: str = '', limit: int = 20, days: int = 30, start_date: str = '', end_date: str = '', time: int = 20 ) -> Dict[str, Any]` | Fetch NASA EONET events, categories, sources, and layers. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `GlobalImagery`

Global Imagery fetcher.

```python
GlobalImagery( self: Any ) -> None
```

**Source:** `fetchers.py`, line 3934

**Functional wrappers:** `fonky.fetch_global_imagery_wms_map()`, `fonky.fetch_global_imagery_map_services()`, `fonky.fetch_global_imagery_mercator_map()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `get_capabilities_url()` | `get_capabilities_url( self: Any, projection: str = 'epsg4326', quality: str = 'best', version: str = '1.1.1' ) -> str` | Get capabilities url. |
| `build_wms_url()` | `build_wms_url( self: Any, layer: str, image_date: str, bbox: Tuple[float, float, float, float], width: int = 1200, height: int = 600, projection: str = 'epsg4326', quality: str = 'best', image_format: str = 'image/png', transparent: bool = True, version: str = '1.1.1' ) -> str` | Build wms url. |
| `fetch_wms_map()` | `fetch_wms_map( self: Any, layer: str, image_date: str, bbox: Tuple[float, float, float, float], width: int = 1200, height: int = 600, projection: str = 'epsg4326', quality: str = 'best', image_format: str = 'image/png', transparent: bool = True, output_dir: str = 'python-examples', output_name: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch wms map. |
| `fetch_map_services()` | `fetch_map_services( self: Any ) -> Dict[str, Any] \| None` | Fetch map services. |
| `fetch_mercator_map()` | `fetch_mercator_map( self: Any, ccrs: Any = None ) -> Dict[str, Any] \| None` | Fetch mercator map. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `NearbyObjects`

Nearby Objects fetcher.

```python
NearbyObjects( self: Any ) -> None
```

**Source:** `fetchers.py`, line 4339

**Functional wrappers:** `fonky.fetch_nearby_objects()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `fetch_close_approaches()` | `fetch_close_approaches( self: Any, start_date: str, end_date: str, dist_max: str = '10LD', body: str = 'Earth', sort: str = 'date', limit: int = 20, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch close approaches. |
| `fetch_object_lookup()` | `fetch_object_lookup( self: Any, query: str, query_type: str = 'sstr', include_physical: bool = True, include_close_approaches: bool = True, ca_body: str = 'Earth', include_discovery: bool = True, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch object lookup. |
| `fetch_nhats_summary()` | `fetch_nhats_summary( self: Any, dv: float = 6.0, dur: int = 360, stay: int = 8, launch: str = '2020-2045', h: float = 26.0, occ: int = 7, time: int = 20 ) -> Dict[str, Any]` | Fetch nhats summary. |
| `fetch_nhats_object()` | `fetch_nhats_object( self: Any, designation: str, dv: float = 6.0, dur: int = 360, stay: int = 8, launch: str = '2020-2045', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch nhats object. |
| `fetch_fireballs()` | `fetch_fireballs( self: Any, date_min: str = '', limit: int = 20, time: int = 20 ) -> Dict[str, Any]` | Fetch fireballs. |
| `fetch()` | `fetch( self: Any, mode: str = 'close_approaches', start_date: str = '', end_date: str = '', query: str = '', query_type: str = 'sstr', dist_max: str = '10LD', body: str = 'Earth', sort: str = 'date', limit: int = 20, dv: float = 6.0, dur: int = 360, stay: int = 8, launch: str = '2020-2045', h: float = 26.0, occ: int = 7, include_physical: bool = True, include_close_approaches: bool = True, ca_body: str = 'Earth', include_discovery: bool = True, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch JPL SSD and CNEOS near-Earth object data. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `OpenScience`

Open Science fetcher.

```python
OpenScience( self: Any ) -> None
```

**Source:** `fetchers.py`, line 4790

**Functional wrappers:** `fonky.fetch_open_science()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_format()` | `validate_format( self: Any, format_value: str ) -> str` | Validate format. |
| `coerce_response()` | `coerce_response( self: Any, response: requests.Response ) -> Dict[str, Any] \| str` | Coerce response. |
| `fetch_dataset()` | `fetch_dataset( self: Any, accession: str, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch dataset. |
| `fetch_metadata()` | `fetch_metadata( self: Any, query: str, format_value: str = 'json', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch metadata. |
| `fetch_assays()` | `fetch_assays( self: Any, query: str, format_value: str = 'json', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch assays. |
| `fetch_data()` | `fetch_data( self: Any, query: str, format_value: str = 'json', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch data. |
| `fetch()` | `fetch( self: Any, mode: str = 'dataset', query: str = '', accession: str = '', format_value: str = 'json', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch NASA Open Science Data Repository resources. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `SpaceWeather`

Space Weather fetcher.

```python
SpaceWeather( self: Any ) -> None
```

**Source:** `fetchers.py`, line 5186

**Functional wrappers:** `fonky.fetch_space_weather()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `fetch_endpoint()` | `fetch_endpoint( self: Any, endpoint: str, start_date: str, end_date: str, time: int = 20, location: str = '', catalog: str = '', notification_type: str = '', most_accurate_only: bool = True, complete_entry_only: bool = True, speed: int = 0, half_angle: int = 0, keyword: str = '', api_key: str = None ) -> Dict[str, Any] \| None` | Fetch endpoint. |
| `fetch()` | `fetch( self: Any, mode: str = 'cme', start_date: str = '', end_date: str = '', time: int = 20, location: str = 'ALL', catalog: str = 'ALL', notification_type: str = 'all', most_accurate_only: bool = True, complete_entry_only: bool = True, speed: int = 0, half_angle: int = 0, keyword: str = '', api_key: str = None ) -> Dict[str, Any] \| None` | Fetch NASA DONKI space weather endpoints. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `AstroCatalog`

Astro Catalog fetcher.

```python
AstroCatalog( self: Any ) -> Any
```

**Source:** `fetchers.py`, line 5461

**Functional wrappers:** `fonky.fetch_astro_catalog()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `normalize_attribute_path()` | `normalize_attribute_path( self: Any, quantity: str = '', attributes: str = '' ) -> str` | Normalize attribute path. |
| `parse_argument()` | `parse_argument( self: Any, argument_string: str ) -> Dict[str, Any]` | Parse argument. |
| `request()` | `request( self: Any, route: str, params: Dict[str, Any] \| None = None, time: int = 20 ) -> Any` | Request Open Astronomy Catalog queries. |
| `fetch_object()` | `fetch_object( self: Any, name: str, quantity: str = '', attributes: str = '', arguments: str = '', data_format: str = 'json', time: int = 20 ) -> Any` | Fetch object. |
| `cone_search()` | `cone_search( self: Any, ra: str, dec: str, radius: int = 2, quantity: str = '', attributes: str = '', arguments: str = '', data_format: str = 'json', time: int = 20 ) -> Any` | Cone search. |
| `fetch()` | `fetch( self: Any, mode: str = 'object_query', query: str = '', quantity: str = '', attributes: str = '', arguments: str = '', ra: str = '', dec: str = '', radius: int = 2, data_format: str = 'json', time: int = 20 ) -> Any` | Fetch Open Astronomy Catalog queries. |

## `AstroQuery`

Astro Query fetcher.

```python
AstroQuery( self: Any ) -> None
```

**Source:** `fetchers.py`, line 5783

**Functional wrappers:** `fonky.fetch_astro_query()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `table_to_records()` | `table_to_records( self: Any, table: Table \| None ) -> List[Dict[str, Any]]` | Table to records. |
| `object_search()` | `object_search( self: Any, name: str, row_limit: int = 100 ) -> Dict[str, Any] \| None` | Object search. |
| `object_ids()` | `object_ids( self: Any, name: str, row_limit: int = 100 ) -> Dict[str, Any] \| None` | Object IDs. |
| `region_search()` | `region_search( self: Any, ra: str, dec: str, radius: float = 0.5, radius_unit: str = 'deg', row_limit: int = 100 ) -> Dict[str, Any] \| None` | Region search. |
| `fetch()` | `fetch( self: Any, mode: str = 'object_search', query: str = '', ra: str = '', dec: str = '', radius: float = 0.5, radius_unit: str = 'deg', row_limit: int = 100 ) -> Dict[str, Any]` | Fetch Simbad and astronomy object search operations. |

## `StarMap`

Star Map fetcher.

```python
StarMap( self: Any ) -> None
```

**Source:** `fetchers.py`, line 6059

**Functional wrappers:** `fonky.fetch_star_map()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `normalize()` | `normalize( self: Any, value: bool ) -> str` | Normalize. |
| `extract_links()` | `extract_links( self: Any, html: str, base_url: str ) -> Dict[str, str]` | Extract links. |
| `fetch_object_link()` | `fetch_object_link( self: Any, name: str, zoom: int = 5, box_color: str = 'yellow', show_box: bool = True, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch object link. |
| `fetch_coordinate_link()` | `fetch_coordinate_link( self: Any, ra: float, dec: float, zoom: int = 5, box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch coordinate link. |
| `fetch_snapshot()` | `fetch_snapshot( self: Any, ra: float, dec: float, zoom: int = 10, image_source: str = 'DSS2', show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch snapshot. |
| `fetch()` | `fetch( self: Any, mode: str = 'object_link', query: str = '', ra: float = 0.0, dec: float = 0.0, zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch astronomical object map links and imagery. |

## `GovData`

Gov Data fetcher.

```python
GovData( self: Any ) -> None
```

**Source:** `fetchers.py`, line 6447

**Functional wrappers:** `fonky.fetch_gov_data()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_page_size()` | `validate_page_size( self: Any, page_size: int ) -> int` | Validate page size. |
| `validate_sort_field()` | `validate_sort_field( self: Any, sort_field: str ) -> str` | Validate sort field. |
| `validate_sort_order()` | `validate_sort_order( self: Any, sort_order: str ) -> str` | Validate sort order. |
| `fetch_search()` | `fetch_search( self: Any, query: str, page_size: int = 10, offset_mark: str = '*', sort_field: str = 'score', sort_order: str = 'DESC', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch search. |
| `fetch_package_summary()` | `fetch_package_summary( self: Any, package_id: str, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch package summary. |
| `fetch_collection()` | `fetch_collection( self: Any, collection: str, start_date: str, page_size: int = 10, offset_mark: str = '*', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch collection. |
| `fetch()` | `fetch( self: Any, mode: str = 'search', query: str = '', page_size: int = 10, offset_mark: str = '*', sort_field: str = 'score', sort_order: str = 'DESC', package_id: str = '', collection: str = '', start_date: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch Data.gov package and collection retrieval. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `StarChart`

Star Chart fetcher.

```python
StarChart( self: Any ) -> None
```

**Source:** `fetchers.py`, line 6958

**Functional wrappers:** `fonky.fetch_star_chart()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `flag()` | `flag( self: Any, value: bool, invert: bool = False ) -> int` | Flag. |
| `search_object()` | `search_object( self: Any, name: str, time: int = 20 ) -> Dict[str, Any] \| None` | Search object. |
| `fetch_object_chart()` | `fetch_object_chart( self: Any, name: str, zoom: int = 5, box_color: str = 'yellow', show_box: bool = True, image_source: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch object chart. |
| `fetch_coordinate_chart()` | `fetch_coordinate_chart( self: Any, ra: float, dec: float, zoom: int = 5, box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, image_source: str = '' ) -> Dict[str, Any] \| None` | Fetch coordinate chart. |
| `fetch_static_chart()` | `fetch_static_chart( self: Any, ra: float, dec: float, zoom: int = 5, image_source: str = 'DSS2', show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, width: int = 900, height: int = 450, magnitude: float = 7.5 ) -> Dict[str, Any] \| None` | Fetch static chart. |
| `fetch()` | `fetch( self: Any, mode: str = 'object_chart', query: str = '', ra: float = 0.0, dec: float = 0.0, zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, width: int = 900, height: int = 450, magnitude: float = 7.5, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch static star chart and coordinate chart generation. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `Congress`

Congress fetcher.

```python
Congress( self: Any ) -> None
```

**Source:** `fetchers.py`, line 7561

**Functional wrappers:** `fonky.fetch_congress()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_limit()` | `validate_limit( self: Any, limit: int ) -> int` | Validate limit. |
| `validate_offset()` | `validate_offset( self: Any, offset: int ) -> int` | Validate offset. |
| `normalize_bill_type()` | `normalize_bill_type( self: Any, bill_type: str ) -> str` | Normalize bill type. |
| `normalize_law_type()` | `normalize_law_type( self: Any, law_type: str ) -> str` | Normalize law type. |
| `normalize_report_type()` | `normalize_report_type( self: Any, report_type: str ) -> str` | Normalize report type. |
| `build_params()` | `build_params( self: Any, limit: int = 20, offset: int = 0, sort: str = 'updateDate+desc' ) -> Dict[str, Any]` | Build params. |
| `request()` | `request( self: Any, mode: str, url: str, params: Dict[str, Any], time: int = 20 ) -> Dict[str, Any] \| None` | Request Congress.gov legislative data retrieval. |
| `fetch_congresses()` | `fetch_congresses( self: Any, limit: int = 20, offset: int = 0, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch congresses. |
| `fetch_bills()` | `fetch_bills( self: Any, congress: int, bill_type: str = '', offset: int = 0, limit: int = 20, sort: str = 'updateDate+desc', from_date_time: str = '', to_date_time: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch bills. |
| `fetch_bill()` | `fetch_bill( self: Any, congress: int, bill_type: str, bill_number: int, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch bill. |
| `fetch_laws()` | `fetch_laws( self: Any, congress: int, law_type: str = '', offset: int = 0, limit: int = 20, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch laws. |
| `fetch_law()` | `fetch_law( self: Any, congress: int, law_type: str, law_number: int, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch law. |
| `fetch_reports()` | `fetch_reports( self: Any, congress: int, report_type: str = '', offset: int = 0, limit: int = 20, conference: bool = False, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch reports. |
| `fetch_report()` | `fetch_report( self: Any, congress: int, report_type: str, report_number: int, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch report. |
| `fetch()` | `fetch( self: Any, mode: str = 'congresses', congress: int = 0, bill_type: str = '', bill_number: int = 0, law_type: str = '', law_number: int = 0, report_type: str = '', report_number: int = 0, offset: int = 0, limit: int = 20, sort: str = 'updateDate+desc', from_date_time: str = '', to_date_time: str = '', conference: bool = False, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch Congress.gov legislative data retrieval. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `InternetArchive`

Internet Archive fetcher.

```python
InternetArchive( self: Any ) -> None
```

**Source:** `fetchers.py`, line 8579

**Functional wrappers:** `fonky.fetch_internet_archive()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_rows()` | `validate_rows( self: Any, rows: int ) -> int` | Validate rows. |
| `validate_page()` | `validate_page( self: Any, page: int ) -> int` | Validate page. |
| `build_query()` | `build_query( self: Any, keywords: str, media_type: str = '', collection: str = '' ) -> str` | Build query. |
| `fetch()` | `fetch( self: Any, keywords: str, fields: List[str] \| None = None, rows: int = 10, page: int = 1, sort: str = 'downloads desc', media_type: str = '', collection: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch Internet Archive search and metadata retrieval. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `OpenWeather`

Open Weather fetcher.

```python
OpenWeather( self: Any ) -> None
```

**Source:** `fetchers.py`, line 8930

**Functional wrappers:** `fonky.fetch_open_weather()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `geocode_location()` | `geocode_location( self: Any, location: str, count: int = 10 ) -> Dict[str, Any] \| None` | Geocode location. |
| `fetch_current()` | `fetch_current( self: Any, lat: float, long: float, zone: str = 'auto', past_days: int = 0 ) -> Dict[str, Any] \| None` | Fetch current. |
| `fetch_hourly()` | `fetch_hourly( self: Any, lat: float, long: float, zone: str = 'auto', forecast_days: int = 7, past_days: int = 0 ) -> Dict[str, Any] \| None` | Fetch hourly. |
| `fetch_daily()` | `fetch_daily( self: Any, lat: float, long: float, zone: str = 'auto', forecast_days: int = 7, past_days: int = 0 ) -> Dict[str, Any] \| None` | Fetch daily. |
| `fetch()` | `fetch( self: Any, location: str, mode: str = 'current', zone: str = 'auto', forecast_days: int = 7, past_days: int = 0, count: int = 10 ) -> Dict[str, Any] \| None` | Fetch Open-Meteo current and forecast weather retrieval. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `HistoricalWeather`

Historical Weather fetcher.

```python
HistoricalWeather( self: Any ) -> None
```

**Source:** `fetchers.py`, line 9544

**Functional wrappers:** `fonky.fetch_historical_weather()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `geocode_location()` | `geocode_location( self: Any, location: str, count: int = 10 ) -> Dict[str, Any] \| None` | Geocode location. |
| `fetch_historical()` | `fetch_historical( self: Any, lat: float, long: float, date: dt.date, zone: str = 'auto' ) -> Dict[str, Any] \| None` | Fetch historical. |
| `fetch()` | `fetch( self: Any, location: str, date: dt.date, zone: str = 'auto', count: int = 10 ) -> Dict[str, Any] \| None` | Fetch historical weather archive retrieval. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `Grokipedia`

Grokipedia fetcher.

```python
Grokipedia( self: Any ) -> None
```

**Source:** `fetchers.py`, line 9950

**Functional wrappers:** `fonky.fetch_grokipedia()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `fetch_search()` | `fetch_search( self: Any, query: str, limit: int = 12, offset: int = 0 ) -> Dict[str, Any] \| None` | Fetch search. |
| `fetch_page()` | `fetch_page( self: Any, page: str, include_content: bool = True ) -> Dict[str, Any] \| None` | Fetch page. |
| `fetch()` | `fetch( self: Any, mode: str = 'search', query: str = '', page: str = '', limit: int = 12, offset: int = 0, include_content: bool = True ) -> Dict[str, Any] \| None` | Fetch Grokipedia search and page retrieval. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `GoogleGeocoding`

Google Geocoding fetcher.

```python
GoogleGeocoding( self: Any ) -> None
```

**Source:** `fetchers.py`, line 10251

**Functional wrappers:** `fonky.fetch_google_geocoding()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `request()` | `request( self: Any, params: Dict[str, Any], time: int = 10, api_key: Optional[str] = None ) -> Dict[str, Any] \| None` | Request Google forward, reverse, and place geocoding. |
| `fetch_forward()` | `fetch_forward( self: Any, query: str, language: str = 'en', region: str = '', time: int = 10, api_key: Optional[str] = None ) -> Dict[str, Any] \| None` | Fetch forward. |
| `fetch_reverse()` | `fetch_reverse( self: Any, latitude: float, longitude: float, language: str = 'en', result_type: str = '', location_type: str = '', time: int = 10, api_key: Optional[str] = None ) -> Dict[str, Any] \| None` | Fetch reverse. |
| `fetch_place()` | `fetch_place( self: Any, place_id: str, language: str = 'en', region: str = '', time: int = 10, api_key: Optional[str] = None ) -> Dict[str, Any] \| None` | Fetch place. |
| `fetch()` | `fetch( self: Any, mode: str = 'forward', query: str = '', latitude: float = 0.0, longitude: float = 0.0, place_id: str = '', language: str = 'en', region: str = '', result_type: str = '', location_type: str = '', time: int = 10, api_key: Optional[str] = None ) -> Dict[str, Any] \| None` | Fetch Google forward, reverse, and place geocoding. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `CensusData`

Census Data fetcher.

```python
CensusData( self: Any ) -> None
```

**Source:** `fetchers.py`, line 10753

**Functional wrappers:** `fonky.fetch_census_data()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `normalize_fields()` | `normalize_fields( self: Any, fields: str ) -> str` | Normalize fields. |
| `parse_predicates()` | `parse_predicates( self: Any, predicates: str = '' ) -> Dict[str, Any]` | Parse predicates. |
| `shape_table()` | `shape_table( self: Any, rows: List[Any] ) -> Dict[str, Any]` | Shape table. |
| `fetch_variables()` | `fetch_variables( self: Any, year: str, dataset: str, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch variables. |
| `fetch_data()` | `fetch_data( self: Any, year: str, dataset: str, fields: str, geography_for: str = '', geography_in: str = '', predicates: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch data. |
| `fetch()` | `fetch( self: Any, mode: str = 'variables', year: str = '2022', dataset: str = 'acs/acs5', fields: str = 'NAME,B01001_001E', geography_for: str = 'state:*', geography_in: str = '', predicates: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch U.S. Census dataset and variable retrieval. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `Socrata`

Socrata fetcher.

```python
Socrata( self: Any ) -> None
```

**Source:** `fetchers.py`, line 11270

**Functional wrappers:** `fonky.fetch_socrata()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `normalize_domain()` | `normalize_domain( self: Any, domain: str ) -> str` | Normalize domain. |
| `normalize_dataset_id()` | `normalize_dataset_id( self: Any, dataset_id: str ) -> str` | Normalize dataset id. |
| `validate_limit()` | `validate_limit( self: Any, limit: int ) -> int` | Validate limit. |
| `validate_offset()` | `validate_offset( self: Any, offset: int ) -> int` | Validate offset. |
| `fetch_metadata()` | `fetch_metadata( self: Any, domain: str, dataset_id: str, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch metadata. |
| `fetch_rows()` | `fetch_rows( self: Any, domain: str, dataset_id: str, select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch rows. |
| `fetch()` | `fetch( self: Any, mode: str = 'rows', domain: str = 'data.cdc.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch Socrata dataset metadata and row retrieval. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `HealthData`

Health Data fetcher.

```python
HealthData( self: Any ) -> None
```

**Source:** `fetchers.py`, line 11822

**Functional wrappers:** `fonky.fetch_health_data()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `normalize_domain()` | `normalize_domain( self: Any, domain: str ) -> str` | Normalize domain. |
| `normalize_dataset_id()` | `normalize_dataset_id( self: Any, dataset_id: str ) -> str` | Normalize dataset id. |
| `validate_limit()` | `validate_limit( self: Any, limit: int ) -> int` | Validate limit. |
| `validate_offset()` | `validate_offset( self: Any, offset: int ) -> int` | Validate offset. |
| `fetch_metadata()` | `fetch_metadata( self: Any, domain: str, dataset_id: str, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch metadata. |
| `fetch_rows()` | `fetch_rows( self: Any, domain: str, dataset_id: str, select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch rows. |
| `fetch()` | `fetch( self: Any, mode: str = 'rows', domain: str = 'healthdata.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch HealthData.gov Socrata metadata and rows. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `GlobalHealthData`

Global Health Data fetcher.

```python
GlobalHealthData( self: Any ) -> None
```

**Source:** `fetchers.py`, line 12375

**Functional wrappers:** `fonky.fetch_global_health_data()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `normalize_query_path()` | `normalize_query_path( self: Any, query_path: str ) -> str` | Normalize query path. |
| `fetch_indicator_registry()` | `fetch_indicator_registry( self: Any, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch indicator registry. |
| `fetch_athena()` | `fetch_athena( self: Any, query_path: str, fmt: str = 'json', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch athena. |
| `fetch()` | `fetch( self: Any, mode: str = 'indicator_registry', query_path: str = '', fmt: str = 'json', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch WHO global health indicator and Athena data. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `UnitedNations`

United Nations fetcher.

```python
UnitedNations( self: Any ) -> None
```

**Source:** `fetchers.py`, line 12768

**Functional wrappers:** `fonky.fetch_united_nations()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `normalize_query_path()` | `normalize_query_path( self: Any, query_path: str ) -> str` | Normalize query path. |
| `fetch_datasets()` | `fetch_datasets( self: Any, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch datasets. |
| `fetch_sdmx_query()` | `fetch_sdmx_query( self: Any, query_path: str, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch sdmx query. |
| `fetch()` | `fetch( self: Any, mode: str = 'datasets', query_path: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch United Nations SDMX dataset and query retrieval. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `WorldPopulation`

World Population fetcher.

```python
WorldPopulation( self: Any ) -> None
```

**Source:** `fetchers.py`, line 13134

**Functional wrappers:** `fonky.fetch_world_population()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `normalize_asset_path()` | `normalize_asset_path( self: Any, asset_path: str ) -> str` | Normalize asset path. |
| `validate_page()` | `validate_page( self: Any, page: int ) -> int` | Validate page. |
| `validate_page_size()` | `validate_page_size( self: Any, page_size: int ) -> int` | Validate page size. |
| `fetch_catalog()` | `fetch_catalog( self: Any, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch catalog. |
| `search_catalog()` | `search_catalog( self: Any, query: str = '', page: int = 1, page_size: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Search catalog. |
| `fetch_raster_metadata()` | `fetch_raster_metadata( self: Any, asset_path: str, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch raster metadata. |
| `fetch()` | `fetch( self: Any, mode: str = 'catalog', query: str = '', asset_path: str = '', page: int = 1, page_size: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch WorldPop catalog and raster metadata retrieval. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `Wonder`

Wonder fetcher.

```python
Wonder( self: Any ) -> None
```

**Source:** `fetchers.py`, line 13673

**Functional wrappers:** `fonky.fetch_wonder()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `normalize_dataset_id()` | `normalize_dataset_id( self: Any, dataset_id: str ) -> str` | Normalize dataset id. |
| `build_template()` | `build_template( self: Any, dataset_id: str = 'D76' ) -> str` | Build template. |
| `fetch_template()` | `fetch_template( self: Any, dataset_id: str = 'D76' ) -> Dict[str, Any] \| None` | Fetch template. |
| `submit_query()` | `submit_query( self: Any, dataset_id: str, request_xml: str, time: int = 20 ) -> Dict[str, Any] \| None` | Submit query. |
| `fetch()` | `fetch( self: Any, mode: str = 'metadata_template', dataset_id: str = 'D76', request_xml: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch CDC WONDER template and query submission. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `USGSEarthquakes`

U S G S Earthquakes fetcher.

```python
USGSEarthquakes( self: Any ) -> None
```

**Source:** `fetchers.py`, line 14085

**Functional wrappers:** `fonky.fetch_usgs_earthquakes()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_feed()` | `validate_feed( self: Any, feed: str ) -> str` | Validate feed. |
| `validate_limit()` | `validate_limit( self: Any, limit: int ) -> int` | Validate limit. |
| `validate_magnitude()` | `validate_magnitude( self: Any, name: str, value: float ) -> float` | Validate magnitude. |
| `validate_order_by()` | `validate_order_by( self: Any, order_by: str ) -> str` | Validate order by. |
| `validate_latitude()` | `validate_latitude( self: Any, latitude: float ) -> float` | Validate latitude. |
| `validate_longitude()` | `validate_longitude( self: Any, longitude: float ) -> float` | Validate longitude. |
| `validate_radius()` | `validate_radius( self: Any, radius: float ) -> float` | Validate radius. |
| `to_iso_date()` | `to_iso_date( self: Any, value: str ) -> str` | Convert to iso date. |
| `epoch_millis_to_iso()` | `epoch_millis_to_iso( self: Any, value: Any ) -> str` | Epoch millis to iso. |
| `shape_feature_rows()` | `shape_feature_rows( self: Any, features: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape feature rows. |
| `summarize_features()` | `summarize_features( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Summarize features. |
| `package_response()` | `package_response( self: Any ) -> Dict[str, Any]` | Package response. |
| `fetch_feed()` | `fetch_feed( self: Any, feed: str = 'all_day.geojson', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch feed. |
| `fetch_search()` | `fetch_search( self: Any, start_date: str, end_date: str, min_magnitude: float = 1.0, max_magnitude: float = 10.0, limit: int = 25, order_by: str = 'time', event_type: str = 'earthquake', latitude: float \| None = None, longitude: float \| None = None, max_radius_km: float \| None = None, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch search. |
| `fetch()` | `fetch( self: Any, mode: str = 'feed', feed: str = 'all_day.geojson', start_date: str = '', end_date: str = '', min_magnitude: float = 1.0, max_magnitude: float = 10.0, limit: int = 25, order_by: str = 'time', event_type: str = 'earthquake', latitude: float \| None = None, longitude: float \| None = None, max_radius_km: float \| None = None, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch USGS earthquake feed and query retrieval. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `USGSWaterData`

U S G S Water Data fetcher.

```python
USGSWaterData( self: Any ) -> None
```

**Source:** `fetchers.py`, line 15004

**Functional wrappers:** `fonky.fetch_usgs_water_data()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_collection()` | `validate_collection( self: Any, collection: str ) -> str` | Validate collection. |
| `validate_limit()` | `validate_limit( self: Any, limit: int ) -> int` | Validate limit. |
| `validate_parameter_code()` | `validate_parameter_code( self: Any, parameter_code: str ) -> str` | Validate parameter code. |
| `coalesce_records()` | `coalesce_records( self: Any, payload: Any ) -> List[Dict[str, Any]]` | Coalesce records. |
| `shape_monitoring_locations()` | `shape_monitoring_locations( self: Any, records: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape monitoring locations. |
| `shape_time_series_metadata()` | `shape_time_series_metadata( self: Any, records: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape time series metadata. |
| `shape_latest_values()` | `shape_latest_values( self: Any, records: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape latest values. |
| `summarize_rows()` | `summarize_rows( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Summarize rows. |
| `package_response()` | `package_response( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Package response. |
| `request()` | `request( self: Any, collection: str, params: Dict[str, Any], time: int = 20 ) -> Dict[str, Any] \| None` | Request USGS water services records. |
| `fetch_monitoring_locations()` | `fetch_monitoring_locations( self: Any, monitoring_location_id: str = '', state_code: str = '', county_code: str = '', site_type: str = '', limit: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch monitoring locations. |
| `fetch_time_series_metadata()` | `fetch_time_series_metadata( self: Any, monitoring_location_id: str = '', parameter_code: str = '', limit: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch time series metadata. |
| `fetch_latest_continuous()` | `fetch_latest_continuous( self: Any, monitoring_location_id: str = '', parameter_code: str = '', limit: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch latest continuous. |
| `fetch_latest_daily()` | `fetch_latest_daily( self: Any, monitoring_location_id: str = '', parameter_code: str = '', limit: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch latest daily. |
| `fetch()` | `fetch( self: Any, mode: str = 'monitoring-locations', monitoring_location_id: str = '', state_code: str = '', county_code: str = '', site_type: str = '', parameter_code: str = '', limit: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch USGS water services records. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `USGSTheNationalMap`

U S G S The National Map fetcher.

```python
USGSTheNationalMap( self: Any ) -> None
```

**Source:** `fetchers.py`, line 16099

**Functional wrappers:** `fonky.fetch_usgs_national_map()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_endpoint()` | `validate_endpoint( self: Any, endpoint: str ) -> str` | Validate endpoint. |
| `validate_max_items()` | `validate_max_items( self: Any, max_items: int ) -> int` | Validate max items. |
| `validate_offset()` | `validate_offset( self: Any, offset: int ) -> int` | Validate offset. |
| `validate_bbox()` | `validate_bbox( self: Any, bbox: str ) -> str` | Validate bbox. |
| `coalesce_records()` | `coalesce_records( self: Any, payload: Any ) -> List[Dict[str, Any]]` | Coalesce records. |
| `shape_dataset_rows()` | `shape_dataset_rows( self: Any, records: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape dataset rows. |
| `shape_product_rows()` | `shape_product_rows( self: Any, records: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape product rows. |
| `summarize_rows()` | `summarize_rows( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Summarize rows. |
| `package_response()` | `package_response( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Package response. |
| `request()` | `request( self: Any, endpoint: str, params: Dict[str, Any], time: int = 20 ) -> Dict[str, Any] \| None` | Request USGS National Map datasets and products. |
| `fetch_datasets()` | `fetch_datasets( self: Any, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch datasets. |
| `fetch_products()` | `fetch_products( self: Any, dataset: str = '', q: str = '', bbox: str = '', prod_formats: str = '', max_items: int = 25, offset: int = 0, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch products. |
| `fetch()` | `fetch( self: Any, mode: str = 'products', dataset: str = '', q: str = '', bbox: str = '', prod_formats: str = '', max_items: int = 25, offset: int = 0, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch USGS National Map datasets and products. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `USGSScienceBase`

U S G S Science Base fetcher.

```python
USGSScienceBase( self: Any ) -> None
```

**Source:** `fetchers.py`, line 16946

**Functional wrappers:** `fonky.fetch_usgs_sciencebase()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_endpoint()` | `validate_endpoint( self: Any, endpoint: str ) -> str` | Validate endpoint. |
| `validate_max_items()` | `validate_max_items( self: Any, max_items: int ) -> int` | Validate max items. |
| `validate_offset()` | `validate_offset( self: Any, offset: int ) -> int` | Validate offset. |
| `coalesce_records()` | `coalesce_records( self: Any, payload: Any ) -> List[Dict[str, Any]]` | Coalesce records. |
| `shape_single_item()` | `shape_single_item( self: Any, item: Dict[str, Any] ) -> Dict[str, Any]` | Shape single item. |
| `shape_item_rows()` | `shape_item_rows( self: Any, records: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape item rows. |
| `summarize_rows()` | `summarize_rows( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Summarize rows. |
| `package_response()` | `package_response( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Package response. |
| `request()` | `request( self: Any, endpoint: str, params: Optional[Dict[str, Any]] = None, time: int = 20 ) -> Dict[str, Any] \| None` | Request USGS ScienceBase items and catalog records. |
| `fetch_items()` | `fetch_items( self: Any, q: str = '', max_items: int = 25, offset: int = 0, fields: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch items. |
| `fetch_item()` | `fetch_item( self: Any, item_id: str, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch item. |
| `fetch()` | `fetch( self: Any, mode: str = 'items', q: str = '', item_id: str = '', max_items: int = 25, offset: int = 0, fields: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch USGS ScienceBase items and catalog records. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `AirNow`

Air Now fetcher.

```python
AirNow( self: Any ) -> None
```

**Source:** `fetchers.py`, line 17664

**Functional wrappers:** `fonky.fetch_air_now()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `request()` | `request( self: Any, endpoint: str, params: Optional[Dict[str, Any]] = None, time: int = 20 ) -> Dict[str, Any] \| None` | Request AirNow current and forecast air quality data. |
| `shape_rows()` | `shape_rows( self: Any, records: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape rows. |
| `summarize_rows()` | `summarize_rows( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Summarize rows. |
| `package_response()` | `package_response( self: Any ) -> Dict[str, Any]` | Package response. |
| `fetch_current_zip()` | `fetch_current_zip( self: Any, zip_code: str, distance: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch current zip. |
| `fetch_current_latlon()` | `fetch_current_latlon( self: Any, latitude: float, longitude: float, distance: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch current latlon. |
| `fetch_forecast_zip()` | `fetch_forecast_zip( self: Any, zip_code: str, date: str, distance: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch forecast zip. |
| `fetch_forecast_latlon()` | `fetch_forecast_latlon( self: Any, latitude: float, longitude: float, date: str, distance: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch forecast latlon. |
| `fetch()` | `fetch( self: Any, mode: str = 'current-zip', zip_code: str = '', latitude: float \| None = None, longitude: float \| None = None, date: str = '', distance: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch AirNow current and forecast air quality data. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `ClimateData`

Climate Data fetcher.

```python
ClimateData( self: Any ) -> None
```

**Source:** `fetchers.py`, line 18337

**Functional wrappers:** `fonky.fetch_climate_data()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_limit()` | `validate_limit( self: Any, limit: int ) -> int` | Validate limit. |
| `validate_offset()` | `validate_offset( self: Any, offset: int ) -> int` | Validate offset. |
| `validate_date_range()` | `validate_date_range( self: Any, start_date: str, end_date: str ) -> Tuple[str, str]` | Validate date range. |
| `coalesce_records()` | `coalesce_records( self: Any, payload: Any ) -> List[Dict[str, Any]]` | Coalesce records. |
| `shape_dataset_rows()` | `shape_dataset_rows( self: Any, records: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape dataset rows. |
| `shape_data_rows()` | `shape_data_rows( self: Any, records: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape data rows. |
| `summarize_rows()` | `summarize_rows( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Summarize rows. |
| `package_response()` | `package_response( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Package response. |
| `request()` | `request( self: Any, url: str, params: Dict[str, Any], time: int = 20 ) -> Dict[str, Any] \| None` | Request NOAA climate dataset and data records. |
| `fetch_datasets()` | `fetch_datasets( self: Any, keyword: str = '', start_date: str = '', end_date: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch datasets. |
| `fetch_data()` | `fetch_data( self: Any, dataset: str, start_date: str, end_date: str, stations: str = '', data_types: str = '', limit: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch data. |
| `fetch()` | `fetch( self: Any, mode: str = 'datasets', keyword: str = '', dataset: str = '', start_date: str = '', end_date: str = '', stations: str = '', data_types: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch NOAA climate dataset and data records. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `EoNet`

Eo Net fetcher.

```python
EoNet( self: Any ) -> None
```

**Source:** `fetchers.py`, line 19105

**Functional wrappers:** `fonky.fetch_eonet()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_endpoint()` | `validate_endpoint( self: Any, endpoint: str ) -> str` | Validate endpoint. |
| `validate_status()` | `validate_status( self: Any, status: str ) -> str` | Validate status. |
| `validate_limit()` | `validate_limit( self: Any, limit: int ) -> int` | Validate limit. |
| `validate_days()` | `validate_days( self: Any, days: int ) -> int` | Validate days. |
| `validate_bbox()` | `validate_bbox( self: Any, bbox: str ) -> str` | Validate bbox. |
| `validate_date_pair()` | `validate_date_pair( self: Any, start_date: str = '', end_date: str = '' ) -> Tuple[str, str]` | Validate date pair. |
| `shape_event_rows()` | `shape_event_rows( self: Any, records: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape event rows. |
| `shape_category_rows()` | `shape_category_rows( self: Any, records: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape category rows. |
| `summarize_rows()` | `summarize_rows( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Summarize rows. |
| `package_response()` | `package_response( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Package response. |
| `request()` | `request( self: Any, endpoint: str, params: Optional[Dict[str, Any]] = None, time: int = 20 ) -> Dict[str, Any] \| None` | Request NASA EONET environmental event data. |
| `fetch_events()` | `fetch_events( self: Any, source: str = '', category: str = '', status: str = 'open', limit: int = 25, days: int = 30, start_date: str = '', end_date: str = '', bbox: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch events. |
| `fetch_categories()` | `fetch_categories( self: Any, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch categories. |
| `fetch()` | `fetch( self: Any, mode: str = 'events', source: str = '', category: str = '', status: str = 'open', limit: int = 25, days: int = 30, start_date: str = '', end_date: str = '', bbox: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch NASA EONET environmental event data. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `EnviroFacts`

Enviro Facts fetcher.

```python
EnviroFacts( self: Any ) -> None
```

**Source:** `fetchers.py`, line 20014

**Functional wrappers:** `fonky.fetch_envirofacts()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_table_name()` | `validate_table_name( self: Any, table_name: str ) -> str` | Validate table name. |
| `validate_state_code()` | `validate_state_code( self: Any, state_code: str = '' ) -> str` | Validate state code. |
| `validate_limit()` | `validate_limit( self: Any, limit: int ) -> int` | Validate limit. |
| `resolve_table_path()` | `resolve_table_path( self: Any, table_name: str, state_code: str = '', facility_name: str = '', limit: int = 25 ) -> str` | Resolve table path. |
| `shape_rows()` | `shape_rows( self: Any, records: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape rows. |
| `summarize_rows()` | `summarize_rows( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Summarize rows. |
| `package_response()` | `package_response( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Package response. |
| `request()` | `request( self: Any, url: str, time: int = 20 ) -> Dict[str, Any] \| None` | Request EPA Envirofacts table and facility records. |
| `fetch_table()` | `fetch_table( self: Any, table_name: str, state_code: str = '', facility_name: str = '', limit: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch table. |
| `fetch()` | `fetch( self: Any, table_name: str = 'TRI_FACILITY', state_code: str = '', facility_name: str = '', limit: int = 25, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch EPA Envirofacts table and facility records. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `TidesAndCurrents`

Tides And Currents fetcher.

```python
TidesAndCurrents( self: Any ) -> None
```

**Source:** `fetchers.py`, line 20676

**Functional wrappers:** `fonky.fetch_tides_and_currents()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_mode()` | `validate_mode( self: Any, mode: str ) -> str` | Validate mode. |
| `validate_station_id()` | `validate_station_id( self: Any, station_id: str ) -> str` | Validate station id. |
| `validate_date_range()` | `validate_date_range( self: Any, begin_date: str, end_date: str ) -> Tuple[str, str]` | Validate date range. |
| `validate_datum()` | `validate_datum( self: Any, datum: str ) -> str` | Validate datum. |
| `validate_units()` | `validate_units( self: Any, units: str ) -> str` | Validate units. |
| `validate_time_zone()` | `validate_time_zone( self: Any, time_zone: str ) -> str` | Validate time zone. |
| `validate_interval()` | `validate_interval( self: Any, interval: str ) -> str` | Validate interval. |
| `shape_station_rows()` | `shape_station_rows( self: Any, payload: Dict[str, Any] ) -> List[Dict[str, Any]]` | Shape station rows. |
| `shape_data_rows()` | `shape_data_rows( self: Any, payload: Dict[str, Any] ) -> List[Dict[str, Any]]` | Shape data rows. |
| `summarize_rows()` | `summarize_rows( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Summarize rows. |
| `package_response()` | `package_response( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Package response. |
| `request()` | `request( self: Any, url: str, params: Optional[Dict[str, Any]] = None, time: int = 20 ) -> Dict[str, Any] \| None` | Request NOAA tides, currents, and station data. |
| `fetch_station()` | `fetch_station( self: Any, station_id: str, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch station. |
| `fetch_water_level()` | `fetch_water_level( self: Any, station_id: str, begin_date: str, end_date: str, datum: str = 'MLLW', units: str = 'metric', time_zone: str = 'gmt', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch water level. |
| `fetch_tide_predictions()` | `fetch_tide_predictions( self: Any, station_id: str, begin_date: str, end_date: str, datum: str = 'MLLW', units: str = 'metric', time_zone: str = 'gmt', interval: str = 'hilo', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch tide predictions. |
| `fetch()` | `fetch( self: Any, mode: str = 'water-level', station_id: str = '', begin_date: str = '', end_date: str = '', datum: str = 'MLLW', units: str = 'metric', time_zone: str = 'gmt', interval: str = 'hilo', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch NOAA tides, currents, and station data. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `UvIndex`

UV Index fetcher.

```python
UvIndex( self: Any ) -> None
```

**Source:** `fetchers.py`, line 21708

**Functional wrappers:** `fonky.fetch_uv_index()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_mode()` | `validate_mode( self: Any, mode: str ) -> str` | Validate mode. |
| `validate_zip_code()` | `validate_zip_code( self: Any, zip_code: str ) -> str` | Validate zip code. |
| `validate_city()` | `validate_city( self: Any, city: str ) -> str` | Validate city. |
| `validate_state()` | `validate_state( self: Any, state: str ) -> str` | Validate state. |
| `shape_rows()` | `shape_rows( self: Any, records: List[Dict[str, Any]] ) -> List[Dict[str, Any]]` | Shape rows. |
| `summarize_rows()` | `summarize_rows( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Summarize rows. |
| `package_response()` | `package_response( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Package response. |
| `request()` | `request( self: Any, url: str, params: Dict[str, Any], time: int = 20 ) -> Dict[str, Any] \| None` | Request EPA UV Index current and forecast data. |
| `fetch_daily_zip()` | `fetch_daily_zip( self: Any, zip_code: str, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch daily zip. |
| `fetch_daily_city_state()` | `fetch_daily_city_state( self: Any, city: str, state: str, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch daily city state. |
| `fetch_hourly_zip()` | `fetch_hourly_zip( self: Any, zip_code: str, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch hourly zip. |
| `fetch_hourly_city_state()` | `fetch_hourly_city_state( self: Any, city: str, state: str, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch hourly city state. |
| `fetch()` | `fetch( self: Any, mode: str = 'daily-zip', zip_code: str = '', city: str = '', state: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch EPA UV Index current and forecast data. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `PurpleAir`

Purple Air fetcher.

```python
PurpleAir( self: Any ) -> None
```

**Source:** `fetchers.py`, line 22538

**Functional wrappers:** `fonky.fetch_purple_air()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_api_key()` | `validate_api_key( self: Any ) -> str` | Validate api key. |
| `validate_mode()` | `validate_mode( self: Any, mode: str ) -> str` | Validate mode. |
| `validate_endpoint()` | `validate_endpoint( self: Any, endpoint: str ) -> str` | Validate endpoint. |
| `validate_sensor_index()` | `validate_sensor_index( self: Any, sensor_index: int ) -> int` | Validate sensor index. |
| `validate_longitude()` | `validate_longitude( self: Any, name: str, value: float ) -> float` | Validate longitude. |
| `validate_latitude()` | `validate_latitude( self: Any, name: str, value: float ) -> float` | Validate latitude. |
| `validate_bbox()` | `validate_bbox( self: Any, nwlng: float, nwlat: float, selng: float, selat: float ) -> Tuple[float, float, float, float]` | Validate bbox. |
| `validate_location_type()` | `validate_location_type( self: Any, location_type: int ) -> int` | Validate location type. |
| `validate_non_negative_integer()` | `validate_non_negative_integer( self: Any, name: str, value: int ) -> int` | Validate non negative integer. |
| `normalize_fields()` | `normalize_fields( self: Any, fields: str, default_fields: str ) -> str` | Normalize fields. |
| `shape_sensor_list_rows()` | `shape_sensor_list_rows( self: Any, payload: Dict[str, Any] ) -> List[Dict[str, Any]]` | Shape sensor list rows. |
| `shape_sensor_detail_rows()` | `shape_sensor_detail_rows( self: Any, payload: Dict[str, Any] ) -> List[Dict[str, Any]]` | Shape sensor detail rows. |
| `summarize_rows()` | `summarize_rows( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Summarize rows. |
| `package_response()` | `package_response( self: Any, rows: List[Dict[str, Any]], params: Dict[str, Any] ) -> Dict[str, Any]` | Package response. |
| `request()` | `request( self: Any, endpoint: str, params: Optional[Dict[str, Any]] = None, time: int = 20 ) -> Dict[str, Any] \| None` | Request PurpleAir sensor and air quality records. |
| `fetch_sensors()` | `fetch_sensors( self: Any, nwlng: float, nwlat: float, selng: float, selat: float, location_type: int = 0, max_age: int = 0, modified_since: int = 0, fields: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch sensors. |
| `fetch_sensor()` | `fetch_sensor( self: Any, sensor_index: int, fields: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch sensor. |
| `fetch()` | `fetch( self: Any, mode: str = 'sensors', sensor_index: int = None, nwlng: float \| None = None, nwlat: float \| None = None, selng: float \| None = None, selat: float \| None = None, location_type: int = 0, max_age: int = 0, modified_since: int = 0, fields: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch PurpleAir sensor and air quality records. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `OpenAQ`

Open A Q fetcher.

```python
OpenAQ( self: Any ) -> None
```

**Source:** `fetchers.py`, line 23615

**Functional wrappers:** `fonky.fetch_open_aq()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_api_key()` | `validate_api_key( self: Any ) -> str` | Validate api key. |
| `validate_mode()` | `validate_mode( self: Any, mode: str ) -> str` | Validate mode. |
| `validate_endpoint()` | `validate_endpoint( self: Any, endpoint: str ) -> str` | Validate endpoint. |
| `validate_positive_integer()` | `validate_positive_integer( self: Any, name: str, value: Any, maximum: int \| None = None ) -> int` | Validate positive integer. |
| `validate_non_negative_integer()` | `validate_non_negative_integer( self: Any, name: str, value: Any ) -> int` | Validate non negative integer. |
| `validate_coordinates()` | `validate_coordinates( self: Any, coordinates: str = '' ) -> str` | Validate coordinates. |
| `validate_radius()` | `validate_radius( self: Any, radius: int ) -> int` | Validate radius. |
| `coalesce_results()` | `coalesce_results( self: Any, payload: Any ) -> List[Dict[str, Any]]` | Coalesce results. |
| `shape_resource_rows()` | `shape_resource_rows( self: Any, payload: Any, resource_name: str ) -> List[Dict[str, Any]]` | Shape resource rows. |
| `shape_location_rows()` | `shape_location_rows( self: Any, payload: Any ) -> List[Dict[str, Any]]` | Shape location rows. |
| `shape_latest_rows()` | `shape_latest_rows( self: Any, payload: Any ) -> List[Dict[str, Any]]` | Shape latest rows. |
| `summarize_rows()` | `summarize_rows( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Summarize rows. |
| `package_response()` | `package_response( self: Any, rows: List[Dict[str, Any]], params: Optional[Dict[str, Any]] = None ) -> Dict[str, Any]` | Package response. |
| `request()` | `request( self: Any, endpoint: str, params: Optional[Dict[str, Any]] = None, time: int = 20 ) -> Dict[str, Any] \| None` | Request OpenAQ location, measurement, and air-quality records. |
| `fetch_countries()` | `fetch_countries( self: Any, providers_id: str = '', parameters_id: str = '', limit: int = 100, page: int = 1, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch countries. |
| `fetch_providers()` | `fetch_providers( self: Any, limit: int = 100, page: int = 1, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch providers. |
| `fetch_parameters()` | `fetch_parameters( self: Any, limit: int = 100, page: int = 1, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch parameters. |
| `fetch_parameter_latest()` | `fetch_parameter_latest( self: Any, parameter_id: int, limit: int = 100, page: int = 1, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch parameter latest. |
| `fetch_locations()` | `fetch_locations( self: Any, country_id: int = None, coordinates: str = '', radius: int = 25000, providers_id: str = '', parameters_id: str = '', limit: int = 25, page: int = 1, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch locations. |
| `fetch_latest()` | `fetch_latest( self: Any, location_id: int, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch latest. |
| `fetch()` | `fetch( self: Any, mode: str = 'locations', location_id: int = None, parameter_id: int = None, country_id: int = None, coordinates: str = '', radius: int = 25000, providers_id: str = '', parameters_id: str = '', limit: int = 25, page: int = 1, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch OpenAQ location, measurement, and air-quality records. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `Firms`

Firms fetcher.

```python
Firms( self: Any ) -> None
```

**Source:** `fetchers.py`, line 25012

**Functional wrappers:** `fonky.fetch_firms()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_map_key()` | `validate_map_key( self: Any ) -> str` | Validate map key. |
| `validate_mode()` | `validate_mode( self: Any, mode: str ) -> str` | Validate mode. |
| `validate_source()` | `validate_source( self: Any, source: str ) -> str` | Validate source. |
| `validate_sensor()` | `validate_sensor( self: Any, sensor: str ) -> str` | Validate sensor. |
| `validate_day_range()` | `validate_day_range( self: Any, day_range: int ) -> int` | Validate day range. |
| `validate_date()` | `validate_date( self: Any, date: str = '' ) -> str` | Validate date. |
| `validate_area_coordinates()` | `validate_area_coordinates( self: Any, area_coordinates: str = 'world' ) -> str` | Validate area coordinates. |
| `csv_to_rows()` | `csv_to_rows( self: Any, csv_text: str ) -> List[Dict[str, Any]]` | CSV to rows. |
| `summarize_rows()` | `summarize_rows( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Summarize rows. |
| `package_response()` | `package_response( self: Any, rows: List[Dict[str, Any]] ) -> Dict[str, Any]` | Package response. |
| `request_csv()` | `request_csv( self: Any, url: str, time: int = 20 ) -> Dict[str, Any] \| None` | Request CSV. |
| `fetch_area()` | `fetch_area( self: Any, source: str, area_coordinates: str = 'world', day_range: int = 1, date: str = '', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch area. |
| `fetch_data_availability()` | `fetch_data_availability( self: Any, sensor: str = 'ALL', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch data availability. |
| `fetch()` | `fetch( self: Any, mode: str = 'area', source: str = 'VIIRS_SNPP_NRT', area_coordinates: str = 'world', day_range: int = 1, date: str = '', sensor: str = 'ALL', time: int = 20 ) -> Dict[str, Any] \| None` | Fetch NASA FIRMS active fire data. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |

## `OpenSky`

Open Sky fetcher.

```python
OpenSky( self: Any ) -> None
```

**Source:** `fetchers.py`, line 25846

**Functional wrappers:** `fonky.fetch_open_sky()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `validate_mode()` | `validate_mode( self: Any, mode: str ) -> str` | Validate mode. |
| `validate_endpoint()` | `validate_endpoint( self: Any, endpoint: str ) -> str` | Validate endpoint. |
| `validate_icao24()` | `validate_icao24( self: Any, icao24: str ) -> str` | Validate icao24. |
| `validate_airport()` | `validate_airport( self: Any, airport: str ) -> str` | Validate airport. |
| `validate_epoch()` | `validate_epoch( self: Any, name: str, value: Any ) -> int` | Validate epoch. |
| `validate_time_range()` | `validate_time_range( self: Any, begin: int, end: int ) -> Tuple[int, int]` | Validate time range. |
| `validate_latitude()` | `validate_latitude( self: Any, name: str, value: Any ) -> float` | Validate latitude. |
| `validate_longitude()` | `validate_longitude( self: Any, name: str, value: Any ) -> float` | Validate longitude. |
| `validate_bbox()` | `validate_bbox( self: Any, lamin: float, lomin: float, lamax: float, lomax: float ) -> Tuple[float, float, float, float]` | Validate bbox. |
| `assign_credentials()` | `assign_credentials( self: Any, client_id: str = None, client_secret: str = None ) -> None` | Assign credentials. |
| `authenticate()` | `authenticate( self: Any ) -> str \| None` | Authenticate. |
| `request()` | `request( self: Any, endpoint: str, params: Dict[str, Any] \| None = None, client_id: str = None, client_secret: str = None ) -> Any` | Request OpenSky Network aircraft, airport, and state-vector data. |
| `normalize_states()` | `normalize_states( self: Any, payload: Dict[str, Any] \| None ) -> Dict[str, Any] \| None` | Normalize states. |
| `normalize_flights()` | `normalize_flights( self: Any, payload: List[Dict[str, Any]] \| None, mode: str ) -> Dict[str, Any] \| None` | Normalize flights. |
| `normalize_track()` | `normalize_track( self: Any, payload: Dict[str, Any] \| None ) -> Dict[str, Any] \| None` | Normalize track. |
| `fetch_states()` | `fetch_states( self: Any, icao24: str = '', time_value: int = None, lamin: float \| None = None, lomin: float \| None = None, lamax: float \| None = None, lomax: float \| None = None, extended: bool = False, client_id: str = None, client_secret: str = None ) -> Dict[str, Any] \| None` | Fetch states. |
| `fetch_flights_aircraft()` | `fetch_flights_aircraft( self: Any, icao24: str, begin: int, end: int, client_id: str = None, client_secret: str = None ) -> Dict[str, Any] \| None` | Fetch flights aircraft. |
| `fetch_arrivals_airport()` | `fetch_arrivals_airport( self: Any, airport: str, begin: int, end: int, client_id: str = None, client_secret: str = None ) -> Dict[str, Any] \| None` | Fetch arrivals airport. |
| `fetch_departures_airport()` | `fetch_departures_airport( self: Any, airport: str, begin: int, end: int, client_id: str = None, client_secret: str = None ) -> Dict[str, Any] \| None` | Fetch departures airport. |
| `fetch_track_aircraft()` | `fetch_track_aircraft( self: Any, icao24: str, time_value: int = None, client_id: str = None, client_secret: str = None ) -> Dict[str, Any] \| None` | Fetch track aircraft. |
| `fetch()` | `fetch( self: Any, mode: str = 'states_bbox', icao24: str = '', airport: str = '', begin: int = None, end: int = None, time_value: int = None, lamin: float \| None = None, lomin: float \| None = None, lamax: float \| None = None, lomax: float \| None = None, extended: bool = False, client_id: str = None, client_secret: str = None, time: int = 20 ) -> Dict[str, Any] \| None` | Fetch OpenSky Network aircraft, airport, and state-vector data. |
| `create_schema()` | `create_schema( self: Any, function: str, tool: str, description: str, parameters: dict, required: list[str] ) -> Dict[str, str] \| None` | Create an AI tool schema. |
