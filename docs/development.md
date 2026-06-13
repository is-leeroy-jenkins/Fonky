# Development

This page defines the development standards for Fonky source files, documentation comments,
exception logging, validation, MkDocs integration, and GitHub Pages deployment.

Fonky development has two linked requirements:

1. Python source files must remain executable, importable, and behavior-preserving.
2. Python docstrings must be valid Google-style documentation that renders through MkDocs and
   mkdocstrings without Griffe warnings.

## Development Goals

Fonky development should preserve a stable framework for document loading, data fetching, web
extraction, text processing, AI tool generation, and source-generated documentation.

| Goal                     | Description                                                                                                                                              |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Runtime stability        | Source files should compile, import, and preserve existing behavior.                                                                                     |
| Documentation quality    | Module, class, function, and method docstrings should render correctly in MkDocs.                                                                        |
| Logging consistency      | Handled exceptions should use the explicit `Error` and `Logger` pattern.                                                                                 |
| API reference generation | `docs/api/*.md` pages should render source docstrings through mkdocstrings.                                                                              |
| User-facing clarity      | Manual documentation should explain setup, configuration, usage, logging, and deployment.                                                                |
| Minimal surprise         | Regenerated files should preserve names, signatures, imports, return contracts, and fallback behavior unless a functional change is explicitly required. |

## Source Layout

Fonky currently uses a flat source-module layout at the repository root.

```text
Fonky/
|-- __init__.py
|-- archives.py
|-- astronomical.py
|-- boogr.py
|-- cloud.py
|-- config.py
|-- core.py
|-- demographic.py
|-- documents.py
|-- environmental.py
|-- fetchers.py
|-- geospatial.py
|-- health.py
|-- loaders.py
|-- models.py
|-- processors.py
|-- scrapers.py
+-- web.py
```

For this layout, imports should use root-level module names:

```python
from loaders import TextLoader
from models import ToolDef
from processors import TextParser
```

Do not use package imports such as this unless the project is later moved into a real package
directory named `fonky`:

```python
from fonky.loaders import TextLoader
```

## Documentation Layout

Expected documentation files:

```text
docs/
|-- index.md
|-- getting-started.md
|-- configuration.md
|-- architecture.md
|-- logging.md
|-- usage.md
|-- user-guide.md
|-- development.md
|-- github-pages.md
|-- api/
|   |-- index.md
|   |-- archives.md
|   |-- astronomical.md
|   |-- boogr.md
|   |-- cloud.md
|   |-- config.md
|   |-- core.md
|   |-- demographic.md
|   |-- documents.md
|   |-- environmental.md
|   |-- fetchers.md
|   |-- geospatial.md
|   |-- health.md
|   |-- loaders.md
|   |-- models.md
|   |-- processors.md
|   |-- scrapers.md
|   +-- web.md
|-- stylesheets/
|   +-- extra.css
+-- javascripts/
    +-- extra.js
```

Manual pages explain the project. API pages render source docstrings.

## Source Regeneration Rules

When regenerating a Python source file, treat the current source file as authoritative.

Preserve:

| Item              | Requirement                                                                                                            |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Imports           | Preserve required imports and add only necessary imports.                                                              |
| Class names       | Do not rename classes.                                                                                                 |
| Function names    | Do not rename functions or methods.                                                                                    |
| Signatures        | Preserve parameters, defaults, annotations, and return annotations unless correcting a documentation or typing defect. |
| Return contracts  | Preserve existing return behavior.                                                                                     |
| Fallback behavior | Preserve existing fallback messages, empty values, and error envelopes.                                                |
| Public API        | Preserve callable public methods.                                                                                      |
| State fields      | Preserve existing instance attributes and class attributes.                                                            |
| Provider calls    | Preserve external API call structure unless explicitly corrected.                                                      |
| Logging pattern   | Use the explicit project pattern in each handled exception block.                                                      |

Avoid:

```text
- Shortened reconstructions
- Helper abstractions that replace required logging blocks
- Partial files unless explicitly requested
- Reordered logic that changes behavior
- Missing methods listed in __dir__
- Missing methods called through self.method_name(...)
- Unsupported claims in docs or comments
```

## Google-Style Docstring Standard

Fonky source comments should use Google-style docstrings that render cleanly with mkdocstrings and
Griffe.

Preferred sections:

```text
Purpose:
Args:
Attributes:
Returns:
Raises:
Notes:
Examples:
```

Use `Args:` for parameters.

Do not use:

```text
Parameters:
----------
Returns:
    None: ...
Returns:
    Any: ...
Returns:
    Description without a type.
Args:
    Request parameters.
Attributes:
    Request parameters.
```

## Required Purpose Section

Every module, class, method, and function docstring should include a meaningful `Purpose:` section
unless the object is extremely small and self-evident.

Good:

```python
def normalize_text(self, text: str) -> str:
    """Normalize text for downstream processing.

    Purpose:
        Converts text into a consistent representation by trimming whitespace,
        normalizing case, and collapsing repeated spacing before tokenization
        or vectorization.

    Args:
        text (str): Text value to normalize.

    Returns:
        str: Normalized text.
    """
```

Bad:

```python
def normalize_text(self, text: str) -> str:
    """Normalize text."""
```

## Args Format

Each argument must use a valid `name (type): description` pair.

Good:

```text
Args:
    path (str): Path to the file that should be loaded.
    encoding (Optional[str]): Optional file encoding.
```

Bad:

```text
Args:
    Request parameters.
```

Bad:

```text
Args:
    path: Path to the file.
```

Bad:

```text
Args:
    path (str):
```

## Returns Format

Return sections must include a type and a description.

Good:

```text
Returns:
    list[str]: Supported option values.
```

Good:

```text
Returns:
    List[Document]: Loaded document objects.
```

Bad:

```text
Returns:
    Supported option values.
```

Bad:

```text
Returns:
    None: This method does not return a value.
```

Bad:

```text
Returns:
    Any: Result value.
```

For no-return procedures, omit the `Returns:` section entirely.

## Attributes Format

Class attributes must use valid `name (type): description` pairs.

Good:

```text
Attributes:
    documents (Optional[List[Document]]): Documents loaded or split by the wrapper.
    file_path (Optional[str]): Active local file path.
    loader (Optional[BaseLoader]): Underlying loader instance.
```

Bad:

```text
Attributes:
    Request parameters.
```

Bad:

```text
Attributes:
    Configuration used by the active request.
```

If a class has no useful public attributes to document, omit `Attributes:`.

## Init Docstring Rules

Do not include `Returns:` in `__init__`.

Good:

```python
def __init__(self) -> None:
    """Initialize the loader.

    Purpose:
        Initializes local state used by the loader. No external files or
        network resources are loaded during construction.
    """
```

Bad:

```python
def __init__(self) -> None:
    """Initialize the loader.

    Returns:
        None: No value is returned.
    """
```

## Exception Logging Standard

Handled exceptions must use the explicit Fonky logging pattern.

Required pattern:

```python
except Exception as e:
    exception = Error(e)
    exception.module = "module_name"
    exception.cause = "ClassName"
    exception.method = "method_name(self, arg: type) -> return_type"
    Logger().write(exception)
    raise exception
```

For this project, do not replace the pattern with a helper such as:

```python
_log_and_raise(e, "ClassName", "method_name(...)")
```

The logging block must remain visible inside each handled exception block.

## Logging Fields

Each wrapped exception should set the following fields:

| Field                       | Meaning                                                          |
| --------------------------- | ---------------------------------------------------------------- |
| `exception.module`          | Source module name such as `loaders`, `fetchers`, or `scrapers`. |
| `exception.cause`           | Class or operation name where the failure occurred.              |
| `exception.method`          | Stable method signature string.                                  |
| `Logger().write(exception)` | Persists the exception record to SQLite.                         |

Example:

```python
except Exception as e:
    exception = Error(e)
    exception.module = "loaders"
    exception.cause = "TextLoader"
    exception.method = "load(self, path: str, encoding: Optional[str]=None) -> List[Document]"
    Logger().write(exception)
    raise exception
```

## Sensitive Data Rule

Do not place live argument values into `exception.method`.

Good:

```python
exception.method = "load(self, path: str, encoding: Optional[str]=None) -> List[Document]"
```

Bad:

```python
exception.method = f"load(self, path={path}, encoding={encoding})"
```

Do not log:

```text
- API keys
- Access tokens
- Passwords
- Full local paths containing private user folders
- Full document text
- OCR text
- Full request payloads
- Full provider responses
```

## Python Validation

Run syntax validation after source changes.

Compile the full project:

```powershell
python -m compileall .
```

Compile targeted files:

```powershell
python -m py_compile .\boogr.py
python -m py_compile .\config.py
python -m py_compile .\core.py
python -m py_compile .\archives.py
python -m py_compile .\fetchers.py
python -m py_compile .\loaders.py
python -m py_compile .\models.py
python -m py_compile .\processors.py
python -m py_compile .\scrapers.py
```

A successful compile check confirms syntax validity. It does not guarantee every optional provider
dependency or credential is available.

## Import Validation

Run basic import checks from the repository root:

```powershell
python -c "import config; import boogr; import core; import loaders; import models; print('imports passed')"
```

If imports fail, resolve the source error or missing dependency before building the documentation.

## MkDocs Validation

MkDocs requires:

| Requirement             | File or package                       |
| ----------------------- | ------------------------------------- |
| Configuration file      | `mkdocs.yml`                          |
| Documentation directory | `docs/`                               |
| Manual pages            | `docs/*.md`                           |
| API reference pages     | `docs/api/*.md`                       |
| MkDocs package          | `mkdocs`                              |
| Material theme          | `mkdocs-material`                     |
| Python API renderer     | `mkdocstrings`, `mkdocstrings-python` |
| Markdown extensions     | `pymdown-extensions`                  |

Install documentation dependencies:

```powershell
python -m pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python pymdown-extensions
```

Build the documentation:

```powershell
mkdocs build
```

Serve locally:

```powershell
mkdocs serve
```

Open:

```text
http://127.0.0.1:8000/
```

## API Page Requirements

Each API page must contain a live mkdocstrings directive.

Correct for this flat source layout:

```text
# Loaders API

::: loaders
```

Incorrect for this project:

```text
# Loaders API

::: fonky.loaders
```

The project currently does not have an importable `fonky` package folder.

## API Reference Pages

Expected API pages:

```text
docs/api/index.md
docs/api/archives.md
docs/api/astronomical.md
docs/api/boogr.md
docs/api/cloud.md
docs/api/config.md
docs/api/core.md
docs/api/demographic.md
docs/api/documents.md
docs/api/environmental.md
docs/api/fetchers.md
docs/api/geospatial.md
docs/api/health.md
docs/api/loaders.md
docs/api/models.md
docs/api/processors.md
docs/api/scrapers.md
docs/api/web.md
```

For the flat source layout, the API pages should use:

```text
::: archives
::: astronomical
::: boogr
::: cloud
::: config
::: core
::: demographic
::: documents
::: environmental
::: fetchers
::: geospatial
::: health
::: loaders
::: models
::: processors
::: scrapers
::: web
```

## Manual Page Rule

Manual pages must not contain live mkdocstrings directives.

Correct manual page behavior:

```text
Manual documentation describes `::: loaders` inside prose or code blocks.
```

Incorrect manual page behavior:

```text
A top-level page contains a live line starting with ::: loaders.
```

Only `docs/api/*.md` should contain live directives.

## Directive Validation

Confirm API pages contain live directives:

```powershell
Select-String -Path .\docs\api\*.md -Pattern "^:::\s+[A-Za-z_]"
```

Expected output includes entries such as:

```text
docs\api\loaders.md:3:::: loaders
docs\api\fetchers.md:3:::: fetchers
docs\api\models.md:3:::: models
```

Confirm manual pages do not contain live directives:

```powershell
Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"
```

Expected output:

```text
No output.
```

## MkDocs Configuration Requirements

The `mkdocs.yml` plugin block must include mkdocstrings:

```yaml
plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths:
            - .
          options:
            docstring_style: google
            show_source: true
            show_root_heading: true
            show_root_full_path: false
            show_signature: true
            show_signature_annotations: true
            separate_signature: true
            merge_init_into_class: false
            members_order: source
            filters:
              - "!^_"
            heading_level: 2
```

Do not include this unless an actual override directory exists:

```yaml
custom_dir: null
```

Correct:

```yaml
theme:
  name: material
  language: en
```

## Common Griffe Warnings

### No type or annotation for returned value

Cause:

```text
Returns:
    Supported values.
```

Fix:

```text
Returns:
    list[str]: Supported values.
```

### Failed to get name: description pair

Cause:

```text
Args:
    Request parameters.
```

or:

```text
Attributes:
    Request parameters for the active call.
```

Fix:

```text
Args:
    params (dict[str, object]): Request parameters for the active call.
```

or omit the section when there is no specific argument or attribute.

### Returns None

Cause:

```text
Returns:
    None: No value is returned.
```

Fix:

```text
Omit the Returns section for procedures that do not return a value.
```

## Common MkDocs Warnings

### API page is blank

Confirm the page contains a directive:

```text
::: loaders
```

### mkdocstrings cannot import module

Confirm:

```text
- The directive matches the flat source layout.
- The command is run from the repository root.
- A dependency required at import time is installed.
- The source file has no syntax errors.
```

### Duplicate API targets

Cause:

```text
Manual pages contain live mkdocstrings directives.
```

Fix:

```text
Remove live ::: module directives from docs/*.md.
Keep them only in docs/api/*.md.
```

### Autorefs cannot find target 0 or :1000

Avoid Python bracket indexing and slicing in Markdown examples.

Bad:

```python
print(documents[0].page_content[:1000])
```

Good:

```python
for document in documents:
    print(document.page_content)
    break
```

## Pre-Build Checklist

Before running `mkdocs build`, run:

```powershell
python -m compileall .
```

Then check API directives:

```powershell
Select-String -Path .\docs\api\*.md -Pattern "^:::\s+[A-Za-z_]"
```

Then check manual pages:

```powershell
Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"
```

The manual page check should return no output.

Then build:

```powershell
mkdocs build
```

## Release Checklist

Before pushing documentation changes:

| Check                              | Command                                                           |
| ---------------------------------- | ----------------------------------------------------------------- |
| Source compiles                    | `python -m compileall .`                                          |
| API pages contain directives       | `Select-String -Path .\docs\api\*.md -Pattern "^:::\s+[A-Za-z_]"` |
| Manual pages contain no directives | `Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"`     |
| Docs build                         | `mkdocs build`                                                    |
| Docs serve locally                 | `mkdocs serve`                                                    |
| Git status reviewed                | `git status`                                                      |
| Changes committed                  | `git add .; git commit -m "Update Fonky documentation"`           |
| GitHub Pages deployed              | `mkdocs gh-deploy --force`                                        |

## Safe Development Workflow

Recommended workflow for source changes:

```text
1. Edit one source file.
2. Preserve signatures and behavior.
3. Update Google-style docstrings.
4. Preserve explicit exception logging.
5. Run python -m py_compile on the edited file.
6. Run python -m compileall .
7. Run mkdocs build.
8. Fix Griffe or import warnings.
9. Review rendered API page.
10. Commit only after source and docs build cleanly.
```

Recommended workflow for documentation changes:

```text
1. Edit one Markdown page.
2. Use ASCII-only Markdown.
3. Avoid emoji headers.
4. Avoid Unicode tree characters.
5. Avoid code fence attributes.
6. Avoid live mkdocstrings directives outside docs/api.
7. Confirm all links point to existing files.
8. Run mkdocs build.
9. Run mkdocs serve.
10. Review the rendered page.
```

## Development Baseline

A healthy development baseline is:

```text
- Python source compiles.
- Core modules import from the repository root.
- boogr.Logger writes to the configured SQLite database.
- API pages contain mkdocstrings directives.
- Manual pages contain no live mkdocstrings directives.
- MkDocs builds without Griffe warnings.
- User-facing docs explain setup, configuration, architecture, logging, usage, and deployment.
- GitHub Pages deploys only after the local site builds cleanly.
```

