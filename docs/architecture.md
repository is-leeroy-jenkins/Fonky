# Architecture

Fonky is organized as a flat Python module framework for data retrieval, document loading, web
extraction, text processing, exception logging, AI tool generation, and MkDocs-based API
documentation.

The architecture is intentionally modular. Each source file owns a clear responsibility, while
export modules provide cleaner import paths for related service groups.

## Architectural Purpose

Fonky is designed to solve a common integration problem:

```text
External data and documents are scattered across local files, APIs, websites, cloud stores, repositories, public data services, and archive systems.
```

Fonky provides a common runtime pattern:

```text
Retrieve or load source content
    -> Normalize the result
    -> Represent content as documents, dictionaries, models, text, or tool results
    -> Process, split, serialize, or expose the result to downstream workflows
```

The framework supports:

| Capability               | Architectural role                                                                                                         |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| Document loading         | Converts local, web, office, PDF, notebook, cloud, and repository sources into document objects.                           |
| API fetching             | Retrieves structured data from public, scientific, government, environmental, demographic, health, and geospatial sources. |
| Web extraction           | Parses HTML and extracts text, links, images, headings, tables, and metadata.                                              |
| Text processing          | Cleans, normalizes, tokenizes, chunks, vectorizes, and prepares text for analysis or retrieval.                            |
| AI tool generation       | Converts Python functions and object methods into structured tool definitions.                                             |
| Exception logging        | Wraps handled exceptions and writes failure metadata to a SQLite database.                                                 |
| Documentation generation | Renders Google-style source docstrings through MkDocs and mkdocstrings.                                                    |

## Repository Structure

Fonky currently uses a flat source layout at the repository root.

```text
Fonky/
|-- mkdocs.yml
|-- README.md
|-- requirements.txt
|-- docs/
|   |-- index.md
|   |-- getting-started.md
|   |-- configuration.md
|   |-- architecture.md
|   |-- logging.md
|   |-- usage.md
|   |-- user-guide.md
|   |-- development.md
|   |-- github-pages.md
|   |-- api/
|   |   |-- index.md
|   |   |-- archives.md
|   |   |-- astronomical.md
|   |   |-- boogr.md
|   |   |-- cloud.md
|   |   |-- config.md
|   |   |-- core.md
|   |   |-- demographic.md
|   |   |-- documents.md
|   |   |-- environmental.md
|   |   |-- fetchers.md
|   |   |-- geospatial.md
|   |   |-- health.md
|   |   |-- loaders.md
|   |   |-- models.md
|   |   |-- processors.md
|   |   |-- scrapers.md
|   |   +-- web.md
|   |-- stylesheets/
|   |   +-- extra.css
|   +-- javascripts/
|       +-- extra.js
|-- __init__.py
|-- archives.py
|-- astronomical.py
|-- boogr.py
|-- cloud.py
|-- config.py
|-- core.py
|-- demographic.py
|-- documents.py
|-- environmental.py
|-- fetchers.py
|-- geospatial.py
|-- health.py
|-- loaders.py
|-- models.py
|-- processors.py
|-- scrapers.py
+-- web.py
```

The current flat layout means imports should use root-level module names:

```python
from loaders import TextLoader
from models import ToolDef
from processors import TextParser
```

The API reference should also use flat module directives inside `docs/api/*.md` files:

```text
::: loaders
::: models
::: processors
```

Do not use `fonky.loaders` unless the project is later moved into an importable package folder named
`fonky`.

## High-Level Runtime Flow

Fonky's runtime flow is:

```text
External source
    -> Loader, fetcher, or scraper
    -> Document object, dictionary, list, text, or model
    -> Processor, serializer, or ToolDef
    -> Notebook, application, retrieval workflow, API service, or AI tool call
```

Example document flow:

```text
PDF, text file, Word file, CSV file, cloud object, or web page
    -> Loader class
    -> Document objects
    -> Split or process documents
    -> Retrieval, search, summarization, or analysis workflow
```

Example API flow:

```text
Method arguments
    -> Fetcher class
    -> Request parameters
    -> External API or public data service
    -> Normalized structured response
```

Example AI tooling flow:

```text
Python function or class method
    -> ToolDef
    -> Provider-compatible schema
    -> Model-selected tool call
    -> Fonky callable execution
    -> JSON-safe result envelope
```

## Architectural Layers

Fonky can be understood as six layers:

```text
Configuration layer
    -> Core and logging layer
    -> Source access layer
    -> Processing layer
    -> Model and tool layer
    -> Documentation layer
```

| Layer                  | Modules                                                   | Responsibility                                                                                              |
| ---------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Configuration layer    | `config.py`                                               | Environment variables, API keys, path constants, logging paths, service descriptions, and helper functions. |
| Core and logging layer | `core.py`, `boogr.py`                                     | Base abstractions, exception wrapper, and SQLite-backed exception logging.                                  |
| Source access layer    | `loaders.py`, `fetchers.py`, `scrapers.py`, `archives.py` | Load documents, retrieve API data, scrape web content, and access archive sources.                          |
| Processing layer       | `processors.py`                                           | Clean, normalize, tokenize, chunk, vectorize, and prepare text.                                             |
| Model and tool layer   | `models.py`                                               | Serialize results and expose callables as AI-compatible tools.                                              |
| Documentation layer    | `docs/`, `mkdocs.yml`                                     | Render manual documentation and source-generated API reference pages.                                       |

## Configuration Layer

The configuration layer is centralized in `config.py`.

It defines:

| Configuration type   | Examples                                                                                  |
| -------------------- | ----------------------------------------------------------------------------------------- |
| Path constants       | `BASE_DIR`, `ROOT_DIR`, `LOG_DIR`, `LOG_PATH`, `LOG_FILE`                                 |
| API keys             | `NASA_API_KEY`, `GOOGLE_API_KEY`, `OPENAI_API_KEY`, `GOVINFO_API_KEY`, `CONGRESS_API_KEY` |
| Cloud settings       | Google Cloud, Google Drive, Microsoft, AWS, and storage-related settings                  |
| Service descriptions | Provider and loader descriptions used by modules and documentation                        |
| Helper functions     | `get_bool`, `get_int`, `get_float`, `get_path`, `get_text`, `throw_if`                    |

Configuration values flow from environment variables into module-level constants:

```text
PowerShell environment variable
    -> os.getenv(...)
    -> config.py constant
    -> loader, fetcher, scraper, processor, model, or logger
```

## Logging Layer

The logging layer is centralized in `boogr.py` and configured by `config.py`.

| Class    | Role                                                      |
| -------- | --------------------------------------------------------- |
| `Error`  | Wraps source exceptions with normalized project metadata. |
| `Logger` | Writes exception records to a SQLite database.            |

The logger uses:

```text
LOG_DIR
LOG_PATH
LOG_FILE
```

Required exception flow:

```text
Handled exception
    -> Error wrapper
    -> module, cause, method, message, info, trace
    -> Logger.write(...)
    -> SQLite Exceptions table
    -> Wrapped exception raised to caller
```

Required source pattern:

```python
except Exception as e:
    exception = Error(e)
    exception.module = "loaders"
    exception.cause = "TextLoader"
    exception.method = "load(self, path: str, encoding: Optional[str]=None) -> List[Document]"
    Logger().write(exception)
    raise exception
```

## Loader Layer

The loader layer is centralized in `loaders.py`.

It wraps document-loading functionality for local files, web content, cloud stores, office
documents, notebooks, repositories, archives, and provider-backed sources.

Representative loader groups:

| Loader group            | Source type                                                                  |
| ----------------------- | ---------------------------------------------------------------------------- |
| Text loaders            | Plain text and Markdown files                                                |
| Structured file loaders | CSV, JSON, XML, and Excel files                                              |
| Office loaders          | Word, PowerPoint, Outlook, and email files                                   |
| PDF loaders             | PDF text and page extraction                                                 |
| Web loaders             | Web pages, sitemap content, and recursive URL loading                        |
| Notebook loaders        | Jupyter notebooks                                                            |
| Cloud loaders           | Google Drive, Google Cloud Storage, AWS S3, OneDrive, and SharePoint sources |
| Archive loaders         | ArXiv, Wikipedia, PubMed, and other archive-backed sources                   |

Typical loader flow:

```text
Path, URL, cloud object, or query
    -> Loader class
    -> Underlying provider or LangChain loader
    -> List of document objects
    -> Optional split operation
```

## Fetcher Layer

The fetcher layer is centralized in `fetchers.py`.

Fetchers retrieve structured data from external APIs and public services.

Fetcher responsibilities include:

| Responsibility       | Description                                                                  |
| -------------------- | ---------------------------------------------------------------------------- |
| Validate inputs      | Required method arguments are checked before a request.                      |
| Build parameters     | Request parameters are assembled from arguments and configuration constants. |
| Execute calls        | HTTP requests or provider client calls are performed.                        |
| Normalize responses  | JSON, XML, CSV, text, or document-like payloads are normalized.              |
| Log handled failures | Exceptions are wrapped with `Error` and written with `Logger`.               |

Representative service areas:

| Area                | Examples                                                  |
| ------------------- | --------------------------------------------------------- |
| Government data     | GovInfo, Congress, Data.gov, Census                       |
| Environmental data  | EPA, AirNow, OpenAQ, PurpleAir, NASA FIRMS                |
| Geospatial data     | NOAA, USGS, tides, water data, national map, geocoding    |
| Astronomy and space | NASA, DONKI, near-earth objects, satellite data, sky maps |
| Health data         | WHO, CDC WONDER, health data services                     |
| News and web data   | News APIs, search APIs, and public web sources            |
| Cloud and storage   | Google, Microsoft, AWS, and related integrations          |

Typical fetcher flow:

```text
Method arguments
    -> Configuration constants and API keys
    -> Request parameter dictionary
    -> HTTP request or client call
    -> Normalized response
```

## Scraper Layer

The scraper layer is centralized in `scrapers.py`.

It handles web extraction and parsing.

Typical scraper capabilities include:

| Capability               | Description                                                              |
| ------------------------ | ------------------------------------------------------------------------ |
| HTML-to-text conversion  | Extract readable text from HTML.                                         |
| Link extraction          | Extract links from web content.                                          |
| Heading extraction       | Extract page heading structure.                                          |
| Table extraction         | Extract HTML table data.                                                 |
| Image extraction         | Extract image references and metadata.                                   |
| Browser-backed retrieval | Use browser automation for dynamic pages when required.                  |
| Normalization            | Return structured dictionaries or text values for downstream processing. |

Typical scraper flow:

```text
URL or HTML
    -> HTTP fetcher or browser renderer
    -> HTML parser
    -> Text, links, tables, headings, images, or metadata
```

## Processor Layer

The processor layer is centralized in `processors.py`.

It prepares raw text and loaded documents for analysis, retrieval, embedding, search, or AI tool
output.

Processor responsibilities include:

| Responsibility          | Examples                                                                            |
| ----------------------- | ----------------------------------------------------------------------------------- |
| Text cleaning           | Remove HTML, XML, Markdown, numbers, symbols, fragments, stopwords, and formatting. |
| Normalization           | Normalize spacing, casing, punctuation, and encoding.                               |
| Tokenization            | Split text into words, sentences, paragraphs, pages, and chunks.                    |
| NLP operations          | Stemming, lemmatization, POS tagging, and named entity extraction where supported.  |
| Vector preparation      | Vocabulary generation, bag-of-words, TF-IDF, and Word2Vec-style utilities.          |
| Semantic search support | Encode sentences and search semantically where dependencies are available.          |

Typical processor flow:

```text
Raw text or loaded documents
    -> Text parser or NLP parser
    -> Cleaning, tokenization, chunking, or vectorization
    -> Analysis-ready text or structures
```

## Model and Tool Layer

The model and tool layer is centralized in `models.py`.

Its primary role is to convert Python functions and object methods into structured AI-callable
tools.

Representative concepts:

| Concept         | Purpose                                                                 |
| --------------- | ----------------------------------------------------------------------- |
| `ToolDef`       | Describes and executes a callable tool.                                 |
| `from_callable` | Builds a tool from a Python function.                                   |
| `from_method`   | Builds a tool from an object method.                                    |
| `to_openai`     | Exports an OpenAI-compatible tool schema.                               |
| `to_gemini`     | Exports a Gemini-compatible tool schema.                                |
| `to_grok`       | Exports a Grok-compatible tool schema.                                  |
| `call`          | Executes the wrapped callable and returns a structured result envelope. |

Typical tool flow:

```text
Python function or class method
    -> ToolDef.from_callable(...) or ToolDef.from_method(...)
    -> JSON-schema-like parameter model
    -> Provider-compatible schema
    -> Structured call result
```

Tool call result shape:

```text
{
    "ok": true or false,
    "name": "tool_name",
    "data": result payload or null,
    "error": error payload or null,
    "metadata": tool metadata
}
```

## Archive Layer

The archive layer is centralized in `archives.py`.

It groups public research, publication, and knowledge-source access.

Typical archive services include:

| Service          | Purpose                                           |
| ---------------- | ------------------------------------------------- |
| ArXiv            | Scholarly article search and retrieval.           |
| Wikipedia        | Encyclopedia search and page retrieval.           |
| PubMed           | Biomedical literature search.                     |
| GovInfo          | Government publication access.                    |
| Internet Archive | Archive and collection retrieval where supported. |

Typical archive flow:

```text
Search term or lookup value
    -> Archive wrapper
    -> External archive source
    -> Document-like result set
```

## Export Modules

Fonky includes small export modules that group related classes for cleaner imports.

| Export module      | Role                                         |
| ------------------ | -------------------------------------------- |
| `documents.py`     | Exports document loader classes.             |
| `web.py`           | Exports web scraping and extraction classes. |
| `cloud.py`         | Exports cloud loader classes.                |
| `astronomical.py`  | Exports astronomy and space-science classes. |
| `demographic.py`   | Exports demographic and population classes.  |
| `environmental.py` | Exports environmental data classes.          |
| `geospatial.py`    | Exports geospatial data classes.             |
| `health.py`        | Exports health data classes.                 |

Example imports:

```python
from documents import TextLoader, PdfLoader
from web import WebExtractor
from cloud import AwsBucketLoader, GoogleBucketLoader
```

Export modules should remain thin. They should not duplicate implementation logic from the main
modules.

## Documentation Architecture

The documentation system has two page types.

| Page type    | Source          | Purpose                                                                                  |
| ------------ | --------------- | ---------------------------------------------------------------------------------------- |
| Manual pages | `docs/*.md`     | Explain setup, configuration, architecture, logging, usage, development, and deployment. |
| API pages    | `docs/api/*.md` | Render Python module docstrings, classes, methods, and signatures through mkdocstrings.  |

Manual pages should not contain live mkdocstrings directives.

Correct manual-page behavior:

```text
docs/architecture.md describes the directive as an example inside a code block.
```

Incorrect manual-page behavior:

```text
docs/architecture.md contains a live line beginning with ::: loaders.
```

Only API pages should contain live directives.

Correct API-page behavior:

```text
docs/api/loaders.md contains a live directive for loaders.
```

## API Documentation Flow

The API documentation flow is:

```text
Python source file
    -> Google-style docstrings
    -> docs/api/module.md with mkdocstrings directive
    -> mkdocs build
    -> Rendered API reference page
```

A valid source method docstring uses Google-style sections:

```python
def load(self, path: str, encoding: Optional[str] = None) -> List[Document]:
    """Load a plain-text file.

    Purpose:
        Loads a local plain-text file into document objects.

    Args:
        path (str): Path to the text file.
        encoding (Optional[str]): Optional file encoding.

    Returns:
        List[Document]: Loaded document objects.
    """
```

A valid API page contains a live directive:

```text
# Loaders API

::: loaders
```

That directive belongs in `docs/api/loaders.md`, not in top-level manual pages.

## Error Handling Architecture

Fonky uses explicit exception wrapping and logging instead of silent failure.

Required pattern:

```python
except Exception as e:
    exception = Error(e)
    exception.module = "fetchers"
    exception.cause = "ClassName"
    exception.method = "method_name(self, arg: type) -> return_type"
    Logger().write(exception)
    raise exception
```

This design provides:

| Benefit                 | Description                                                                      |
| ----------------------- | -------------------------------------------------------------------------------- |
| Consistent metadata     | Each handled failure records module, cause, method, message, and traceback data. |
| Persistent audit trail  | Exceptions are written to SQLite for later inspection.                           |
| Debuggable failure path | Exceptions are still raised after logging.                                       |
| Source visibility       | Logging behavior remains visible in each handler.                                |

## Validation Architecture

Every source or documentation change should be validated in this order:

```text
1. Compile Python source.
2. Validate imports.
3. Confirm API pages contain mkdocstrings directives.
4. Confirm manual pages do not contain live directives.
5. Build MkDocs.
6. Fix Griffe, import, autorefs, and broken-link warnings.
7. Serve locally.
8. Review rendered pages.
9. Deploy to GitHub Pages.
```

Command set:

```powershell
python -m compileall .
Select-String -Path .\docs\api\*.md -Pattern "^:::\s+[A-Za-z_]"
Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"
mkdocs build
mkdocs serve
```

Expected directive behavior:

```text
docs/api/*.md -> contains live mkdocstrings directives
docs/*.md     -> contains no live mkdocstrings directives
```

## Common Architecture Decisions

### Flat source layout

Current layout:

```text
loaders.py
fetchers.py
processors.py
models.py
```

Use API directives like this inside `docs/api/*.md`:

```text
::: loaders
```

### Package source layout

A future package layout might be:

```text
fonky/
|-- loaders.py
|-- fetchers.py
|-- processors.py
+-- models.py
```

Only after that change should directives use package paths:

```text
::: fonky.loaders
```

### Export modules

Export modules provide convenient import groupings:

```python
from documents import TextLoader
from web import WebExtractor
from cloud import AwsBucketLoader
```

They should not contain independent business logic.

## Architectural Baseline

A healthy Fonky architecture has the following properties:

```text
- Source modules compile.
- Configuration imports without making external service calls.
- Logging writes handled exceptions to SQLite.
- Loaders return document objects.
- Fetchers return normalized structured payloads.
- Scrapers return parsed web content structures.
- Processors return cleaned, tokenized, chunked, or vector-ready text.
- Models expose callables as provider-compatible tools.
- Export modules provide clean import paths.
- API docs render source docstrings through mkdocstrings.
- Manual docs explain setup, configuration, architecture, logging, usage, development, and deployment.
```

