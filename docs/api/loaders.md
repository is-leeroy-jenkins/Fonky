# API Reference: `loaders.py`

`loaders.py` contains document and cloud ingestion implementations for local text/structured files, Office formats, PDF, web content, repositories, cloud storage, email/Outlook, SharePoint, speech, and provider-backed loading.

## Module Inventory

- **Classes:** 29
- **Top-level functions:** 1

## Module-Level Functions

| Function | Signature | Purpose |
|---|---|---|
| `throw_if()` | `throw_if( name: str, value: object ) -> None` | Throw if. |

## Classes

| Class | Constructor | Public Methods | Functional Wrappers |
|---|---|---:|---:|
| [`Loader`](#loader) | `Loader( self: Any ) -> None` | 4 | 0 |
| [`TextLoader`](#textloader) | `TextLoader( self: Any ) -> None` | 2 | 1 |
| [`CsvLoader`](#csvloader) | `CsvLoader( self: Any ) -> None` | 2 | 1 |
| [`WebLoader`](#webloader) | `WebLoader( self: Any, recursive: bool = False, max_depth: int = 2, prevent_outside: bool = True, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> None` | 4 | 3 |
| [`PdfReader`](#pdfreader) | `PdfReader( self: Any ) -> None` | 2 | 1 |
| [`PdfLoader`](#pdfloader) | `PdfLoader( self: Any, size: int = 1000, overlap: int = 150, has_tables: bool = True, include: bool = True ) -> None` | 4 | 1 |
| [`ExcelLoader`](#excelloader) | `ExcelLoader( self: Any ) -> None` | 3 | 1 |
| [`WordLoader`](#wordloader) | `WordLoader( self: Any ) -> None` | 2 | 1 |
| [`MarkdownLoader`](#markdownloader) | `MarkdownLoader( self: Any ) -> None` | 2 | 1 |
| [`HtmlLoader`](#htmlloader) | `HtmlLoader( self: Any ) -> None` | 2 | 1 |
| [`ArXivLoader`](#arxivloader) | `ArXivLoader( self: Any ) -> None` | 2 | 1 |
| [`WikiLoader`](#wikiloader) | `WikiLoader( self: Any ) -> None` | 2 | 1 |
| [`GoogleDriveLoader`](#googledriveloader) | `GoogleDriveLoader( self: Any ) -> None` | 4 | 2 |
| [`OutlookLoader`](#outlookloader) | `OutlookLoader( self: Any ) -> None` | 2 | 1 |
| [`SpfxLoader`](#spfxloader) | `SpfxLoader( self: Any ) -> None` | 3 | 2 |
| [`PowerPointLoader`](#powerpointloader) | `PowerPointLoader( self: Any ) -> None` | 3 | 2 |
| [`OneDriveDocLoader`](#onedrivedocloader) | `OneDriveDocLoader( self: Any ) -> None` | 2 | 1 |
| [`EmailLoader`](#emailloader) | `EmailLoader( self: Any ) -> None` | 2 | 1 |
| [`JsonLoader`](#jsonloader) | `JsonLoader( self: Any ) -> None` | 2 | 1 |
| [`GithubLoader`](#githubloader) | `GithubLoader( self: Any ) -> None` | 2 | 1 |
| [`XmlLoader`](#xmlloader) | `XmlLoader( self: Any ) -> None` | 4 | 2 |
| [`PubMedSearchLoader`](#pubmedsearchloader) | `PubMedSearchLoader( self: Any ) -> None` | 2 | 1 |
| [`OpenCityLoader`](#opencityloader) | `OpenCityLoader( self: Any ) -> None` | 2 | 1 |
| [`JupyterNotebookLoader`](#jupyternotebookloader) | `JupyterNotebookLoader( self: Any ) -> None` | 2 | 1 |
| [`GoogleCloudFileLoader`](#googlecloudfileloader) | `GoogleCloudFileLoader( self: Any ) -> None` | 2 | 1 |
| [`AwsFileLoader`](#awsfileloader) | `AwsFileLoader( self: Any ) -> None` | 2 | 1 |
| [`GoogleSpeechToTextLoader`](#googlespeechtotextloader) | `GoogleSpeechToTextLoader( self: Any ) -> None` | 2 | 1 |
| [`GoogleBucketLoader`](#googlebucketloader) | `GoogleBucketLoader( self: Any ) -> None` | 2 | 1 |
| [`AwsBucketLoader`](#awsbucketloader) | `AwsBucketLoader( self: Any ) -> None` | 2 | 1 |

## `Loader`

Loader document loader wrapper.

```python
Loader( self: Any ) -> None
```

**Source:** `loaders.py`, line 128

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `verify_exists()` | `verify_exists( self: Any, path: str ) -> str \| None` | Validate a local file path. |
| `resolve_paths()` | `resolve_paths( self: Any, pattern: str ) -> List[str] \| None` | Resolve file paths or glob patterns. |
| `load_documents()` | `load_documents( self: Any, path: str, encoding: Optional[str], csv_args: Optional[Dict[str, Any]], source_column: Optional[str] ) -> List[Document] \| None` | Load CSV-style documents. |
| `split_documents()` | `split_documents( self: Any, docs: List[Document], chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split document collections. |

## `TextLoader`

TextLoader document loader wrapper.

```python
TextLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 325

**Functional wrappers:** `fonky.load_text()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, path: str, encoding: Optional[str] = None ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `CsvLoader`

CsvLoader document loader wrapper.

```python
CsvLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 455

**Functional wrappers:** `fonky.load_csv()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, path: str, encoding: Optional[str] = 'utf-8', source_column: Optional[str] = None, delimiter: str = ',', quotechar: str = '"' ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `WebLoader`

WebLoader document loader wrapper.

```python
WebLoader( self: Any, recursive: bool = False, max_depth: int = 2, prevent_outside: bool = True, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> None
```

**Source:** `loaders.py`, line 589

**Functional wrappers:** `fonky.load_web()`, `fonky.load_web_recursive()`, `fonky.load_web_pages()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, urls: str \| List[str] ) -> List[Document] \| None` | Load source content. |
| `load_recursive()` | `load_recursive( self: Any, url: str, depth: int = 2, max_time: int = 10, ignore: bool = True ) -> List[Document] \| None` | Load web documents recursively. |
| `load_pages()` | `load_pages( self: Any, urls: List[str], depth: int = 2, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> List[Document] \| None` | Load static web pages. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `PdfReader`

PdfReader document loader wrapper.

```python
PdfReader( self: Any ) -> None
```

**Source:** `loaders.py`, line 884

**Functional wrappers:** `fonky.read_pdf()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, path: str, mode: str = 'single' ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `PdfLoader`

PdfLoader document loader wrapper.

```python
PdfLoader( self: Any, size: int = 1000, overlap: int = 150, has_tables: bool = True, include: bool = True ) -> None
```

**Source:** `loaders.py`, line 1004

**Functional wrappers:** `fonky.load_pdf()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `mode_options()` | `mode_options( self: Any ) -> List[str]` | Return loading mode options. |
| `extraction_options()` | `extraction_options( self: Any ) -> List[str]` | Return PDF extraction options. |
| `image_options()` | `image_options( self: Any ) -> List[str]` | Return PDF image output options. |
| `load()` | `load( self: Any, path: str, mode: str = 'single', extract: str = 'plain', include: bool = False, format: str = 'markdown-img' ) -> List[Document]` | Load source content. |

## `ExcelLoader`

ExcelLoader document loader wrapper.

```python
ExcelLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 1163

**Functional wrappers:** `fonky.load_excel()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `mode_options()` | `mode_options( self: Any ) -> List[str]` | Return loading mode options. |
| `load()` | `load( self: Any, path: str, mode: str = 'elements', has_headers: bool = True ) -> List[Document]` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `WordLoader`

WordLoader document loader wrapper.

```python
WordLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 1297

**Functional wrappers:** `fonky.load_word()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, path: str ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `MarkdownLoader`

MarkdownLoader document loader wrapper.

```python
MarkdownLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 1407

**Functional wrappers:** `fonky.load_markdown()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, path: str ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `HtmlLoader`

HtmlLoader document loader wrapper.

```python
HtmlLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 1515

**Functional wrappers:** `fonky.load_html()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, path: str ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `ArXivLoader`

ArXivLoader document loader wrapper.

```python
ArXivLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 1625

**Functional wrappers:** `fonky.load_arxiv()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, question: str ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `WikiLoader`

WikiLoader document loader wrapper.

```python
WikiLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 1747

**Functional wrappers:** `fonky.load_wikipedia()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, question: str ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `GoogleDriveLoader`

GoogleDriveLoader document loader wrapper.

```python
GoogleDriveLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 1872

**Functional wrappers:** `fonky.load_google_drive_file()`, `fonky.load_google_drive_folder()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `file_options()` | `file_options( self: Any ) -> List[str]` | Return Google Drive file options. |
| `load_file()` | `load_file( self: Any, file_id: str, recursive: bool = False ) -> List[Document] \| None` | Load a provider file. |
| `load_folder()` | `load_folder( self: Any, folder_id: str, recursive: bool = False ) -> List[Document] \| None` | Load provider folder content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `OutlookLoader`

OutlookLoader document loader wrapper.

```python
OutlookLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 2044

**Functional wrappers:** `fonky.load_outlook()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, path: str ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `SpfxLoader`

SpfxLoader document loader wrapper.

```python
SpfxLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 2162

**Functional wrappers:** `fonky.load_spfx()`, `fonky.load_spfx_folder()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, library_id: str ) -> List[Document] \| None` | Load source content. |
| `load_folder()` | `load_folder( self: Any, library_id: str, folder_id: str ) -> List[Document] \| None` | Load provider folder content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `PowerPointLoader`

PowerPointLoader document loader wrapper.

```python
PowerPointLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 2328

**Functional wrappers:** `fonky.load_powerpoint()`, `fonky.load_powerpoint_multiple()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, path: str, mode: str = 'single' ) -> List[Document] \| None` | Load source content. |
| `load_multiple()` | `load_multiple( self: Any, path: str ) -> List[Document] \| None` | Load multiple presentation elements. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `OneDriveDocLoader`

OneDriveDocLoader document loader wrapper.

```python
OneDriveDocLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 2477

**Functional wrappers:** `fonky.load_onedrive()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, drive_id: str, folder_path: Optional[str] = None, object_ids: Optional[List[str]] = None, auth_with_token: bool = True ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `EmailLoader`

EmailLoader document loader wrapper.

```python
EmailLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 2616

**Functional wrappers:** `fonky.load_email()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, path: str, mode: str = 'single', attachments: bool = True ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `JsonLoader`

JsonLoader document loader wrapper.

```python
JsonLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 2735

**Functional wrappers:** `fonky.load_json()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, filepath: str, is_text: bool = True, is_lines: bool = False ) -> List[Document]` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `GithubLoader`

GithubLoader document loader wrapper.

```python
GithubLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 2860

**Functional wrappers:** `fonky.load_github()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, url: str, repo: str, branch: str, filetype: str = '.md' ) -> List[Document]` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `XmlLoader`

XmlLoader document loader wrapper.

```python
XmlLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 3007

**Functional wrappers:** `fonky.load_xml()`, `fonky.load_xml_tree()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, filepath: str ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, size: int = 1000, amount: int = 200 ) -> List[Document] \| None` | Split loaded documents. |
| `load_tree()` | `load_tree( self: Any, filepath: str ) -> etree._ElementTree \| None` | Parse an XML element tree. |
| `get_elements()` | `get_elements( self: Any, xpath: str ) -> List[etree._Element] \| None` | Return XML elements by XPath. |

## `PubMedSearchLoader`

PubMedSearchLoader document loader wrapper.

```python
PubMedSearchLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 3200

**Functional wrappers:** `fonky.load_pubmed()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, query: str, max_docs: int = 5 ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `OpenCityLoader`

OpenCityLoader document loader wrapper.

```python
OpenCityLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 3311

**Functional wrappers:** `fonky.load_open_city()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, city_id: str, dataset_id: str, limit: int = 100 ) -> List[Document]` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document]` | Split loaded documents. |

## `JupyterNotebookLoader`

JupyterNotebookLoader document loader wrapper.

```python
JupyterNotebookLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 3437

**Functional wrappers:** `fonky.load_jupyter_notebook()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, path: str, include_outputs: bool = False, max_output_length: int = 10, remove_newline: bool = False, traceback: bool = False ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `GoogleCloudFileLoader`

GoogleCloudFileLoader document loader wrapper.

```python
GoogleCloudFileLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 3567

**Functional wrappers:** `fonky.load_google_cloud_file()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, project_name: str, bucket: str, blob: str ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `AwsFileLoader`

AwsFileLoader document loader wrapper.

```python
AwsFileLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 3688

**Functional wrappers:** `fonky.load_aws_file()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, bucket: str, key: str, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `GoogleSpeechToTextLoader`

GoogleSpeechToTextLoader document loader wrapper.

```python
GoogleSpeechToTextLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 3836

**Functional wrappers:** `fonky.load_google_speech_to_text()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, project_id: str, file_path: str, config: Optional[Dict[str, Any]] = None ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `GoogleBucketLoader`

GoogleBucketLoader document loader wrapper.

```python
GoogleBucketLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 3969

**Functional wrappers:** `fonky.load_google_bucket()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, project_name: str, bucket: str, prefix: Optional[str] = None, continue_on_failure: bool = False ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |

## `AwsBucketLoader`

AwsBucketLoader document loader wrapper.

```python
AwsBucketLoader( self: Any ) -> None
```

**Source:** `loaders.py`, line 4099

**Functional wrappers:** `fonky.load_aws_bucket()`

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( self: Any, bucket: str, prefix: Optional[str] = None, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None, endpoint_url: Optional[str] = None ) -> List[Document] \| None` | Load source content. |
| `split()` | `split( self: Any, chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. |
