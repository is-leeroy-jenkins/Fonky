# Configuration

Fonky centralizes runtime settings in `config.py`. The configuration layer provides
environment-variable loading, path helpers, exception logging locations, API keys, service
descriptions, and settings used by loaders, fetchers, scrapers, processors, models, and MkDocs.

This page explains how Fonky configuration works, which settings are required for different
workflows, and how to validate configuration before running the project.

## Configuration Model

Fonky uses a simple configuration pattern:

```text
Environment variables
    -> config.py helper functions
    -> module-level constants
    -> loaders, fetchers, scrapers, processors, models, and logging
```

The goal is to keep source modules importable while allowing credentials, paths, and runtime options
to be supplied externally.

The main configuration areas are:

| Area                  | Purpose                                                                        |
| --------------------- | ------------------------------------------------------------------------------ |
| Path configuration    | Defines repository paths and logging paths.                                    |
| Logging configuration | Defines the SQLite database and table used by `boogr.Logger`.                  |
| API keys              | Supplies credentials for optional external services.                           |
| Service descriptions  | Provides human-readable descriptions used by source modules and documentation. |
| Documentation support | Keeps source modules importable for MkDocs and mkdocstrings.                   |

## Path Constants

The main path constants are defined in `config.py`.

| Constant   | Purpose                                                 |
| ---------- | ------------------------------------------------------- |
| `BASE_DIR` | Directory containing `config.py`.                       |
| `ROOT_DIR` | Project root directory used by runtime configuration.   |
| `LOG_DIR`  | Directory where exception logging artifacts are stored. |
| `LOG_PATH` | Full path to the SQLite exception database.             |
| `LOG_FILE` | SQLite table name used by the exception logger.         |

Default logging database:

```text
logging/Exceptions.db
```

Default logging table:

```text
Exceptions
```

## Logging Configuration

Fonky uses `boogr.Error` and `boogr.Logger` for handled exceptions.

The logging constants required by `boogr.py` are:

```python
LOG_DIR
LOG_PATH
LOG_FILE
```

Recommended local defaults:

```text
LOG_DIR  = logging
LOG_PATH = logging/Exceptions.db
LOG_FILE = Exceptions
```

PowerShell override example:

```powershell
$env:LOG_DIR = "C:\Users\terry\source\repos\Fonky\logging"
$env:LOG_PATH = "C:\Users\terry\source\repos\Fonky\logging\Exceptions.db"
$env:LOG_FILE = "Exceptions"
```

The database is created or updated when source code calls:

```python
Logger().write(exception)
```

## API Key Strategy

Fonky does not require every API key for every workflow.

Only configure the keys required for the services you plan to use.

| Workflow               | Required or likely variables                                                      |
| ---------------------- | --------------------------------------------------------------------------------- |
| Basic document loading | None                                                                              |
| Local text processing  | None                                                                              |
| Basic HTML parsing     | None                                                                              |
| Google Custom Search   | `GOOGLE_API_KEY`, `GOOGLE_CSE_ID`                                                 |
| Google Weather         | `GOOGLE_WEATHER_API_KEY`                                                          |
| Google Drive           | `GOOGLE_ACCOUNT_CREDENTIALS`, `GOOGLE_DRIVE_TOKEN_PATH`, `GOOGLE_DRIVE_FOLDER_ID` |
| Google Cloud Storage   | Google Cloud credentials and project settings                                     |
| Google Speech-to-Text  | Google Cloud credentials and Speech-to-Text access                                |
| NASA APIs              | `NASA_API_KEY`, `NASA_EARTHDATA_TOKEN` where applicable                           |
| GovInfo                | `GOVINFO_API_KEY`                                                                 |
| Congress API           | `CONGRESS_API_KEY`                                                                |
| News APIs              | `NEWSAPI_API_KEY`, `THENEWSAPI_API_KEY`                                           |
| Census                 | `CENSUS_API_KEY`                                                                  |
| AirNow                 | `AIRNOW_API_KEY`                                                                  |
| OpenAQ                 | `OPENAQ_API_KEY`                                                                  |
| PurpleAir              | `PURPLEAIR_API_KEY`                                                               |
| OpenAI tooling         | `OPENAI_API_KEY`                                                                  |
| Gemini tooling         | `GEMINI_API_KEY`                                                                  |
| Grok or xAI tooling    | `XAI_API_KEY`                                                                     |
| Mistral tooling        | `MISTRAL_API_KEY`                                                                 |
| Claude tooling         | `CLAUDE_API_KEY`                                                                  |

## Common Environment Variables

### AI and model provider keys

```text
OPENAI_API_KEY
GEMINI_API_KEY
GOOGLE_API_KEY
CLAUDE_API_KEY
MISTRAL_API_KEY
XAI_API_KEY
HUGGINGFACE_API_KEY
PINECONE_API_KEY
CHROMA_API_KEY
CHROMA_TENET_ID
LANGSMITH_API_KEY
LLAMAINDEX_API_KEY
LLAMACLOUD_API_KEY
```

### Google service keys and settings

```text
GOOGLE_API_KEY
GOOGLE_CSE_ID
GOOGLE_WEATHER_API_KEY
GOOGLE_ACCOUNT_CREDENTIALS
GOOGLE_DRIVE_TOKEN_PATH
GOOGLE_DRIVE_FOLDER_ID
GOOGLE_CLOUD_PROJECT_ID
GOOGLE_CLOUD_LOCATION
GOOGLE_GENAI_USE_VERTEXAI
```

### Public data and government service keys

```text
NASA_API_KEY
NASA_EARTHDATA_TOKEN
GOVINFO_API_KEY
CONGRESS_API_KEY
CENSUS_API_KEY
DATAGOV_API_KEY
SOCRATA_API_KEY
HEALTHDATA_API_KEY
USGS_API_KEY
FIRMS_MAP_KEY
```

### Environmental and geospatial service keys

```text
AIRNOW_API_KEY
OPENAQ_API_KEY
PURPLEAIR_API_KEY
GEOAPIFY_API_KEY
GEOCODING_API_KEY
WEATHERAPI_API_KEY
IPINFO_API_KEY
SKY_MAP_TOKEN
```

### Microsoft and cloud service keys

```text
O365_CLIENT_ID
O365_CLIENT_SECRET
OPENSKY_API_CLIENT_ID
OPENSKY_API_CREDENTIALS
OPENSKY_API_CLIENT_SECRET
```

### Logging variables

```text
LOG_DIR
LOG_PATH
LOG_FILE
```

## PowerShell Configuration Examples

Set Google Custom Search variables:

```powershell
$env:GOOGLE_API_KEY = "your-google-api-key"
$env:GOOGLE_CSE_ID = "your-custom-search-engine-id"
```

Set NASA variables:

```powershell
$env:NASA_API_KEY = "your-nasa-api-key"
$env:NASA_EARTHDATA_TOKEN = "your-earthdata-token"
```

Set GovInfo and Congress variables:

```powershell
$env:GOVINFO_API_KEY = "your-govinfo-api-key"
$env:CONGRESS_API_KEY = "your-congress-api-key"
```

Set environmental service variables:

```powershell
$env:AIRNOW_API_KEY = "your-airnow-api-key"
$env:OPENAQ_API_KEY = "your-openaq-api-key"
$env:PURPLEAIR_API_KEY = "your-purpleair-api-key"
```

Set model provider variables:

```powershell
$env:OPENAI_API_KEY = "your-openai-api-key"
$env:GEMINI_API_KEY = "your-gemini-api-key"
$env:XAI_API_KEY = "your-xai-api-key"
$env:MISTRAL_API_KEY = "your-mistral-api-key"
$env:CLAUDE_API_KEY = "your-claude-api-key"
```

## Validate Configuration Imports

Run this from the repository root:

```powershell
python -c "import config; print(config.ROOT_DIR); print(config.LOG_PATH); print(config.LOG_FILE)"
```

Expected result:

```text
The command prints the project root path, exception database path, and exception table name.
```

If the import fails, resolve the source error or missing dependency before building documentation.

## Validate Logging Configuration

Run this from the repository root:

```powershell
python -c "from boogr import Error, Logger; import config as cfg; error = Error(Exception('configuration test')); error.module = 'config'; error.cause = 'ConfigurationValidation'; error.method = 'manual logging validation'; Logger().write(error); print(cfg.LOG_PATH)"
```

Confirm the database exists:

```powershell
Test-Path .\logging\Exceptions.db
```

Expected output:

```text
True
```

If the result is `False`, confirm that `LOG_DIR` and `LOG_PATH` point to writable locations.

## Configuration for Document Loading

Most local document loaders do not require API keys.

| Loader type       | Typical requirement                     |
| ----------------- | --------------------------------------- |
| Text files        | Local file path                         |
| CSV files         | Local CSV path                          |
| PDF files         | Local PDF path and parsing dependencies |
| Word files        | Local DOCX path                         |
| Excel files       | Local workbook path                     |
| Markdown files    | Local Markdown path                     |
| HTML files        | Local HTML path                         |
| JSON files        | Local JSON or JSONL path                |
| XML files         | Local XML path                          |
| Jupyter notebooks | Local notebook path                     |

Credential-backed loaders require provider configuration.

| Loader type                 | Required configuration                             |
| --------------------------- | -------------------------------------------------- |
| Google Drive                | Google credentials and Drive access                |
| Google Cloud file loading   | Google Cloud credentials and project configuration |
| Google Cloud bucket loading | Google Cloud credentials and bucket access         |
| Google Speech-to-Text       | Google Cloud credentials and Speech-to-Text access |
| AWS file loading            | AWS credentials or profile configuration           |
| AWS bucket loading          | AWS credentials or profile configuration           |
| OneDrive document loading   | Microsoft authentication and OneDrive access       |
| SharePoint loading          | Microsoft authentication and SharePoint access     |

## Configuration for Web and Search Workflows

Static HTML extraction usually does not require API keys.

Search-oriented workflows often do.

| Service              | Common variables                        |
| -------------------- | --------------------------------------- |
| Google Custom Search | `GOOGLE_API_KEY`, `GOOGLE_CSE_ID`       |
| Wikipedia            | Usually none                            |
| ArXiv                | Usually none                            |
| PubMed               | Usually none                            |
| News APIs            | `NEWSAPI_API_KEY`, `THENEWSAPI_API_KEY` |
| GovInfo              | `GOVINFO_API_KEY`                       |
| Congress             | `CONGRESS_API_KEY`                      |

Browser-backed scraping may require Playwright browser binaries:

```powershell
python -m playwright install chromium
```

## Configuration for Public Data APIs

Fonky includes fetchers and export modules for public, scientific, government, environmental,
health, demographic, and geospatial data.

| Module area        | Example service types                               |
| ------------------ | --------------------------------------------------- |
| `astronomical.py`  | NASA, near-earth objects, space weather, sky maps   |
| `environmental.py` | EPA, AirNow, OpenAQ, PurpleAir, NASA FIRMS          |
| `geospatial.py`    | USGS, NOAA, geocoding, tides, water data            |
| `health.py`        | WHO, CDC WONDER, health data services               |
| `demographic.py`   | Census, population, demographic datasets            |
| `archives.py`      | ArXiv, Wikipedia, PubMed, GovInfo, Internet Archive |

Not every service requires a key. Check the provider and the corresponding class or method in the
API reference before configuring credentials.

## Configuration Helper Functions

`config.py` includes helper functions for import-safe configuration parsing.

| Helper                     | Purpose                                             |
| -------------------------- | --------------------------------------------------- |
| `throw_if(name, value)`    | Raises `ValueError` when a required value is empty. |
| `get_bool(name, default)`  | Reads a Boolean environment variable.               |
| `get_int(name, default)`   | Reads an integer environment variable.              |
| `get_float(name, default)` | Reads a floating-point environment variable.        |
| `get_path(name, default)`  | Reads and resolves a filesystem path.               |
| `get_text(name, default)`  | Reads a text environment variable.                  |

Example:

```python
from pathlib import Path
import config

log_dir = config.get_path(
    name="LOG_DIR",
    default=Path("logging")
)

print(log_dir)
```

## MkDocs Configuration

MkDocs configuration is stored in:

```text
mkdocs.yml
```

The key block for rendering Python source docstrings is the `mkdocstrings` plugin:

```yaml
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

The `paths` setting must let mkdocstrings import the modules referenced in `docs/api/*.md`.

For this flat source layout, the API page for loaders should contain this directive as literal page
content:

```text
::: loaders
```

The project should not use:

```text
::: fonky.loaders
```

unless the source files are moved into an importable package folder named `fonky`.

## API Directive Rules

Only files under `docs/api/` should contain live mkdocstrings directives.

Correct:

```text
docs/api/loaders.md contains ::: loaders
docs/api/fetchers.md contains ::: fetchers
docs/api/models.md contains ::: models
```

Incorrect:

```text
docs/configuration.md contains ::: loaders
docs/architecture.md contains ::: loaders
docs/development.md contains ::: loaders
```

Confirm API pages contain directives:

```powershell
Select-String -Path .\docs\api\*.md -Pattern "^:::\s+[A-Za-z_]"
```

Confirm top-level manual pages do not:

```powershell
Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"
```

Expected output for the top-level manual page check:

```text
No output.
```

## Configuration Validation Checklist

Use this checklist after editing `config.py`, environment variables, MkDocs settings, or deployment
settings.

| Check                                | Command                                                                                                                                                          |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Python source compiles               | `python -m compileall .`                                                                                                                                         |
| Config imports                       | `python -c "import config; print(config.LOG_PATH)"`                                                                                                              |
| Logging constants exist              | `python -c "import config; print(config.LOG_DIR); print(config.LOG_PATH); print(config.LOG_FILE)"`                                                               |
| Logger writes database record        | `python -c "from boogr import Error, Logger; e = Error(Exception('test')); e.module = 'config'; e.cause = 'Validation'; e.method = 'manual'; Logger().write(e)"` |
| Documentation dependencies installed | `python -m pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python pymdown-extensions`                                                               |
| API pages contain directives         | `Select-String -Path .\docs\api\*.md -Pattern "^:::\s+[A-Za-z_]"`                                                                                                |
| Manual pages contain no directives   | `Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"`                                                                                                    |
| Documentation builds                 | `mkdocs build`                                                                                                                                                   |

## Common Configuration Problems

### Missing API key

Symptom:

```text
A provider fetcher fails authorization or returns an authentication error.
```

Fix:

```powershell
$env:PROVIDER_API_KEY = "your-provider-key"
```

Then rerun the command in the same PowerShell session.

### Logging database is not created

Symptoms:

```text
The expected logging/Exceptions.db file does not appear.
Logger write calls fail or the configured database path is wrong.
```

Fix:

```powershell
New-Item -ItemType Directory -Force .\logging | Out-Null
$env:LOG_PATH = "C:\Users\terry\source\repos\Fonky\logging\Exceptions.db"
$env:LOG_FILE = "Exceptions"
```

Then rerun a logging validation command.

### MkDocs cannot import modules

Symptoms:

```text
mkdocstrings reports that it cannot import a module.
API pages are blank or fail to render.
```

Fix for this flat source layout:

```text
::: loaders
```

Do not use:

```text
::: fonky.loaders
```

Also confirm `mkdocs.yml` includes:

```yaml
paths:
  - .
```

### Griffe reports malformed Google-style sections

Symptoms:

```text
No type or annotation for returned value
Failed to get name: description pair
```

Use typed return sections:

```text
Returns:
    list[str]: Supported option values.
```

Use valid argument entries:

```text
Args:
    name (str): Description of the value.
```

Avoid untyped entries:

```text
Args:
    Request parameters.
```

Avoid `Returns: None`. For functions that do not return values, omit the `Returns:` section.

## Recommended Local Baseline

For local development, use this baseline:

```text
- Use a project-local virtual environment.
- Keep source files importable from the repository root.
- Set only API keys required for the current workflow.
- Keep logging at logging/Exceptions.db unless deployment requires a different path.
- Keep docs/api pages aligned with actual module import paths.
- Run python -m compileall . before mkdocs build.
- Run mkdocs build before mkdocs serve or gh-deploy.
```

