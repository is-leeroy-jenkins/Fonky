# User Guide

## Choose the Surface

| Surface              | Use When                                                                |
|----------------------|-------------------------------------------------------------------------|
| `fonky.py`           | direct invocation of a specific public operation                        |
| `tools.py`           | tool discovery or agent-scoped selection                                |
| implementation class | debugging, low-level behavior, or repeated operations with shared state |

## Quick Recipes

- archives and public research → `guides/archives.md`
- astronomy and flight → `guides/astronomical.md`
- cloud and remote storage → `guides/cloud.md`
- file ingestion and document loading → `guides/documents.md`
- environmental and geospatial → `guides/environmental.md`, `guides/geospatial.md`
- health and demographic data → `guides/health.md`, `guides/demographic.md`
- HTML extraction and recursive loading → `guides/web.md`

## Working Rule

Use the smallest surface that solves the task. Use domain sets for agents, single tools for deterministic workflows, and implementation classes for source-level control.
