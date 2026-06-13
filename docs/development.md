# ðŸ› ï¸ Development

This page defines the development standards for Fonky source files, documentation comments,
exception logging, validation, MkDocs integration, and release workflow.

Fonky relies on two linked development practices:

1. Python source files must remain executable, importable, and behavior-preserving.
2. Python docstrings must be valid Google-style documentation that can be rendered by MkDocs and
   mkdocstrings without Griffe warnings.



## ðŸŽ¯ Development Goals

Fonky development should preserve a stable framework for:

| Goal                     | Description                                                                                                                                              |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Runtime stability        | Source files should compile, import, and preserve existing behavior.                                                                                     |
| Documentation quality    | Module, class, function, and method docstrings should render correctly in MkDocs.                                                                        |
| Logging consistency      | Handled exceptions should use the explicit `Error` and `Logger` pattern.                                                                                 |
| API reference generation | `docs/api/*.md` pages should render source docstrings through mkdocstrings.                                                                              |
| User-facing clarity      | Top-level documentation should explain setup, configuration, usage, logging, and deployment.                                                             |
| Minimal surprise         | Regenerated files should preserve names, signatures, imports, return contracts, and fallback behavior unless a functional change is explicitly required. |



## ðŸ“ Source Layout

Fonky currently uses a flat source-module layout at the repository root.

Expected source files:

```text id="source_layout"
Fonky/
â”œâ”€â”€ __init__.py
â”œâ”€â”€ archives.py
â”œâ”€â”€ astronomical.py
â”œâ”€â”€ boogr.py
â”œâ”€â”€ cloud.py
â”œâ”€â”€ config.py
â”œâ”€â”€ core.py
â”œâ”€â”€ demographic.py
â”œâ”€â”€ documents.py
â”œâ”€â”€ environmental.py
â”œâ”€â”€ fetchers.py
â”œâ”€â”€ geospatial.py
â”œâ”€â”€ health.py
â”œâ”€â”€ loaders.py
â”œâ”€â”€ models.py
â”œâ”€â”€ processors.py
â”œâ”€â”€ scrapers.py
â””â”€â”€ web.py
```

If the project is later moved into a package folder named `fonky`, update imports and mkdocstrings
directives accordingly.

Flat layout directive:

```markdown id="flat_layout_directive"
`::: loaders`
```

Package layout directive:

```markdown id="package_layout_directive"
`::: loaders`
```



## ðŸ“š Documentation Layout

Expected documentation files:

```text id="docs_layout"
docs/
â”œâ”€â”€ index.md
â”œâ”€â”€ getting-started.md
â”œâ”€â”€ configuration.md
â”œâ”€â”€ architecture.md
â”œâ”€â”€ logging.md
â”œâ”€â”€ usage.md
â”œâ”€â”€ user-guide.md
â”œâ”€â”€ development.md
â”œâ”€â”€ github-pages.md
â”œâ”€â”€ api/
â”‚   â”œâ”€â”€ index.md
â”‚   â”œâ”€â”€ archives.md
â”‚   â”œâ”€â”€ astronomical.md
â”‚   â”œâ”€â”€ boogr.md
â”‚   â”œâ”€â”€ cloud.md
â”‚   â”œâ”€â”€ config.md
â”‚   â”œâ”€â”€ core.md
â”‚   â”œâ”€â”€ demographic.md
â”‚   â”œâ”€â”€ documents.md
â”‚   â”œâ”€â”€ environmental.md
â”‚   â”œâ”€â”€ fetchers.md
â”‚   â”œâ”€â”€ geospatial.md
â”‚   â”œâ”€â”€ health.md
â”‚   â”œâ”€â”€ loaders.md
â”‚   â”œâ”€â”€ models.md
â”‚   â”œâ”€â”€ processors.md
â”‚   â”œâ”€â”€ scrapers.md
â”‚   â””â”€â”€ web.md
â””â”€â”€ stylesheets/
    â””â”€â”€ extra.css
```

Top-level documentation pages explain the project. API pages render docstrings from Python source
files.



## ðŸ§¾ Source Regeneration Rules

When regenerating a Python source file, preserve the uploaded or current source file as
authoritative.

Do not change behavior unless a functional change is explicitly requested.

Preserve:

| Item              | Requirement                                                                                                      |
|-------------------|------------------------------------------------------------------------------------------------------------------|
| Imports           | Preserve required imports and add only necessary imports.                                                        |
| Class names       | Do not rename classes.                                                                                           |
| Function names    | Do not rename functions or methods.                                                                              |
| Signatures        | Preserve parameters, defaults, annotations, and return annotations unless correcting a documentation/type issue. |
| Return contracts  | Preserve existing return behavior.                                                                               |
| Fallback behavior | Preserve existing fallback messages, empty values, and error envelopes.                                          |
| Public API        | Preserve callable public methods.                                                                                |
| State fields      | Preserve existing instance attributes and class attributes.                                                      |
| Provider calls    | Preserve external API call structure unless explicitly corrected.                                                |
| Logging pattern   | Use the explicit project pattern in each handled exception block.                                                |

Avoid:

```text id="avoid_regeneration"
- Shortened reconstructions
- Helper abstractions that replace required logging blocks
- Partial files unless explicitly requested
- Reordered logic that changes behavior
- Missing methods listed in __dir__
- Missing methods called through self.method_name(...)
- Unsupported claims in docs or comments
```



## ðŸ§  Google-Style Docstring Standard

Fonky source comments should use Google-style docstrings that render cleanly with mkdocstrings and
Griffe.

Preferred sections:

```text id="docstring_sections"
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

```text id="bad_docstring_sections"
Parameters:
-
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



## âœ… Required `Purpose:` Section

Every module, class, method, and function docstring should include a meaningful `Purpose:` section
unless the function is extremely small and already self-evident.

Good:

```python id="purpose_good"
def normalize_text(self, text: str) -> str:
	"""Normalize text for downstream processing.

	Purpose:
		Converts text into a consistent representation by trimming whitespace, normalizing
		case, and collapsing repeated spacing before tokenization or vectorization.

	Args:
		text (str): Text value to normalize.

	Returns:
		str: Normalized text.
	"""
```

Bad:

```python id="purpose_bad"
def normalize_text(self, text: str) -> str:
	"""Normalize text."""
```



## ðŸ§© `Args:` Format

Each argument must use a valid `name (type): description` pair.

Good:

```python id="args_good"
Args:
	path (str): Path to the file that should be loaded.
	encoding (Optional[str]): Optional file encoding.
```

Bad:

```python id="args_bad"
Args:
	Request parameters.
```

Bad:

```python id="args_bad_untyped"
Args:
	path: Path to the file.
```

Bad:

```python id="args_bad_missing_description"
Args:
	path (str):
```



## ðŸ“¤ `Returns:` Format

Return sections must include a type and a description.

Good:

```python id="returns_good"
Returns:
	list[str]: Supported option values.
```

Good:

```python id="returns_good_document"
Returns:
	List[Document]: Loaded LangChain document objects.
```

Bad:

```python id="returns_bad_untyped"
Returns:
	Supported option values.
```

Bad:

```python id="returns_bad_none"
Returns:
	None: This method does not return a value.
```

Bad:

```python id="returns_bad_any"
Returns:
	Any: Result value.
```

For no-return procedures, omit the `Returns:` section entirely.



## ðŸ§± `Attributes:` Format

Class attributes must also use valid `name (type): description` pairs.

Good:

```python id="attributes_good"
Attributes:
	documents (Optional[List[Document]]): Documents loaded or split by the wrapper.
	file_path (Optional[str]): Active local file path.
	loader (Optional[BaseLoader]): Underlying LangChain loader instance.
```

Bad:

```python id="attributes_bad"
Attributes:
	Request parameters.
```

Bad:

```python id="attributes_bad_description_only"
Attributes:
	Configuration used by the active request.
```

If a class has no useful public attributes to document, omit `Attributes:`.



## ðŸš« `__init__` Docstring Rules

Do not include `Returns:` in `__init__`.

Good:

```python id="init_good"
def __init__(self) -> None:
	"""Initialize the loader.

	Purpose:
		Initializes local state used by the loader. No external files or network resources
		are loaded during construction.
	"""
```

Bad:

```python id="init_bad"
def __init__(self) -> None:
	"""Initialize the loader.

	Returns:
		None: No value is returned.
	"""
```



## ðŸªµ Exception Logging Standard

Handled exceptions must use the explicit Fonky logging pattern.

Required pattern:

```python id="required_logging_pattern"
except Exception as e:
	exception = Error(e)
	exception.module = "module_name"
	exception.cause = "ClassName"
	exception.method = "method_name(self, arg: type) -> return_type"
	Logger().write(exception)
	raise exception
```

For this project, do not replace the pattern with a helper such as:

```python id="bad_logging_helper"
_log_and_raise(e, "ClassName", "method_name(...)")
```

The logging block must remain visible inside each handled exception block.



## ðŸ“Œ Logging Fields

Each wrapped exception should set the following fields:

| Field                       | Meaning                                                          |
|  | - |
| `exception.module`          | Source module name such as `loaders`, `fetchers`, or `scrapers`. |
| `exception.cause`           | Class or operation name where the failure occurred.              |
| `exception.method`          | Stable method signature string.                                  |
| `Logger().write(exception)` | Persists the exception record to SQLite.                         |

Example:

```python id="logging_example"
except Exception as e:
	exception = Error(e)
	exception.module = "loaders"
	exception.cause = "TextLoader"
	exception.method = "load(self, path: str, encoding: Optional[str]=None) -> List[Document]"
	Logger().write(exception)
	raise exception
```



## ðŸ§ª Python Validation

Run syntax validation after source changes.

Compile the full project:

```powershell id="compileall_project"
python -m compileall .
```

Compile targeted files:

```powershell id="py_compile_targeted"
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

A successful compile check confirms syntax validity. It does not guarantee all optional provider
dependencies or credentials are available.



## ðŸ”Ž Import Validation

Run basic import checks from the repository root:

```powershell id="import_validation_flat"
python -c "import config; import boogr; import core; import loaders; import models; print('imports passed')"
```

If source files are later moved under `fonky/`, use:

```powershell id="import_validation_package"
python -c "import fonky.config; import fonky.boogr; import fonky.core; import fonky.loaders; import fonky.models; print('package imports passed')"
```



## ðŸ“š MkDocs Validation

MkDocs requires:

| Requirement             | File or Package                       |
| -- | - |
| Configuration file      | `mkdocs.yml`                          |
| Documentation directory | `docs/`                               |
| Markdown pages          | `docs/*.md`                           |
| API reference pages     | `docs/api/*.md`                       |
| MkDocs package          | `mkdocs`                              |
| Material theme          | `mkdocs-material`                     |
| Python API renderer     | `mkdocstrings`, `mkdocstrings-python` |
| Markdown extensions     | `pymdown-extensions`                  |

Install documentation dependencies:

```powershell id="install_mkdocs_deps"
python -m pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python pymdown-extensions
```

Build the documentation:

```powershell id="mkdocs_build"
mkdocs build
```

Serve locally:

```powershell id="mkdocs_serve"
mkdocs serve
```

Open:

```text id="local_mkdocs_url"
http://127.0.0.1:8000/
```



## ðŸ”Œ API Page Requirements

Each API page must contain a mkdocstrings directive.

Flat source layout:

```markdown id="api_directive_flat"
# Loaders API

`::: loaders`
```

Package source layout:

```markdown id="api_directive_package"
# Loaders API

`::: loaders`
```

If a page contains only normal Markdown prose, the source comments will not render.

Check a page:

```powershell id="check_api_page"
Get-Content .\docs\api\loaders.md
```

The page should contain a line beginning with:

```text id="directive_marker"
```


