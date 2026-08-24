# Configuration

## Configuration Sources

Fonky reads runtime settings from `config.py`, explicit function parameters, provider libraries, and environment variables.

## Configuration Layers

| Layer | Scope | Examples |
|---|---|---|
| Function arguments | per invocation | query strings, limits, file paths, booleans |
| Provider credentials | external services | API keys, tokens, account identifiers |
| Loader/runtime options | ingestion behavior | OCR mode, recursive depth, parsing flags |
| Global environment | cross-module defaults | timeout, base paths, provider keys |

## Common Environment Variables

| Category | Examples |
|---|---|
| Search / research | `GOOGLE_API_KEY`, `CONGRESS_API_KEY`, `DATAGOV_API_KEY` |
| Environmental / weather | `OPENWEATHER_API_KEY`, `AIRNOW_API_KEY`, `PURPLEAIR_API_KEY` |
| Geospatial | `GOOGLE_MAPS_API_KEY`, `GEOCODING_API_KEY`, `GEOAPIFY_API_KEY` |
| Cloud / storage | `AWS_*`, `AZURE_*`, Google Drive / Google Cloud credentials |
| LangChain / model integrations | model-provider credentials required by downstream workflows |

## Configuration Practices

- Keep provider credentials out of source control.
- Prefer environment-backed secrets over hard-coded values.
- Bind function-level overrides only where local behavior must differ.
- Treat parser, OCR, and recursive crawl options as workload-specific, not global defaults.

## Build-Time Checks

- importability of `config.py`
- presence of required provider libraries
- presence of required credentials for provider-backed tools
- filesystem accessibility for local loaders
