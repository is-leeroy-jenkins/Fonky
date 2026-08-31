# Fonky

![](https://github.com/is-leeroy-jenkins/fonky/blob/main/resources/images/fonky-project.png)

<p align="left">
  <a href="#purpose">Purpose</a> &nbsp;|&nbsp;
  <a href="#architecture">Architecture</a> &nbsp;|&nbsp;
  <a href="#installation">Installation</a> &nbsp;|&nbsp;
  <a href="#configuration">Configuration</a> &nbsp;|&nbsp;
  <a href="#direct-python-api">Python API</a> &nbsp;|&nbsp;
  <a href="#openai-agents-sdk">Agents SDK</a> &nbsp;|&nbsp;
  <a href="#validation">Validation</a> &nbsp;|&nbsp;
  <a href="#documentation">Documentation</a>
</p>

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-0078FC?style=for-the-badge&logo=github)](https://is-leeroy-jenkins.github.io/fonky/)

## Purpose

| Capability | Module |
|---|---|
| Data retrieval | `fonky.fetchers` |
| Document ingestion | `fonky.loaders` |
| Web extraction | `fonky.scrapers` |
| Text and NLP preprocessing | `fonky.preprocessors` |
| Shared models and response structures | `fonky.models` |
| OpenAI Agents SDK tools | `fonky.tools` |
| Runtime configuration | `fonky.config` |
| Error wrapping and logging | `fonky.boogr` |

### Tool Inventory

| Tool Type | Count |
|---|---:|
| Retrieval, loading, and scraping tools | 110 |
| Preprocessing and NLTK tools | 40 |
| **Total OpenAI `FunctionTool` objects** | **150** |

## Architecture

```text
OpenAI Agent / Application
           |
           v
      fonky/tools.py
  @function_tool wrappers
           |
   +-------+---------+-------------+
   |       |         |             |
   v       v         v             v
fetchers loaders  scrapers  preprocessors
   |       |         |             |
   +-------+---------+-------------+
           |
           v
        models.py

config.py
boogr.py
```

### Dependency Contract

```text
tools.py -> fetchers.py
tools.py -> loaders.py
tools.py -> scrapers.py
tools.py -> preprocessors.py

fetchers.py       -X-> tools.py
loaders.py        -X-> tools.py
scrapers.py       -X-> tools.py
preprocessors.py  -X-> tools.py
```

## Package Structure

```text
fonky/
├── __init__.py
├── boogr.py
├── config.py
├── fetchers.py
├── loaders.py
├── models.py
├── preprocessors.py
├── scrapers.py
└── tools.py
```

### Repository Documentation

```text
README.md
Tools.md
user-guide.md
requirements.txt
```

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel
python -m pip install "setuptools==81.0.0"
python -m pip install -r requirements.txt
python -m pip check
```

### Playwright

```powershell
python -m playwright install chromium
```

### Import Validation

```powershell
python -c "import fonky; import fonky.tools; print('ok')"
```

## Configuration

```python
from fonky import config
```

### Environment Variables

```text
OPENAI_API_KEY
GOOGLE_API_KEY
GOOGLE_CSE_ID
GOOGLE_WEATHER_API_KEY
GOOGLE_ACCOUNT_CREDENTIALS
GOOGLE_DRIVE_TOKEN_PATH
GOOGLE_DRIVE_FOLDER_ID
GEMINI_API_KEY
NASA_API_KEY
NASA_EARTHDATA_TOKEN
THENEWSAPI_API_KEY
AIRNOW_API_KEY
CONGRESS_API_KEY
OPENAQ_API_KEY
PURPLEAIR_API_KEY
FIRMS_MAP_KEY
PINECONE_API_KEY
XAI_API_KEY
```

```powershell
$env:OPENAI_API_KEY = "..."
$env:GOOGLE_API_KEY = "..."
$env:GOOGLE_CSE_ID = "..."
```

## Direct Python API

### Fetcher

```python
from fonky.fetchers import ArXiv

fetcher = ArXiv( )

documents = fetcher.fetch(
    question='retrieval augmented generation',
    max_documents=5,
    full_documents=False,
    include_metadata=True )
```

### Loader

```python
from fonky.loaders import TextLoader

loader = TextLoader( )

documents = loader.load(
    path='data/sample.txt',
    encoding='utf-8' )
```

### Scraper

```python
from fonky.scrapers import WebExtractor

extractor = WebExtractor( )

paragraphs = extractor.scrape_paragraphs(
    uri='https://example.com' )
```

### Preprocessor

```python
from fonky.preprocessors import TextParser

parser = TextParser( )

value = parser.normalize_text(
    text='Fonky PROVIDES reusable preprocessing.' )
```

## OpenAI Agents SDK

### Function Tools

```python
from fonky.tools import fetch_arxiv
from fonky.tools import load_pdf
from fonky.tools import preprocess_normalize_text
from fonky.tools import scrape_tables
```

### Synchronous Agent

```python
from agents import Agent, Runner

from fonky.tools import fetch_arxiv
from fonky.tools import fetch_wikipedia

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

### Asynchronous Agent

```python
result = await Runner.run(
    agent,
    'Research retrieval augmented generation.' )
```

### Streaming Agent

```python
result = Runner.run_streamed(
    agent,
    'Research retrieval augmented generation.' )

async for event in result.stream_events( ):
    print( event )
```

### Tool Schema

```python
import json

from agents import FunctionTool
from fonky.tools import fetch_arxiv

if isinstance( fetch_arxiv, FunctionTool ):
    print( fetch_arxiv.name )
    print( fetch_arxiv.description )
    print( json.dumps( fetch_arxiv.params_json_schema, indent=2 ) )
```

### Wrapped Callable Test

```python
from fonky.tools import preprocess_normalize_text

value = preprocess_normalize_text.__wrapped__(
    text='  MULTIPLE    SPACES  ' )

print( value )
```

## Internal LangChain Dependencies

| Package | Runtime Use |
|---|---|
| `langchain-core` | `Document` and core abstractions |
| `langchain-community` | Loaders and retrievers |
| `langchain-text-splitters` | Text splitting |
| `langchain-google-community` | Google integrations |
| `langchain-googledrive` | Google Drive retrieval |

```text
LangChain @tool: not used
OpenAI Agents SDK @function_tool: used by fonky.tools
```

## Validation

### Compile

```powershell
python -m compileall .\fonky
```

### Core Imports

```powershell
python -c "from fonky.fetchers import ArXiv; from fonky.loaders import PdfLoader; from fonky.scrapers import WebExtractor; from fonky.preprocessors import TextParser; print('ok')"
```

### Tool Imports

```powershell
python -c "from fonky.tools import fetch_arxiv, load_pdf, scrape_tables, preprocess_normalize_text; print('ok')"
```

### Dependency Integrity

```powershell
python -m pip check
```

### Tool Count

```python
import inspect

import fonky.tools as tools

count = sum(
    1
    for _, value in inspect.getmembers( tools )
    if value.__class__.__name__ == 'FunctionTool'
)

print( count )
```

```text
150
```

## Documentation

| File | Scope |
|---|---|
| `README.md` | Installation, architecture, configuration, validation |
| `Tools.md` | Complete 150-tool API reference |
| `user-guide.md` | Production usage patterns and examples |

### MkDocs

```powershell
mkdocs build
mkdocs serve
```

```text
http://127.0.0.1:8000/
```

## License

[LICENSE.txt](https://github.com/is-leeroy-jenkins/fonky/blob/main/LICENSE.txt)
