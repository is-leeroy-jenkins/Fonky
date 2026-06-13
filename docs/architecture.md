# ðŸ§± Architecture

Fonky is organized as a flat Python module framework for data retrieval, document loading, web
extraction, text processing, exception logging, and agent-ready tool orchestration.

The architecture is intentionally modular. Each major source file owns a specific responsibility,
while export modules provide cleaner import paths for related service groups.



## ðŸŽ¯ Architectural Purpose

Fonky is designed to solve a common integration problem:

```text id="architecture_problem"
External data and documents are scattered across files, APIs, websites, cloud stores, repositories, and public data services.
```

Fonky provides a common runtime pattern:

```text id="architecture_solution"
Retrieve or load source content
    â†“
Normalize the result
    â†“
Represent content as documents, dictionaries, models, or tool results
    â†“
Process, split, serialize, or expose the result to downstream workflows
```

The framework supports:

| Capability               | Architectural role                                                                                                         |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| Document loading         | Converts local, cloud, repository, web, and office sources into LangChain `Document` objects.                              |
| API fetching             | Retrieves structured data from public, scientific, government, environmental, demographic, health, and geospatial sources. |
| Web extraction           | Parses HTML and extracts text, links, images, headings, tables, metadata, and browser-rendered content.                    |
| Text processing          | Cleans, tokenizes, chunks, vectorizes, and prepares text for search, retrieval, or analysis.                               |
| Tool orchestration       | Converts Python callables and class methods into structured tool definitions.                                              |
| Exception logging        | Wraps handled exceptions and writes them to a SQLite database.                                                             |
| Documentation generation | Renders Google-style docstrings through MkDocs and mkdocstrings.                                                           |



## ðŸ“ Repository-Level Structure

Fonky currently uses a flat source layout at the repository root.

```text id="architecture_project_layout"
Fonky/
â”œâ”€â”€ mkdocs.yml
â”œâ”€â”€ README.md
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ index.md
â”‚   â”œâ”€â”€ getting-started.md
â”‚   â”œâ”€â”€ configuration.md
â”‚   â”œâ”€â”€ architecture.md
â”‚   â”œâ”€â”€ logging.md
â”‚   â”œâ”€â”€ usage.md
â”‚   â”œâ”€â”€ user-guide.md
â”‚   â”œâ”€â”€ development.md
â”‚   â”œâ”€â”€ github-pages.md
â”‚   â”œâ”€â”€ api/
â”‚   â”‚   â”œâ”€â”€ index.md
â”‚   â”‚   â”œâ”€â”€ archives.md
â”‚   â”‚   â”œâ”€â”€ astronomical.md
â”‚   â”‚   â”œâ”€â”€ boogr.md
â”‚   â”‚   â”œâ”€â”€ cloud.md
â”‚   â”‚   â”œâ”€â”€ config.md
â”‚   â”‚   â”œâ”€â”€ core.md
â”‚   â”‚   â”œâ”€â”€ demographic.md
â”‚   â”‚   â”œâ”€â”€ documents.md
â”‚   â”‚   â”œâ”€â”€ environmental.md
â”‚   â”‚   â”œâ”€â”€ fetchers.md
â”‚   â”‚   â”œâ”€â”€ geospatial.md
â”‚   â”‚   â”œâ”€â”€ health.md
â”‚   â”‚   â”œâ”€â”€ loaders.md
â”‚   â”‚   â”œâ”€â”€ models.md
â”‚   â”‚   â”œâ”€â”€ processors.md
â”‚   â”‚   â”œâ”€â”€ scrapers.md
â”‚   â”‚   â””â”€â”€ web.md
â”‚   â””â”€â”€ stylesheets/
â”‚       â””â”€â”€ extra.css
â”œâ”€â”€ __init__.py
â”œâ”€â”€ archives.py
â”œâ”€â”€ astronomical.py
â”œâ”€â”€ boogr.py
â”œâ”€â”€ cloud.py
â”œâ”€â”€ config.py
â”œâ”€â”€ core.py
â”œâ”€â”€ demographic.py
â”œâ”€â”€ documents.py
â”œâ”€â”€ environmental.py
â”œâ”€â”€ fetchers.py
â”œâ”€â”€ geospatial.py
â”œâ”€â”€ health.py
â”œâ”€â”€ loaders.py
â”œâ”€â”€ models.py
â”œâ”€â”€ processors.py
â”œâ”€â”€ scrapers.py
â””â”€â”€ web.py
```

!!! note
If the source is later moved into a package directory named `fonky/`, update API reference
directives from `::: loaders` to `::: loaders`, and update examples from
`from loaders import TextLoader` to `from fonky.loaders import TextLoader`.



## ðŸ” High-Level Runtime Flow

The core runtime flow is:

```text id="runtime_flow"
External source
    â†“
Fetcher, scraper, or loader
    â†“
Document object, structured dictionary, list, text, or model
    â†“
Processor, serializer, or ToolDef
    â†“
Notebook, application, API service, retrieval workflow, or AI tool call
```

Examples:

```text id="runtime_flow_pdf"
PDF file
    â†“
PdfLoader
    â†“
LangChain Document objects
    â†“
split documents
    â†“
retrieval or analysis workflow
```

```text id="runtime_flow_web"
Web page
    â†“
WebLoader or WebExtractor
    â†“
clean text, links, tables, metadata
    â†“
structured application output
```

```text id="runtime_flow_tool"
Python method
    â†“
ToolDef.from_method(...)
    â†“
OpenAI / Gemini / Grok-compatible schema
    â†“
tool-calling workflow
```



## ðŸ§© Architectural Layers

Fonky can be understood as six layers:

```text id="architecture_layers"
Configuration layer
    â†“
Core and logging layer
    â†“
Source access layer
    â†“
Processing layer
    â†“
Model and tool layer
    â†“
Documentation layer
```

| Layer                  | Modules                                                   | Responsibility                                                                        |
| ---------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Configuration layer    | `config.py`                                               | Environment variables, API keys, path constants, logging paths, service descriptions. |
| Core and logging layer | `core.py`, `boogr.py`                                     | Base abstractions, exception wrapper, SQLite-backed logging.                          |
| Source access layer    | `fetchers.py`, `loaders.py`, `scrapers.py`, `archives.py` | Retrieve external data, load documents, scrape web content, query archives.           |
| Processing layer       | `processors.py`                                           | Clean, normalize, tokenize, chunk, vectorize, and prepare text.                       |
| Model and tool layer   | `models.py`                                               | Serialize results and expose methods as provider-compatible tools.                    |
| Documentation layer    | `docs/`, `mkdocs.yml`                                     | Render Markdown pages and source docstrings into a documentation site.                |



## âš™ï¸ Configuration Layer

The configuration layer is centralized in:

```text id="configuration_layer_file"
config.py
```

It defines:

| Configuration type   | Examples                                                                                  |
| -------------------- | ----------------------------------------------------------------------------------------- |
| Path constants       | `BASE_DIR`, `ROOT_DIR`, `LOG_DIR`, `LOG_PATH`, `LOG_FILE`                                 |
| API keys             | `NASA_API_KEY`, `GOOGLE_API_KEY`, `OPENAI_API_KEY`, `GOVINFO_API_KEY`, `CONGRESS_API_KEY` |
| Cloud settings       | Google Cloud, Google Drive, Microsoft, AWS-related variables                              |
| Service descriptions | API and loader descriptions used by documentation and UI layers                           |
| Helper functions     | `get_bool`, `get_int`, `get_float`, `get_path`, `get_text`, `throw_if`                    |

Configuration is read at import time through environment variables.

Example flow:

```text id="configuration_flow"
PowerShell environment variable
    â†“
os.getenv(...)
    â†“
config.py constant
    â†“
fetcher, loader, scraper, logger, or model
```



## ðŸªµ Logging Layer

The logging layer is centralized in:

```text id="logging_layer_files"
boogr.py
config.py
```

`boogr.py` provides:

| Class    | Role                                                    |
| -------- | ------------------------------------------------------- |
| `Error`  | Wraps source exceptions with project-specific metadata. |
| `Logger` | Writes exception records to a SQLite database.          |

The logger uses configuration values from `config.py`:

```text id="logging_config_values"
LOG_DIR
LOG_PATH
LOG_FILE
```

Required exception pattern:

```python id="architecture_exception_pattern"
except Exception as e:
	exception = Error(e)
	exception.module = "loaders"
	exception.cause = "TextLoader"
	exception.method = "load(self, path: str, encoding: Optional[str]=None) -> List[Document]"
	Logger().write(exception)
	raise exception
```

Architectural purpose:

```text id="logging_architecture_purpose"
Handled exception
    â†“
Error wrapper
    â†“
module, cause, method metadata
    â†“
Logger.write(...)
    â†“
SQLite Exceptions table
```



## ðŸ“„ Loader Layer

The loader layer is centralized in:

```text id="loader_layer_file"
loaders.py
```

It wraps LangChain and community document loaders to load different source types into `Document`
objects.

Representative loaders:

| Loader                  | Source type                         |
| ----------------------- | ----------------------------------- |
| `TextLoader`            | Plain-text files                    |
| `CsvLoader`             | CSV files                           |
| `PdfLoader`             | PDF files                           |
| `PdfReader`             | PDF reading wrapper                 |
| `ExcelLoader`           | Excel workbooks                     |
| `WordLoader`            | Word documents                      |
| `MarkdownLoader`        | Markdown files                      |
| `HtmlLoader`            | HTML files                          |
| `WebLoader`             | Web pages and recursive URL loading |
| `JsonLoader`            | JSON and JSON Lines files           |
| `XmlLoader`             | XML files and XPath access          |
| `EmailLoader`           | Email files                         |
| `OutlookLoader`         | Outlook message files               |
| `PowerPointLoader`      | PowerPoint files                    |
| `JupyterNotebookLoader` | Jupyter notebooks                   |
| `GoogleDriveLoader`     | Google Drive files and folders      |
| `GoogleCloudFileLoader` | Google Cloud Storage files          |
| `GoogleBucketLoader`    | Google Cloud Storage buckets        |
| `AwsFileLoader`         | AWS S3 files                        |
| `AwsBucketLoader`       | AWS S3 buckets                      |
| `OneDriveDocLoader`     | Microsoft OneDrive documents        |
| `SpfxLoader`            | SharePoint document libraries       |
| `ArXivLoader`           | ArXiv document search               |
| `WikiLoader`            | Wikipedia document search           |
| `PubMedSearchLoader`    | PubMed document search              |

Typical loader flow:

```text id="loader_flow"
Path, URL, cloud object, or query
    â†“
Loader class
    â†“
LangChain loader instance
    â†“
List[Document]
    â†“
split_documents(...)
```



## ðŸ”Œ Fetcher Layer

The fetcher layer is centralized in:

```text id="fetcher_layer_file"
fetchers.py
```

Fetchers retrieve structured data from external APIs and public services.

Fetcher responsibilities include:

| Responsibility           | Description                                                                        |
| ------------------------ | ---------------------------------------------------------------------------------- |
| Validate request inputs  | Required parameters are checked before making a request.                           |
| Build request parameters | Parameters are assembled from method arguments and configuration constants.        |
| Execute external calls   | Requests are sent to public or credential-backed services.                         |
| Normalize responses      | JSON, XML, CSV, text, or document-like payloads are normalized for downstream use. |
| Log handled failures     | Exceptions are wrapped and written through `Logger`.                               |

Representative service areas:

| Service area        | Examples                                                  |
| ------------------- | --------------------------------------------------------- |
| Government data     | GovInfo, Congress, Data.gov, Census                       |
| Environmental data  | EPA, AirNow, OpenAQ, PurpleAir, NASA FIRMS                |
| Geospatial data     | NOAA, USGS, tides, water data, national map, geocoding    |
| Astronomy and space | NASA, DONKI, near-earth objects, satellite data, sky maps |
| Health data         | WHO, CDC WONDER, health data services                     |
| News and web data   | News APIs, search APIs, public web sources                |
| Cloud and storage   | Google, Microsoft, AWS-related integrations               |

Typical fetcher flow:

```text id="fetcher_flow"
Method arguments
    â†“
Configuration constants and API keys
    â†“
Request parameter dictionary
    â†“
HTTP request or client call
    â†“
Normalized response
```



## ðŸ•¸ï¸ Scraper Layer

The scraper layer is centralized in:

```text id="scraper_layer_file"
scrapers.py
```

It handles web extraction and parsing.

Typical scraper capabilities include:

| Capability               | Description                                                              |
| ------------------------ | ------------------------------------------------------------------------ |
| HTML-to-text conversion  | Extract readable text from HTML.                                         |
| Link extraction          | Extract absolute or resolved links.                                      |
| Heading extraction       | Extract heading structure.                                               |
| Table extraction         | Extract HTML table data.                                                 |
| Image extraction         | Extract image references and metadata.                                   |
| Browser-backed retrieval | Use browser automation for dynamic pages when needed.                    |
| Normalization            | Return structured dictionaries or text values for downstream processing. |

Typical scraper flow:

```text id="scraper_flow"
URL or HTML
    â†“
Fetcher or browser renderer
    â†“
HTML parser
    â†“
Text, links, tables, headings, images, or metadata
```



## ðŸ§¹ Processor Layer

The processor layer is centralized in:

```text id="processor_layer_file"
processors.py
```

It prepares raw text and loaded documents for analysis, retrieval, embedding, or tool output.

Processor responsibilities include:

| Responsibility          | Examples                                                                                |
| ----------------------- | --------------------------------------------------------------------------------------- |
| Text cleaning           | Remove HTML, XML, Markdown, numbers, symbols, encodings, headers, fragments, stopwords. |
| Normalization           | Normalize spacing, casing, punctuation, and formatting.                                 |
| Tokenization            | Split text into words, sentences, paragraphs, pages, and chunks.                        |
| NLP operations          | Stemming, lemmatization, POS tagging, named entity recognition.                         |
| Vector preparation      | Vocabulary, bag-of-words, TF-IDF, Word2Vec-style utilities.                             |
| Semantic search support | Encode sentences and search semantically where dependencies are available.              |

Typical processor flow:

```text id="processor_flow"
Raw text or loaded documents
    â†“
TextParser or NltkParser
    â†“
cleaning, tokenization, chunking, vectorization
    â†“
analysis-ready text or structures
```



## ðŸ§© Model and Tool Layer

The model and tool layer is centralized in:

```text id="model_layer_file"
models.py
```

It provides structured models and tool definitions.

Primary responsibility:

```text id="model_layer_responsibility"
Convert Python functions and methods into structured tool definitions that can be called directly or exported to provider-specific tool schemas.
```

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

```text id="tool_flow"
Python function or class method
    â†“
ToolDef.from_callable(...) or ToolDef.from_method(...)
    â†“
JSON-schema-like parameter model
    â†“
provider-compatible schema
    â†“
structured call result
```

Tool call result shape:

```text id="tool_result_shape"
{
    "ok": true or false,
    "name": "tool_name",
    "data": result payload or null,
    "error": error payload or null,
    "metadata": tool metadata
}
```



## ðŸ“š Archive Layer

The archive layer is centralized in:

```text id="archive_layer_file"
archives.py
```

It groups public research and knowledge-source access.

Typical archive services include:

| Service          | Purpose                                           |
| ---------------- | ------------------------------------------------- |
| ArXiv            | Scholarly article search and retrieval.           |
| Wikipedia        | Encyclopedia search and page retrieval.           |
| PubMed           | Biomedical literature search.                     |
| GovInfo          | Government publication access.                    |
| Internet Archive | Archive and collection retrieval where supported. |

Typical archive flow:

```text id="archive_flow"
Question or search term
    â†“
Archive wrapper
    â†“
External source query
    â†“
Document-like result set
```



## ðŸ“¦ Export Modules

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

Example import pattern:

```python id="export_import_pattern"
from documents import TextLoader, PdfLoader
from web import WebExtractor
from cloud import AwsBucketLoader, GoogleBucketLoader
```

If the project is moved into a package folder:

```python id="package_export_import_pattern"
from fonky.documents import TextLoader, PdfLoader
from fonky.web import WebExtractor
from fonky.cloud import AwsBucketLoader, GoogleBucketLoader
```



## ðŸ§¾ Documentation Architecture

The documentation system has two types of pages:

| Page type    | Source          | Purpose                                                                                  |
| ------------ | --------------- | ---------------------------------------------------------------------------------------- |
| Manual pages | `docs/*.md`     | Explain usage, setup, architecture, configuration, logging, development, and deployment. |
| API pages    | `docs/api/*.md` | Render Python module docstrings, classes, methods, and signatures through mkdocstrings.  |

Manual pages include:

```text id="manual_pages"
docs/index.md
docs/getting-started.md
docs/configuration.md
docs/architecture.md
docs/logging.md
docs/usage.md
docs/user-guide.md
docs/development.md
docs/github-pages.md
```

API pages include:

```text id="api_pages_architecture"
docs/api/archives.md
docs/api/astronomical.md
docs/api/boogr.md
docs/api/cloud.md
docs/api/config.md
docs/api/core.md
docs/api/demographic.md
docs/api/documents.md
docs/api/environmental.md
docs/api/fetchers.md
docs/api/geospatial.md
docs/api/health.md
docs/api/loaders.md
docs/api/models.md
docs/api/processors.md
docs/api/scrapers.md
docs/api/web.md
```

Each API page must contain a mkdocstrings directive.

Flat layout example:

```markdown id="api_directive_flat_architecture"
# Loaders API

`::: loaders`
```

Package layout example:

```markdown id="api_directive_package_architecture"
# Loaders API

`::: loaders`
```



## ðŸ” Documentation Generation Flow

The API documentation flow is:

```text id="api_documentation_flow"
Python source file
    â†“
Google-style docstrings
    â†“
docs/api/module.md with mkdocstrings directive
    â†“
mkdocs build
    â†“
Rendered API reference page
```

A valid source method docstring:

```python id="valid_source_docstring_architecture"
def load(self, path: str, encoding: Optional[str] = None) -> List[Document]:
	"""Load a plain-text file.

	Purpose:
		Loads a local plain-text file into LangChain Document objects.

	Args:
		path (str): Path to the text file.
		encoding (Optional[str]): Optional file encoding.

	Returns:
		List[Document]: Loaded LangChain Document objects.
	"""
```

A valid API page:

```markdown id="valid_api_page_architecture"
# Loaders API

`::: loaders`
```

A valid `mkdocs.yml` plugin configuration:

```yaml id="valid_mkdocstrings_architecture"
plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths:
            - .
          options:
            docstring_style: google
            show_source: true
            show_root_heading: true
            show_root_full_path: false
            show_signature: true
            show_signature_annotations: true
            separate_signature: true
            merge_init_into_class: false
            members_order: source
            filters:
              - "!^_"
            heading_level: 2
```



## ðŸ›¡ï¸ Error Handling Architecture

Fonky uses explicit exception wrapping and logging instead of silent failure.

Required pattern:

```python id="error_architecture_pattern"
except Exception as e:
	exception = Error(e)
	exception.module = "fetchers"
	exception.cause = "ClassName"
	exception.method = "method_name(self, arg: type) -> return_type"
	Logger().write(exception)
	raise exception
```

This design provides:

| Benefit                   | Description                                                                   |
| ------------------------- | ----------------------------------------------------------------------------- |
| Consistent metadata       | Every handled failure records module, cause, method, message, and trace data. |
| Persistent audit trail    | Exceptions are written to SQLite for later inspection.                        |
| Debuggable failure path   | Exceptions are still raised after logging.                                    |
| Documentation consistency | Logging behavior is visible in source and API reference.                      |



## ðŸ§ª Validation Architecture

Every source or documentation change should be validated in this order:

```text id="validation_architecture_order"
1. Compile Python source.
2. Validate imports.
3. Confirm API pages contain mkdocstrings directives.
4. Build MkDocs.
5. Fix Griffe, import, autorefs, and broken-link warnings.
6. Serve locally.
7. Review rendered pages.
8. Deploy to GitHub Pages.
```

Command set:

```powershell id="architecture_validation_commands"
python -m compileall .
Select-String -Path .\docs\api\*.md -Pattern "^:::"
mkdocs build
mkdocs serve
```



## ðŸ§­ Common Architecture Decisions

### Flat source layout

Current layout:

```text id="flat_source_decision"
loaders.py
fetchers.py
processors.py
models.py
```

Use API directives like:

```markdown id="flat_source_api"
`::: loaders`
```

### Package source layout

Future package layout:

```text id="package_source_decision"
fonky/
    loaders.py
    fetchers.py
    processors.py
    models.py
```

Use API directives like:

```markdown id="package_source_api"
`::: loaders`
```

### Export modules

Export modules are used to provide convenient imports and group related functionality:

```python id="export_module_architecture_example"
from documents import TextLoader
from web import WebExtractor
from cloud import AwsBucketLoader
```

They should remain thin and should not duplicate implementation logic from the core modules.



## âœ… Architectural Baseline

A healthy Fonky architecture has the following properties:

```text id="architecture_baseline"
- Source modules compile.
- Configuration imports without external service calls.
- Logging writes handled exceptions to SQLite.
- Loaders return LangChain Document objects.
- Fetchers return normalized structured payloads.
- Scrapers return parsed web content structures.
- Processors return cleaned, tokenized, chunked, or vector-ready text.
- Models expose callables as provider-compatible tools.
- Export modules provide clean import paths.
- API docs render source docstrings through mkdocstrings.
- Manual docs explain setup, configuration, architecture, logging, usage, development, and deployment.
```



## âž¡ï¸ Next Step

Continue to [Logging](logging.md) for the detailed exception model, database logging behavior, and
required handler pattern.


