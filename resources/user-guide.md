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

## Tool Examples for Every Loader and Fetcher Class

The following examples cover every class declared in `loaders.py` and `fetchers.py`. Each
example creates a provider-neutral `ToolDef`, exports the OpenAI-compatible schema, executes the
bound method, and inspects Fonky's structured result envelope.

Run this helper once before the individual examples:

```python
from typing import Any

from models import ToolDef


def run_tool(tool: ToolDef, arguments: dict[str, Any]) -> dict[str, Any]:
    """Export, execute, and display a Fonky tool.

    Purpose:
        Prints the OpenAI-compatible schema, executes the bound method, and displays either
        serialized data or structured error information.

    Args:
        tool (ToolDef): Bound Fonky tool definition.
        arguments (dict[str, Any]): Keyword arguments passed to the bound method.

    Returns:
        dict[str, Any]: Structured tool execution result.
    """
    print("Schema:")
    print(tool.to_openai())

    result = tool.call(arguments)

    print("Succeeded:", result["ok"])

    if result["ok"]:
        print("Data:", result["data"])
    else:
        print("Error:", result["error"])

    return result
```

Local paths and provider identifiers below are illustrative. Create the referenced sample files or
replace the values with real resources. Configure API keys, cloud credentials, and identity tokens
outside model-generated argument payloads whenever the class can obtain them from application
configuration or the provider's normal credential chain.

## Loader Class Tool Examples

These 29 examples cover the shared `Loader` base and every concrete loader class. The examples
wrap the primary ingestion method for each class; inherited `split` methods can be registered as
separate tools after a successful load when model-directed chunking is required.

### `Loader.verify_exists`

Validate a local path through the shared loader base.

```python
from loaders import Loader

target = Loader()

tool = ToolDef.from_method(
    target=target,
    method="verify_exists",
    name="loader_verify_exists",
    description="Validate a local path through the shared loader base.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "path": "data/sample.txt"
    }
)
```

The base `Loader` is concrete for shared path and splitting utilities; normal ingestion should use a specialized loader.
### `TextLoader.load`

Load a UTF-8 text file as document objects.

```python
from loaders import TextLoader

target = TextLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="text_loader_load",
    description="Load a UTF-8 text file as document objects.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "path": "data/sample.txt",
        "encoding": "utf-8"
    }
)
```
### `CsvLoader.load`

Load a comma-delimited file and retain a source column in document metadata.

```python
from loaders import CsvLoader

target = CsvLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="csv_loader_load",
    description="Load a comma-delimited file and retain a source column in document metadata.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "path": "data/sample.csv",
        "encoding": "utf-8",
        "source_column": "source",
        "delimiter": ",",
        "quotechar": "\""
    }
)
```
### `WebLoader.load`

Load one or more web pages without recursive crawling.

```python
from loaders import WebLoader

target = WebLoader(recursive=False)

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="web_loader_load",
    description="Load one or more web pages without recursive crawling.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "urls": ["https://example.com"]
    }
)
```

Set `recursive=True` on the constructor when the tool should follow links.
### `PdfReader.load`

Read a local PDF in single-document mode.

```python
from loaders import PdfReader

target = PdfReader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="pdf_reader_load",
    description="Read a local PDF in single-document mode.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "path": "data/sample.pdf",
        "mode": "single"
    }
)
```
### `PdfLoader.load`

Load a PDF with the wrapper's configurable text and image extraction behavior.

```python
from loaders import PdfLoader

target = PdfLoader(size=1000, overlap=150, has_tables=True, include=True)

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="pdf_loader_load",
    description="Load a PDF with the wrapper's configurable text and image extraction behavior.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "path": "data/sample.pdf",
        "mode": "single",
        "extract": "plain",
        "include": False,
        "format": "markdown-img"
    }
)
```

Constructor settings control chunking and table/image preparation; method arguments control the active extraction run.
### `ExcelLoader.load`

Load workbook content as document elements with a header row.

```python
from loaders import ExcelLoader

target = ExcelLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="excel_loader_load",
    description="Load workbook content as document elements with a header row.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "path": "data/sample.xlsx",
        "mode": "elements",
        "has_headers": True
    }
)
```
### `WordLoader.load`

Load a local Microsoft Word document.

```python
from loaders import WordLoader

target = WordLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="word_loader_load",
    description="Load a local Microsoft Word document.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "path": "data/sample.docx"
    }
)
```
### `MarkdownLoader.load`

Load a Markdown document.

```python
from loaders import MarkdownLoader

target = MarkdownLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="markdown_loader_load",
    description="Load a Markdown document.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "path": "README.md"
    }
)
```
### `HtmlLoader.load`

Load a local HTML file.

```python
from loaders import HtmlLoader

target = HtmlLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="html_loader_load",
    description="Load a local HTML file.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "path": "data/sample.html"
    }
)
```
### `ArXivLoader.load`

Search arXiv and return matching papers as documents.

```python
from loaders import ArXivLoader

target = ArXivLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="ar_xiv_loader_load",
    description="Search arXiv and return matching papers as documents.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "question": "retrieval augmented generation"
    }
)
```

This operation requires network access.
### `WikiLoader.load`

Search Wikipedia and return matching pages as documents.

```python
from loaders import WikiLoader

target = WikiLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="wiki_loader_load",
    description="Search Wikipedia and return matching pages as documents.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "question": "federal budget process"
    }
)
```

This operation requires network access.
### `GoogleDriveLoader.load_file`

Load a Google Drive file by its provider identifier.

```python
from loaders import GoogleDriveLoader

target = GoogleDriveLoader()

tool = ToolDef.from_method(
    target=target,
    method="load_file",
    name="google_drive_loader_load_file",
    description="Load a Google Drive file by its provider identifier.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "file_id": "replace-with-google-drive-file-id",
        "recursive": False
    }
)
```

Configure Google credentials before execution. Use `load_folder` instead when the tool should retrieve an entire folder.
### `OutlookLoader.load`

Load a local Outlook `.msg` message.

```python
from loaders import OutlookLoader

target = OutlookLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="outlook_loader_load",
    description="Load a local Outlook `.msg` message.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "path": "data/sample.msg"
    }
)
```
### `SpfxLoader.load`

Load an authenticated SharePoint document library.

```python
from loaders import SpfxLoader

target = SpfxLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="spfx_loader_load",
    description="Load an authenticated SharePoint document library.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "library_id": "replace-with-sharepoint-library-id"
    }
)
```

Configure Microsoft identity credentials before execution.
### `PowerPointLoader.load`

Load a local PowerPoint file as a single document stream.

```python
from loaders import PowerPointLoader

target = PowerPointLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="power_point_loader_load",
    description="Load a local PowerPoint file as a single document stream.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "path": "data/sample.pptx",
        "mode": "single"
    }
)
```

Use `load_multiple` when a path pattern should resolve multiple presentations.
### `OneDriveDocLoader.load`

Load a OneDrive folder by drive identifier and folder path.

```python
from loaders import OneDriveDocLoader

target = OneDriveDocLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="one_drive_doc_loader_load",
    description="Load a OneDrive folder by drive identifier and folder path.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "drive_id": "replace-with-onedrive-drive-id",
        "folder_path": "/Shared Documents/Guidance",
        "auth_with_token": True
    }
)
```

Configure Microsoft identity credentials before execution; `object_ids` can replace `folder_path` for item-specific retrieval.
### `EmailLoader.load`

Load an email file and process attachments.

```python
from loaders import EmailLoader

target = EmailLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="email_loader_load",
    description="Load an email file and process attachments.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "path": "data/sample.eml",
        "mode": "single",
        "attachments": True
    }
)
```
### `JsonLoader.load`

Load JSON content using the loader's configured `.messages[].content` jq path.

```python
from loaders import JsonLoader

target = JsonLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="json_loader_load",
    description="Load JSON content using the loader's configured `.messages[].content` jq path.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "filepath": "data/messages.json",
        "is_text": True,
        "is_lines": False
    }
)
```

The input JSON must contain the structure expected by the class's jq expression.
### `GithubLoader.load`

Load Markdown files from a GitHub repository branch.

```python
from loaders import GithubLoader

target = GithubLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="github_loader_load",
    description="Load Markdown files from a GitHub repository branch.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "url": "https://api.github.com",
        "repo": "openai/openai-python",
        "branch": "main",
        "filetype": ".md"
    }
)
```

Configure a GitHub token when the repository or API rate limit requires authentication.
### `XmlLoader.load`

Load a local XML document through the unstructured XML path.

```python
from loaders import XmlLoader

target = XmlLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="xml_loader_load",
    description="Load a local XML document through the unstructured XML path.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "filepath": "data/sample.xml"
    }
)
```

Use `load_tree` and `get_elements` for XPath-oriented workflows.
### `PubMedSearchLoader.load`

Retrieve a bounded set of PubMed records.

```python
from loaders import PubMedSearchLoader

target = PubMedSearchLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="pub_med_search_loader_load",
    description="Retrieve a bounded set of PubMed records.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "query": "machine learning clinical decision support",
        "max_docs": 5
    }
)
```
### `OpenCityLoader.load`

Load records from an Open City dataset.

```python
from loaders import OpenCityLoader

target = OpenCityLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="open_city_loader_load",
    description="Load records from an Open City dataset.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "city_id": "replace-with-city-id",
        "dataset_id": "replace-with-dataset-id",
        "limit": 25
    }
)
```

Replace both identifiers with values supported by the backing Open City service.
### `JupyterNotebookLoader.load`

Load notebook source and optionally include cell outputs.

```python
from loaders import JupyterNotebookLoader

target = JupyterNotebookLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="jupyter_notebook_loader_load",
    description="Load notebook source and optionally include cell outputs.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "path": "data/sample.ipynb",
        "include_outputs": True,
        "max_output_length": 200,
        "remove_newline": False,
        "traceback": False
    }
)
```
### `GoogleCloudFileLoader.load`

Load one object from Google Cloud Storage.

```python
from loaders import GoogleCloudFileLoader

target = GoogleCloudFileLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="google_cloud_file_loader_load",
    description="Load one object from Google Cloud Storage.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "project_name": "replace-with-gcp-project",
        "bucket": "replace-with-gcs-bucket",
        "blob": "guidance/sample.pdf"
    }
)
```

Configure Google Application Default Credentials before execution.
### `AwsFileLoader.load`

Load one Amazon S3 object while relying on the normal AWS credential chain.

```python
from loaders import AwsFileLoader

target = AwsFileLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="aws_file_loader_load",
    description="Load one Amazon S3 object while relying on the normal AWS credential chain.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "bucket": "replace-with-s3-bucket",
        "key": "guidance/sample.pdf",
        "region_name": "us-east-1"
    }
)
```

Keep AWS secrets outside model-generated arguments; use environment, profile, workload, or instance credentials.
### `GoogleSpeechToTextLoader.load`

Transcribe an audio source through Google Cloud Speech-to-Text.

```python
from loaders import GoogleSpeechToTextLoader

target = GoogleSpeechToTextLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="google_speech_to_text_loader_load",
    description="Transcribe an audio source through Google Cloud Speech-to-Text.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "project_id": "replace-with-gcp-project",
        "file_path": "gs://replace-with-bucket/audio/sample.wav"
    }
)
```

Configure Google credentials and provide a service-supported audio URI or path.
### `GoogleBucketLoader.load`

Load a Google Cloud Storage prefix as a document collection.

```python
from loaders import GoogleBucketLoader

target = GoogleBucketLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="google_bucket_loader_load",
    description="Load a Google Cloud Storage prefix as a document collection.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "project_name": "replace-with-gcp-project",
        "bucket": "replace-with-gcs-bucket",
        "prefix": "guidance/",
        "continue_on_failure": False
    }
)
```
### `AwsBucketLoader.load`

Load an Amazon S3 prefix as a document collection.

```python
from loaders import AwsBucketLoader

target = AwsBucketLoader()

tool = ToolDef.from_method(
    target=target,
    method="load",
    name="aws_bucket_loader_load",
    description="Load an Amazon S3 prefix as a document collection.",
    category="loaders"
)

result = run_tool(
    tool=tool,
    arguments={
        "bucket": "replace-with-s3-bucket",
        "prefix": "guidance/",
        "region_name": "us-east-1"
    }
)
```

Keep AWS secrets outside the tool call and rely on the normal AWS credential chain.

## Fetcher Class Tool Examples

These 49 examples cover the abstract `Fetcher` contract and every concrete fetcher class. Most
examples wrap the class's unified `fetch` method. Classes without a unified dispatcher use their
most representative public retrieval or URL-construction method.

### `Fetcher.fetch`

Expose the abstract base contract for schema inspection and failure-envelope testing.

```python
from fetchers import Fetcher

target = Fetcher()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="fetcher_fetch",
    description="Expose the abstract base contract for schema inspection and failure-envelope testing.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "query": "example",
        "url": "https://example.com",
        "time": 10
    }
)
```

`Fetcher.fetch` intentionally raises `NotImplementedError`; `run_tool` therefore reports `ok=False`. Register a concrete subclass for production execution.
### `WebFetcher.fetch`

Fetch and normalize a web page.

```python
from fetchers import WebFetcher

target = WebFetcher()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="web_fetcher_fetch",
    description="Fetch and normalize a web page.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "url": "https://example.com",
        "time": 10
    }
)
```
### `WebCrawler.crawl`

Crawl a bounded set of same-domain pages.

```python
from fetchers import WebCrawler

target = WebCrawler(use_playwright=False)

tool = ToolDef.from_method(
    target=target,
    method="crawl",
    name="web_crawler_crawl",
    description="Crawl a bounded set of same-domain pages.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "seed_url": "https://example.com",
        "recursive": True,
        "max_depth": 1,
        "max_pages": 5,
        "same_domain_only": True
    }
)
```

Set `use_playwright=True` only when browser rendering is installed and required.
### `ArXiv.fetch`

Search arXiv with constructor defaults retained by the instance.

```python
from fetchers import ArXiv

target = ArXiv(max_documents=5, full_documents=False, include_metadata=True)

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="ar_xiv_fetch",
    description="Search arXiv with constructor defaults retained by the instance.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "question": "retrieval augmented generation"
    }
)
```
### `GoogleDrive.fetch`

Search Google Drive content through the configured query template.

```python
from fetchers import GoogleDrive

target = GoogleDrive()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="google_drive_fetch",
    description="Search Google Drive content through the configured query template.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "question": "budget execution guidance",
        "folder_id": "root",
        "results": 10,
        "mode": "documents"
    }
)
```

Configure Google Drive authentication before execution.
### `Wikipedia.fetch`

Search Wikipedia in the configured language.

```python
from fetchers import Wikipedia

target = Wikipedia(language="en", max_documents=5, include_metadata=True)

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="wikipedia_fetch",
    description="Search Wikipedia in the configured language.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "question": "Congressional Budget and Impoundment Control Act"
    }
)
```
### `TheNews.fetch`

Retrieve recent English-language articles matching a query.

```python
from fetchers import TheNews

target = TheNews()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="the_news_fetch",
    description="Retrieve recent English-language articles matching a query.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "endpoint": "all",
        "query": "artificial intelligence",
        "language": "en",
        "limit": 10,
        "page": 1
    }
)
```

Configure the news API key outside model-generated arguments.
### `GoogleSearch.fetch`

Run a bounded Google Custom Search query.

```python
from fetchers import GoogleSearch

target = GoogleSearch()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="google_search_fetch",
    description="Run a bounded Google Custom Search query.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "keywords": "site:gao.gov artificial intelligence",
        "results": 10,
        "safe": "off"
    }
)
```

Configure both the Google API key and Custom Search Engine identifier.
### `GoogleMaps.geocode_location`

Geocode a street address with Google Maps.

```python
from fetchers import GoogleMaps

target = GoogleMaps()

tool = ToolDef.from_method(
    target=target,
    method="geocode_location",
    name="google_maps_geocode_location",
    description="Geocode a street address with Google Maps.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "address": "1600 Pennsylvania Avenue NW, Washington, DC"
    }
)
```

Configure the Google Maps API key before execution.
### `GoogleWeather.fetch_current`

Retrieve current weather for a resolved address.

```python
from fetchers import GoogleWeather

target = GoogleWeather()

tool = ToolDef.from_method(
    target=target,
    method="fetch_current",
    name="google_weather_fetch_current",
    description="Retrieve current weather for a resolved address.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "address": "Arlington, VA",
        "units_system": "METRIC",
        "language_code": "en",
        "time": 10
    }
)
```

Configure the Google Weather/Maps credentials required by coordinate resolution and weather requests.
### `NavalObservatory.fetch`

Request a celestial-navigation observation for a date, time, and position.

```python
from fetchers import NavalObservatory

target = NavalObservatory()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="naval_observatory_fetch",
    description="Request a celestial-navigation observation for a date, time, and position.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "celnav",
        "date_value": "2026-08-11",
        "time_value": "12:00:00",
        "latitude": 38.8816,
        "longitude": -77.0910,
        "location_label": "Arlington, VA"
    }
)
```
### `SatelliteCenter.fetch`

List satellite observatories from the coordinated-data service.

```python
from fetchers import SatelliteCenter

target = SatelliteCenter()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="satellite_center_fetch",
    description="List satellite observatories from the coordinated-data service.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "observatories"
    }
)
```
### `EarthObservatory.fetch`

Retrieve currently open Earth-observation events.

```python
from fetchers import EarthObservatory

target = EarthObservatory()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="earth_observatory_fetch",
    description="Retrieve currently open Earth-observation events.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "events",
        "status": "open",
        "limit": 20,
        "days": 30
    }
)
```
### `GlobalImagery.get_capabilities_url`

Build the service-capabilities URL for a selected global imagery projection.

```python
from fetchers import GlobalImagery

target = GlobalImagery()

tool = ToolDef.from_method(
    target=target,
    method="get_capabilities_url",
    name="global_imagery_get_capabilities_url",
    description="Build the service-capabilities URL for a selected global imagery projection.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "projection": "epsg4326",
        "quality": "best",
        "version": "1.1.1"
    }
)
```

Use `fetch_wms_map` instead when the tool should download and save a rendered map image.
### `NearbyObjects.fetch`

Retrieve near-Earth-object close approaches for a bounded date range.

```python
from fetchers import NearbyObjects

target = NearbyObjects()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="nearby_objects_fetch",
    description="Retrieve near-Earth-object close approaches for a bounded date range.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "close_approaches",
        "start_date": "2026-08-11",
        "end_date": "2026-08-18",
        "dist_max": "10LD",
        "body": "Earth",
        "limit": 20
    }
)
```
### `OpenScience.fetch`

Search open-science metadata and request JSON output.

```python
from fetchers import OpenScience

target = OpenScience()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="open_science_fetch",
    description="Search open-science metadata and request JSON output.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "metadata",
        "query": "climate change",
        "format_value": "json"
    }
)
```
### `SpaceWeather.fetch`

Retrieve coronal-mass-ejection records for a date range.

```python
from fetchers import SpaceWeather

target = SpaceWeather()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="space_weather_fetch",
    description="Retrieve coronal-mass-ejection records for a date range.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "cme",
        "start_date": "2026-08-01",
        "end_date": "2026-08-11",
        "location": "ALL",
        "catalog": "ALL"
    }
)
```

Configure a DONKI/NASA API key outside model arguments when the service requires one.
### `AstroCatalog.fetch`

Query an astronomical catalog by object name.

```python
from fetchers import AstroCatalog

target = AstroCatalog()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="astro_catalog_fetch",
    description="Query an astronomical catalog by object name.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "object_query",
        "query": "M31",
        "data_format": "json"
    }
)
```
### `AstroQuery.fetch`

Search astronomical object data through Astroquery.

```python
from fetchers import AstroQuery

target = AstroQuery()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="astro_query_fetch",
    description="Search astronomical object data through Astroquery.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "object_search",
        "query": "M31",
        "row_limit": 25
    }
)
```
### `StarMap.fetch`

Create a link to an interactive star map centered on an object.

```python
from fetchers import StarMap

target = StarMap()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="star_map_fetch",
    description="Create a link to an interactive star map centered on an object.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "object_link",
        "query": "Polaris",
        "zoom": 5,
        "show_box": True
    }
)
```
### `GovData.fetch`

Search the federal data catalog.

```python
from fetchers import GovData

target = GovData()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="gov_data_fetch",
    description="Search the federal data catalog.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "search",
        "query": "federal budget",
        "page_size": 10,
        "sort_field": "score",
        "sort_order": "DESC"
    }
)
```
### `StarChart.fetch`

Generate an object-centered astronomical chart.

```python
from fetchers import StarChart

target = StarChart()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="star_chart_fetch",
    description="Generate an object-centered astronomical chart.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "object_chart",
        "query": "M31",
        "zoom": 5,
        "image_source": "DSS2"
    }
)
```
### `Congress.fetch`

Retrieve a page of bills for a Congress.

```python
from fetchers import Congress

target = Congress()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="congress_fetch",
    description="Retrieve a page of bills for a Congress.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "bills",
        "congress": 119,
        "offset": 0,
        "limit": 20,
        "sort": "updateDate+desc"
    }
)
```

Configure the Congress.gov API key before execution.
### `InternetArchive.fetch`

Search Internet Archive metadata.

```python
from fetchers import InternetArchive

target = InternetArchive()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="internet_archive_fetch",
    description="Search Internet Archive metadata.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "keywords": "federal budget",
        "fields": ["identifier", "title", "date"],
        "rows": 10,
        "page": 1,
        "sort": "downloads desc"
    }
)
```
### `OpenWeather.fetch`

Retrieve current weather by place name.

```python
from fetchers import OpenWeather

target = OpenWeather()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="open_weather_fetch",
    description="Retrieve current weather by place name.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "location": "Arlington, VA",
        "mode": "current",
        "zone": "auto",
        "count": 5
    }
)
```
### `HistoricalWeather.fetch`

Retrieve historical weather for a place and Python date value.

```python
import datetime as dt

from fetchers import HistoricalWeather

target = HistoricalWeather()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="historical_weather_fetch",
    description="Retrieve historical weather for a place and Python date value.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "location": "Arlington, VA",
        "date": dt.date(2026, 8, 1),
        "zone": "auto",
        "count": 5
    }
)
```

Direct `ToolDef.call` dispatch does not coerce an ISO string into `datetime.date`, so the example
passes a Python `date` object explicitly.
### `Grokipedia.fetch`

Search Grokipedia and return a bounded result set.

```python
from fetchers import Grokipedia

target = Grokipedia()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="grokipedia_fetch",
    description="Search Grokipedia and return a bounded result set.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "search",
        "query": "federal appropriations",
        "limit": 10,
        "offset": 0
    }
)
```
### `GoogleGeocoding.fetch`

Forward-geocode a location through the unified dispatch method.

```python
from fetchers import GoogleGeocoding

target = GoogleGeocoding()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="google_geocoding_fetch",
    description="Forward-geocode a location through the unified dispatch method.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "forward",
        "query": "Arlington, VA",
        "language": "en",
        "region": "us"
    }
)
```

Configure the Google Geocoding API key outside model arguments.
### `CensusData.fetch`

Retrieve ACS population values for every state.

```python
from fetchers import CensusData

target = CensusData()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="census_data_fetch",
    description="Retrieve ACS population values for every state.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "data",
        "year": "2022",
        "dataset": "acs/acs5",
        "fields": "NAME,B01001_001E",
        "geography_for": "state:*"
    }
)
```
### `Socrata.fetch`

Retrieve a small page from a Socrata dataset.

```python
from fetchers import Socrata

target = Socrata()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="socrata_fetch",
    description="Retrieve a small page from a Socrata dataset.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "rows",
        "domain": "data.cdc.gov",
        "dataset_id": "unsk-b7fc",
        "limit": 5,
        "offset": 0
    }
)
```

Dataset identifiers can be retired or replaced; substitute a current identifier from the target Socrata catalog.
### `HealthData.fetch`

Retrieve rows from a HealthData.gov Socrata dataset.

```python
from fetchers import HealthData

target = HealthData()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="health_data_fetch",
    description="Retrieve rows from a HealthData.gov Socrata dataset.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "rows",
        "domain": "healthdata.gov",
        "dataset_id": "replace-with-healthdata-dataset-id",
        "limit": 5,
        "offset": 0
    }
)
```

Replace the dataset identifier with the current catalog value.
### `GlobalHealthData.fetch`

Retrieve the global health indicator registry.

```python
from fetchers import GlobalHealthData

target = GlobalHealthData()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="global_health_data_fetch",
    description="Retrieve the global health indicator registry.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "indicator_registry"
    }
)
```
### `UnitedNations.fetch`

Retrieve the United Nations dataset catalog.

```python
from fetchers import UnitedNations

target = UnitedNations()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="united_nations_fetch",
    description="Retrieve the United Nations dataset catalog.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "datasets"
    }
)
```
### `WorldPopulation.fetch`

Retrieve the World Bank population-data catalog.

```python
from fetchers import WorldPopulation

target = WorldPopulation()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="world_population_fetch",
    description="Retrieve the World Bank population-data catalog.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "catalog",
        "page": 1,
        "page_size": 25
    }
)
```
### `Wonder.fetch`

Retrieve the CDC WONDER request template for a dataset.

```python
from fetchers import Wonder

target = Wonder()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="wonder_fetch",
    description="Retrieve the CDC WONDER request template for a dataset.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "metadata_template",
        "dataset_id": "D76"
    }
)
```

Use a carefully reviewed `request_xml` value only for modes that submit a WONDER query.
### `USGSEarthquakes.fetch`

Retrieve the USGS all-earthquakes daily feed.

```python
from fetchers import USGSEarthquakes

target = USGSEarthquakes()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="usgsearthquakes_fetch",
    description="Retrieve the USGS all-earthquakes daily feed.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "feed",
        "feed": "all_day.geojson",
        "limit": 25
    }
)
```
### `USGSWaterData.fetch`

List USGS monitoring locations with a bounded result count.

```python
from fetchers import USGSWaterData

target = USGSWaterData()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="usgswater_data_fetch",
    description="List USGS monitoring locations with a bounded result count.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "monitoring-locations",
        "state_code": "US:51",
        "limit": 25
    }
)
```
### `USGSTheNationalMap.fetch`

List datasets exposed by The National Map.

```python
from fetchers import USGSTheNationalMap

target = USGSTheNationalMap()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="usgsthe_national_map_fetch",
    description="List datasets exposed by The National Map.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "datasets"
    }
)
```
### `USGSScienceBase.fetch`

Search ScienceBase items.

```python
from fetchers import USGSScienceBase

target = USGSScienceBase()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="usgsscience_base_fetch",
    description="Search ScienceBase items.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "items",
        "q": "climate change",
        "max_items": 25,
        "offset": 0
    }
)
```
### `AirNow.fetch`

Retrieve current air-quality observations by ZIP Code.

```python
from fetchers import AirNow

target = AirNow()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="air_now_fetch",
    description="Retrieve current air-quality observations by ZIP Code.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "current-zip",
        "zip_code": "22201",
        "distance": 25
    }
)
```

Configure the AirNow API key before execution.
### `ClimateData.fetch`

Search the climate dataset catalog.

```python
from fetchers import ClimateData

target = ClimateData()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="climate_data_fetch",
    description="Search the climate dataset catalog.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "datasets",
        "keyword": "temperature",
        "limit": 25,
        "offset": 0
    }
)
```

Configure the climate-data service token before execution when required.
### `EoNet.fetch`

Retrieve open natural-event records from EONET.

```python
from fetchers import EoNet

target = EoNet()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="eo_net_fetch",
    description="Retrieve open natural-event records from EONET.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "events",
        "status": "open",
        "limit": 25,
        "days": 30
    }
)
```
### `EnviroFacts.fetch`

Retrieve EPA Envirofacts TRI facility records for a state.

```python
from fetchers import EnviroFacts

target = EnviroFacts()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="enviro_facts_fetch",
    description="Retrieve EPA Envirofacts TRI facility records for a state.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "table_name": "TRI_FACILITY",
        "state_code": "VA",
        "limit": 25
    }
)
```
### `TidesAndCurrents.fetch`

Retrieve NOAA water-level observations for a station and date range.

```python
from fetchers import TidesAndCurrents

target = TidesAndCurrents()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="tides_and_currents_fetch",
    description="Retrieve NOAA water-level observations for a station and date range.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "water-level",
        "station_id": "8638610",
        "begin_date": "20260801",
        "end_date": "20260802",
        "datum": "MLLW",
        "units": "metric",
        "time_zone": "gmt"
    }
)
```
### `UvIndex.fetch`

Retrieve the daily ultraviolet-index forecast by ZIP Code.

```python
from fetchers import UvIndex

target = UvIndex()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="uv_index_fetch",
    description="Retrieve the daily ultraviolet-index forecast by ZIP Code.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "daily-zip",
        "zip_code": "22201"
    }
)
```
### `PurpleAir.fetch`

Retrieve PurpleAir sensors inside a geographic bounding box.

```python
from fetchers import PurpleAir

target = PurpleAir()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="purple_air_fetch",
    description="Retrieve PurpleAir sensors inside a geographic bounding box.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "sensors",
        "nwlng": -77.20,
        "nwlat": 39.00,
        "selng": -76.90,
        "selat": 38.75,
        "fields": "name,latitude,longitude,pm2.5"
    }
)
```

Configure the PurpleAir API key before execution.
### `OpenAQ.fetch`

Retrieve OpenAQ locations near a coordinate pair.

```python
from fetchers import OpenAQ

target = OpenAQ()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="open_aq_fetch",
    description="Retrieve OpenAQ locations near a coordinate pair.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "locations",
        "coordinates": "38.8816,-77.0910",
        "radius": 25000,
        "limit": 25,
        "page": 1
    }
)
```

Configure the OpenAQ API key before execution when required by the active endpoint.
### `Firms.fetch`

Retrieve recent NASA FIRMS fire detections for an area.

```python
from fetchers import Firms

target = Firms()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="firms_fetch",
    description="Retrieve recent NASA FIRMS fire detections for an area.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "area",
        "source": "VIIRS_SNPP_NRT",
        "area_coordinates": "-78,38,-76,40",
        "day_range": 1
    }
)
```

Configure the NASA FIRMS map key before execution.
### `OpenSky.fetch`

Retrieve aircraft states inside a geographic bounding box.

```python
from fetchers import OpenSky

target = OpenSky()

tool = ToolDef.from_method(
    target=target,
    method="fetch",
    name="open_sky_fetch",
    description="Retrieve aircraft states inside a geographic bounding box.",
    category="fetchers"
)

result = run_tool(
    tool=tool,
    arguments={
        "mode": "states_bbox",
        "lamin": 38.70,
        "lomin": -77.30,
        "lamax": 39.10,
        "lomax": -76.80,
        "extended": False
    }
)
```

Public access may be rate-limited; configure OpenSky OAuth client credentials outside model arguments when authenticated access is needed.
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
| Every loader class is documented       | Confirm all 29 loader class headings are present.                 |
| Every fetcher class is documented      | Confirm all 49 fetcher class headings are present.                |
| Manual docs contain no live directives | `Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"`     |
| API docs contain live directives       | `Select-String -Path .\docs\api\*.md -Pattern "^:::\s+[A-Za-z_]"` |
| Docs build                             | `mkdocs build`                                                    |


