# 🧰 Fonky

![](https://github.com/is-leeroy-jenkins/fonky/blob/main/resources/images/fonky-project.png)

<p align="left">
  <a href="#purpose">Purpose</a> &nbsp;|&nbsp;
  <a href="#architecture">Architecture</a> &nbsp;|&nbsp;
  <a href="#installation">Installation</a> &nbsp;|&nbsp;
  <a href="#configuration">Configuration</a> &nbsp;|&nbsp;
  <a href="https://github.com/is-leeroy-jenkins/funkytown/blob/main/resources/Tools.md">Tools</a> &nbsp;|&nbsp;
  <a href="https://github.com/is-leeroy-jenkins/funkytown/blob/main/resources/user-guide.md">User-Guide</a> &nbsp;|&nbsp;
  <a href="#validation">Validation</a> &nbsp;|&nbsp;
  <a href="#documentation">Documentation</a>
</p>

___

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-0078FC?style=for-the-badge&logo=github)](https://is-leeroy-jenkins.github.io/fonky/)

## 🎯 Purpose

| Capability                            | Module                |
|---------------------------------------|-----------------------|
| Data retrieval                        | `fonky.fetchers`      |
| Document ingestion                    | `fonky.loaders`       |
| Web extraction                        | `fonky.scrapers`      |
| Text and NLP preprocessing            | `fonky.preprocessors` |
| Shared models and response structures | `fonky.models`        |
| OpenAI Agents SDK tools               | `fonky.tools`         |
| Runtime configuration                 | `fonky.config`        |
| Error wrapping and logging            | `fonky.boogr`         |


## 🛠️ Architecture 

![](https://github.com/is-leeroy-jenkins/Fonky/blob/main/resources/fonky-architecture.png)

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

### 🔗 Dependency Contract

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

## 📦 Package Structure

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

### 📚 Repository Documentation

```text
README.md
Tools.md
user-guide.md
requirements.txt
```

## ⚙️ Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel
python -m pip install "setuptools==81.0.0"
python -m pip install -r requirements.txt
python -m pip check
```

### 🌐 Playwright

```powershell
python -m playwright install chromium
```

### ✅ Import Validation

```powershell
python -c "import fonky; import fonky.tools; print('ok')"
```


### ▶️ Synchronous Agent

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

### ⏱️  Asynchronous Agent

```python
result = await Runner.run(
    agent,
    'Research retrieval augmented generation.' )
```

### 📡 Streaming Agent

```python
result = Runner.run_streamed(
    agent,
    'Research retrieval augmented generation.' )

async for event in result.stream_events( ):
    print( event )
```

### 🧩 Tool Schema

```python
import json

from agents import FunctionTool
from fonky.tools import fetch_arxiv

if isinstance( fetch_arxiv, FunctionTool ):
    print( fetch_arxiv.name )
    print( fetch_arxiv.description )
    print( json.dumps( fetch_arxiv.params_json_schema, indent=2 ) )
```

### 🧪 Wrapped Callable Test

```python
from fonky.tools import preprocess_normalize_text

value = preprocess_normalize_text.__wrapped__(
    text='  MULTIPLE    SPACES  ' )

print( value )
```


## ✅ Validation

### 🛠️ Compile

```powershell
python -m compileall .\fonky
```

### 📥 Core Imports

```powershell
python -c "from fonky.fetchers import ArXiv; from fonky.loaders import PdfLoader; from fonky.scrapers import WebExtractor; from fonky.preprocessors import TextParser; print('ok')"
```



## 📝 License

- [MIT License](https://github.com/is-leeroy-jenkins/fonky/blob/main/LICENSE.txt)

