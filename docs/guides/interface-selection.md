# Interface Selection

## Choose by Required Control

| Need | Surface |
|---|---|
| invoke a single public operation | `fonky.py` |
| retrieve a domain-scoped list of tools | `tools.py` |
| inspect provider or parser behavior | source implementation class |
| build documentation from source docs | API pages via `mkdocstrings` |

## Decision Rules

- choose `fonky.py` for deterministic execution,
- choose `tools.py` for agent-facing tool discovery,
- choose `fetchers.py` / `loaders.py` / `scrapers.py` when you need implementation behavior directly,
- choose API pages only as a source browser, not as a runtime surface.
