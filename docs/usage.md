# Usage

## Task to Entry Point

| Task | Recommended Entry Point | Follow-On |
|---|---|---|
| search papers, government data, archives | `fonky.fonky` fetch tools | use `tools.py` for agent selection |
| ingest documents from local or cloud sources | `fonky.fonky` load tools | optional chunking / indexing downstream |
| scrape page sections or links | `fonky.fonky` scrape tools | pair with loaders for recursive capture |
| run an agent with scoped tools | `fonky.tools.get_tools(domain)` | supply only the required domain set |
| debug provider behavior | implementation class | instantiate class in source module directly |

## Common Patterns

- **Research retrieval** — archives → loaders → downstream summarization.
- **Web capture** — recursive load → structured extraction → chunking.
- **Environmental analysis** — weather / air / seismic fetchers → tabular or document downstream processing.
- **Location workflows** — geocoding / directions / imagery → mapping or alerting.

## Execution Reference

```python
from fonky.tools import get_tools

agent_tools = get_tools( domain='archives' )
```

```python
from fonky.fonky import load_pdf

docs = load_pdf.invoke(
    {
        'file_path': 'input.pdf',
        'mode': 'single',
        'strategy': 'fast',
        'extract_images': False
    }
)
```
