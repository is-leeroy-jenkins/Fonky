# Adding a Loader

## Checklist

- implement loader behavior in `loaders.py`,
- keep output normalization explicit,
- preserve source metadata,
- document dependency prerequisites,
- add a public export if the loader is intended for external use,
- test at least one real sample and one failure path.

## Loader-Specific Concerns

- file type detection,
- parser selection,
- metadata propagation,
- cloud/provider authentication,
- encoding and malformed-content handling.
