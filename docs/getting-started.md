# Getting Started

## Prerequisites

| Requirement | Why It Matters |
|---|---|
| Python 3.11+ | Runs Fonky and its integration libraries. |
| Git | Clones and updates the repository. |
| Virtual environment | Isolates Fonky's broad dependency set. |
| Provider credentials | Required only for providers you actually call. |
| Browser runtime | Required for Playwright-backed web rendering/crawling. |

## Create the Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

When browser-backed retrieval is needed:

```powershell
python -m playwright install chromium
```

## Verify Imports Before Provider Testing

```powershell
python -c "from fonky import fonky; print('Fonky import succeeded')"
```

If that command fails with `ModuleNotFoundError`, resolve the missing Python dependency before
investigating API credentials or provider behavior.

## First Local Workflow — Load a Text File

Start with a local operation so network and credentials are not variables:

```python
from pathlib import Path
from fonky import fonky

path = Path('sample.txt')
path.write_text(
    'Fonky is ready for document ingestion.',
    encoding='utf-8'
)

documents = fonky.load_text(
    path=str(path),
    encoding='utf-8'
)

for document in documents:
    print(document.page_content)
```

## First Web Workflow — Extract Headings

```python
from fonky import fonky

headings = fonky.scrape_headings(
    uri='https://example.com'
)

for heading in headings or []:
    print(heading)
```

## First Provider Workflow — ArXiv

```python
from fonky import fonky

papers = fonky.fetch_arxiv(
    question='agentic retrieval systems',
    max_documents=3,
    full_documents=False,
    include_metadata=True
)

for paper in papers:
    print(paper.metadata)
```

## Validate Documentation Locally

```powershell
python -m pip install mkdocs-material
mkdocs serve
```

Before committing documentation changes:

```powershell
mkdocs build --strict
```

## Next

Use [Configuration](configuration.md) for credentials, then select a workflow in the [User Guide](user-guide.md).
