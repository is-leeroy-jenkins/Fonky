###### Fonky

![](https://github.com/is-leeroy-jenkins/fonky/blob/main/resources/images/fonky_project.png)

<p align="center">
  <a href="#-purpose">Purpose</a> &nbsp;|&nbsp;
  <a href="#%EF%B8%8F-architecture">Architecture</a> &nbsp;|&nbsp;
  <a href="#%EF%B8%8F-installation">Installation</a> &nbsp;|&nbsp;
  <a href="#-functional-interface">Functional Interface</a> &nbsp;|&nbsp;
  <a href="#-domain-api-reference">Domains</a> &nbsp;|&nbsp;
  <a href="resources/user-guide.md">Usage</a> &nbsp;|&nbsp;
  <a href="https://is-leeroy-jenkins.github.io/Fonky/">Documentation</a> &nbsp;|&nbsp;
  <a href="#-requirements">Requirements</a>
</p>

___

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-0078FC?style=for-the-badge&logo=github)](https://is-leeroy-jenkins.github.io/Fonky/)

Fonky is a reusable Python framework for data retrieval, document ingestion, web scraping,
cloud loading, and domain-oriented data access.

The implementation remains object-oriented in `fetchers.py`, `loaders.py`, and `scrapers.py`.
The new `fonky.py` module adds a simple functional interface over those implementation classes:
each module-level function creates the appropriate implementation object, invokes its existing
method, and returns the result.

The current functional interface exposes **110 module-level operations** organized
across **9 domains**.

## 🎯 Purpose

Fonky provides a reusable library for:

| Capability | Description |
|---|---|
| 🌐 Web Fetching | Retrieve web pages, crawl sites, extract links and structured content, and render or scrape web sources |
| 🔎 Search & Archives | Query ArXiv, Wikipedia, Google Search, Google Drive, Congress, government data, news, Internet Archive, and Grokipedia |
| 📄 Document Loading | Load text, PDF, CSV, Excel, Word, Markdown, HTML, PowerPoint, JSON, XML, Outlook, email, SharePoint, and Jupyter content |
| ☁️ Cloud Loading | Load from Google Drive, Google Cloud Storage, AWS S3, OneDrive, and Google Speech-to-Text |
| 🌿 Environmental Data | Retrieve weather, climate, air-quality, water, earthquake, fire, UV, tide, and natural-event data |
| 🗺️ Geospatial Data | Geocode locations, reverse-geocode coordinates, validate addresses, request directions, and retrieve imagery and mapping data |
| 🔭 Astronomy & Space | Query astronomical catalogs, satellites, space weather, star maps, star charts, OpenSky, and near-Earth objects |
| 👥 Demographic & Health | Retrieve Census, Socrata, United Nations, population, health, CDC WONDER, PubMed, and open-city data |
| 🧰 Functional Tool Surface | Call implementation functionality through ordinary, explicitly typed module-level functions in `fonky.py` |

## 🏗️ Architecture

![](https://github.com/is-leeroy-jenkins/Fonky/blob/main/resources/images/fonky-architecture.png)

Fonky now has two intentionally simple layers:

```text
Application / Notebook / Agent
            |
            v
      fonky/fonky.py
 module-level functions
            |
    +-------+-------+
    |       |       |
    v       v       v
fetchers  loaders  scrapers
    |       |       |
    v       v       v
 existing implementation classes
```

`fonky.py` does not duplicate provider, loading, or scraping logic. Its functions are thin wrappers
over the existing classes.

A wrapper follows this pattern:

```python
def scrape_tables( uri: str ):
    scraper = WebExtractor( )
    return scraper.scrape_tables( uri=uri )
```

This keeps class lifecycle local to each invocation and avoids shared mutable implementation
instances.

## 🧰 Project Structure

```text
Fonky/
    README.md
    requirements.txt

    notebook/
        fonkytown.ipynb

    fonky/
        __init__.py
        fonky.py
        config.py
        core.py
        fetchers.py
        loaders.py
        models.py
        processors.py
        scrapers.py

        archives.py
        astronomical.py
        cloud.py
        demographic.py
        documents.py
        environmental.py
        geospatial.py
        health.py
        web.py
```

## 🗺️ Class Map

![](https://github.com/is-leeroy-jenkins/Fonky/blob/main/resources/images/fonky-classmap.png)

The original class-based APIs remain available:

```python
from fonky.fetchers import WebFetcher, GoogleSearch, Wikipedia, ArXiv
from fonky.loaders import TextLoader, PdfLoader, CsvLoader, WebLoader
from fonky.scrapers import WebExtractor
```

The new functional API provides a simpler entry point for application and Tool use.

## ⚙️ Installation

From the project root:

```powershell
cd Fonky
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Install Playwright browser support when using Playwright-backed web functionality:

```powershell
python -m playwright install chromium
```

## 🔐 Environment Configuration

Fonky reads credentials from environment variables through `fonky.config`.

Common variables include:

```text
OPENAI_API_KEY
GOOGLE_API_KEY
GOOGLE_CSE_ID
GOOGLE_WEATHER_API_KEY
GOOGLE_ACCOUNT_CREDENTIALS
GOOGLE_DRIVE_TOKEN_PATH
GOOGLE_DRIVE_FOLDER_ID
GEMINI_API_KEY
NASA_API_KEY
NASA_EARTHDATA_TOKEN
THENEWSAPI_API_KEY
MISTRAL_API_KEY
PINECONE_API_KEY
XAI_API_KEY
AIRNOW_API_KEY
CONGRESS_API_KEY
OPENAQ_API_KEY
PURPLEAIR_API_KEY
```

Example PowerShell setup:

```powershell
$env:GOOGLE_API_KEY = "your-google-api-key"
$env:GOOGLE_CSE_ID = "your-google-custom-search-engine-id"
$env:GOOGLE_WEATHER_API_KEY = "your-google-weather-api-key"
$env:NASA_API_KEY = "your-nasa-api-key"
$env:THENEWSAPI_API_KEY = "your-thenewsapi-key"
```

Credentials should remain in environment variables or controlled configuration and should not be
embedded in source code.

## 🧰 Functional Interface

The new `fonky.py` module is the consolidated functional interface for the functionality implemented
by `fetchers.py`, `loaders.py`, and `scrapers.py`.

Each function:

1. accepts explicit typed arguments;
2. creates a fresh implementation-class instance;
3. invokes the corresponding implementation method;
4. returns the implementation result directly.

No provider logic is duplicated in `fonky.py`.

### Import the functional module

```python
from fonky import fonky
```

### Fetch environmental data

```python
weather = fonky.fetch_google_weather_current(
    address='Arlington, VA',
    units_system='METRIC',
    language_code='en',
    time=10
)
```

```python
earthquakes = fonky.fetch_usgs_earthquakes(
    mode='feed',
    feed='all_day.geojson',
    min_magnitude=1.0,
    limit=25
)
```

### Load documents

```python
documents = fonky.load_pdf(
    path='sample.pdf',
    mode='single',
    extract='plain',
    include=False,
    format='markdown-img',
    size=1000,
    overlap=150,
    has_tables=True
)
```

```python
documents = fonky.load_excel(
    path='sample.xlsx',
    mode='elements',
    has_headers=True
)
```

### Scrape web content

```python
tables = fonky.scrape_tables(
    uri='https://example.com'
)
```

```python
paragraphs = fonky.scrape_paragraphs(
    uri='https://example.com'
)
```

### Search archive and research sources

```python
documents = fonky.fetch_arxiv(
    question='large language model tool use',
    max_documents=5,
    full_documents=False,
    include_metadata=True
)
```

### Geocode locations

```python
location = fonky.geocode_location(
    address='1600 Pennsylvania Avenue NW, Washington, DC'
)
```

## 🤖 Tool Usage

The functions in `fonky.py` are ordinary Python callables with explicit signatures and documentation.
They are intended to provide a clean callable surface for later Tool integration.

Provider-specific registration, registry design, and Tool orchestration are intentionally outside the
scope of this interface revision. The underlying `ToolDef` infrastructure in `models.py` remains
available for future integration without changing these wrapper functions.

## 📓 Jupyter Notebook

The included notebook is located at:

```text
notebook/fonkytown.ipynb
```

Launch it from the project root:

```powershell
python -m jupyter lab notebook/fonkytown.ipynb
```

or:

```powershell
python -m notebook notebook/fonkytown.ipynb
```

If the notebook cannot find the local package, add the project root to `sys.path`:

```python
from pathlib import Path
import sys

project_root = Path.cwd().parent if Path.cwd().name == 'notebook' else Path.cwd()

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
```

## 🧭 Domain API Reference

`fonky.py` groups its functional surface by domain while keeping all functions in one module.

### Archives

Archive, reference, public-data, search, and research-source retrieval.

| Function | Purpose |
|---|---|
| `fetch_arxiv()` | Fetch ArXiv research document retrieval. |
| `fetch_google_drive()` | Fetch Google Drive document retrieval. |
| `fetch_wikipedia()` | Fetch Wikipedia document retrieval. |
| `fetch_news()` | Fetch The News API article retrieval. |
| `fetch_google_search()` | Fetch Google Custom Search retrieval. |
| `fetch_gov_data()` | Fetch Data.gov package and collection retrieval. |
| `fetch_congress()` | Fetch Congress.gov legislative data retrieval. |
| `fetch_internet_archive()` | Fetch Internet Archive search and metadata retrieval. |
| `fetch_grokipedia()` | Fetch Grokipedia search and page retrieval. |
| `load_arxiv()` | Load source content. |
| `load_wikipedia()` | Load source content. |

### Astronomical

Astronomy, satellite, space-weather, star-chart, and near-Earth-object retrieval.

| Function | Purpose |
|---|---|
| `fetch_naval_observatory()` | Fetch U.S. Naval Observatory celestial-navigation data. |
| `fetch_satellite_center()` | Fetch SSC satellite observatory, ground-station, and location data. |
| `fetch_nearby_objects()` | Fetch JPL SSD and CNEOS near-Earth object data. |
| `fetch_open_science()` | Fetch NASA Open Science Data Repository resources. |
| `fetch_space_weather()` | Fetch NASA DONKI space weather endpoints. |
| `fetch_astro_catalog()` | Fetch Open Astronomy Catalog queries. |
| `fetch_astro_query()` | Fetch Simbad and astronomy object search operations. |
| `fetch_star_map()` | Fetch astronomical object map links and imagery. |
| `fetch_star_chart()` | Fetch static star chart and coordinate chart generation. |
| `fetch_open_sky()` | Fetch OpenSky Network aircraft, airport, and state-vector data. |

### Cloud

Cloud-storage, OneDrive, Google Drive, Google Cloud, AWS, and speech-loading operations.

| Function | Purpose |
|---|---|
| `load_google_drive_file()` | Load a provider file. |
| `load_google_drive_folder()` | Load provider folder content. |
| `load_onedrive()` | Load source content. |
| `load_google_cloud_file()` | Load source content. |
| `load_aws_file()` | Load source content. |
| `load_google_speech_to_text()` | Load source content. |
| `load_google_bucket()` | Load source content. |
| `load_aws_bucket()` | Load source content. |

### Demographic

Census, Socrata, United Nations, population, and open-city data operations.

| Function | Purpose |
|---|---|
| `fetch_census_data()` | Fetch U.S. Census dataset and variable retrieval. |
| `fetch_socrata()` | Fetch Socrata dataset metadata and row retrieval. |
| `fetch_united_nations()` | Fetch United Nations SDMX dataset and query retrieval. |
| `fetch_world_population()` | Fetch WorldPop catalog and raster metadata retrieval. |
| `load_open_city()` | Load source content. |

### Documents

Local document loading and parsing for common office, structured-data, and notebook formats.

| Function | Purpose |
|---|---|
| `load_text()` | Load source content. |
| `load_csv()` | Load source content. |
| `read_pdf()` | Load source content. |
| `load_pdf()` | Load source content. |
| `load_excel()` | Load source content. |
| `load_word()` | Load source content. |
| `load_markdown()` | Load source content. |
| `load_html()` | Load source content. |
| `load_outlook()` | Load source content. |
| `load_spfx()` | Load source content. |
| `load_spfx_folder()` | Load provider folder content. |
| `load_powerpoint()` | Load source content. |
| `load_powerpoint_multiple()` | Load multiple presentation elements. |
| `load_email()` | Load source content. |
| `load_json()` | Load source content. |
| `load_xml()` | Load source content. |
| `load_xml_tree()` | Parse an XML element tree. |
| `load_jupyter_notebook()` | Load source content. |

### Environmental

Weather, climate, air quality, natural hazards, water, fire, UV, and environmental data.

| Function | Purpose |
|---|---|
| `fetch_google_weather_current()` | Fetch current. |
| `fetch_google_weather_hourly_forecast()` | Fetch hourly forecast. |
| `fetch_google_weather_daily_forecast()` | Fetch daily forecast. |
| `fetch_google_weather_hourly_history()` | Fetch hourly history. |
| `fetch_google_weather_alerts()` | Fetch alerts. |
| `fetch_earth_observatory()` | Fetch NASA EONET events, categories, sources, and layers. |
| `fetch_open_weather()` | Fetch Open-Meteo current and forecast weather retrieval. |
| `fetch_historical_weather()` | Fetch historical weather archive retrieval. |
| `fetch_usgs_earthquakes()` | Fetch USGS earthquake feed and query retrieval. |
| `fetch_usgs_water_data()` | Fetch USGS water services records. |
| `fetch_air_now()` | Fetch AirNow current and forecast air quality data. |
| `fetch_climate_data()` | Fetch NOAA climate dataset and data records. |
| `fetch_eonet()` | Fetch NASA EONET environmental event data. |
| `fetch_envirofacts()` | Fetch EPA Envirofacts table and facility records. |
| `fetch_tides_and_currents()` | Fetch NOAA tides, currents, and station data. |
| `fetch_uv_index()` | Fetch EPA UV Index current and forecast data. |
| `fetch_purple_air()` | Fetch PurpleAir sensor and air quality records. |
| `fetch_open_aq()` | Fetch OpenAQ location, measurement, and air-quality records. |
| `fetch_firms()` | Fetch NASA FIRMS active fire data. |

### Geospatial

Geocoding, directions, global imagery, maps, National Map, and ScienceBase operations.

| Function | Purpose |
|---|---|
| `geocode_location()` | Geocode location. |
| `geocode_coordinates()` | Geocode coordinates. |
| `validate_address()` | Validate address. |
| `request_directions()` | Request directions. |
| `fetch_global_imagery_wms_map()` | Fetch wms map. |
| `fetch_global_imagery_map_services()` | Fetch map services. |
| `fetch_global_imagery_mercator_map()` | Fetch mercator map. |
| `fetch_google_geocoding()` | Fetch Google forward, reverse, and place geocoding. |
| `fetch_usgs_national_map()` | Fetch USGS National Map datasets and products. |
| `fetch_usgs_sciencebase()` | Fetch USGS ScienceBase items and catalog records. |

### Health

HealthData.gov, global health, CDC WONDER, and PubMed operations.

| Function | Purpose |
|---|---|
| `fetch_health_data()` | Fetch HealthData.gov Socrata metadata and rows. |
| `fetch_global_health_data()` | Fetch WHO global health indicator and Athena data. |
| `fetch_wonder()` | Fetch CDC WONDER template and query submission. |
| `load_pubmed()` | Load source content. |

### Web

Web fetching, crawling, loading, HTML extraction, scraping, GitHub loading, and image encoding.

| Function | Purpose |
|---|---|
| `fetch_web_page()` | Fetch HTTP web page retrieval and HTML extraction. |
| `convert_html_to_text()` | HTML to text. |
| `extract_web_title()` | Extract title. |
| `extract_web_links()` | Extract links. |
| `extract_web_structured_data()` | Extract structured data. |
| `crawl_web()` | Crawl. |
| `scrape_crawler_page()` | Scrape page. |
| `render_web_page()` | Render with playwright. |
| `load_web()` | Load source content. |
| `load_web_recursive()` | Load web documents recursively. |
| `load_web_pages()` | Load static web pages. |
| `load_github()` | Load source content. |
| `scrape_web_page()` | Fetch a web page. |
| `scraper_html_to_text()` | Convert HTML to plain text. |
| `scrape_paragraphs()` | Extract paragraph text. |
| `scrape_lists()` | Extract list item text. |
| `scrape_tables()` | Extract table cell text. |
| `scrape_articles()` | Extract article text. |
| `scrape_headings()` | Extract heading text. |
| `scrape_divisions()` | Extract division text. |
| `scrape_sections()` | Extract section text. |
| `scrape_blockquotes()` | Extract blockquote text. |
| `scrape_hyperlinks()` | Extract hyperlinks. |
| `scrape_images()` | Extract image references. |
| `encode_image()` | Encode an image as Base64 text. |

## 🧾 Requirements

| Package                      | Purpose                                                   | Notes                                                       |
|------------------------------|-----------------------------------------------------------|-------------------------------------------------------------|
| `pydantic`                   | Defines structured models and tool input schemas          | Required for `models.py` and structured tool-definition models             |
| `typing_extensions`          | Backports newer typing features                           | Useful for compatibility across Python versions             |
| `requests`                   | HTTP client for API fetchers                              | Required by most fetchers                                   |
| `pandas`                     | DataFrame handling and tabular data processing            | Used for structured data and loader outputs                 |
| `numpy`                      | Numeric processing                                        | Common dependency for data workflows                        |
| `python-dateutil`            | Date parsing and date utilities                           | Useful for API date parameters and notebooks                |
| `langchain`                  | Main LangChain framework                                  | Required for agent/tool workflows                           |
| `langchain-core`             | Core LangChain abstractions                               | Required for `Document`, tools, and retrievers              |
| `langchain-community`        | Community loaders and retrievers                          | Required by many loader/fetcher wrappers                    |
| `langchain-text-splitters`   | Document chunking                                         | Required for recursive text splitting                       |
| `langchain-google-community` | Google community integrations                             | Used by Google loaders                                      |
| `langchain-googledrive`      | Google Drive retriever support                            | Used by Google Drive tools                                  |
| `pypdf`                      | PDF parsing                                               | Required by PDF loaders                                     |
| `docx2txt`                   | Word document extraction                                  | Required by DOCX loaders                                    |
| `openpyxl`                   | Excel `.xlsx` support                                     | Required for Excel workflows                                |
| `xlrd`                       | Legacy Excel `.xls` support                               | Optional but useful                                         |
| `python-pptx`                | PowerPoint document support                               | Used by PowerPoint loaders                                  |
| `unstructured`               | Parses Office, HTML, Markdown, and mixed document formats | Heavy dependency; useful for full document support          |
| `lxml`                       | XML/HTML parsing                                          | Required by XML and HTML workflows                          |
| `beautifulsoup4`             | HTML parsing and scraping                                 | Required by web scraping methods                            |
| `html5lib`                   | HTML parser backend                                       | Useful with BeautifulSoup and document loaders              |
| `markdown`                   | Markdown parsing                                          | Useful for Markdown loader workflows                        |
| `nbformat`                   | Jupyter notebook parsing                                  | Required for notebook loader support                        |
| `pillow`                     | Image handling                                            | Required by image and OCR-related loaders                   |
| `rapidocr-onnxruntime`       | OCR fallback for PDFs/images                              | Useful for image-heavy PDFs                                 |
| `playwright`                 | Browser automation/rendering                              | Requires browser installation                               |
| `crawl4ai`                   | Web crawling/rendering support                            | Useful for dynamic pages                                    |
| `arxiv`                      | ArXiv API support                                         | Required by ArXiv retrieval                                 |
| `wikipedia`                  | Wikipedia API support                                     | Required by Wikipedia retrieval                             |
| `xmltodict`                  | XML-to-dictionary conversion                              | Useful for API and XML workflows                            |
| `google-genai`               | Gemini / Google GenAI SDK                                 | Required for Gemini-oriented workflows                      |
| `google-api-python-client`   | Google API client support                                 | Useful for Google Drive and other Google APIs               |
| `google-auth`                | Google authentication                                     | Required for Google API access                              |
| `google-auth-oauthlib`       | OAuth support for Google services                         | Required for user-authenticated Google workflows            |
| `google-cloud-storage`       | Google Cloud Storage support                              | Required by GCS loaders                                     |
| `google-cloud-speech`        | Google Speech-to-Text support                             | Required by speech loaders                                  |
| `boto3`                      | AWS SDK                                                   | Required by S3 file/directory loaders                       |
| `botocore`                   | Low-level AWS dependency                                  | Installed with `boto3`, but can be pinned explicitly        |
| `astropy`                    | Astronomy coordinate and data tools                       | Required by astronomy fetchers                              |
| `astroquery`                 | Astronomy data queries                                    | Required by SIMBAD / astronomy workflows                    |
| `sscws`                      | NASA SSC Web Services client                              | Required by satellite center tools                          |
| `OWSLib`                     | Web Map Service support                                   | Required by WMS/global imagery workflows                    |
| `cartopy`                    | Geospatial mapping/projections                            | Heavy dependency; needed for map rendering                  |
| `matplotlib`                 | Plotting and map rendering                                | Required by imagery/geospatial rendering                    |
| `grokipedia-api`             | Grokipedia client support                                 | Required only when Grokipedia tools are enabled             |
| `boogr`                      | Custom error wrapper used by service classes              | Keep as local package/module or replace with `fonky.errors` |

#### 📝 License

- Fonky is published under
- ![License: Public Domain](https://img.shields.io/badge/license-public%20domain-brightgreen.svg)
  the [MIT General Public License v3](https://github.com/is-leeroy-jenkins/Fonky/blob/main/LICENSE.txt).
