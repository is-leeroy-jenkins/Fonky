# Boogr Integration

Fonky's implementation modules currently import error and logging support from the external `boogr`
package. This page documents that boundary so operators know why imports may fail before provider
calls run.

## Where Boogr Appears

| Module | Imported symbols |
| --- | --- |
| `fetchers.py` | `Error` |
| `loaders.py` | `Error`, `Logger` |
| `models.py` | `Error` |
| `processors.py` | `Error` |
| `scrapers.py` | `Error`, `Logger` |

## Operational Meaning

If `boogr` is unavailable, importing some implementation modules may fail before any wrapper call is
executed. That is a dependency/environment issue, not a `fonky.py` routing issue.

## Handling Strategy

- install or expose the expected `boogr` package/module;
- do not replace the error boundary in `fonky.py`;
- keep wrapper functions thin;
- handle exceptions at application boundaries.
