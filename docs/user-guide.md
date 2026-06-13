# User Guide

This guide provides practical workflows for using Fonky across document loading, text processing,
web extraction, API fetching, and AI tool orchestration.

The examples assume a flat source layout where modules such as `loaders.py`, `processors.py`,
`scrapers.py`, `fetchers.py`, and `models.py` are located at the repository root.

## Guide Scope

Fonky is designed around a common workflow:

```text
Source content
    -> loader, fetcher, or scraper
    -> normalized output
    -> processor or tool wrapper
    -> downstream application, analysis workflow, or AI tool call
```

The most common user paths are:

| Workflow                 | Modules used            |
| ------------------------ | ----------------------- |
| Load local files         | `loaders.py`            |
| Split documents          | `loaders.py`            |
| Clean text               | `processors.py`         |
| Extract web content      | `scrapers.py`           |
| Fetch public API data    | `fetchers.py`           |
| Create AI-callable tools | `models.py`             |
| Log handled exceptions   | `boogr.py`, `config.py` |

## Basic Import Pattern

Use root-level imports for the current project layout:

```python
from loaders import TextLoader
from models import ToolDef
from processors import TextParser
```

Do not use package imports such as `from fonky.loaders import TextLoader` unless the source files
are later moved into a real package directory named `fonky`.

## Create Sample Data

Create a small sample text file:

```powershell
New-Item -ItemType Directory -Force .\data | Out-Null
"Fonky loads documents, processes text, and exposes callable tools." | Set-Content .\data\sample.txt -Encoding UTF8
```

Confirm the file exists:

```powershell
Test-Path .\data\sample.txt
```

Expected output:

```text
True
```

## Load a Text File

Use `TextLoader` to load a local text file.

```python
from loaders import TextLoader

loader = TextLoader()

documents = loader.load(
    path="data/sample.txt",
    encoding="utf-8"
)

print("Document count:", len(documents))

for document in documents:
    print("Metadata:", document.metadata)
    print("Content:", document.page_content)
    break
```

PowerShell inline version:

```powershell
python -c "from loaders import TextLoader; loader = TextLoader(); docs = loader.load(path='data/sample.txt', encoding='utf-8'); print(len(docs)); print(next(iter(docs)).page_content)"
```

## Split Loaded Documents

After a loader has loaded documents, call the loader split method.

```python
from loaders import TextLoader

loader = TextLoader()

loader.load(
    path="data/sample.txt",
    encoding="utf-8"
)

chunks = loader.split(
    chunk=500,
    overlap=50
)

print("Chunk count:", len(chunks))

for chunk in chunks:
    print(chunk.page_content)
    break
```

Use this when preparing documents for retrieval, indexing, summarization, or embedding workflows.

## Load and Process Text

A common workflow is to load text first, then pass the page content into a processor.

```python
from loaders import TextLoader
from processors import TextParser

loader = TextLoader()
parser = TextParser()

documents = loader.load(
    path="data/sample.txt",
    encoding="utf-8"
)

for document in documents:
    text = document.page_content
    break

cleaned = parser.clean_text(
    text=text
)

print(cleaned)
```

If the active `TextParser` class uses a different method name, use the exact method listed in the
API reference.

## Build a Reusable Load Function

Wrap a common loader pattern in a normal Python function.

```python
from loaders import TextLoader


def load_first_text(path: str, encoding: str = "utf-8") -> str:
    """Load the first document text from a local text file.

    Purpose:
        Provides a small helper that loads a local text file and returns the first
        available document text value.

    Args:
        path (str): Local text file path.
        encoding (str): File encoding.

    Returns:
        str: First document text or an empty string.
    """
    loader = TextLoader()

    documents = loader.load(
        path=path,
        encoding=encoding
    )

    for document in documents:
        return document.page_content

    return ""


text = load_first_text(
    path="data/sample.txt"
)

print(text)
```

This kind of helper can also be exposed as an AI tool through `ToolDef`.

## Create a Tool from a Function

Fonky can convert plain Python functions into structured tools.

```python
from models import ToolDef


def count_words(text: str) -> int:
    """Count words in a text value.

    Purpose:
        Counts whitespace-separated words in a text value.

    Args:
        text (str): Text to count.

    Returns:
        int: Number of words.
    """
    return len(text.split())


tool = ToolDef.from_callable(
    function=count_words,
    name="count_words",
    description="Count words in a text value.",
    category="text"
)

result = tool.call(
    {
        "text": "Fonky exposes Python functions as AI-callable tools."
    }
)

print(result)
```

Expected result shape:

```text
{
    "ok": true,
    "name": "count_words",
    "data": 7,
    "error": null,
    "metadata": {
        "category": "text"
    }
}
```

The exact metadata fields depend on the active `ToolDef` implementation.

## Create a Tool from a Loader Method

Expose `TextLoader.load` as an AI-callable tool.

```python
from loaders import TextLoader
from models import ToolDef

loader = TextLoader()

load_tool = ToolDef.from_method(
    target=loader,
    method="load",
    name="load_text_file",
    description="Load a local text file into document objects.",
    category="documents"
)

result = load_tool.call(
    {
        "path": "data/sample.txt",
        "encoding": "utf-8"
    }
)

print("Succeeded:", result.get("ok"))

if result.get("ok"):
    data = result.get("data") or []

    for item in data:
        print(item.get("page_content"))
        break
else:
    print(result.get("error"))
```

This pattern allows an AI model to select a file-loading tool while Fonky executes the underlying
Python method.

## Export Tool Schemas

Export tool schemas before passing them to a model provider.

```python
from models import ToolDef


def uppercase_text(text: str) -> str:
    """Convert text to uppercase.

    Purpose:
        Provides a deterministic text transformation tool.

    Args:
        text (str): Text to transform.

    Returns:
        str: Uppercase text.
    """
    return text.upper()


tool = ToolDef.from_callable(
    function=uppercase_text,
    name="uppercase_text",
    description="Convert text to uppercase.",
    category="text"
)

print("Provider neutral:")
print(tool.to_dict())

print("OpenAI:")
print(tool.to_openai())

print("Gemini:")
print(tool.to_gemini())

print("Grok:")
print(tool.to_grok())
```

## Build a Tool Registry

A registry maps tool names to `ToolDef` objects.

```python
from models import ToolDef


def count_words(text: str) -> int:
    """Count words in text.

    Purpose:
        Provides a deterministic word-count tool.

    Args:
        text (str): Text to count.

    Returns:
        int: Number of words.
    """
    return len(text.split())


def reverse_text(text: str) -> str:
    """Reverse text.

    Purpose:
        Provides a deterministic text reversal tool.

    Args:
        text (str): Text to reverse.

    Returns:
        str: Reversed text.
    """
    return text[::-1]


tools = [
    ToolDef.from_callable(
        function=count_words,
        name="count_words",
        description="Count words in text.",
        category="text"
    ),
    ToolDef.from_callable(
        function=reverse_text,
        name="reverse_text",
        description="Reverse a text value.",
        category="text"
    )
]

registry = {
    tool.name: tool
    for tool in tools
}

for tool_name in registry:
    print(tool_name)
```

## Dispatch a Model-Selected Tool Call

Most model providers return a tool name and argument dictionary when a tool is selected.

This example uses a provider-neutral payload.

```python
model_selected_call = {
    "name": "count_words",
    "arguments": {
        "text": "Fonky can dispatch AI-selected tool calls."
    }
}

tool_name = model_selected_call.get("name")
arguments = model_selected_call.get("arguments") or {}

selected_tool = registry.get(tool_name)

if selected_tool is None:
    result = {
        "ok": False,
        "name": tool_name,
        "data": None,
        "error": {
            "type": "ToolNotFound",
            "message": f"No registered tool named {tool_name}."
        },
        "metadata": {}
    }
else:
    result = selected_tool.call(arguments)

print(result)
```

This is the basic bridge between a model provider's tool-calling response and Fonky's Python
execution layer.

## Chain Loader and Tool Calls

You can chain a file-loading tool with a text-processing tool.

```python
from loaders import TextLoader
from models import ToolDef


def first_document_text(documents: list[dict]) -> str:
    """Extract the first document text value.

    Purpose:
        Reads serialized document dictionaries and returns the first available
        page content value.

    Args:
        documents (list[dict]): Serialized document dictionaries.

    Returns:
        str: First page content value or an empty string.
    """
    for document in documents:
        value = document.get("page_content")

        if value:
            return value

    return ""


def count_words(text: str) -> int:
    """Count words in text.

    Purpose:
        Counts whitespace-separated words in a text value.

    Args:
        text (str): Text to count.

    Returns:
        int: Number of words.
    """
    return len(text.split())


loader = TextLoader()

tools = [
    ToolDef.from_method(
        target=loader,
        method="load",
        name="load_text_file",
        description="Load a local text file.",
        category="documents"
    ),
    ToolDef.from_callable(
        function=first_document_text,
        name="first_document_text",
        description="Extract the first text value from serialized document output.",
        category="documents"
    ),
    ToolDef.from_callable(
        function=count_words,
        name="count_words",
        description="Count words in text.",
        category="text"
    )
]

registry = {
    tool.name: tool
    for tool in tools
}

load_result = registry.get("load_text_file").call(
    {
        "path": "data/sample.txt",
        "encoding": "utf-8"
    }
)

if not load_result.get("ok"):
    print(load_result.get("error"))
    raise SystemExit(1)

text_result = registry.get("first_document_text").call(
    {
        "documents": load_result.get("data") or []
    }
)

if not text_result.get("ok"):
    print(text_result.get("error"))
    raise SystemExit(1)

count_result = registry.get("count_words").call(
    {
        "text": text_result.get("data") or ""
    }
)

print(count_result)
```

## Use a Fetcher as a Tool

Fetcher methods can be wrapped in the same way as loader methods.

Use the exact class and method names from the API reference.

```python
from models import ToolDef
from fetchers import SomeFetcherClass

fetcher = SomeFetcherClass()

fetch_tool = ToolDef.from_method(
    target=fetcher,
    method="some_fetch_method",
    name="fetch_external_data",
    description="Fetch external data using a Fonky fetcher method.",
    category="fetchers"
)

schema = fetch_tool.to_openai()

print(schema)
```

Call the tool with the method's actual arguments:

```python
result = fetch_tool.call(
    {
        "query": "example",
        "limit": 10
    }
)

print("Succeeded:", result.get("ok"))

if result.get("ok"):
    print(result.get("data"))
else:
    print(result.get("error"))
```

Replace `SomeFetcherClass`, `some_fetch_method`, and the arguments with real names from the active
`fetchers.py` API reference.

## Use a Scraper as a Tool

Scraper methods can be exposed as tools.

```python
from models import ToolDef
from scrapers import WebExtractor

extractor = WebExtractor()

extract_tool = ToolDef.from_method(
    target=extractor,
    method="extract_text",
    name="extract_web_text",
    description="Extract readable text from web content.",
    category="web"
)

print(extract_tool.to_openai())
```

Call the tool with arguments matching the method signature:

```python
result = extract_tool.call(
    {
        "url": "https://example.com"
    }
)

print("Succeeded:", result.get("ok"))

if result.get("ok"):
    print(result.get("data"))
else:
    print(result.get("error"))
```

If your scraper method expects HTML instead of a URL, pass the correct argument name from the API
reference.

## Validate Tool Results

Successful tools should return a structured result envelope.

```text
ok = true
data = serialized result payload
error = null
```

Failed tools should return:

```text
ok = false
data = null
error = error details
```

Example failure:

```python
from models import ToolDef


def divide_numbers(numerator: float, denominator: float) -> float:
    """Divide two numbers.

    Purpose:
        Demonstrates structured tool failure handling.

    Args:
        numerator (float): Numerator value.
        denominator (float): Denominator value.

    Returns:
        float: Division result.
    """
    return numerator / denominator


divide_tool = ToolDef.from_callable(
    function=divide_numbers,
    name="divide_numbers",
    description="Divide one number by another.",
    category="math"
)

result = divide_tool.call(
    {
        "numerator": 10,
        "denominator": 0
    }
)

print(result)
```

## Work with Serialized Documents

When tool calls return document-like objects, Fonky should serialize them into dictionaries.

Common serialized document fields:

```text
page_content
metadata
```

Example:

```python
result = load_tool.call(
    {
        "path": "data/sample.txt",
        "encoding": "utf-8"
    }
)

if result.get("ok"):
    documents = result.get("data") or []

    for document in documents:
        print(document.get("page_content"))
        print(document.get("metadata"))
        break
```

## Validate Documentation Directives

Manual docs should not contain live mkdocstrings directives.

Run:

```powershell
Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"
```

Expected output:

```text
No output.
```

API docs should contain live directives.

Run:

```powershell
Select-String -Path .\docs\api\*.md -Pattern "^:::\s+[A-Za-z_]"
```

Expected output includes entries such as:

```text
docs\api\loaders.md:3:::: loaders
docs\api\models.md:3:::: models
docs\api\processors.md:3:::: processors
```

## Validate the Site

Run these commands before deployment:

```powershell
python -m compileall .
mkdocs build
mkdocs serve
```

Review the local site at:

```text
http://127.0.0.1:8000/
```

## User Guide Checklist

| Check                                  | Command or action                                                 |
| -------------------------------------- | ----------------------------------------------------------------- |
| Source compiles                        | `python -m compileall .`                                          |
| Core imports work                      | `python -c "import loaders; import models; print('ok')"`          |
| ToolDef imports                        | `python -c "from models import ToolDef; print('ok')"`             |
| Sample text loads                      | Run the `TextLoader` example.                                     |
| Tool executes                          | Run a `ToolDef.call(...)` example.                                |
| Provider schema exports                | Run `to_openai`, `to_gemini`, or `to_grok`.                       |
| Manual docs contain no live directives | `Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"`     |
| API docs contain live directives       | `Select-String -Path .\docs\api\*.md -Pattern "^:::\s+[A-Za-z_]"` |
| Docs build                             | `mkdocs build`                                                    |


