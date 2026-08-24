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
cloud loading, domain-oriented data access, and LangChain tool integration.

The implementation remains object-oriented in `fetchers.py`, `loaders.py`, and `scrapers.py`.
The `fonky.py` module provides a simple functional interface over those implementation classes:
each module-level function creates the appropriate implementation object, invokes its existing
method, and returns the result.

Fonky exposes **110 operations across 9 domains** through both its functional API and
LangChain tool surface.

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
| 🧰 Functional API | Typed, stateless entry points over Fonky fetchers, loaders, and scrapers |
| 🤖 LangChain Tools | Agent-callable versions of the functional API with schemas derived from type hints and Google-style docstrings |

## 🏗️ Architecture

Fonky's LangChain integration is implemented directly in `fonky.py`.

```text
LangChain Agent / Application
            |
            v
       fonky/fonky.py
 literal @tool decorators
            |
    +-------+-------+
    |       |       |
    v       v       v
fetchers  loaders  scrapers
```

Each public operation is decorated directly:

```python
from langchain_core.tools import tool


@tool(
    parse_docstring=True,
    error_on_invalid_docstring=True
)
def scrape_tables( uri: str ) -> Any:
    """Extract table cell text.

    Args:
        uri: Fully qualified URI of the target HTML document.

    Returns:
        List[str] | None: Table cell text values produced by the operation.
    """
    _instance = WebExtractor( )
    return _instance.scrape_tables( uri=uri )
```

`tools.py` is a grouping and discovery module only. It imports the already-decorated `BaseTool`
objects from `fonky.py` and organizes them into the nine Fonky domains.

### Important API consequence

Because `@tool` replaces each decorated function binding with a LangChain `BaseTool`, decorated
operations are invoked with `.invoke()` rather than as ordinary Python functions:

```python
from fonky.fonky import fetch_arxiv

result = fetch_arxiv.invoke(
    {
        'question': 'large language model tool use',
        'max_documents': 5,
        'full_documents': False,
        'include_metadata': True
    }
)
```

If ordinary function-call semantics are required, the underlying implementation classes in
`fetchers.py`, `loaders.py`, and `scrapers.py` remain directly callable.

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
        tools.py

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

The functional API provides a simple entry point for applications and notebooks. The
LangChain-facing API is available from `fonky.tools`.

## ⚙️ Installation

From the project root:

```powershell
cd Fonky
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel
python -m pip install "setuptools==81.0.0"
python -m pip install -r requirements.txt
python -m pip check
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

## 🧰 Public Tool Interface

The 110 public operations in `fonky.py` are LangChain `BaseTool` objects because they are decorated
directly with `@tool(...)`.

Import an operation:

```python
from fonky.fonky import fetch_usgs_earthquakes
```

Invoke it:

```python
result = fetch_usgs_earthquakes.invoke(
    {
        'mode': 'feed',
        'feed': 'all_day.geojson',
        'min_magnitude': 1.0,
        'limit': 25
    }
)
```

The operation's typed signature and Google-style `Args:` documentation are used to construct the
LangChain input schema.

## 🤖 LangChain Tool Integration

### Literal decorators

Every public operation in `fonky.py` uses the actual decorator syntax:

```python
@tool(
    parse_docstring=True,
    error_on_invalid_docstring=True
)
def fetch_arxiv( ... ):
    ...
```

No callable-conversion expression is used as a substitute for the requested decorator syntax.

### Domain-scoped tool sets

`tools.py` groups the already-decorated tools:

```python
from fonky.tools import get_tools

tools = get_tools( domain='archives' )
```

Supported domains:

```text
archives
astronomical
cloud
demographic
documents
environmental
geospatial
health
web
```

### Agent usage

```python
from langchain.agents import create_agent

from fonky.tools import get_tools

agent = create_agent(
    model='openai:gpt-5',
    tools=get_tools( domain='archives' ),
    system_prompt='Use Fonky tools when external research or public-source retrieval is required.'
)
```

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
| `fetch_arxiv()` | Search ArXiv and return matching research documents with configurable result count, full-document retrieval, and metadata inclusion. |
| `fetch_google_drive()` | Search Google Drive content within a folder using configurable query templates, MIME filtering, result limits, and retrieval modes. |
| `fetch_wikipedia()` | Retrieve Wikipedia documents for a topic with configurable language, result count, and metadata inclusion. |
| `fetch_news()` | Query The News API across article or headline endpoints with date, category, locale, domain, source, sorting, paging, and similarity filters. |
| `fetch_google_search()` | Run Google Custom Search with pagination, exact/excluded terms, file type, locale, site, safe-search, image, and date restrictions. |
| `fetch_gov_data()` | Search Data.gov packages or retrieve package and collection metadata using paging, sorting, and collection filters. |
| `fetch_congress()` | Retrieve Congress.gov congresses, bills, laws, reports, and conference-report data with date, paging, and sort controls. |
| `fetch_internet_archive()` | Search Internet Archive metadata with selectable fields, media-type and collection filters, paging, and download-oriented sorting. |
| `fetch_grokipedia()` | Search Grokipedia or retrieve a specific page with pagination and optional page-content inclusion. |
| `load_arxiv()` | Load ArXiv search results directly into LangChain `Document` objects for downstream retrieval or analysis. |
| `load_wikipedia()` | Load Wikipedia search results directly into LangChain `Document` objects for downstream retrieval or analysis. |

### Astronomical

Astronomy, satellite, space-weather, star-chart, and near-Earth-object retrieval.

| Function | Purpose |
|---|---|
| `fetch_naval_observatory()` | Retrieve U.S. Naval Observatory celestial-navigation data for a date, time, geographic position, and location label. |
| `fetch_satellite_center()` | Query NASA SSCWeb observatories, ground stations, or spacecraft-location data with time ranges, coordinate systems, and resolution control. |
| `fetch_nearby_objects()` | Query JPL SSD/CNEOS close approaches and small-body data with distance, body, orbital, physical-property, and discovery filters. |
| `fetch_open_science()` | Retrieve NASA Open Science Data Repository datasets or accession records in a requested response format. |
| `fetch_space_weather()` | Query NASA DONKI space-weather events such as CMEs and notifications with date, catalog, location, quality, speed, and keyword filters. |
| `fetch_astro_catalog()` | Query Open Astronomy Catalog resources by object, quantity, attributes, coordinates, radius, and response format. |
| `fetch_astro_query()` | Query SIMBAD objects by identifier or sky position using configurable radius, angular units, and row limits. |
| `fetch_star_map()` | Build astronomical map links or imagery for an object or coordinates with configurable survey source, zoom, overlays, and constellation display. |
| `fetch_star_chart()` | Generate static star or coordinate charts with configurable dimensions, limiting magnitude, survey imagery, and constellation overlays. |
| `fetch_open_sky()` | Retrieve OpenSky aircraft states, flights, airport activity, or bounded-area traffic with optional authentication and time filters. |

### Cloud

Cloud-storage, OneDrive, Google Drive, Google Cloud, AWS, and speech-loading operations.

| Function | Purpose |
|---|---|
| `load_google_drive_file()` | Load a Google Drive file into LangChain documents, with optional recursive traversal for supported content. |
| `load_google_drive_folder()` | Load documents from a Google Drive folder with optional recursive traversal. |
| `load_onedrive()` | Load OneDrive content by drive, folder path, or object IDs using token-based authentication when configured. |
| `load_google_cloud_file()` | Load a single Google Cloud Storage blob into LangChain documents by project, bucket, and blob name. |
| `load_aws_file()` | Load a single Amazon S3 object into LangChain documents with optional explicit AWS credentials, session token, and region. |
| `load_google_speech_to_text()` | Transcribe an audio file with Google Speech-to-Text and return the transcription as LangChain documents. |
| `load_google_bucket()` | Load objects from a Google Cloud Storage bucket with optional prefix filtering and configurable failure handling. |
| `load_aws_bucket()` | Load objects from an Amazon S3 bucket or prefix into LangChain documents with configurable AWS credentials and failure handling. |

### Demographic

Census, Socrata, United Nations, population, and open-city data operations.

| Function | Purpose |
|---|---|
| `fetch_census_data()` | Query U.S. Census datasets, variables, groups, geographies, and observations using dataset, year, geography, and predicate parameters. |
| `fetch_socrata()` | Retrieve Socrata dataset metadata or rows using dataset identifiers, SoQL selection/filtering, ordering, paging, and app-token authentication. |
| `fetch_united_nations()` | List United Nations SDMX datasets or submit SDMX data queries with agency, dataset, version, key, date, and format parameters. |
| `fetch_world_population()` | Search WorldPop datasets and retrieve raster/catalog metadata for population and demographic products. |
| `load_open_city()` | Load municipal open-data resources into LangChain documents through the OpenCity loader. |

### Documents

Local document loading and parsing for common office, structured-data, and notebook formats.

| Function | Purpose |
|---|---|
| `load_text()` | Read a local text file into LangChain `Document` objects with optional encoding selection. |
| `load_csv()` | Parse delimited tabular data into LangChain documents with configurable encoding, delimiter, quote character, and source-column metadata. |
| `read_pdf()` | Read a PDF through the base PDF loader using the requested document/page extraction mode. |
| `load_pdf()` | Extract PDF content with configurable extraction strategy, image handling, output format, table awareness, chunk size, and overlap. |
| `load_excel()` | Convert an Excel workbook into LangChain documents with selectable parsing mode and header handling. |
| `load_word()` | Extract text from a local Word document into LangChain `Document` objects. |
| `load_markdown()` | Parse a Markdown file into LangChain documents while preserving content for downstream chunking and retrieval. |
| `load_html()` | Parse a local HTML file into LangChain documents using the configured HTML document loader. |
| `load_outlook()` | Extract message content and metadata from a local Outlook `.msg` file into LangChain documents. |
| `load_spfx()` | Load documents from a SharePoint document library identified by its library ID. |
| `load_spfx_folder()` | Load documents from a specific folder within a SharePoint document library. |
| `load_powerpoint()` | Extract PowerPoint content into LangChain documents using the selected presentation parsing mode. |
| `load_powerpoint_multiple()` | Load multiple PowerPoint presentation elements or matched presentation sources in one operation. |
| `load_email()` | Parse an email file into LangChain documents with selectable extraction mode and optional attachment inclusion. |
| `load_json()` | Parse JSON or JSON Lines into LangChain documents, with control over text-content interpretation. |
| `load_xml()` | Parse a local XML document into LangChain `Document` objects. |
| `load_xml_tree()` | Parse a local XML source into an `lxml` element tree for structured XML traversal. |
| `load_jupyter_notebook()` | Load notebook cells into LangChain documents with controls for outputs, traceback inclusion, output length, and newline handling. |

### Environmental

Weather, climate, air quality, natural hazards, water, fire, UV, and environmental data.

| Function | Purpose |
|---|---|
| `fetch_google_weather_current()` | Retrieve current Google Weather conditions for an address or coordinates with configurable units, language, and timeout. |
| `fetch_google_weather_hourly_forecast()` | Retrieve Google Weather hourly forecasts for a location with configurable units, language, and forecast horizon. |
| `fetch_google_weather_daily_forecast()` | Retrieve Google Weather daily forecasts for a location with configurable units, language, and forecast horizon. |
| `fetch_google_weather_hourly_history()` | Retrieve historical hourly Google Weather observations for a location and requested time range. |
| `fetch_google_weather_alerts()` | Retrieve active Google Weather alerts for a location using the configured language and request timeout. |
| `fetch_earth_observatory()` | Query NASA Earth Observatory/EONET event, category, source, and layer information for natural-event monitoring. |
| `fetch_open_weather()` | Retrieve current conditions and forecasts from Open-Meteo using coordinates, weather variables, timezone, and forecast controls. |
| `fetch_historical_weather()` | Retrieve historical weather observations from the Open-Meteo archive for a location and date range. |
| `fetch_usgs_earthquakes()` | Retrieve predefined USGS earthquake feeds or filtered event queries using date, magnitude, ordering, event type, and geographic radius. |
| `fetch_usgs_water_data()` | Query USGS Water Services for site, instantaneous, daily, groundwater, or water-quality records using site and parameter filters. |
| `fetch_air_now()` | Retrieve AirNow current observations or forecasts by ZIP code, coordinates, distance, date, and monitored pollutant parameters. |
| `fetch_climate_data()` | Query NOAA climate datasets, stations, locations, data categories, data types, or observations with date and paging filters. |
| `fetch_eonet()` | Query NASA EONET natural events using category, source, status, date, limit, and event-selection filters. |
| `fetch_envirofacts()` | Query EPA Envirofacts tables and facility records using table, column, value, row-range, and geographic criteria. |
| `fetch_tides_and_currents()` | Retrieve NOAA CO-OPS station metadata, water levels, predictions, currents, meteorological observations, or datums. |
| `fetch_uv_index()` | Retrieve EPA UV Index current or forecast values for a ZIP code or geographic area. |
| `fetch_purple_air()` | Retrieve PurpleAir sensor metadata and measurements using sensor IDs, fields, geographic bounds, and API authentication. |
| `fetch_open_aq()` | Query OpenAQ locations, sensors, measurements, parameters, countries, or providers with geographic and temporal filtering. |
| `fetch_firms()` | Retrieve NASA FIRMS active-fire detections for a geographic area, satellite source, date window, and API map key. |

### Geospatial

Geocoding, directions, global imagery, maps, National Map, and ScienceBase operations.

| Function | Purpose |
|---|---|
| `geocode_location()` | Convert a street address or place description into latitude/longitude coordinates and normalized location metadata. |
| `geocode_coordinates()` | Reverse-geocode latitude/longitude coordinates into address and place metadata. |
| `validate_address()` | Validate and normalize an address using Google address-validation services. |
| `request_directions()` | Request route directions between origin and destination with configurable travel mode, waypoints, alternatives, and routing preferences. |
| `fetch_global_imagery_wms_map()` | Request and render imagery from a Web Map Service using layer, bounding box, dimensions, CRS, and image-format parameters. |
| `fetch_global_imagery_map_services()` | Discover available global imagery map services and layer metadata. |
| `fetch_global_imagery_mercator_map()` | Render global imagery in a Mercator-oriented map view using geographic bounds and projection settings. |
| `fetch_google_geocoding()` | Perform Google forward geocoding, reverse geocoding, or place lookup with optional language, region, result-type, and location-type filters. |
| `fetch_usgs_national_map()` | Search USGS National Map datasets and downloadable products using bounding box, dataset, format, date, and paging criteria. |
| `fetch_usgs_sciencebase()` | Search or retrieve USGS ScienceBase catalog items using text, item IDs, parent IDs, spatial filters, and paging controls. |

### Health

HealthData.gov, global health, CDC WONDER, and PubMed operations.

| Function | Purpose |
|---|---|
| `fetch_health_data()` | Retrieve HealthData.gov Socrata metadata or rows using dataset IDs, SoQL selection/filtering, ordering, paging, and app-token authentication. |
| `fetch_global_health_data()` | Query WHO Global Health Observatory indicators and Athena API data using indicator, profile, filter, format, and paging parameters. |
| `fetch_wonder()` | Retrieve CDC WONDER dataset templates or submit structured WONDER query requests. |
| `load_pubmed()` | Search PubMed and load matching biomedical literature into LangChain `Document` objects. |

### Web

Web fetching, crawling, loading, HTML extraction, scraping, GitHub loading, and image encoding.

| Function | Purpose |
|---|---|
| `fetch_web_page()` | Fetch an HTTP page, retain response/HTML state, and return Fonky's normalized `Result` wrapper. |
| `convert_html_to_text()` | Remove scripts, styles, markup, and repeated whitespace from raw HTML to produce compact plain text. |
| `extract_web_title()` | Extract and normalize the document title from supplied HTML. |
| `extract_web_links()` | Extract, normalize, deduplicate, and resolve HTTP(S) links relative to a base URL. |
| `extract_web_structured_data()` | Extract selected HTML structures—headings, paragraphs, lists, tables, articles, sections, links, or images—into labeled collections. |
| `crawl_web()` | Crawl a website with configurable page, depth, byte, timeout, and domain-boundary limits. |
| `scrape_crawler_page()` | Extract normalized content and metadata from a crawler-retrieved page. |
| `render_web_page()` | Render JavaScript-dependent web content through Playwright before returning the resulting page content. |
| `load_web()` | Load one or more URLs into LangChain documents, optionally using recursive same-domain traversal. |
| `load_web_recursive()` | Recursively load documents from a seed URL to a bounded depth with optional same-domain filtering. |
| `load_web_pages()` | Load a fixed list of web pages into LangChain documents with timeout, progress, and failure-handling controls. |
| `load_github()` | Load repository files from GitHub into LangChain documents using repository, branch, file-filter, and authentication settings. |
| `scrape_web_page()` | Issue a synchronous HTTP request and return the Fonky `Result` wrapper for the retrieved page. |
| `scraper_html_to_text()` | Convert raw HTML into readable plain text using the scraper's markup-removal and whitespace-normalization logic. |
| `scrape_paragraphs()` | Extract non-empty paragraph text from all `<p>` elements in a web page. |
| `scrape_lists()` | Extract non-empty list-item text from all `<li>` elements in a web page. |
| `scrape_tables()` | Flatten text from all table header and data cells across the page's HTML tables. |
| `scrape_articles()` | Extract consolidated text blocks from HTML `<article>` elements. |
| `scrape_headings()` | Extract heading text from `<h1>` through `<h6>` elements. |
| `scrape_divisions()` | Extract readable text from HTML `<div>` elements. |
| `scrape_sections()` | Extract readable text from HTML `<section>` elements. |
| `scrape_blockquotes()` | Extract readable text from HTML `<blockquote>` elements. |
| `scrape_hyperlinks()` | Extract populated `href` values from anchor elements. |
| `scrape_images()` | Extract populated `src` values from image elements. |
| `encode_image()` | Read an image from disk and return its bytes as a Base64-encoded string. |

## 🧾 Requirements

### Verified LangChain Stack

The following LangChain versions were installed together in the Fonky virtual environment and
validated with `python -m pip check`:

```text
langchain==1.3.16
langchain-core==1.6.0
langchain-community==0.4.2
langchain-text-splitters==1.1.2
langchain-google-community==5.0.0
langchain-googledrive==0.1.52
setuptools==81.0.0
```

`setuptools==81.0.0` is retained because the validated environment includes PyTorch 2.12.0, which
requires `setuptools<82`.


| Package                      | Purpose                                                   | Notes                                                       |
|------------------------------|-----------------------------------------------------------|-------------------------------------------------------------|
| `pydantic`                   | Defines structured models and tool input schemas          | Required for `models.py` and structured tool-definition models             |
| `typing_extensions`          | Backports newer typing features                           | Useful for compatibility across Python versions             |
| `requests`                   | HTTP client for API fetchers                              | Required by most fetchers                                   |
| `pandas`                     | DataFrame handling and tabular data processing            | Used for structured data and loader outputs                 |
| `numpy`                      | Numeric processing                                        | Common dependency for data workflows                        |
| `python-dateutil`            | Date parsing and date utilities                           | Useful for API date parameters and notebooks                |
| `langchain`                  | Main LangChain framework                                  | Verified with `1.3.16` for agent/tool workflows            |
| `langchain-core`             | Core LangChain abstractions                               | Verified with `1.6.0`; provides `@tool`, `Document`, and tool primitives |
| `langchain-community`        | Community loaders and retrievers                          | Verified with `0.4.2`; required by existing loaders/retrievers |
| `langchain-text-splitters`   | Document chunking                                         | Verified with `1.1.2`; required for recursive text splitting |
| `langchain-google-community` | Google community integrations                             | Verified with `5.0.0`; used by Google loaders              |
| `langchain-googledrive`      | Google Drive retriever support                            | Verified with `0.1.52`; temporary upstream integration package |
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

Fonky is distributed under the license defined in
[`LICENSE.txt`](https://github.com/is-leeroy-jenkins/Fonky/blob/main/LICENSE.txt).
