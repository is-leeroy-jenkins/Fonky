###### fonky

![](https://github.com/is-leeroy-jenkins/Fonky/blob/main/resources/images/fonky-project.png)

<p align="left">
  <a href="#-purpose">Purpose</a> &nbsp;|&nbsp;
  <a href="#%EF%B8%8F-architecture">Architecture</a> &nbsp;|&nbsp;
  <a href="#-package-structure">Package Structure</a> &nbsp;|&nbsp;
  <a href="#%EF%B8%8F-installation">Installation</a> &nbsp;|&nbsp;
  <a href="#-provider-integrations">Integrations</a> &nbsp;|&nbsp;
  <a href="https://github.com/is-leeroy-jenkins/Fonky/blob/main/resources/Tools.md#-tool-index">Tool Index</a> &nbsp;|&nbsp;
  <a href="https://github.com/is-leeroy-jenkins/Fonky/blob/main/resources/User-Guide.md">User Guide</a> &nbsp;|&nbsp;
  <a href="#-validation">Validation</a>
</p>

___

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-0078FC?style=for-the-badge&logo=github)](https://is-leeroy-jenkins.github.io/Fonky/)


## 🎯 Purpose

| Capability                            | Module                  |
|---------------------------------------|-------------------------|
| Data retrieval                        | `fonky.fetchers`        |
| Document ingestion                    | `fonky.loaders`         |
| Web extraction                        | `fonky.scrapers`        |
| Text and NLP processing               | `fonky.processors`      |
| Shared models and response structures | `fonky.models`          |
| Runtime configuration                 | `fonky.config`          |
| Error wrapping and logging            | `fonky.boogr`           |
| OpenAI Agents SDK tools               | `fonky.gpt.tools`       |
| Google ADK tools                      | `fonky.gemini.tools`    |
| xAI Grok tools                        | `fonky.grok.tools`      |
| LangChain tools                       | `fonky.langchain.tools` |


## 🛠️ Architecture

![](https://github.com/is-leeroy-jenkins/Fonky/blob/main/resources/images/fonky-architecture.png)

## 🔁 Workflow

![](https://github.com/is-leeroy-jenkins/Fonky/blob/main/resources/images/fonky-workflow.png)

## 📦 Package Structure

```text
fonky/
├── __init__.py
├── boogr.py
├── config.py
├── fetchers.py
├── loaders.py
├── models.py
├── processors.py
├── scrapers.py
├── gpt/
│   ├── __init__.py
│   └── tools.py
├── gemini/
│   ├── __init__.py
│   └── tools.py
├── grok/
│   ├── __init__.py
│   └── tools.py
└── langchain/
    ├── __init__.py
    └── tools.py
```

## ⚙️ Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel
python -m pip install -r requirements.txt
python -m pip check
```

### Playwright

```powershell
python -m playwright install chromium
```


## 🔑 Configuration and API Keys

![Set-up API Keys](https://github.com/is-leeroy-jenkins/Fonky/blob/main/resources/Configuration.md)

Fonky reads credentials and service configuration from environment variables in `config.py`.
Only configure the variables required by the tools and providers you use.

### Environment Variables

| `config.py` constant        | Environment variable         | Service / setting                                      |
|-----------------------------|------------------------------|--------------------------------------------------------|
| `AIRNOW_API_KEY`            | `AIRNOW_API_KEY`             | AirNow                                                 |
| `CLAUDE_API_KEY`            | `CLAUDE_API_KEY`             | Anthropic Claude                                       |
| `CONGRESS_API_KEY`          | `CONGRESS_API_KEY`           | Congress.gov / congressional data                      |
| `CHROMA_API_KEY`            | `CHROMA_API_KEY`             | Chroma                                                 |
| `CHROMA_TENET_ID`           | `CHROMA_TENET_ID`            | Chroma tenant identifier                               |
| `GEOAPIFY_API_KEY`          | `GEOAPIFY_API_KEY`           | Geoapify                                               |
| `GEOCODING_API_KEY`         | `GEOCODING_API_KEY`          | Geocoding service                                      |
| `GEMINI_API_KEY`            | `GEMINI_API_KEY`             | Google Gemini                                          |
| `GOOGLE_API_KEY`            | `GOOGLE_API_KEY`             | Google APIs / Programmable Search                      |
| `GOOGLE_CSE_ID`             | `GOOGLE_CSE_ID`              | Google Programmable Search Engine ID                   |
| `GOOGLE_CLOUD_PROJECT_ID`   | `GOOGLE_CLOUD_PROJECT_ID`    | Google Cloud project                                   |
| `GOOGLE_CLOUD_LOCATION`     | `GOOGLE_CLOUD_LOCATION`      | Google Cloud location                                  |
| `GOVINFO_API_KEY`           | `GOVINFO_API_KEY`            | GovInfo                                                |
| `GOOGLE_GENAI_USE_VERTEXAI` | `GOOGLE_GENAI_USE_VERTEXAI`  | Google GenAI Vertex AI mode                            |
| `GOOGLE_WEATHER_API_KEY`    | `GOOGLE_WEATHER_API_KEY`     | Google Weather                                         |
| `GOOGLE_ACCOUNT_FILE`       | `GOOGLE_ACCOUNT_CREDENTIALS` | Google service-account credentials file                |
| `GOOGLE_DRIVE_TOKEN_PATH`   | `GOOGLE_DRIVE_TOKEN_PATH`    | Google Drive OAuth token path                          |
| `GOOGLE_DRIVE_FOLDER_ID`    | `GOOGLE_DRIVE_FOLDER_ID`     | Default Google Drive folder                            |
| `HUGGINGFACE_API_KEY`       | `HUGGINGFACE_API_KEY`        | Hugging Face                                           |
| `IPINFO_API_KEY`            | `IPINFO_API_KEY`             | IPinfo                                                 |
| `OPENAI_API_KEY`            | `OPENAI_API_KEY`             | OpenAI                                                 |
| `PINECONE_API_KEY`          | `PINECONE_API_KEY`           | Pinecone                                               |
| `LANGSMITH_API_KEY`         | `LANGSMITH_API_KEY`          | LangSmith                                              |
| `LLAMAINDEX_API_KEY`        | `LLAMAINDEX_API_KEY`         | LlamaIndex                                             |
| `LLAMACLOUD_API_KEY`        | `LLAMACLOUD_API_KEY`         | LlamaCloud                                             |
| `MISTRAL_API_KEY`           | `MISTRAL_API_KEY`            | Mistral                                                |
| `NASA_API_KEY`              | `NASA_API_KEY`               | NASA APIs                                              |
| `NASA_EARTHDATA_TOKEN`      | `NASA_EARTHDATA_TOKEN`       | NASA Earthdata                                         |
| `NEWS_API_KEY`              | `NEWSAPI_API_KEY`            | NewsAPI                                                |
| `THENEWS_API_KEY`           | `THENEWSAPI_API_KEY`         | TheNewsAPI                                             |
| `WEATHERAPI_API_KEY`        | `WEATHERAPI_API_KEY`         | WeatherAPI                                             |
| `XAI_API_KEY`               | `XAI_API_KEY`                | xAI                                                    |
| `O365_CLIENT_ID`            | `O365_CLIENT_ID`             | Microsoft 365 OAuth client ID                          |
| `O365_CLIENT_SECRET`        | `O365_CLIENT_SECRET`         | Microsoft 365 OAuth client secret                      |
| `OPENAQ_API_KEY`            | `OPENAQ_API_KEY`             | OpenAQ                                                 |
| `OPENSKY_API_CLIENT_ID`     | `OPENSKY_API_CLIENT_ID`      | OpenSky API client ID                                  |
| `OPENSKY_API_CREDENTIALS`   | `OPENSKY_API_CREDENTIALS`    | OpenSky API credentials                                |
| `OPENSKY_API_CLIENT_SECRET` | `OPENSKY_API_CLIENT_ID`      | OpenSky API client secret binding in current config.py |
| `CENSUS_API_KEY`            | `CENSUS_API_KEY`             | U.S. Census                                            |
| `SOCRATA_API_KEY`           | `SOCRATA_API_KEY`            | Socrata                                                |
| `HEALTHDATA_API_KEY`        | `HEALTHDATA_API_KEY`         | HealthData.gov                                         |
| `USGS_WATERDATA_API_KEY`    | `USGS_API_KEY`               | USGS                                                   |
| `DATA_GOV_API_KEY`          | `DATAGOV_API_KEY`            | Data.gov                                               |
| `FIRMS_MAP_KEY`             | `FIRMS_MAP_KEY`              | NASA FIRMS                                             |
| `PURPLEAIR_API_KEY`         | `PURPLEAIR_API_KEY`          | PurpleAir                                              |
| `SKY_MAP_TOKEN`             | `SKY_MAP_TOKEN`              | Sky Map                                                |


## 🤖 Provider Integrations

### OpenAI Agents SDK

```python
from agents import Agent, Runner

from fonky.gpt.tools import fetch_arxiv
from fonky.gpt.tools import fetch_wikipedia

agent = Agent(
    name='Research Assistant',
    instructions='Use the supplied Fonky tools when required.',
    tools=[
        fetch_arxiv,
        fetch_wikipedia,
    ] )

result = Runner.run_sync(
    agent,
    'Research retrieval augmented generation.' )

print( result.final_output )
```

### Google ADK

```python
from google.adk.agents import Agent

from fonky.gemini.tools import fetch_arxiv
from fonky.gemini.tools import fetch_wikipedia

agent = Agent(
    name='research_assistant',
    model='gemini-3.7-flash',
    instruction='Use the supplied Fonky tools when required.',
    tools=[
        fetch_arxiv,
        fetch_wikipedia,
    ] )
```

### xAI Grok

```python
from fonky.grok.tools import cse_search_tool
from fonky.grok.tools import fetch_cse_search

tools = [
    cse_search_tool,
]

# Pass ``tools`` to the xAI chat request.
# When Grok requests ``fetch_cse_search``, execute the callable locally:
result = fetch_cse_search(
    keywords='federal appropriations law',
    results=5 )
```

### LangChain

```python
from fonky.langchain.tools import fetch_arxiv
from fonky.langchain.tools import fetch_wikipedia

tools = [
    fetch_arxiv,
    fetch_wikipedia,
]
```

## ✅ Validation

```powershell
python -m compileall .\fonky
python -c "import fonky; import fonky.gpt.tools; import fonky.gemini.tools; import fonky.grok.tools; import fonky.langchain.tools; print('ok')"
```

## 📚 Documentation

- [Tools Reference](resources/Tools.md)
- [User Guide](resources/user-guide.md)
- [MkDocs Site](https://is-leeroy-jenkins.github.io/Fonky/)

## 📝 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/is-leeroy-jenkins/Fonky/blob/main/LICENSE.txt)