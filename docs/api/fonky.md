# Functional API — `fonky.py`

Current wrapper count: **110**.

## Archives

| Function | Signature | Purpose |
|---|---|---|
| `fetch_arxiv()` | `fetch_arxiv( question: str, max_documents: int = None, full_documents: bool = None, include_metadata: bool = None ) -> Any` | Fetch ArXiv research document retrieval. Provides direct module-level access to ``ArXiv.fetch`` using a fresh ``ArXiv`` instance. Any: Value returned by ``ArXiv.fetch``. |
| `fetch_google_drive()` | `fetch_google_drive( question: str, folder_id: str = 'root', results: int = 10, template: str = 'gdrive-query', mime_type: str = None, mode: str = 'documents' ) -> Any` | Fetch Google Drive document retrieval. Provides direct module-level access to ``GoogleDrive.fetch`` using a fresh ``GoogleDrive`` instance. Any: Value returned by ``GoogleDrive.fetch``. |
| `fetch_wikipedia()` | `fetch_wikipedia( question: str, language: str = None, max_documents: int = None, include_metadata: bool = None ) -> Any` | Fetch Wikipedia document retrieval. Provides direct module-level access to ``Wikipedia.fetch`` using a fresh ``Wikipedia`` instance. Any: Value returned by ``Wikipedia.fetch``. |
| `fetch_news()` | `fetch_news( endpoint: str = 'all', query: str = '', language: str = 'en', categories: str = '', exclude_categories: str = '', locale: str = '', domains: str = '', exclude_domains: str = '', source_ids: str = '', exclude_source_ids: str = '', published_after: str = '', published_before: str = '', published_on: str = '', sort: str = 'published_at', limit: int = 10, page: int = 1, include_similar: bool = True, headlines_per_category: int = 6, time: int = 10, api_key: str = None ) -> Any` | Fetch The News API article retrieval. Provides direct module-level access to ``TheNews.fetch`` using a fresh ``TheNews`` instance. Any: Value returned by ``TheNews.fetch``. |
| `fetch_google_search()` | `fetch_google_search( keywords: str, results: int = 10, start: int = 1, exact_terms: str = '', exclude_terms: str = '', file_type: str = '', date_restrict: str = '', gl: str = '', lr: str = '', safe: str = 'off', search_type: str = '', site_search: str = '', site_search_filter: str = '', sort: str = '', img_size: str = '', img_type: str = '', img_color_type: str = '', img_dominant_color: str = '', time: int = 10, api_key: str = None, cse_id: str = None ) -> Any` | Fetch Google Custom Search retrieval. Provides direct module-level access to ``GoogleSearch.fetch`` using a fresh ``GoogleSearch`` instance. Any: Value returned by ``GoogleSearch.fetch``. |
| `fetch_gov_data()` | `fetch_gov_data( mode: str = 'search', query: str = '', page_size: int = 10, offset_mark: str = '*', sort_field: str = 'score', sort_order: str = 'DESC', package_id: str = '', collection: str = '', start_date: str = '', time: int = 20 ) -> Any` | Fetch Data.gov package and collection retrieval. Provides direct module-level access to ``GovData.fetch`` using a fresh ``GovData`` instance. Any: Value returned by ``GovData.fetch``. |
| `fetch_congress()` | `fetch_congress( mode: str = 'congresses', congress: int = 0, bill_type: str = '', bill_number: int = 0, law_type: str = '', law_number: int = 0, report_type: str = '', report_number: int = 0, offset: int = 0, limit: int = 20, sort: str = 'updateDate+desc', from_date_time: str = '', to_date_time: str = '', conference: bool = False, time: int = 20 ) -> Any` | Fetch Congress.gov legislative data retrieval. Provides direct module-level access to ``Congress.fetch`` using a fresh ``Congress`` instance. Any: Value returned by ``Congress.fetch``. |
| `fetch_internet_archive()` | `fetch_internet_archive( keywords: str, fields: List[str] \| None = None, rows: int = 10, page: int = 1, sort: str = 'downloads desc', media_type: str = '', collection: str = '', time: int = 20 ) -> Any` | Fetch Internet Archive search and metadata retrieval. Provides direct module-level access to ``InternetArchive.fetch`` using a fresh ``InternetArchive`` instance. Any: Value returned by ``InternetArchive.fetch``. |
| `fetch_grokipedia()` | `fetch_grokipedia( mode: str = 'search', query: str = '', page: str = '', limit: int = 12, offset: int = 0, include_content: bool = True ) -> Any` | Fetch Grokipedia search and page retrieval. Provides direct module-level access to ``Grokipedia.fetch`` using a fresh ``Grokipedia`` instance. Any: Value returned by ``Grokipedia.fetch``. |
| `load_arxiv()` | `load_arxiv( question: str ) -> Any` | Load source content. Provides direct module-level access to ``ArXivLoader.load`` using a fresh ``ArXivLoader`` instance. Any: Value returned by ``ArXivLoader.load``. |
| `load_wikipedia()` | `load_wikipedia( question: str ) -> Any` | Load source content. Provides direct module-level access to ``WikiLoader.load`` using a fresh ``WikiLoader`` instance. Any: Value returned by ``WikiLoader.load``. |

### `fetch_arxiv()`

Fetch ArXiv research document retrieval. Provides direct module-level access to ``ArXiv.fetch`` using a fresh ``ArXiv`` instance. Any: Value returned by ``ArXiv.fetch``.

```python
fetch_arxiv( question: str, max_documents: int = None, full_documents: bool = None, include_metadata: bool = None ) -> Any
```

**Implementation target:** `ArXiv.fetch()`

### `fetch_google_drive()`

Fetch Google Drive document retrieval. Provides direct module-level access to ``GoogleDrive.fetch`` using a fresh ``GoogleDrive`` instance. Any: Value returned by ``GoogleDrive.fetch``.

```python
fetch_google_drive( question: str, folder_id: str = 'root', results: int = 10, template: str = 'gdrive-query', mime_type: str = None, mode: str = 'documents' ) -> Any
```

**Implementation target:** `GoogleDrive.fetch()`

### `fetch_wikipedia()`

Fetch Wikipedia document retrieval. Provides direct module-level access to ``Wikipedia.fetch`` using a fresh ``Wikipedia`` instance. Any: Value returned by ``Wikipedia.fetch``.

```python
fetch_wikipedia( question: str, language: str = None, max_documents: int = None, include_metadata: bool = None ) -> Any
```

**Implementation target:** `Wikipedia.fetch()`

### `fetch_news()`

Fetch The News API article retrieval. Provides direct module-level access to ``TheNews.fetch`` using a fresh ``TheNews`` instance. Any: Value returned by ``TheNews.fetch``.

```python
fetch_news( endpoint: str = 'all', query: str = '', language: str = 'en', categories: str = '', exclude_categories: str = '', locale: str = '', domains: str = '', exclude_domains: str = '', source_ids: str = '', exclude_source_ids: str = '', published_after: str = '', published_before: str = '', published_on: str = '', sort: str = 'published_at', limit: int = 10, page: int = 1, include_similar: bool = True, headlines_per_category: int = 6, time: int = 10, api_key: str = None ) -> Any
```

**Implementation target:** `TheNews.fetch()`

### `fetch_google_search()`

Fetch Google Custom Search retrieval. Provides direct module-level access to ``GoogleSearch.fetch`` using a fresh ``GoogleSearch`` instance. Any: Value returned by ``GoogleSearch.fetch``.

```python
fetch_google_search( keywords: str, results: int = 10, start: int = 1, exact_terms: str = '', exclude_terms: str = '', file_type: str = '', date_restrict: str = '', gl: str = '', lr: str = '', safe: str = 'off', search_type: str = '', site_search: str = '', site_search_filter: str = '', sort: str = '', img_size: str = '', img_type: str = '', img_color_type: str = '', img_dominant_color: str = '', time: int = 10, api_key: str = None, cse_id: str = None ) -> Any
```

**Implementation target:** `GoogleSearch.fetch()`

### `fetch_gov_data()`

Fetch Data.gov package and collection retrieval. Provides direct module-level access to ``GovData.fetch`` using a fresh ``GovData`` instance. Any: Value returned by ``GovData.fetch``.

```python
fetch_gov_data( mode: str = 'search', query: str = '', page_size: int = 10, offset_mark: str = '*', sort_field: str = 'score', sort_order: str = 'DESC', package_id: str = '', collection: str = '', start_date: str = '', time: int = 20 ) -> Any
```

**Implementation target:** `GovData.fetch()`

### `fetch_congress()`

Fetch Congress.gov legislative data retrieval. Provides direct module-level access to ``Congress.fetch`` using a fresh ``Congress`` instance. Any: Value returned by ``Congress.fetch``.

```python
fetch_congress( mode: str = 'congresses', congress: int = 0, bill_type: str = '', bill_number: int = 0, law_type: str = '', law_number: int = 0, report_type: str = '', report_number: int = 0, offset: int = 0, limit: int = 20, sort: str = 'updateDate+desc', from_date_time: str = '', to_date_time: str = '', conference: bool = False, time: int = 20 ) -> Any
```

**Implementation target:** `Congress.fetch()`

### `fetch_internet_archive()`

Fetch Internet Archive search and metadata retrieval. Provides direct module-level access to ``InternetArchive.fetch`` using a fresh ``InternetArchive`` instance. Any: Value returned by ``InternetArchive.fetch``.

```python
fetch_internet_archive( keywords: str, fields: List[str] | None = None, rows: int = 10, page: int = 1, sort: str = 'downloads desc', media_type: str = '', collection: str = '', time: int = 20 ) -> Any
```

**Implementation target:** `InternetArchive.fetch()`

### `fetch_grokipedia()`

Fetch Grokipedia search and page retrieval. Provides direct module-level access to ``Grokipedia.fetch`` using a fresh ``Grokipedia`` instance. Any: Value returned by ``Grokipedia.fetch``.

```python
fetch_grokipedia( mode: str = 'search', query: str = '', page: str = '', limit: int = 12, offset: int = 0, include_content: bool = True ) -> Any
```

**Implementation target:** `Grokipedia.fetch()`

### `load_arxiv()`

Load source content. Provides direct module-level access to ``ArXivLoader.load`` using a fresh ``ArXivLoader`` instance. Any: Value returned by ``ArXivLoader.load``.

```python
load_arxiv( question: str ) -> Any
```

**Implementation target:** `ArXivLoader.load()`

### `load_wikipedia()`

Load source content. Provides direct module-level access to ``WikiLoader.load`` using a fresh ``WikiLoader`` instance. Any: Value returned by ``WikiLoader.load``.

```python
load_wikipedia( question: str ) -> Any
```

**Implementation target:** `WikiLoader.load()`

## Astronomical

| Function | Signature | Purpose |
|---|---|---|
| `fetch_naval_observatory()` | `fetch_naval_observatory( mode: str = 'celnav', date_value: str = '', time_value: str = '', latitude: float = 0.0, longitude: float = 0.0, location_label: str = '', time: int = 20 ) -> Any` | Fetch U.S. Naval Observatory celestial-navigation data. Provides direct module-level access to ``NavalObservatory.fetch`` using a fresh ``NavalObservatory`` instance. Any: Value returned by ``NavalObservatory.fetch``. |
| `fetch_satellite_center()` | `fetch_satellite_center( mode: str = 'observatories', query: str = '', start_time: str = '', end_time: str = '', coordinate_systems: str = 'gse', resolution_factor: int = 1, time: int = 20 ) -> Any` | Fetch SSC satellite observatory, ground-station, and location data. Provides direct module-level access to ``SatelliteCenter.fetch`` using a fresh ``SatelliteCenter`` instance. Any: Value returned by ``SatelliteCenter.fetch``. |
| `fetch_nearby_objects()` | `fetch_nearby_objects( mode: str = 'close_approaches', start_date: str = '', end_date: str = '', query: str = '', query_type: str = 'sstr', dist_max: str = '10LD', body: str = 'Earth', sort: str = 'date', limit: int = 20, dv: float = 6.0, dur: int = 360, stay: int = 8, launch: str = '2020-2045', h: float = 26.0, occ: int = 7, include_physical: bool = True, include_close_approaches: bool = True, ca_body: str = 'Earth', include_discovery: bool = True, time: int = 20 ) -> Any` | Fetch JPL SSD and CNEOS near-Earth object data. Provides direct module-level access to ``NearbyObjects.fetch`` using a fresh ``NearbyObjects`` instance. Any: Value returned by ``NearbyObjects.fetch``. |
| `fetch_open_science()` | `fetch_open_science( mode: str = 'dataset', query: str = '', accession: str = '', format_value: str = 'json', time: int = 20 ) -> Any` | Fetch NASA Open Science Data Repository resources. Provides direct module-level access to ``OpenScience.fetch`` using a fresh ``OpenScience`` instance. Any: Value returned by ``OpenScience.fetch``. |
| `fetch_space_weather()` | `fetch_space_weather( mode: str = 'cme', start_date: str = '', end_date: str = '', time: int = 20, location: str = 'ALL', catalog: str = 'ALL', notification_type: str = 'all', most_accurate_only: bool = True, complete_entry_only: bool = True, speed: int = 0, half_angle: int = 0, keyword: str = '', api_key: str = None ) -> Any` | Fetch NASA DONKI space weather endpoints. Provides direct module-level access to ``SpaceWeather.fetch`` using a fresh ``SpaceWeather`` instance. Any: Value returned by ``SpaceWeather.fetch``. |
| `fetch_astro_catalog()` | `fetch_astro_catalog( mode: str = 'object_query', query: str = '', quantity: str = '', attributes: str = '', arguments: str = '', ra: str = '', dec: str = '', radius: int = 2, data_format: str = 'json', time: int = 20 ) -> Any` | Fetch Open Astronomy Catalog queries. Provides direct module-level access to ``AstroCatalog.fetch`` using a fresh ``AstroCatalog`` instance. Any: Value returned by ``AstroCatalog.fetch``. |
| `fetch_astro_query()` | `fetch_astro_query( mode: str = 'object_search', query: str = '', ra: str = '', dec: str = '', radius: float = 0.5, radius_unit: str = 'deg', row_limit: int = 100 ) -> Any` | Fetch Simbad and astronomy object search operations. Provides direct module-level access to ``AstroQuery.fetch`` using a fresh ``AstroQuery`` instance. Any: Value returned by ``AstroQuery.fetch``. |
| `fetch_star_map()` | `fetch_star_map( mode: str = 'object_link', query: str = '', ra: float = 0.0, dec: float = 0.0, zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, time: int = 20 ) -> Any` | Fetch astronomical object map links and imagery. Provides direct module-level access to ``StarMap.fetch`` using a fresh ``StarMap`` instance. Any: Value returned by ``StarMap.fetch``. |
| `fetch_star_chart()` | `fetch_star_chart( mode: str = 'object_chart', query: str = '', ra: float = 0.0, dec: float = 0.0, zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, width: int = 900, height: int = 450, magnitude: float = 7.5, time: int = 20 ) -> Any` | Fetch static star chart and coordinate chart generation. Provides direct module-level access to ``StarChart.fetch`` using a fresh ``StarChart`` instance. Any: Value returned by ``StarChart.fetch``. |
| `fetch_open_sky()` | `fetch_open_sky( mode: str = 'states_bbox', icao24: str = '', airport: str = '', begin: int = None, end: int = None, time_value: int = None, lamin: float \| None = None, lomin: float \| None = None, lamax: float \| None = None, lomax: float \| None = None, extended: bool = False, client_id: str = None, client_secret: str = None, time: int = 20 ) -> Any` | Fetch OpenSky Network aircraft, airport, and state-vector data. Provides direct module-level access to ``OpenSky.fetch`` using a fresh ``OpenSky`` instance. Any: Value returned by ``OpenSky.fetch``. |

### `fetch_naval_observatory()`

Fetch U.S. Naval Observatory celestial-navigation data. Provides direct module-level access to ``NavalObservatory.fetch`` using a fresh ``NavalObservatory`` instance. Any: Value returned by ``NavalObservatory.fetch``.

```python
fetch_naval_observatory( mode: str = 'celnav', date_value: str = '', time_value: str = '', latitude: float = 0.0, longitude: float = 0.0, location_label: str = '', time: int = 20 ) -> Any
```

**Implementation target:** `NavalObservatory.fetch()`

### `fetch_satellite_center()`

Fetch SSC satellite observatory, ground-station, and location data. Provides direct module-level access to ``SatelliteCenter.fetch`` using a fresh ``SatelliteCenter`` instance. Any: Value returned by ``SatelliteCenter.fetch``.

```python
fetch_satellite_center( mode: str = 'observatories', query: str = '', start_time: str = '', end_time: str = '', coordinate_systems: str = 'gse', resolution_factor: int = 1, time: int = 20 ) -> Any
```

**Implementation target:** `SatelliteCenter.fetch()`

### `fetch_nearby_objects()`

Fetch JPL SSD and CNEOS near-Earth object data. Provides direct module-level access to ``NearbyObjects.fetch`` using a fresh ``NearbyObjects`` instance. Any: Value returned by ``NearbyObjects.fetch``.

```python
fetch_nearby_objects( mode: str = 'close_approaches', start_date: str = '', end_date: str = '', query: str = '', query_type: str = 'sstr', dist_max: str = '10LD', body: str = 'Earth', sort: str = 'date', limit: int = 20, dv: float = 6.0, dur: int = 360, stay: int = 8, launch: str = '2020-2045', h: float = 26.0, occ: int = 7, include_physical: bool = True, include_close_approaches: bool = True, ca_body: str = 'Earth', include_discovery: bool = True, time: int = 20 ) -> Any
```

**Implementation target:** `NearbyObjects.fetch()`

### `fetch_open_science()`

Fetch NASA Open Science Data Repository resources. Provides direct module-level access to ``OpenScience.fetch`` using a fresh ``OpenScience`` instance. Any: Value returned by ``OpenScience.fetch``.

```python
fetch_open_science( mode: str = 'dataset', query: str = '', accession: str = '', format_value: str = 'json', time: int = 20 ) -> Any
```

**Implementation target:** `OpenScience.fetch()`

### `fetch_space_weather()`

Fetch NASA DONKI space weather endpoints. Provides direct module-level access to ``SpaceWeather.fetch`` using a fresh ``SpaceWeather`` instance. Any: Value returned by ``SpaceWeather.fetch``.

```python
fetch_space_weather( mode: str = 'cme', start_date: str = '', end_date: str = '', time: int = 20, location: str = 'ALL', catalog: str = 'ALL', notification_type: str = 'all', most_accurate_only: bool = True, complete_entry_only: bool = True, speed: int = 0, half_angle: int = 0, keyword: str = '', api_key: str = None ) -> Any
```

**Implementation target:** `SpaceWeather.fetch()`

### `fetch_astro_catalog()`

Fetch Open Astronomy Catalog queries. Provides direct module-level access to ``AstroCatalog.fetch`` using a fresh ``AstroCatalog`` instance. Any: Value returned by ``AstroCatalog.fetch``.

```python
fetch_astro_catalog( mode: str = 'object_query', query: str = '', quantity: str = '', attributes: str = '', arguments: str = '', ra: str = '', dec: str = '', radius: int = 2, data_format: str = 'json', time: int = 20 ) -> Any
```

**Implementation target:** `AstroCatalog.fetch()`

### `fetch_astro_query()`

Fetch Simbad and astronomy object search operations. Provides direct module-level access to ``AstroQuery.fetch`` using a fresh ``AstroQuery`` instance. Any: Value returned by ``AstroQuery.fetch``.

```python
fetch_astro_query( mode: str = 'object_search', query: str = '', ra: str = '', dec: str = '', radius: float = 0.5, radius_unit: str = 'deg', row_limit: int = 100 ) -> Any
```

**Implementation target:** `AstroQuery.fetch()`

### `fetch_star_map()`

Fetch astronomical object map links and imagery. Provides direct module-level access to ``StarMap.fetch`` using a fresh ``StarMap`` instance. Any: Value returned by ``StarMap.fetch``.

```python
fetch_star_map( mode: str = 'object_link', query: str = '', ra: float = 0.0, dec: float = 0.0, zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, time: int = 20 ) -> Any
```

**Implementation target:** `StarMap.fetch()`

### `fetch_star_chart()`

Fetch static star chart and coordinate chart generation. Provides direct module-level access to ``StarChart.fetch`` using a fresh ``StarChart`` instance. Any: Value returned by ``StarChart.fetch``.

```python
fetch_star_chart( mode: str = 'object_chart', query: str = '', ra: float = 0.0, dec: float = 0.0, zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True, show_const_names: bool = False, width: int = 900, height: int = 450, magnitude: float = 7.5, time: int = 20 ) -> Any
```

**Implementation target:** `StarChart.fetch()`

### `fetch_open_sky()`

Fetch OpenSky Network aircraft, airport, and state-vector data. Provides direct module-level access to ``OpenSky.fetch`` using a fresh ``OpenSky`` instance. Any: Value returned by ``OpenSky.fetch``.

```python
fetch_open_sky( mode: str = 'states_bbox', icao24: str = '', airport: str = '', begin: int = None, end: int = None, time_value: int = None, lamin: float | None = None, lomin: float | None = None, lamax: float | None = None, lomax: float | None = None, extended: bool = False, client_id: str = None, client_secret: str = None, time: int = 20 ) -> Any
```

**Implementation target:** `OpenSky.fetch()`

## Cloud

| Function | Signature | Purpose |
|---|---|---|
| `load_google_drive_file()` | `load_google_drive_file( file_id: str, recursive: bool = False ) -> Any` | Load a provider file. Provides direct module-level access to ``GoogleDriveLoader.load_file`` using a fresh ``GoogleDriveLoader`` instance. Any: Value returned by ``GoogleDriveLoader.load_file``. |
| `load_google_drive_folder()` | `load_google_drive_folder( folder_id: str, recursive: bool = False ) -> Any` | Load provider folder content. Provides direct module-level access to ``GoogleDriveLoader.load_folder`` using a fresh ``GoogleDriveLoader`` instance. Any: Value returned by ``GoogleDriveLoader.load_folder``. |
| `load_onedrive()` | `load_onedrive( drive_id: str, folder_path: Optional[str] = None, object_ids: Optional[List[str]] = None, auth_with_token: bool = True ) -> Any` | Load source content. Provides direct module-level access to ``OneDriveDocLoader.load`` using a fresh ``OneDriveDocLoader`` instance. Any: Value returned by ``OneDriveDocLoader.load``. |
| `load_google_cloud_file()` | `load_google_cloud_file( project_name: str, bucket: str, blob: str ) -> Any` | Load source content. Provides direct module-level access to ``GoogleCloudFileLoader.load`` using a fresh ``GoogleCloudFileLoader`` instance. Any: Value returned by ``GoogleCloudFileLoader.load``. |
| `load_aws_file()` | `load_aws_file( bucket: str, key: str, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None ) -> Any` | Load source content. Provides direct module-level access to ``AwsFileLoader.load`` using a fresh ``AwsFileLoader`` instance. Any: Value returned by ``AwsFileLoader.load``. |
| `load_google_speech_to_text()` | `load_google_speech_to_text( project_id: str, file_path: str, config: Optional[Dict[str, Any]] = None ) -> Any` | Load source content. Provides direct module-level access to ``GoogleSpeechToTextLoader.load`` using a fresh ``GoogleSpeechToTextLoader`` instance. Any: Value returned by ``GoogleSpeechToTextLoader.load``. |
| `load_google_bucket()` | `load_google_bucket( project_name: str, bucket: str, prefix: Optional[str] = None, continue_on_failure: bool = False ) -> Any` | Load source content. Provides direct module-level access to ``GoogleBucketLoader.load`` using a fresh ``GoogleBucketLoader`` instance. Any: Value returned by ``GoogleBucketLoader.load``. |
| `load_aws_bucket()` | `load_aws_bucket( bucket: str, prefix: Optional[str] = None, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None, endpoint_url: Optional[str] = None ) -> Any` | Load source content. Provides direct module-level access to ``AwsBucketLoader.load`` using a fresh ``AwsBucketLoader`` instance. Any: Value returned by ``AwsBucketLoader.load``. |

### `load_google_drive_file()`

Load a provider file. Provides direct module-level access to ``GoogleDriveLoader.load_file`` using a fresh ``GoogleDriveLoader`` instance. Any: Value returned by ``GoogleDriveLoader.load_file``.

```python
load_google_drive_file( file_id: str, recursive: bool = False ) -> Any
```

**Implementation target:** `GoogleDriveLoader.load_file()`

### `load_google_drive_folder()`

Load provider folder content. Provides direct module-level access to ``GoogleDriveLoader.load_folder`` using a fresh ``GoogleDriveLoader`` instance. Any: Value returned by ``GoogleDriveLoader.load_folder``.

```python
load_google_drive_folder( folder_id: str, recursive: bool = False ) -> Any
```

**Implementation target:** `GoogleDriveLoader.load_folder()`

### `load_onedrive()`

Load source content. Provides direct module-level access to ``OneDriveDocLoader.load`` using a fresh ``OneDriveDocLoader`` instance. Any: Value returned by ``OneDriveDocLoader.load``.

```python
load_onedrive( drive_id: str, folder_path: Optional[str] = None, object_ids: Optional[List[str]] = None, auth_with_token: bool = True ) -> Any
```

**Implementation target:** `OneDriveDocLoader.load()`

### `load_google_cloud_file()`

Load source content. Provides direct module-level access to ``GoogleCloudFileLoader.load`` using a fresh ``GoogleCloudFileLoader`` instance. Any: Value returned by ``GoogleCloudFileLoader.load``.

```python
load_google_cloud_file( project_name: str, bucket: str, blob: str ) -> Any
```

**Implementation target:** `GoogleCloudFileLoader.load()`

### `load_aws_file()`

Load source content. Provides direct module-level access to ``AwsFileLoader.load`` using a fresh ``AwsFileLoader`` instance. Any: Value returned by ``AwsFileLoader.load``.

```python
load_aws_file( bucket: str, key: str, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None ) -> Any
```

**Implementation target:** `AwsFileLoader.load()`

### `load_google_speech_to_text()`

Load source content. Provides direct module-level access to ``GoogleSpeechToTextLoader.load`` using a fresh ``GoogleSpeechToTextLoader`` instance. Any: Value returned by ``GoogleSpeechToTextLoader.load``.

```python
load_google_speech_to_text( project_id: str, file_path: str, config: Optional[Dict[str, Any]] = None ) -> Any
```

**Implementation target:** `GoogleSpeechToTextLoader.load()`

### `load_google_bucket()`

Load source content. Provides direct module-level access to ``GoogleBucketLoader.load`` using a fresh ``GoogleBucketLoader`` instance. Any: Value returned by ``GoogleBucketLoader.load``.

```python
load_google_bucket( project_name: str, bucket: str, prefix: Optional[str] = None, continue_on_failure: bool = False ) -> Any
```

**Implementation target:** `GoogleBucketLoader.load()`

### `load_aws_bucket()`

Load source content. Provides direct module-level access to ``AwsBucketLoader.load`` using a fresh ``AwsBucketLoader`` instance. Any: Value returned by ``AwsBucketLoader.load``.

```python
load_aws_bucket( bucket: str, prefix: Optional[str] = None, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None, endpoint_url: Optional[str] = None ) -> Any
```

**Implementation target:** `AwsBucketLoader.load()`

## Demographic

| Function | Signature | Purpose |
|---|---|---|
| `fetch_census_data()` | `fetch_census_data( mode: str = 'variables', year: str = '2022', dataset: str = 'acs/acs5', fields: str = 'NAME,B01001_001E', geography_for: str = 'state:*', geography_in: str = '', predicates: str = '', time: int = 20 ) -> Any` | Fetch U.S. Census dataset and variable retrieval. Provides direct module-level access to ``CensusData.fetch`` using a fresh ``CensusData`` instance. Any: Value returned by ``CensusData.fetch``. |
| `fetch_socrata()` | `fetch_socrata( mode: str = 'rows', domain: str = 'data.cdc.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any` | Fetch Socrata dataset metadata and row retrieval. Provides direct module-level access to ``Socrata.fetch`` using a fresh ``Socrata`` instance. Any: Value returned by ``Socrata.fetch``. |
| `fetch_united_nations()` | `fetch_united_nations( mode: str = 'datasets', query_path: str = '', time: int = 20 ) -> Any` | Fetch United Nations SDMX dataset and query retrieval. Provides direct module-level access to ``UnitedNations.fetch`` using a fresh ``UnitedNations`` instance. Any: Value returned by ``UnitedNations.fetch``. |
| `fetch_world_population()` | `fetch_world_population( mode: str = 'catalog', query: str = '', asset_path: str = '', page: int = 1, page_size: int = 25, time: int = 20 ) -> Any` | Fetch WorldPop catalog and raster metadata retrieval. Provides direct module-level access to ``WorldPopulation.fetch`` using a fresh ``WorldPopulation`` instance. Any: Value returned by ``WorldPopulation.fetch``. |
| `load_open_city()` | `load_open_city( city_id: str, dataset_id: str, limit: int = 100 ) -> Any` | Load source content. Provides direct module-level access to ``OpenCityLoader.load`` using a fresh ``OpenCityLoader`` instance. Any: Value returned by ``OpenCityLoader.load``. |

### `fetch_census_data()`

Fetch U.S. Census dataset and variable retrieval. Provides direct module-level access to ``CensusData.fetch`` using a fresh ``CensusData`` instance. Any: Value returned by ``CensusData.fetch``.

```python
fetch_census_data( mode: str = 'variables', year: str = '2022', dataset: str = 'acs/acs5', fields: str = 'NAME,B01001_001E', geography_for: str = 'state:*', geography_in: str = '', predicates: str = '', time: int = 20 ) -> Any
```

**Implementation target:** `CensusData.fetch()`

### `fetch_socrata()`

Fetch Socrata dataset metadata and row retrieval. Provides direct module-level access to ``Socrata.fetch`` using a fresh ``Socrata`` instance. Any: Value returned by ``Socrata.fetch``.

```python
fetch_socrata( mode: str = 'rows', domain: str = 'data.cdc.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

**Implementation target:** `Socrata.fetch()`

### `fetch_united_nations()`

Fetch United Nations SDMX dataset and query retrieval. Provides direct module-level access to ``UnitedNations.fetch`` using a fresh ``UnitedNations`` instance. Any: Value returned by ``UnitedNations.fetch``.

```python
fetch_united_nations( mode: str = 'datasets', query_path: str = '', time: int = 20 ) -> Any
```

**Implementation target:** `UnitedNations.fetch()`

### `fetch_world_population()`

Fetch WorldPop catalog and raster metadata retrieval. Provides direct module-level access to ``WorldPopulation.fetch`` using a fresh ``WorldPopulation`` instance. Any: Value returned by ``WorldPopulation.fetch``.

```python
fetch_world_population( mode: str = 'catalog', query: str = '', asset_path: str = '', page: int = 1, page_size: int = 25, time: int = 20 ) -> Any
```

**Implementation target:** `WorldPopulation.fetch()`

### `load_open_city()`

Load source content. Provides direct module-level access to ``OpenCityLoader.load`` using a fresh ``OpenCityLoader`` instance. Any: Value returned by ``OpenCityLoader.load``.

```python
load_open_city( city_id: str, dataset_id: str, limit: int = 100 ) -> Any
```

**Implementation target:** `OpenCityLoader.load()`

## Documents

| Function | Signature | Purpose |
|---|---|---|
| `load_text()` | `load_text( path: str, encoding: Optional[str] = None ) -> Any` | Load source content. Provides direct module-level access to ``TextLoader.load`` using a fresh ``TextLoader`` instance. Any: Value returned by ``TextLoader.load``. |
| `load_csv()` | `load_csv( path: str, encoding: Optional[str] = 'utf-8', source_column: Optional[str] = None, delimiter: str = ',', quotechar: str = '"' ) -> Any` | Load source content. Provides direct module-level access to ``CsvLoader.load`` using a fresh ``CsvLoader`` instance. Any: Value returned by ``CsvLoader.load``. |
| `read_pdf()` | `read_pdf( path: str, mode: str = 'single' ) -> Any` | Load source content. Provides direct module-level access to ``PdfReader.load`` using a fresh ``PdfReader`` instance. Any: Value returned by ``PdfReader.load``. |
| `load_pdf()` | `load_pdf( path: str, mode: str = 'single', extract: str = 'plain', include: bool = False, format: str = 'markdown-img', size: int = 1000, overlap: int = 150, has_tables: bool = True ) -> Any` | Load source content. Provides direct module-level access to ``PdfLoader.load`` using a fresh ``PdfLoader`` instance. Any: Value returned by ``PdfLoader.load``. |
| `load_excel()` | `load_excel( path: str, mode: str = 'elements', has_headers: bool = True ) -> Any` | Load source content. Provides direct module-level access to ``ExcelLoader.load`` using a fresh ``ExcelLoader`` instance. Any: Value returned by ``ExcelLoader.load``. |
| `load_word()` | `load_word( path: str ) -> Any` | Load source content. Provides direct module-level access to ``WordLoader.load`` using a fresh ``WordLoader`` instance. Any: Value returned by ``WordLoader.load``. |
| `load_markdown()` | `load_markdown( path: str ) -> Any` | Load source content. Provides direct module-level access to ``MarkdownLoader.load`` using a fresh ``MarkdownLoader`` instance. Any: Value returned by ``MarkdownLoader.load``. |
| `load_html()` | `load_html( path: str ) -> Any` | Load source content. Provides direct module-level access to ``HtmlLoader.load`` using a fresh ``HtmlLoader`` instance. Any: Value returned by ``HtmlLoader.load``. |
| `load_outlook()` | `load_outlook( path: str ) -> Any` | Load source content. Provides direct module-level access to ``OutlookLoader.load`` using a fresh ``OutlookLoader`` instance. Any: Value returned by ``OutlookLoader.load``. |
| `load_spfx()` | `load_spfx( library_id: str ) -> Any` | Load source content. Provides direct module-level access to ``SpfxLoader.load`` using a fresh ``SpfxLoader`` instance. Any: Value returned by ``SpfxLoader.load``. |
| `load_spfx_folder()` | `load_spfx_folder( library_id: str, folder_id: str ) -> Any` | Load provider folder content. Provides direct module-level access to ``SpfxLoader.load_folder`` using a fresh ``SpfxLoader`` instance. Any: Value returned by ``SpfxLoader.load_folder``. |
| `load_powerpoint()` | `load_powerpoint( path: str, mode: str = 'single' ) -> Any` | Load source content. Provides direct module-level access to ``PowerPointLoader.load`` using a fresh ``PowerPointLoader`` instance. Any: Value returned by ``PowerPointLoader.load``. |
| `load_powerpoint_multiple()` | `load_powerpoint_multiple( path: str ) -> Any` | Load multiple presentation elements. Provides direct module-level access to ``PowerPointLoader.load_multiple`` using a fresh ``PowerPointLoader`` instance. Any: Value returned by ``PowerPointLoader.load_multiple``. |
| `load_email()` | `load_email( path: str, mode: str = 'single', attachments: bool = True ) -> Any` | Load source content. Provides direct module-level access to ``EmailLoader.load`` using a fresh ``EmailLoader`` instance. Any: Value returned by ``EmailLoader.load``. |
| `load_json()` | `load_json( filepath: str, is_text: bool = True, is_lines: bool = False ) -> Any` | Load source content. Provides direct module-level access to ``JsonLoader.load`` using a fresh ``JsonLoader`` instance. Any: Value returned by ``JsonLoader.load``. |
| `load_xml()` | `load_xml( filepath: str ) -> Any` | Load source content. Provides direct module-level access to ``XmlLoader.load`` using a fresh ``XmlLoader`` instance. Any: Value returned by ``XmlLoader.load``. |
| `load_xml_tree()` | `load_xml_tree( filepath: str ) -> Any` | Parse an XML element tree. Provides direct module-level access to ``XmlLoader.load_tree`` using a fresh ``XmlLoader`` instance. Any: Value returned by ``XmlLoader.load_tree``. |
| `load_jupyter_notebook()` | `load_jupyter_notebook( path: str, include_outputs: bool = False, max_output_length: int = 10, remove_newline: bool = False, traceback: bool = False ) -> Any` | Load source content. Provides direct module-level access to ``JupyterNotebookLoader.load`` using a fresh ``JupyterNotebookLoader`` instance. Any: Value returned by ``JupyterNotebookLoader.load``. |

### `load_text()`

Load source content. Provides direct module-level access to ``TextLoader.load`` using a fresh ``TextLoader`` instance. Any: Value returned by ``TextLoader.load``.

```python
load_text( path: str, encoding: Optional[str] = None ) -> Any
```

**Implementation target:** `TextLoader.load()`

### `load_csv()`

Load source content. Provides direct module-level access to ``CsvLoader.load`` using a fresh ``CsvLoader`` instance. Any: Value returned by ``CsvLoader.load``.

```python
load_csv( path: str, encoding: Optional[str] = 'utf-8', source_column: Optional[str] = None, delimiter: str = ',', quotechar: str = '"' ) -> Any
```

**Implementation target:** `CsvLoader.load()`

### `read_pdf()`

Load source content. Provides direct module-level access to ``PdfReader.load`` using a fresh ``PdfReader`` instance. Any: Value returned by ``PdfReader.load``.

```python
read_pdf( path: str, mode: str = 'single' ) -> Any
```

**Implementation target:** `PdfReader.load()`

### `load_pdf()`

Load source content. Provides direct module-level access to ``PdfLoader.load`` using a fresh ``PdfLoader`` instance. Any: Value returned by ``PdfLoader.load``.

```python
load_pdf( path: str, mode: str = 'single', extract: str = 'plain', include: bool = False, format: str = 'markdown-img', size: int = 1000, overlap: int = 150, has_tables: bool = True ) -> Any
```

**Implementation target:** `PdfLoader.load()`

### `load_excel()`

Load source content. Provides direct module-level access to ``ExcelLoader.load`` using a fresh ``ExcelLoader`` instance. Any: Value returned by ``ExcelLoader.load``.

```python
load_excel( path: str, mode: str = 'elements', has_headers: bool = True ) -> Any
```

**Implementation target:** `ExcelLoader.load()`

### `load_word()`

Load source content. Provides direct module-level access to ``WordLoader.load`` using a fresh ``WordLoader`` instance. Any: Value returned by ``WordLoader.load``.

```python
load_word( path: str ) -> Any
```

**Implementation target:** `WordLoader.load()`

### `load_markdown()`

Load source content. Provides direct module-level access to ``MarkdownLoader.load`` using a fresh ``MarkdownLoader`` instance. Any: Value returned by ``MarkdownLoader.load``.

```python
load_markdown( path: str ) -> Any
```

**Implementation target:** `MarkdownLoader.load()`

### `load_html()`

Load source content. Provides direct module-level access to ``HtmlLoader.load`` using a fresh ``HtmlLoader`` instance. Any: Value returned by ``HtmlLoader.load``.

```python
load_html( path: str ) -> Any
```

**Implementation target:** `HtmlLoader.load()`

### `load_outlook()`

Load source content. Provides direct module-level access to ``OutlookLoader.load`` using a fresh ``OutlookLoader`` instance. Any: Value returned by ``OutlookLoader.load``.

```python
load_outlook( path: str ) -> Any
```

**Implementation target:** `OutlookLoader.load()`

### `load_spfx()`

Load source content. Provides direct module-level access to ``SpfxLoader.load`` using a fresh ``SpfxLoader`` instance. Any: Value returned by ``SpfxLoader.load``.

```python
load_spfx( library_id: str ) -> Any
```

**Implementation target:** `SpfxLoader.load()`

### `load_spfx_folder()`

Load provider folder content. Provides direct module-level access to ``SpfxLoader.load_folder`` using a fresh ``SpfxLoader`` instance. Any: Value returned by ``SpfxLoader.load_folder``.

```python
load_spfx_folder( library_id: str, folder_id: str ) -> Any
```

**Implementation target:** `SpfxLoader.load_folder()`

### `load_powerpoint()`

Load source content. Provides direct module-level access to ``PowerPointLoader.load`` using a fresh ``PowerPointLoader`` instance. Any: Value returned by ``PowerPointLoader.load``.

```python
load_powerpoint( path: str, mode: str = 'single' ) -> Any
```

**Implementation target:** `PowerPointLoader.load()`

### `load_powerpoint_multiple()`

Load multiple presentation elements. Provides direct module-level access to ``PowerPointLoader.load_multiple`` using a fresh ``PowerPointLoader`` instance. Any: Value returned by ``PowerPointLoader.load_multiple``.

```python
load_powerpoint_multiple( path: str ) -> Any
```

**Implementation target:** `PowerPointLoader.load_multiple()`

### `load_email()`

Load source content. Provides direct module-level access to ``EmailLoader.load`` using a fresh ``EmailLoader`` instance. Any: Value returned by ``EmailLoader.load``.

```python
load_email( path: str, mode: str = 'single', attachments: bool = True ) -> Any
```

**Implementation target:** `EmailLoader.load()`

### `load_json()`

Load source content. Provides direct module-level access to ``JsonLoader.load`` using a fresh ``JsonLoader`` instance. Any: Value returned by ``JsonLoader.load``.

```python
load_json( filepath: str, is_text: bool = True, is_lines: bool = False ) -> Any
```

**Implementation target:** `JsonLoader.load()`

### `load_xml()`

Load source content. Provides direct module-level access to ``XmlLoader.load`` using a fresh ``XmlLoader`` instance. Any: Value returned by ``XmlLoader.load``.

```python
load_xml( filepath: str ) -> Any
```

**Implementation target:** `XmlLoader.load()`

### `load_xml_tree()`

Parse an XML element tree. Provides direct module-level access to ``XmlLoader.load_tree`` using a fresh ``XmlLoader`` instance. Any: Value returned by ``XmlLoader.load_tree``.

```python
load_xml_tree( filepath: str ) -> Any
```

**Implementation target:** `XmlLoader.load_tree()`

### `load_jupyter_notebook()`

Load source content. Provides direct module-level access to ``JupyterNotebookLoader.load`` using a fresh ``JupyterNotebookLoader`` instance. Any: Value returned by ``JupyterNotebookLoader.load``.

```python
load_jupyter_notebook( path: str, include_outputs: bool = False, max_output_length: int = 10, remove_newline: bool = False, traceback: bool = False ) -> Any
```

**Implementation target:** `JupyterNotebookLoader.load()`

## Environmental

| Function | Signature | Purpose |
|---|---|---|
| `fetch_google_weather_current()` | `fetch_google_weather_current( address: str, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any` | Fetch current. Provides direct module-level access to ``GoogleWeather.fetch_current`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_current``. |
| `fetch_google_weather_hourly_forecast()` | `fetch_google_weather_hourly_forecast( address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any` | Fetch hourly forecast. Provides direct module-level access to ``GoogleWeather.fetch_hourly_forecast`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_hourly_forecast``. |
| `fetch_google_weather_daily_forecast()` | `fetch_google_weather_daily_forecast( address: str, days: int = 5, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any` | Fetch daily forecast. Provides direct module-level access to ``GoogleWeather.fetch_daily_forecast`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_daily_forecast``. |
| `fetch_google_weather_hourly_history()` | `fetch_google_weather_hourly_history( address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any` | Fetch hourly history. Provides direct module-level access to ``GoogleWeather.fetch_hourly_history`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_hourly_history``. |
| `fetch_google_weather_alerts()` | `fetch_google_weather_alerts( address: str, language_code: str = 'en', time: int = 10 ) -> Any` | Fetch alerts. Provides direct module-level access to ``GoogleWeather.fetch_alerts`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_alerts``. |
| `fetch_earth_observatory()` | `fetch_earth_observatory( mode: str = 'events', status: str = 'open', category: str = '', source: str = '', limit: int = 20, days: int = 30, start_date: str = '', end_date: str = '', time: int = 20 ) -> Any` | Fetch NASA EONET events, categories, sources, and layers. Provides direct module-level access to ``EarthObservatory.fetch`` using a fresh ``EarthObservatory`` instance. Any: Value returned by ``EarthObservatory.fetch``. |
| `fetch_open_weather()` | `fetch_open_weather( location: str, mode: str = 'current', zone: str = 'auto', forecast_days: int = 7, past_days: int = 0, count: int = 10 ) -> Any` | Fetch Open-Meteo current and forecast weather retrieval. Provides direct module-level access to ``OpenWeather.fetch`` using a fresh ``OpenWeather`` instance. Any: Value returned by ``OpenWeather.fetch``. |
| `fetch_historical_weather()` | `fetch_historical_weather( location: str, date: dt.date, zone: str = 'auto', count: int = 10 ) -> Any` | Fetch historical weather archive retrieval. Provides direct module-level access to ``HistoricalWeather.fetch`` using a fresh ``HistoricalWeather`` instance. Any: Value returned by ``HistoricalWeather.fetch``. |
| `fetch_usgs_earthquakes()` | `fetch_usgs_earthquakes( mode: str = 'feed', feed: str = 'all_day.geojson', start_date: str = '', end_date: str = '', min_magnitude: float = 1.0, max_magnitude: float = 10.0, limit: int = 25, order_by: str = 'time', event_type: str = 'earthquake', latitude: float \| None = None, longitude: float \| None = None, max_radius_km: float \| None = None, time: int = 20 ) -> Any` | Fetch USGS earthquake feed and query retrieval. Provides direct module-level access to ``USGSEarthquakes.fetch`` using a fresh ``USGSEarthquakes`` instance. Any: Value returned by ``USGSEarthquakes.fetch``. |
| `fetch_usgs_water_data()` | `fetch_usgs_water_data( mode: str = 'monitoring-locations', monitoring_location_id: str = '', state_code: str = '', county_code: str = '', site_type: str = '', parameter_code: str = '', limit: int = 25, time: int = 20 ) -> Any` | Fetch USGS water services records. Provides direct module-level access to ``USGSWaterData.fetch`` using a fresh ``USGSWaterData`` instance. Any: Value returned by ``USGSWaterData.fetch``. |
| `fetch_air_now()` | `fetch_air_now( mode: str = 'current-zip', zip_code: str = '', latitude: float \| None = None, longitude: float \| None = None, date: str = '', distance: int = 25, time: int = 20 ) -> Any` | Fetch AirNow current and forecast air quality data. Provides direct module-level access to ``AirNow.fetch`` using a fresh ``AirNow`` instance. Any: Value returned by ``AirNow.fetch``. |
| `fetch_climate_data()` | `fetch_climate_data( mode: str = 'datasets', keyword: str = '', dataset: str = '', start_date: str = '', end_date: str = '', stations: str = '', data_types: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any` | Fetch NOAA climate dataset and data records. Provides direct module-level access to ``ClimateData.fetch`` using a fresh ``ClimateData`` instance. Any: Value returned by ``ClimateData.fetch``. |
| `fetch_eonet()` | `fetch_eonet( mode: str = 'events', source: str = '', category: str = '', status: str = 'open', limit: int = 25, days: int = 30, start_date: str = '', end_date: str = '', bbox: str = '', time: int = 20 ) -> Any` | Fetch NASA EONET environmental event data. Provides direct module-level access to ``EoNet.fetch`` using a fresh ``EoNet`` instance. Any: Value returned by ``EoNet.fetch``. |
| `fetch_envirofacts()` | `fetch_envirofacts( table_name: str = 'TRI_FACILITY', state_code: str = '', facility_name: str = '', limit: int = 25, time: int = 20 ) -> Any` | Fetch EPA Envirofacts table and facility records. Provides direct module-level access to ``EnviroFacts.fetch`` using a fresh ``EnviroFacts`` instance. Any: Value returned by ``EnviroFacts.fetch``. |
| `fetch_tides_and_currents()` | `fetch_tides_and_currents( mode: str = 'water-level', station_id: str = '', begin_date: str = '', end_date: str = '', datum: str = 'MLLW', units: str = 'metric', time_zone: str = 'gmt', interval: str = 'hilo', time: int = 20 ) -> Any` | Fetch NOAA tides, currents, and station data. Provides direct module-level access to ``TidesAndCurrents.fetch`` using a fresh ``TidesAndCurrents`` instance. Any: Value returned by ``TidesAndCurrents.fetch``. |
| `fetch_uv_index()` | `fetch_uv_index( mode: str = 'daily-zip', zip_code: str = '', city: str = '', state: str = '', time: int = 20 ) -> Any` | Fetch EPA UV Index current and forecast data. Provides direct module-level access to ``UvIndex.fetch`` using a fresh ``UvIndex`` instance. Any: Value returned by ``UvIndex.fetch``. |
| `fetch_purple_air()` | `fetch_purple_air( mode: str = 'sensors', sensor_index: int = None, nwlng: float \| None = None, nwlat: float \| None = None, selng: float \| None = None, selat: float \| None = None, location_type: int = 0, max_age: int = 0, modified_since: int = 0, fields: str = '', time: int = 20 ) -> Any` | Fetch PurpleAir sensor and air quality records. Provides direct module-level access to ``PurpleAir.fetch`` using a fresh ``PurpleAir`` instance. Any: Value returned by ``PurpleAir.fetch``. |
| `fetch_open_aq()` | `fetch_open_aq( mode: str = 'locations', location_id: int = None, parameter_id: int = None, country_id: int = None, coordinates: str = '', radius: int = 25000, providers_id: str = '', parameters_id: str = '', limit: int = 25, page: int = 1, time: int = 20 ) -> Any` | Fetch OpenAQ location, measurement, and air-quality records. Provides direct module-level access to ``OpenAQ.fetch`` using a fresh ``OpenAQ`` instance. Any: Value returned by ``OpenAQ.fetch``. |
| `fetch_firms()` | `fetch_firms( mode: str = 'area', source: str = 'VIIRS_SNPP_NRT', area_coordinates: str = 'world', day_range: int = 1, date: str = '', sensor: str = 'ALL', time: int = 20 ) -> Any` | Fetch NASA FIRMS active fire data. Provides direct module-level access to ``Firms.fetch`` using a fresh ``Firms`` instance. Any: Value returned by ``Firms.fetch``. |

### `fetch_google_weather_current()`

Fetch current. Provides direct module-level access to ``GoogleWeather.fetch_current`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_current``.

```python
fetch_google_weather_current( address: str, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

**Implementation target:** `GoogleWeather.fetch_current()`

### `fetch_google_weather_hourly_forecast()`

Fetch hourly forecast. Provides direct module-level access to ``GoogleWeather.fetch_hourly_forecast`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_hourly_forecast``.

```python
fetch_google_weather_hourly_forecast( address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

**Implementation target:** `GoogleWeather.fetch_hourly_forecast()`

### `fetch_google_weather_daily_forecast()`

Fetch daily forecast. Provides direct module-level access to ``GoogleWeather.fetch_daily_forecast`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_daily_forecast``.

```python
fetch_google_weather_daily_forecast( address: str, days: int = 5, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

**Implementation target:** `GoogleWeather.fetch_daily_forecast()`

### `fetch_google_weather_hourly_history()`

Fetch hourly history. Provides direct module-level access to ``GoogleWeather.fetch_hourly_history`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_hourly_history``.

```python
fetch_google_weather_hourly_history( address: str, hours: int = 24, units_system: str = 'METRIC', language_code: str = 'en', time: int = 10 ) -> Any
```

**Implementation target:** `GoogleWeather.fetch_hourly_history()`

### `fetch_google_weather_alerts()`

Fetch alerts. Provides direct module-level access to ``GoogleWeather.fetch_alerts`` using a fresh ``GoogleWeather`` instance. Any: Value returned by ``GoogleWeather.fetch_alerts``.

```python
fetch_google_weather_alerts( address: str, language_code: str = 'en', time: int = 10 ) -> Any
```

**Implementation target:** `GoogleWeather.fetch_alerts()`

### `fetch_earth_observatory()`

Fetch NASA EONET events, categories, sources, and layers. Provides direct module-level access to ``EarthObservatory.fetch`` using a fresh ``EarthObservatory`` instance. Any: Value returned by ``EarthObservatory.fetch``.

```python
fetch_earth_observatory( mode: str = 'events', status: str = 'open', category: str = '', source: str = '', limit: int = 20, days: int = 30, start_date: str = '', end_date: str = '', time: int = 20 ) -> Any
```

**Implementation target:** `EarthObservatory.fetch()`

### `fetch_open_weather()`

Fetch Open-Meteo current and forecast weather retrieval. Provides direct module-level access to ``OpenWeather.fetch`` using a fresh ``OpenWeather`` instance. Any: Value returned by ``OpenWeather.fetch``.

```python
fetch_open_weather( location: str, mode: str = 'current', zone: str = 'auto', forecast_days: int = 7, past_days: int = 0, count: int = 10 ) -> Any
```

**Implementation target:** `OpenWeather.fetch()`

### `fetch_historical_weather()`

Fetch historical weather archive retrieval. Provides direct module-level access to ``HistoricalWeather.fetch`` using a fresh ``HistoricalWeather`` instance. Any: Value returned by ``HistoricalWeather.fetch``.

```python
fetch_historical_weather( location: str, date: dt.date, zone: str = 'auto', count: int = 10 ) -> Any
```

**Implementation target:** `HistoricalWeather.fetch()`

### `fetch_usgs_earthquakes()`

Fetch USGS earthquake feed and query retrieval. Provides direct module-level access to ``USGSEarthquakes.fetch`` using a fresh ``USGSEarthquakes`` instance. Any: Value returned by ``USGSEarthquakes.fetch``.

```python
fetch_usgs_earthquakes( mode: str = 'feed', feed: str = 'all_day.geojson', start_date: str = '', end_date: str = '', min_magnitude: float = 1.0, max_magnitude: float = 10.0, limit: int = 25, order_by: str = 'time', event_type: str = 'earthquake', latitude: float | None = None, longitude: float | None = None, max_radius_km: float | None = None, time: int = 20 ) -> Any
```

**Implementation target:** `USGSEarthquakes.fetch()`

### `fetch_usgs_water_data()`

Fetch USGS water services records. Provides direct module-level access to ``USGSWaterData.fetch`` using a fresh ``USGSWaterData`` instance. Any: Value returned by ``USGSWaterData.fetch``.

```python
fetch_usgs_water_data( mode: str = 'monitoring-locations', monitoring_location_id: str = '', state_code: str = '', county_code: str = '', site_type: str = '', parameter_code: str = '', limit: int = 25, time: int = 20 ) -> Any
```

**Implementation target:** `USGSWaterData.fetch()`

### `fetch_air_now()`

Fetch AirNow current and forecast air quality data. Provides direct module-level access to ``AirNow.fetch`` using a fresh ``AirNow`` instance. Any: Value returned by ``AirNow.fetch``.

```python
fetch_air_now( mode: str = 'current-zip', zip_code: str = '', latitude: float | None = None, longitude: float | None = None, date: str = '', distance: int = 25, time: int = 20 ) -> Any
```

**Implementation target:** `AirNow.fetch()`

### `fetch_climate_data()`

Fetch NOAA climate dataset and data records. Provides direct module-level access to ``ClimateData.fetch`` using a fresh ``ClimateData`` instance. Any: Value returned by ``ClimateData.fetch``.

```python
fetch_climate_data( mode: str = 'datasets', keyword: str = '', dataset: str = '', start_date: str = '', end_date: str = '', stations: str = '', data_types: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

**Implementation target:** `ClimateData.fetch()`

### `fetch_eonet()`

Fetch NASA EONET environmental event data. Provides direct module-level access to ``EoNet.fetch`` using a fresh ``EoNet`` instance. Any: Value returned by ``EoNet.fetch``.

```python
fetch_eonet( mode: str = 'events', source: str = '', category: str = '', status: str = 'open', limit: int = 25, days: int = 30, start_date: str = '', end_date: str = '', bbox: str = '', time: int = 20 ) -> Any
```

**Implementation target:** `EoNet.fetch()`

### `fetch_envirofacts()`

Fetch EPA Envirofacts table and facility records. Provides direct module-level access to ``EnviroFacts.fetch`` using a fresh ``EnviroFacts`` instance. Any: Value returned by ``EnviroFacts.fetch``.

```python
fetch_envirofacts( table_name: str = 'TRI_FACILITY', state_code: str = '', facility_name: str = '', limit: int = 25, time: int = 20 ) -> Any
```

**Implementation target:** `EnviroFacts.fetch()`

### `fetch_tides_and_currents()`

Fetch NOAA tides, currents, and station data. Provides direct module-level access to ``TidesAndCurrents.fetch`` using a fresh ``TidesAndCurrents`` instance. Any: Value returned by ``TidesAndCurrents.fetch``.

```python
fetch_tides_and_currents( mode: str = 'water-level', station_id: str = '', begin_date: str = '', end_date: str = '', datum: str = 'MLLW', units: str = 'metric', time_zone: str = 'gmt', interval: str = 'hilo', time: int = 20 ) -> Any
```

**Implementation target:** `TidesAndCurrents.fetch()`

### `fetch_uv_index()`

Fetch EPA UV Index current and forecast data. Provides direct module-level access to ``UvIndex.fetch`` using a fresh ``UvIndex`` instance. Any: Value returned by ``UvIndex.fetch``.

```python
fetch_uv_index( mode: str = 'daily-zip', zip_code: str = '', city: str = '', state: str = '', time: int = 20 ) -> Any
```

**Implementation target:** `UvIndex.fetch()`

### `fetch_purple_air()`

Fetch PurpleAir sensor and air quality records. Provides direct module-level access to ``PurpleAir.fetch`` using a fresh ``PurpleAir`` instance. Any: Value returned by ``PurpleAir.fetch``.

```python
fetch_purple_air( mode: str = 'sensors', sensor_index: int = None, nwlng: float | None = None, nwlat: float | None = None, selng: float | None = None, selat: float | None = None, location_type: int = 0, max_age: int = 0, modified_since: int = 0, fields: str = '', time: int = 20 ) -> Any
```

**Implementation target:** `PurpleAir.fetch()`

### `fetch_open_aq()`

Fetch OpenAQ location, measurement, and air-quality records. Provides direct module-level access to ``OpenAQ.fetch`` using a fresh ``OpenAQ`` instance. Any: Value returned by ``OpenAQ.fetch``.

```python
fetch_open_aq( mode: str = 'locations', location_id: int = None, parameter_id: int = None, country_id: int = None, coordinates: str = '', radius: int = 25000, providers_id: str = '', parameters_id: str = '', limit: int = 25, page: int = 1, time: int = 20 ) -> Any
```

**Implementation target:** `OpenAQ.fetch()`

### `fetch_firms()`

Fetch NASA FIRMS active fire data. Provides direct module-level access to ``Firms.fetch`` using a fresh ``Firms`` instance. Any: Value returned by ``Firms.fetch``.

```python
fetch_firms( mode: str = 'area', source: str = 'VIIRS_SNPP_NRT', area_coordinates: str = 'world', day_range: int = 1, date: str = '', sensor: str = 'ALL', time: int = 20 ) -> Any
```

**Implementation target:** `Firms.fetch()`

## Geospatial

| Function | Signature | Purpose |
|---|---|---|
| `geocode_location()` | `geocode_location( address: str ) -> Any` | Geocode location. Provides direct module-level access to ``GoogleMaps.geocode_location`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.geocode_location``. |
| `geocode_coordinates()` | `geocode_coordinates( lat: float, long: float ) -> Any` | Geocode coordinates. Provides direct module-level access to ``GoogleMaps.geocode_coordinates`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.geocode_coordinates``. |
| `validate_address()` | `validate_address( address: List[str] ) -> Any` | Validate address. Provides direct module-level access to ``GoogleMaps.validate_address`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.validate_address``. |
| `request_directions()` | `request_directions( origin: str, destination: str, mode: str = 'driving' ) -> Any` | Request directions. Provides direct module-level access to ``GoogleMaps.request_directions`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.request_directions``. |
| `fetch_global_imagery_wms_map()` | `fetch_global_imagery_wms_map( layer: str, image_date: str, bbox: Tuple[float, float, float, float], width: int = 1200, height: int = 600, projection: str = 'epsg4326', quality: str = 'best', image_format: str = 'image/png', transparent: bool = True, output_dir: str = 'python-examples', output_name: str = '', time: int = 20 ) -> Any` | Fetch wms map. Provides direct module-level access to ``GlobalImagery.fetch_wms_map`` using a fresh ``GlobalImagery`` instance. Any: Value returned by ``GlobalImagery.fetch_wms_map``. |
| `fetch_global_imagery_map_services()` | `fetch_global_imagery_map_services(  ) -> Any` | Fetch map services. Provides direct module-level access to ``GlobalImagery.fetch_map_services`` using a fresh ``GlobalImagery`` instance. None. Any: Value returned by ``GlobalImagery.fetch_map_services``. |
| `fetch_global_imagery_mercator_map()` | `fetch_global_imagery_mercator_map( ccrs: Any = None ) -> Any` | Fetch mercator map. Provides direct module-level access to ``GlobalImagery.fetch_mercator_map`` using a fresh ``GlobalImagery`` instance. Any: Value returned by ``GlobalImagery.fetch_mercator_map``. |
| `fetch_google_geocoding()` | `fetch_google_geocoding( mode: str = 'forward', query: str = '', latitude: float = 0.0, longitude: float = 0.0, place_id: str = '', language: str = 'en', region: str = '', result_type: str = '', location_type: str = '', time: int = 10, api_key: Optional[str] = None ) -> Any` | Fetch Google forward, reverse, and place geocoding. Provides direct module-level access to ``GoogleGeocoding.fetch`` using a fresh ``GoogleGeocoding`` instance. Any: Value returned by ``GoogleGeocoding.fetch``. |
| `fetch_usgs_national_map()` | `fetch_usgs_national_map( mode: str = 'products', dataset: str = '', q: str = '', bbox: str = '', prod_formats: str = '', max_items: int = 25, offset: int = 0, time: int = 20 ) -> Any` | Fetch USGS National Map datasets and products. Provides direct module-level access to ``USGSTheNationalMap.fetch`` using a fresh ``USGSTheNationalMap`` instance. Any: Value returned by ``USGSTheNationalMap.fetch``. |
| `fetch_usgs_sciencebase()` | `fetch_usgs_sciencebase( mode: str = 'items', q: str = '', item_id: str = '', max_items: int = 25, offset: int = 0, fields: str = '', time: int = 20 ) -> Any` | Fetch USGS ScienceBase items and catalog records. Provides direct module-level access to ``USGSScienceBase.fetch`` using a fresh ``USGSScienceBase`` instance. Any: Value returned by ``USGSScienceBase.fetch``. |

### `geocode_location()`

Geocode location. Provides direct module-level access to ``GoogleMaps.geocode_location`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.geocode_location``.

```python
geocode_location( address: str ) -> Any
```

**Implementation target:** `GoogleMaps.geocode_location()`

### `geocode_coordinates()`

Geocode coordinates. Provides direct module-level access to ``GoogleMaps.geocode_coordinates`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.geocode_coordinates``.

```python
geocode_coordinates( lat: float, long: float ) -> Any
```

**Implementation target:** `GoogleMaps.geocode_coordinates()`

### `validate_address()`

Validate address. Provides direct module-level access to ``GoogleMaps.validate_address`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.validate_address``.

```python
validate_address( address: List[str] ) -> Any
```

**Implementation target:** `GoogleMaps.validate_address()`

### `request_directions()`

Request directions. Provides direct module-level access to ``GoogleMaps.request_directions`` using a fresh ``GoogleMaps`` instance. Any: Value returned by ``GoogleMaps.request_directions``.

```python
request_directions( origin: str, destination: str, mode: str = 'driving' ) -> Any
```

**Implementation target:** `GoogleMaps.request_directions()`

### `fetch_global_imagery_wms_map()`

Fetch wms map. Provides direct module-level access to ``GlobalImagery.fetch_wms_map`` using a fresh ``GlobalImagery`` instance. Any: Value returned by ``GlobalImagery.fetch_wms_map``.

```python
fetch_global_imagery_wms_map( layer: str, image_date: str, bbox: Tuple[float, float, float, float], width: int = 1200, height: int = 600, projection: str = 'epsg4326', quality: str = 'best', image_format: str = 'image/png', transparent: bool = True, output_dir: str = 'python-examples', output_name: str = '', time: int = 20 ) -> Any
```

**Implementation target:** `GlobalImagery.fetch_wms_map()`

### `fetch_global_imagery_map_services()`

Fetch map services. Provides direct module-level access to ``GlobalImagery.fetch_map_services`` using a fresh ``GlobalImagery`` instance. None. Any: Value returned by ``GlobalImagery.fetch_map_services``.

```python
fetch_global_imagery_map_services(  ) -> Any
```

**Implementation target:** `GlobalImagery.fetch_map_services()`

### `fetch_global_imagery_mercator_map()`

Fetch mercator map. Provides direct module-level access to ``GlobalImagery.fetch_mercator_map`` using a fresh ``GlobalImagery`` instance. Any: Value returned by ``GlobalImagery.fetch_mercator_map``.

```python
fetch_global_imagery_mercator_map( ccrs: Any = None ) -> Any
```

**Implementation target:** `GlobalImagery.fetch_mercator_map()`

### `fetch_google_geocoding()`

Fetch Google forward, reverse, and place geocoding. Provides direct module-level access to ``GoogleGeocoding.fetch`` using a fresh ``GoogleGeocoding`` instance. Any: Value returned by ``GoogleGeocoding.fetch``.

```python
fetch_google_geocoding( mode: str = 'forward', query: str = '', latitude: float = 0.0, longitude: float = 0.0, place_id: str = '', language: str = 'en', region: str = '', result_type: str = '', location_type: str = '', time: int = 10, api_key: Optional[str] = None ) -> Any
```

**Implementation target:** `GoogleGeocoding.fetch()`

### `fetch_usgs_national_map()`

Fetch USGS National Map datasets and products. Provides direct module-level access to ``USGSTheNationalMap.fetch`` using a fresh ``USGSTheNationalMap`` instance. Any: Value returned by ``USGSTheNationalMap.fetch``.

```python
fetch_usgs_national_map( mode: str = 'products', dataset: str = '', q: str = '', bbox: str = '', prod_formats: str = '', max_items: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

**Implementation target:** `USGSTheNationalMap.fetch()`

### `fetch_usgs_sciencebase()`

Fetch USGS ScienceBase items and catalog records. Provides direct module-level access to ``USGSScienceBase.fetch`` using a fresh ``USGSScienceBase`` instance. Any: Value returned by ``USGSScienceBase.fetch``.

```python
fetch_usgs_sciencebase( mode: str = 'items', q: str = '', item_id: str = '', max_items: int = 25, offset: int = 0, fields: str = '', time: int = 20 ) -> Any
```

**Implementation target:** `USGSScienceBase.fetch()`

## Health

| Function | Signature | Purpose |
|---|---|---|
| `fetch_health_data()` | `fetch_health_data( mode: str = 'rows', domain: str = 'healthdata.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any` | Fetch HealthData.gov Socrata metadata and rows. Provides direct module-level access to ``HealthData.fetch`` using a fresh ``HealthData`` instance. Any: Value returned by ``HealthData.fetch``. |
| `fetch_global_health_data()` | `fetch_global_health_data( mode: str = 'indicator_registry', query_path: str = '', fmt: str = 'json', time: int = 20 ) -> Any` | Fetch WHO global health indicator and Athena data. Provides direct module-level access to ``GlobalHealthData.fetch`` using a fresh ``GlobalHealthData`` instance. Any: Value returned by ``GlobalHealthData.fetch``. |
| `fetch_wonder()` | `fetch_wonder( mode: str = 'metadata_template', dataset_id: str = 'D76', request_xml: str = '', time: int = 20 ) -> Any` | Fetch CDC WONDER template and query submission. Provides direct module-level access to ``Wonder.fetch`` using a fresh ``Wonder`` instance. Any: Value returned by ``Wonder.fetch``. |
| `load_pubmed()` | `load_pubmed( query: str, max_docs: int = 5 ) -> Any` | Load source content. Provides direct module-level access to ``PubMedSearchLoader.load`` using a fresh ``PubMedSearchLoader`` instance. Any: Value returned by ``PubMedSearchLoader.load``. |

### `fetch_health_data()`

Fetch HealthData.gov Socrata metadata and rows. Provides direct module-level access to ``HealthData.fetch`` using a fresh ``HealthData`` instance. Any: Value returned by ``HealthData.fetch``.

```python
fetch_health_data( mode: str = 'rows', domain: str = 'healthdata.gov', dataset_id: str = '', select: str = '', where: str = '', order: str = '', group: str = '', limit: int = 25, offset: int = 0, time: int = 20 ) -> Any
```

**Implementation target:** `HealthData.fetch()`

### `fetch_global_health_data()`

Fetch WHO global health indicator and Athena data. Provides direct module-level access to ``GlobalHealthData.fetch`` using a fresh ``GlobalHealthData`` instance. Any: Value returned by ``GlobalHealthData.fetch``.

```python
fetch_global_health_data( mode: str = 'indicator_registry', query_path: str = '', fmt: str = 'json', time: int = 20 ) -> Any
```

**Implementation target:** `GlobalHealthData.fetch()`

### `fetch_wonder()`

Fetch CDC WONDER template and query submission. Provides direct module-level access to ``Wonder.fetch`` using a fresh ``Wonder`` instance. Any: Value returned by ``Wonder.fetch``.

```python
fetch_wonder( mode: str = 'metadata_template', dataset_id: str = 'D76', request_xml: str = '', time: int = 20 ) -> Any
```

**Implementation target:** `Wonder.fetch()`

### `load_pubmed()`

Load source content. Provides direct module-level access to ``PubMedSearchLoader.load`` using a fresh ``PubMedSearchLoader`` instance. Any: Value returned by ``PubMedSearchLoader.load``.

```python
load_pubmed( query: str, max_docs: int = 5 ) -> Any
```

**Implementation target:** `PubMedSearchLoader.load()`

## Web

| Function | Signature | Purpose |
|---|---|---|
| `fetch_web_page()` | `fetch_web_page( url: str, time: int = 10 ) -> Any` | Fetch HTTP web page retrieval and HTML extraction. Provides direct module-level access to ``WebFetcher.fetch`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.fetch``. |
| `convert_html_to_text()` | `convert_html_to_text( html: str ) -> Any` | HTML to text. Provides direct module-level access to ``WebFetcher.html_to_text`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.html_to_text``. |
| `extract_web_title()` | `extract_web_title( html: str ) -> Any` | Extract title. Provides direct module-level access to ``WebFetcher.extract_title`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_title``. |
| `extract_web_links()` | `extract_web_links( base_url: str, html: str ) -> Any` | Extract links. Provides direct module-level access to ``WebFetcher.extract_links`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_links``. |
| `extract_web_structured_data()` | `extract_web_structured_data( url: str, html: str, selected_methods: Optional[List[str]] = None ) -> Any` | Extract structured data. Provides direct module-level access to ``WebFetcher.extract_structured_data`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_structured_data``. |
| `crawl_web()` | `crawl_web( seed_url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, recursive: bool = False, max_depth: int = 1, max_pages: int = 10, same_domain_only: bool = True, request_timeout: int = 10, delay_seconds: float = 0.25, max_bytes: int = 1000000, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any` | Crawl. Provides direct module-level access to ``WebCrawler.crawl`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.crawl``. |
| `scrape_crawler_page()` | `scrape_crawler_page( url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, request_timeout: int = 10, max_bytes: int = 1000000, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any` | Scrape page. Provides direct module-level access to ``WebCrawler.scrape_page`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.scrape_page``. |
| `render_web_page()` | `render_web_page( url: str, timeout: int = 15, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any` | Render with playwright. Provides direct module-level access to ``WebCrawler.render_with_playwright`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.render_with_playwright``. |
| `load_web()` | `load_web( urls: str \| List[str], recursive: bool = False, max_depth: int = 2, prevent_outside: bool = True, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> Any` | Load source content. Provides direct module-level access to ``WebLoader.load`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load``. |
| `load_web_recursive()` | `load_web_recursive( url: str, depth: int = 2, max_time: int = 10, ignore: bool = True ) -> Any` | Load web documents recursively. Provides direct module-level access to ``WebLoader.load_recursive`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load_recursive``. |
| `load_web_pages()` | `load_web_pages( urls: List[str], depth: int = 2, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> Any` | Load static web pages. Provides direct module-level access to ``WebLoader.load_pages`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load_pages``. |
| `load_github()` | `load_github( url: str, repo: str, branch: str, filetype: str = '.md' ) -> Any` | Load source content. Provides direct module-level access to ``GithubLoader.load`` using a fresh ``GithubLoader`` instance. Any: Value returned by ``GithubLoader.load``. |
| `scrape_web_page()` | `scrape_web_page( url: str, time: int = 10 ) -> Any` | Fetch a web page. Provides direct module-level access to ``WebExtractor.scrape`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape``. |
| `scraper_html_to_text()` | `scraper_html_to_text( html: str ) -> Any` | Convert HTML to plain text. Provides direct module-level access to ``WebExtractor.html_to_text`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.html_to_text``. |
| `scrape_paragraphs()` | `scrape_paragraphs( uri: str ) -> Any` | Extract paragraph text. Provides direct module-level access to ``WebExtractor.scrape_paragraphs`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_paragraphs``. |
| `scrape_lists()` | `scrape_lists( uri: str ) -> Any` | Extract list item text. Provides direct module-level access to ``WebExtractor.scrape_lists`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_lists``. |
| `scrape_tables()` | `scrape_tables( uri: str ) -> Any` | Extract table cell text. Provides direct module-level access to ``WebExtractor.scrape_tables`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_tables``. |
| `scrape_articles()` | `scrape_articles( uri: str ) -> Any` | Extract article text. Provides direct module-level access to ``WebExtractor.scrape_articles`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_articles``. |
| `scrape_headings()` | `scrape_headings( uri: str ) -> Any` | Extract heading text. Provides direct module-level access to ``WebExtractor.scrape_headings`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_headings``. |
| `scrape_divisions()` | `scrape_divisions( uri: str ) -> Any` | Extract division text. Provides direct module-level access to ``WebExtractor.scrape_divisions`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_divisions``. |
| `scrape_sections()` | `scrape_sections( uri: str ) -> Any` | Extract section text. Provides direct module-level access to ``WebExtractor.scrape_sections`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_sections``. |
| `scrape_blockquotes()` | `scrape_blockquotes( uri: str ) -> Any` | Extract blockquote text. Provides direct module-level access to ``WebExtractor.scrape_blockquotes`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_blockquotes``. |
| `scrape_hyperlinks()` | `scrape_hyperlinks( uri: str ) -> Any` | Extract hyperlinks. Provides direct module-level access to ``WebExtractor.scrape_hyperlinks`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_hyperlinks``. |
| `scrape_images()` | `scrape_images( uri: str ) -> Any` | Extract image references. Provides direct module-level access to ``WebExtractor.scrape_images`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_images``. |
| `encode_image()` | `encode_image( path: str ) -> str` | Encode an image as Base64 text. Provides direct module-level access to ``fetchers.encode_image``. str: Base64-encoded image data. |

### `fetch_web_page()`

Fetch HTTP web page retrieval and HTML extraction. Provides direct module-level access to ``WebFetcher.fetch`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.fetch``.

```python
fetch_web_page( url: str, time: int = 10 ) -> Any
```

**Implementation target:** `WebFetcher.fetch()`

### `convert_html_to_text()`

HTML to text. Provides direct module-level access to ``WebFetcher.html_to_text`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.html_to_text``.

```python
convert_html_to_text( html: str ) -> Any
```

**Implementation target:** `WebFetcher.html_to_text()`

### `extract_web_title()`

Extract title. Provides direct module-level access to ``WebFetcher.extract_title`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_title``.

```python
extract_web_title( html: str ) -> Any
```

**Implementation target:** `WebFetcher.extract_title()`

### `extract_web_links()`

Extract links. Provides direct module-level access to ``WebFetcher.extract_links`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_links``.

```python
extract_web_links( base_url: str, html: str ) -> Any
```

**Implementation target:** `WebFetcher.extract_links()`

### `extract_web_structured_data()`

Extract structured data. Provides direct module-level access to ``WebFetcher.extract_structured_data`` using a fresh ``WebFetcher`` instance. Any: Value returned by ``WebFetcher.extract_structured_data``.

```python
extract_web_structured_data( url: str, html: str, selected_methods: Optional[List[str]] = None ) -> Any
```

**Implementation target:** `WebFetcher.extract_structured_data()`

### `crawl_web()`

Crawl. Provides direct module-level access to ``WebCrawler.crawl`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.crawl``.

```python
crawl_web( seed_url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, recursive: bool = False, max_depth: int = 1, max_pages: int = 10, same_domain_only: bool = True, request_timeout: int = 10, delay_seconds: float = 0.25, max_bytes: int = 1000000, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any
```

**Implementation target:** `WebCrawler.crawl()`

### `scrape_crawler_page()`

Scrape page. Provides direct module-level access to ``WebCrawler.scrape_page`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.scrape_page``.

```python
scrape_crawler_page( url: str, include_title: bool = True, include_basic_text: bool = True, include_raw_html: bool = False, selected_methods: Optional[List[str]] = None, request_timeout: int = 10, max_bytes: int = 1000000, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any
```

**Implementation target:** `WebCrawler.scrape_page()`

### `render_web_page()`

Render with playwright. Provides direct module-level access to ``WebCrawler.render_with_playwright`` using a fresh ``WebCrawler`` instance. Any: Value returned by ``WebCrawler.render_with_playwright``.

```python
render_web_page( url: str, timeout: int = 15, headers: Optional[Dict[str, str]] = None, use_playwright: bool = False ) -> Any
```

**Implementation target:** `WebCrawler.render_with_playwright()`

### `load_web()`

Load source content. Provides direct module-level access to ``WebLoader.load`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load``.

```python
load_web( urls: str | List[str], recursive: bool = False, max_depth: int = 2, prevent_outside: bool = True, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> Any
```

**Implementation target:** `WebLoader.load()`

### `load_web_recursive()`

Load web documents recursively. Provides direct module-level access to ``WebLoader.load_recursive`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load_recursive``.

```python
load_web_recursive( url: str, depth: int = 2, max_time: int = 10, ignore: bool = True ) -> Any
```

**Implementation target:** `WebLoader.load_recursive()`

### `load_web_pages()`

Load static web pages. Provides direct module-level access to ``WebLoader.load_pages`` using a fresh ``WebLoader`` instance. Any: Value returned by ``WebLoader.load_pages``.

```python
load_web_pages( urls: List[str], depth: int = 2, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> Any
```

**Implementation target:** `WebLoader.load_pages()`

### `load_github()`

Load source content. Provides direct module-level access to ``GithubLoader.load`` using a fresh ``GithubLoader`` instance. Any: Value returned by ``GithubLoader.load``.

```python
load_github( url: str, repo: str, branch: str, filetype: str = '.md' ) -> Any
```

**Implementation target:** `GithubLoader.load()`

### `scrape_web_page()`

Fetch a web page. Provides direct module-level access to ``WebExtractor.scrape`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape``.

```python
scrape_web_page( url: str, time: int = 10 ) -> Any
```

**Implementation target:** `WebExtractor.scrape()`

### `scraper_html_to_text()`

Convert HTML to plain text. Provides direct module-level access to ``WebExtractor.html_to_text`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.html_to_text``.

```python
scraper_html_to_text( html: str ) -> Any
```

**Implementation target:** `WebExtractor.html_to_text()`

### `scrape_paragraphs()`

Extract paragraph text. Provides direct module-level access to ``WebExtractor.scrape_paragraphs`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_paragraphs``.

```python
scrape_paragraphs( uri: str ) -> Any
```

**Implementation target:** `WebExtractor.scrape_paragraphs()`

### `scrape_lists()`

Extract list item text. Provides direct module-level access to ``WebExtractor.scrape_lists`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_lists``.

```python
scrape_lists( uri: str ) -> Any
```

**Implementation target:** `WebExtractor.scrape_lists()`

### `scrape_tables()`

Extract table cell text. Provides direct module-level access to ``WebExtractor.scrape_tables`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_tables``.

```python
scrape_tables( uri: str ) -> Any
```

**Implementation target:** `WebExtractor.scrape_tables()`

### `scrape_articles()`

Extract article text. Provides direct module-level access to ``WebExtractor.scrape_articles`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_articles``.

```python
scrape_articles( uri: str ) -> Any
```

**Implementation target:** `WebExtractor.scrape_articles()`

### `scrape_headings()`

Extract heading text. Provides direct module-level access to ``WebExtractor.scrape_headings`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_headings``.

```python
scrape_headings( uri: str ) -> Any
```

**Implementation target:** `WebExtractor.scrape_headings()`

### `scrape_divisions()`

Extract division text. Provides direct module-level access to ``WebExtractor.scrape_divisions`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_divisions``.

```python
scrape_divisions( uri: str ) -> Any
```

**Implementation target:** `WebExtractor.scrape_divisions()`

### `scrape_sections()`

Extract section text. Provides direct module-level access to ``WebExtractor.scrape_sections`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_sections``.

```python
scrape_sections( uri: str ) -> Any
```

**Implementation target:** `WebExtractor.scrape_sections()`

### `scrape_blockquotes()`

Extract blockquote text. Provides direct module-level access to ``WebExtractor.scrape_blockquotes`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_blockquotes``.

```python
scrape_blockquotes( uri: str ) -> Any
```

**Implementation target:** `WebExtractor.scrape_blockquotes()`

### `scrape_hyperlinks()`

Extract hyperlinks. Provides direct module-level access to ``WebExtractor.scrape_hyperlinks`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_hyperlinks``.

```python
scrape_hyperlinks( uri: str ) -> Any
```

**Implementation target:** `WebExtractor.scrape_hyperlinks()`

### `scrape_images()`

Extract image references. Provides direct module-level access to ``WebExtractor.scrape_images`` using a fresh ``WebExtractor`` instance. Any: Value returned by ``WebExtractor.scrape_images``.

```python
scrape_images( uri: str ) -> Any
```

**Implementation target:** `WebExtractor.scrape_images()`

### `encode_image()`

Encode an image as Base64 text. Provides direct module-level access to ``fetchers.encode_image``. str: Base64-encoded image data.

```python
encode_image( path: str ) -> str
```

**Implementation target:** `_encode_image()`
