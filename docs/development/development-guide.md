# Development Guide

This page defines the maintenance workflow for Fonky's current architecture. The goal is to add
capabilities without turning the functional layer into a second implementation.

## Development Rule

Provider, loader, scraper, validation, request, parsing, and result-shaping logic belongs in the
implementation modules. `fonky.py` contains thin call surfaces only.

## Add a New Fetcher Capability

| Step | Action |
| --- | --- |
| 1 | Add or update a class/method in `fetchers.py`. |
| 2 | Keep API key handling, endpoint construction, parameter validation, request execution, and payload shaping inside the class. |
| 3 | Add a wrapper in `fonky.py` if the capability should be exposed in the flat interface. |
| 4 | Route the wrapper to exactly one target implementation method. |

## Add a New Loader Capability

| Step | Action |
| --- | --- |
| 1 | Add or update a class/method in `loaders.py`. |
| 2 | Keep file/path/cloud-loader setup and parsing logic in the loader. |
| 3 | Expose stateless or self-contained operations as wrappers. |
| 4 | Use direct class workflows for multi-step stateful loader operations. |

## Add a New Scraper Capability

| Step | Action |
| --- | --- |
| 1 | Add or update extraction behavior in `scrapers.py`. |
| 2 | Keep HTTP retrieval and BeautifulSoup extraction logic in `WebExtractor`. |
| 3 | Expose the extraction as a wrapper only when it is a useful independent operation. |

## Wrapper Requirements

A wrapper should:

- use explicit typed parameters;
- instantiate the target implementation locally;
- pass arguments by name;
- avoid recreating provider logic;
- return the implementation result directly;
- include a docstring that explains the operational purpose, arguments, and return value;
- be added to `__all__`.

## Test Expectations

| Category | Expectation |
| --- | --- |
| Syntax | All changed Python files compile. |
| Routing | Every wrapper resolves to an existing class and method. |
| Arguments | Every wrapper forwards valid keyword names for the target method. |
| Smoke | At least one local loader and one scraper path execute in a dependency-controlled environment. |
| Provider | External provider tests are credential-gated and may be skipped without secrets. |
| Documentation | MkDocs navigation, local links, images, and function references validate. |

## Documentation Expectations

Documentation changes must explain behavior, not merely list symbols. When adding a wrapper, update:

1. `api/fonky.md`;
2. the relevant implementation API page;
3. usage examples if the capability is user-facing;
4. configuration if the provider requires credentials;
5. troubleshooting if the provider introduces unique failure modes;
6. diagrams when counts or relationships change.


## Source-to-Documentation Contract

The documentation is expected to remain synchronized with the source. When the source changes,
rebuild the documentation inventory rather than editing counts by hand.

| Documentation element | Source of truth |
| --- | --- |
| Wrapper count | Derived from `fonky.py` function definitions grouped by domain comments. |
| Class count | Derived from class definitions in implementation modules. |
| Method tables | Derived from public methods on each class. |
| Configuration inventory | Derived from `os.getenv(...)` assignments in `config.py`. |
| Diagrams | Generated from the same counts and architectural relationships. |

## Review Checklist

Before accepting a documentation regeneration, verify:

| Area | Acceptance criterion |
| --- | --- |
| Navigation | Every `mkdocs.yml` target exists. |
| Links | Every local Markdown link resolves. |
| Images | Every image referenced by Markdown exists. |
| Wrapper examples | Every `fonky.<function>()` reference exists in `fonky.py`. |
| API coverage | Every wrapper is represented in `api/fonky.md`. |
| Architecture | Diagrams explain execution, dependency, lifecycle, failure, or extension relationships—not repository decoration. |
| Depth | Pages explain behavior, choices, constraints, and operations, not just symbol names. |
