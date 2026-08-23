# Functional API — `fonky.py`

The functional module exposes **110** public operations. This section is reference material; use the User Guide for workflows.

## Archives

| Function | Purpose | Implementation |
|---|---|---|
| [`fetch_arxiv()`](#fetch_arxiv) | Fetch ArXiv research document retrieval. Provides direct module-level access to ``ArXiv.fetch`` using a fresh ``ArXiv`` instance. Any: Value returned by ``ArXiv.fetch``. | `ArXiv.fetch()` |
| [`fetch_google_drive()`](#fetch_google_drive) | Fetch Google Drive document retrieval. Provides direct module-level access to ``GoogleDrive.fetch`` using a fresh ``GoogleDrive`` instance. Any: Value returned by ``GoogleDrive.fetch``. | `GoogleDrive.fetch()` |
| [`fetch_wikipedia()`](#fetch_wikipedia) | Fetch Wikipedia document retrieval. Provides direct module-level access to ``Wikipedia.fetch`` using a fresh ``Wikipedia`` instance. Any: Value returned by ``Wikipedia.fetch``. | `Wikipedia.fetch()` |
| [`fetch_news()`](#fetch_news) | Fetch The News API article retrieval. Provides direct module-level access to ``TheNews.fetch`` using a fresh ``TheNews`` instance. Any: Value returned by ``TheNews.fetch``. | `TheNews.fetch()` |
| [`fetch_google_search()`](#fetch_google_search) | Fetch Google Custom Search retrieval. Provides direct module-level access to ``GoogleSearch.fetch`` using a fresh ``GoogleSearch`` instance. Any: Value returned by ``GoogleSearch.fetch``. | `GoogleSearch.fetch()` |
| [`fetch_gov_data()`](#fetch_gov_data) | Fetch Data.gov package and collection retrieval. Provides direct module-level access to ``GovData.fetch`` using a fresh ``GovData`` instance. Any: Value returned by ``GovData.fetch``. | `GovData.fetch()` |
| [`fetch_congress()`](#fetch_congress) | Fetch Congress.gov legislative data retrieval. Provides direct module-level access to ``Congress.fetch`` using a fresh ``Congress`` instance. Any: Value returned by ``Congress.fetch``. | `Congress.fetch()` |
| [`fetch_internet_archive()`](#fetch_internet_archive) | Fetch Internet Archive search and metadata retrieval. Provides direct module-level access to ``InternetArchive.fetch`` using a fresh ``InternetArchive`` instance. Any: Value returned by ``InternetArchive.fetch``. | `InternetArchive.fetch()` |
| [`fetch_grokipedia()`](#fetch_grokipedia) | Fetch Grokipedia search and page retrieval. Provides direct module-level access to ``Grokipedia.fetch`` using a fresh ``Grokipedia`` instance. Any: Value returned by ``Grokipedia.fetch``. | `Grokipedia.fetch()` |
| [`load_arxiv()`](#load_arxiv) | Load source content. Provides direct module-level access to ``ArXivLoader.load`` using a fresh ``ArXivLoader`` instance. Any: Value returned by ``ArXivLoader.load``. | `ArXivLoader.load()` |
| [`load_wikipedia()`](#load_wikipedia) | Load source content. Provides direct module-level access to ``WikiLoader.load`` using a fresh ``WikiLoader`` instance. Any: Value returned by ``WikiLoader.load``. | `WikiLoader.load()` |

### `fetch_arxiv()`

Fetch ArXiv research document retrieval. Provides direct module-level access to ``ArXiv.fetch`` using a fresh ``ArXiv`` instance. Any: Value returned by ``ArXiv.fetch``.

```python
fetch_arxiv( question: str, max_documents: int = None, full_documents: bool = None, include_metadata: bool = None ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `question` | `str` | Required | Value passed to ``ArXiv.fetch``. |
| `max_documents` | `int` | `None` | Value passed to ``ArXiv.fetch``. |
| `full_documents` | `bool` | `None` | Value passed to ``ArXiv.fetch``. |
| `include_metadata` | `bool` | `None` | Value passed to ``ArXiv.fetch``. |

### `fetch_google_drive()`

Fetch Google Drive document retrieval. Provides direct module-level access to ``GoogleDrive.fetch`` using a fresh ``GoogleDrive`` instance. Any: Value returned by ``GoogleDrive.fetch``.

```python
fetch_google_drive( question: str, folder_id: str = 'root', results: int = 10, template: str = 'gdrive-query', mime_type: str = None, mode: str = 'documents' ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `question` | `str` | Required | Value passed to ``GoogleDrive.fetch``. |
| `folder_id` | `str` | `'root'` | Value passed to ``GoogleDrive.fetch``. |
| `results` | `int` | `10` | Value passed to ``GoogleDrive.fetch``. |
| `template` | `str` | `'gdrive-query'` | Value passed to ``GoogleDrive.fetch``. |
| `mime_type` | `str` | `None` | Value passed to ``GoogleDrive.fetch``. |
| `mode` | `str` | `'documents'` | Value passed to ``GoogleDrive.fetch``. |

### `fetch_wikipedia()`

Fetch Wikipedia document retrieval. Provides direct module-level access to ``Wikipedia.fetch`` using a fresh ``Wikipedia`` instance. Any: Value returned by ``Wikipedia.fetch``.

```python
fetch_wikipedia( question: str, language: str = None, max_documents: int = None, include_metadata: bool = None ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `question` | `str` | Required | Value passed to ``Wikipedia.fetch``. |
| `language` | `str` | `None` | Value passed to ``Wikipedia.fetch``. |
| `max_documents` | `int` | `None` | Value passed to ``Wikipedia.fetch``. |
| `include_metadata` | `bool` | `None` | Value passed to ``Wikipedia.fetch``. |

### `fetch_news()`

Fetch The News API article retrieval. Provides direct module-level access to ``TheNews.fetch`` using a fresh ``TheNews`` instance. Any: Value returned by ``TheNews.fetch``.

```python
fetch_news( endpoint: str = 'all', query: str = '', language: str = 'en', categories: str = '', exclude_categories: str = '', locale: str = '', domains: str = '', exclude_domains: str = '', source_ids: str = '', exclude_source_ids: str = '', published_after: str = '', published_before: str = '', published_on: str = '', sort: str = 'published_at', limit: int = 10, page: int = 1, include_similar: bool = True, headlines_per_category: int = 6, time: int = 10, api_key: str = None ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_google_search()`

Fetch Google Custom Search retrieval. Provides direct module-level access to ``GoogleSearch.fetch`` using a fresh ``GoogleSearch`` instance. Any: Value returned by ``GoogleSearch.fetch``.

```python
fetch_google_search( keywords: str, results: int = 10, start: int = 1, exact_terms: str = '', exclude_terms: str = '', file_type: str = '', date_restrict: str = '', gl: str = '', lr: str = '', safe: str = 'off', search_type: str = '', site_search: str = '', site_search_filter: str = '', sort: str = '', img_size: str = '', img_type: str = '', img_color_type: str = '', img_dominant_color: str = '', time: int = 10, api_key: str = None, cse_id: str = None ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_gov_data()`

Fetch Data.gov package and collection retrieval. Provides direct module-level access to ``GovData.fetch`` using a fresh ``GovData`` instance. Any: Value returned by ``GovData.fetch``.

```python
fetch_gov_data( mode: str = 'search', query: str = '', page_size: int = 10, offset_mark: str = '*', sort_field: str = 'score', sort_order: str = 'DESC', package_id: str = '', collection: str = '', start_date: str = '', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_congress()`

Fetch Congress.gov legislative data retrieval. Provides direct module-level access to ``Congress.fetch`` using a fresh ``Congress`` instance. Any: Value returned by ``Congress.fetch``.

```python
fetch_congress( mode: str = 'congresses', congress: int = 0, bill_type: str = '', bill_number: int = 0, law_type: str = '', law_number: int = 0, report_type: str = '', report_number: int = 0, offset: int = 0, limit: int = 20, sort: str = 'updateDate+desc', from_date_time: str = '', to_date_time: str = '', conference: bool = False, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_internet_archive()`

Fetch Internet Archive search and metadata retrieval. Provides direct module-level access to ``InternetArchive.fetch`` using a fresh ``InternetArchive`` instance. Any: Value returned by ``InternetArchive.fetch``.

```python
fetch_internet_archive( keywords: str, fields: List[str] | None = None, rows: int = 10, page: int = 1, sort: str = 'downloads desc', media_type: str = '', collection: str = '', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `keywords` | `str` | Required | Value passed to ``InternetArchive.fetch``. |
| `fields` | `List[str] | None` | `None` | Value passed to ``InternetArchive.fetch``. |
| `rows` | `int` | `10` | Value passed to ``InternetArchive.fetch``. |
| `page` | `int` | `1` | Value passed to ``InternetArchive.fetch``. |
| `sort` | `str` | `'downloads desc'` | Value passed to ``InternetArchive.fetch``. |
| `media_type` | `str` | `''` | Value passed to ``InternetArchive.fetch``. |
| `collection` | `str` | `''` | Value passed to ``InternetArchive.fetch``. |
| `time` | `int` | `20` | Value passed to ``InternetArchive.fetch``. |

### `fetch_grokipedia()`

Fetch Grokipedia search and page retrieval. Provides direct module-level access to ``Grokipedia.fetch`` using a fresh ``Grokipedia`` instance. Any: Value returned by ``Grokipedia.fetch``.

```python
fetch_grokipedia( mode: str = 'search', query: str = '', page: str = '', limit: int = 12, offset: int = 0, include_content: bool = True ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'search'` | Value passed to ``Grokipedia.fetch``. |
| `query` | `str` | `''` | Value passed to ``Grokipedia.fetch``. |
| `page` | `str` | `''` | Value passed to ``Grokipedia.fetch``. |
| `limit` | `int` | `12` | Value passed to ``Grokipedia.fetch``. |
| `offset` | `int` | `0` | Value passed to ``Grokipedia.fetch``. |
| `include_content` | `bool` | `True` | Value passed to ``Grokipedia.fetch``. |

### `load_arxiv()`

Load source content. Provides direct module-level access to ``ArXivLoader.load`` using a fresh ``ArXivLoader`` instance. Any: Value returned by ``ArXivLoader.load``.

```python
load_arxiv( question: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `question` | `str` | Required | Value passed to ``ArXivLoader.load``. |

### `load_wikipedia()`

Load source content. Provides direct module-level access to ``WikiLoader.load`` using a fresh ``WikiLoader`` instance. Any: Value returned by ``WikiLoader.load``.

```python
load_wikipedia( question: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `question` | `str` | Required | Value passed to ``WikiLoader.load``. |

## Astronomical

| Function | Purpose | Implementation |
|---|---|---|
| [`fetch_naval_observatory()`](#fetch_naval_observatory) | Fetch U.S. Naval Observatory celestial-navigation data. Provides direct module-level access to ``NavalObservatory.fetch`` using a fresh ``NavalObservatory`` instance. Any: Value returned by ``NavalObservatory.fetch``. | `NavalObservatory.fetch()` |
| [`fetch_satellite_center()`](#fetch_satellite_center) | Fetch SSC satellite observatory, ground-station, and location data. Provides direct module-level access to ``SatelliteCenter.fetch`` using a fresh ``SatelliteCenter`` instance. Any: Value returned by ``SatelliteCenter.fetch``. | `SatelliteCenter.fetch()` |
| [`fetch_nearby_objects()`](#fetch_nearby_objects) | Fetch JPL SSD and CNEOS near-Earth object data. Provides direct module-level access to ``NearbyObjects.fetch`` using a fresh ``NearbyObjects`` instance. Any: Value returned by ``NearbyObjects.fetch``. | `NearbyObjects.fetch()` |
| [`fetch_open_science()`](#fetch_open_science) | Fetch NASA Open Science Data Repository resources. Provides direct module-level access to ``OpenScience.fetch`` using a fresh ``OpenScience`` instance. Any: Value returned by ``OpenScience.fetch``. | `OpenScience.fetch()` |
| [`fetch_space_weather()`](#fetch_space_weather) | Fetch NASA DONKI space weather endpoints. Provides direct module-level access to ``SpaceWeather.fetch`` using a fresh ``SpaceWeather`` instance. Any: Value returned by ``SpaceWeather.fetch``. | `SpaceWeather.fetch()` |
| [`fetch_astro_catalog()`](#fetch_astro_catalog) | Fetch Open Astronomy Catalog queries. Provides direct module-level access to ``AstroCatalog.fetch`` using a fresh ``AstroCatalog`` instance. Any: Value returned by ``AstroCatalog.fetch``. | `AstroCatalog.fetch()` |
| [`fetch_astro_query()`](#fetch_astro_query) | Fetch Simbad and astronomy object search operations. Provides direct module-level access to ``AstroQuery.fetch`` using a fresh ``AstroQuery`` instance. Any: Value returned by ``AstroQuery.fetch``. | `AstroQuery.fetch()` |
| [`fetch_star_map()`](#fetch_star_map) | Fetch astronomical object map links and imagery. Provides direct module-level access to ``StarMap.fetch`` using a fresh ``StarMap`` instance. Any: Value returned by ``StarMap.fetch``. | `StarMap.fetch()` |
| [`fetch_star_chart()`](#fetch_star_chart) | Fetch static star chart and coordinate chart generation. Provides direct module-level access to ``StarChart.fetch`` using a fresh ``StarChart`` instance. Any: Value returned by ``StarChart.fetch``. | `StarChart.fetch()` |
| [`fetch_open_sky()`](#fetch_open_sky) | Fetch OpenSky Network aircraft, airport, and state-vector data. Provides direct module-level access to ``OpenSky.fetch`` using a fresh ``OpenSky`` instance. Any: Value returned by ``OpenSky.fetch``. | `OpenSky.fetch()` |

### `fetch_naval_observatory()`

Fetch U.S. Naval Observatory celestial-navigation data. Provides direct module-level access to ``NavalObservatory.fetch`` using a fresh ``NavalObservatory`` instance. Any: Value returned by ``NavalObservatory.fetch``.

```python
fetch_naval_observatory( mode: str = 'celnav', date_value: str = '', time_value: str = '', latitude: float = 0.0, longitude: float = 0.0, location_label: str = '', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'celnav'` | Value passed to ``NavalObservatory.fetch``. |
| `date_value` | `str` | `''` | Value passed to ``NavalObservatory.fetch``. |
| `time_value` | `str` | `''` | Value passed to ``NavalObservatory.fetch``. |
| `latitude` | `float` | `0.0` | Value passed to ``NavalObservatory.fetch``. |
| `longitude` | `float` | `0.0` | Value passed to ``NavalObservatory.fetch``. |
| `location_label` | `str` | `''` | Value passed to ``NavalObservatory.fetch``. |
| `time` | `int` | `20` | Value passed to ``NavalObservatory.fetch``. |

### `fetch_satellite_center()`

Fetch SSC satellite observatory, ground-station, and location data. Provides direct module-level access to ``SatelliteCenter.fetch`` using a fresh ``SatelliteCenter`` instance. Any: Value returned by ``SatelliteCenter.fetch``.

```python
fetch_satellite_center( mode: str = 'observatories', query: str = '', start_time: str = '', end_time: str = '', coordinate_systems: str = 'gse', resolution_factor: int = 1, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'observatories'` | Value passed to ``SatelliteCenter.fetch``. |
| `query` | `str` | `''` | Value passed to ``SatelliteCenter.fetch``. |
| `start_time` | `str` | `''` | Value passed to ``SatelliteCenter.fetch``. |
| `end_time` | `str` | `''` | Value passed to ``SatelliteCenter.fetch``. |
| `coordinate_systems` | `str` | `'gse'` | Value passed to ``SatelliteCenter.fetch``. |
| `resolution_factor` | `int` | `1` | Value passed to ``SatelliteCenter.fetch``. |
| `time` | `int` | `20` | Value passed to ``SatelliteCenter.fetch``. |

### `fetch_nearby_objects()`

Fetch JPL SSD and CNEOS near-Earth object data. Provides direct module-level access to ``NearbyObjects.fetch`` using a fresh ``NearbyObjects`` instance. Any: Value returned by ``NearbyObjects.fetch``.

```python
fetch_nearby_objects( mode: str = 'close_approaches', start_date: str = '', end_date: str = '', query: str = '', query_type: str = 'sstr', dist_max: str = '10LD', body: str = 'Earth', sort: str = 'date', limit: int = 20, dv: float = 6.0, dur: int = 360, stay: int = 8, launch: str = '2020-2045', h: float = 26.0, occ: int = 7, include_physical: bool = True, include_close_approaches: bool = True, ca_body: str = 'Earth', include_discovery: bool = True, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_open_science()`

Fetch NASA Open Science Data Repository resources. Provides direct module-level access to ``OpenScience.fetch`` using a fresh ``OpenScience`` instance. Any: Value returned by ``OpenScience.fetch``.

```python
fetch_open_science( mode: str = 'dataset', query: str = '', accession: str = '', format_value: str = 'json', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'dataset'` | Value passed to ``OpenScience.fetch``. |
| `query` | `str` | `''` | Value passed to ``OpenScience.fetch``. |
| `accession` | `str` | `''` | Value passed to ``OpenScience.fetch``. |
| `format_value` | `str` | `'json'` | Value passed to ``OpenScience.fetch``. |
| `time` | `int` | `20` | Value passed to ``OpenScience.fetch``. |

### `fetch_space_weather()`

Fetch NASA DONKI space weather endpoints. Provides direct module-level access to ``SpaceWeather.fetch`` using a fresh ``SpaceWeather`` instance. Any: Value returned by ``SpaceWeather.fetch``.

```python
fetch_space_weather( mode: str = 'cme', start_date: str = '', end_date: str = '', time: int = 20, location: str = 'ALL', catalog: str = 'ALL', notification_type: str = 'all', most_accurate_only: bool = True, complete_entry_only: bool = True, speed: int = 0, half_angle: int = 0, keyword: str = '', api_key: str = None ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_astro_catalog()`

Fetch Open Astronomy Catalog queries. Provides direct module-level access to ``AstroCatalog.fetch`` using a fresh ``AstroCatalog`` instance. Any: Value returned by ``AstroCatalog.fetch``.

```python
fetch_astro_catalog( mode: str = 'object_query', query: str = '', quantity: str = '', attributes: str = '', arguments: str = '', ra: str = '', dec: str = '', radius: int = 2, data_format: str = 'json', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_astro_query()`

Fetch Simbad and astronomy object search operations. Provides direct module-level access to ``AstroQuery.fetch`` using a fresh ``AstroQuery`` instance. Any: Value returned by ``AstroQuery.fetch``.

```python
fetch_astro_query( mode: str = 'object_search', query: str = '', ra: str = '', dec: str = '', radius: float = 0.5, radius_unit: str = 'deg', row_limit: int = 100 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'object_search'` | Value passed to ``AstroQuery.fetch``. |
| `query` | `str` | `''` | Value passed to ``AstroQuery.fetch``. |
| `ra` | `str` | `''` | Value passed to ``AstroQuery.fetch``. |
| `dec` | `str` | `''` | Value passed to ``AstroQuery.fetch``. |
| `radius` | `float` | `0.5` | Value passed to ``AstroQuery.fetch``. |
| `radius_unit` | `str` | `'deg'` | Value passed to ``AstroQuery.fetch``. |
| `row_limit` | `int` | `100` | Value passed to ``AstroQuery.fetch``. |

### `fetch_star_map()`

Fetch astronomical object map links and imagery. Provides direct module-level access to ``StarMap.fetch`` using a fresh ``StarMap`` instance. Any: Value returned by ``StarMap.fetch``.

```python
fetch_star_map( mode: str = 'object_link', query: str = '', ra: float = 0.0, dec: float = 0.0, zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_star_chart()`

Fetch static star chart and coordinate chart generation. Provides direct module-level access to ``StarChart.fetch`` using a fresh ``StarChart`` instance. Any: Value returned by ``StarChart.fetch``.

```python
fetch_star_chart( mode: str = 'object_chart', query: str = '', ra: float = 0.0, dec: float = 0.0, zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, width: int = 900, height: int = 450, magnitude: float = 7.5, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_open_sky()`

Fetch OpenSky Network aircraft, airport, and state-vector data. Provides direct module-level access to ``OpenSky.fetch`` using a fresh ``OpenSky`` instance. Any: Value returned by ``OpenSky.fetch``.

```python
fetch_open_sky( mode: str = 'states_bbox', icao24: str = '', airport: str = '', begin: int = None, end: int = None, time_value: int = None, lamin: float | None = None, lomin: float | None = None, lamax: float | None = None, lomax: float | None = None, extended: bool = False, client_id: str = None, client_secret: str = None, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

## Cloud

| Function | Purpose | Implementation |
|---|---|---|
| [`load_google_drive_file()`](#load_google_drive_file) | Load a provider file. Provides direct module-level access to ``GoogleDriveLoader.load_file`` using a fresh ``GoogleDriveLoader`` instance. Any: Value returned by ``GoogleDriveLoader.load_file``. | `GoogleDriveLoader.load_file()` |
| [`load_google_drive_folder()`](#load_google_drive_folder) | Load provider folder content. Provides direct module-level access to ``GoogleDriveLoader.load_folder`` using a fresh ``GoogleDriveLoader`` instance. Any: Value returned by ``GoogleDriveLoader.load_folder``. | `GoogleDriveLoader.load_folder()` |
| [`load_onedrive()`](#load_onedrive) | Load source content. Provides direct module-level access to ``OneDriveDocLoader.load`` using a fresh ``OneDriveDocLoader`` instance. Any: Value returned by ``OneDriveDocLoader.load``. | `OneDriveDocLoader.load()` |
| [`load_google_cloud_file()`](#load_google_cloud_file) | Load source content. Provides direct module-level access to ``GoogleCloudFileLoader.load`` using a fresh ``GoogleCloudFileLoader`` instance. Any: Value returned by ``GoogleCloudFileLoader.load``. | `GoogleCloudFileLoader.load()` |
| [`load_aws_file()`](#load_aws_file) | Load source content. Provides direct module-level access to ``AwsFileLoader.load`` using a fresh ``AwsFileLoader`` instance. Any: Value returned by ``AwsFileLoader.load``. | `AwsFileLoader.load()` |
| [`load_google_speech_to_text()`](#load_google_speech_to_text) | Load source content. Provides direct module-level access to ``GoogleSpeechToTextLoader.load`` using a fresh ``GoogleSpeechToTextLoader`` instance. Any: Value returned by ``GoogleSpeechToTextLoader.load``. | `GoogleSpeechToTextLoader.load()` |
| [`load_google_bucket()`](#load_google_bucket) | Load source content. Provides direct module-level access to ``GoogleBucketLoader.load`` using a fresh ``GoogleBucketLoader`` instance. Any: Value returned by ``GoogleBucketLoader.load``. | `GoogleBucketLoader.load()` |
| [`load_aws_bucket()`](#load_aws_bucket) | Load source content. Provides direct module-level access to ``AwsBucketLoader.load`` using a fresh ``AwsBucketLoader`` instance. Any: Value returned by ``AwsBucketLoader.load``. | `AwsBucketLoader.load()` |

### `load_google_drive_file()`

Load a provider file. Provides direct module-level access to ``GoogleDriveLoader.load_file`` using a fresh ``GoogleDriveLoader`` instance. Any: Value returned by ``GoogleDriveLoader.load_file``.

```python
load_google_drive_file( file_id: str, recursive: bool = False ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `file_id` | `str` | Required | Value passed to ``GoogleDriveLoader.load_file``. |
| `recursive` | `bool` | `False` | Value passed to ``GoogleDriveLoader.load_file``. |

### `load_google_drive_folder()`

Load provider folder content. Provides direct module-level access to ``GoogleDriveLoader.load_folder`` using a fresh ``GoogleDriveLoader`` instance. Any: Value returned by ``GoogleDriveLoader.load_folder``.

```python
load_google_drive_folder( folder_id: str, recursive: bool = False ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `folder_id` | `str` | Required | Value passed to ``GoogleDriveLoader.load_folder``. |
| `recursive` | `bool` | `False` | Value passed to ``GoogleDriveLoader.load_folder``. |

### `load_onedrive()`

Load source content. Provides direct module-level access to ``OneDriveDocLoader.load`` using a fresh ``OneDriveDocLoader`` instance. Any: Value returned by ``OneDriveDocLoader.load``.

```python
load_onedrive( drive_id: str, folder_path: Optional[str] = None, object_ids: Optional[List[str]] = None, auth_with_token: bool = True ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `drive_id` | `str` | Required | Value passed to ``OneDriveDocLoader.load``. |
| `folder_path` | `Optional[str]` | `None` | Value passed to ``OneDriveDocLoader.load``. |
| `object_ids` | `Optional[List[str]]` | `None` | Value passed to ``OneDriveDocLoader.load``. |
| `auth_with_token` | `bool` | `True` | Value passed to ``OneDriveDocLoader.load``. |

### `load_google_cloud_file()`

Load source content. Provides direct module-level access to ``GoogleCloudFileLoader.load`` using a fresh ``GoogleCloudFileLoader`` instance. Any: Value returned by ``GoogleCloudFileLoader.load``.

```python
load_google_cloud_file( project_name: str, bucket: str, blob: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `project_name` | `str` | Required | Value passed to ``GoogleCloudFileLoader.load``. |
| `bucket` | `str` | Required | Value passed to ``GoogleCloudFileLoader.load``. |
| `blob` | `str` | Required | Value passed to ``GoogleCloudFileLoader.load``. |

### `load_aws_file()`

Load source content. Provides direct module-level access to ``AwsFileLoader.load`` using a fresh ``AwsFileLoader`` instance. Any: Value returned by ``AwsFileLoader.load``.

```python
load_aws_file( bucket: str, key: str, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `bucket` | `str` | Required | Value passed to ``AwsFileLoader.load``. |
| `key` | `str` | Required | Value passed to ``AwsFileLoader.load``. |
| `aws_access_key_id` | `Optional[str]` | `None` | Value passed to ``AwsFileLoader.load``. |
| `aws_secret_access_key` | `Optional[str]` | `None` | Value passed to ``AwsFileLoader.load``. |
| `aws_session_token` | `Optional[str]` | `None` | Value passed to ``AwsFileLoader.load``. |
| `region_name` | `Optional[str]` | `None` | Value passed to ``AwsFileLoader.load``. |

### `load_google_speech_to_text()`

Load source content. Provides direct module-level access to ``GoogleSpeechToTextLoader.load`` using a fresh ``GoogleSpeechToTextLoader`` instance. Any: Value returned by ``GoogleSpeechToTextLoader.load``.

```python
load_google_speech_to_text( project_id: str, file_path: str, config: Optional[Dict[str, Any]] = None ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `project_id` | `str` | Required | Value passed to ``GoogleSpeechToTextLoader.load``. |
| `file_path` | `str` | Required | Value passed to ``GoogleSpeechToTextLoader.load``. |
| `config` | `Optional[Dict[str, Any]]` | `None` | Value passed to ``GoogleSpeechToTextLoader.load``. |

### `load_google_bucket()`

Load source content. Provides direct module-level access to ``GoogleBucketLoader.load`` using a fresh ``GoogleBucketLoader`` instance. Any: Value returned by ``GoogleBucketLoader.load``.

```python
load_google_bucket( project_name: str, bucket: str, prefix: Optional[str] = None, continue_on_failure: bool = False ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `project_name` | `str` | Required | Value passed to ``GoogleBucketLoader.load``. |
| `bucket` | `str` | Required | Value passed to ``GoogleBucketLoader.load``. |
| `prefix` | `Optional[str]` | `None` | Value passed to ``GoogleBucketLoader.load``. |
| `continue_on_failure` | `bool` | `False` | Value passed to ``GoogleBucketLoader.load``. |

### `load_aws_bucket()`

Load source content. Provides direct module-level access to ``AwsBucketLoader.load`` using a fresh ``AwsBucketLoader`` instance. Any: Value returned by ``AwsBucketLoader.load``.

```python
load_aws_bucket( bucket: str, prefix: Optional[str] = None, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None, endpoint_url: Optional[str] = None ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `bucket` | `str` | Required | Value passed to ``AwsBucketLoader.load``. |
| `prefix` | `Optional[str]` | `None` | Value passed to ``AwsBucketLoader.load``. |
| `aws_access_key_id` | `Optional[str]` | `None` | Value passed to ``AwsBucketLoader.load``. |
| `aws_secret_access_key` | `Optional[str]` | `None` | Value passed to ``AwsBucketLoader.load``. |
| `aws_session_token` | `Optional[str]` | `None` | Value passed to ``AwsBucketLoader.load``. |
| `region_name` | `Optional[str]` | `None` | Value passed to ``AwsBucketLoader.load``. |
| `endpoint_url` | `Optional[str]` | `None` | Value passed to ``AwsBucketLoader.load``. |

## Demographic

| Function | Purpose | Implementation |
|---|---|---|
| [`fetch_census_data()`](#fetch_census_data) | Fetch U.S. Census dataset and variable retrieval. Provides direct module-level access to ``CensusData.fetch`` using a fresh ``CensusData`` instance. Any: Value returned by ``CensusData.fetch``. | `CensusData.fetch()` |
| [`fetch_socrata()`](#fetch_socrata) | Fetch Socrata dataset metadata and row retrieval. Provides direct module-level access to ``Socrata.fetch`` using a fresh ``Socrata`` instance. Any: Value returned by ``Socrata.fetch``. | `Socrata.fetch()` |
| [`fetch_united_nations()`](#fetch_united_nations) | Fetch United Nations SDMX dataset and query retrieval. Provides direct module-level access to ``UnitedNations.fetch`` using a fresh ``UnitedNations`` instance. Any: Value returned by ``UnitedNations.fetch``. | `UnitedNations.fetch()` |
| [`fetch_world_population()`](#fetch_world_population) | Fetch WorldPop catalog and raster metadata retrieval. Provides direct module-level access to ``WorldPopulation.fetch`` using a fresh ``WorldPopulation`` instance. Any: Value returned by ``WorldPopulation.fetch``. | `WorldPopulation.fetch()` |
| [`load_open_city()`](#load_open_city) | Load source content. Provides direct module-level access to ``OpenCityLoader.load`` using a fresh ``OpenCityLoader`` instance. Any: Value returned by ``OpenCityLoader.load``. | `OpenCityLoader.load()` |

### `fetch_census_data()`

Fetch U.S. Census dataset and variable retrieval. Provides direct module-level access to ``CensusData.fetch`` using a fresh ``CensusData`` instance. Any: Value returned by ``CensusData.fetch``.

```python
fetch_census_data( mode: str = 'variables', year: str = '2022', dataset: str = 'acs/acs5', fields: str = 'NAME,B01001_001E', geography_for: str = 'state:*', geography_in: str = '', predicates: str = '', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'variables'` | Value passed to ``CensusData.fetch``. |
| `year` | `str` | `'2022'` | Value passed to ``CensusData.fetch``. |
| `dataset` | `str` | `'acs/acs5'` | Value passed to ``CensusData.fetch``. |
| `fields` | `str` | `'NAME,B01001_001E'` | Value passed to ``CensusData.fetch``. |
| `geography_for` | `str` | `'state:*'` | Value passed to ``CensusData.fetch``. |
| `geography_in` | `str` | `''` | Value passed to ``CensusData.fetch``. |
| `predicates` | `str` | `''` | Value passed to ``CensusData.fetch``. |
| `time` | `int` | `20` | Value passed to ``CensusData.fetch``. |

### `fetch_socrata()`

Fetch Socrata dataset metadata and row retrieval. Provides direct module-level access to ``Socrata.fetch`` using a fresh ``Socrata`` instance. Any: Value returned by ``Socrata.fetch``.

```python
fetch_socrata( mode: str = 'rows', domain: str = 'data.cdc.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_united_nations()`

Fetch United Nations SDMX dataset and query retrieval. Provides direct module-level access to ``UnitedNations.fetch`` using a fresh ``UnitedNations`` instance. Any: Value returned by ``UnitedNations.fetch``.

```python
fetch_united_nations( mode: str = 'datasets', query_path: str = '', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'datasets'` | Value passed to ``UnitedNations.fetch``. |
| `query_path` | `str` | `''` | Value passed to ``UnitedNations.fetch``. |
| `time` | `int` | `20` | Value passed to ``UnitedNations.fetch``. |

### `fetch_world_population()`

Fetch WorldPop catalog and raster metadata retrieval. Provides direct module-level access to ``WorldPopulation.fetch`` using a fresh ``WorldPopulation`` instance. Any: Value returned by ``WorldPopulation.fetch``.

```python
fetch_world_population( mode: str = 'catalog', query: str = '', asset_path: str = '', page: int = 1, page_size: int = 25, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'catalog'` | Value passed to ``WorldPopulation.fetch``. |
| `query` | `str` | `''` | Value passed to ``WorldPopulation.fetch``. |
| `asset_path` | `str` | `''` | Value passed to ``WorldPopulation.fetch``. |
| `page` | `int` | `1` | Value passed to ``WorldPopulation.fetch``. |
| `page_size` | `int` | `25` | Value passed to ``WorldPopulation.fetch``. |
| `time` | `int` | `20` | Value passed to ``WorldPopulation.fetch``. |

### `load_open_city()`

Load source content. Provides direct module-level access to ``OpenCityLoader.load`` using a fresh ``OpenCityLoader`` instance. Any: Value returned by ``OpenCityLoader.load``.

```python
load_open_city( city_id: str, dataset_id: str, limit: int = 100 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `city_id` | `str` | Required | Value passed to ``OpenCityLoader.load``. |
| `dataset_id` | `str` | Required | Value passed to ``OpenCityLoader.load``. |
| `limit` | `int` | `100` | Value passed to ``OpenCityLoader.load``. |

## Documents

| Function | Purpose | Implementation |
|---|---|---|
| [`load_text()`](#load_text) | Load source content. Provides direct module-level access to ``TextLoader.load`` using a fresh ``TextLoader`` instance. Any: Value returned by ``TextLoader.load``. | `TextLoader.load()` |
| [`load_csv()`](#load_csv) | Load source content. Provides direct module-level access to ``CsvLoader.load`` using a fresh ``CsvLoader`` instance. Any: Value returned by ``CsvLoader.load``. | `CsvLoader.load()` |
| [`read_pdf()`](#read_pdf) | Load source content. Provides direct module-level access to ``PdfReader.load`` using a fresh ``PdfReader`` instance. Any: Value returned by ``PdfReader.load``. | `PdfReader.load()` |
| [`load_pdf()`](#load_pdf) | Load source content. Provides direct module-level access to ``PdfLoader.load`` using a fresh ``PdfLoader`` instance. Any: Value returned by ``PdfLoader.load``. | `PdfLoader.load()` |
| [`load_excel()`](#load_excel) | Load source content. Provides direct module-level access to ``ExcelLoader.load`` using a fresh ``ExcelLoader`` instance. Any: Value returned by ``ExcelLoader.load``. | `ExcelLoader.load()` |
| [`load_word()`](#load_word) | Load source content. Provides direct module-level access to ``WordLoader.load`` using a fresh ``WordLoader`` instance. Any: Value returned by ``WordLoader.load``. | `WordLoader.load()` |
| [`load_markdown()`](#load_markdown) | Load source content. Provides direct module-level access to ``MarkdownLoader.load`` using a fresh ``MarkdownLoader`` instance. Any: Value returned by ``MarkdownLoader.load``. | `MarkdownLoader.load()` |
| [`load_html()`](#load_html) | Load source content. Provides direct module-level access to ``HtmlLoader.load`` using a fresh ``HtmlLoader`` instance. Any: Value returned by ``HtmlLoader.load``. | `HtmlLoader.load()` |
| [`load_outlook()`](#load_outlook) | Load source content. Provides direct module-level access to ``OutlookLoader.load`` using a fresh ``OutlookLoader`` instance. Any: Value returned by ``OutlookLoader.load``. | `OutlookLoader.load()` |
| [`load_spfx()`](#load_spfx) | Load source content. Provides direct module-level access to ``SpfxLoader.load`` using a fresh ``SpfxLoader`` instance. Any: Value returned by ``SpfxLoader.load``. | `SpfxLoader.load()` |
| [`load_spfx_folder()`](#load_spfx_folder) | Load provider folder content. Provides direct module-level access to ``SpfxLoader.load_folder`` using a fresh ``SpfxLoader`` instance. Any: Value returned by ``SpfxLoader.load_folder``. | `SpfxLoader.load_folder()` |
| [`load_powerpoint()`](#load_powerpoint) | Load source content. Provides direct module-level access to ``PowerPointLoader.load`` using a fresh ``PowerPointLoader`` instance. Any: Value returned by ``PowerPointLoader.load``. | `PowerPointLoader.load()` |
| [`load_powerpoint_multiple()`](#load_powerpoint_multiple) | Load multiple presentation elements. Provides direct module-level access to ``PowerPointLoader.load_multiple`` using a fresh ``PowerPointLoader`` instance. Any: Value returned by ``PowerPointLoader.load_multiple``. | `PowerPointLoader.load_multiple()` |
| [`load_email()`](#load_email) | Load source content. Provides direct module-level access to ``EmailLoader.load`` using a fresh ``EmailLoader`` instance. Any: Value returned by ``EmailLoader.load``. | `EmailLoader.load()` |
| [`load_json()`](#load_json) | Load source content. Provides direct module-level access to ``JsonLoader.load`` using a fresh ``JsonLoader`` instance. Any: Value returned by ``JsonLoader.load``. | `JsonLoader.load()` |
| [`load_xml()`](#load_xml) | Load source content. Provides direct module-level access to ``XmlLoader.load`` using a fresh ``XmlLoader`` instance. Any: Value returned by ``XmlLoader.load``. | `XmlLoader.load()` |
| [`load_xml_tree()`](#load_xml_tree) | Parse an XML element tree. Provides direct module-level access to ``XmlLoader.load_tree`` using a fresh ``XmlLoader`` instance. Any: Value returned by ``XmlLoader.load_tree``. | `XmlLoader.load_tree()` |
| [`load_jupyter_notebook()`](#load_jupyter_notebook) | Load source content. Provides direct module-level access to ``JupyterNotebookLoader.load`` using a fresh ``JupyterNotebookLoader`` instance. Any: Value returned by ``JupyterNotebookLoader.load``. | `JupyterNotebookLoader.load()` |

### `load_text()`

Load source content. Provides direct module-level access to ``TextLoader.load`` using a fresh ``TextLoader`` instance. Any: Value returned by ``TextLoader.load``.

```python
load_text( path: str, encoding: Optional[str] = None ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``TextLoader.load``. |
| `encoding` | `Optional[str]` | `None` | Value passed to ``TextLoader.load``. |

### `load_csv()`

Load source content. Provides direct module-level access to ``CsvLoader.load`` using a fresh ``CsvLoader`` instance. Any: Value returned by ``CsvLoader.load``.

```python
load_csv( path: str, encoding: Optional[str] = 'utf-8', source_column: Optional[str] = None, delimiter: str = ',', quotechar: str = '"' ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``CsvLoader.load``. |
| `encoding` | `Optional[str]` | `'utf-8'` | Value passed to ``CsvLoader.load``. |
| `source_column` | `Optional[str]` | `None` | Value passed to ``CsvLoader.load``. |
| `delimiter` | `str` | `','` | Value passed to ``CsvLoader.load``. |
| `quotechar` | `str` | `'"'` | Value passed to ``CsvLoader.load``. |

### `read_pdf()`

Load source content. Provides direct module-level access to ``PdfReader.load`` using a fresh ``PdfReader`` instance. Any: Value returned by ``PdfReader.load``.

```python
read_pdf( path: str, mode: str = 'single' ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``PdfReader.load``. |
| `mode` | `str` | `'single'` | Value passed to ``PdfReader.load``. |

### `load_pdf()`

Load source content. Provides direct module-level access to ``PdfLoader.load`` using a fresh ``PdfLoader`` instance. Any: Value returned by ``PdfLoader.load``.

```python
load_pdf( path: str, mode: str = 'single', extract: str = 'plain', include: bool = False, format: str = 'markdown-img', size: int = 1000, overlap: int = 150, has_tables: bool = True ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``PdfLoader.load``. |
| `mode` | `str` | `'single'` | Value passed to ``PdfLoader.load``. |
| `extract` | `str` | `'plain'` | Value passed to ``PdfLoader.load``. |
| `include` | `bool` | `False` | Value passed to ``PdfLoader.load``. |
| `format` | `str` | `'markdown-img'` | Value passed to ``PdfLoader.load``. |
| `size` | `int` | `1000` | Value passed to ``PdfLoader.load``. |
| `overlap` | `int` | `150` | Value passed to ``PdfLoader.load``. |
| `has_tables` | `bool` | `True` | Value passed to ``PdfLoader.load``. |

### `load_excel()`

Load source content. Provides direct module-level access to ``ExcelLoader.load`` using a fresh ``ExcelLoader`` instance. Any: Value returned by ``ExcelLoader.load``.

```python
load_excel( path: str, mode: str = 'elements', has_headers: bool = True ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``ExcelLoader.load``. |
| `mode` | `str` | `'elements'` | Value passed to ``ExcelLoader.load``. |
| `has_headers` | `bool` | `True` | Value passed to ``ExcelLoader.load``. |

### `load_word()`

Load source content. Provides direct module-level access to ``WordLoader.load`` using a fresh ``WordLoader`` instance. Any: Value returned by ``WordLoader.load``.

```python
load_word( path: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``WordLoader.load``. |

### `load_markdown()`

Load source content. Provides direct module-level access to ``MarkdownLoader.load`` using a fresh ``MarkdownLoader`` instance. Any: Value returned by ``MarkdownLoader.load``.

```python
load_markdown( path: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``MarkdownLoader.load``. |

### `load_html()`

Load source content. Provides direct module-level access to ``HtmlLoader.load`` using a fresh ``HtmlLoader`` instance. Any: Value returned by ``HtmlLoader.load``.

```python
load_html( path: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``HtmlLoader.load``. |

### `load_outlook()`

Load source content. Provides direct module-level access to ``OutlookLoader.load`` using a fresh ``OutlookLoader`` instance. Any: Value returned by ``OutlookLoader.load``.

```python
load_outlook( path: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``OutlookLoader.load``. |

### `load_spfx()`

Load source content. Provides direct module-level access to ``SpfxLoader.load`` using a fresh ``SpfxLoader`` instance. Any: Value returned by ``SpfxLoader.load``.

```python
load_spfx( library_id: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `library_id` | `str` | Required | Value passed to ``SpfxLoader.load``. |

### `load_spfx_folder()`

Load provider folder content. Provides direct module-level access to ``SpfxLoader.load_folder`` using a fresh ``SpfxLoader`` instance. Any: Value returned by ``SpfxLoader.load_folder``.

```python
load_spfx_folder( library_id: str, folder_id: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `library_id` | `str` | Required | Value passed to ``SpfxLoader.load_folder``. |
| `folder_id` | `str` | Required | Value passed to ``SpfxLoader.load_folder``. |

### `load_powerpoint()`

Load source content. Provides direct module-level access to ``PowerPointLoader.load`` using a fresh ``PowerPointLoader`` instance. Any: Value returned by ``PowerPointLoader.load``.

```python
load_powerpoint( path: str, mode: str = 'single' ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``PowerPointLoader.load``. |
| `mode` | `str` | `'single'` | Value passed to ``PowerPointLoader.load``. |

### `load_powerpoint_multiple()`

Load multiple presentation elements. Provides direct module-level access to ``PowerPointLoader.load_multiple`` using a fresh ``PowerPointLoader`` instance. Any: Value returned by ``PowerPointLoader.load_multiple``.

```python
load_powerpoint_multiple( path: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``PowerPointLoader.load_multiple``. |

### `load_email()`

Load source content. Provides direct module-level access to ``EmailLoader.load`` using a fresh ``EmailLoader`` instance. Any: Value returned by ``EmailLoader.load``.

```python
load_email( path: str, mode: str = 'single', attachments: bool = True ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``EmailLoader.load``. |
| `mode` | `str` | `'single'` | Value passed to ``EmailLoader.load``. |
| `attachments` | `bool` | `True` | Value passed to ``EmailLoader.load``. |

### `load_json()`

Load source content. Provides direct module-level access to ``JsonLoader.load`` using a fresh ``JsonLoader`` instance. Any: Value returned by ``JsonLoader.load``.

```python
load_json( filepath: str, is_text: bool = True, is_lines: bool = False ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `filepath` | `str` | Required | Value passed to ``JsonLoader.load``. |
| `is_text` | `bool` | `True` | Value passed to ``JsonLoader.load``. |
| `is_lines` | `bool` | `False` | Value passed to ``JsonLoader.load``. |

### `load_xml()`

Load source content. Provides direct module-level access to ``XmlLoader.load`` using a fresh ``XmlLoader`` instance. Any: Value returned by ``XmlLoader.load``.

```python
load_xml( filepath: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `filepath` | `str` | Required | Value passed to ``XmlLoader.load``. |

### `load_xml_tree()`

Parse an XML element tree. Provides direct module-level access to ``XmlLoader.load_tree`` using a fresh ``XmlLoader`` instance. Any: Value returned by ``XmlLoader.load_tree``.

```python
load_xml_tree( filepath: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `filepath` | `str` | Required | Value passed to ``XmlLoader.load_tree``. |

### `load_jupyter_notebook()`

Load source content. Provides direct module-level access to ``JupyterNotebookLoader.load`` using a fresh ``JupyterNotebookLoader`` instance. Any: Value returned by ``JupyterNotebookLoader.load``.

```python
load_jupyter_notebook( path: str, include_outputs: bool = False, max_output_length: int = 10, remove_newline: bool = False, traceback: bool = False ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Value passed to ``JupyterNotebookLoader.load``. |
| `include_outputs` | `bool` | `False` | Value passed to ``JupyterNotebookLoader.load``. |
| `max_output_length` | `int` | `10` | Value passed to ``JupyterNotebookLoader.load``. |
| `remove_newline` | `bool` | `False` | Value passed to ``JupyterNotebookLoader.load``. |
| `traceback` | `bool` | `False` | Value passed to ``JupyterNotebookLoader.load``. |

## Environmental

| Function | Purpose | Implementation |
|---|---|---|
| [`fetch_google_weather_current()`](#fetch_google_weather_current) | Fetch current. Provides direct module-level access to ``GoogleWeather.fetch_current`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_current``. | `GoogleWeather.fetch_current()` |
| [`fetch_google_weather_hourly_forecast()`](#fetch_google_weather_hourly_forecast) | Fetch hourly forecast. Provides direct module-level access to ``GoogleWeather.fetch_hourly_forecast`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_hourly_forecast``. | `GoogleWeather.fetch_hourly_forecast()` |
| [`fetch_google_weather_daily_forecast()`](#fetch_google_weather_daily_forecast) | Fetch daily forecast. Provides direct module-level access to ``GoogleWeather.fetch_daily_forecast`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_daily_forecast``. | `GoogleWeather.fetch_daily_forecast()` |
| [`fetch_google_weather_hourly_history()`](#fetch_google_weather_hourly_history) | Fetch hourly history. Provides direct module-level access to ``GoogleWeather.fetch_hourly_history`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_hourly_history``. | `GoogleWeather.fetch_hourly_history()` |
| [`fetch_google_weather_alerts()`](#fetch_google_weather_alerts) | Fetch alerts. Provides direct module-level access to ``GoogleWeather.fetch_alerts`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_alerts``. | `GoogleWeather.fetch_alerts()` |
| [`fetch_earth_observatory()`](#fetch_earth_observatory) | Fetch NASA EONET events, categories, sources, and layers. Provides direct module-level access to ``EarthObservatory.fetch`` using a fresh ``EarthObservatory`` instance. Any: Value returned by ``EarthObservatory.fetch``. | `EarthObservatory.fetch()` |
| [`fetch_open_weather()`](#fetch_open_weather) | Fetch Open-Meteo current and forecast weather retrieval. Provides direct module-level access to ``OpenWeather.fetch`` using a fresh ``OpenWeather`` instance. Any: Value returned by ``OpenWeather.fetch``. | `OpenWeather.fetch()` |
| [`fetch_historical_weather()`](#fetch_historical_weather) | Fetch historical weather archive retrieval. Provides direct module-level access to ``HistoricalWeather.fetch`` using a fresh ``HistoricalWeather`` instance. Any: Value returned by ``HistoricalWeather.fetch``. | `HistoricalWeather.fetch()` |
| [`fetch_usgs_earthquakes()`](#fetch_usgs_earthquakes) | Fetch USGS earthquake feed and query retrieval. Provides direct module-level access to ``USGSEarthquakes.fetch`` using a fresh ``USGSEarthquakes`` instance. Any: Value returned by ``USGSEarthquakes.fetch``. | `USGSEarthquakes.fetch()` |
| [`fetch_usgs_water_data()`](#fetch_usgs_water_data) | Fetch USGS water services records. Provides direct module-level access to ``USGSWaterData.fetch`` using a fresh ``USGSWaterData`` instance. Any: Value returned by ``USGSWaterData.fetch``. | `USGSWaterData.fetch()` |
| [`fetch_air_now()`](#fetch_air_now) | Fetch AirNow current and forecast air quality data. Provides direct module-level access to ``AirNow.fetch`` using a fresh ``AirNow`` instance. Any: Value returned by ``AirNow.fetch``. | `AirNow.fetch()` |
| [`fetch_climate_data()`](#fetch_climate_data) | Fetch NOAA climate dataset and data records. Provides direct module-level access to ``ClimateData.fetch`` using a fresh ``ClimateData`` instance. Any: Value returned by ``ClimateData.fetch``. | `ClimateData.fetch()` |
| [`fetch_eonet()`](#fetch_eonet) | Fetch NASA EONET environmental event data. Provides direct module-level access to ``EoNet.fetch`` using a fresh ``EoNet`` instance. Any: Value returned by ``EoNet.fetch``. | `EoNet.fetch()` |
| [`fetch_envirofacts()`](#fetch_envirofacts) | Fetch EPA Envirofacts table and facility records. Provides direct module-level access to ``EnviroFacts.fetch`` using a fresh ``EnviroFacts`` instance. Any: Value returned by ``EnviroFacts.fetch``. | `EnviroFacts.fetch()` |
| [`fetch_tides_and_currents()`](#fetch_tides_and_currents) | Fetch NOAA tides, currents, and station data. Provides direct module-level access to ``TidesAndCurrents.fetch`` using a fresh ``TidesAndCurrents`` instance. Any: Value returned by ``TidesAndCurrents.fetch``. | `TidesAndCurrents.fetch()` |
| [`fetch_uv_index()`](#fetch_uv_index) | Fetch EPA UV Index current and forecast data. Provides direct module-level access to ``UvIndex.fetch`` using a fresh ``UvIndex`` instance. Any: Value returned by ``UvIndex.fetch``. | `UvIndex.fetch()` |
| [`fetch_purple_air()`](#fetch_purple_air) | Fetch PurpleAir sensor and air quality records. Provides direct module-level access to ``PurpleAir.fetch`` using a fresh ``PurpleAir`` instance. Any: Value returned by ``PurpleAir.fetch``. | `PurpleAir.fetch()` |
| [`fetch_open_aq()`](#fetch_open_aq) | Fetch OpenAQ location, measurement, and air-quality records. Provides direct module-level access to ``OpenAQ.fetch`` using a fresh ``OpenAQ`` instance. Any: Value returned by ``OpenAQ.fetch``. | `OpenAQ.fetch()` |
| [`fetch_firms()`](#fetch_firms) | Fetch NASA FIRMS active fire data. Provides direct module-level access to ``Firms.fetch`` using a fresh ``Firms`` instance. Any: Value returned by ``Firms.fetch``. | `Firms.fetch()` |

### `fetch_google_weather_current()`

Fetch current. Provides direct module-level access to ``GoogleWeather.fetch_current`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_current``.

```python
fetch_google_weather_current( address: str, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `address` | `str` | Required | Value passed to ``GoogleWeather.fetch_current``. |
| `units_system` | `str` | `'METRIC'` | Value passed to ``GoogleWeather.fetch_current``. |
| `language_code` | `str` | `'en'` | Value passed to ``GoogleWeather.fetch_current``. |
| `time` | `int` | `10` | Value passed to ``GoogleWeather.fetch_current``. |

### `fetch_google_weather_hourly_forecast()`

Fetch hourly forecast. Provides direct module-level access to ``GoogleWeather.fetch_hourly_forecast`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_hourly_forecast``.

```python
fetch_google_weather_hourly_forecast( address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `address` | `str` | Required | Value passed to ``GoogleWeather.fetch_hourly_forecast``. |
| `hours` | `int` | `24` | Value passed to ``GoogleWeather.fetch_hourly_forecast``. |
| `units_system` | `str` | `'METRIC'` | Value passed to ``GoogleWeather.fetch_hourly_forecast``. |
| `language_code` | `str` | `'en'` | Value passed to ``GoogleWeather.fetch_hourly_forecast``. |
| `time` | `int` | `10` | Value passed to ``GoogleWeather.fetch_hourly_forecast``. |

### `fetch_google_weather_daily_forecast()`

Fetch daily forecast. Provides direct module-level access to ``GoogleWeather.fetch_daily_forecast`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_daily_forecast``.

```python
fetch_google_weather_daily_forecast( address: str, days: int = 5, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `address` | `str` | Required | Value passed to ``GoogleWeather.fetch_daily_forecast``. |
| `days` | `int` | `5` | Value passed to ``GoogleWeather.fetch_daily_forecast``. |
| `units_system` | `str` | `'METRIC'` | Value passed to ``GoogleWeather.fetch_daily_forecast``. |
| `language_code` | `str` | `'en'` | Value passed to ``GoogleWeather.fetch_daily_forecast``. |
| `time` | `int` | `10` | Value passed to ``GoogleWeather.fetch_daily_forecast``. |

### `fetch_google_weather_hourly_history()`

Fetch hourly history. Provides direct module-level access to ``GoogleWeather.fetch_hourly_history`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_hourly_history``.

```python
fetch_google_weather_hourly_history( address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `address` | `str` | Required | Value passed to ``GoogleWeather.fetch_hourly_history``. |
| `hours` | `int` | `24` | Value passed to ``GoogleWeather.fetch_hourly_history``. |
| `units_system` | `str` | `'METRIC'` | Value passed to ``GoogleWeather.fetch_hourly_history``. |
| `language_code` | `str` | `'en'` | Value passed to ``GoogleWeather.fetch_hourly_history``. |
| `time` | `int` | `10` | Value passed to ``GoogleWeather.fetch_hourly_history``. |

### `fetch_google_weather_alerts()`

Fetch alerts. Provides direct module-level access to ``GoogleWeather.fetch_alerts`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_alerts``.

```python
fetch_google_weather_alerts( address: str, language_code: str = 'en', time: int = 10 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `address` | `str` | Required | Value passed to ``GoogleWeather.fetch_alerts``. |
| `language_code` | `str` | `'en'` | Value passed to ``GoogleWeather.fetch_alerts``. |
| `time` | `int` | `10` | Value passed to ``GoogleWeather.fetch_alerts``. |

### `fetch_earth_observatory()`

Fetch NASA EONET events, categories, sources, and layers. Provides direct module-level access to ``EarthObservatory.fetch`` using a fresh ``EarthObservatory`` instance. Any: Value returned by ``EarthObservatory.fetch``.

```python
fetch_earth_observatory( mode: str = 'events', status: str = 'open', category: str = '', source: str = '', limit: int = 20, days: int = 30, start_date: str = '', end_date: str = '', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_open_weather()`

Fetch Open-Meteo current and forecast weather retrieval. Provides direct module-level access to ``OpenWeather.fetch`` using a fresh ``OpenWeather`` instance. Any: Value returned by ``OpenWeather.fetch``.

```python
fetch_open_weather( location: str, mode: str = 'current', zone: str = 'auto', forecast_days: int = 7, past_days: int = 0, count: int = 10 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `location` | `str` | Required | Value passed to ``OpenWeather.fetch``. |
| `mode` | `str` | `'current'` | Value passed to ``OpenWeather.fetch``. |
| `zone` | `str` | `'auto'` | Value passed to ``OpenWeather.fetch``. |
| `forecast_days` | `int` | `7` | Value passed to ``OpenWeather.fetch``. |
| `past_days` | `int` | `0` | Value passed to ``OpenWeather.fetch``. |
| `count` | `int` | `10` | Value passed to ``OpenWeather.fetch``. |

### `fetch_historical_weather()`

Fetch historical weather archive retrieval. Provides direct module-level access to ``HistoricalWeather.fetch`` using a fresh ``HistoricalWeather`` instance. Any: Value returned by ``HistoricalWeather.fetch``.

```python
fetch_historical_weather( location: str, date: dt.date, zone: str = 'auto', count: int = 10 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `location` | `str` | Required | Value passed to ``HistoricalWeather.fetch``. |
| `date` | `dt.date` | Required | Value passed to ``HistoricalWeather.fetch``. |
| `zone` | `str` | `'auto'` | Value passed to ``HistoricalWeather.fetch``. |
| `count` | `int` | `10` | Value passed to ``HistoricalWeather.fetch``. |

### `fetch_usgs_earthquakes()`

Fetch USGS earthquake feed and query retrieval. Provides direct module-level access to ``USGSEarthquakes.fetch`` using a fresh ``USGSEarthquakes`` instance. Any: Value returned by ``USGSEarthquakes.fetch``.

```python
fetch_usgs_earthquakes( mode: str = 'feed', feed: str = 'all_day.geojson', start_date: str = '', end_date: str = '', min_magnitude: float = 1.0, max_magnitude: float = 10.0, limit: int = 25, order_by: str = 'time', event_type: str = 'earthquake', latitude: float | None = None, longitude: float | None = None, max_radius_km: float | None = None, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_usgs_water_data()`

Fetch USGS water services records. Provides direct module-level access to ``USGSWaterData.fetch`` using a fresh ``USGSWaterData`` instance. Any: Value returned by ``USGSWaterData.fetch``.

```python
fetch_usgs_water_data( mode: str = 'monitoring-locations', monitoring_location_id: str = '', state_code: str = '', county_code: str = '', site_type: str = '', parameter_code: str = '', limit: int = 25, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'monitoring-locations'` | Value passed to ``USGSWaterData.fetch``. |
| `monitoring_location_id` | `str` | `''` | Value passed to ``USGSWaterData.fetch``. |
| `state_code` | `str` | `''` | Value passed to ``USGSWaterData.fetch``. |
| `county_code` | `str` | `''` | Value passed to ``USGSWaterData.fetch``. |
| `site_type` | `str` | `''` | Value passed to ``USGSWaterData.fetch``. |
| `parameter_code` | `str` | `''` | Value passed to ``USGSWaterData.fetch``. |
| `limit` | `int` | `25` | Value passed to ``USGSWaterData.fetch``. |
| `time` | `int` | `20` | Value passed to ``USGSWaterData.fetch``. |

### `fetch_air_now()`

Fetch AirNow current and forecast air quality data. Provides direct module-level access to ``AirNow.fetch`` using a fresh ``AirNow`` instance. Any: Value returned by ``AirNow.fetch``.

```python
fetch_air_now( mode: str = 'current-zip', zip_code: str = '', latitude: float | None = None, longitude: float | None = None, date: str = '', distance: int = 25, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'current-zip'` | Value passed to ``AirNow.fetch``. |
| `zip_code` | `str` | `''` | Value passed to ``AirNow.fetch``. |
| `latitude` | `float | None` | `None` | Value passed to ``AirNow.fetch``. |
| `longitude` | `float | None` | `None` | Value passed to ``AirNow.fetch``. |
| `date` | `str` | `''` | Value passed to ``AirNow.fetch``. |
| `distance` | `int` | `25` | Value passed to ``AirNow.fetch``. |
| `time` | `int` | `20` | Value passed to ``AirNow.fetch``. |

### `fetch_climate_data()`

Fetch NOAA climate dataset and data records. Provides direct module-level access to ``ClimateData.fetch`` using a fresh ``ClimateData`` instance. Any: Value returned by ``ClimateData.fetch``.

```python
fetch_climate_data( mode: str = 'datasets', keyword: str = '', dataset: str = '', start_date: str = '', end_date: str = '', stations: str = '', data_types: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_eonet()`

Fetch NASA EONET environmental event data. Provides direct module-level access to ``EoNet.fetch`` using a fresh ``EoNet`` instance. Any: Value returned by ``EoNet.fetch``.

```python
fetch_eonet( mode: str = 'events', source: str = '', category: str = '', status: str = 'open', limit: int = 25, days: int = 30, start_date: str = '', end_date: str = '', bbox: str = '', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_envirofacts()`

Fetch EPA Envirofacts table and facility records. Provides direct module-level access to ``EnviroFacts.fetch`` using a fresh ``EnviroFacts`` instance. Any: Value returned by ``EnviroFacts.fetch``.

```python
fetch_envirofacts( table_name: str = 'TRI_FACILITY', state_code: str = '', facility_name: str = '', limit: int = 25, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `table_name` | `str` | `'TRI_FACILITY'` | Value passed to ``EnviroFacts.fetch``. |
| `state_code` | `str` | `''` | Value passed to ``EnviroFacts.fetch``. |
| `facility_name` | `str` | `''` | Value passed to ``EnviroFacts.fetch``. |
| `limit` | `int` | `25` | Value passed to ``EnviroFacts.fetch``. |
| `time` | `int` | `20` | Value passed to ``EnviroFacts.fetch``. |

### `fetch_tides_and_currents()`

Fetch NOAA tides, currents, and station data. Provides direct module-level access to ``TidesAndCurrents.fetch`` using a fresh ``TidesAndCurrents`` instance. Any: Value returned by ``TidesAndCurrents.fetch``.

```python
fetch_tides_and_currents( mode: str = 'water-level', station_id: str = '', begin_date: str = '', end_date: str = '', datum: str = 'MLLW', units: str = 'metric', time_zone: str = 'gmt', interval: str = 'hilo', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_uv_index()`

Fetch EPA UV Index current and forecast data. Provides direct module-level access to ``UvIndex.fetch`` using a fresh ``UvIndex`` instance. Any: Value returned by ``UvIndex.fetch``.

```python
fetch_uv_index( mode: str = 'daily-zip', zip_code: str = '', city: str = '', state: str = '', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'daily-zip'` | Value passed to ``UvIndex.fetch``. |
| `zip_code` | `str` | `''` | Value passed to ``UvIndex.fetch``. |
| `city` | `str` | `''` | Value passed to ``UvIndex.fetch``. |
| `state` | `str` | `''` | Value passed to ``UvIndex.fetch``. |
| `time` | `int` | `20` | Value passed to ``UvIndex.fetch``. |

### `fetch_purple_air()`

Fetch PurpleAir sensor and air quality records. Provides direct module-level access to ``PurpleAir.fetch`` using a fresh ``PurpleAir`` instance. Any: Value returned by ``PurpleAir.fetch``.

```python
fetch_purple_air( mode: str = 'sensors', sensor_index: int = None, nwlng: float | None = None, nwlat: float | None = None, selng: float | None = None, selat: float | None = None, location_type: int = 0, max_age: int = 0, modified_since: int = 0, fields: str = '', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_open_aq()`

Fetch OpenAQ location, measurement, and air-quality records. Provides direct module-level access to ``OpenAQ.fetch`` using a fresh ``OpenAQ`` instance. Any: Value returned by ``OpenAQ.fetch``.

```python
fetch_open_aq( mode: str = 'locations', location_id: int = None, parameter_id: int = None, country_id: int = None, coordinates: str = '', radius: int = 25000, providers_id: str = '', parameters_id: str = '', limit: int = 25, page: int = 1, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_firms()`

Fetch NASA FIRMS active fire data. Provides direct module-level access to ``Firms.fetch`` using a fresh ``Firms`` instance. Any: Value returned by ``Firms.fetch``.

```python
fetch_firms( mode: str = 'area', source: str = 'VIIRS_SNPP_NRT', area_coordinates: str = 'world', day_range: int = 1, date: str = '', sensor: str = 'ALL', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'area'` | Value passed to ``Firms.fetch``. |
| `source` | `str` | `'VIIRS_SNPP_NRT'` | Value passed to ``Firms.fetch``. |
| `area_coordinates` | `str` | `'world'` | Value passed to ``Firms.fetch``. |
| `day_range` | `int` | `1` | Value passed to ``Firms.fetch``. |
| `date` | `str` | `''` | Value passed to ``Firms.fetch``. |
| `sensor` | `str` | `'ALL'` | Value passed to ``Firms.fetch``. |
| `time` | `int` | `20` | Value passed to ``Firms.fetch``. |

## Geospatial

| Function | Purpose | Implementation |
|---|---|---|
| [`geocode_location()`](#geocode_location) | Geocode location. Provides direct module-level access to ``GoogleMaps.geocode_location`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.geocode_location``. | `GoogleMaps.geocode_location()` |
| [`geocode_coordinates()`](#geocode_coordinates) | Geocode coordinates. Provides direct module-level access to ``GoogleMaps.geocode_coordinates`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.geocode_coordinates``. | `GoogleMaps.geocode_coordinates()` |
| [`validate_address()`](#validate_address) | Validate address. Provides direct module-level access to ``GoogleMaps.validate_address`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.validate_address``. | `GoogleMaps.validate_address()` |
| [`request_directions()`](#request_directions) | Request directions. Provides direct module-level access to ``GoogleMaps.request_directions`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.request_directions``. | `GoogleMaps.request_directions()` |
| [`fetch_global_imagery_wms_map()`](#fetch_global_imagery_wms_map) | Fetch wms map. Provides direct module-level access to ``GlobalImagery.fetch_wms_map`` using a fresh ``GlobalImagery`` instance. Any: Value returned by ``GlobalImagery.fetch_wms_map``. | `GlobalImagery.fetch_wms_map()` |
| [`fetch_global_imagery_map_services()`](#fetch_global_imagery_map_services) | Fetch map services. Provides direct module-level access to ``GlobalImagery.fetch_map_services`` using a fresh ``GlobalImagery`` instance. None. Any: Value returned by ``GlobalImagery.fetch_map_services``. | `GlobalImagery.fetch_map_services()` |
| [`fetch_global_imagery_mercator_map()`](#fetch_global_imagery_mercator_map) | Fetch mercator map. Provides direct module-level access to ``GlobalImagery.fetch_mercator_map`` using a fresh ``GlobalImagery`` instance. Any: Value returned by ``GlobalImagery.fetch_mercator_map``. | `GlobalImagery.fetch_mercator_map()` |
| [`fetch_google_geocoding()`](#fetch_google_geocoding) | Fetch Google forward, reverse, and place geocoding. Provides direct module-level access to ``GoogleGeocoding.fetch`` using a fresh ``GoogleGeocoding`` instance. Any: Value returned by ``GoogleGeocoding.fetch``. | `GoogleGeocoding.fetch()` |
| [`fetch_usgs_national_map()`](#fetch_usgs_national_map) | Fetch USGS National Map datasets and products. Provides direct module-level access to ``USGSTheNationalMap.fetch`` using a fresh ``USGSTheNationalMap`` instance. Any: Value returned by ``USGSTheNationalMap.fetch``. | `USGSTheNationalMap.fetch()` |
| [`fetch_usgs_sciencebase()`](#fetch_usgs_sciencebase) | Fetch USGS ScienceBase items and catalog records. Provides direct module-level access to ``USGSScienceBase.fetch`` using a fresh ``USGSScienceBase`` instance. Any: Value returned by ``USGSScienceBase.fetch``. | `USGSScienceBase.fetch()` |

### `geocode_location()`

Geocode location. Provides direct module-level access to ``GoogleMaps.geocode_location`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.geocode_location``.

```python
geocode_location( address: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `address` | `str` | Required | Value passed to ``GoogleMaps.geocode_location``. |

### `geocode_coordinates()`

Geocode coordinates. Provides direct module-level access to ``GoogleMaps.geocode_coordinates`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.geocode_coordinates``.

```python
geocode_coordinates( lat: float, long: float ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `lat` | `float` | Required | Value passed to ``GoogleMaps.geocode_coordinates``. |
| `long` | `float` | Required | Value passed to ``GoogleMaps.geocode_coordinates``. |

### `validate_address()`

Validate address. Provides direct module-level access to ``GoogleMaps.validate_address`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.validate_address``.

```python
validate_address( address: List[str] ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `address` | `List[str]` | Required | Value passed to ``GoogleMaps.validate_address``. |

### `request_directions()`

Request directions. Provides direct module-level access to ``GoogleMaps.request_directions`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.request_directions``.

```python
request_directions( origin: str, destination: str, mode: str = 'driving' ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `origin` | `str` | Required | Value passed to ``GoogleMaps.request_directions``. |
| `destination` | `str` | Required | Value passed to ``GoogleMaps.request_directions``. |
| `mode` | `str` | `'driving'` | Value passed to ``GoogleMaps.request_directions``. |

### `fetch_global_imagery_wms_map()`

Fetch wms map. Provides direct module-level access to ``GlobalImagery.fetch_wms_map`` using a fresh ``GlobalImagery`` instance. Any: Value returned by ``GlobalImagery.fetch_wms_map``.

```python
fetch_global_imagery_wms_map( layer: str, image_date: str, bbox: Tuple[float, float, float, float], width: int = 1200, height: int = 600, projection: str = 'epsg4326', quality: str = 'best', image_format: str = 'image/png', transparent: bool = True, output_dir: str = 'python-examples', output_name: str = '', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_global_imagery_map_services()`

Fetch map services. Provides direct module-level access to ``GlobalImagery.fetch_map_services`` using a fresh ``GlobalImagery`` instance. None. Any: Value returned by ``GlobalImagery.fetch_map_services``.

```python
fetch_global_imagery_map_services(  ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|

### `fetch_global_imagery_mercator_map()`

Fetch mercator map. Provides direct module-level access to ``GlobalImagery.fetch_mercator_map`` using a fresh ``GlobalImagery`` instance. Any: Value returned by ``GlobalImagery.fetch_mercator_map``.

```python
fetch_global_imagery_mercator_map( ccrs: Any = None ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `ccrs` | `Any` | `None` | Value passed to ``GlobalImagery.fetch_mercator_map``. |

### `fetch_google_geocoding()`

Fetch Google forward, reverse, and place geocoding. Provides direct module-level access to ``GoogleGeocoding.fetch`` using a fresh ``GoogleGeocoding`` instance. Any: Value returned by ``GoogleGeocoding.fetch``.

```python
fetch_google_geocoding( mode: str = 'forward', query: str = '', latitude: float = 0.0, longitude: float = 0.0, place_id: str = '', language: str = 'en', region: str = '', result_type: str = '', location_type: str = '', time: int = 10, api_key: Optional[str] = None ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_usgs_national_map()`

Fetch USGS National Map datasets and products. Provides direct module-level access to ``USGSTheNationalMap.fetch`` using a fresh ``USGSTheNationalMap`` instance. Any: Value returned by ``USGSTheNationalMap.fetch``.

```python
fetch_usgs_national_map( mode: str = 'products', dataset: str = '', q: str = '', bbox: str = '', prod_formats: str = '', max_items: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'products'` | Value passed to ``USGSTheNationalMap.fetch``. |
| `dataset` | `str` | `''` | Value passed to ``USGSTheNationalMap.fetch``. |
| `q` | `str` | `''` | Value passed to ``USGSTheNationalMap.fetch``. |
| `bbox` | `str` | `''` | Value passed to ``USGSTheNationalMap.fetch``. |
| `prod_formats` | `str` | `''` | Value passed to ``USGSTheNationalMap.fetch``. |
| `max_items` | `int` | `25` | Value passed to ``USGSTheNationalMap.fetch``. |
| `offset` | `int` | `0` | Value passed to ``USGSTheNationalMap.fetch``. |
| `time` | `int` | `20` | Value passed to ``USGSTheNationalMap.fetch``. |

### `fetch_usgs_sciencebase()`

Fetch USGS ScienceBase items and catalog records. Provides direct module-level access to ``USGSScienceBase.fetch`` using a fresh ``USGSScienceBase`` instance. Any: Value returned by ``USGSScienceBase.fetch``.

```python
fetch_usgs_sciencebase( mode: str = 'items', q: str = '', item_id: str = '', max_items: int = 25, offset: int = 0, fields: str = '', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'items'` | Value passed to ``USGSScienceBase.fetch``. |
| `q` | `str` | `''` | Value passed to ``USGSScienceBase.fetch``. |
| `item_id` | `str` | `''` | Value passed to ``USGSScienceBase.fetch``. |
| `max_items` | `int` | `25` | Value passed to ``USGSScienceBase.fetch``. |
| `offset` | `int` | `0` | Value passed to ``USGSScienceBase.fetch``. |
| `fields` | `str` | `''` | Value passed to ``USGSScienceBase.fetch``. |
| `time` | `int` | `20` | Value passed to ``USGSScienceBase.fetch``. |

## Health

| Function | Purpose | Implementation |
|---|---|---|
| [`fetch_health_data()`](#fetch_health_data) | Fetch HealthData.gov Socrata metadata and rows. Provides direct module-level access to ``HealthData.fetch`` using a fresh ``HealthData`` instance. Any: Value returned by ``HealthData.fetch``. | `HealthData.fetch()` |
| [`fetch_global_health_data()`](#fetch_global_health_data) | Fetch WHO global health indicator and Athena data. Provides direct module-level access to ``GlobalHealthData.fetch`` using a fresh ``GlobalHealthData`` instance. Any: Value returned by ``GlobalHealthData.fetch``. | `GlobalHealthData.fetch()` |
| [`fetch_wonder()`](#fetch_wonder) | Fetch CDC WONDER template and query submission. Provides direct module-level access to ``Wonder.fetch`` using a fresh ``Wonder`` instance. Any: Value returned by ``Wonder.fetch``. | `Wonder.fetch()` |
| [`load_pubmed()`](#load_pubmed) | Load source content. Provides direct module-level access to ``PubMedSearchLoader.load`` using a fresh ``PubMedSearchLoader`` instance. Any: Value returned by ``PubMedSearchLoader.load``. | `PubMedSearchLoader.load()` |

### `fetch_health_data()`

Fetch HealthData.gov Socrata metadata and rows. Provides direct module-level access to ``HealthData.fetch`` using a fresh ``HealthData`` instance. Any: Value returned by ``HealthData.fetch``.

```python
fetch_health_data( mode: str = 'rows', domain: str = 'healthdata.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `fetch_global_health_data()`

Fetch WHO global health indicator and Athena data. Provides direct module-level access to ``GlobalHealthData.fetch`` using a fresh ``GlobalHealthData`` instance. Any: Value returned by ``GlobalHealthData.fetch``.

```python
fetch_global_health_data( mode: str = 'indicator_registry', query_path: str = '', fmt: str = 'json', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'indicator_registry'` | Value passed to ``GlobalHealthData.fetch``. |
| `query_path` | `str` | `''` | Value passed to ``GlobalHealthData.fetch``. |
| `fmt` | `str` | `'json'` | Value passed to ``GlobalHealthData.fetch``. |
| `time` | `int` | `20` | Value passed to ``GlobalHealthData.fetch``. |

### `fetch_wonder()`

Fetch CDC WONDER template and query submission. Provides direct module-level access to ``Wonder.fetch`` using a fresh ``Wonder`` instance. Any: Value returned by ``Wonder.fetch``.

```python
fetch_wonder( mode: str = 'metadata_template', dataset_id: str = 'D76', request_xml: str = '', time: int = 20 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `mode` | `str` | `'metadata_template'` | Value passed to ``Wonder.fetch``. |
| `dataset_id` | `str` | `'D76'` | Value passed to ``Wonder.fetch``. |
| `request_xml` | `str` | `''` | Value passed to ``Wonder.fetch``. |
| `time` | `int` | `20` | Value passed to ``Wonder.fetch``. |

### `load_pubmed()`

Load source content. Provides direct module-level access to ``PubMedSearchLoader.load`` using a fresh ``PubMedSearchLoader`` instance. Any: Value returned by ``PubMedSearchLoader.load``.

```python
load_pubmed( query: str, max_docs: int = 5 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `query` | `str` | Required | Value passed to ``PubMedSearchLoader.load``. |
| `max_docs` | `int` | `5` | Value passed to ``PubMedSearchLoader.load``. |

## Web

| Function | Purpose | Implementation |
|---|---|---|
| [`fetch_web_page()`](#fetch_web_page) | Fetch HTTP web page retrieval and HTML extraction. Provides direct module-level access to ``WebFetcher.fetch`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.fetch``. | `WebFetcher.fetch()` |
| [`convert_html_to_text()`](#convert_html_to_text) | HTML to text. Provides direct module-level access to ``WebFetcher.html_to_text`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.html_to_text``. | `WebFetcher.html_to_text()` |
| [`extract_web_title()`](#extract_web_title) | Extract title. Provides direct module-level access to ``WebFetcher.extract_title`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_title``. | `WebFetcher.extract_title()` |
| [`extract_web_links()`](#extract_web_links) | Extract links. Provides direct module-level access to ``WebFetcher.extract_links`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_links``. | `WebFetcher.extract_links()` |
| [`extract_web_structured_data()`](#extract_web_structured_data) | Extract structured data. Provides direct module-level access to ``WebFetcher.extract_structured_data`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_structured_data``. | `WebFetcher.extract_structured_data()` |
| [`crawl_web()`](#crawl_web) | Crawl. Provides direct module-level access to ``WebCrawler.crawl`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.crawl``. | `WebCrawler.crawl()` |
| [`scrape_crawler_page()`](#scrape_crawler_page) | Scrape page. Provides direct module-level access to ``WebCrawler.scrape_page`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.scrape_page``. | `WebCrawler.scrape_page()` |
| [`render_web_page()`](#render_web_page) | Render with playwright. Provides direct module-level access to ``WebCrawler.render_with_playwright`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.render_with_playwright``. | `WebCrawler.render_with_playwright()` |
| [`load_web()`](#load_web) | Load source content. Provides direct module-level access to ``WebLoader.load`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load``. | `WebLoader.load()` |
| [`load_web_recursive()`](#load_web_recursive) | Load web documents recursively. Provides direct module-level access to ``WebLoader.load_recursive`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load_recursive``. | `WebLoader.load_recursive()` |
| [`load_web_pages()`](#load_web_pages) | Load static web pages. Provides direct module-level access to ``WebLoader.load_pages`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load_pages``. | `WebLoader.load_pages()` |
| [`load_github()`](#load_github) | Load source content. Provides direct module-level access to ``GithubLoader.load`` using a fresh ``GithubLoader`` instance. Any: Value returned by ``GithubLoader.load``. | `GithubLoader.load()` |
| [`scrape_web_page()`](#scrape_web_page) | Fetch a web page. Provides direct module-level access to ``WebExtractor.scrape`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape``. | `WebExtractor.scrape()` |
| [`scraper_html_to_text()`](#scraper_html_to_text) | Convert HTML to plain text. Provides direct module-level access to ``WebExtractor.html_to_text`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.html_to_text``. | `WebExtractor.html_to_text()` |
| [`scrape_paragraphs()`](#scrape_paragraphs) | Extract paragraph text. Provides direct module-level access to ``WebExtractor.scrape_paragraphs`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_paragraphs``. | `WebExtractor.scrape_paragraphs()` |
| [`scrape_lists()`](#scrape_lists) | Extract list item text. Provides direct module-level access to ``WebExtractor.scrape_lists`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_lists``. | `WebExtractor.scrape_lists()` |
| [`scrape_tables()`](#scrape_tables) | Extract table cell text. Provides direct module-level access to ``WebExtractor.scrape_tables`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_tables``. | `WebExtractor.scrape_tables()` |
| [`scrape_articles()`](#scrape_articles) | Extract article text. Provides direct module-level access to ``WebExtractor.scrape_articles`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_articles``. | `WebExtractor.scrape_articles()` |
| [`scrape_headings()`](#scrape_headings) | Extract heading text. Provides direct module-level access to ``WebExtractor.scrape_headings`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_headings``. | `WebExtractor.scrape_headings()` |
| [`scrape_divisions()`](#scrape_divisions) | Extract division text. Provides direct module-level access to ``WebExtractor.scrape_divisions`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_divisions``. | `WebExtractor.scrape_divisions()` |
| [`scrape_sections()`](#scrape_sections) | Extract section text. Provides direct module-level access to ``WebExtractor.scrape_sections`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_sections``. | `WebExtractor.scrape_sections()` |
| [`scrape_blockquotes()`](#scrape_blockquotes) | Extract blockquote text. Provides direct module-level access to ``WebExtractor.scrape_blockquotes`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_blockquotes``. | `WebExtractor.scrape_blockquotes()` |
| [`scrape_hyperlinks()`](#scrape_hyperlinks) | Extract hyperlinks. Provides direct module-level access to ``WebExtractor.scrape_hyperlinks`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_hyperlinks``. | `WebExtractor.scrape_hyperlinks()` |
| [`scrape_images()`](#scrape_images) | Extract image references. Provides direct module-level access to ``WebExtractor.scrape_images`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_images``. | `WebExtractor.scrape_images()` |
| [`encode_image()`](#encode_image) | Encode an image as Base64 text. Provides direct module-level access to ``fetchers.encode_image``. str: Base64-encoded image data. | `_encode_image()` |

### `fetch_web_page()`

Fetch HTTP web page retrieval and HTML extraction. Provides direct module-level access to ``WebFetcher.fetch`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.fetch``.

```python
fetch_web_page( url: str, time: int = 10 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `url` | `str` | Required | Value passed to ``WebFetcher.fetch``. |
| `time` | `int` | `10` | Value passed to ``WebFetcher.fetch``. |

### `convert_html_to_text()`

HTML to text. Provides direct module-level access to ``WebFetcher.html_to_text`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.html_to_text``.

```python
convert_html_to_text( html: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `html` | `str` | Required | Value passed to ``WebFetcher.html_to_text``. |

### `extract_web_title()`

Extract title. Provides direct module-level access to ``WebFetcher.extract_title`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_title``.

```python
extract_web_title( html: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `html` | `str` | Required | Value passed to ``WebFetcher.extract_title``. |

### `extract_web_links()`

Extract links. Provides direct module-level access to ``WebFetcher.extract_links`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_links``.

```python
extract_web_links( base_url: str, html: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `base_url` | `str` | Required | Value passed to ``WebFetcher.extract_links``. |
| `html` | `str` | Required | Value passed to ``WebFetcher.extract_links``. |

### `extract_web_structured_data()`

Extract structured data. Provides direct module-level access to ``WebFetcher.extract_structured_data`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_structured_data``.

```python
extract_web_structured_data( url: str, html: str, selected_methods: Optional[List[str]] = None ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `url` | `str` | Required | Value passed to ``WebFetcher.extract_structured_data``. |
| `html` | `str` | Required | Value passed to ``WebFetcher.extract_structured_data``. |
| `selected_methods` | `Optional[List[str]]` | `None` | Value passed to ``WebFetcher.extract_structured_data``. |

### `crawl_web()`

Crawl. Provides direct module-level access to ``WebCrawler.crawl`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.crawl``.

```python
crawl_web( seed_url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, recursive: bool = False, max_depth: int = 1, max_pages: int = 10, same_domain_only: bool = True, request_timeout: int = 10, delay_seconds: float = 0.25, max_bytes: int = 1000000, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `scrape_crawler_page()`

Scrape page. Provides direct module-level access to ``WebCrawler.scrape_page`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.scrape_page``.

```python
scrape_crawler_page( url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, request_timeout: int = 10, max_bytes: int = 1000000, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any
```

| Parameter | Type | Default | Notes |
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

### `render_web_page()`

Render with playwright. Provides direct module-level access to ``WebCrawler.render_with_playwright`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.render_with_playwright``.

```python
render_web_page( url: str, timeout: int = 15, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `url` | `str` | Required | Value passed to ``WebCrawler.render_with_playwright``. |
| `timeout` | `int` | `15` | Value passed to ``WebCrawler.render_with_playwright``. |
| `headers` | `Optional[Dict[str, str]]` | `None` | Value passed to ``WebCrawler.render_with_playwright``. |
| `use_playwright` | `bool` | `False` | Value passed to ``WebCrawler.render_with_playwright``. |

### `load_web()`

Load source content. Provides direct module-level access to ``WebLoader.load`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load``.

```python
load_web( urls: str | List[str], recursive: bool = False, max_depth: int = 2, prevent_outside: bool = True, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `urls` | `str | List[str]` | Required | Value passed to ``WebLoader.load``. |
| `recursive` | `bool` | `False` | Value passed to ``WebLoader.load``. |
| `max_depth` | `int` | `2` | Value passed to ``WebLoader.load``. |
| `prevent_outside` | `bool` | `True` | Value passed to ``WebLoader.load``. |
| `timeout` | `int` | `10` | Value passed to ``WebLoader.load``. |
| `ignore` | `bool` | `True` | Value passed to ``WebLoader.load``. |
| `progress` | `bool` | `True` | Value passed to ``WebLoader.load``. |

### `load_web_recursive()`

Load web documents recursively. Provides direct module-level access to ``WebLoader.load_recursive`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load_recursive``.

```python
load_web_recursive( url: str, depth: int = 2, max_time: int = 10, ignore: bool = True ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `url` | `str` | Required | Value passed to ``WebLoader.load_recursive``. |
| `depth` | `int` | `2` | Value passed to ``WebLoader.load_recursive``. |
| `max_time` | `int` | `10` | Value passed to ``WebLoader.load_recursive``. |
| `ignore` | `bool` | `True` | Value passed to ``WebLoader.load_recursive``. |

### `load_web_pages()`

Load static web pages. Provides direct module-level access to ``WebLoader.load_pages`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load_pages``.

```python
load_web_pages( urls: List[str], depth: int = 2, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `urls` | `List[str]` | Required | Value passed to ``WebLoader.load_pages``. |
| `depth` | `int` | `2` | Value passed to ``WebLoader.load_pages``. |
| `timeout` | `int` | `10` | Value passed to ``WebLoader.load_pages``. |
| `ignore` | `bool` | `True` | Value passed to ``WebLoader.load_pages``. |
| `progress` | `bool` | `True` | Value passed to ``WebLoader.load_pages``. |

### `load_github()`

Load source content. Provides direct module-level access to ``GithubLoader.load`` using a fresh ``GithubLoader`` instance. Any: Value returned by ``GithubLoader.load``.

```python
load_github( url: str, repo: str, branch: str, filetype: str = '.md' ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `url` | `str` | Required | Value passed to ``GithubLoader.load``. |
| `repo` | `str` | Required | Value passed to ``GithubLoader.load``. |
| `branch` | `str` | Required | Value passed to ``GithubLoader.load``. |
| `filetype` | `str` | `'.md'` | Value passed to ``GithubLoader.load``. |

### `scrape_web_page()`

Fetch a web page. Provides direct module-level access to ``WebExtractor.scrape`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape``.

```python
scrape_web_page( url: str, time: int = 10 ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `url` | `str` | Required | Value passed to ``WebExtractor.scrape``. |
| `time` | `int` | `10` | Value passed to ``WebExtractor.scrape``. |

### `scraper_html_to_text()`

Convert HTML to plain text. Provides direct module-level access to ``WebExtractor.html_to_text`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.html_to_text``.

```python
scraper_html_to_text( html: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `html` | `str` | Required | Value passed to ``WebExtractor.html_to_text``. |

### `scrape_paragraphs()`

Extract paragraph text. Provides direct module-level access to ``WebExtractor.scrape_paragraphs`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_paragraphs``.

```python
scrape_paragraphs( uri: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_paragraphs``. |

### `scrape_lists()`

Extract list item text. Provides direct module-level access to ``WebExtractor.scrape_lists`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_lists``.

```python
scrape_lists( uri: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_lists``. |

### `scrape_tables()`

Extract table cell text. Provides direct module-level access to ``WebExtractor.scrape_tables`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_tables``.

```python
scrape_tables( uri: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_tables``. |

### `scrape_articles()`

Extract article text. Provides direct module-level access to ``WebExtractor.scrape_articles`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_articles``.

```python
scrape_articles( uri: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_articles``. |

### `scrape_headings()`

Extract heading text. Provides direct module-level access to ``WebExtractor.scrape_headings`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_headings``.

```python
scrape_headings( uri: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_headings``. |

### `scrape_divisions()`

Extract division text. Provides direct module-level access to ``WebExtractor.scrape_divisions`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_divisions``.

```python
scrape_divisions( uri: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_divisions``. |

### `scrape_sections()`

Extract section text. Provides direct module-level access to ``WebExtractor.scrape_sections`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_sections``.

```python
scrape_sections( uri: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_sections``. |

### `scrape_blockquotes()`

Extract blockquote text. Provides direct module-level access to ``WebExtractor.scrape_blockquotes`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_blockquotes``.

```python
scrape_blockquotes( uri: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_blockquotes``. |

### `scrape_hyperlinks()`

Extract hyperlinks. Provides direct module-level access to ``WebExtractor.scrape_hyperlinks`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_hyperlinks``.

```python
scrape_hyperlinks( uri: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_hyperlinks``. |

### `scrape_images()`

Extract image references. Provides direct module-level access to ``WebExtractor.scrape_images`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_images``.

```python
scrape_images( uri: str ) -> Any
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `uri` | `str` | Required | Value passed to ``WebExtractor.scrape_images``. |

### `encode_image()`

Encode an image as Base64 text. Provides direct module-level access to ``fetchers.encode_image``. str: Base64-encoded image data.

```python
encode_image( path: str ) -> str
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | Required | Local image path to encode. |
