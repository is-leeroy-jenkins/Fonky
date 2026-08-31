###### Fonky

![](https://github.com/is-leeroy-jenkins/fonky/blob/main/resources/images/fonky-project.png)

<p align="left">
  <a href="#-purpose">Purpose</a> &nbsp;|&nbsp;
  <a href="#%EF%B8%8F-architecture">Architecture</a> &nbsp;|&nbsp;
  <a href="#%EF%B8%8F-installation">Installation</a> &nbsp;|&nbsp;
  <a href="resources/user-guide.md">Usage</a> &nbsp;|&nbsp;
  <a href="resources/Tools.md">Tools</a> &nbsp;|&nbsp;
  <a href="#-requirements">Requirements</a>
</p>

___

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-0078FC?style=for-the-badge&logo=github)](https://is-leeroy-jenkins.github.io/fonky/)

Fonky is a reusable Python framework for data retrieval, document ingestion, web scraping,
preprocessing, cloud loading, structured data access, and agent-callable tool integration.

The implementation remains object-oriented in `fetchers.py`, `loaders.py`, `scrapers.py`, and
`preprocessors.py`. The `tools.py` module is the OpenAI Agents SDK adapter layer: each public
`@function_tool` wrapper creates the appropriate implementation object, invokes the existing method,
and returns its result.

The rebuilt package preserves the original **110 retrieval, loading, and scraping tools** and adds
**40 preprocessing tools**, for a flat surface of **150 OpenAI Agents SDK function tools**. Fonky no
longer uses runtime domains, category registries, or category facade modules.

## 🎯 Purpose

Fonky provides a reusable library for:

| Capability              | Description                                                                                                                   |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| 🌐 Web Fetching         | Retrieve web pages, crawl sites, extract links and structured content, and render or scrape web sources                       |
| 🔎 Search & Archives    | Query ArXiv, Wikipedia, Google Search, Google Drive, Congress, government data, news, Internet Archive, and Grokipedia        |
| 📄 Document Loading     | Load text, PDF, CSV, Excel, Word, Markdown, HTML, PowerPoint, JSON, XML, Outlook, email, SharePoint, and Jupyter content      |
| ☁️ Cloud Loading        | Load from Google Drive, Google Cloud Storage, AWS S3, OneDrive, and Google Speech-to-Text                                     |
| 🌿 Environmental Data   | Retrieve weather, climate, air-quality, water, earthquake, fire, UV, tide, and natural-event data                             |
| 🗺️ Geospatial Data      | Geocode locations, reverse-geocode coordinates, validate addresses, request directions, and retrieve imagery and mapping data |
| 🔭 Astronomy & Space    | Query astronomical catalogs, satellites, space weather, star maps, star charts, OpenSky, and near-Earth objects               |
| 👥 Demographic & Health | Retrieve Census, Socrata, United Nations, population, health, CDC WONDER, PubMed, and open-city data                          |
| 🧰 Functional API       | Typed entry points over Fonky fetchers, loaders, scrapers, and preprocessors                                                   |
| 🤖 OpenAI Agent Tools   | Agent-callable `@function_tool` wrappers with schemas derived from type hints and docstrings                                  |

## 🏗️ Architecture

Fonky's agent integration is implemented directly in `tools.py`.

![](https://github.com/is-leeroy-jenkins/fonky/blob/main/resources/images/fonky-architecture.png)

___

```text
OpenAI Agent / Application
           |
           v
      fonky/tools.py
  @function_tool wrappers
           |
   +-------+---------+-------------+
   |       |         |             |
   v       v         v             v
fetchers loaders  scrapers  preprocessors
           |
           v
        models
```

The implementation modules remain directly usable as ordinary Python APIs. Only `tools.py` serves
as the OpenAI Agents SDK adapter layer.

Each public agent operation is decorated directly:

```python
from agents import function_tool

from .scrapers import WebExtractor


@function_tool
def scrape_tables( uri: str ) -> list[ str ] | None:
    """Extract table cell text.

    Purpose:
        Extracts table cell text from the supplied HTML document.

    Args:
        uri: Fully qualified URI of the target HTML document.

    Returns:
        list[str] | None: Extracted table cell values.
    """
    instance = WebExtractor( )
    return instance.scrape_tables( uri=uri )
```

The underlying implementation remains directly callable:

```python
from fonky.scrapers import WebExtractor

extractor = WebExtractor( )
result = extractor.scrape_tables( uri='https://example.com' )
```

## 🧰 Project Structure

```text
fonky/
    README.md
    requirements.txt

    fonky/
        __init__.py
        boogr.py
        config.py
        fetchers.py
        loaders.py
        models.py
        preprocessors.py
        scrapers.py
        tools.py

    notebook/
        fonky.ipynb

    logging/
        Exceptions.db
```

The former `tools.py`, `core.py`, `processors.py`, and category facade modules are no longer part of
the package. `processors.py` became `preprocessors.py`, and the shared `Result` response container is
provided through `models.py`.

## 🗺️ Class Map

![](https://github.com/is-leeroy-jenkins/fonky/blob/main/resources/images/fonky-classmap.png)

The implementation APIs remain directly available:

```python
from fonky.fetchers import WebFetcher, GoogleSearch, Wikipedia, ArXiv
from fonky.loaders import TextLoader, PdfLoader, CsvLoader, WebLoader
from fonky.scrapers import WebExtractor
from fonky.preprocessors import TextParser
```

The OpenAI Agents SDK function-tool interface is available from `fonky.tools`.

## ⚙️ Installation

From the project root:

```powershell
cd fonky
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

The public agent-facing operations are defined in `fonky.tools` as OpenAI Agents SDK `FunctionTool`
objects created with `@function_tool`.

Import only the tools required by the application:

```python
from fonky.tools import (
    fetch_arxiv,
    fetch_google_search,
    load_pdf,
    scrape_tables,
    normalize_text,
)
```

Use them directly with an OpenAI Agents SDK agent:

```python
from agents import Agent

from fonky.tools import fetch_arxiv, fetch_google_search


agent = Agent(
    name='Research Agent',
    instructions='Use Fonky tools when external research is required.',
    tools=[
        fetch_arxiv,
        fetch_google_search,
    ] )
```

The Agents SDK derives each tool's input schema from the function signature, type annotations, and
docstring.

### Flat Tool Surface

Fonky intentionally does **not** use domains, category registries, or domain-specific helper modules.
The sections later in this README group related tools only for documentation readability; they have
no runtime significance.

### Direct Implementation Usage

The OpenAI tool layer is optional. Applications can call the implementation classes directly:

```python
from fonky.fetchers import ArXiv

fetcher = ArXiv( )

documents = fetcher.fetch(
    question='agentic retrieval',
    max_documents=5,
    full_documents=False,
    include_metadata=True )
```

### OpenAI Agents SDK Integration

Fonky uses OpenAI Agents SDK `@function_tool` rather than LangChain `@tool`:

```python
from agents import function_tool


@function_tool
def fetch_arxiv( ... ):
    ...
```

The core implementation modules do not depend on the Agents SDK tool abstraction. `tools.py` imports
the implementation modules; the implementation modules do not import `tools.py`.

### LangChain Components Retained Internally

Fonky still uses selected LangChain packages internally for document loaders, retrievers,
`Document` objects, Google integrations, and text splitting. Replacing LangChain's `@tool` decorator
does not remove those internal implementation dependencies.

## 📓 Jupyter Notebook

The included notebook is located at:

```text
notebook/fonky.ipynb
```

Launch it from the project root:

```powershell
python -m jupyter lab notebook/fonky.ipynb
```

or:

```powershell
python -m notebook notebook/fonky.ipynb
```

If the notebook cannot find the local package, add the project root to `sys.path`:

```python
from pathlib import Path
import sys

project_root = Path.cwd().parent if Path.cwd().name == 'notebook' else Path.cwd()

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
```

## 🧭 Tool Reference

`tools.py` exposes a flat tool surface. The topical sections below are documentation groupings only and do not represent runtime domains, registries, or package modules.

### Archives

Archive, reference, public-data, search, and research-source retrieval.

| Function                   | Purpose                                                                                                                                       |
|----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `fetch_arxiv()`            | Search ArXiv and return matching research documents with configurable result count, full-document retrieval, and metadata inclusion.          |
| `fetch_google_drive()`     | Search Google Drive content within a folder using configurable query templates, MIME filtering, result limits, and retrieval modes.           |
| `fetch_wikipedia()`        | Retrieve Wikipedia documents for a topic with configurable language, result count, and metadata inclusion.                                    |
| `fetch_news()`             | Query The News API across article or headline endpoints with date, category, locale, domain, source, sorting, paging, and similarity filters. |
| `fetch_google_search()`    | Run Google Custom Search with pagination, exact/excluded terms, file type, locale, site, safe-search, image, and date restrictions.           |
| `fetch_gov_data()`         | Search Data.gov packages or retrieve package and collection metadata using paging, sorting, and collection filters.                           |
| `fetch_congress()`         | Retrieve Congress.gov congresses, bills, laws, reports, and conference-report data with date, paging, and sort controls.                      |
| `fetch_internet_archive()` | Search Internet Archive metadata with selectable fields, media-type and collection filters, paging, and download-oriented sorting.            |
| `fetch_grokipedia()`       | Search Grokipedia or retrieve a specific page with pagination and optional page-content inclusion.                                            |
| `load_arxiv()`             | Load ArXiv search results directly into LangChain `Document` objects for downstream retrieval or analysis.                                    |
| `load_wikipedia()`         | Load Wikipedia search results directly into LangChain `Document` objects for downstream retrieval or analysis.                                |

### Astronomical

Astronomy, satellite, space-weather, star-chart, and near-Earth-object retrieval.

![](https://github.com/is-leeroy-jenkins/fonky/blob/main/resources/images/fonky-astro-space.png)

| Function                    | Purpose                                                                                                                                          |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| `fetch_naval_observatory()` | Retrieve U.S. Naval Observatory celestial-navigation data for a date, time, geographic position, and location label.                             |
| `fetch_satellite_center()`  | Query NASA SSCWeb observatories, ground stations, or spacecraft-location data with time ranges, coordinate systems, and resolution control.      |
| `fetch_nearby_objects()`    | Query JPL SSD/CNEOS close approaches and small-body data with distance, body, orbital, physical-property, and discovery filters.                 |
| `fetch_open_science()`      | Retrieve NASA Open Science Data Repository datasets or accession records in a requested response format.                                         |
| `fetch_space_weather()`     | Query NASA DONKI space-weather events such as CMEs and notifications with date, catalog, location, quality, speed, and keyword filters.          |
| `fetch_astro_catalog()`     | Query Open Astronomy Catalog resources by object, quantity, attributes, coordinates, radius, and response format.                                |
| `fetch_astro_query()`       | Query SIMBAD objects by identifier or sky position using configurable radius, angular units, and row limits.                                     |
| `fetch_star_map()`          | Build astronomical map links or imagery for an object or coordinates with configurable survey source, zoom, overlays, and constellation display. |
| `fetch_star_chart()`        | Generate static star or coordinate charts with configurable dimensions, limiting magnitude, survey imagery, and constellation overlays.          |
| `fetch_open_sky()`          | Retrieve OpenSky aircraft states, flights, airport activity, or bounded-area traffic with optional authentication and time filters.              |

### Cloud

Cloud-storage, OneDrive, Google Drive, Google Cloud, AWS, and speech-loading operations.

| Function                       | Purpose                                                                                                                          |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| `load_google_drive_file()`     | Load a Google Drive file into LangChain documents, with optional recursive traversal for supported content.                      |
| `load_google_drive_folder()`   | Load documents from a Google Drive folder with optional recursive traversal.                                                     |
| `load_onedrive()`              | Load OneDrive content by drive, folder path, or object IDs using token-based authentication when configured.                     |
| `load_google_cloud_file()`     | Load a single Google Cloud Storage blob into LangChain documents by project, bucket, and blob name.                              |
| `load_aws_file()`              | Load a single Amazon S3 object into LangChain documents with optional explicit AWS credentials, session token, and region.       |
| `load_google_speech_to_text()` | Transcribe an audio file with Google Speech-to-Text and return the transcription as LangChain documents.                         |
| `load_google_bucket()`         | Load objects from a Google Cloud Storage bucket with optional prefix filtering and configurable failure handling.                |
| `load_aws_bucket()`            | Load objects from an Amazon S3 bucket or prefix into LangChain documents with configurable AWS credentials and failure handling. |

### Demographic

Census, Socrata, United Nations, population, and open-city data operations.

![](https://github.com/is-leeroy-jenkins/fonky/blob/main/resources/images/fonky-demo-health.png)

| Function                   | Purpose                                                                                                                                        |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `fetch_census_data()`      | Query U.S. Census datasets, variables, groups, geographies, and observations using dataset, year, geography, and predicate parameters.         |
| `fetch_socrata()`          | Retrieve Socrata dataset metadata or rows using dataset identifiers, SoQL selection/filtering, ordering, paging, and app-token authentication. |
| `fetch_united_nations()`   | List United Nations SDMX datasets or submit SDMX data queries with agency, dataset, version, key, date, and format parameters.                 |
| `fetch_world_population()` | Search WorldPop datasets and retrieve raster/catalog metadata for population and demographic products.                                         |
| `load_open_city()`         | Load municipal open-data resources into LangChain documents through the OpenCity loader.                                                       |

### Documents

Local document loading and parsing for common office, structured-data, and notebook formats.

| Function                     | Purpose                                                                                                                                   |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `load_text()`                | Read a local text file into LangChain `Document` objects with optional encoding selection.                                                |
| `load_csv()`                 | Parse delimited tabular data into LangChain documents with configurable encoding, delimiter, quote character, and source-column metadata. |
| `read_pdf()`                 | Read a PDF through the base PDF loader using the requested document/page extraction mode.                                                 |
| `load_pdf()`                 | Extract PDF content with configurable extraction strategy, image handling, output format, table awareness, chunk size, and overlap.       |
| `load_excel()`               | Convert an Excel workbook into LangChain documents with selectable parsing mode and header handling.                                      |
| `load_word()`                | Extract text from a local Word document into LangChain `Document` objects.                                                                |
| `load_markdown()`            | Parse a Markdown file into LangChain documents while preserving content for downstream chunking and retrieval.                            |
| `load_html()`                | Parse a local HTML file into LangChain documents using the configured HTML document loader.                                               |
| `load_outlook()`             | Extract message content and metadata from a local Outlook `.msg` file into LangChain documents.                                           |
| `load_spfx()`                | Load documents from a SharePoint document library identified by its library ID.                                                           |
| `load_spfx_folder()`         | Load documents from a specific folder within a SharePoint document library.                                                               |
| `load_powerpoint()`          | Extract PowerPoint content into LangChain documents using the selected presentation parsing mode.                                         |
| `load_powerpoint_multiple()` | Load multiple PowerPoint presentation elements or matched presentation sources in one operation.                                          |
| `load_email()`               | Parse an email file into LangChain documents with selectable extraction mode and optional attachment inclusion.                           |
| `load_json()`                | Parse JSON or JSON Lines into LangChain documents, with control over text-content interpretation.                                         |
| `load_xml()`                 | Parse a local XML document into LangChain `Document` objects.                                                                             |
| `load_xml_tree()`            | Parse a local XML source into an `lxml` element tree for structured XML traversal.                                                        |
| `load_jupyter_notebook()`    | Load notebook cells into LangChain documents with controls for outputs, traceback inclusion, output length, and newline handling.         |

### Environmental

Weather, climate, air quality, natural hazards, water, fire, UV, and environmental data.

![](https://github.com/is-leeroy-jenkins/fonky/blob/main/resources/images/fonky-geo-climate.png)

___

| Function                                 | Purpose                                                                                                                                 |
|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| `fetch_google_weather_current()`         | Retrieve current Google Weather conditions for an address or coordinates with configurable units, language, and timeout.                |
| `fetch_google_weather_hourly_forecast()` | Retrieve Google Weather hourly forecasts for a location with configurable units, language, and forecast horizon.                        |
| `fetch_google_weather_daily_forecast()`  | Retrieve Google Weather daily forecasts for a location with configurable units, language, and forecast horizon.                         |
| `fetch_google_weather_hourly_history()`  | Retrieve historical hourly Google Weather observations for a location and requested time range.                                         |
| `fetch_google_weather_alerts()`          | Retrieve active Google Weather alerts for a location using the configured language and request timeout.                                 |
| `fetch_earth_observatory()`              | Query NASA Earth Observatory/EONET event, category, source, and layer information for natural-event monitoring.                         |
| `fetch_open_weather()`                   | Retrieve current conditions and forecasts from Open-Meteo using coordinates, weather variables, timezone, and forecast controls.        |
| `fetch_historical_weather()`             | Retrieve historical weather observations from the Open-Meteo archive for a location and date range.                                     |
| `fetch_usgs_earthquakes()`               | Retrieve predefined USGS earthquake feeds or filtered event queries using date, magnitude, ordering, event type, and geographic radius. |
| `fetch_usgs_water_data()`                | Query USGS Water Services for site, instantaneous, daily, groundwater, or water-quality records using site and parameter filters.       |
| `fetch_air_now()`                        | Retrieve AirNow current observations or forecasts by ZIP code, coordinates, distance, date, and monitored pollutant parameters.         |
| `fetch_climate_data()`                   | Query NOAA climate datasets, stations, locations, data categories, data types, or observations with date and paging filters.            |
| `fetch_eonet()`                          | Query NASA EONET natural events using category, source, status, date, limit, and event-selection filters.                               |
| `fetch_envirofacts()`                    | Query EPA Envirofacts tables and facility records using table, column, value, row-range, and geographic criteria.                       |
| `fetch_tides_and_currents()`             | Retrieve NOAA CO-OPS station metadata, water levels, predictions, currents, meteorological observations, or datums.                     |
| `fetch_uv_index()`                       | Retrieve EPA UV Index current or forecast values for a ZIP code or geographic area.                                                     |
| `fetch_purple_air()`                     | Retrieve PurpleAir sensor metadata and measurements using sensor IDs, fields, geographic bounds, and API authentication.                |
| `fetch_open_aq()`                        | Query OpenAQ locations, sensors, measurements, parameters, countries, or providers with geographic and temporal filtering.              |
| `fetch_firms()`                          | Retrieve NASA FIRMS active-fire detections for a geographic area, satellite source, date window, and API map key.                       |

### Geospatial

Geocoding, directions, global imagery, maps, National Map, and ScienceBase operations.

| Function                              | Purpose                                                                                                                                      |
|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `geocode_location()`                  | Convert a street address or place description into latitude/longitude coordinates and normalized location metadata.                          |
| `geocode_coordinates()`               | Reverse-geocode latitude/longitude coordinates into address and place metadata.                                                              |
| `validate_address()`                  | Validate and normalize an address using Google address-validation services.                                                                  |
| `request_directions()`                | Request route directions between origin and destination with configurable travel mode, waypoints, alternatives, and routing preferences.     |
| `fetch_global_imagery_wms_map()`      | Request and render imagery from a Web Map Service using layer, bounding box, dimensions, CRS, and image-format parameters.                   |
| `fetch_global_imagery_map_services()` | Discover available global imagery map services and layer metadata.                                                                           |
| `fetch_global_imagery_mercator_map()` | Render global imagery in a Mercator-oriented map view using geographic bounds and projection settings.                                       |
| `fetch_google_geocoding()`            | Perform Google forward geocoding, reverse geocoding, or place lookup with optional language, region, result-type, and location-type filters. |
| `fetch_usgs_national_map()`           | Search USGS National Map datasets and downloadable products using bounding box, dataset, format, date, and paging criteria.                  |
| `fetch_usgs_sciencebase()`            | Search or retrieve USGS ScienceBase catalog items using text, item IDs, parent IDs, spatial filters, and paging controls.                    |

### Health

HealthData.gov, global health, CDC WONDER, and PubMed operations.

| Function                     | Purpose                                                                                                                                       |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `fetch_health_data()`        | Retrieve HealthData.gov Socrata metadata or rows using dataset IDs, SoQL selection/filtering, ordering, paging, and app-token authentication. |
| `fetch_global_health_data()` | Query WHO Global Health Observatory indicators and Athena API data using indicator, profile, filter, format, and paging parameters.           |
| `fetch_wonder()`             | Retrieve CDC WONDER dataset templates or submit structured WONDER query requests.                                                             |
| `load_pubmed()`              | Search PubMed and load matching biomedical literature into LangChain `Document` objects.                                                      |

### Web

Web fetching, crawling, loading, HTML extraction, scraping, GitHub loading, and image encoding.

| Function                        | Purpose                                                                                                                              |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `fetch_web_page()`              | Fetch an HTTP page, retain response/HTML state, and return Fonky's normalized `Result` wrapper.                                      |
| `convert_html_to_text()`        | Remove scripts, styles, markup, and repeated whitespace from raw HTML to produce compact plain text.                                 |
| `extract_web_title()`           | Extract and normalize the document title from supplied HTML.                                                                         |
| `extract_web_links()`           | Extract, normalize, deduplicate, and resolve HTTP(S) links relative to a base URL.                                                   |
| `extract_web_structured_data()` | Extract selected HTML structures—headings, paragraphs, lists, tables, articles, sections, links, or images—into labeled collections. |
| `crawl_web()`                   | Crawl a website with configurable page, depth, byte, timeout, and domain-boundary limits.                                            |
| `scrape_crawler_page()`         | Extract normalized content and metadata from a crawler-retrieved page.                                                               |
| `render_web_page()`             | Render JavaScript-dependent web content through Playwright before returning the resulting page content.                              |
| `load_web()`                    | Load one or more URLs into LangChain documents, optionally using recursive same-domain traversal.                                    |
| `load_web_recursive()`          | Recursively load documents from a seed URL to a bounded depth with optional same-domain filtering.                                   |
| `load_web_pages()`              | Load a fixed list of web pages into LangChain documents with timeout, progress, and failure-handling controls.                       |
| `load_github()`                 | Load repository files from GitHub into LangChain documents using repository, branch, file-filter, and authentication settings.       |
| `scrape_web_page()`             | Issue a synchronous HTTP request and return the Fonky `Result` wrapper for the retrieved page.                                       |
| `scraper_html_to_text()`        | Convert raw HTML into readable plain text using the scraper's markup-removal and whitespace-normalization logic.                     |
| `scrape_paragraphs()`           | Extract non-empty paragraph text from all `<p>` elements in a web page.                                                              |
| `scrape_lists()`                | Extract non-empty list-item text from all `<li>` elements in a web page.                                                             |
| `scrape_tables()`               | Flatten text from all table header and data cells across the page's HTML tables.                                                     |
| `scrape_articles()`             | Extract consolidated text blocks from HTML `<article>` elements.                                                                     |
| `scrape_headings()`             | Extract heading text from `<h1>` through `<h6>` elements.                                                                            |
| `scrape_divisions()`            | Extract readable text from HTML `<div>` elements.                                                                                    |
| `scrape_sections()`             | Extract readable text from HTML `<section>` elements.                                                                                |
| `scrape_blockquotes()`          | Extract readable text from HTML `<blockquote>` elements.                                                                             |
| `scrape_hyperlinks()`           | Extract populated `href` values from anchor elements.                                                                                |
| `scrape_images()`               | Extract populated `src` values from image elements.                                                                                  |
| `encode_image()`                | Read an image from disk and return its bytes as a Base64-encoded string.                                                             |

## 🧾 Requirements

Fonky uses the OpenAI Agents SDK for its public function-tool interface while retaining selected
LangChain packages internally for document ingestion, retrieval, `Document` objects, Google
integrations, and text splitting.

The dependency set must include the packages used by the rebuilt implementation and tool layer.

| Package                      | Purpose                                                                 |
|------------------------------|-------------------------------------------------------------------------|
| `openai-agents`              | OpenAI Agents SDK and `@function_tool`                                  |
| `pydantic`                   | Structured models and validation                                        |
| `requests`                   | HTTP client used by fetchers and scrapers                               |
| `pandas`                     | Tabular data handling                                                   |
| `numpy`                      | Numeric processing                                                      |
| `langchain-core`             | `Document` and core LangChain abstractions used internally              |
| `langchain-community`        | Community loaders and retrievers                                        |
| `langchain-text-splitters`   | Recursive document chunking                                             |
| `langchain-google-community` | Google-backed LangChain loaders                                         |
| `langchain-googledrive`      | Google Drive retriever support                                          |
| `nltk`                       | Tokenization, stop words, lexical processing, and frequency analysis    |
| `spacy`                      | NLP pipeline support                                                    |
| `sentence-transformers`      | Embeddings and semantic processing                                      |
| `scikit-learn`               | Vectorization, PCA, and similarity support                              |
| `textblob`                   | Text-processing utilities                                               |
| `tiktoken`                   | Tokenization and chunking support                                       |
| `python-docx`                | Word document processing                                                |
| `PyMuPDF`                    | PDF processing                                                          |
| `chromadb`                   | Chroma vector database integration                                      |
| `pinecone`                   | Pinecone vector integration                                             |
| `gensim`                     | Word2Vec and vector-processing support                                  |
| `jq`                         | Required by LangChain JSON loading                                      |
| `O365`                       | Required by OneDrive and SharePoint loaders                             |
| `extract-msg`                | Required by Outlook `.msg` loading                                      |
| `pypdf`                      | PDF loading                                                             |
| `docx2txt`                   | DOCX text extraction                                                    |
| `openpyxl`                   | Excel `.xlsx` support                                                   |
| `xlrd`                       | Legacy Excel `.xls` support                                             |
| `python-pptx`                | PowerPoint support                                                      |
| `unstructured`               | Office, HTML, Markdown, and mixed document parsing                      |
| `lxml`                       | XML/HTML parsing                                                        |
| `beautifulsoup4`             | HTML parsing and scraping                                               |
| `html5lib`                   | HTML parser backend                                                     |
| `markdown`                   | Markdown parsing                                                        |
| `nbformat`                   | Jupyter notebook parsing                                                |
| `pillow`                     | Image support                                                           |
| `rapidocr-onnxruntime`       | OCR support                                                             |
| `playwright`                 | Browser rendering                                                       |
| `crawl4ai`                   | Web crawling                                                            |
| `arxiv`                      | ArXiv API support                                                       |
| `wikipedia`                  | Wikipedia API support                                                   |
| `xmltodict`                  | XML-to-dictionary conversion                                            |
| `google-genai`               | Google GenAI SDK                                                        |
| `google-api-python-client`   | Google API client                                                       |
| `google-auth`                | Google authentication                                                   |
| `google-auth-oauthlib`       | Google OAuth support                                                    |
| `google-cloud-storage`       | Google Cloud Storage loaders                                            |
| `google-cloud-speech`        | Google Speech-to-Text loader                                            |
| `boto3`                      | AWS S3 integration                                                      |
| `botocore`                   | AWS low-level client dependency                                         |
| `astropy`                    | Astronomy and coordinate utilities                                      |
| `astroquery`                 | Astronomy service queries                                               |
| `sscws`                      | NASA SSC Web Services                                                   |
| `OWSLib`                     | WMS/global imagery support                                              |
| `cartopy`                    | Geospatial projections and map rendering                               |
| `matplotlib`                 | Plotting and map output                                                 |
| `grokipedia-api`             | Grokipedia client support                                               |

Install the complete dependency set from the project root:

```powershell
python -m pip install -r requirements.txt
python -m pip check
```

Install Playwright's Chromium runtime when browser-backed functionality is required:

```powershell
python -m playwright install chromium
```

The requirements file should reflect the rebuilt OpenAI Agents SDK tool layer and include
`openai-agents`, `nltk`, `spacy`, `jq`, `O365`, and `extract-msg` in addition to the retained
LangChain loader/retriever dependencies.

#### 📝 License

Fonky is distributed under the license defined in
[`LICENSE.txt`](https://github.com/is-leeroy-jenkins/fonky/blob/main/LICENSE.txt).
