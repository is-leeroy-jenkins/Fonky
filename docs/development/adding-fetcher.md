# Adding a Fetcher

## Checklist

- add the implementation class in `fetchers.py`,
- keep provider behavior localized,
- document purpose, parameters, returns, and failures,
- add a public export in `fonky.py` only if the behavior is part of the supported public surface,
- add the export to `tools.py` only if it belongs in a domain set,
- test provider failure and happy-path behavior.

## Minimum Documentation

- provider or source,
- expected input parameters,
- output shape,
- required credentials,
- typical exceptions.
