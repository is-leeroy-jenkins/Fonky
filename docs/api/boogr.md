# Boogr Integration

Fonky currently imports error/logging support from the external `boogr` package.

## Source Usage

```text
fetchers.py   → Error
loaders.py    → Error, Logger
models.py     → Error
processors.py → Error
scrapers.py   → Error, Logger
```

Because `boogr` is external, its internal API is not documented here beyond what Fonky's source demonstrates. If the package is missing, importing affected modules can fail before a provider or loader is called. The `fonky.py` wrapper layer does not replace or alter this dependency.
