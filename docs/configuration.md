# Configuration

Fonky reads provider and runtime settings from the environment. Configure only the integrations you use.

## Environment Variable Inventory

| Variable | Role |
|---|---|
| `AIRNOW_API_KEY` | Provider/runtime setting read by `config.py`. |
| `CENSUS_API_KEY` | Provider/runtime setting read by `config.py`. |
| `CHROMA_API_KEY` | Provider/runtime setting read by `config.py`. |
| `CHROMA_TENET_ID` | Provider/runtime setting read by `config.py`. |
| `CLAUDE_API_KEY` | Provider/runtime setting read by `config.py`. |
| `CONGRESS_API_KEY` | Provider/runtime setting read by `config.py`. |
| `DATAGOV_API_KEY` | Provider/runtime setting read by `config.py`. |
| `FIRMS_MAP_KEY` | Provider/runtime setting read by `config.py`. |
| `GEMINI_API_KEY` | Provider/runtime setting read by `config.py`. |
| `GEOAPIFY_API_KEY` | Provider/runtime setting read by `config.py`. |
| `GEOCODING_API_KEY` | Provider/runtime setting read by `config.py`. |
| `GOOGLE_ACCOUNT_CREDENTIALS` | Provider/runtime setting read by `config.py`. |
| `GOOGLE_API_KEY` | Provider/runtime setting read by `config.py`. |
| `GOOGLE_CLOUD_LOCATION` | Provider/runtime setting read by `config.py`. |
| `GOOGLE_CLOUD_PROJECT_ID` | Provider/runtime setting read by `config.py`. |
| `GOOGLE_CSE_ID` | Provider/runtime setting read by `config.py`. |
| `GOOGLE_DRIVE_FOLDER_ID` | Provider/runtime setting read by `config.py`. |
| `GOOGLE_DRIVE_TOKEN_PATH` | Provider/runtime setting read by `config.py`. |
| `GOOGLE_GENAI_USE_VERTEXAI` | Provider/runtime setting read by `config.py`. |
| `GOOGLE_WEATHER_API_KEY` | Provider/runtime setting read by `config.py`. |
| `GOVINFO_API_KEY` | Provider/runtime setting read by `config.py`. |
| `HEALTHDATA_API_KEY` | Provider/runtime setting read by `config.py`. |
| `HUGGINGFACE_API_KEY` | Provider/runtime setting read by `config.py`. |
| `IPINFO_API_KEY` | Provider/runtime setting read by `config.py`. |
| `LANGSMITH_API_KEY` | Provider/runtime setting read by `config.py`. |
| `LLAMACLOUD_API_KEY` | Provider/runtime setting read by `config.py`. |
| `LLAMAINDEX_API_KEY` | Provider/runtime setting read by `config.py`. |
| `MISTRAL_API_KEY` | Provider/runtime setting read by `config.py`. |
| `NASA_API_KEY` | Provider/runtime setting read by `config.py`. |
| `NASA_EARTHDATA_TOKEN` | Provider/runtime setting read by `config.py`. |
| `NEWSAPI_API_KEY` | Provider/runtime setting read by `config.py`. |
| `O365_CLIENT_ID` | Provider/runtime setting read by `config.py`. |
| `O365_CLIENT_SECRET` | Provider/runtime setting read by `config.py`. |
| `OPENAI_API_KEY` | Provider/runtime setting read by `config.py`. |
| `OPENAQ_API_KEY` | Provider/runtime setting read by `config.py`. |
| `OPENSKY_API_CLIENT_ID` | Provider/runtime setting read by `config.py`. |
| `OPENSKY_API_CREDENTIALS` | Provider/runtime setting read by `config.py`. |
| `PINECONE_API_KEY` | Provider/runtime setting read by `config.py`. |
| `PURPLEAIR_API_KEY` | Provider/runtime setting read by `config.py`. |
| `SKY_MAP_TOKEN` | Provider/runtime setting read by `config.py`. |
| `SOCRATA_API_KEY` | Provider/runtime setting read by `config.py`. |
| `THENEWSAPI_API_KEY` | Provider/runtime setting read by `config.py`. |
| `USGS_API_KEY` | Provider/runtime setting read by `config.py`. |
| `WEATHERAPI_API_KEY` | Provider/runtime setting read by `config.py`. |
| `XAI_API_KEY` | Provider/runtime setting read by `config.py`. |

## PowerShell

```powershell
$env:GOOGLE_API_KEY = "..."
$env:GOOGLE_CSE_ID = "..."
$env:GOOGLE_WEATHER_API_KEY = "..."
$env:NASA_API_KEY = "..."
$env:CONGRESS_API_KEY = "..."
$env:AIRNOW_API_KEY = "..."
```

## Operational guidance

- Keep secrets out of source control.
- Distinguish missing SDKs from missing credentials.
- Cloud providers may require service-account/OAuth credential files rather than simple API keys.
- Test a provider independently before composing it into a larger workflow.
