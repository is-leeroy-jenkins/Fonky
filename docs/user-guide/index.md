# User Guide

The user guide is organized by operation rather than provider.

| Guide | Scope |
|---|---|
| [Provider Setup](providers.md) | Import and register Fonky tools with OpenAI Agents SDK, Google ADK, xAI, and LangChain. |
| [Retrieval](retrieval.md) | Search, public-data, environmental, geospatial, astronomy, health, and web retrieval tools. |
| [Loading](loading.md) | Local documents, cloud files, mail, notebooks, and structured-data loaders. |
| [Web Extraction](web-extraction.md) | Fetching, rendering, crawling, and HTML extraction tools. |
| [Processing](processing.md) | Text normalization, cleaning, chunking, NLP, vectorization, and semantic search. |

## Import a provider tool package

```python
from fonky.gpt import tools as gpt_tools
from fonky.gemini import tools as gemini_tools
from fonky.grok import tools as grok_tools
from fonky.langchain import tools as langchain_tools
```

Use only the integration package required by the active agent framework.
