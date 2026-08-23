# Getting Started

This guide takes a Fonky checkout from an empty Python environment to verified functional and class-based calls.

## Prerequisites

Fonky is a broad integration library. The exact dependency and credential requirements depend on the providers and loaders you call. Start with a supported Python installation, `pip`, the repository, and `requirements.txt`.

## Create a Virtual Environment

```powershell
cd Fonky
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

POSIX:

```bash
cd Fonky
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Optional Browser Runtime

```powershell
python -m playwright install chromium
```

## Configure Only the Services You Use

```powershell
$env:GOOGLE_API_KEY = "..."
$env:GOOGLE_CSE_ID = "..."
$env:GOOGLE_WEATHER_API_KEY = "..."
$env:NASA_API_KEY = "..."
$env:THENEWSAPI_API_KEY = "..."
```

See [Configuration](configuration.md) for the complete source-derived environment-variable inventory.

## Import the Functional API

```python
from fonky import fonky
```

## Verify a Local Loader First

```python
from pathlib import Path
from fonky import fonky

path = Path('sample.txt')
path.write_text('Fonky verification document.', encoding='utf-8')

documents = fonky.load_text(
    path=str(path),
    encoding='utf-8',
    size=1000,
    overlap=100,
    chunk=False
)

print(documents)
```

Local loading is a useful first test because it avoids external service availability.

## Verify Web Extraction

```python
from fonky import fonky

paragraphs = fonky.scrape_paragraphs(
    uri='https://example.com'
)

print(paragraphs)
```

## Verify a Provider Call

After configuring the credentials required by the target provider:

```python
from fonky import fonky

results = fonky.fetch_google_search(
    question='USGS earthquake data',
    exact_terms='',
    exclude_terms='',
    file_type='',
    date_restrict='',
    site_search='',
    site_search_filter='',
    image_search=False,
    country='',
    language='lang_en',
    safe='off',
    max_results=10
)

print(results)
```

## Use Classes Directly When Needed

```python
from fonky.scrapers import WebExtractor

extractor = WebExtractor( )
tables = extractor.scrape_tables(
    uri='https://example.com'
)
```

## Import Failures

Fonky imports a broad dependency surface. A missing integration package can cause import-time failures such as `ModuleNotFoundError`. Resolve the missing package before diagnosing wrapper routing.

```powershell
python -m pip install -r requirements.txt
python -c "from fonky import fonky; print('Fonky import succeeded')"
```

## Build the Documentation

```powershell
python -m mkdocs serve
python -m mkdocs build --strict
```

The replacement bundle validates every local navigation target, local Markdown link, and image reference before packaging.
