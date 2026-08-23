# Usage Recipes

This page is organized by task domain. It is intentionally example-driven and points to the
exhaustive [Functional API](../api/fonky.md) when a full signature or parameter table is needed.

## Archives

This domain currently exposes **11** operations. Common entry points include:

| Function | Purpose | Implementation |
| --- | --- | --- |
| `fetch_arxiv()` | Fetch ArXiv research document retrieval. Purpose: Provides direct module-level access to ``ArXiv.fetch`` using a fresh ``ArXiv`` instance. Args: question (str): Value passed to ``ArXiv.fetch``. max_documents (int): Value passed to ``ArXiv.fetch``. full_documents (bool): Value passed to ``ArXiv.fetch``. include_metadata (bool): Value passed to ``ArXiv.fetch``. Returns: Any: Value returned by ``ArXiv.fetch``. | `ArXiv.fetch()` |
| `fetch_google_drive()` | Fetch Google Drive document retrieval. Purpose: Provides direct module-level access to ``GoogleDrive.fetch`` using a fresh ``GoogleDrive`` instance. Args: question (str): Value passed to ``GoogleDrive.fetch``. folder_id (str): Value passed to ``GoogleDrive.fetch``. results (int): Value passed to ``GoogleDrive.fetch``. template (str): Value passed to ``GoogleDrive.fetch``. mime_type (str): Value passed to ``GoogleDri… | `GoogleDrive.fetch()` |
| `fetch_wikipedia()` | Fetch Wikipedia document retrieval. Purpose: Provides direct module-level access to ``Wikipedia.fetch`` using a fresh ``Wikipedia`` instance. Args: question (str): Value passed to ``Wikipedia.fetch``. language (str): Value passed to ``Wikipedia.fetch``. max_documents (int): Value passed to ``Wikipedia.fetch``. include_metadata (bool): Value passed to ``Wikipedia.fetch``. Returns: Any: Value returned by ``Wikipedia.f… | `Wikipedia.fetch()` |
| `fetch_news()` | Fetch The News API article retrieval. Purpose: Provides direct module-level access to ``TheNews.fetch`` using a fresh ``TheNews`` instance. Args: endpoint (str): Value passed to ``TheNews.fetch``. query (str): Value passed to ``TheNews.fetch``. language (str): Value passed to ``TheNews.fetch``. categories (str): Value passed to ``TheNews.fetch``. exclude_categories (str): Value passed to ``TheNews.fetch``. locale (s… | `TheNews.fetch()` |
| `fetch_google_search()` | Fetch Google Custom Search retrieval. Purpose: Provides direct module-level access to ``GoogleSearch.fetch`` using a fresh ``GoogleSearch`` instance. Args: keywords (str): Value passed to ``GoogleSearch.fetch``. results (int): Value passed to ``GoogleSearch.fetch``. start (int): Value passed to ``GoogleSearch.fetch``. exact_terms (str): Value passed to ``GoogleSearch.fetch``. exclude_terms (str): Value passed to ``G… | `GoogleSearch.fetch()` |
| `fetch_gov_data()` | Fetch Data.gov package and collection retrieval. Purpose: Provides direct module-level access to ``GovData.fetch`` using a fresh ``GovData`` instance. Args: mode (str): Value passed to ``GovData.fetch``. query (str): Value passed to ``GovData.fetch``. page_size (int): Value passed to ``GovData.fetch``. offset_mark (str): Value passed to ``GovData.fetch``. sort_field (str): Value passed to ``GovData.fetch``. sort_ord… | `GovData.fetch()` |
| `fetch_congress()` | Fetch Congress.gov legislative data retrieval. Purpose: Provides direct module-level access to ``Congress.fetch`` using a fresh ``Congress`` instance. Args: mode (str): Value passed to ``Congress.fetch``. congress (int): Value passed to ``Congress.fetch``. bill_type (str): Value passed to ``Congress.fetch``. bill_number (int): Value passed to ``Congress.fetch``. law_type (str): Value passed to ``Congress.fetch``. la… | `Congress.fetch()` |
| `fetch_internet_archive()` | Fetch Internet Archive search and metadata retrieval. Purpose: Provides direct module-level access to ``InternetArchive.fetch`` using a fresh ``InternetArchive`` instance. Args: keywords (str): Value passed to ``InternetArchive.fetch``. fields (List[str] \| None): Value passed to ``InternetArchive.fetch``. rows (int): Value passed to ``InternetArchive.fetch``. page (int): Value passed to ``InternetArchive.fetch``. so… | `InternetArchive.fetch()` |

Representative call:

```python
from fonky import fonky

result = fonky.fetch_arxiv(
    question='value',
    max_documents=None,
    full_documents=None,
    include_metadata=None
)
```

## Astronomical

This domain currently exposes **10** operations. Common entry points include:

| Function | Purpose | Implementation |
| --- | --- | --- |
| `fetch_naval_observatory()` | Fetch U.S. Naval Observatory celestial-navigation data. Purpose: Provides direct module-level access to ``NavalObservatory.fetch`` using a fresh ``NavalObservatory`` instance. Args: mode (str): Value passed to ``NavalObservatory.fetch``. date_value (str): Value passed to ``NavalObservatory.fetch``. time_value (str): Value passed to ``NavalObservatory.fetch``. latitude (float): Value passed to ``NavalObservatory.fetc… | `NavalObservatory.fetch()` |
| `fetch_satellite_center()` | Fetch SSC satellite observatory, ground-station, and location data. Purpose: Provides direct module-level access to ``SatelliteCenter.fetch`` using a fresh ``SatelliteCenter`` instance. Args: mode (str): Value passed to ``SatelliteCenter.fetch``. query (str): Value passed to ``SatelliteCenter.fetch``. start_time (str): Value passed to ``SatelliteCenter.fetch``. end_time (str): Value passed to ``SatelliteCenter.fetch… | `SatelliteCenter.fetch()` |
| `fetch_nearby_objects()` | Fetch JPL SSD and CNEOS near-Earth object data. Purpose: Provides direct module-level access to ``NearbyObjects.fetch`` using a fresh ``NearbyObjects`` instance. Args: mode (str): Value passed to ``NearbyObjects.fetch``. start_date (str): Value passed to ``NearbyObjects.fetch``. end_date (str): Value passed to ``NearbyObjects.fetch``. query (str): Value passed to ``NearbyObjects.fetch``. query_type (str): Value pass… | `NearbyObjects.fetch()` |
| `fetch_open_science()` | Fetch NASA Open Science Data Repository resources. Purpose: Provides direct module-level access to ``OpenScience.fetch`` using a fresh ``OpenScience`` instance. Args: mode (str): Value passed to ``OpenScience.fetch``. query (str): Value passed to ``OpenScience.fetch``. accession (str): Value passed to ``OpenScience.fetch``. format_value (str): Value passed to ``OpenScience.fetch``. time (int): Value passed to ``Open… | `OpenScience.fetch()` |
| `fetch_space_weather()` | Fetch NASA DONKI space weather endpoints. Purpose: Provides direct module-level access to ``SpaceWeather.fetch`` using a fresh ``SpaceWeather`` instance. Args: mode (str): Value passed to ``SpaceWeather.fetch``. start_date (str): Value passed to ``SpaceWeather.fetch``. end_date (str): Value passed to ``SpaceWeather.fetch``. time (int): Value passed to ``SpaceWeather.fetch``. location (str): Value passed to ``SpaceWe… | `SpaceWeather.fetch()` |
| `fetch_astro_catalog()` | Fetch Open Astronomy Catalog queries. Purpose: Provides direct module-level access to ``AstroCatalog.fetch`` using a fresh ``AstroCatalog`` instance. Args: mode (str): Value passed to ``AstroCatalog.fetch``. query (str): Value passed to ``AstroCatalog.fetch``. quantity (str): Value passed to ``AstroCatalog.fetch``. attributes (str): Value passed to ``AstroCatalog.fetch``. arguments (str): Value passed to ``AstroCata… | `AstroCatalog.fetch()` |
| `fetch_astro_query()` | Fetch Simbad and astronomy object search operations. Purpose: Provides direct module-level access to ``AstroQuery.fetch`` using a fresh ``AstroQuery`` instance. Args: mode (str): Value passed to ``AstroQuery.fetch``. query (str): Value passed to ``AstroQuery.fetch``. ra (str): Value passed to ``AstroQuery.fetch``. dec (str): Value passed to ``AstroQuery.fetch``. radius (float): Value passed to ``AstroQuery.fetch``.… | `AstroQuery.fetch()` |
| `fetch_star_map()` | Fetch astronomical object map links and imagery. Purpose: Provides direct module-level access to ``StarMap.fetch`` using a fresh ``StarMap`` instance. Args: mode (str): Value passed to ``StarMap.fetch``. query (str): Value passed to ``StarMap.fetch``. ra (float): Value passed to ``StarMap.fetch``. dec (float): Value passed to ``StarMap.fetch``. zoom (int): Value passed to ``StarMap.fetch``. image_source (str): Value… | `StarMap.fetch()` |

Representative call:

```python
from fonky import fonky

result = fonky.fetch_naval_observatory(
    mode='celnav',
    date_value='',
    time_value='',
    latitude=0.0,
    longitude=0.0,
    location_label=''
)
```

## Cloud

This domain currently exposes **8** operations. Common entry points include:

| Function | Purpose | Implementation |
| --- | --- | --- |
| `load_google_drive_file()` | Load a provider file. Purpose: Provides direct module-level access to ``GoogleDriveLoader.load_file`` using a fresh ``GoogleDriveLoader`` instance. Args: file_id (str): Value passed to ``GoogleDriveLoader.load_file``. recursive (bool): Value passed to ``GoogleDriveLoader.load_file``. Returns: Any: Value returned by ``GoogleDriveLoader.load_file``. | `GoogleDriveLoader.load_file()` |
| `load_google_drive_folder()` | Load provider folder content. Purpose: Provides direct module-level access to ``GoogleDriveLoader.load_folder`` using a fresh ``GoogleDriveLoader`` instance. Args: folder_id (str): Value passed to ``GoogleDriveLoader.load_folder``. recursive (bool): Value passed to ``GoogleDriveLoader.load_folder``. Returns: Any: Value returned by ``GoogleDriveLoader.load_folder``. | `GoogleDriveLoader.load_folder()` |
| `load_onedrive()` | Load source content. Purpose: Provides direct module-level access to ``OneDriveDocLoader.load`` using a fresh ``OneDriveDocLoader`` instance. Args: drive_id (str): Value passed to ``OneDriveDocLoader.load``. folder_path (Optional[str]): Value passed to ``OneDriveDocLoader.load``. object_ids (Optional[List[str]]): Value passed to ``OneDriveDocLoader.load``. auth_with_token (bool): Value passed to ``OneDriveDocLoader.… | `OneDriveDocLoader.load()` |
| `load_google_cloud_file()` | Load source content. Purpose: Provides direct module-level access to ``GoogleCloudFileLoader.load`` using a fresh ``GoogleCloudFileLoader`` instance. Args: project_name (str): Value passed to ``GoogleCloudFileLoader.load``. bucket (str): Value passed to ``GoogleCloudFileLoader.load``. blob (str): Value passed to ``GoogleCloudFileLoader.load``. Returns: Any: Value returned by ``GoogleCloudFileLoader.load``. | `GoogleCloudFileLoader.load()` |
| `load_aws_file()` | Load source content. Purpose: Provides direct module-level access to ``AwsFileLoader.load`` using a fresh ``AwsFileLoader`` instance. Args: bucket (str): Value passed to ``AwsFileLoader.load``. key (str): Value passed to ``AwsFileLoader.load``. aws_access_key_id (Optional[str]): Value passed to ``AwsFileLoader.load``. aws_secret_access_key (Optional[str]): Value passed to ``AwsFileLoader.load``. aws_session_token (O… | `AwsFileLoader.load()` |
| `load_google_speech_to_text()` | Load source content. Purpose: Provides direct module-level access to ``GoogleSpeechToTextLoader.load`` using a fresh ``GoogleSpeechToTextLoader`` instance. Args: project_id (str): Value passed to ``GoogleSpeechToTextLoader.load``. file_path (str): Value passed to ``GoogleSpeechToTextLoader.load``. config (Optional[Dict[str, Any]]): Value passed to ``GoogleSpeechToTextLoader.load``. Returns: Any: Value returned by ``… | `GoogleSpeechToTextLoader.load()` |
| `load_google_bucket()` | Load source content. Purpose: Provides direct module-level access to ``GoogleBucketLoader.load`` using a fresh ``GoogleBucketLoader`` instance. Args: project_name (str): Value passed to ``GoogleBucketLoader.load``. bucket (str): Value passed to ``GoogleBucketLoader.load``. prefix (Optional[str]): Value passed to ``GoogleBucketLoader.load``. continue_on_failure (bool): Value passed to ``GoogleBucketLoader.load``. Ret… | `GoogleBucketLoader.load()` |
| `load_aws_bucket()` | Load source content. Purpose: Provides direct module-level access to ``AwsBucketLoader.load`` using a fresh ``AwsBucketLoader`` instance. Args: bucket (str): Value passed to ``AwsBucketLoader.load``. prefix (Optional[str]): Value passed to ``AwsBucketLoader.load``. aws_access_key_id (Optional[str]): Value passed to ``AwsBucketLoader.load``. aws_secret_access_key (Optional[str]): Value passed to ``AwsBucketLoader.loa… | `AwsBucketLoader.load()` |

Representative call:

```python
from fonky import fonky

result = fonky.load_google_drive_file(
    file_id='value',
    recursive=False
)
```

## Demographic

This domain currently exposes **5** operations. Common entry points include:

| Function | Purpose | Implementation |
| --- | --- | --- |
| `fetch_census_data()` | Fetch U.S. Census dataset and variable retrieval. Purpose: Provides direct module-level access to ``CensusData.fetch`` using a fresh ``CensusData`` instance. Args: mode (str): Value passed to ``CensusData.fetch``. year (str): Value passed to ``CensusData.fetch``. dataset (str): Value passed to ``CensusData.fetch``. fields (str): Value passed to ``CensusData.fetch``. geography_for (str): Value passed to ``CensusData.… | `CensusData.fetch()` |
| `fetch_socrata()` | Fetch Socrata dataset metadata and row retrieval. Purpose: Provides direct module-level access to ``Socrata.fetch`` using a fresh ``Socrata`` instance. Args: mode (str): Value passed to ``Socrata.fetch``. domain (str): Value passed to ``Socrata.fetch``. dataset_id (str): Value passed to ``Socrata.fetch``. select (str): Value passed to ``Socrata.fetch``. where (str): Value passed to ``Socrata.fetch``. order (str): Va… | `Socrata.fetch()` |
| `fetch_united_nations()` | Fetch United Nations SDMX dataset and query retrieval. Purpose: Provides direct module-level access to ``UnitedNations.fetch`` using a fresh ``UnitedNations`` instance. Args: mode (str): Value passed to ``UnitedNations.fetch``. query_path (str): Value passed to ``UnitedNations.fetch``. time (int): Value passed to ``UnitedNations.fetch``. Returns: Any: Value returned by ``UnitedNations.fetch``. | `UnitedNations.fetch()` |
| `fetch_world_population()` | Fetch WorldPop catalog and raster metadata retrieval. Purpose: Provides direct module-level access to ``WorldPopulation.fetch`` using a fresh ``WorldPopulation`` instance. Args: mode (str): Value passed to ``WorldPopulation.fetch``. query (str): Value passed to ``WorldPopulation.fetch``. asset_path (str): Value passed to ``WorldPopulation.fetch``. page (int): Value passed to ``WorldPopulation.fetch``. page_size (int… | `WorldPopulation.fetch()` |
| `load_open_city()` | Load source content. Purpose: Provides direct module-level access to ``OpenCityLoader.load`` using a fresh ``OpenCityLoader`` instance. Args: city_id (str): Value passed to ``OpenCityLoader.load``. dataset_id (str): Value passed to ``OpenCityLoader.load``. limit (int): Value passed to ``OpenCityLoader.load``. Returns: Any: Value returned by ``OpenCityLoader.load``. | `OpenCityLoader.load()` |

Representative call:

```python
from fonky import fonky

result = fonky.fetch_census_data(
    mode='variables',
    year='2022',
    dataset='acs/acs5',
    fields='NAME,B01001_001E',
    geography_for='state:*',
    geography_in=''
)
```

## Documents

This domain currently exposes **18** operations. Common entry points include:

| Function | Purpose | Implementation |
| --- | --- | --- |
| `load_text()` | Load source content. Purpose: Provides direct module-level access to ``TextLoader.load`` using a fresh ``TextLoader`` instance. Args: path (str): Value passed to ``TextLoader.load``. encoding (Optional[str]): Value passed to ``TextLoader.load``. Returns: Any: Value returned by ``TextLoader.load``. | `TextLoader.load()` |
| `load_csv()` | Load source content. Purpose: Provides direct module-level access to ``CsvLoader.load`` using a fresh ``CsvLoader`` instance. Args: path (str): Value passed to ``CsvLoader.load``. encoding (Optional[str]): Value passed to ``CsvLoader.load``. source_column (Optional[str]): Value passed to ``CsvLoader.load``. delimiter (str): Value passed to ``CsvLoader.load``. quotechar (str): Value passed to ``CsvLoader.load``. Retu… | `CsvLoader.load()` |
| `read_pdf()` | Load source content. Purpose: Provides direct module-level access to ``PdfReader.load`` using a fresh ``PdfReader`` instance. Args: path (str): Value passed to ``PdfReader.load``. mode (str): Value passed to ``PdfReader.load``. Returns: Any: Value returned by ``PdfReader.load``. | `PdfReader.load()` |
| `load_pdf()` | Load source content. Purpose: Provides direct module-level access to ``PdfLoader.load`` using a fresh ``PdfLoader`` instance. Args: path (str): Value passed to ``PdfLoader.load``. mode (str): Value passed to ``PdfLoader.load``. extract (str): Value passed to ``PdfLoader.load``. include (bool): Value passed to ``PdfLoader.load``. format (str): Value passed to ``PdfLoader.load``. size (int): Value passed to ``PdfLoade… | `PdfLoader.load()` |
| `load_excel()` | Load source content. Purpose: Provides direct module-level access to ``ExcelLoader.load`` using a fresh ``ExcelLoader`` instance. Args: path (str): Value passed to ``ExcelLoader.load``. mode (str): Value passed to ``ExcelLoader.load``. has_headers (bool): Value passed to ``ExcelLoader.load``. Returns: Any: Value returned by ``ExcelLoader.load``. | `ExcelLoader.load()` |
| `load_word()` | Load source content. Purpose: Provides direct module-level access to ``WordLoader.load`` using a fresh ``WordLoader`` instance. Args: path (str): Value passed to ``WordLoader.load``. Returns: Any: Value returned by ``WordLoader.load``. | `WordLoader.load()` |
| `load_markdown()` | Load source content. Purpose: Provides direct module-level access to ``MarkdownLoader.load`` using a fresh ``MarkdownLoader`` instance. Args: path (str): Value passed to ``MarkdownLoader.load``. Returns: Any: Value returned by ``MarkdownLoader.load``. | `MarkdownLoader.load()` |
| `load_html()` | Load source content. Purpose: Provides direct module-level access to ``HtmlLoader.load`` using a fresh ``HtmlLoader`` instance. Args: path (str): Value passed to ``HtmlLoader.load``. Returns: Any: Value returned by ``HtmlLoader.load``. | `HtmlLoader.load()` |

Representative call:

```python
from fonky import fonky

result = fonky.load_text(
    path='value',
    encoding=None
)
```

## Environmental

This domain currently exposes **19** operations. Common entry points include:

| Function | Purpose | Implementation |
| --- | --- | --- |
| `fetch_google_weather_current()` | Fetch current. Purpose: Provides direct module-level access to ``GoogleWeather.fetch_current`` using a fresh ``GoogleWeather`` instance. Args: address (str): Value passed to ``GoogleWeather.fetch_current``. units_system (str): Value passed to ``GoogleWeather.fetch_current``. language_code (str): Value passed to ``GoogleWeather.fetch_current``. time (int): Value passed to ``GoogleWeather.fetch_current``. Returns: Any… | `GoogleWeather.fetch_current()` |
| `fetch_google_weather_hourly_forecast()` | Fetch hourly forecast. Purpose: Provides direct module-level access to ``GoogleWeather.fetch_hourly_forecast`` using a fresh ``GoogleWeather`` instance. Args: address (str): Value passed to ``GoogleWeather.fetch_hourly_forecast``. hours (int): Value passed to ``GoogleWeather.fetch_hourly_forecast``. units_system (str): Value passed to ``GoogleWeather.fetch_hourly_forecast``. language_code (str): Value passed to ``Go… | `GoogleWeather.fetch_hourly_forecast()` |
| `fetch_google_weather_daily_forecast()` | Fetch daily forecast. Purpose: Provides direct module-level access to ``GoogleWeather.fetch_daily_forecast`` using a fresh ``GoogleWeather`` instance. Args: address (str): Value passed to ``GoogleWeather.fetch_daily_forecast``. days (int): Value passed to ``GoogleWeather.fetch_daily_forecast``. units_system (str): Value passed to ``GoogleWeather.fetch_daily_forecast``. language_code (str): Value passed to ``GoogleWe… | `GoogleWeather.fetch_daily_forecast()` |
| `fetch_google_weather_hourly_history()` | Fetch hourly history. Purpose: Provides direct module-level access to ``GoogleWeather.fetch_hourly_history`` using a fresh ``GoogleWeather`` instance. Args: address (str): Value passed to ``GoogleWeather.fetch_hourly_history``. hours (int): Value passed to ``GoogleWeather.fetch_hourly_history``. units_system (str): Value passed to ``GoogleWeather.fetch_hourly_history``. language_code (str): Value passed to ``GoogleW… | `GoogleWeather.fetch_hourly_history()` |
| `fetch_google_weather_alerts()` | Fetch alerts. Purpose: Provides direct module-level access to ``GoogleWeather.fetch_alerts`` using a fresh ``GoogleWeather`` instance. Args: address (str): Value passed to ``GoogleWeather.fetch_alerts``. language_code (str): Value passed to ``GoogleWeather.fetch_alerts``. time (int): Value passed to ``GoogleWeather.fetch_alerts``. Returns: Any: Value returned by ``GoogleWeather.fetch_alerts``. | `GoogleWeather.fetch_alerts()` |
| `fetch_earth_observatory()` | Fetch NASA EONET events, categories, sources, and layers. Purpose: Provides direct module-level access to ``EarthObservatory.fetch`` using a fresh ``EarthObservatory`` instance. Args: mode (str): Value passed to ``EarthObservatory.fetch``. status (str): Value passed to ``EarthObservatory.fetch``. category (str): Value passed to ``EarthObservatory.fetch``. source (str): Value passed to ``EarthObservatory.fetch``. lim… | `EarthObservatory.fetch()` |
| `fetch_open_weather()` | Fetch Open-Meteo current and forecast weather retrieval. Purpose: Provides direct module-level access to ``OpenWeather.fetch`` using a fresh ``OpenWeather`` instance. Args: location (str): Value passed to ``OpenWeather.fetch``. mode (str): Value passed to ``OpenWeather.fetch``. zone (str): Value passed to ``OpenWeather.fetch``. forecast_days (int): Value passed to ``OpenWeather.fetch``. past_days (int): Value passed… | `OpenWeather.fetch()` |
| `fetch_historical_weather()` | Fetch historical weather archive retrieval. Purpose: Provides direct module-level access to ``HistoricalWeather.fetch`` using a fresh ``HistoricalWeather`` instance. Args: location (str): Value passed to ``HistoricalWeather.fetch``. date (dt.date): Value passed to ``HistoricalWeather.fetch``. zone (str): Value passed to ``HistoricalWeather.fetch``. count (int): Value passed to ``HistoricalWeather.fetch``. Returns: A… | `HistoricalWeather.fetch()` |

Representative call:

```python
from fonky import fonky

result = fonky.fetch_google_weather_current(
    address='value',
    units_system='METRIC',
    language_code='en',
    time=10
)
```

## Geospatial

This domain currently exposes **10** operations. Common entry points include:

| Function | Purpose | Implementation |
| --- | --- | --- |
| `geocode_location()` | Geocode location. Purpose: Provides direct module-level access to ``GoogleMaps.geocode_location`` using a fresh ``GoogleMaps`` instance. Args: address (str): Value passed to ``GoogleMaps.geocode_location``. Returns: Any: Value returned by ``GoogleMaps.geocode_location``. | `GoogleMaps.geocode_location()` |
| `geocode_coordinates()` | Geocode coordinates. Purpose: Provides direct module-level access to ``GoogleMaps.geocode_coordinates`` using a fresh ``GoogleMaps`` instance. Args: lat (float): Value passed to ``GoogleMaps.geocode_coordinates``. long (float): Value passed to ``GoogleMaps.geocode_coordinates``. Returns: Any: Value returned by ``GoogleMaps.geocode_coordinates``. | `GoogleMaps.geocode_coordinates()` |
| `validate_address()` | Validate address. Purpose: Provides direct module-level access to ``GoogleMaps.validate_address`` using a fresh ``GoogleMaps`` instance. Args: address (List[str]): Value passed to ``GoogleMaps.validate_address``. Returns: Any: Value returned by ``GoogleMaps.validate_address``. | `GoogleMaps.validate_address()` |
| `request_directions()` | Request directions. Purpose: Provides direct module-level access to ``GoogleMaps.request_directions`` using a fresh ``GoogleMaps`` instance. Args: origin (str): Value passed to ``GoogleMaps.request_directions``. destination (str): Value passed to ``GoogleMaps.request_directions``. mode (str): Value passed to ``GoogleMaps.request_directions``. Returns: Any: Value returned by ``GoogleMaps.request_directions``. | `GoogleMaps.request_directions()` |
| `fetch_global_imagery_wms_map()` | Fetch wms map. Purpose: Provides direct module-level access to ``GlobalImagery.fetch_wms_map`` using a fresh ``GlobalImagery`` instance. Args: layer (str): Value passed to ``GlobalImagery.fetch_wms_map``. image_date (str): Value passed to ``GlobalImagery.fetch_wms_map``. bbox (Tuple[float, float, float, float]): Value passed to ``GlobalImagery.fetch_wms_map``. width (int): Value passed to ``GlobalImagery.fetch_wms_m… | `GlobalImagery.fetch_wms_map()` |
| `fetch_global_imagery_map_services()` | Fetch map services. Purpose: Provides direct module-level access to ``GlobalImagery.fetch_map_services`` using a fresh ``GlobalImagery`` instance. Args: None. Returns: Any: Value returned by ``GlobalImagery.fetch_map_services``. | `GlobalImagery.fetch_map_services()` |
| `fetch_global_imagery_mercator_map()` | Fetch mercator map. Purpose: Provides direct module-level access to ``GlobalImagery.fetch_mercator_map`` using a fresh ``GlobalImagery`` instance. Args: ccrs (Any): Value passed to ``GlobalImagery.fetch_mercator_map``. Returns: Any: Value returned by ``GlobalImagery.fetch_mercator_map``. | `GlobalImagery.fetch_mercator_map()` |
| `fetch_google_geocoding()` | Fetch Google forward, reverse, and place geocoding. Purpose: Provides direct module-level access to ``GoogleGeocoding.fetch`` using a fresh ``GoogleGeocoding`` instance. Args: mode (str): Value passed to ``GoogleGeocoding.fetch``. query (str): Value passed to ``GoogleGeocoding.fetch``. latitude (float): Value passed to ``GoogleGeocoding.fetch``. longitude (float): Value passed to ``GoogleGeocoding.fetch``. place_id… | `GoogleGeocoding.fetch()` |

Representative call:

```python
from fonky import fonky

result = fonky.geocode_location(
    address='value'
)
```

## Health

This domain currently exposes **4** operations. Common entry points include:

| Function | Purpose | Implementation |
| --- | --- | --- |
| `fetch_health_data()` | Fetch HealthData.gov Socrata metadata and rows. Purpose: Provides direct module-level access to ``HealthData.fetch`` using a fresh ``HealthData`` instance. Args: mode (str): Value passed to ``HealthData.fetch``. domain (str): Value passed to ``HealthData.fetch``. dataset_id (str): Value passed to ``HealthData.fetch``. select (str): Value passed to ``HealthData.fetch``. where (str): Value passed to ``HealthData.fetch… | `HealthData.fetch()` |
| `fetch_global_health_data()` | Fetch WHO global health indicator and Athena data. Purpose: Provides direct module-level access to ``GlobalHealthData.fetch`` using a fresh ``GlobalHealthData`` instance. Args: mode (str): Value passed to ``GlobalHealthData.fetch``. query_path (str): Value passed to ``GlobalHealthData.fetch``. fmt (str): Value passed to ``GlobalHealthData.fetch``. time (int): Value passed to ``GlobalHealthData.fetch``. Returns: Any:… | `GlobalHealthData.fetch()` |
| `fetch_wonder()` | Fetch CDC WONDER template and query submission. Purpose: Provides direct module-level access to ``Wonder.fetch`` using a fresh ``Wonder`` instance. Args: mode (str): Value passed to ``Wonder.fetch``. dataset_id (str): Value passed to ``Wonder.fetch``. request_xml (str): Value passed to ``Wonder.fetch``. time (int): Value passed to ``Wonder.fetch``. Returns: Any: Value returned by ``Wonder.fetch``. | `Wonder.fetch()` |
| `load_pubmed()` | Load source content. Purpose: Provides direct module-level access to ``PubMedSearchLoader.load`` using a fresh ``PubMedSearchLoader`` instance. Args: query (str): Value passed to ``PubMedSearchLoader.load``. max_docs (int): Value passed to ``PubMedSearchLoader.load``. Returns: Any: Value returned by ``PubMedSearchLoader.load``. | `PubMedSearchLoader.load()` |

Representative call:

```python
from fonky import fonky

result = fonky.fetch_health_data(
    mode='rows',
    domain='healthdata.gov',
    dataset_id='',
    select='',
    where='',
    order=''
)
```

## Web

This domain currently exposes **25** operations. Common entry points include:

| Function | Purpose | Implementation |
| --- | --- | --- |
| `fetch_web_page()` | Fetch HTTP web page retrieval and HTML extraction. Purpose: Provides direct module-level access to ``WebFetcher.fetch`` using a fresh ``WebFetcher`` instance. Args: url (str): Value passed to ``WebFetcher.fetch``. time (int): Value passed to ``WebFetcher.fetch``. Returns: Any: Value returned by ``WebFetcher.fetch``. | `WebFetcher.fetch()` |
| `convert_html_to_text()` | HTML to text. Purpose: Provides direct module-level access to ``WebFetcher.html_to_text`` using a fresh ``WebFetcher`` instance. Args: html (str): Value passed to ``WebFetcher.html_to_text``. Returns: Any: Value returned by ``WebFetcher.html_to_text``. | `WebFetcher.html_to_text()` |
| `extract_web_title()` | Extract title. Purpose: Provides direct module-level access to ``WebFetcher.extract_title`` using a fresh ``WebFetcher`` instance. Args: html (str): Value passed to ``WebFetcher.extract_title``. Returns: Any: Value returned by ``WebFetcher.extract_title``. | `WebFetcher.extract_title()` |
| `extract_web_links()` | Extract links. Purpose: Provides direct module-level access to ``WebFetcher.extract_links`` using a fresh ``WebFetcher`` instance. Args: base_url (str): Value passed to ``WebFetcher.extract_links``. html (str): Value passed to ``WebFetcher.extract_links``. Returns: Any: Value returned by ``WebFetcher.extract_links``. | `WebFetcher.extract_links()` |
| `extract_web_structured_data()` | Extract structured data. Purpose: Provides direct module-level access to ``WebFetcher.extract_structured_data`` using a fresh ``WebFetcher`` instance. Args: url (str): Value passed to ``WebFetcher.extract_structured_data``. html (str): Value passed to ``WebFetcher.extract_structured_data``. selected_methods (Optional[List[str]]): Value passed to ``WebFetcher.extract_structured_data``. Returns: Any: Value returned by… | `WebFetcher.extract_structured_data()` |
| `crawl_web()` | Crawl. Purpose: Provides direct module-level access to ``WebCrawler.crawl`` using a fresh ``WebCrawler`` instance. Args: seed_url (str): Value passed to ``WebCrawler.crawl``. include_title (bool): Value passed to ``WebCrawler.crawl``. include_basic_text (bool): Value passed to ``WebCrawler.crawl``. include_raw_html (bool): Value passed to ``WebCrawler.crawl``. selected_methods (Optional[List[str]]): Value passed to… | `WebCrawler.crawl()` |
| `scrape_crawler_page()` | Scrape page. Purpose: Provides direct module-level access to ``WebCrawler.scrape_page`` using a fresh ``WebCrawler`` instance. Args: url (str): Value passed to ``WebCrawler.scrape_page``. include_title (bool): Value passed to ``WebCrawler.scrape_page``. include_basic_text (bool): Value passed to ``WebCrawler.scrape_page``. include_raw_html (bool): Value passed to ``WebCrawler.scrape_page``. selected_methods (Optiona… | `WebCrawler.scrape_page()` |
| `render_web_page()` | Render with playwright. Purpose: Provides direct module-level access to ``WebCrawler.render_with_playwright`` using a fresh ``WebCrawler`` instance. Args: url (str): Value passed to ``WebCrawler.render_with_playwright``. timeout (int): Value passed to ``WebCrawler.render_with_playwright``. headers (Optional[ Dict[ str, str ] ]): Value passed to ``WebCrawler.render_with_playwright``. use_playwright (bool): Value pass… | `WebCrawler.render_with_playwright()` |

Representative call:

```python
from fonky import fonky

result = fonky.fetch_web_page(
    url='value',
    time=10
)
```


## Composing Calls

A typical application will normalize outputs at its own boundary rather than expecting every Fonky
call to return the same shape.

```python
from fonky import fonky

location = fonky.geocode_location(
    address='Arlington, VA'
)

weather = fonky.fetch_google_weather_current(
    address='Arlington, VA',
    units_system='METRIC',
    language_code='en',
    time=10
)

paragraphs = fonky.scrape_paragraphs(
    uri='https://example.com'
)
```
