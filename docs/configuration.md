# âš™ï¸ Configuration

Fonky centralizes runtime settings in `config.py`. The configuration layer provides
environment-variable loading, path helpers, exception logging locations, API keys, service
descriptions, and loader descriptions used by the rest of the project.

This page explains how Fonky configuration works, which settings are required for different
workflows, and how to validate configuration before running loaders, fetchers, scrapers, processors,
or documentation builds.



## ðŸ§­ Configuration Model

Fonky uses a simple configuration pattern:

```text id="config_model_flow"
Environment variables
    â†“
config.py helper functions
    â†“
module-level constants
    â†“
fetchers, loaders, scrapers, processors, models, and logging
```

The goal is to keep source modules import-safe while allowing service credentials and runtime paths
to be supplied externally.

The most important configuration areas are:

| Area                  | Purpose                                                       |
|-----------------------|---------------------------------------------------------------|
| Path configuration    | Establishes the repository root and logging database path.    |
| Logging configuration | Defines the SQLite database and table used by `boogr.Logger`. |
| API keys              | Supplies credentials for optional external services.          |
| Service descriptions  | Provides human-readable descriptions for APIs and loaders.    |
| Documentation support | Provides stable source metadata for MkDocs and mkdocstrings.  |



## ðŸ“ Path Constants

The core path constants are defined in `config.py`.

| Constant   | Purpose                                                 |
|------------|---------------------------------------------------------|
| `BASE_DIR` | Directory containing `config.py`.                       |
| `ROOT_DIR` | Project root directory used by runtime configuration.   |
| `LOG_DIR`  | Directory where exception logging artifacts are stored. |
| `LOG_PATH` | Full path to the SQLite exception database.             |
| `LOG_FILE` | SQLite table name used by the exception logger.         |

Default logging path:

```text id="default_log_path"
logging/Exceptions.db
```

Default logging table:

```text id="default_log_file"
Exceptions
```



## ðŸªµ Logging Configuration

Fonky uses `boogr.Error` and `boogr.Logger` for handled exceptions.

The logging constants required by `boogr.py` are:

```python id="required_logging_constants"
LOG_DIR
LOG_PATH
LOG_FILE
```

Recommended defaults:

```python id="recommended_logging_defaults"
LOG_DIR = ROOT_DIR / "logging"
LOG_PATH = "logging/Exceptions.db"
LOG_FILE = "Exceptions"
```

PowerShell override example:

```powershell id="override_logging_config"
$env:LOG_DIR = "C:\Users\terry\source\repos\Fonky\logging"
$env:LOG_PATH = "C:\Users\terry\source\repos\Fonky\logging\Exceptions.db"
$env:LOG_FILE = "Exceptions"
```

The exception database is created or updated when `Logger().write(exception)` is called.



## ðŸ” API Key Strategy

Fonky does not require every API key for every workflow.

Only configure the keys required for the services you plan to use.

For example:

| Workflow               | Required or likely variables                                                       |
|------------------------|------------------------------------------------------------------------------------|
| Basic document loading | None                                                                               |
| Local text processing  | None                                                                               |
| Web scraping           | Usually none, unless a provider requires credentials                               |
| Google Custom Search   | `GOOGLE_API_KEY`, `GOOGLE_CSE_ID`                                                  |
| Google Weather         | `GOOGLE_WEATHER_API_KEY`                                                           |
| Google Drive           | `GOOGLE_ACCOUNT_CREDENTIALS`, `GOOGLE_DRIVE_TOKEN_PATH`, `GOOGLE_DRIVE_FOLDER_ID`  |
| Google Cloud Storage   | `GOOGLE_CLOUD_PROJECT_ID`, Google credentials                                      |
| Google Speech-to-Text  | `GOOGLE_CLOUD_PROJECT_ID`, Google credentials                                      |
| NASA APIs              | `NASA_API_KEY`, `NASA_EARTHDATA_TOKEN` where applicable                            |
| GovInfo                | `GOVINFO_API_KEY`                                                                  |
| Congress API           | `CONGRESS_API_KEY`                                                                 |
| News APIs              | `NEWSAPI_API_KEY`, `THENEWSAPI_API_KEY`                                            |
| Census                 | `CENSUS_API_KEY`                                                                   |
| AirNow                 | `AIRNOW_API_KEY`                                                                   |
| OpenAQ                 | `OPENAQ_API_KEY`                                                                   |
| PurpleAir              | `PURPLEAIR_API_KEY`                                                                |
| OpenAI tooling         | `OPENAI_API_KEY`                                                                   |
| Gemini tooling         | `GEMINI_API_KEY`                                                                   |
| Grok or xAI tooling    | `XAI_API_KEY`                                                                      |
| Mistral tooling        | `MISTRAL_API_KEY`                                                                  |
| Claude tooling         | `CLAUDE_API_KEY`                                                                   |



## ðŸ”‘ Common Environment Variables

The following variables are read by `config.py`.

### AI and model provider keys

```text id="ai_provider_keys"
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

```text id="google_service_keys"
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

```text id="public_data_keys"
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

```text id="environmental_keys"
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

```text id="microsoft_cloud_keys"
O365_CLIENT_ID
O365_CLIENT_SECRET
OPENSKY_API_CLIENT_ID
OPENSKY_API_CREDENTIALS
OPENSKY_API_CLIENT_SECRET
```

### Logging variables

```text id="logging_keys"
LOG_DIR
LOG_PATH
LOG_FILE
```



## ðŸªŸ PowerShell Configuration Examples

Set variables for Google Custom Search:

```powershell id="set_google_search_keys"
$env:GOOGLE_API_KEY = "your-google-api-key"
$env:GOOGLE_CSE_ID = "your-custom-search-engine-id"
```

Set variables for NASA services:

```powershell id="set_nasa_keys"
$env:NASA_API_KEY = "your-nasa-api-key"
$env:NASA_EARTHDATA_TOKEN = "your-earthdata-token"
```

Set variables for GovInfo and Congress:

```powershell id="set_gov_keys"
$env:GOVINFO_API_KEY = "your-govinfo-api-key"
$env:CONGRESS_API_KEY = "your-congress-api-key"
```

Set variables for environmental services:

```powershell id="set_environmental_keys"
$env:AIRNOW_API_KEY = "your-airnow-api-key"
$env:OPENAQ_API_KEY = "your-openaq-api-key"
$env:PURPLEAIR_API_KEY = "your-purpleair-api-key"
```

Set variables for model providers:

```powershell id="set_model_keys"
$env:OPENAI_API_KEY = "your-openai-api-key"
$env:GEMINI_API_KEY = "your-gemini-api-key"
$env:XAI_API_KEY = "your-xai-api-key"
$env:MISTRAL_API_KEY = "your-mistral-api-key"
$env:CLAUDE_API_KEY = "your-claude-api-key"
```



## ðŸ§ª Validate Configuration Imports

Run this from the repository root:

```powershell id="validate_config_import"
python -c "import config; print(config.ROOT_DIR); print(config.LOG_PATH); print(config.LOG_FILE)"
```

Expected result:

```text id="config_import_expected"
The command prints the project root path, the exception database path, and the exception table name.
```

If the source files are moved into a package folder named `fonky`, use:

```powershell id="validate_package_config_import"
python -c "import fonky.config as config; print(config.ROOT_DIR); print(config.LOG_PATH); print(config.LOG_FILE)"
```



## ðŸ§ª Validate Logging Configuration

Run this from the repository root to confirm the logger can write an exception:

```powershell id="validate_logging_config"
python -c "from boogr import Error, Logger; import config as cfg; error = Error(Exception('configuration test')); error.module = 'config'; error.cause = 'ConfigurationValidation'; error.method = 'manual logging validation'; Logger().write(error); print(cfg.LOG_PATH)"
```

Confirm the database exists:

```powershell id="confirm_logging_database"
Test-Path .\logging\Exceptions.db
```

Expected result:

```text id="logging_database_expected"
True
```

If the result is `False`, confirm that `LOG_DIR` and `LOG_PATH` point to writable locations.



## ðŸ“„ Configuration for Document Loading

Most local document loaders do not require API keys.

Examples that normally do not require credentials:

| Loader                  | Typical requirement                          |
| -- | -- |
| `TextLoader`            | Local text file path                         |
| `CsvLoader`             | Local CSV file path                          |
| `PdfLoader`             | Local PDF file path and parsing dependencies |
| `WordLoader`            | Local DOCX file path                         |
| `ExcelLoader`           | Local XLSX file path                         |
| `MarkdownLoader`        | Local Markdown file path                     |
| `HtmlLoader`            | Local HTML file path                         |
| `JsonLoader`            | Local JSON or JSONL file path                |
| `XmlLoader`             | Local XML file path                          |
| `JupyterNotebookLoader` | Local notebook file path                     |

Credential-backed loaders include:

| Loader                     | Required configuration                             |
| -- | -- |
| `GoogleDriveLoader`        | Google credentials and Drive access                |
| `GoogleCloudFileLoader`    | Google Cloud credentials and project configuration |
| `GoogleBucketLoader`       | Google Cloud credentials and project configuration |
| `GoogleSpeechToTextLoader` | Google Cloud credentials and Speech-to-Text access |
| `AwsFileLoader`            | AWS credentials or environment-based AWS profile   |
| `AwsBucketLoader`          | AWS credentials or environment-based AWS profile   |
| `OneDriveDocLoader`        | Microsoft authentication and OneDrive access       |
| `SpfxLoader`               | Microsoft authentication and SharePoint access     |



## ðŸŒ Configuration for Web and Search Workflows

Web extraction from static HTML does not usually require API keys.

Search-oriented workflows often do.

| Service              | Common variables                        |
| -- |  |
| Google Custom Search | `GOOGLE_API_KEY`, `GOOGLE_CSE_ID`       |
| Wikipedia            | Usually none                            |
| ArXiv                | Usually none                            |
| PubMed               | Usually none                            |
| News APIs            | `NEWSAPI_API_KEY`, `THENEWSAPI_API_KEY` |
| GovInfo              | `GOVINFO_API_KEY`                       |
| Congress             | `CONGRESS_API_KEY`                      |

Browser-backed scraping may require Playwright browser binaries:

```powershell id="install_browser_for_scraping"
python -m playwright install chromium
```



## ðŸ›°ï¸ Configuration for Scientific and Public APIs

Fonky includes fetchers and export modules for astronomy, environment, geography, health,
demographics, public data, and government data.

Representative service groups:

| Module area        | Example services                                       |
|  |  |
| `astronomical.py`  | NASA, sky maps, near-earth objects, astronomy catalogs |
| `environmental.py` | EPA, AirNow, OpenAQ, PurpleAir, NASA FIRMS             |
| `geospatial.py`    | USGS, NOAA, geocoding, weather, tides, national map    |
| `health.py`        | WHO, CDC WONDER, health data services                  |
| `demographic.py`   | Census, world population, demographic data             |
| `archives.py`      | ArXiv, Wikipedia, PubMed, Internet Archive, GovInfo    |

Not every service requires a key. Check the API provider and the corresponding class docstring in
the API reference before configuring credentials.



## ðŸ§° Configuration Helper Functions

`config.py` includes helper functions for import-safe configuration parsing.

| Helper                     | Purpose                                             |
| -- |  |
| `throw_if(name, value)`    | Raises `ValueError` when a required value is empty. |
| `get_bool(name, default)`  | Reads a Boolean environment variable.               |
| `get_int(name, default)`   | Reads an integer environment variable.              |
| `get_float(name, default)` | Reads a floating-point environment variable.        |
| `get_path(name, default)`  | Reads and resolves a filesystem path.               |
| `get_text(name, default)`  | Reads a text environment variable.                  |

These helpers allow configuration values to be optional while still giving deterministic defaults.

Example:

```python id="config_helper_example"
from pathlib import Path
import config

log_dir = config.get_path(
	name="LOG_DIR",
	default=Path("logging")
)

print(log_dir)
```



## ðŸ“š MkDocs Configuration

MkDocs configuration is stored in:

```text id="mkdocs_config_file"
mkdocs.yml
```

The key block for rendering source docstrings is the `mkdocstrings` plugin:

```yaml id="mkdocstrings_config"
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

Root-level module example:

```markdown id="root_level_directive"
`::: loaders`
```

Package-level module example:

```markdown id="package_level_directive"
`::: loaders`
```



## ðŸ§ª Configuration Validation Checklist

Use this checklist after editing `config.py`, `.env` handling, or deployment settings.

| Check                                | Command                                                                                                                                                          |
|  | - |
| Python files compile                 | `python -m compileall .`                                                                                                                                         |
| Config imports                       | `python -c "import config; print(config.LOG_PATH)"`                                                                                                              |
| Logging constants exist              | `python -c "import config; print(config.LOG_DIR); print(config.LOG_PATH); print(config.LOG_FILE)"`                                                               |
| Logger writes database record        | `python -c "from boogr import Error, Logger; e = Error(Exception('test')); e.module = 'config'; e.cause = 'Validation'; e.method = 'manual'; Logger().write(e)"` |
| Documentation dependencies installed | `python -m pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python pymdown-extensions`                                                               |
| Documentation builds                 | `mkdocs build`                                                                                                                                                   |
| API pages render docstrings          | Confirm `docs/api/*.md` files contain `:::` directives                                                                                                           |



## ðŸ§¯ Common Configuration Problems

### Missing API key

Symptom:

```text id="missing_api_key_symptom"
A provider fetcher fails authorization or returns an authentication error.
```

Fix:

```powershell id="missing_api_key_fix"
$env:PROVIDER_API_KEY = "your-provider-key"
```

Then rerun the command in the same PowerShell session.



### Logging database is not created

Symptoms:

```text id="logging_database_missing"
The expected logging/Exceptions.db file does not appear.
Logger write calls fail silently or raise filesystem errors.
```

Fix:

```powershell id="logging_database_fix"
New-Item -ItemType Directory -Force .\logging | Out-Null
$env:LOG_PATH = "C:\Users\terry\source\repos\Fonky\logging\Exceptions.db"
$env:LOG_FILE = "Exceptions"
```

Then rerun a logging validation command.



### MkDocs cannot import modules

Symptoms:

```text id="mkdocs_import_problem"
mkdocstrings reports that it cannot import a module.
API pages are blank or fail to render.
```

Fix for root-level source files:

```markdown id="mkdocs_root_fix"
`::: loaders`
```

Fix for package-folder source files:

```markdown id="mkdocs_package_fix"
`::: loaders`
```

Also confirm `mkdocs.yml` includes:

```yaml id="mkdocs_paths_fix"
paths:
  - .
```



### Griffe reports malformed Google-style sections

Symptoms:

```text id="griffe_malformed_sections"
No type or annotation for returned value
Failed to get name: description pair
```

Fix:

Use typed return sections:

```text id="typed_returns_fix"
Returns:
	list[str]: Supported option values.
```

Use valid `Args:` or `Attributes:` entries:

```text id="valid_args_fix"
Args:
	name (str): Description of the value.
```

Avoid untyped entries:

```text id="invalid_args_example"
Args:
	Request parameters.
```

Avoid `Returns: None`. For functions that do not return values, omit the `Returns:` section.



## âœ… Recommended Configuration Baseline

For local development, keep this baseline:

```text id="local_configuration_baseline"
- Use a project-local virtual environment.
- Keep source files importable from the repository root.
- Set only API keys required for the current workflow.
- Keep logging at logging/Exceptions.db unless deployment requires a different path.
- Keep docs/api pages aligned with actual module import paths.
- Run python -m compileall . before mkdocs build.
- Run mkdocs build before mkdocs serve or gh-deploy.
```



## âž¡ï¸ Next Step

Continue to [Architecture](architecture.md) to understand how configuration flows through fetchers,
loaders, scrapers, processors, models, and the MkDocs-generated API reference.


