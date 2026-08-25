# Troubleshooting Guide

### Diagnostic Flow

1. import the target tool,
2. confirm `.invoke(...)` usage,
3. validate required provider settings,
4. validate file path or URL,
5. test the implementation class directly,
6. rebuild docs with `mkdocs build --strict` if the issue is documentation.

### Tooling Problems

| Problem | Corrective Action |
|---|---|
| `BaseTool` expected but plain function assumptions remain | update calling code to `.invoke(...)` |
| invalid tool schema | repair Google-style docstring in source |
| empty API reference page | replace static page with `mkdocstrings` module page |
| missing nav target | update `mkdocs.yml` |
