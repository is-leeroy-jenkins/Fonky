# 🪵 Logging

Fonky uses a project-specific exception wrapper and SQLite-backed logger to preserve useful failure
details during loader, fetcher, scraper, processor, and model execution.

The logging system is implemented in:

```text id="logging_source_files"
boogr.py
config.py
```

The logging database is configured through:

```text id="logging_config_values"
LOG_DIR
LOG_PATH
LOG_FILE
```



## 🎯 Logging Purpose

Fonky interacts with local files, APIs, websites, cloud storage, document parsers, browser tooling,
and AI tool wrappers. Those operations can fail for many reasons:

```text id="logging_failure_sources"
- Missing local files
- Invalid paths
- Missing API keys
- Expired credentials
- Network failures
- Provider rate limits
- Invalid response payloads
- Document parsing failures
- Browser rendering failures
- Dependency import failures
- Tool execution failures
```

The logging layer gives handled exceptions a consistent structure before they are raised again.

The purpose is not to hide failures. The purpose is to make failures traceable.



## 🧱 Logging Architecture

The logging flow is:

```text id="logging_flow"
Handled exception
    ↓
boogr.Error
    ↓
module, cause, method, message, info, trace
    ↓
boogr.Logger
    ↓
SQLite database
    ↓
Exception re-raised to caller
```

The source modules keep the logging block visible inside each `except` block.

Required pattern:

```python id="required_logging_pattern"
except Exception as e:
	exception = Error(e)
	exception.module = "loaders"
	exception.cause = "TextLoader"
	exception.method = "load(self, path: str, encoding: Optional[str]=None) -> List[Document]"
	Logger().write(exception)
	raise exception
```



## 📦 Logging Components

| Component  | Source      | Responsibility                                                     |
| ---------- | ----------- | ------------------------------------------------------------------ |
| `Error`    | `boogr.py`  | Wraps the original exception and stores normalized metadata.       |
| `Logger`   | `boogr.py`  | Creates the SQLite table when needed and writes exception records. |
| `LOG_DIR`  | `config.py` | Directory used for logging artifacts.                              |
| `LOG_PATH` | `config.py` | Full SQLite database path.                                         |
| `LOG_FILE` | `config.py` | SQLite table name.                                                 |



## ⚙️ Configuration Values

The logging configuration should exist in `config.py`.

Expected constants:

```python id="logging_constants_expected"
LOG_DIR
LOG_PATH
LOG_FILE
```

Recommended defaults:

```text id="logging_default_values"
LOG_DIR  = logging
LOG_PATH = logging/Exceptions.db
LOG_FILE = Exceptions
```

On Windows, the resolved database path usually becomes:

```text id="windows_logging_database"
C:\Users\terry\source\repos\Fonky\logging\Exceptions.db
```



## 🪟 PowerShell Logging Overrides

Set a custom logging directory:

```powershell id="set_log_dir"
$env:LOG_DIR = "C:\Users\terry\source\repos\Fonky\logging"
```

Set a custom database path:

```powershell id="set_log_path"
$env:LOG_PATH = "C:\Users\terry\source\repos\Fonky\logging\Exceptions.db"
```

Set a custom table name:

```powershell id="set_log_file"
$env:LOG_FILE = "Exceptions"
```

These variables apply to the current PowerShell session.



## 🧾 Error Metadata

`Error` stores metadata that makes an exception easier to diagnose.

| Field     | Meaning                                                                |
| --------- | ---------------------------------------------------------------------- |
| `cause`   | Class, operation, or component where the exception occurred.           |
| `module`  | Source module, such as `loaders`, `fetchers`, `scrapers`, or `models`. |
| `method`  | Stable method signature string or operation name.                      |
| `message` | Exception message.                                                     |
| `info`    | Additional contextual information when available.                      |
| `trace`   | Exception traceback.                                                   |

The most important fields to set manually are:

```python id="manual_error_fields"
exception.module = "module_name"
exception.cause = "ClassName"
exception.method = "method_signature"
```



## 🧱 Required Exception Pattern

Every handled exception block in regenerated Fonky source should use this explicit pattern:

```python id="standard_exception_pattern"
except Exception as e:
	exception = Error(e)
	exception.module = "module_name"
	exception.cause = "ClassName"
	exception.method = "method_name(self, arg: type) -> return_type"
	Logger().write(exception)
	raise exception
```

This pattern has four required behaviors:

| Behavior | Requirement                                     |
| -------- | ----------------------------------------------- |
| Wrap     | Convert the original exception into `Error(e)`. |
| Annotate | Set `module`, `cause`, and `method`.            |
| Persist  | Call `Logger().write(exception)`.               |
| Raise    | Re-raise the wrapped exception.                 |



## 🚫 Logging Pattern to Avoid

Do not hide the logging operation behind a helper function.

Avoid:

```python id="bad_helper_pattern"
except Exception as e:
	_log_and_raise(e, "TextLoader", "load(...)")
```

Avoid:

```python id="bad_logger_helper_pattern"
except Exception as e:
	raise log_exception(e)
```

For Fonky, the required logging operation should remain visible in the handler:

```python id="visible_logger_pattern"
Logger().write(exception)
```

This makes the logging behavior obvious in the source and visible in the API reference.



## 📌 Module Naming Standard

Use stable, lower-case module names.

Examples:

| Source file     | `exception.module` |
| --------------- | ------------------ |
| `loaders.py`    | `"loaders"`        |
| `fetchers.py`   | `"fetchers"`       |
| `scrapers.py`   | `"scrapers"`       |
| `processors.py` | `"processors"`     |
| `models.py`     | `"models"`         |
| `config.py`     | `"config"`         |
| `boogr.py`      | `"boogr"`          |



## 📌 Cause Naming Standard

Use the class name or operation name where the exception occurred.

Examples:

| Context                  | `exception.cause`           |
| ------------------------ | --------------------------- |
| `TextLoader.load`        | `"TextLoader"`              |
| `PdfLoader.split`        | `"PdfLoader"`               |
| API fetcher class        | Fetcher class name          |
| Web extraction class     | Extractor class name        |
| Tool execution           | `"ToolDef"`                 |
| Configuration validation | `"ConfigurationValidation"` |



## 📌 Method String Standard

Use a stable method signature string. Do not include live argument values, file contents, user data,
API keys, tokens, OCR text, or full payloads.

Good:

```python id="good_method_string"
exception.method = "load(self, path: str, encoding: Optional[str]=None) -> List[Document]"
```

Good:

```python id="good_fetch_method_string"
exception.method = "fetch(self, query: str, limit: int=10) -> dict"
```

Bad:

```python id="bad_method_string_with_value"
exception.method = "load(self, path='C:\\Users\\terry\\private\\file.txt')"
```

Bad:

```python id="bad_method_string_with_secret"
exception.method = "fetch(self, api_key='actual-secret-key')"
```

Bad:

```python id="bad_method_string_with_payload"
exception.method = "parse(self, text='full document text goes here')"
```



## 🧪 Validate Logger Write

Run this from the repository root:

```powershell id="validate_logger_write"
python -c "from boogr import Error, Logger; import config as cfg; error = Error(Exception('logging validation')); error.module = 'logging'; error.cause = 'ManualValidation'; error.method = 'manual logger validation'; Logger().write(error); print(cfg.LOG_PATH)"
```

Confirm the database exists:

```powershell id="confirm_logger_database"
Test-Path .\logging\Exceptions.db
```

Expected output:

```text id="expected_logger_database_output"
True
```



## 🧪 Validate Database with Python

Use this command to confirm the exception table exists and contains records:

```powershell id="validate_sqlite_records"
python -c "import sqlite3, config as cfg; conn = sqlite3.connect(cfg.LOG_PATH); cur = conn.cursor(); cur.execute('SELECT COUNT(*) FROM ' + cfg.LOG_FILE); print(cur.fetchone()); conn.close()"
```

Expected output shape:

```text id="expected_sqlite_count_shape"
(number_of_records,)
```

If the table does not exist, run the logger validation command first.



## 🧪 Intentional Loader Failure Test

Create the logging directory:

```powershell id="create_logging_directory"
New-Item -ItemType Directory -Force .\logging | Out-Null
```

Trigger a handled loader failure:

```powershell id="trigger_loader_failure"
python -c "from loaders import TextLoader; TextLoader().load(path='data/missing-file.txt', encoding='utf-8')"
```

Expected behavior:

```text id="expected_loader_failure"
- The command raises an exception.
- The exception is wrapped by boogr.Error.
- Logger writes a row to logging/Exceptions.db when the loader handler uses the required pattern.
```

Then inspect the record count:

```powershell id="inspect_record_count_after_failure"
python -c "import sqlite3, config as cfg; conn = sqlite3.connect(cfg.LOG_PATH); cur = conn.cursor(); cur.execute('SELECT COUNT(*) FROM ' + cfg.LOG_FILE); print(cur.fetchone()); conn.close()"
```



## 🧾 Inspect Recent Log Records

Use this PowerShell command to print recent exception records:

```powershell id="inspect_recent_records"
python -c "import sqlite3, config as cfg; conn = sqlite3.connect(cfg.LOG_PATH); cur = conn.cursor(); cur.execute('SELECT cause, module, method, message FROM ' + cfg.LOG_FILE + ' ORDER BY rowid DESC LIMIT 5'); rows = cur.fetchall(); conn.close(); [print(row) for row in rows]"
```

Expected output shape:

```text id="recent_records_shape"
('TextLoader', 'loaders', 'load(self, path: str, encoding: Optional[str]=None) -> List[Document]', '...')
```



## 🔐 Sensitive Data Rule

Do not log sensitive values in `exception.method`, `exception.cause`, or `exception.module`.

Do not include:

```text id="do_not_log_values"
- API keys
- Access tokens
- Passwords
- Full local file paths containing private directories
- Full document text
- OCR text
- User-provided payloads
- Provider response payloads
- Full request bodies
```

Use stable signatures instead.

Good:

```python id="safe_method_signature"
exception.method = "load(self, path: str, encoding: Optional[str]=None) -> List[Document]"
```

Bad:

```python id="unsafe_method_signature"
exception.method = f"load(self, path={path}, encoding={encoding})"
```



## 🧩 Logging in Loader Classes

Loader methods should log handled failures before re-raising.

Example:

```python id="loader_logging_example"
from boogr import Error, Logger


class TextLoader:
	def load(self, path: str, encoding: Optional[str] = None) -> List[Document]:
		"""Load a plain-text file.

		Purpose:
			Loads a local plain-text file into LangChain Document objects.

		Args:
			path (str): Path to the text file.
			encoding (Optional[str]): Optional file encoding.

		Returns:
			List[Document]: Loaded document objects.
		"""
		try:
			# Loader implementation.
			pass
		except Exception as e:
			exception = Error(e)
			exception.module = "loaders"
			exception.cause = "TextLoader"
			exception.method = "load(self, path: str, encoding: Optional[str]=None) -> List[Document]"
			Logger().write(exception)
			raise exception
```



## 🔌 Logging in Fetcher Classes

Fetcher methods should log request or provider failures without storing sensitive request payloads.

Example:

```python id="fetcher_logging_example"
from boogr import Error, Logger


class ExampleFetcher:
	def fetch(self, query: str, limit: int = 10) -> dict:
		"""Fetch example data.

		Purpose:
			Demonstrates the required logging pattern for fetcher methods.

		Args:
			query (str): Search query or lookup value.
			limit (int): Maximum number of records.

		Returns:
			dict: Normalized provider response.
		"""
		try:
			# Fetcher implementation.
			return { "query": query, "limit": limit, "items": [] }
		except Exception as e:
			exception = Error(e)
			exception.module = "fetchers"
			exception.cause = "ExampleFetcher"
			exception.method = "fetch(self, query: str, limit: int=10) -> dict"
			Logger().write(exception)
			raise exception
```



## 🧰 Logging in Tool Execution

`ToolDef.call()` should return structured failures for tool execution errors.

A tool result failure should preserve this shape:

```text id="tool_failure_shape"
{
    "ok": false,
    "name": "tool_name",
    "data": null,
    "error": {
        "type": "ExceptionType",
        "message": "Exception message"
    },
    "metadata": {
        "category": "...",
        "source_module": "...",
        "source_class": "...",
        "method": "..."
    }
}
```

This allows an AI tool loop to continue handling errors without losing the failure details.



## 🔁 Logging Validation Workflow

Use this workflow after regenerating source files:

```text id="logging_validation_workflow"
1. Confirm source imports include Error and Logger where handled exceptions are logged.
2. Confirm each handled exception creates exception = Error(e).
3. Confirm exception.module is set.
4. Confirm exception.cause is set.
5. Confirm exception.method is set.
6. Confirm Logger().write(exception) appears before raise exception.
7. Run python -m py_compile on the edited file.
8. Run python -m compileall .
9. Trigger one controlled failure.
10. Confirm logging/Exceptions.db exists and contains a record.
```



## 🔎 Search for Missing Logger Writes

Use this command to find handlers that wrap errors:

```powershell id="find_error_wrappers"
Select-String -Path .\*.py -Pattern "exception = Error\(e\)"
```

Use this command to find logger writes:

```powershell id="find_logger_writes"
Select-String -Path .\*.py -Pattern "Logger\(\)\.write\(exception\)"
```

The number of logger writes should match the number of handled wrappers that raise the wrapped
exception, unless a method intentionally returns a structured error envelope instead of raising.



## 🔎 Search for Helper Abstractions

Use this command to find helper-style logging abstractions that should not replace the explicit
pattern:

```powershell id="find_logging_helpers"
Select-String -Path .\*.py -Pattern "_log_and_raise|log_exception|raise_logged"
```

Expected result:

```text id="expected_no_logging_helpers"
No output.
```



## 🧯 Common Logging Problems

### Database file is not created

Likely causes:

```text id="database_not_created_causes"
- No handled exception has triggered Logger().write(exception).
- LOG_PATH points to a non-writable location.
- LOG_DIR was not created.
- The active source file lacks Logger().write(exception).
```

Fix:

```powershell id="database_not_created_fix"
New-Item -ItemType Directory -Force .\logging | Out-Null
python -c "from boogr import Error, Logger; e = Error(Exception('test')); e.module = 'logging'; e.cause = 'ManualValidation'; e.method = 'manual'; Logger().write(e)"
Test-Path .\logging\Exceptions.db
```



### Exception is raised but no row appears

Likely causes:

```text id="exception_no_row_causes"
- The exception occurred before the handled try-except block.
- The handler raises without Logger().write(exception).
- A different database path is configured through LOG_PATH.
- The query is checking the wrong table name.
```

Check the active values:

```powershell id="check_active_logging_values"
python -c "import config as cfg; print(cfg.LOG_PATH); print(cfg.LOG_FILE)"
```



### Method field contains live data

Bad:

```python id="bad_live_data_method"
exception.method = f"load(self, path={path})"
```

Fix:

```python id="fixed_stable_method"
exception.method = "load(self, path: str) -> List[Document]"
```



### Logger helper hides required behavior

Bad:

```python id="bad_hidden_logger"
except Exception as e:
	_raise_logged(e)
```

Fix:

```python id="fixed_explicit_logger"
except Exception as e:
	exception = Error(e)
	exception.module = "loaders"
	exception.cause = "TextLoader"
	exception.method = "load(self, path: str, encoding: Optional[str]=None) -> List[Document]"
	Logger().write(exception)
	raise exception
```



## ✅ Logging Checklist

| Check                    | Command or inspection                                                        |               |                |
| ------------------------ | ---------------------------------------------------------------------------- | ------------- | -------------- |
| Logging constants exist  | `python -c "import config as cfg; print(cfg.LOG_PATH); print(cfg.LOG_FILE)"` |               |                |
| Logger imports work      | `python -c "from boogr import Error, Logger; print('ok')"`                   |               |                |
| Database can be written  | Manual logger validation command                                             |               |                |
| Database exists          | `Test-Path .\logging\Exceptions.db`                                          |               |                |
| Error wrappers exist     | `Select-String -Path .\*.py -Pattern "exception = Error\(e\)"`               |               |                |
| Logger writes exist      | `Select-String -Path .\*.py -Pattern "Logger\(\)\.write\(exception\)"`       |               |                |
| No hidden helper pattern | `Select-String -Path .*.py -Pattern "_log_and_raise                          | log_exception | raise_logged"` |
| Source compiles          | `python -m compileall .`                                                     |               |                |
| Docs build               | `mkdocs build`                                                               |               |                |



## ➡️ Next Step

Continue to [Usage](usage.md) for practical examples showing how Fonky loaders, processors, and AI
tooling work together.
