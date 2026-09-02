# Configuration & API Keys

Fonky centralizes environment-backed credentials and service settings in `config.py`. The module
reads these values during import with `os.getenv(...)`.


[Gov Info API](https://www.govinfo.gov/api-signup)


[Google Geolocation API](https://developers.google.com/maps/documentation/geolocation/overview)


[Google Maps API](https://developers.google.com/maps/documentation/urls/get-started)


[Google Weather API](https://developers.google.com/maps/documentation/weather/get-api-key)


[Gemini AI API](https://aistudio.google.com/api-keys?)


[CDC API](https://data.cdc.gov/login)


[NASA Firms API](https://firms.modaps.eosdis.nasa.gov/usfs/api/map_key/)


[Wikipedia API](https://www.mediawiki.org/wiki/Wikimedia_APIs/Get_started)


[Xai API](https://accounts.x.ai/account)


[Claude AI API](https://platform.claude.com/docs/en/api/admin/api_keys)

[NASA API](https://api.nasa.gov/)


[TheNewsAPI](https://www.thenewsapi.com/register)


[Grokipedia API](https://accounts.x.ai/account)


[Purpler Air API](https://develop.purpleair.com/dashboards/keys)


[Census API](https://api.census.gov/data/key_signup.html)


[Air Now API](https://docs.airnowapi.org/account/request/)


[Astronomy API](https://astronomyapi.com/auth/signup)


[ChromaDB API](https://docs.trychroma.com/cloud/getting-started)


[GeoApify API](https://apidocs.geoapify.com/)

[Google Custom Search Engine API](https://developers.google.com/custom-search/v1/introduction)

[Hugging Face API](https://huggingface.co/)

[IP Info API](https://ipinfo.io/signup)

[Jina AI API](https://jina.ai/api-dashboard/)

[LangSmith API](https://smith.langchain.com/?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup)

[Llama Index API](https://developers.llamaindex.ai/llamaparse/general/api_key/)

[Mistral AI API](https://v2.auth.mistral.ai/login?flow=93cd89ac-fb49-4ed7-ac7d-4357537c9ffc)

[USGS API](https://api.waterdata.usgs.gov/signup/)

[The Weather API](https://www.weatherapi.com/api-explorer.aspx)

[Socrata API](https://dev.socrata.com/docs/other/api-keys#?route=overview)

[Open Weather API](https://openweathermap.org/api)

[Pinecone API](https://docs.pinecone.io/reference/api/2025-04/admin/create_api_key)

[Weaviate API](https://docs.weaviate.io/cloud/manage-clusters/connect#retrieve-your-api-key-and-rest-endpoint)

[OpenSky API](https://opensky-network.org/data/api)

[Aviation Stack API](https://aviationstack.com/signup/free/monthly)

[Congress API](https://api.congress.gov/sign-up/)

[OpenAQ API](https://docs.openaq.org/using-the-api/api-key)


## Credential and Service Variables

| `config.py` constant | Environment variable | Service / setting |
|---|---|---|
| `AIRNOW_API_KEY` | `AIRNOW_API_KEY` | AirNow |
| `CLAUDE_API_KEY` | `CLAUDE_API_KEY` | Anthropic Claude |
| `CONGRESS_API_KEY` | `CONGRESS_API_KEY` | Congress.gov / congressional data |
| `CHROMA_API_KEY` | `CHROMA_API_KEY` | Chroma |
| `CHROMA_TENET_ID` | `CHROMA_TENET_ID` | Chroma tenant identifier |
| `GEOAPIFY_API_KEY` | `GEOAPIFY_API_KEY` | Geoapify |
| `GEOCODING_API_KEY` | `GEOCODING_API_KEY` | Geocoding service |
| `GEMINI_API_KEY` | `GEMINI_API_KEY` | Google Gemini |
| `GOOGLE_API_KEY` | `GOOGLE_API_KEY` | Google APIs / Programmable Search |
| `GOOGLE_CSE_ID` | `GOOGLE_CSE_ID` | Google Programmable Search Engine ID |
| `GOOGLE_CLOUD_PROJECT_ID` | `GOOGLE_CLOUD_PROJECT_ID` | Google Cloud project |
| `GOOGLE_CLOUD_LOCATION` | `GOOGLE_CLOUD_LOCATION` | Google Cloud location |
| `GOVINFO_API_KEY` | `GOVINFO_API_KEY` | GovInfo |
| `GOOGLE_GENAI_USE_VERTEXAI` | `GOOGLE_GENAI_USE_VERTEXAI` | Google GenAI Vertex AI mode |
| `GOOGLE_WEATHER_API_KEY` | `GOOGLE_WEATHER_API_KEY` | Google Weather |
| `GOOGLE_ACCOUNT_FILE` | `GOOGLE_ACCOUNT_CREDENTIALS` | Google service-account credentials file |
| `GOOGLE_DRIVE_TOKEN_PATH` | `GOOGLE_DRIVE_TOKEN_PATH` | Google Drive OAuth token path |
| `GOOGLE_DRIVE_FOLDER_ID` | `GOOGLE_DRIVE_FOLDER_ID` | Default Google Drive folder |
| `HUGGINGFACE_API_KEY` | `HUGGINGFACE_API_KEY` | Hugging Face |
| `IPINFO_API_KEY` | `IPINFO_API_KEY` | IPinfo |
| `OPENAI_API_KEY` | `OPENAI_API_KEY` | OpenAI |
| `PINECONE_API_KEY` | `PINECONE_API_KEY` | Pinecone |
| `LANGSMITH_API_KEY` | `LANGSMITH_API_KEY` | LangSmith |
| `LLAMAINDEX_API_KEY` | `LLAMAINDEX_API_KEY` | LlamaIndex |
| `LLAMACLOUD_API_KEY` | `LLAMACLOUD_API_KEY` | LlamaCloud |
| `MISTRAL_API_KEY` | `MISTRAL_API_KEY` | Mistral |
| `NASA_API_KEY` | `NASA_API_KEY` | NASA APIs |
| `NASA_EARTHDATA_TOKEN` | `NASA_EARTHDATA_TOKEN` | NASA Earthdata |
| `NEWS_API_KEY` | `NEWSAPI_API_KEY` | NewsAPI |
| `THENEWS_API_KEY` | `THENEWSAPI_API_KEY` | TheNewsAPI |
| `WEATHERAPI_API_KEY` | `WEATHERAPI_API_KEY` | WeatherAPI |
| `XAI_API_KEY` | `XAI_API_KEY` | xAI |
| `O365_CLIENT_ID` | `O365_CLIENT_ID` | Microsoft 365 OAuth client ID |
| `O365_CLIENT_SECRET` | `O365_CLIENT_SECRET` | Microsoft 365 OAuth client secret |
| `OPENAQ_API_KEY` | `OPENAQ_API_KEY` | OpenAQ |
| `OPENSKY_API_CLIENT_ID` | `OPENSKY_API_CLIENT_ID` | OpenSky API client ID |
| `OPENSKY_API_CREDENTIALS` | `OPENSKY_API_CREDENTIALS` | OpenSky API credentials |
| `OPENSKY_API_CLIENT_SECRET` | `OPENSKY_API_CLIENT_ID` | OpenSky API client secret binding in current config.py |
| `CENSUS_API_KEY` | `CENSUS_API_KEY` | U.S. Census |
| `SOCRATA_API_KEY` | `SOCRATA_API_KEY` | Socrata |
| `HEALTHDATA_API_KEY` | `HEALTHDATA_API_KEY` | HealthData.gov |
| `USGS_WATERDATA_API_KEY` | `USGS_API_KEY` | USGS |
| `DATA_GOV_API_KEY` | `DATAGOV_API_KEY` | Data.gov |
| `FIRMS_MAP_KEY` | `FIRMS_MAP_KEY` | NASA FIRMS |
| `PURPLEAIR_API_KEY` | `PURPLEAIR_API_KEY` | PurpleAir |
| `SKY_MAP_TOKEN` | `SKY_MAP_TOKEN` | Sky Map |

## Minimal Provider Configuration

### OpenAI Agents SDK

```dotenv
OPENAI_API_KEY=
```

### Google Gemini / ADK

```dotenv
GEMINI_API_KEY=
```

Google services used by individual Fonky tools may additionally require:

```dotenv
GOOGLE_API_KEY=
GOOGLE_CSE_ID=
GOOGLE_WEATHER_API_KEY=
GOOGLE_CLOUD_PROJECT_ID=
GOOGLE_CLOUD_LOCATION=
GOOGLE_GENAI_USE_VERTEXAI=
GOOGLE_ACCOUNT_CREDENTIALS=
GOOGLE_DRIVE_TOKEN_PATH=
GOOGLE_DRIVE_FOLDER_ID=
```

### xAI Grok

```dotenv
XAI_API_KEY=
```

### LangChain / LangSmith

LangChain tools themselves do not require a single universal API key. Configure the credentials
for the underlying provider or service used by each tool. LangSmith tracing uses:

```dotenv
LANGSMITH_API_KEY=
```

## Public Data and Government Services

```dotenv
CONGRESS_API_KEY=
GOVINFO_API_KEY=
DATAGOV_API_KEY=
CENSUS_API_KEY=
SOCRATA_API_KEY=
HEALTHDATA_API_KEY=
USGS_API_KEY=
```

## Environmental and Weather Services

```dotenv
AIRNOW_API_KEY=
OPENAQ_API_KEY=
PURPLEAIR_API_KEY=
FIRMS_MAP_KEY=
GOOGLE_WEATHER_API_KEY=
WEATHERAPI_API_KEY=
```

## Geospatial Services

```dotenv
GEOAPIFY_API_KEY=
GEOCODING_API_KEY=
IPINFO_API_KEY=
```

## NASA and Astronomy Services

```dotenv
NASA_API_KEY=
NASA_EARTHDATA_TOKEN=
SKY_MAP_TOKEN=
OPENSKY_API_CLIENT_ID=
OPENSKY_API_CREDENTIALS=
```

## News Services

```dotenv
NEWSAPI_API_KEY=
THENEWSAPI_API_KEY=
```

## Vector, Model, and AI Services

```dotenv
CLAUDE_API_KEY=
HUGGINGFACE_API_KEY=
MISTRAL_API_KEY=
PINECONE_API_KEY=
CHROMA_API_KEY=
CHROMA_TENET_ID=
LLAMAINDEX_API_KEY=
LLAMACLOUD_API_KEY=
```

## Microsoft 365

```dotenv
O365_CLIENT_ID=
O365_CLIENT_SECRET=
```

## Complete `.env` Template

```dotenv
AIRNOW_API_KEY=
CLAUDE_API_KEY=
CONGRESS_API_KEY=
CHROMA_API_KEY=
CHROMA_TENET_ID=
GEOAPIFY_API_KEY=
GEOCODING_API_KEY=
GEMINI_API_KEY=
GOOGLE_API_KEY=
GOOGLE_CSE_ID=
GOOGLE_CLOUD_PROJECT_ID=
GOOGLE_CLOUD_LOCATION=
GOVINFO_API_KEY=
GOOGLE_GENAI_USE_VERTEXAI=
GOOGLE_WEATHER_API_KEY=
GOOGLE_ACCOUNT_CREDENTIALS=
GOOGLE_DRIVE_TOKEN_PATH=
GOOGLE_DRIVE_FOLDER_ID=
HUGGINGFACE_API_KEY=
IPINFO_API_KEY=
OPENAI_API_KEY=
PINECONE_API_KEY=
LANGSMITH_API_KEY=
LLAMAINDEX_API_KEY=
LLAMACLOUD_API_KEY=
MISTRAL_API_KEY=
NASA_API_KEY=
NASA_EARTHDATA_TOKEN=
NEWSAPI_API_KEY=
THENEWSAPI_API_KEY=
WEATHERAPI_API_KEY=
XAI_API_KEY=
O365_CLIENT_ID=
O365_CLIENT_SECRET=
OPENAQ_API_KEY=
OPENSKY_API_CLIENT_ID=
OPENSKY_API_CREDENTIALS=
CENSUS_API_KEY=
SOCRATA_API_KEY=
HEALTHDATA_API_KEY=
USGS_API_KEY=
DATAGOV_API_KEY=
FIRMS_MAP_KEY=
PURPLEAIR_API_KEY=
SKY_MAP_TOKEN=
```

## Source Binding Notes

The Python constant name and the environment-variable name are not always identical:

| Python constant | Environment variable |
|---|---|
| `GOOGLE_ACCOUNT_FILE` | `GOOGLE_ACCOUNT_CREDENTIALS` |
| `NEWS_API_KEY` | `NEWSAPI_API_KEY` |
| `THENEWS_API_KEY` | `THENEWSAPI_API_KEY` |
| `USGS_WATERDATA_API_KEY` | `USGS_API_KEY` |
| `DATA_GOV_API_KEY` | `DATAGOV_API_KEY` |
| `OPENSKY_API_CLIENT_SECRET` | `OPENSKY_API_CLIENT_ID` in the current source |

!!! warning "OpenSky client-secret binding"
    The current `config.py` reads `OPENSKY_API_CLIENT_SECRET` from `OPENSKY_API_CLIENT_ID`.
    This page documents the current source behavior. Correct the binding in `config.py` separately
    if a dedicated client-secret variable is intended.

## Secret Handling

Keep populated `.env` files, OAuth tokens, service-account files, and other credentials outside
source control. Commit only empty templates or documented variable names.
