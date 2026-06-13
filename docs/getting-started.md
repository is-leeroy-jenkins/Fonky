# Getting Started

This guide walks through setting up Fonky locally, validating the Python environment, installing
documentation dependencies, running a first import test, loading a first document, and building the
MkDocs site.

The commands assume a Windows PowerShell environment and a flat source layout where files such as
`loaders.py`, `models.py`, and `config.py` are located at the repository root.

## Prerequisites

Before working with Fonky, confirm the following are available:

| Requirement          | Purpose                                                    |
| -------------------- | ---------------------------------------------------------- |
| Python 3.11 or later | Runtime environment for the source files.                  |
| Git                  | Repository cloning, branching, committing, and deployment. |
| PowerShell           | Command shell used by the examples in this guide.          |
| Virtual environment  | Isolates project dependencies from global Python packages. |
| MkDocs dependencies  | Builds the documentation site.                             |
| Optional API keys    | Required only for external services you use.               |

Check Python:

```powershell
python --version
```

Check Git:

```powershell
git --version
```

## Project Layout

A working Fonky repository should contain the source files, documentation files, and MkDocs
configuration at the repository root.

```text
Fonky/
|-- mkdocs.yml
|-- README.md
|-- requirements.txt
|-- docs/
|   |-- index.md
|   |-- getting-started.md
|   |-- configuration.md
|   |-- architecture.md
|   |-- logging.md
|   |-- usage.md
|   |-- user-guide.md
|   |-- development.md
|   |-- github-pages.md
|   |-- api/
|   |   |-- index.md
|   |   |-- archives.md
|   |   |-- astronomical.md
|   |   |-- boogr.md
|   |   |-- cloud.md
|   |   |-- config.md
|   |   |-- core.md
|   |   |-- demographic.md
|   |   |-- documents.md
|   |   |-- environmental.md
|   |   |-- fetchers.md
|   |   |-- geospatial.md
|   |   |-- health.md
|   |   |-- loaders.md
|   |   |-- models.md
|   |   |-- processors.md
|   |   |-- scrapers.md
|   |   +-- web.md
|   |-- stylesheets/
|   |   +-- extra.css
|   +-- javascripts/
|       +-- extra.js
|-- __init__.py
|-- archives.py
|-- astronomical.py
|-- boogr.py
|-- cloud.py
|-- config.py
|-- core.py
|-- demographic.py
|-- documents.py
|-- environmental.py
|-- fetchers.py
|-- geospatial.py
|-- health.py
|-- loaders.py
|-- models.py
|-- processors.py
|-- scrapers.py
+-- web.py
```

## Create the Virtual Environment

From the repository root:

```powershell
cd C:\Users\terry\source\repos\Fonky
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

After activation, the prompt should begin with:

```text
(.venv)
```

Upgrade `pip`:

```powershell
python -m pip install --upgrade pip
```

## Install Runtime Requirements

Install project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Fonky includes many optional integrations. Some modules depend on cloud SDKs, browser tooling,
document parsing packages, OCR packages, or external API credentials. You only need credentials for
the providers you actually use.

## Install Documentation Requirements

Install the MkDocs documentation toolchain:

```powershell
python -m pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python pymdown-extensions
```

The recommended `requirements.txt` section is:

```text
# Documentation
mkdocs
mkdocs-material
mkdocstrings
mkdocstrings-python
pymdown-extensions
```

## Install Browser Support for Scraping

Some scraping workflows may use Playwright.

Install Chromium support:

```powershell
python -m playwright install chromium
```

This is only required for workflows that depend on browser rendering or dynamic page extraction.

## Configure Environment Variables

Fonky reads service keys and runtime settings from `config.py`.

Set only the values required for the services you plan to call.

Example PowerShell values:

```powershell
$env:OPENAI_API_KEY = "your-openai-api-key"
$env:GOOGLE_API_KEY = "your-google-api-key"
$env:GOOGLE_CSE_ID = "your-google-custom-search-engine-id"
$env:NASA_API_KEY = "your-nasa-api-key"
$env:GOVINFO_API_KEY = "your-govinfo-api-key"
$env:CONGRESS_API_KEY = "your-congress-api-key"
```

The default logging database is:

```text
logging/Exceptions.db
```

The default logging table is:

```text
Exceptions
```

Override the logging location when needed:

```powershell
$env:LOG_DIR = "C:\Users\terry\source\repos\Fonky\logging"
$env:LOG_PATH = "C:\Users\terry\source\repos\Fonky\logging\Exceptions.db"
$env:LOG_FILE = "Exceptions"
```

## Validate Source Files

Compile the full project:

```powershell
python -m compileall .
```

Compile targeted files:

```powershell
python -m py_compile .\boogr.py
python -m py_compile .\config.py
python -m py_compile .\core.py
python -m py_compile .\archives.py
python -m py_compile .\fetchers.py
python -m py_compile .\loaders.py
python -m py_compile .\models.py
python -m py_compile .\processors.py
python -m py_compile .\scrapers.py
```

A successful compile check confirms syntax validity. It does not guarantee that every optional
provider dependency or API credential is installed.

## Validate Basic Imports

Run a basic import check from the repository root:

```powershell
python -c "import config; import boogr; import core; import loaders; import models; print('Fonky imports passed')"
```

Expected output:

```text
Fonky imports passed
```

If this fails, resolve missing dependencies or source import errors before continuing to MkDocs.

## Create a Sample File

Create a simple test document:

```powershell
New-Item -ItemType Directory -Force .\data | Out-Null
"Fonky loads documents, processes text, and exposes callable tools." | Set-Content .\data\sample.txt -Encoding UTF8
```

Confirm the file exists:

```powershell
Test-Path .\data\sample.txt
```

Expected output:

```text
True
```

## First Document Load

Use `TextLoader` to load the sample file.

```python
from loaders import TextLoader

loader = TextLoader()

documents = loader.load(
    path="data/sample.txt",
    encoding="utf-8"
)

print("Document count:", len(documents))

for document in documents:
    print("Metadata:", document.metadata)
    print("Content:", document.page_content)
    break
```

PowerShell inline version:

```powershell
python -c "from loaders import TextLoader; loader = TextLoader(); docs = loader.load(path='data/sample.txt', encoding='utf-8'); print(len(docs)); print(next(iter(docs)).page_content)"
```

## First Document Split

After loading a document, split it into chunks:

```python
from loaders import TextLoader

loader = TextLoader()

loader.load(
    path="data/sample.txt",
    encoding="utf-8"
)

chunks = loader.split(
    chunk=1000,
    overlap=200
)

print("Chunk count:", len(chunks))

for chunk in chunks:
    print(chunk.page_content)
    break
```

PowerShell inline version:

```powershell
python -c "from loaders import TextLoader; loader = TextLoader(); loader.load(path='data/sample.txt', encoding='utf-8'); chunks = loader.split(chunk=1000, overlap=200); print(len(chunks)); print(next(iter(chunks)).page_content)"
```

## First AI Tool Definition

Fonky can expose functions and methods as structured AI-callable tools through `ToolDef`.

Create a tool from `TextLoader.load`:

```python
from loaders import TextLoader
from models import ToolDef

loader = TextLoader()

tool = ToolDef.from_method(
    target=loader,
    method="load",
    name="load_text_file",
    description="Load a local text file into document objects.",
    category="documents"
)

print(tool.to_dict())
```

Call the tool directly:

```python
result = tool.call(
    {
        "path": "data/sample.txt",
        "encoding": "utf-8"
    }
)

print("Succeeded:", result.get("ok"))

if result.get("ok"):
    for item in result.get("data"):
        print(item.get("page_content"))
        break
else:
    print(result.get("error"))
```

Export a provider schema:

```python
schema = tool.to_openai()
print(schema)
```

This is the basic pattern for exposing Fonky loaders, fetchers, scrapers, and processors as AI
tool-calling functions.

## Validate Logging

Fonky handled exceptions should use `boogr.Error` and `boogr.Logger`.

The required source pattern is:

```python
except Exception as e:
    exception = Error(e)
    exception.module = "loaders"
    exception.cause = "TextLoader"
    exception.method = "load(self, path: str, encoding: Optional[str]=None) -> List[Document]"
    Logger().write(exception)
    raise exception
```

Create the logging directory:

```powershell
New-Item -ItemType Directory -Force .\logging | Out-Null
```

Run a direct logger test:

```powershell
python -c "from boogr import Error, Logger; import config as cfg; error = Error(Exception('logging validation')); error.module = 'logging'; error.cause = 'ManualValidation'; error.method = 'manual logger validation'; Logger().write(error); print(cfg.LOG_PATH)"
```

Confirm the database exists:

```powershell
Test-Path .\logging\Exceptions.db
```

Expected output:

```text
True
```

## Build the Documentation Site

Confirm `mkdocs.yml` exists:

```powershell
Test-Path .\mkdocs.yml
```

Confirm the `docs/` folder exists:

```powershell
Test-Path .\docs
```

Confirm API pages exist:

```powershell
Get-ChildItem .\docs\api
```

Build the site:

```powershell
mkdocs build
```

Serve the site locally:

```powershell
mkdocs serve
```

Open:

```text
http://127.0.0.1:8000/
```

## Confirm API Pages Render Docstrings

The API pages must contain live mkdocstrings directives.

Confirm the API pages have them:

```powershell
Select-String -Path .\docs\api\*.md -Pattern "^:::\s+[A-Za-z_]"
```

Expected output should include entries such as:

```text
docs\api\loaders.md:3:::: loaders
docs\api\fetchers.md:3:::: fetchers
docs\api\processors.md:3:::: processors
docs\api\models.md:3:::: models
```

Manual pages should not contain live mkdocstrings directives:

```powershell
Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"
```

Expected output:

```text
No output.
```

## Common Setup Problems

### MkDocs cannot import a module

Confirm that the API directive matches the flat source layout.

Correct for this project:

```text
::: loaders
```

Incorrect for this project:

```text
::: fonky.loaders
```

The repository currently does not use a `fonky/` package folder, so `fonky.loaders` is not
importable.

### API docstrings do not render

Check the relevant API page:

```powershell
Get-Content .\docs\api\loaders.md
```

It should contain:

```text
::: loaders
```

If it contains only prose, mkdocstrings has nothing to render.

### Manual pages create duplicate API targets

Manual pages should not contain live directives such as:

```text
::: loaders
```

Only `docs/api/*.md` should contain those directives.

### Griffe warns about return values

Use typed Google-style returns in source docstrings:

```text
Returns:
    list[str]: Supported option values.
```

Do not use:

```text
Returns:
    Supported option values.
```

Do not use `Returns: None`. For no-return procedures, omit the `Returns:` section.

### Autorefs warns about numeric references

Avoid Python bracket indexing and slicing in Markdown examples.

Use this:

```python
for document in documents:
    print(document.page_content)
    break
```

Avoid this:

```python
print(documents[0].page_content[:1000])
```

## Setup Checklist

| Check                              | Command                                                                                                                                             |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Virtual environment active         | Confirm prompt begins with `(.venv)`                                                                                                                |
| Dependencies installed             | `python -m pip install -r requirements.txt`                                                                                                         |
| MkDocs installed                   | `python -m pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python pymdown-extensions`                                                  |
| Source compiles                    | `python -m compileall .`                                                                                                                            |
| Core imports work                  | `python -c "import config; import loaders; import models; print('ok')"`                                                                             |
| Sample text loads                  | `python -c "from loaders import TextLoader; loader = TextLoader(); docs = loader.load(path='data/sample.txt', encoding='utf-8'); print(len(docs))"` |
| API pages contain directives       | `Select-String -Path .\docs\api\*.md -Pattern "^:::\s+[A-Za-z_]"`                                                                                   |
| Manual pages contain no directives | `Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"`                                                                                       |
| Docs build                         | `mkdocs build`                                                                                                                                      |
| Docs serve locally                 | `mkdocs serve`                                                                                                                                      |

