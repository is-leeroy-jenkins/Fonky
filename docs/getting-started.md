# Getting Started

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Install Playwright's Chromium runtime when using browser-backed features:

```powershell
python -m playwright install chromium
```

## Verify the package

```powershell
python -c "from fonky import fonky; print('Fonky import succeeded')"
```

## First local document workflow

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

## First scraper workflow

```python
from fonky import fonky

tables = fonky.scrape_tables(uri='https://example.com')
print(tables)
```

## Functional vs class-based usage

Use `fonky.py` for one-shot operations. Instantiate implementation classes directly when a workflow needs retained state or provider-specific helper methods.
