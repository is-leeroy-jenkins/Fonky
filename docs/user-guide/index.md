# User Guide

## Provider Integration

| Guide | Scope |
|---|---|
| [Provider Setup](providers.md) | OpenAI Agents SDK, Google ADK, xAI Grok, and LangChain registration and invocation. |
| [Configuration & API Keys](configuration.md) | Environment variables, API keys, OAuth credentials, Google service settings, and a complete `.env` template. |

## Tool Domains

| Domain | Tools | Guide |
|---|---:|---|
| Research & Reference | 11 | [Research & Reference](research-reference.md) |
| Astronomy & Space | 10 | [Astronomy & Space](astronomy-space.md) |
| Cloud & Storage | 8 | [Cloud & Storage](cloud-storage.md) |
| Demographics & Public Data | 5 | [Demographics & Public Data](demographics-public-data.md) |
| Documents & Files | 18 | [Documents & Files](documents-files.md) |
| Environment & Weather | 19 | [Environment & Weather](environment-weather.md) |
| Geospatial | 10 | [Geospatial](geospatial.md) |
| Health & Science | 4 | [Health & Science](health-science.md) |
| Web Retrieval & Loading | 11 | [Web Retrieval & Loading](web-retrieval-loading.md) |
| Web Scraping | 14 | [Web Scraping](web-scraping.md) |
| Processing & NLP | 40 | [Processing & NLP](processing-nlp.md) |
| **Total** | **150** | |

## Provider Import Paths

```python
from fonky.gpt import tools as gpt_tools
from fonky.gemini import tools as gemini_tools
from fonky.grok import tools as grok_tools
from fonky.langchain import tools as langchain_tools
```