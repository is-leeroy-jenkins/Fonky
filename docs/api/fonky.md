# API Reference: `fonky.py`

`fonky.py` exposes **110 module-level functions across 9 domains**. Every entry below is derived from the current source signature and implementation path.

## Domain Index

| Domain | Functions |
|---|---:|
| [Archives](#archives) | 11 |
| [Astronomical](#astronomical) | 10 |
| [Cloud](#cloud) | 8 |
| [Demographic](#demographic) | 5 |
| [Documents](#documents) | 18 |
| [Environmental](#environmental) | 19 |
| [Geospatial](#geospatial) | 10 |
| [Health](#health) | 4 |
| [Web](#web) | 25 |

## Archives

**11 functions**

| Function | Implementation |
|---|---|
| [`fetch_arxiv()`](#fetch_arxiv) | `ArXiv.fetch()` |
| [`fetch_google_drive()`](#fetch_google_drive) | `GoogleDrive.fetch()` |
| [`fetch_wikipedia()`](#fetch_wikipedia) | `Wikipedia.fetch()` |
| [`fetch_news()`](#fetch_news) | `TheNews.fetch()` |
| [`fetch_google_search()`](#fetch_google_search) | `GoogleSearch.fetch()` |
| [`fetch_gov_data()`](#fetch_gov_data) | `GovData.fetch()` |
| [`fetch_congress()`](#fetch_congress) | `Congress.fetch()` |
| [`fetch_internet_archive()`](#fetch_internet_archive) | `InternetArchive.fetch()` |
| [`fetch_grokipedia()`](#fetch_grokipedia) | `Grokipedia.fetch()` |
| [`load_arxiv()`](#load_arxiv) | `ArXivLoader.load()` |
| [`load_wikipedia()`](#load_wikipedia) | `WikiLoader.load()` |

### `fetch_arxiv()`

Fetch ArXiv research document retrieval.

```python
fetch_arxiv( question: str, max_documents: int = None, full_documents: bool = None, include_metadata: bool = None ) -> Any
```

**Implementation path:** `fonky.fetch_arxiv()` → `ArXiv.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `question` | `str` | Required | Value passed to ``ArXiv.fetch``. |
| `max_documents` | `int` | `None` | Value passed to ``ArXiv.fetch``. |
| `full_documents` | `bool` | `None` | Value passed to ``ArXiv.fetch``. |
| `include_metadata` | `bool` | `None` | Value passed to ``ArXiv.fetch``. |

**Returns:** Any: Value returned by ``ArXiv.fetch``.

### `fetch_google_drive()`

Fetch Google Drive document retrieval.

```python
fetch_google_drive( question: str, folder_id: str = 'root', results: int = 10, template: str = 'gdrive-query', mime_type: str = None, mode: str = 'documents' ) -> Any
```

**Implementation path:** `fonky.fetch_google_drive()` → `GoogleDrive.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `question` | `str` | Required | Value passed to ``GoogleDrive.fetch``. |
| `folder_id` | `str` | `'root'` | Value passed to ``GoogleDrive.fetch``. |
| `results` | `int` | `10` | Value passed to ``GoogleDrive.fetch``. |
| `template` | `str` | `'gdrive-query'` | Value passed to ``GoogleDrive.fetch``. |
| `mime_type` | `str` | `None` | Value passed to ``GoogleDrive.fetch``. |
| `mode` | `str` | `'documents'` | Value passed to ``GoogleDrive.fetch``. |

**Returns:** Any: Value returned by ``GoogleDrive.fetch``.

### `fetch_wikipedia()`

Fetch Wikipedia document retrieval.

```python
fetch_wikipedia( question: str, language: str = None, max_documents: int = None, include_metadata: bool = None ) -> Any
```

**Implementation path:** `fonky.fetch_wikipedia()` → `Wikipedia.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `question` | `str` | Required | Value passed to ``Wikipedia.fetch``. |
| `language` | `str` | `None` | Value passed to ``Wikipedia.fetch``. |
| `max_documents` | `int` | `None` | Value passed to ``Wikipedia.fetch``. |
| `include_metadata` | `bool` | `None` | Value passed to ``Wikipedia.fetch``. |

**Returns:** Any: Value returned by ``Wikipedia.fetch``.

### `fetch_news()`

Fetch The News API article retrieval.

```python
fetch_news( endpoint: str = 'all', query: str = '', language: str = 'en', categories: str = '', exclude_categories: str = '', locale: str = '', domains: str = '', exclude_domains: str = '', source_ids: str = '', exclude_source_ids: str = '', published_after: str = '', published_before: str = '', published_on: str = '', sort: str = 'published_at', limit: int = 10, page: int = 1, include_similar: bool = True, headlines_per_category: int = 6, time: int = 10, api_key: str = None ) -> Any
```

**Implementation path:** `fonky.fetch_news()` → `TheNews.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `endpoint` | `str` | `'all'` | Value passed to ``TheNews.fetch``. |
| `query` | `str` | `''` | Value passed to ``TheNews.fetch``. |
| `language` | `str` | `'en'` | Value passed to ``TheNews.fetch``. |
| `categories` | `str` | `''` | Value passed to ``TheNews.fetch``. |
| `exclude_categories` | `str` | `''` | Value passed to ``TheNews.fetch``. |
| `locale` | `str` | `''` | Value passed to ``TheNews.fetch``. |
| `domains` | `str` | `''` | Value passed to ``TheNews.fetch``. |
| `exclude_domains` | `str` | `''` | Value passed to ``TheNews.fetch``. |
| `source_ids` | `str` | `''` | Value passed to ``TheNews.fetch``. |
| `exclude_source_ids` | `str` | `''` | Value passed to ``TheNews.fetch``. |
| `published_after` | `str` | `''` | Value passed to ``TheNews.fetch``. |
| `published_before` | `str` | `''` | Value passed to ``TheNews.fetch``. |
| `published_on` | `str` | `''` | Value passed to ``TheNews.fetch``. |
| `sort` | `str` | `'published_at'` | Value passed to ``TheNews.fetch``. |
| `limit` | `int` | `10` | Value passed to ``TheNews.fetch``. |
| `page` | `int` | `1` | Value passed to ``TheNews.fetch``. |
| `include_similar` | `bool` | `True` | Value passed to ``TheNews.fetch``. |
| `headlines_per_category` | `int` | `6` | Value passed to ``TheNews.fetch``. |
| `time` | `int` | `10` | Value passed to ``TheNews.fetch``. |
| `api_key` | `str` | `None` | Value passed to ``TheNews.fetch``. |

**Returns:** Any: Value returned by ``TheNews.fetch``.

### `fetch_google_search()`

Fetch Google Custom Search retrieval.

```python
fetch_google_search( keywords: str, results: int = 10, start: int = 1, exact_terms: str = '', exclude_terms: str = '', file_type: str = '', date_restrict: str = '', gl: str = '', lr: str = '', safe: str = 'off', search_type: str = '', site_search: str = '', site_search_filter: str = '', sort: str = '', img_size: str = '', img_type: str = '', img_color_type: str = '', img_dominant_color: str = '', time: int = 10, api_key: str = None, cse_id: str = None ) -> Any
```

**Implementation path:** `fonky.fetch_google_search()` → `GoogleSearch.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keywords` | `str` | Required | Value passed to ``GoogleSearch.fetch``. |
| `results` | `int` | `10` | Value passed to ``GoogleSearch.fetch``. |
| `start` | `int` | `1` | Value passed to ``GoogleSearch.fetch``. |
| `exact_terms` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `exclude_terms` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `file_type` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `date_restrict` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `gl` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `lr` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `safe` | `str` | `'off'` | Value passed to ``GoogleSearch.fetch``. |
| `search_type` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `site_search` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `site_search_filter` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `sort` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `img_size` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `img_type` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `img_color_type` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `img_dominant_color` | `str` | `''` | Value passed to ``GoogleSearch.fetch``. |
| `time` | `int` | `10` | Value passed to ``GoogleSearch.fetch``. |
| `api_key` | `str` | `None` | Value passed to ``GoogleSearch.fetch``. |
| `cse_id` | `str` | `None` | Value passed to ``GoogleSearch.fetch``. |

**Returns:** Any: Value returned by ``GoogleSearch.fetch``.

### `fetch_gov_data()`

Fetch Data.gov package and collection retrieval.

```python
fetch_gov_data( mode: str = 'search', query: str = '', page_size: int = 10, offset_mark: str = '*', sort_field: str = 'score', sort_order: str = 'DESC', package_id: str = '', collection: str = '', start_date: str = '', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_gov_data()` → `GovData.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'search'` | Value passed to ``GovData.fetch``. |
| `query` | `str` | `''` | Value passed to ``GovData.fetch``. |
| `page_size` | `int` | `10` | Value passed to ``GovData.fetch``. |
| `offset_mark` | `str` | `'*'` | Value passed to ``GovData.fetch``. |
| `sort_field` | `str` | `'score'` | Value passed to ``GovData.fetch``. |
| `sort_order` | `str` | `'DESC'` | Value passed to ``GovData.fetch``. |
| `package_id` | `str` | `''` | Value passed to ``GovData.fetch``. |
| `collection` | `str` | `''` | Value passed to ``GovData.fetch``. |
| `start_date` | `str` | `''` | Value passed to ``GovData.fetch``. |
| `time` | `int` | `20` | Value passed to ``GovData.fetch``. |

**Returns:** Any: Value returned by ``GovData.fetch``.

### `fetch_congress()`

Fetch Congress.gov legislative data retrieval.

```python
fetch_congress( mode: str = 'congresses', congress: int = 0, bill_type: str = '', bill_number: int = 0, law_type: str = '', law_number: int = 0, report_type: str = '', report_number: int = 0, offset: int = 0, limit: int = 20, sort: str = 'updateDate+desc', from_date_time: str = '', to_date_time: str = '', conference: bool = False, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_congress()` → `Congress.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'congresses'` | Value passed to ``Congress.fetch``. |
| `congress` | `int` | `0` | Value passed to ``Congress.fetch``. |
| `bill_type` | `str` | `''` | Value passed to ``Congress.fetch``. |
| `bill_number` | `int` | `0` | Value passed to ``Congress.fetch``. |
| `law_type` | `str` | `''` | Value passed to ``Congress.fetch``. |
| `law_number` | `int` | `0` | Value passed to ``Congress.fetch``. |
| `report_type` | `str` | `''` | Value passed to ``Congress.fetch``. |
| `report_number` | `int` | `0` | Value passed to ``Congress.fetch``. |
| `offset` | `int` | `0` | Value passed to ``Congress.fetch``. |
| `limit` | `int` | `20` | Value passed to ``Congress.fetch``. |
| `sort` | `str` | `'updateDate+desc'` | Value passed to ``Congress.fetch``. |
| `from_date_time` | `str` | `''` | Value passed to ``Congress.fetch``. |
| `to_date_time` | `str` | `''` | Value passed to ``Congress.fetch``. |
| `conference` | `bool` | `False` | Value passed to ``Congress.fetch``. |
| `time` | `int` | `20` | Value passed to ``Congress.fetch``. |

**Returns:** Any: Value returned by ``Congress.fetch``.

### `fetch_internet_archive()`

Fetch Internet Archive search and metadata retrieval.

```python
fetch_internet_archive( keywords: str, fields: List[str] | None = None, rows: int = 10, page: int = 1, sort: str = 'downloads desc', media_type: str = '', collection: str = '', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_internet_archive()` → `InternetArchive.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `keywords` | `str` | Required | Value passed to ``InternetArchive.fetch``. |
| `fields` | `List[str] | None` | `None` | Value passed to ``InternetArchive.fetch``. |
| `rows` | `int` | `10` | Value passed to ``InternetArchive.fetch``. |
| `page` | `int` | `1` | Value passed to ``InternetArchive.fetch``. |
| `sort` | `str` | `'downloads desc'` | Value passed to ``InternetArchive.fetch``. |
| `media_type` | `str` | `''` | Value passed to ``InternetArchive.fetch``. |
| `collection` | `str` | `''` | Value passed to ``InternetArchive.fetch``. |
| `time` | `int` | `20` | Value passed to ``InternetArchive.fetch``. |

**Returns:** Any: Value returned by ``InternetArchive.fetch``.

### `fetch_grokipedia()`

Fetch Grokipedia search and page retrieval.

```python
fetch_grokipedia( mode: str = 'search', query: str = '', page: str = '', limit: int = 12, offset: int = 0, include_content: bool = True ) -> Any
```

**Implementation path:** `fonky.fetch_grokipedia()` → `Grokipedia.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'search'` | Value passed to ``Grokipedia.fetch``. |
| `query` | `str` | `''` | Value passed to ``Grokipedia.fetch``. |
| `page` | `str` | `''` | Value passed to ``Grokipedia.fetch``. |
| `limit` | `int` | `12` | Value passed to ``Grokipedia.fetch``. |
| `offset` | `int` | `0` | Value passed to ``Grokipedia.fetch``. |
| `include_content` | `bool` | `True` | Value passed to ``Grokipedia.fetch``. |

**Returns:** Any: Value returned by ``Grokipedia.fetch``.

### `load_arxiv()`

Load source content.

```python
load_arxiv( question: str ) -> Any
```

**Implementation path:** `fonky.load_arxiv()` → `ArXivLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `question` | `str` | Required | Value passed to ``ArXivLoader.load``. |

**Returns:** Any: Value returned by ``ArXivLoader.load``.

### `load_wikipedia()`

Load source content.

```python
load_wikipedia( question: str ) -> Any
```

**Implementation path:** `fonky.load_wikipedia()` → `WikiLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `question` | `str` | Required | Value passed to ``WikiLoader.load``. |

**Returns:** Any: Value returned by ``WikiLoader.load``.

## Astronomical

**10 functions**

| Function | Implementation |
|---|---|
| [`fetch_naval_observatory()`](#fetch_naval_observatory) | `NavalObservatory.fetch()` |
| [`fetch_satellite_center()`](#fetch_satellite_center) | `SatelliteCenter.fetch()` |
| [`fetch_nearby_objects()`](#fetch_nearby_objects) | `NearbyObjects.fetch()` |
| [`fetch_open_science()`](#fetch_open_science) | `OpenScience.fetch()` |
| [`fetch_space_weather()`](#fetch_space_weather) | `SpaceWeather.fetch()` |
| [`fetch_astro_catalog()`](#fetch_astro_catalog) | `AstroCatalog.fetch()` |
| [`fetch_astro_query()`](#fetch_astro_query) | `AstroQuery.fetch()` |
| [`fetch_star_map()`](#fetch_star_map) | `StarMap.fetch()` |
| [`fetch_star_chart()`](#fetch_star_chart) | `StarChart.fetch()` |
| [`fetch_open_sky()`](#fetch_open_sky) | `OpenSky.fetch()` |

### `fetch_naval_observatory()`

Fetch U.S. Naval Observatory celestial-navigation data.

```python
fetch_naval_observatory( mode: str = 'celnav', date_value: str = '', time_value: str = '', latitude: float = 0.0, longitude: float = 0.0, location_label: str = '', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_naval_observatory()` → `NavalObservatory.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'celnav'` | Value passed to ``NavalObservatory.fetch``. |
| `date_value` | `str` | `''` | Value passed to ``NavalObservatory.fetch``. |
| `time_value` | `str` | `''` | Value passed to ``NavalObservatory.fetch``. |
| `latitude` | `float` | `0.0` | Value passed to ``NavalObservatory.fetch``. |
| `longitude` | `float` | `0.0` | Value passed to ``NavalObservatory.fetch``. |
| `location_label` | `str` | `''` | Value passed to ``NavalObservatory.fetch``. |
| `time` | `int` | `20` | Value passed to ``NavalObservatory.fetch``. |

**Returns:** Any: Value returned by ``NavalObservatory.fetch``.

### `fetch_satellite_center()`

Fetch SSC satellite observatory, ground-station, and location data.

```python
fetch_satellite_center( mode: str = 'observatories', query: str = '', start_time: str = '', end_time: str = '', coordinate_systems: str = 'gse', resolution_factor: int = 1, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_satellite_center()` → `SatelliteCenter.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'observatories'` | Value passed to ``SatelliteCenter.fetch``. |
| `query` | `str` | `''` | Value passed to ``SatelliteCenter.fetch``. |
| `start_time` | `str` | `''` | Value passed to ``SatelliteCenter.fetch``. |
| `end_time` | `str` | `''` | Value passed to ``SatelliteCenter.fetch``. |
| `coordinate_systems` | `str` | `'gse'` | Value passed to ``SatelliteCenter.fetch``. |
| `resolution_factor` | `int` | `1` | Value passed to ``SatelliteCenter.fetch``. |
| `time` | `int` | `20` | Value passed to ``SatelliteCenter.fetch``. |

**Returns:** Any: Value returned by ``SatelliteCenter.fetch``.

### `fetch_nearby_objects()`

Fetch JPL SSD and CNEOS near-Earth object data.

```python
fetch_nearby_objects( mode: str = 'close_approaches', start_date: str = '', end_date: str = '', query: str = '', query_type: str = 'sstr', dist_max: str = '10LD', body: str = 'Earth', sort: str = 'date', limit: int = 20, dv: float = 6.0, dur: int = 360, stay: int = 8, launch: str = '2020-2045', h: float = 26.0, occ: int = 7, include_physical: bool = True, include_close_approaches: bool = True, ca_body: str = 'Earth', include_discovery: bool = True, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_nearby_objects()` → `NearbyObjects.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'close_approaches'` | Value passed to ``NearbyObjects.fetch``. |
| `start_date` | `str` | `''` | Value passed to ``NearbyObjects.fetch``. |
| `end_date` | `str` | `''` | Value passed to ``NearbyObjects.fetch``. |
| `query` | `str` | `''` | Value passed to ``NearbyObjects.fetch``. |
| `query_type` | `str` | `'sstr'` | Value passed to ``NearbyObjects.fetch``. |
| `dist_max` | `str` | `'10LD'` | Value passed to ``NearbyObjects.fetch``. |
| `body` | `str` | `'Earth'` | Value passed to ``NearbyObjects.fetch``. |
| `sort` | `str` | `'date'` | Value passed to ``NearbyObjects.fetch``. |
| `limit` | `int` | `20` | Value passed to ``NearbyObjects.fetch``. |
| `dv` | `float` | `6.0` | Value passed to ``NearbyObjects.fetch``. |
| `dur` | `int` | `360` | Value passed to ``NearbyObjects.fetch``. |
| `stay` | `int` | `8` | Value passed to ``NearbyObjects.fetch``. |
| `launch` | `str` | `'2020-2045'` | Value passed to ``NearbyObjects.fetch``. |
| `h` | `float` | `26.0` | Value passed to ``NearbyObjects.fetch``. |
| `occ` | `int` | `7` | Value passed to ``NearbyObjects.fetch``. |
| `include_physical` | `bool` | `True` | Value passed to ``NearbyObjects.fetch``. |
| `include_close_approaches` | `bool` | `True` | Value passed to ``NearbyObjects.fetch``. |
| `ca_body` | `str` | `'Earth'` | Value passed to ``NearbyObjects.fetch``. |
| `include_discovery` | `bool` | `True` | Value passed to ``NearbyObjects.fetch``. |
| `time` | `int` | `20` | Value passed to ``NearbyObjects.fetch``. |

**Returns:** Any: Value returned by ``NearbyObjects.fetch``.

### `fetch_open_science()`

Fetch NASA Open Science Data Repository resources.

```python
fetch_open_science( mode: str = 'dataset', query: str = '', accession: str = '', format_value: str = 'json', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_open_science()` → `OpenScience.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'dataset'` | Value passed to ``OpenScience.fetch``. |
| `query` | `str` | `''` | Value passed to ``OpenScience.fetch``. |
| `accession` | `str` | `''` | Value passed to ``OpenScience.fetch``. |
| `format_value` | `str` | `'json'` | Value passed to ``OpenScience.fetch``. |
| `time` | `int` | `20` | Value passed to ``OpenScience.fetch``. |

**Returns:** Any: Value returned by ``OpenScience.fetch``.

### `fetch_space_weather()`

Fetch NASA DONKI space weather endpoints.

```python
fetch_space_weather( mode: str = 'cme', start_date: str = '', end_date: str = '', time: int = 20, location: str = 'ALL', catalog: str = 'ALL', notification_type: str = 'all', most_accurate_only: bool = True, complete_entry_only: bool = True, speed: int = 0, half_angle: int = 0, keyword: str = '', api_key: str = None ) -> Any
```

**Implementation path:** `fonky.fetch_space_weather()` → `SpaceWeather.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'cme'` | Value passed to ``SpaceWeather.fetch``. |
| `start_date` | `str` | `''` | Value passed to ``SpaceWeather.fetch``. |
| `end_date` | `str` | `''` | Value passed to ``SpaceWeather.fetch``. |
| `time` | `int` | `20` | Value passed to ``SpaceWeather.fetch``. |
| `location` | `str` | `'ALL'` | Value passed to ``SpaceWeather.fetch``. |
| `catalog` | `str` | `'ALL'` | Value passed to ``SpaceWeather.fetch``. |
| `notification_type` | `str` | `'all'` | Value passed to ``SpaceWeather.fetch``. |
| `most_accurate_only` | `bool` | `True` | Value passed to ``SpaceWeather.fetch``. |
| `complete_entry_only` | `bool` | `True` | Value passed to ``SpaceWeather.fetch``. |
| `speed` | `int` | `0` | Value passed to ``SpaceWeather.fetch``. |
| `half_angle` | `int` | `0` | Value passed to ``SpaceWeather.fetch``. |
| `keyword` | `str` | `''` | Value passed to ``SpaceWeather.fetch``. |
| `api_key` | `str` | `None` | Value passed to ``SpaceWeather.fetch``. |

**Returns:** Any: Value returned by ``SpaceWeather.fetch``.

### `fetch_astro_catalog()`

Fetch Open Astronomy Catalog queries.

```python
fetch_astro_catalog( mode: str = 'object_query', query: str = '', quantity: str = '', attributes: str = '', arguments: str = '', ra: str = '', dec: str = '', radius: int = 2, data_format: str = 'json', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_astro_catalog()` → `AstroCatalog.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'object_query'` | Value passed to ``AstroCatalog.fetch``. |
| `query` | `str` | `''` | Value passed to ``AstroCatalog.fetch``. |
| `quantity` | `str` | `''` | Value passed to ``AstroCatalog.fetch``. |
| `attributes` | `str` | `''` | Value passed to ``AstroCatalog.fetch``. |
| `arguments` | `str` | `''` | Value passed to ``AstroCatalog.fetch``. |
| `ra` | `str` | `''` | Value passed to ``AstroCatalog.fetch``. |
| `dec` | `str` | `''` | Value passed to ``AstroCatalog.fetch``. |
| `radius` | `int` | `2` | Value passed to ``AstroCatalog.fetch``. |
| `data_format` | `str` | `'json'` | Value passed to ``AstroCatalog.fetch``. |
| `time` | `int` | `20` | Value passed to ``AstroCatalog.fetch``. |

**Returns:** Any: Value returned by ``AstroCatalog.fetch``.

### `fetch_astro_query()`

Fetch Simbad and astronomy object search operations.

```python
fetch_astro_query( mode: str = 'object_search', query: str = '', ra: str = '', dec: str = '', radius: float = 0.5, radius_unit: str = 'deg', row_limit: int = 100 ) -> Any
```

**Implementation path:** `fonky.fetch_astro_query()` → `AstroQuery.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'object_search'` | Value passed to ``AstroQuery.fetch``. |
| `query` | `str` | `''` | Value passed to ``AstroQuery.fetch``. |
| `ra` | `str` | `''` | Value passed to ``AstroQuery.fetch``. |
| `dec` | `str` | `''` | Value passed to ``AstroQuery.fetch``. |
| `radius` | `float` | `0.5` | Value passed to ``AstroQuery.fetch``. |
| `radius_unit` | `str` | `'deg'` | Value passed to ``AstroQuery.fetch``. |
| `row_limit` | `int` | `100` | Value passed to ``AstroQuery.fetch``. |

**Returns:** Any: Value returned by ``AstroQuery.fetch``.

### `fetch_star_map()`

Fetch astronomical object map links and imagery.

```python
fetch_star_map( mode: str = 'object_link', query: str = '', ra: float = 0.0, dec: float = 0.0, zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_star_map()` → `StarMap.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'object_link'` | Value passed to ``StarMap.fetch``. |
| `query` | `str` | `''` | Value passed to ``StarMap.fetch``. |
| `ra` | `float` | `0.0` | Value passed to ``StarMap.fetch``. |
| `dec` | `float` | `0.0` | Value passed to ``StarMap.fetch``. |
| `zoom` | `int` | `5` | Value passed to ``StarMap.fetch``. |
| `image_source` | `str` | `'DSS2'` | Value passed to ``StarMap.fetch``. |
| `box_color` | `str` | `'yellow'` | Value passed to ``StarMap.fetch``. |
| `show_box` | `bool` | `True` | Value passed to ``StarMap.fetch``. |
| `show_grid` | `bool` | `True` | Value passed to ``StarMap.fetch``. |
| `show_lines` | `bool` | `True` | Value passed to ``StarMap.fetch``. |
| `show_boundaries` | `bool` | `True` | Value passed to ``StarMap.fetch``. |
| `show_const_names` | `bool` | `False` | Value passed to ``StarMap.fetch``. |
| `time` | `int` | `20` | Value passed to ``StarMap.fetch``. |

**Returns:** Any: Value returned by ``StarMap.fetch``.

### `fetch_star_chart()`

Fetch static star chart and coordinate chart generation.

```python
fetch_star_chart( mode: str = 'object_chart', query: str = '', ra: float = 0.0, dec: float = 0.0, zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, width: int = 900, height: int = 450, magnitude: float = 7.5, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_star_chart()` → `StarChart.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'object_chart'` | Value passed to ``StarChart.fetch``. |
| `query` | `str` | `''` | Value passed to ``StarChart.fetch``. |
| `ra` | `float` | `0.0` | Value passed to ``StarChart.fetch``. |
| `dec` | `float` | `0.0` | Value passed to ``StarChart.fetch``. |
| `zoom` | `int` | `5` | Value passed to ``StarChart.fetch``. |
| `image_source` | `str` | `'DSS2'` | Value passed to ``StarChart.fetch``. |
| `box_color` | `str` | `'yellow'` | Value passed to ``StarChart.fetch``. |
| `show_box` | `bool` | `True` | Value passed to ``StarChart.fetch``. |
| `show_grid` | `bool` | `True` | Value passed to ``StarChart.fetch``. |
| `show_lines` | `bool` | `True` | Value passed to ``StarChart.fetch``. |
| `show_boundaries` | `bool` | `True` | Value passed to ``StarChart.fetch``. |
| `show_const_names` | `bool` | `False` | Value passed to ``StarChart.fetch``. |
| `width` | `int` | `900` | Value passed to ``StarChart.fetch``. |
| `height` | `int` | `450` | Value passed to ``StarChart.fetch``. |
| `magnitude` | `float` | `7.5` | Value passed to ``StarChart.fetch``. |
| `time` | `int` | `20` | Value passed to ``StarChart.fetch``. |

**Returns:** Any: Value returned by ``StarChart.fetch``.

### `fetch_open_sky()`

Fetch OpenSky Network aircraft, airport, and state-vector data.

```python
fetch_open_sky( mode: str = 'states_bbox', icao24: str = '', airport: str = '', begin: int = None, end: int = None, time_value: int = None, lamin: float | None = None, lomin: float | None = None, lamax: float | None = None, lomax: float | None = None, extended: bool = False, client_id: str = None, client_secret: str = None, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_open_sky()` → `OpenSky.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'states_bbox'` | Value passed to ``OpenSky.fetch``. |
| `icao24` | `str` | `''` | Value passed to ``OpenSky.fetch``. |
| `airport` | `str` | `''` | Value passed to ``OpenSky.fetch``. |
| `begin` | `int` | `None` | Value passed to ``OpenSky.fetch``. |
| `end` | `int` | `None` | Value passed to ``OpenSky.fetch``. |
| `time_value` | `int` | `None` | Value passed to ``OpenSky.fetch``. |
| `lamin` | `float | None` | `None` | Value passed to ``OpenSky.fetch``. |
| `lomin` | `float | None` | `None` | Value passed to ``OpenSky.fetch``. |
| `lamax` | `float | None` | `None` | Value passed to ``OpenSky.fetch``. |
| `lomax` | `float | None` | `None` | Value passed to ``OpenSky.fetch``. |
| `extended` | `bool` | `False` | Value passed to ``OpenSky.fetch``. |
| `client_id` | `str` | `None` | Value passed to ``OpenSky.fetch``. |
| `client_secret` | `str` | `None` | Value passed to ``OpenSky.fetch``. |
| `time` | `int` | `20` | Value passed to ``OpenSky.fetch``. |

**Returns:** Any: Value returned by ``OpenSky.fetch``.

## Cloud

**8 functions**

| Function | Implementation |
|---|---|
| [`load_google_drive_file()`](#load_google_drive_file) | `GoogleDriveLoader.load_file()` |
| [`load_google_drive_folder()`](#load_google_drive_folder) | `GoogleDriveLoader.load_folder()` |
| [`load_onedrive()`](#load_onedrive) | `OneDriveDocLoader.load()` |
| [`load_google_cloud_file()`](#load_google_cloud_file) | `GoogleCloudFileLoader.load()` |
| [`load_aws_file()`](#load_aws_file) | `AwsFileLoader.load()` |
| [`load_google_speech_to_text()`](#load_google_speech_to_text) | `GoogleSpeechToTextLoader.load()` |
| [`load_google_bucket()`](#load_google_bucket) | `GoogleBucketLoader.load()` |
| [`load_aws_bucket()`](#load_aws_bucket) | `AwsBucketLoader.load()` |

### `load_google_drive_file()`

Load a provider file.

```python
load_google_drive_file( file_id: str, recursive: bool = False ) -> Any
```

**Implementation path:** `fonky.load_google_drive_file()` → `GoogleDriveLoader.load_file()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `file_id` | `str` | Required | Value passed to ``GoogleDriveLoader.load_file``. |
| `recursive` | `bool` | `False` | Value passed to ``GoogleDriveLoader.load_file``. |

**Returns:** Any: Value returned by ``GoogleDriveLoader.load_file``.

### `load_google_drive_folder()`

Load provider folder content.

```python
load_google_drive_folder( folder_id: str, recursive: bool = False ) -> Any
```

**Implementation path:** `fonky.load_google_drive_folder()` → `GoogleDriveLoader.load_folder()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `folder_id` | `str` | Required | Value passed to ``GoogleDriveLoader.load_folder``. |
| `recursive` | `bool` | `False` | Value passed to ``GoogleDriveLoader.load_folder``. |

**Returns:** Any: Value returned by ``GoogleDriveLoader.load_folder``.

### `load_onedrive()`

Load source content.

```python
load_onedrive( drive_id: str, folder_path: Optional[str] = None, object_ids: Optional[List[str]] = None, auth_with_token: bool = True ) -> Any
```

**Implementation path:** `fonky.load_onedrive()` → `OneDriveDocLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `drive_id` | `str` | Required | Value passed to ``OneDriveDocLoader.load``. |
| `folder_path` | `Optional[str]` | `None` | Value passed to ``OneDriveDocLoader.load``. |
| `object_ids` | `Optional[List[str]]` | `None` | Value passed to ``OneDriveDocLoader.load``. |
| `auth_with_token` | `bool` | `True` | Value passed to ``OneDriveDocLoader.load``. |

**Returns:** Any: Value returned by ``OneDriveDocLoader.load``.

### `load_google_cloud_file()`

Load source content.

```python
load_google_cloud_file( project_name: str, bucket: str, blob: str ) -> Any
```

**Implementation path:** `fonky.load_google_cloud_file()` → `GoogleCloudFileLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `project_name` | `str` | Required | Value passed to ``GoogleCloudFileLoader.load``. |
| `bucket` | `str` | Required | Value passed to ``GoogleCloudFileLoader.load``. |
| `blob` | `str` | Required | Value passed to ``GoogleCloudFileLoader.load``. |

**Returns:** Any: Value returned by ``GoogleCloudFileLoader.load``.

### `load_aws_file()`

Load source content.

```python
load_aws_file( bucket: str, key: str, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None ) -> Any
```

**Implementation path:** `fonky.load_aws_file()` → `AwsFileLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bucket` | `str` | Required | Value passed to ``AwsFileLoader.load``. |
| `key` | `str` | Required | Value passed to ``AwsFileLoader.load``. |
| `aws_access_key_id` | `Optional[str]` | `None` | Value passed to ``AwsFileLoader.load``. |
| `aws_secret_access_key` | `Optional[str]` | `None` | Value passed to ``AwsFileLoader.load``. |
| `aws_session_token` | `Optional[str]` | `None` | Value passed to ``AwsFileLoader.load``. |
| `region_name` | `Optional[str]` | `None` | Value passed to ``AwsFileLoader.load``. |

**Returns:** Any: Value returned by ``AwsFileLoader.load``.

### `load_google_speech_to_text()`

Load source content.

```python
load_google_speech_to_text( project_id: str, file_path: str, config: Optional[Dict[str, Any]] = None ) -> Any
```

**Implementation path:** `fonky.load_google_speech_to_text()` → `GoogleSpeechToTextLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `project_id` | `str` | Required | Value passed to ``GoogleSpeechToTextLoader.load``. |
| `file_path` | `str` | Required | Value passed to ``GoogleSpeechToTextLoader.load``. |
| `config` | `Optional[Dict[str, Any]]` | `None` | Value passed to ``GoogleSpeechToTextLoader.load``. |

**Returns:** Any: Value returned by ``GoogleSpeechToTextLoader.load``.

### `load_google_bucket()`

Load source content.

```python
load_google_bucket( project_name: str, bucket: str, prefix: Optional[str] = None, continue_on_failure: bool = False ) -> Any
```

**Implementation path:** `fonky.load_google_bucket()` → `GoogleBucketLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `project_name` | `str` | Required | Value passed to ``GoogleBucketLoader.load``. |
| `bucket` | `str` | Required | Value passed to ``GoogleBucketLoader.load``. |
| `prefix` | `Optional[str]` | `None` | Value passed to ``GoogleBucketLoader.load``. |
| `continue_on_failure` | `bool` | `False` | Value passed to ``GoogleBucketLoader.load``. |

**Returns:** Any: Value returned by ``GoogleBucketLoader.load``.

### `load_aws_bucket()`

Load source content.

```python
load_aws_bucket( bucket: str, prefix: Optional[str] = None, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None, endpoint_url: Optional[str] = None ) -> Any
```

**Implementation path:** `fonky.load_aws_bucket()` → `AwsBucketLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bucket` | `str` | Required | Value passed to ``AwsBucketLoader.load``. |
| `prefix` | `Optional[str]` | `None` | Value passed to ``AwsBucketLoader.load``. |
| `aws_access_key_id` | `Optional[str]` | `None` | Value passed to ``AwsBucketLoader.load``. |
| `aws_secret_access_key` | `Optional[str]` | `None` | Value passed to ``AwsBucketLoader.load``. |
| `aws_session_token` | `Optional[str]` | `None` | Value passed to ``AwsBucketLoader.load``. |
| `region_name` | `Optional[str]` | `None` | Value passed to ``AwsBucketLoader.load``. |
| `endpoint_url` | `Optional[str]` | `None` | Value passed to ``AwsBucketLoader.load``. |

**Returns:** Any: Value returned by ``AwsBucketLoader.load``.

## Demographic

**5 functions**

| Function | Implementation |
|---|---|
| [`fetch_census_data()`](#fetch_census_data) | `CensusData.fetch()` |
| [`fetch_socrata()`](#fetch_socrata) | `Socrata.fetch()` |
| [`fetch_united_nations()`](#fetch_united_nations) | `UnitedNations.fetch()` |
| [`fetch_world_population()`](#fetch_world_population) | `WorldPopulation.fetch()` |
| [`load_open_city()`](#load_open_city) | `OpenCityLoader.load()` |

### `fetch_census_data()`

Fetch U.S. Census dataset and variable retrieval.

```python
fetch_census_data( mode: str = 'variables', year: str = '2022', dataset: str = 'acs/acs5', fields: str = 'NAME,B01001_001E', geography_for: str = 'state:*', geography_in: str = '', predicates: str = '', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_census_data()` → `CensusData.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'variables'` | Value passed to ``CensusData.fetch``. |
| `year` | `str` | `'2022'` | Value passed to ``CensusData.fetch``. |
| `dataset` | `str` | `'acs/acs5'` | Value passed to ``CensusData.fetch``. |
| `fields` | `str` | `'NAME,B01001_001E'` | Value passed to ``CensusData.fetch``. |
| `geography_for` | `str` | `'state:*'` | Value passed to ``CensusData.fetch``. |
| `geography_in` | `str` | `''` | Value passed to ``CensusData.fetch``. |
| `predicates` | `str` | `''` | Value passed to ``CensusData.fetch``. |
| `time` | `int` | `20` | Value passed to ``CensusData.fetch``. |

**Returns:** Any: Value returned by ``CensusData.fetch``.

### `fetch_socrata()`

Fetch Socrata dataset metadata and row retrieval.

```python
fetch_socrata( mode: str = 'rows', domain: str = 'data.cdc.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_socrata()` → `Socrata.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'rows'` | Value passed to ``Socrata.fetch``. |
| `domain` | `str` | `'data.cdc.gov'` | Value passed to ``Socrata.fetch``. |
| `dataset_id` | `str` | `''` | Value passed to ``Socrata.fetch``. |
| `select` | `str` | `''` | Value passed to ``Socrata.fetch``. |
| `where` | `str` | `''` | Value passed to ``Socrata.fetch``. |
| `order` | `str` | `''` | Value passed to ``Socrata.fetch``. |
| `group` | `str` | `''` | Value passed to ``Socrata.fetch``. |
| `limit` | `int` | `25` | Value passed to ``Socrata.fetch``. |
| `offset` | `int` | `0` | Value passed to ``Socrata.fetch``. |
| `time` | `int` | `20` | Value passed to ``Socrata.fetch``. |

**Returns:** Any: Value returned by ``Socrata.fetch``.

### `fetch_united_nations()`

Fetch United Nations SDMX dataset and query retrieval.

```python
fetch_united_nations( mode: str = 'datasets', query_path: str = '', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_united_nations()` → `UnitedNations.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'datasets'` | Value passed to ``UnitedNations.fetch``. |
| `query_path` | `str` | `''` | Value passed to ``UnitedNations.fetch``. |
| `time` | `int` | `20` | Value passed to ``UnitedNations.fetch``. |

**Returns:** Any: Value returned by ``UnitedNations.fetch``.

### `fetch_world_population()`

Fetch WorldPop catalog and raster metadata retrieval.

```python
fetch_world_population( mode: str = 'catalog', query: str = '', asset_path: str = '', page: int = 1, page_size: int = 25, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_world_population()` → `WorldPopulation.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'catalog'` | Value passed to ``WorldPopulation.fetch``. |
| `query` | `str` | `''` | Value passed to ``WorldPopulation.fetch``. |
| `asset_path` | `str` | `''` | Value passed to ``WorldPopulation.fetch``. |
| `page` | `int` | `1` | Value passed to ``WorldPopulation.fetch``. |
| `page_size` | `int` | `25` | Value passed to ``WorldPopulation.fetch``. |
| `time` | `int` | `20` | Value passed to ``WorldPopulation.fetch``. |

**Returns:** Any: Value returned by ``WorldPopulation.fetch``.

### `load_open_city()`

Load source content.

```python
load_open_city( city_id: str, dataset_id: str, limit: int = 100 ) -> Any
```

**Implementation path:** `fonky.load_open_city()` → `OpenCityLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `city_id` | `str` | Required | Value passed to ``OpenCityLoader.load``. |
| `dataset_id` | `str` | Required | Value passed to ``OpenCityLoader.load``. |
| `limit` | `int` | `100` | Value passed to ``OpenCityLoader.load``. |

**Returns:** Any: Value returned by ``OpenCityLoader.load``.

## Documents

**18 functions**

| Function | Implementation |
|---|---|
| [`load_text()`](#load_text) | `TextLoader.load()` |
| [`load_csv()`](#load_csv) | `CsvLoader.load()` |
| [`read_pdf()`](#read_pdf) | `PdfReader.load()` |
| [`load_pdf()`](#load_pdf) | `PdfLoader.load()` |
| [`load_excel()`](#load_excel) | `ExcelLoader.load()` |
| [`load_word()`](#load_word) | `WordLoader.load()` |
| [`load_markdown()`](#load_markdown) | `MarkdownLoader.load()` |
| [`load_html()`](#load_html) | `HtmlLoader.load()` |
| [`load_outlook()`](#load_outlook) | `OutlookLoader.load()` |
| [`load_spfx()`](#load_spfx) | `SpfxLoader.load()` |
| [`load_spfx_folder()`](#load_spfx_folder) | `SpfxLoader.load_folder()` |
| [`load_powerpoint()`](#load_powerpoint) | `PowerPointLoader.load()` |
| [`load_powerpoint_multiple()`](#load_powerpoint_multiple) | `PowerPointLoader.load_multiple()` |
| [`load_email()`](#load_email) | `EmailLoader.load()` |
| [`load_json()`](#load_json) | `JsonLoader.load()` |
| [`load_xml()`](#load_xml) | `XmlLoader.load()` |
| [`load_xml_tree()`](#load_xml_tree) | `XmlLoader.load_tree()` |
| [`load_jupyter_notebook()`](#load_jupyter_notebook) | `JupyterNotebookLoader.load()` |

### `load_text()`

Load source content.

```python
load_text( path: str, encoding: Optional[str] = None ) -> Any
```

**Implementation path:** `fonky.load_text()` → `TextLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``TextLoader.load``. |
| `encoding` | `Optional[str]` | `None` | Value passed to ``TextLoader.load``. |

**Returns:** Any: Value returned by ``TextLoader.load``.

### `load_csv()`

Load source content.

```python
load_csv( path: str, encoding: Optional[str] = 'utf-8', source_column: Optional[str] = None, delimiter: str = ',', quotechar: str = '"' ) -> Any
```

**Implementation path:** `fonky.load_csv()` → `CsvLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``CsvLoader.load``. |
| `encoding` | `Optional[str]` | `'utf-8'` | Value passed to ``CsvLoader.load``. |
| `source_column` | `Optional[str]` | `None` | Value passed to ``CsvLoader.load``. |
| `delimiter` | `str` | `','` | Value passed to ``CsvLoader.load``. |
| `quotechar` | `str` | `'"'` | Value passed to ``CsvLoader.load``. |

**Returns:** Any: Value returned by ``CsvLoader.load``.

### `read_pdf()`

Load source content.

```python
read_pdf( path: str, mode: str = 'single' ) -> Any
```

**Implementation path:** `fonky.read_pdf()` → `PdfReader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``PdfReader.load``. |
| `mode` | `str` | `'single'` | Value passed to ``PdfReader.load``. |

**Returns:** Any: Value returned by ``PdfReader.load``.

### `load_pdf()`

Load source content.

```python
load_pdf( path: str, mode: str = 'single', extract: str = 'plain', include: bool = False, format: str = 'markdown-img', size: int = 1000, overlap: int = 150, has_tables: bool = True ) -> Any
```

**Implementation path:** `fonky.load_pdf()` → `PdfLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``PdfLoader.load``. |
| `mode` | `str` | `'single'` | Value passed to ``PdfLoader.load``. |
| `extract` | `str` | `'plain'` | Value passed to ``PdfLoader.load``. |
| `include` | `bool` | `False` | Value passed to ``PdfLoader.load``. |
| `format` | `str` | `'markdown-img'` | Value passed to ``PdfLoader.load``. |
| `size` | `int` | `1000` | Value passed to ``PdfLoader.load``. |
| `overlap` | `int` | `150` | Value passed to ``PdfLoader.load``. |
| `has_tables` | `bool` | `True` | Value passed to ``PdfLoader.load``. |

**Returns:** Any: Value returned by ``PdfLoader.load``.

### `load_excel()`

Load source content.

```python
load_excel( path: str, mode: str = 'elements', has_headers: bool = True ) -> Any
```

**Implementation path:** `fonky.load_excel()` → `ExcelLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``ExcelLoader.load``. |
| `mode` | `str` | `'elements'` | Value passed to ``ExcelLoader.load``. |
| `has_headers` | `bool` | `True` | Value passed to ``ExcelLoader.load``. |

**Returns:** Any: Value returned by ``ExcelLoader.load``.

### `load_word()`

Load source content.

```python
load_word( path: str ) -> Any
```

**Implementation path:** `fonky.load_word()` → `WordLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``WordLoader.load``. |

**Returns:** Any: Value returned by ``WordLoader.load``.

### `load_markdown()`

Load source content.

```python
load_markdown( path: str ) -> Any
```

**Implementation path:** `fonky.load_markdown()` → `MarkdownLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``MarkdownLoader.load``. |

**Returns:** Any: Value returned by ``MarkdownLoader.load``.

### `load_html()`

Load source content.

```python
load_html( path: str ) -> Any
```

**Implementation path:** `fonky.load_html()` → `HtmlLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``HtmlLoader.load``. |

**Returns:** Any: Value returned by ``HtmlLoader.load``.

### `load_outlook()`

Load source content.

```python
load_outlook( path: str ) -> Any
```

**Implementation path:** `fonky.load_outlook()` → `OutlookLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``OutlookLoader.load``. |

**Returns:** Any: Value returned by ``OutlookLoader.load``.

### `load_spfx()`

Load source content.

```python
load_spfx( library_id: str ) -> Any
```

**Implementation path:** `fonky.load_spfx()` → `SpfxLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `library_id` | `str` | Required | Value passed to ``SpfxLoader.load``. |

**Returns:** Any: Value returned by ``SpfxLoader.load``.

### `load_spfx_folder()`

Load provider folder content.

```python
load_spfx_folder( library_id: str, folder_id: str ) -> Any
```

**Implementation path:** `fonky.load_spfx_folder()` → `SpfxLoader.load_folder()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `library_id` | `str` | Required | Value passed to ``SpfxLoader.load_folder``. |
| `folder_id` | `str` | Required | Value passed to ``SpfxLoader.load_folder``. |

**Returns:** Any: Value returned by ``SpfxLoader.load_folder``.

### `load_powerpoint()`

Load source content.

```python
load_powerpoint( path: str, mode: str = 'single' ) -> Any
```

**Implementation path:** `fonky.load_powerpoint()` → `PowerPointLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``PowerPointLoader.load``. |
| `mode` | `str` | `'single'` | Value passed to ``PowerPointLoader.load``. |

**Returns:** Any: Value returned by ``PowerPointLoader.load``.

### `load_powerpoint_multiple()`

Load multiple presentation elements.

```python
load_powerpoint_multiple( path: str ) -> Any
```

**Implementation path:** `fonky.load_powerpoint_multiple()` → `PowerPointLoader.load_multiple()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``PowerPointLoader.load_multiple``. |

**Returns:** Any: Value returned by ``PowerPointLoader.load_multiple``.

### `load_email()`

Load source content.

```python
load_email( path: str, mode: str = 'single', attachments: bool = True ) -> Any
```

**Implementation path:** `fonky.load_email()` → `EmailLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``EmailLoader.load``. |
| `mode` | `str` | `'single'` | Value passed to ``EmailLoader.load``. |
| `attachments` | `bool` | `True` | Value passed to ``EmailLoader.load``. |

**Returns:** Any: Value returned by ``EmailLoader.load``.

### `load_json()`

Load source content.

```python
load_json( filepath: str, is_text: bool = True, is_lines: bool = False ) -> Any
```

**Implementation path:** `fonky.load_json()` → `JsonLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `filepath` | `str` | Required | Value passed to ``JsonLoader.load``. |
| `is_text` | `bool` | `True` | Value passed to ``JsonLoader.load``. |
| `is_lines` | `bool` | `False` | Value passed to ``JsonLoader.load``. |

**Returns:** Any: Value returned by ``JsonLoader.load``.

### `load_xml()`

Load source content.

```python
load_xml( filepath: str ) -> Any
```

**Implementation path:** `fonky.load_xml()` → `XmlLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `filepath` | `str` | Required | Value passed to ``XmlLoader.load``. |

**Returns:** Any: Value returned by ``XmlLoader.load``.

### `load_xml_tree()`

Parse an XML element tree.

```python
load_xml_tree( filepath: str ) -> Any
```

**Implementation path:** `fonky.load_xml_tree()` → `XmlLoader.load_tree()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `filepath` | `str` | Required | Value passed to ``XmlLoader.load_tree``. |

**Returns:** Any: Value returned by ``XmlLoader.load_tree``.

### `load_jupyter_notebook()`

Load source content.

```python
load_jupyter_notebook( path: str, include_outputs: bool = False, max_output_length: int = 10, remove_newline: bool = False, traceback: bool = False ) -> Any
```

**Implementation path:** `fonky.load_jupyter_notebook()` → `JupyterNotebookLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``JupyterNotebookLoader.load``. |
| `include_outputs` | `bool` | `False` | Value passed to ``JupyterNotebookLoader.load``. |
| `max_output_length` | `int` | `10` | Value passed to ``JupyterNotebookLoader.load``. |
| `remove_newline` | `bool` | `False` | Value passed to ``JupyterNotebookLoader.load``. |
| `traceback` | `bool` | `False` | Value passed to ``JupyterNotebookLoader.load``. |

**Returns:** Any: Value returned by ``JupyterNotebookLoader.load``.

## Environmental

**19 functions**

| Function | Implementation |
|---|---|
| [`fetch_google_weather_current()`](#fetch_google_weather_current) | `GoogleWeather.fetch_current()` |
| [`fetch_google_weather_hourly_forecast()`](#fetch_google_weather_hourly_forecast) | `GoogleWeather.fetch_hourly_forecast()` |
| [`fetch_google_weather_daily_forecast()`](#fetch_google_weather_daily_forecast) | `GoogleWeather.fetch_daily_forecast()` |
| [`fetch_google_weather_hourly_history()`](#fetch_google_weather_hourly_history) | `GoogleWeather.fetch_hourly_history()` |
| [`fetch_google_weather_alerts()`](#fetch_google_weather_alerts) | `GoogleWeather.fetch_alerts()` |
| [`fetch_earth_observatory()`](#fetch_earth_observatory) | `EarthObservatory.fetch()` |
| [`fetch_open_weather()`](#fetch_open_weather) | `OpenWeather.fetch()` |
| [`fetch_historical_weather()`](#fetch_historical_weather) | `HistoricalWeather.fetch()` |
| [`fetch_usgs_earthquakes()`](#fetch_usgs_earthquakes) | `USGSEarthquakes.fetch()` |
| [`fetch_usgs_water_data()`](#fetch_usgs_water_data) | `USGSWaterData.fetch()` |
| [`fetch_air_now()`](#fetch_air_now) | `AirNow.fetch()` |
| [`fetch_climate_data()`](#fetch_climate_data) | `ClimateData.fetch()` |
| [`fetch_eonet()`](#fetch_eonet) | `EoNet.fetch()` |
| [`fetch_envirofacts()`](#fetch_envirofacts) | `EnviroFacts.fetch()` |
| [`fetch_tides_and_currents()`](#fetch_tides_and_currents) | `TidesAndCurrents.fetch()` |
| [`fetch_uv_index()`](#fetch_uv_index) | `UvIndex.fetch()` |
| [`fetch_purple_air()`](#fetch_purple_air) | `PurpleAir.fetch()` |
| [`fetch_open_aq()`](#fetch_open_aq) | `OpenAQ.fetch()` |
| [`fetch_firms()`](#fetch_firms) | `Firms.fetch()` |

### `fetch_google_weather_current()`

Fetch current.

```python
fetch_google_weather_current( address: str, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

**Implementation path:** `fonky.fetch_google_weather_current()` → `GoogleWeather.fetch_current()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `address` | `str` | Required | Value passed to ``GoogleWeather.fetch_current``. |
| `units_system` | `str` | `'METRIC'` | Value passed to ``GoogleWeather.fetch_current``. |
| `language_code` | `str` | `'en'` | Value passed to ``GoogleWeather.fetch_current``. |
| `time` | `int` | `10` | Value passed to ``GoogleWeather.fetch_current``. |

**Returns:** Any: Value returned by ``GoogleWeather.fetch_current``.

### `fetch_google_weather_hourly_forecast()`

Fetch hourly forecast.

```python
fetch_google_weather_hourly_forecast( address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

**Implementation path:** `fonky.fetch_google_weather_hourly_forecast()` → `GoogleWeather.fetch_hourly_forecast()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `address` | `str` | Required | Value passed to ``GoogleWeather.fetch_hourly_forecast``. |
| `hours` | `int` | `24` | Value passed to ``GoogleWeather.fetch_hourly_forecast``. |
| `units_system` | `str` | `'METRIC'` | Value passed to ``GoogleWeather.fetch_hourly_forecast``. |
| `language_code` | `str` | `'en'` | Value passed to ``GoogleWeather.fetch_hourly_forecast``. |
| `time` | `int` | `10` | Value passed to ``GoogleWeather.fetch_hourly_forecast``. |

**Returns:** Any: Value returned by ``GoogleWeather.fetch_hourly_forecast``.

### `fetch_google_weather_daily_forecast()`

Fetch daily forecast.

```python
fetch_google_weather_daily_forecast( address: str, days: int = 5, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

**Implementation path:** `fonky.fetch_google_weather_daily_forecast()` → `GoogleWeather.fetch_daily_forecast()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `address` | `str` | Required | Value passed to ``GoogleWeather.fetch_daily_forecast``. |
| `days` | `int` | `5` | Value passed to ``GoogleWeather.fetch_daily_forecast``. |
| `units_system` | `str` | `'METRIC'` | Value passed to ``GoogleWeather.fetch_daily_forecast``. |
| `language_code` | `str` | `'en'` | Value passed to ``GoogleWeather.fetch_daily_forecast``. |
| `time` | `int` | `10` | Value passed to ``GoogleWeather.fetch_daily_forecast``. |

**Returns:** Any: Value returned by ``GoogleWeather.fetch_daily_forecast``.

### `fetch_google_weather_hourly_history()`

Fetch hourly history.

```python
fetch_google_weather_hourly_history( address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

**Implementation path:** `fonky.fetch_google_weather_hourly_history()` → `GoogleWeather.fetch_hourly_history()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `address` | `str` | Required | Value passed to ``GoogleWeather.fetch_hourly_history``. |
| `hours` | `int` | `24` | Value passed to ``GoogleWeather.fetch_hourly_history``. |
| `units_system` | `str` | `'METRIC'` | Value passed to ``GoogleWeather.fetch_hourly_history``. |
| `language_code` | `str` | `'en'` | Value passed to ``GoogleWeather.fetch_hourly_history``. |
| `time` | `int` | `10` | Value passed to ``GoogleWeather.fetch_hourly_history``. |

**Returns:** Any: Value returned by ``GoogleWeather.fetch_hourly_history``.

### `fetch_google_weather_alerts()`

Fetch alerts.

```python
fetch_google_weather_alerts( address: str, language_code: str = 'en', time: int = 10 ) -> Any
```

**Implementation path:** `fonky.fetch_google_weather_alerts()` → `GoogleWeather.fetch_alerts()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `address` | `str` | Required | Value passed to ``GoogleWeather.fetch_alerts``. |
| `language_code` | `str` | `'en'` | Value passed to ``GoogleWeather.fetch_alerts``. |
| `time` | `int` | `10` | Value passed to ``GoogleWeather.fetch_alerts``. |

**Returns:** Any: Value returned by ``GoogleWeather.fetch_alerts``.

### `fetch_earth_observatory()`

Fetch NASA EONET events, categories, sources, and layers.

```python
fetch_earth_observatory( mode: str = 'events', status: str = 'open', category: str = '', source: str = '', limit: int = 20, days: int = 30, start_date: str = '', end_date: str = '', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_earth_observatory()` → `EarthObservatory.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'events'` | Value passed to ``EarthObservatory.fetch``. |
| `status` | `str` | `'open'` | Value passed to ``EarthObservatory.fetch``. |
| `category` | `str` | `''` | Value passed to ``EarthObservatory.fetch``. |
| `source` | `str` | `''` | Value passed to ``EarthObservatory.fetch``. |
| `limit` | `int` | `20` | Value passed to ``EarthObservatory.fetch``. |
| `days` | `int` | `30` | Value passed to ``EarthObservatory.fetch``. |
| `start_date` | `str` | `''` | Value passed to ``EarthObservatory.fetch``. |
| `end_date` | `str` | `''` | Value passed to ``EarthObservatory.fetch``. |
| `time` | `int` | `20` | Value passed to ``EarthObservatory.fetch``. |

**Returns:** Any: Value returned by ``EarthObservatory.fetch``.

### `fetch_open_weather()`

Fetch Open-Meteo current and forecast weather retrieval.

```python
fetch_open_weather( location: str, mode: str = 'current', zone: str = 'auto', forecast_days: int = 7, past_days: int = 0, count: int = 10 ) -> Any
```

**Implementation path:** `fonky.fetch_open_weather()` → `OpenWeather.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | `str` | Required | Value passed to ``OpenWeather.fetch``. |
| `mode` | `str` | `'current'` | Value passed to ``OpenWeather.fetch``. |
| `zone` | `str` | `'auto'` | Value passed to ``OpenWeather.fetch``. |
| `forecast_days` | `int` | `7` | Value passed to ``OpenWeather.fetch``. |
| `past_days` | `int` | `0` | Value passed to ``OpenWeather.fetch``. |
| `count` | `int` | `10` | Value passed to ``OpenWeather.fetch``. |

**Returns:** Any: Value returned by ``OpenWeather.fetch``.

### `fetch_historical_weather()`

Fetch historical weather archive retrieval.

```python
fetch_historical_weather( location: str, date: dt.date, zone: str = 'auto', count: int = 10 ) -> Any
```

**Implementation path:** `fonky.fetch_historical_weather()` → `HistoricalWeather.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | `str` | Required | Value passed to ``HistoricalWeather.fetch``. |
| `date` | `dt.date` | Required | Value passed to ``HistoricalWeather.fetch``. |
| `zone` | `str` | `'auto'` | Value passed to ``HistoricalWeather.fetch``. |
| `count` | `int` | `10` | Value passed to ``HistoricalWeather.fetch``. |

**Returns:** Any: Value returned by ``HistoricalWeather.fetch``.

### `fetch_usgs_earthquakes()`

Fetch USGS earthquake feed and query retrieval.

```python
fetch_usgs_earthquakes( mode: str = 'feed', feed: str = 'all_day.geojson', start_date: str = '', end_date: str = '', min_magnitude: float = 1.0, max_magnitude: float = 10.0, limit: int = 25, order_by: str = 'time', event_type: str = 'earthquake', latitude: float | None = None, longitude: float | None = None, max_radius_km: float | None = None, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_usgs_earthquakes()` → `USGSEarthquakes.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'feed'` | Value passed to ``USGSEarthquakes.fetch``. |
| `feed` | `str` | `'all_day.geojson'` | Value passed to ``USGSEarthquakes.fetch``. |
| `start_date` | `str` | `''` | Value passed to ``USGSEarthquakes.fetch``. |
| `end_date` | `str` | `''` | Value passed to ``USGSEarthquakes.fetch``. |
| `min_magnitude` | `float` | `1.0` | Value passed to ``USGSEarthquakes.fetch``. |
| `max_magnitude` | `float` | `10.0` | Value passed to ``USGSEarthquakes.fetch``. |
| `limit` | `int` | `25` | Value passed to ``USGSEarthquakes.fetch``. |
| `order_by` | `str` | `'time'` | Value passed to ``USGSEarthquakes.fetch``. |
| `event_type` | `str` | `'earthquake'` | Value passed to ``USGSEarthquakes.fetch``. |
| `latitude` | `float | None` | `None` | Value passed to ``USGSEarthquakes.fetch``. |
| `longitude` | `float | None` | `None` | Value passed to ``USGSEarthquakes.fetch``. |
| `max_radius_km` | `float | None` | `None` | Value passed to ``USGSEarthquakes.fetch``. |
| `time` | `int` | `20` | Value passed to ``USGSEarthquakes.fetch``. |

**Returns:** Any: Value returned by ``USGSEarthquakes.fetch``.

### `fetch_usgs_water_data()`

Fetch USGS water services records.

```python
fetch_usgs_water_data( mode: str = 'monitoring-locations', monitoring_location_id: str = '', state_code: str = '', county_code: str = '', site_type: str = '', parameter_code: str = '', limit: int = 25, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_usgs_water_data()` → `USGSWaterData.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'monitoring-locations'` | Value passed to ``USGSWaterData.fetch``. |
| `monitoring_location_id` | `str` | `''` | Value passed to ``USGSWaterData.fetch``. |
| `state_code` | `str` | `''` | Value passed to ``USGSWaterData.fetch``. |
| `county_code` | `str` | `''` | Value passed to ``USGSWaterData.fetch``. |
| `site_type` | `str` | `''` | Value passed to ``USGSWaterData.fetch``. |
| `parameter_code` | `str` | `''` | Value passed to ``USGSWaterData.fetch``. |
| `limit` | `int` | `25` | Value passed to ``USGSWaterData.fetch``. |
| `time` | `int` | `20` | Value passed to ``USGSWaterData.fetch``. |

**Returns:** Any: Value returned by ``USGSWaterData.fetch``.

### `fetch_air_now()`

Fetch AirNow current and forecast air quality data.

```python
fetch_air_now( mode: str = 'current-zip', zip_code: str = '', latitude: float | None = None, longitude: float | None = None, date: str = '', distance: int = 25, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_air_now()` → `AirNow.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'current-zip'` | Value passed to ``AirNow.fetch``. |
| `zip_code` | `str` | `''` | Value passed to ``AirNow.fetch``. |
| `latitude` | `float | None` | `None` | Value passed to ``AirNow.fetch``. |
| `longitude` | `float | None` | `None` | Value passed to ``AirNow.fetch``. |
| `date` | `str` | `''` | Value passed to ``AirNow.fetch``. |
| `distance` | `int` | `25` | Value passed to ``AirNow.fetch``. |
| `time` | `int` | `20` | Value passed to ``AirNow.fetch``. |

**Returns:** Any: Value returned by ``AirNow.fetch``.

### `fetch_climate_data()`

Fetch NOAA climate dataset and data records.

```python
fetch_climate_data( mode: str = 'datasets', keyword: str = '', dataset: str = '', start_date: str = '', end_date: str = '', stations: str = '', data_types: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_climate_data()` → `ClimateData.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'datasets'` | Value passed to ``ClimateData.fetch``. |
| `keyword` | `str` | `''` | Value passed to ``ClimateData.fetch``. |
| `dataset` | `str` | `''` | Value passed to ``ClimateData.fetch``. |
| `start_date` | `str` | `''` | Value passed to ``ClimateData.fetch``. |
| `end_date` | `str` | `''` | Value passed to ``ClimateData.fetch``. |
| `stations` | `str` | `''` | Value passed to ``ClimateData.fetch``. |
| `data_types` | `str` | `''` | Value passed to ``ClimateData.fetch``. |
| `limit` | `int` | `25` | Value passed to ``ClimateData.fetch``. |
| `offset` | `int` | `0` | Value passed to ``ClimateData.fetch``. |
| `time` | `int` | `20` | Value passed to ``ClimateData.fetch``. |

**Returns:** Any: Value returned by ``ClimateData.fetch``.

### `fetch_eonet()`

Fetch NASA EONET environmental event data.

```python
fetch_eonet( mode: str = 'events', source: str = '', category: str = '', status: str = 'open', limit: int = 25, days: int = 30, start_date: str = '', end_date: str = '', bbox: str = '', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_eonet()` → `EoNet.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'events'` | Value passed to ``EoNet.fetch``. |
| `source` | `str` | `''` | Value passed to ``EoNet.fetch``. |
| `category` | `str` | `''` | Value passed to ``EoNet.fetch``. |
| `status` | `str` | `'open'` | Value passed to ``EoNet.fetch``. |
| `limit` | `int` | `25` | Value passed to ``EoNet.fetch``. |
| `days` | `int` | `30` | Value passed to ``EoNet.fetch``. |
| `start_date` | `str` | `''` | Value passed to ``EoNet.fetch``. |
| `end_date` | `str` | `''` | Value passed to ``EoNet.fetch``. |
| `bbox` | `str` | `''` | Value passed to ``EoNet.fetch``. |
| `time` | `int` | `20` | Value passed to ``EoNet.fetch``. |

**Returns:** Any: Value returned by ``EoNet.fetch``.

### `fetch_envirofacts()`

Fetch EPA Envirofacts table and facility records.

```python
fetch_envirofacts( table_name: str = 'TRI_FACILITY', state_code: str = '', facility_name: str = '', limit: int = 25, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_envirofacts()` → `EnviroFacts.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `table_name` | `str` | `'TRI_FACILITY'` | Value passed to ``EnviroFacts.fetch``. |
| `state_code` | `str` | `''` | Value passed to ``EnviroFacts.fetch``. |
| `facility_name` | `str` | `''` | Value passed to ``EnviroFacts.fetch``. |
| `limit` | `int` | `25` | Value passed to ``EnviroFacts.fetch``. |
| `time` | `int` | `20` | Value passed to ``EnviroFacts.fetch``. |

**Returns:** Any: Value returned by ``EnviroFacts.fetch``.

### `fetch_tides_and_currents()`

Fetch NOAA tides, currents, and station data.

```python
fetch_tides_and_currents( mode: str = 'water-level', station_id: str = '', begin_date: str = '', end_date: str = '', datum: str = 'MLLW', units: str = 'metric', time_zone: str = 'gmt', interval: str = 'hilo', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_tides_and_currents()` → `TidesAndCurrents.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'water-level'` | Value passed to ``TidesAndCurrents.fetch``. |
| `station_id` | `str` | `''` | Value passed to ``TidesAndCurrents.fetch``. |
| `begin_date` | `str` | `''` | Value passed to ``TidesAndCurrents.fetch``. |
| `end_date` | `str` | `''` | Value passed to ``TidesAndCurrents.fetch``. |
| `datum` | `str` | `'MLLW'` | Value passed to ``TidesAndCurrents.fetch``. |
| `units` | `str` | `'metric'` | Value passed to ``TidesAndCurrents.fetch``. |
| `time_zone` | `str` | `'gmt'` | Value passed to ``TidesAndCurrents.fetch``. |
| `interval` | `str` | `'hilo'` | Value passed to ``TidesAndCurrents.fetch``. |
| `time` | `int` | `20` | Value passed to ``TidesAndCurrents.fetch``. |

**Returns:** Any: Value returned by ``TidesAndCurrents.fetch``.

### `fetch_uv_index()`

Fetch EPA UV Index current and forecast data.

```python
fetch_uv_index( mode: str = 'daily-zip', zip_code: str = '', city: str = '', state: str = '', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_uv_index()` → `UvIndex.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'daily-zip'` | Value passed to ``UvIndex.fetch``. |
| `zip_code` | `str` | `''` | Value passed to ``UvIndex.fetch``. |
| `city` | `str` | `''` | Value passed to ``UvIndex.fetch``. |
| `state` | `str` | `''` | Value passed to ``UvIndex.fetch``. |
| `time` | `int` | `20` | Value passed to ``UvIndex.fetch``. |

**Returns:** Any: Value returned by ``UvIndex.fetch``.

### `fetch_purple_air()`

Fetch PurpleAir sensor and air quality records.

```python
fetch_purple_air( mode: str = 'sensors', sensor_index: int = None, nwlng: float | None = None, nwlat: float | None = None, selng: float | None = None, selat: float | None = None, location_type: int = 0, max_age: int = 0, modified_since: int = 0, fields: str = '', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_purple_air()` → `PurpleAir.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'sensors'` | Value passed to ``PurpleAir.fetch``. |
| `sensor_index` | `int` | `None` | Value passed to ``PurpleAir.fetch``. |
| `nwlng` | `float | None` | `None` | Value passed to ``PurpleAir.fetch``. |
| `nwlat` | `float | None` | `None` | Value passed to ``PurpleAir.fetch``. |
| `selng` | `float | None` | `None` | Value passed to ``PurpleAir.fetch``. |
| `selat` | `float | None` | `None` | Value passed to ``PurpleAir.fetch``. |
| `location_type` | `int` | `0` | Value passed to ``PurpleAir.fetch``. |
| `max_age` | `int` | `0` | Value passed to ``PurpleAir.fetch``. |
| `modified_since` | `int` | `0` | Value passed to ``PurpleAir.fetch``. |
| `fields` | `str` | `''` | Value passed to ``PurpleAir.fetch``. |
| `time` | `int` | `20` | Value passed to ``PurpleAir.fetch``. |

**Returns:** Any: Value returned by ``PurpleAir.fetch``.

### `fetch_open_aq()`

Fetch OpenAQ location, measurement, and air-quality records.

```python
fetch_open_aq( mode: str = 'locations', location_id: int = None, parameter_id: int = None, country_id: int = None, coordinates: str = '', radius: int = 25000, providers_id: str = '', parameters_id: str = '', limit: int = 25, page: int = 1, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_open_aq()` → `OpenAQ.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'locations'` | Value passed to ``OpenAQ.fetch``. |
| `location_id` | `int` | `None` | Value passed to ``OpenAQ.fetch``. |
| `parameter_id` | `int` | `None` | Value passed to ``OpenAQ.fetch``. |
| `country_id` | `int` | `None` | Value passed to ``OpenAQ.fetch``. |
| `coordinates` | `str` | `''` | Value passed to ``OpenAQ.fetch``. |
| `radius` | `int` | `25000` | Value passed to ``OpenAQ.fetch``. |
| `providers_id` | `str` | `''` | Value passed to ``OpenAQ.fetch``. |
| `parameters_id` | `str` | `''` | Value passed to ``OpenAQ.fetch``. |
| `limit` | `int` | `25` | Value passed to ``OpenAQ.fetch``. |
| `page` | `int` | `1` | Value passed to ``OpenAQ.fetch``. |
| `time` | `int` | `20` | Value passed to ``OpenAQ.fetch``. |

**Returns:** Any: Value returned by ``OpenAQ.fetch``.

### `fetch_firms()`

Fetch NASA FIRMS active fire data.

```python
fetch_firms( mode: str = 'area', source: str = 'VIIRS_SNPP_NRT', area_coordinates: str = 'world', day_range: int = 1, date: str = '', sensor: str = 'ALL', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_firms()` → `Firms.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'area'` | Value passed to ``Firms.fetch``. |
| `source` | `str` | `'VIIRS_SNPP_NRT'` | Value passed to ``Firms.fetch``. |
| `area_coordinates` | `str` | `'world'` | Value passed to ``Firms.fetch``. |
| `day_range` | `int` | `1` | Value passed to ``Firms.fetch``. |
| `date` | `str` | `''` | Value passed to ``Firms.fetch``. |
| `sensor` | `str` | `'ALL'` | Value passed to ``Firms.fetch``. |
| `time` | `int` | `20` | Value passed to ``Firms.fetch``. |

**Returns:** Any: Value returned by ``Firms.fetch``.

## Geospatial

**10 functions**

| Function | Implementation |
|---|---|
| [`geocode_location()`](#geocode_location) | `GoogleMaps.geocode_location()` |
| [`geocode_coordinates()`](#geocode_coordinates) | `GoogleMaps.geocode_coordinates()` |
| [`validate_address()`](#validate_address) | `GoogleMaps.validate_address()` |
| [`request_directions()`](#request_directions) | `GoogleMaps.request_directions()` |
| [`fetch_global_imagery_wms_map()`](#fetch_global_imagery_wms_map) | `GlobalImagery.fetch_wms_map()` |
| [`fetch_global_imagery_map_services()`](#fetch_global_imagery_map_services) | `GlobalImagery.fetch_map_services()` |
| [`fetch_global_imagery_mercator_map()`](#fetch_global_imagery_mercator_map) | `GlobalImagery.fetch_mercator_map()` |
| [`fetch_google_geocoding()`](#fetch_google_geocoding) | `GoogleGeocoding.fetch()` |
| [`fetch_usgs_national_map()`](#fetch_usgs_national_map) | `USGSTheNationalMap.fetch()` |
| [`fetch_usgs_sciencebase()`](#fetch_usgs_sciencebase) | `USGSScienceBase.fetch()` |

### `geocode_location()`

Geocode location.

```python
geocode_location( address: str ) -> Any
```

**Implementation path:** `fonky.geocode_location()` → `GoogleMaps.geocode_location()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `address` | `str` | Required | Value passed to ``GoogleMaps.geocode_location``. |

**Returns:** Any: Value returned by ``GoogleMaps.geocode_location``.

### `geocode_coordinates()`

Geocode coordinates.

```python
geocode_coordinates( lat: float, long: float ) -> Any
```

**Implementation path:** `fonky.geocode_coordinates()` → `GoogleMaps.geocode_coordinates()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `lat` | `float` | Required | Value passed to ``GoogleMaps.geocode_coordinates``. |
| `long` | `float` | Required | Value passed to ``GoogleMaps.geocode_coordinates``. |

**Returns:** Any: Value returned by ``GoogleMaps.geocode_coordinates``.

### `validate_address()`

Validate address.

```python
validate_address( address: List[str] ) -> Any
```

**Implementation path:** `fonky.validate_address()` → `GoogleMaps.validate_address()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `address` | `List[str]` | Required | Value passed to ``GoogleMaps.validate_address``. |

**Returns:** Any: Value returned by ``GoogleMaps.validate_address``.

### `request_directions()`

Request directions.

```python
request_directions( origin: str, destination: str, mode: str = 'driving' ) -> Any
```

**Implementation path:** `fonky.request_directions()` → `GoogleMaps.request_directions()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `origin` | `str` | Required | Value passed to ``GoogleMaps.request_directions``. |
| `destination` | `str` | Required | Value passed to ``GoogleMaps.request_directions``. |
| `mode` | `str` | `'driving'` | Value passed to ``GoogleMaps.request_directions``. |

**Returns:** Any: Value returned by ``GoogleMaps.request_directions``.

### `fetch_global_imagery_wms_map()`

Fetch wms map.

```python
fetch_global_imagery_wms_map( layer: str, image_date: str, bbox: Tuple[float, float, float, float], width: int = 1200, height: int = 600, projection: str = 'epsg4326', quality: str = 'best', image_format: str = 'image/png', transparent: bool = True, output_dir: str = 'python-examples', output_name: str = '', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_global_imagery_wms_map()` → `GlobalImagery.fetch_wms_map()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `layer` | `str` | Required | Value passed to ``GlobalImagery.fetch_wms_map``. |
| `image_date` | `str` | Required | Value passed to ``GlobalImagery.fetch_wms_map``. |
| `bbox` | `Tuple[float, float, float, float]` | Required | Value passed to ``GlobalImagery.fetch_wms_map``. |
| `width` | `int` | `1200` | Value passed to ``GlobalImagery.fetch_wms_map``. |
| `height` | `int` | `600` | Value passed to ``GlobalImagery.fetch_wms_map``. |
| `projection` | `str` | `'epsg4326'` | Value passed to ``GlobalImagery.fetch_wms_map``. |
| `quality` | `str` | `'best'` | Value passed to ``GlobalImagery.fetch_wms_map``. |
| `image_format` | `str` | `'image/png'` | Value passed to ``GlobalImagery.fetch_wms_map``. |
| `transparent` | `bool` | `True` | Value passed to ``GlobalImagery.fetch_wms_map``. |
| `output_dir` | `str` | `'python-examples'` | Value passed to ``GlobalImagery.fetch_wms_map``. |
| `output_name` | `str` | `''` | Value passed to ``GlobalImagery.fetch_wms_map``. |
| `time` | `int` | `20` | Value passed to ``GlobalImagery.fetch_wms_map``. |

**Returns:** Any: Value returned by ``GlobalImagery.fetch_wms_map``.

### `fetch_global_imagery_map_services()`

Fetch map services.

```python
fetch_global_imagery_map_services(  ) -> Any
```

**Implementation path:** `fonky.fetch_global_imagery_map_services()` → `GlobalImagery.fetch_map_services()`

| Parameter | Type | Default | Description |
|---|---|---|---|

**Returns:** Any: Value returned by ``GlobalImagery.fetch_map_services``.

### `fetch_global_imagery_mercator_map()`

Fetch mercator map.

```python
fetch_global_imagery_mercator_map( ccrs: Any = None ) -> Any
```

**Implementation path:** `fonky.fetch_global_imagery_mercator_map()` → `GlobalImagery.fetch_mercator_map()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ccrs` | `Any` | `None` | Value passed to ``GlobalImagery.fetch_mercator_map``. |

**Returns:** Any: Value returned by ``GlobalImagery.fetch_mercator_map``.

### `fetch_google_geocoding()`

Fetch Google forward, reverse, and place geocoding.

```python
fetch_google_geocoding( mode: str = 'forward', query: str = '', latitude: float = 0.0, longitude: float = 0.0, place_id: str = '', language: str = 'en', region: str = '', result_type: str = '', location_type: str = '', time: int = 10, api_key: Optional[str] = None ) -> Any
```

**Implementation path:** `fonky.fetch_google_geocoding()` → `GoogleGeocoding.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'forward'` | Value passed to ``GoogleGeocoding.fetch``. |
| `query` | `str` | `''` | Value passed to ``GoogleGeocoding.fetch``. |
| `latitude` | `float` | `0.0` | Value passed to ``GoogleGeocoding.fetch``. |
| `longitude` | `float` | `0.0` | Value passed to ``GoogleGeocoding.fetch``. |
| `place_id` | `str` | `''` | Value passed to ``GoogleGeocoding.fetch``. |
| `language` | `str` | `'en'` | Value passed to ``GoogleGeocoding.fetch``. |
| `region` | `str` | `''` | Value passed to ``GoogleGeocoding.fetch``. |
| `result_type` | `str` | `''` | Value passed to ``GoogleGeocoding.fetch``. |
| `location_type` | `str` | `''` | Value passed to ``GoogleGeocoding.fetch``. |
| `time` | `int` | `10` | Value passed to ``GoogleGeocoding.fetch``. |
| `api_key` | `Optional[str]` | `None` | Value passed to ``GoogleGeocoding.fetch``. |

**Returns:** Any: Value returned by ``GoogleGeocoding.fetch``.

### `fetch_usgs_national_map()`

Fetch USGS National Map datasets and products.

```python
fetch_usgs_national_map( mode: str = 'products', dataset: str = '', q: str = '', bbox: str = '', prod_formats: str = '', max_items: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_usgs_national_map()` → `USGSTheNationalMap.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'products'` | Value passed to ``USGSTheNationalMap.fetch``. |
| `dataset` | `str` | `''` | Value passed to ``USGSTheNationalMap.fetch``. |
| `q` | `str` | `''` | Value passed to ``USGSTheNationalMap.fetch``. |
| `bbox` | `str` | `''` | Value passed to ``USGSTheNationalMap.fetch``. |
| `prod_formats` | `str` | `''` | Value passed to ``USGSTheNationalMap.fetch``. |
| `max_items` | `int` | `25` | Value passed to ``USGSTheNationalMap.fetch``. |
| `offset` | `int` | `0` | Value passed to ``USGSTheNationalMap.fetch``. |
| `time` | `int` | `20` | Value passed to ``USGSTheNationalMap.fetch``. |

**Returns:** Any: Value returned by ``USGSTheNationalMap.fetch``.

### `fetch_usgs_sciencebase()`

Fetch USGS ScienceBase items and catalog records.

```python
fetch_usgs_sciencebase( mode: str = 'items', q: str = '', item_id: str = '', max_items: int = 25, offset: int = 0, fields: str = '', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_usgs_sciencebase()` → `USGSScienceBase.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'items'` | Value passed to ``USGSScienceBase.fetch``. |
| `q` | `str` | `''` | Value passed to ``USGSScienceBase.fetch``. |
| `item_id` | `str` | `''` | Value passed to ``USGSScienceBase.fetch``. |
| `max_items` | `int` | `25` | Value passed to ``USGSScienceBase.fetch``. |
| `offset` | `int` | `0` | Value passed to ``USGSScienceBase.fetch``. |
| `fields` | `str` | `''` | Value passed to ``USGSScienceBase.fetch``. |
| `time` | `int` | `20` | Value passed to ``USGSScienceBase.fetch``. |

**Returns:** Any: Value returned by ``USGSScienceBase.fetch``.

## Health

**4 functions**

| Function | Implementation |
|---|---|
| [`fetch_health_data()`](#fetch_health_data) | `HealthData.fetch()` |
| [`fetch_global_health_data()`](#fetch_global_health_data) | `GlobalHealthData.fetch()` |
| [`fetch_wonder()`](#fetch_wonder) | `Wonder.fetch()` |
| [`load_pubmed()`](#load_pubmed) | `PubMedSearchLoader.load()` |

### `fetch_health_data()`

Fetch HealthData.gov Socrata metadata and rows.

```python
fetch_health_data( mode: str = 'rows', domain: str = 'healthdata.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_health_data()` → `HealthData.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'rows'` | Value passed to ``HealthData.fetch``. |
| `domain` | `str` | `'healthdata.gov'` | Value passed to ``HealthData.fetch``. |
| `dataset_id` | `str` | `''` | Value passed to ``HealthData.fetch``. |
| `select` | `str` | `''` | Value passed to ``HealthData.fetch``. |
| `where` | `str` | `''` | Value passed to ``HealthData.fetch``. |
| `order` | `str` | `''` | Value passed to ``HealthData.fetch``. |
| `group` | `str` | `''` | Value passed to ``HealthData.fetch``. |
| `limit` | `int` | `25` | Value passed to ``HealthData.fetch``. |
| `offset` | `int` | `0` | Value passed to ``HealthData.fetch``. |
| `time` | `int` | `20` | Value passed to ``HealthData.fetch``. |

**Returns:** Any: Value returned by ``HealthData.fetch``.

### `fetch_global_health_data()`

Fetch WHO global health indicator and Athena data.

```python
fetch_global_health_data( mode: str = 'indicator_registry', query_path: str = '', fmt: str = 'json', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_global_health_data()` → `GlobalHealthData.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'indicator_registry'` | Value passed to ``GlobalHealthData.fetch``. |
| `query_path` | `str` | `''` | Value passed to ``GlobalHealthData.fetch``. |
| `fmt` | `str` | `'json'` | Value passed to ``GlobalHealthData.fetch``. |
| `time` | `int` | `20` | Value passed to ``GlobalHealthData.fetch``. |

**Returns:** Any: Value returned by ``GlobalHealthData.fetch``.

### `fetch_wonder()`

Fetch CDC WONDER template and query submission.

```python
fetch_wonder( mode: str = 'metadata_template', dataset_id: str = 'D76', request_xml: str = '', time: int = 20 ) -> Any
```

**Implementation path:** `fonky.fetch_wonder()` → `Wonder.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | `str` | `'metadata_template'` | Value passed to ``Wonder.fetch``. |
| `dataset_id` | `str` | `'D76'` | Value passed to ``Wonder.fetch``. |
| `request_xml` | `str` | `''` | Value passed to ``Wonder.fetch``. |
| `time` | `int` | `20` | Value passed to ``Wonder.fetch``. |

**Returns:** Any: Value returned by ``Wonder.fetch``.

### `load_pubmed()`

Load source content.

```python
load_pubmed( query: str, max_docs: int = 5 ) -> Any
```

**Implementation path:** `fonky.load_pubmed()` → `PubMedSearchLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | `str` | Required | Value passed to ``PubMedSearchLoader.load``. |
| `max_docs` | `int` | `5` | Value passed to ``PubMedSearchLoader.load``. |

**Returns:** Any: Value returned by ``PubMedSearchLoader.load``.

## Web

**25 functions**

| Function | Implementation |
|---|---|
| [`fetch_web_page()`](#fetch_web_page) | `WebFetcher.fetch()` |
| [`convert_html_to_text()`](#convert_html_to_text) | `WebFetcher.html_to_text()` |
| [`extract_web_title()`](#extract_web_title) | `WebFetcher.extract_title()` |
| [`extract_web_links()`](#extract_web_links) | `WebFetcher.extract_links()` |
| [`extract_web_structured_data()`](#extract_web_structured_data) | `WebFetcher.extract_structured_data()` |
| [`crawl_web()`](#crawl_web) | `WebCrawler.crawl()` |
| [`scrape_crawler_page()`](#scrape_crawler_page) | `WebCrawler.scrape_page()` |
| [`render_web_page()`](#render_web_page) | `WebCrawler.render_with_playwright()` |
| [`load_web()`](#load_web) | `WebLoader.load()` |
| [`load_web_recursive()`](#load_web_recursive) | `WebLoader.load_recursive()` |
| [`load_web_pages()`](#load_web_pages) | `WebLoader.load_pages()` |
| [`load_github()`](#load_github) | `GithubLoader.load()` |
| [`scrape_web_page()`](#scrape_web_page) | `WebExtractor.scrape()` |
| [`scraper_html_to_text()`](#scraper_html_to_text) | `WebExtractor.html_to_text()` |
| [`scrape_paragraphs()`](#scrape_paragraphs) | `WebExtractor.scrape_paragraphs()` |
| [`scrape_lists()`](#scrape_lists) | `WebExtractor.scrape_lists()` |
| [`scrape_tables()`](#scrape_tables) | `WebExtractor.scrape_tables()` |
| [`scrape_articles()`](#scrape_articles) | `WebExtractor.scrape_articles()` |
| [`scrape_headings()`](#scrape_headings) | `WebExtractor.scrape_headings()` |
| [`scrape_divisions()`](#scrape_divisions) | `WebExtractor.scrape_divisions()` |
| [`scrape_sections()`](#scrape_sections) | `WebExtractor.scrape_sections()` |
| [`scrape_blockquotes()`](#scrape_blockquotes) | `WebExtractor.scrape_blockquotes()` |
| [`scrape_hyperlinks()`](#scrape_hyperlinks) | `WebExtractor.scrape_hyperlinks()` |
| [`scrape_images()`](#scrape_images) | `WebExtractor.scrape_images()` |
| [`encode_image()`](#encode_image) | `_encode_image()` |

### `fetch_web_page()`

Fetch HTTP web page retrieval and HTML extraction.

```python
fetch_web_page( url: str, time: int = 10 ) -> Any
```

**Implementation path:** `fonky.fetch_web_page()` → `WebFetcher.fetch()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | `str` | Required | Value passed to ``WebFetcher.fetch``. |
| `time` | `int` | `10` | Value passed to ``WebFetcher.fetch``. |

**Returns:** Any: Value returned by ``WebFetcher.fetch``.

### `convert_html_to_text()`

HTML to text.

```python
convert_html_to_text( html: str ) -> Any
```

**Implementation path:** `fonky.convert_html_to_text()` → `WebFetcher.html_to_text()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `html` | `str` | Required | Value passed to ``WebFetcher.html_to_text``. |

**Returns:** Any: Value returned by ``WebFetcher.html_to_text``.

### `extract_web_title()`

Extract title.

```python
extract_web_title( html: str ) -> Any
```

**Implementation path:** `fonky.extract_web_title()` → `WebFetcher.extract_title()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `html` | `str` | Required | Value passed to ``WebFetcher.extract_title``. |

**Returns:** Any: Value returned by ``WebFetcher.extract_title``.

### `extract_web_links()`

Extract links.

```python
extract_web_links( base_url: str, html: str ) -> Any
```

**Implementation path:** `fonky.extract_web_links()` → `WebFetcher.extract_links()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `base_url` | `str` | Required | Value passed to ``WebFetcher.extract_links``. |
| `html` | `str` | Required | Value passed to ``WebFetcher.extract_links``. |

**Returns:** Any: Value returned by ``WebFetcher.extract_links``.

### `extract_web_structured_data()`

Extract structured data.

```python
extract_web_structured_data( url: str, html: str, selected_methods: Optional[List[str]] = None ) -> Any
```

**Implementation path:** `fonky.extract_web_structured_data()` → `WebFetcher.extract_structured_data()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | `str` | Required | Value passed to ``WebFetcher.extract_structured_data``. |
| `html` | `str` | Required | Value passed to ``WebFetcher.extract_structured_data``. |
| `selected_methods` | `Optional[List[str]]` | `None` | Value passed to ``WebFetcher.extract_structured_data``. |

**Returns:** Any: Value returned by ``WebFetcher.extract_structured_data``.

### `crawl_web()`

Crawl.

```python
crawl_web( seed_url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, recursive: bool = False, max_depth: int = 1, max_pages: int = 10, same_domain_only: bool = True, request_timeout: int = 10, delay_seconds: float = 0.25, max_bytes: int = 1000000, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any
```

**Implementation path:** `fonky.crawl_web()` → `WebCrawler.crawl()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `seed_url` | `str` | Required | Value passed to ``WebCrawler.crawl``. |
| `include_title` | `bool` | `True` | Value passed to ``WebCrawler.crawl``. |
| `include_basic_text` | `bool` | `True` | Value passed to ``WebCrawler.crawl``. |
| `include_raw_html` | `bool` | `False` | Value passed to ``WebCrawler.crawl``. |
| `selected_methods` | `Optional[List[str]]` | `None` | Value passed to ``WebCrawler.crawl``. |
| `recursive` | `bool` | `False` | Value passed to ``WebCrawler.crawl``. |
| `max_depth` | `int` | `1` | Value passed to ``WebCrawler.crawl``. |
| `max_pages` | `int` | `10` | Value passed to ``WebCrawler.crawl``. |
| `same_domain_only` | `bool` | `True` | Value passed to ``WebCrawler.crawl``. |
| `request_timeout` | `int` | `10` | Value passed to ``WebCrawler.crawl``. |
| `delay_seconds` | `float` | `0.25` | Value passed to ``WebCrawler.crawl``. |
| `max_bytes` | `int` | `1000000` | Value passed to ``WebCrawler.crawl``. |
| `headers` | `Optional[Dict[str, str]]` | `None` | Value passed to ``WebCrawler.crawl``. |
| `use_playwright` | `bool` | `False` | Value passed to ``WebCrawler.crawl``. |

**Returns:** Any: Value returned by ``WebCrawler.crawl``.

### `scrape_crawler_page()`

Scrape page.

```python
scrape_crawler_page( url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, request_timeout: int = 10, max_bytes: int = 1000000, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any
```

**Implementation path:** `fonky.scrape_crawler_page()` → `WebCrawler.scrape_page()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | `str` | Required | Value passed to ``WebCrawler.scrape_page``. |
| `include_title` | `bool` | `True` | Value passed to ``WebCrawler.scrape_page``. |
| `include_basic_text` | `bool` | `True` | Value passed to ``WebCrawler.scrape_page``. |
| `include_raw_html` | `bool` | `False` | Value passed to ``WebCrawler.scrape_page``. |
| `selected_methods` | `Optional[List[str]]` | `None` | Value passed to ``WebCrawler.scrape_page``. |
| `request_timeout` | `int` | `10` | Value passed to ``WebCrawler.scrape_page``. |
| `max_bytes` | `int` | `1000000` | Value passed to ``WebCrawler.scrape_page``. |
| `headers` | `Optional[Dict[str, str]]` | `None` | Value passed to ``WebCrawler.scrape_page``. |
| `use_playwright` | `bool` | `False` | Value passed to ``WebCrawler.scrape_page``. |

**Returns:** Any: Value returned by ``WebCrawler.scrape_page``.

### `render_web_page()`

Render with playwright.

```python
render_web_page( url: str, timeout: int = 15, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any
```

**Implementation path:** `fonky.render_web_page()` → `WebCrawler.render_with_playwright()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | `str` | Required | Value passed to ``WebCrawler.render_with_playwright``. |
| `timeout` | `int` | `15` | Value passed to ``WebCrawler.render_with_playwright``. |
| `headers` | `Optional[Dict[str, str]]` | `None` | Value passed to ``WebCrawler.render_with_playwright``. |
| `use_playwright` | `bool` | `False` | Value passed to ``WebCrawler.render_with_playwright``. |

**Returns:** Any: Value returned by ``WebCrawler.render_with_playwright``.

### `load_web()`

Load source content.

```python
load_web( urls: str | List[str], recursive: bool = False, max_depth: int = 2, prevent_outside: bool = True, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> Any
```

**Implementation path:** `fonky.load_web()` → `WebLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `urls` | `str | List[str]` | Required | Value passed to ``WebLoader.load``. |
| `recursive` | `bool` | `False` | Value passed to ``WebLoader.load``. |
| `max_depth` | `int` | `2` | Value passed to ``WebLoader.load``. |
| `prevent_outside` | `bool` | `True` | Value passed to ``WebLoader.load``. |
| `timeout` | `int` | `10` | Value passed to ``WebLoader.load``. |
| `ignore` | `bool` | `True` | Value passed to ``WebLoader.load``. |
| `progress` | `bool` | `True` | Value passed to ``WebLoader.load``. |

**Returns:** Any: Value returned by ``WebLoader.load``.

### `load_web_recursive()`

Load web documents recursively.

```python
load_web_recursive( url: str, depth: int = 2, max_time: int = 10, ignore: bool = True ) -> Any
```

**Implementation path:** `fonky.load_web_recursive()` → `WebLoader.load_recursive()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | `str` | Required | Value passed to ``WebLoader.load_recursive``. |
| `depth` | `int` | `2` | Value passed to ``WebLoader.load_recursive``. |
| `max_time` | `int` | `10` | Value passed to ``WebLoader.load_recursive``. |
| `ignore` | `bool` | `True` | Value passed to ``WebLoader.load_recursive``. |

**Returns:** Any: Value returned by ``WebLoader.load_recursive``.

### `load_web_pages()`

Load static web pages.

```python
load_web_pages( urls: List[str], depth: int = 2, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> Any
```

**Implementation path:** `fonky.load_web_pages()` → `WebLoader.load_pages()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `urls` | `List[str]` | Required | Value passed to ``WebLoader.load_pages``. |
| `depth` | `int` | `2` | Value passed to ``WebLoader.load_pages``. |
| `timeout` | `int` | `10` | Value passed to ``WebLoader.load_pages``. |
| `ignore` | `bool` | `True` | Value passed to ``WebLoader.load_pages``. |
| `progress` | `bool` | `True` | Value passed to ``WebLoader.load_pages``. |

**Returns:** Any: Value returned by ``WebLoader.load_pages``.

### `load_github()`

Load source content.

```python
load_github( url: str, repo: str, branch: str, filetype: str = '.md' ) -> Any
```

**Implementation path:** `fonky.load_github()` → `GithubLoader.load()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | `str` | Required | Value passed to ``GithubLoader.load``. |
| `repo` | `str` | Required | Value passed to ``GithubLoader.load``. |
| `branch` | `str` | Required | Value passed to ``GithubLoader.load``. |
| `filetype` | `str` | `'.md'` | Value passed to ``GithubLoader.load``. |

**Returns:** Any: Value returned by ``GithubLoader.load``.

### `scrape_web_page()`

Fetch a web page.

```python
scrape_web_page( url: str, time: int = 10 ) -> Any
```

**Implementation path:** `fonky.scrape_web_page()` → `WebExtractor.scrape()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | `str` | Required | Value passed to ``WebExtractor.scrape``. |
| `time` | `int` | `10` | Value passed to ``WebExtractor.scrape``. |

**Returns:** Any: Value returned by ``WebExtractor.scrape``.

### `scraper_html_to_text()`

Convert HTML to plain text.

```python
scraper_html_to_text( html: str ) -> Any
```

**Implementation path:** `fonky.scraper_html_to_text()` → `WebExtractor.html_to_text()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `html` | `str` | Required | Value passed to ``WebExtractor.html_to_text``. |

**Returns:** Any: Value returned by ``WebExtractor.html_to_text``.

### `scrape_paragraphs()`

Extract paragraph text.

```python
scrape_paragraphs( uri: str ) -> Any
```

**Implementation path:** `fonky.scrape_paragraphs()` → `WebExtractor.scrape_paragraphs()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_paragraphs``. |

**Returns:** Any: Value returned by ``WebExtractor.scrape_paragraphs``.

### `scrape_lists()`

Extract list item text.

```python
scrape_lists( uri: str ) -> Any
```

**Implementation path:** `fonky.scrape_lists()` → `WebExtractor.scrape_lists()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_lists``. |

**Returns:** Any: Value returned by ``WebExtractor.scrape_lists``.

### `scrape_tables()`

Extract table cell text.

```python
scrape_tables( uri: str ) -> Any
```

**Implementation path:** `fonky.scrape_tables()` → `WebExtractor.scrape_tables()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_tables``. |

**Returns:** Any: Value returned by ``WebExtractor.scrape_tables``.

### `scrape_articles()`

Extract article text.

```python
scrape_articles( uri: str ) -> Any
```

**Implementation path:** `fonky.scrape_articles()` → `WebExtractor.scrape_articles()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_articles``. |

**Returns:** Any: Value returned by ``WebExtractor.scrape_articles``.

### `scrape_headings()`

Extract heading text.

```python
scrape_headings( uri: str ) -> Any
```

**Implementation path:** `fonky.scrape_headings()` → `WebExtractor.scrape_headings()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_headings``. |

**Returns:** Any: Value returned by ``WebExtractor.scrape_headings``.

### `scrape_divisions()`

Extract division text.

```python
scrape_divisions( uri: str ) -> Any
```

**Implementation path:** `fonky.scrape_divisions()` → `WebExtractor.scrape_divisions()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_divisions``. |

**Returns:** Any: Value returned by ``WebExtractor.scrape_divisions``.

### `scrape_sections()`

Extract section text.

```python
scrape_sections( uri: str ) -> Any
```

**Implementation path:** `fonky.scrape_sections()` → `WebExtractor.scrape_sections()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_sections``. |

**Returns:** Any: Value returned by ``WebExtractor.scrape_sections``.

### `scrape_blockquotes()`

Extract blockquote text.

```python
scrape_blockquotes( uri: str ) -> Any
```

**Implementation path:** `fonky.scrape_blockquotes()` → `WebExtractor.scrape_blockquotes()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_blockquotes``. |

**Returns:** Any: Value returned by ``WebExtractor.scrape_blockquotes``.

### `scrape_hyperlinks()`

Extract hyperlinks.

```python
scrape_hyperlinks( uri: str ) -> Any
```

**Implementation path:** `fonky.scrape_hyperlinks()` → `WebExtractor.scrape_hyperlinks()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_hyperlinks``. |

**Returns:** Any: Value returned by ``WebExtractor.scrape_hyperlinks``.

### `scrape_images()`

Extract image references.

```python
scrape_images( uri: str ) -> Any
```

**Implementation path:** `fonky.scrape_images()` → `WebExtractor.scrape_images()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_images``. |

**Returns:** Any: Value returned by ``WebExtractor.scrape_images``.

### `encode_image()`

Encode an image as Base64 text.

```python
encode_image( path: str ) -> str
```

**Implementation path:** `fonky.encode_image()` → `_encode_image()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str` | Required | Local image path to encode. |

**Returns:** str: Base64-encoded image data.
