# Development Guide

## Contribution Sequence

1. implement behavior in the owning module,
2. add or update the public export,
3. verify docstring compliance,
4. update tool grouping if the public export is agent-facing,
5. add or update tests,
6. rebuild documentation.

## Standards

- no duplicate public wrapper layers,
- no undocumented public parameters,
- no generic boilerplate API descriptions,
- no static method/signature tables in place of source-driven API docs,
- no navigation drift between files on disk and `mkdocs.yml`.
