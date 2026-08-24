# Getting Started

## Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel
python -m pip install "setuptools==81.0.0"
python -m pip install -r requirements.txt
python -m pip check
```

## Smoke Tests

```powershell
python -c "from fonky.fonky import fetch_arxiv; print(fetch_arxiv.name)"
python -c "from fonky.tools import get_domains; print(get_domains())"
```

## First Direct Invocation

```python
from fonky.fonky import fetch_arxiv

result = fetch_arxiv.invoke(
    {
        'question': 'federal AI governance',
        'max_documents': 3,
        'full_documents': False,
        'include_metadata': True
    }
)
```

## First Domain Tool Set

```python
from fonky.tools import get_tools

web_tools = get_tools( domain='web' )
```

## Runtime Expectations

- Public exports in `fonky.py` are `BaseTool` objects.
- Direct calls use `.invoke(...)`.
- `tools.py` groups existing tools; it does not define new ones.
- Google-style docstrings are part of the runtime contract because tool schemas are parsed from them.

## Validation Checklist

- `pip check` returns no broken requirements.
- `pytest` completes for decorator and runtime tests.
- `mkdocs build --strict` completes without navigation or import errors.
