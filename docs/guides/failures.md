# Failure Handling

## Failure Taxonomy

| Class | Typical Trigger | Surface |
|---|---|---|
| missing source | bad path, missing URL, 404 | loaders / fetchers / scrapers |
| auth failure | absent or invalid credentials | provider-backed fetchers/loaders |
| parse failure | malformed or unsupported content | loaders / scrapers |
| dependency failure | missing package, driver, or binary | loaders / rendering paths |
| schema failure | unexpected provider shape | fetchers / models |
| documentation failure | invalid docstring or import path | `fonky.py`, API docs |

## Response Pattern

1. isolate the failing surface,
2. reduce to the smallest reproducible invocation,
3. verify dependency and credential prerequisites,
4. test the underlying implementation class,
5. restore documentation or schema parity if the failure is tooling-related.

## Documentation-Specific Failures

- `mkdocstrings` import path wrong,
- navigation references missing pages,
- source page replaced by static tables,
- tool docstring cannot be parsed into schema.
