# ðŸš€ Getting Started

This guide walks through setting up Fonky locally, validating the Python environment, installing
documentation dependencies, running a first import test, loading a first document, and building the
MkDocs site.



## âœ… Prerequisites

Fonky is a Python project that uses document loaders, web fetchers, scrapers, text processors,
structured models, and MkDocs-generated API documentation.

Before setup, confirm you have:

| Requirement            | Purpose                                                            |
|------------------------|--------------------------------------------------------------------|
| Python 3.11 or later   | Runtime environment for Fonky source files.                        |
| Git                    | Clone, branch, commit, and deploy the repository.                  |
| PowerShell             | Windows command shell used in the examples below.                  |
| A virtual environment  | Keeps Fonky dependencies isolated from global Python packages.     |
| MkDocs dependencies    | Builds the documentation site from Markdown and Python docstrings. |
| Optional API keys      | Required only for external services you plan to call.              |

Confirm Python is available:

```powershell
python --version
```

Confirm Git is available:

```powershell
git --version
```



## ðŸ“ Project Layout

A working Fonky repository should contain the source files, documentation files, and MkDocs
configuration at the repository root.

Expected high-level structure:

```text
Fonky/
â”œâ”€â”€ mkdocs.yml
â”œâ”€â”€ README.md
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ index.md
â”‚   â”œâ”€â”€ getting-started.md
â”‚   â”œâ”€â”€ configuration.md
â”‚   â”œâ”€â”€ architecture.md
â”‚   â”œâ”€â”€ logging.md
â”‚   â”œâ”€â”€ usage.md
â”‚   â”œâ”€â”€ user-guide.md
â”‚   â”œâ”€â”€ development.md
â”‚   â”œâ”€â”€ github-pages.md
â”‚   â”œâ”€â”€ api/
â”‚   â”‚   â”œâ”€â”€ index.md
â”‚   â”‚   â”œâ”€â”€ archives.md
â”‚   â”‚   â”œâ”€â”€ astronomical.md
â”‚   â”‚   â”œâ”€â”€ boogr.md
â”‚   â”‚   â”œâ”€â”€ cloud.md
â”‚   â”‚   â”œâ”€â”€ config.md
â”‚   â”‚   â”œâ”€â”€ core.md
â”‚   â”‚   â”œâ”€â”€ demographic.md
â”‚   â”‚   â”œâ”€â”€ documents.md
â”‚   â”‚   â”œâ”€â”€ environmental.md
â”‚   â”‚   â”œâ”€â”€ fetchers.md
â”‚   â”‚   â”œâ”€â”€ geospatial.md
â”‚   â”‚   â”œâ”€â”€ health.md
â”‚   â”‚   â”œâ”€â”€ loaders.md
â”‚   â”‚   â”œâ”€â”€ models.md
â”‚   â”‚   â”œâ”€â”€ processors.md
â”‚   â”‚   â”œâ”€â”€ scrapers.md
â”‚   â”‚   â””â”€â”€ web.md
â”‚   â””â”€â”€ stylesheets/
â”‚       â””â”€â”€ extra.css
â”œâ”€â”€ __init__.py
â”œâ”€â”€ archives.py
â”œâ”€â”€ astronomical.py
â”œâ”€â”€ boogr.py
â”œâ”€â”€ cloud.py
â”œâ”€â”€ config.py
â”œâ”€â”€ core.py
â”œâ”€â”€ demographic.py
â”œâ”€â”€ documents.py
â”œâ”€â”€ environmental.py
â”œâ”€â”€ fetchers.py
â”œâ”€â”€ geospatial.py
â”œâ”€â”€ health.py
â”œâ”€â”€ loaders.py
â”œâ”€â”€ models.py
â”œâ”€â”€ processors.py
â”œâ”€â”€ scrapers.py
â””â”€â”€ web.py
```

!!! note
If your Python files are later moved into a package folder such as `fonky/`, the API reference
directives and import examples should use `fonky.<module>` paths instead of root-level module paths.



## ðŸ§± Create and Activate the Virtual Environment

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



## ðŸ“¦ Install Runtime Requirements

Install the project dependencies from `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

Fonky uses a broad set of optional integrations. Some modules depend on third-party services, cloud
SDKs, browser tooling, OCR packages, or document-parsing libraries. You only need API credentials
for the services you actually call.



## ðŸ“š Install Documentation Requirements

MkDocs does not build automatically from source comments. It needs a documentation toolchain.

Make sure the following packages are installed:

```powershell
python -m pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python pymdown-extensions
```

Recommended `requirements.txt` section:

```text
# Documentation
mkdocs
mkdocs-material
mkdocstrings
mkdocstrings-python
pymdown-extensions
```



## ðŸŒ Install Browser Support for Scraping

Some web scraping and browser-backed retrieval workflows may require Playwright browser binaries.

Install Chromium support:

```powershell
python -m playwright install chromium
```

This is only required for workflows that use browser rendering or dynamic page extraction.



## ðŸ” Configure Environment Variables

Fonky reads service keys and runtime settings from `config.py`.

Set only the values needed for the services you plan to call.

Example PowerShell setup:

```powershell
$env:OPENAI_API_KEY = "your-openai-api-key"
$env:GOOGLE_API_KEY = "your-google-api-key"
$env:GOOGLE_CSE_ID = "your-google-custom-search-engine-id"
$env:GOOGLE_WEATHER_API_KEY = "your-google-weather-api-key"
$env:NASA_API_KEY = "your-nasa-api-key"
$env:GOVINFO_API_KEY = "your-govinfo-api-key"
$env:CONGRESS_API_KEY = "your-congress-api-key"
$env:THENEWSAPI_API_KEY = "your-thenewsapi-key"
```

Fonky logging defaults to:

```text
logging/Exceptions.db
```

with table name:

```text
Exceptions
```

Override the logging location when needed:

```powershell
$env:LOG_DIR = "C:\Users\terry\source\repos\Fonky\logging"
$env:LOG_PATH = "C:\Users\terry\source\repos\Fonky\logging\Exceptions.db"
$env:LOG_FILE = "Exceptions"
```



## ðŸ§ª Validate the Source Files

Run a full compile check from the repository root:

```powershell
python -m compileall .
```

For targeted checks:

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

A successful compile check confirms the files are syntactically valid. It does not guarantee every
optional provider dependency or API credential is installed and configured.



## ðŸ”Ž Validate Basic Imports

Run a small import test from the repository root:

```powershell
python -c "import config; import boogr; import core; import loaders; import models; print('Fonky imports passed')"
```

If the source files are later moved into a package folder named `fonky`, use:

```powershell
python -c "import fonky.config; import fonky.boogr; import fonky.core; import fonky.loaders; import fonky.models; print('Fonky package imports passed')"
```



## ðŸ“„ First Document Load

Create a simple test file:

```powershell
New-Item -ItemType Directory -Force .\data | Out-Null
"Fonky loads documents, processes text, and exposes callable tools." | Set-Content .\data\sample.txt -Encoding UTF8
```

Load the file:

```python
from loaders import TextLoader

loader = TextLoader()

documents = loader.load(
	path="data/sample.txt",
	encoding="utf-8"
)

print("Document count:", len(documents))

for document_number, document in enumerate(documents, start=1):
	print("Document:", document_number)
	print("Metadata:", document.metadata)
	print("Content:", document.page_content)
	break
```

Run it from PowerShell as an inline test:

```powershell
python -c "from loaders import TextLoader; loader = TextLoader(); docs = loader.load(path='data/sample.txt', encoding='utf-8'); print(len(docs)); print(next(iter(docs)).page_content)"
```

If your source files are inside a package folder named `fonky`, use:

```powershell
python -c "from fonky.loaders import TextLoader; loader = TextLoader(); docs = loader.load(path='data/sample.txt', encoding='utf-8'); print(len(docs)); print(next(iter(docs)).page_content)"
```



## âœ‚ï¸ First Document Split

After loading a document, split it into chunks:

```python
from loaders import TextLoader

loader = TextLoader()

documents = loader.load(
	path="data/sample.txt",
	encoding="utf-8"
)

chunks = loader.split(
	chunk=1000,
	overlap=200
)

print("Chunk count:", len(chunks))

for chunk_number, chunk in enumerate(chunks, start=1):
	print("Chunk:", chunk_number)
	print(chunk.page_content)
	break
```

Inline PowerShell check:

```powershell
python -c "from loaders import TextLoader; loader = TextLoader(); loader.load(path='data/sample.txt', encoding='utf-8'); chunks = loader.split(chunk=1000, overlap=200); print(len(chunks)); print(next(iter(chunks)).page_content)"
```



## ðŸ› ï¸ First Tool Definition

Fonky can expose functions and methods as structured tool definitions.

Create a tool from `TextLoader.load`:

```python
from loaders import TextLoader
from models import ToolDef

tool = ToolDef.from_method(
	target=TextLoader(),
	method="load",
	name="load_text_file",
	category="documents"
)

schema = tool.to_openai()

print(schema)
```

Call the tool:

```python
result = tool.call(
	{
		"path": "data/sample.txt",
		"encoding": "utf-8"
	}
)

print("Succeeded:", result.get("ok"))

if result.get("ok"):
	data = result.get("data")
	for item in data:
		print(item.get("page_content"))
		break
else:
	print(result.get("error"))
```



## ðŸªµ Confirm Logging Setup

Fonky handled exceptions use `boogr.Error` and `boogr.Logger`.

The required pattern is:

```python
except Exception as e:
	exception = Error(e)
	exception.module = "loaders"
	exception.cause = "TextLoader"
	exception.method = "load(self, path: str, encoding: Optional[str]=None) -> List[Document]"
	Logger().write(exception)
	raise exception
```

To confirm the logger can create the logging database, run a failure intentionally:

```powershell
python -c "from loaders import TextLoader; TextLoader().load(path='data/missing-file.txt', encoding='utf-8')"
```

Expected result:

```text
A wrapped exception is raised.
The logging database is created or updated at logging/Exceptions.db.
```

Then confirm the database file exists:

```powershell
Test-Path .\logging\Exceptions.db
```



## ðŸ“š Build the Documentation Site

Confirm `mkdocs.yml` exists at the repository root:

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



## ðŸ”Œ Confirm mkdocstrings Is Rendering API Pages

The API pages must contain mkdocstrings directives.

Example for root-level module layout:

```markdown
# Loaders API

`::: loaders`
```

Example for package layout:

```markdown
# Loaders API

`::: loaders`
```

Check one API page:

```powershell
Get-Content .\docs\api\loaders.md
```

If the file contains only prose and no `:::` directive, mkdocstrings has nothing to render.



## ðŸ§­ Troubleshooting

### MkDocs fails with `custom_dir` and `NoneType`

Remove this line from `mkdocs.yml`:

```yaml
custom_dir: null
```

Only use `custom_dir` when you have an actual override directory.

Correct:

```yaml
theme:
  name: material
  language: en
```

### API docstrings do not render

Check that each API page contains a directive:

```markdown
`::: loaders`
```

or:

```markdown
`::: loaders`
```

Then verify that `mkdocs.yml` includes the mkdocstrings plugin.

### MkDocs cannot import a module

Use the directive path that matches the actual source layout.

Root-level module:

```markdown
`::: loaders`
```

Package module:

```markdown
`::: loaders`
```

Also confirm the current directory is the repository root when running:

```powershell
mkdocs build
```

### Griffe warns about malformed `Returns:` sections

Use typed Google-style return sections:

```text
Returns:
	list[str]: Supported option values.
```

Do not use untyped return descriptions such as:

```text
Returns:
	Supported option values.
```

Do not use:

```text
Returns:
	None: No value is returned.
```

For procedures that do not return a value, omit the `Returns:` section.

### MkDocs autorefs warns about `0` or `:1000`

Avoid Python bracket indexing and slicing in Markdown code examples when autorefs interprets them as
cross-reference syntax.

Use iterator examples instead of this pattern:

```python
print(documents[0].page_content[:1000])
```

Preferred:

```python
for document in documents:
	print(document.page_content)
	break
```



## âœ… Setup Checklist

Use this checklist to confirm the project is ready:

| Check                        | Command                                                                                             |
|------------------------------|-----------------------------------------------------------------------------------------------------|
| Virtual environment active   | Confirm prompt begins with `(.venv)`                                                                |
| Dependencies installed       | `python -m pip install -r requirements.txt`                                                         |
| MkDocs installed             | `python -m pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python pymdown-extensions`  |
| Source compiles              | `python -m compileall .`                                                                            |
| Core imports work            | `python -c "import config; import loaders; import models; print('ok')"`                             |
| Sample text loads            | `python -c "from loaders import TextLoader; print(TextLoader().load('data/sample.txt'))"`           |
| Docs build                   | `mkdocs build`                                                                                      |
| Docs serve locally           | `mkdocs serve`                                                                                      |
| API pages render docstrings  | Confirm `docs/api/*.md` files contain `:::` directives                                              |



## âž¡ï¸ Next Step

After setup succeeds, continue to:

* [Configuration](configuration.md) for environment variables and service settings.
* [Architecture](architecture.md) for module responsibilities and data flow.
* [User Guide](user-guide.md) for detailed usage examples.
* [API Reference](api/index.md) for source-generated documentation.


