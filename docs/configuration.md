# Configuration

`config.py` centralizes runtime paths, environment-derived credentials, provider descriptions, and environment parsing helpers. Optional variables remain optional during import.

## Configuration Helpers

| Helper | Behavior |
|---|---|
| `throw_if()` | Raise a ``ValueError`` when a required value is empty. |
| `get_bool()` | Read a Boolean environment variable. |
| `get_int()` | Read an integer environment variable. |
| `get_float()` | Read a floating-point environment variable. |
| `get_path()` | Read a path environment variable. |
| `get_text()` | Read a text environment variable. |

## Runtime Paths

`BASE_DIR` and `ROOT_DIR` are derived from the location of `config.py`. Logging paths can be overridden through `LOG_DIR`, `LOG_PATH`, and `LOG_FILE`.

## Environment Variables

The current source reads **45 distinct environment-variable names**.

| Variable | Behavior |
|---|---|
| `AIRNOW_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `CENSUS_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `CHROMA_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `CHROMA_TENET_ID` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `CLAUDE_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `CONGRESS_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `DATAGOV_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `FIRMS_MAP_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `GEMINI_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `GEOAPIFY_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `GEOCODING_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `GOOGLE_ACCOUNT_CREDENTIALS` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `GOOGLE_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `GOOGLE_CLOUD_LOCATION` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `GOOGLE_CLOUD_PROJECT_ID` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `GOOGLE_CSE_ID` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `GOOGLE_DRIVE_FOLDER_ID` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `GOOGLE_DRIVE_TOKEN_PATH` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `GOOGLE_GENAI_USE_VERTEXAI` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `GOOGLE_WEATHER_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `GOVINFO_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `HEALTHDATA_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `HUGGINGFACE_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `IPINFO_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `LANGSMITH_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `LLAMACLOUD_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `LLAMAINDEX_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `MISTRAL_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `NASA_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `NASA_EARTHDATA_TOKEN` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `NEWSAPI_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `O365_CLIENT_ID` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `O365_CLIENT_SECRET` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `OPENAI_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `OPENAQ_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `OPENSKY_API_CLIENT_ID` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `OPENSKY_API_CREDENTIALS` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `PINECONE_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `PURPLEAIR_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `SKY_MAP_TOKEN` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `SOCRATA_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `THENEWSAPI_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `USGS_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `WEATHERAPI_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |
| `XAI_API_KEY` | Read from the process environment by `config.py`; required only when the consuming provider or integration requires it. |

## Example

```powershell
$env:GOOGLE_API_KEY = "..."
$env:GOOGLE_CSE_ID = "..."
$env:GOOGLE_WEATHER_API_KEY = "..."
$env:NASA_API_KEY = "..."
$env:CONGRESS_API_KEY = "..."
$env:AIRNOW_API_KEY = "..."
```

## Import-Safe Defaults

`get_bool()`, `get_int()`, `get_float()`, `get_path()`, and `get_text()` return caller-supplied defaults when optional environment values are missing or invalid. `throw_if()` is the strict required-value guard.
