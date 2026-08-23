# API — `loaders.py`

| Class | Public methods | Purpose |
|---|---:|---|
| `Loader` | 4 | Loader document loader wrapper. Provides shared path validation, path expansion, document loading support, and document splitting behavior used by concrete LangChain loader wrappers. |
| `TextLoader` | 2 | TextLoader document loader wrapper. Loads local plain-text files into LangChain Document objects and prepares those documents for chunking workflows. |
| `CsvLoader` | 2 | CsvLoader document loader wrapper. Loads comma-separated or delimiter-separated files into LangChain Document objects with configurable encoding, source-column, delimiter, and quote-character behavior. |
| `WebLoader` | 4 | WebLoader document loader wrapper. Loads documents from one or more web pages, with optional recursive URL traversal and same-domain filtering for bounded web ingestion workflows. |
| `PdfReader` | 2 | PdfReader document loader wrapper. Loads PDF files with PyPDFLoader and provides a base PDF reading path for simpler page or single-document extraction workflows. |
| `PdfLoader` | 4 | PdfLoader document loader wrapper. Extends PDF loading with extraction-mode, image-inclusion, image-format, and chunk-size settings for richer PDF ingestion workflows. |
| `ExcelLoader` | 3 | ExcelLoader document loader wrapper. Loads Excel workbooks through the unstructured Excel loader and exposes the loaded workbook content as LangChain Document objects. |
| `WordLoader` | 2 | WordLoader document loader wrapper. Loads Microsoft Word documents through Docx2txtLoader and returns the extracted document text as LangChain Document objects. |
| `MarkdownLoader` | 2 | MarkdownLoader document loader wrapper. Loads local Markdown files with the unstructured Markdown loader and returns parsed content as LangChain Document objects. |
| `HtmlLoader` | 2 | HtmlLoader document loader wrapper. Loads local HTML files with the unstructured HTML loader and returns parsed page content as LangChain Document objects. |
| `ArXivLoader` | 2 | ArXivLoader document loader wrapper. Queries ArXiv through the LangChain ArxivLoader and returns scholarly search results as LangChain Document objects. |
| `WikiLoader` | 2 | WikiLoader document loader wrapper. Queries Wikipedia through the LangChain WikipediaLoader and returns encyclopedia search results as LangChain Document objects. |
| `GoogleDriveLoader` | 4 | GoogleDriveLoader document loader wrapper. Loads files or folders from Google Drive through the Google Drive loader and returns accessible Drive content as LangChain Document objects. |
| `OutlookLoader` | 2 | OutlookLoader document loader wrapper. Loads Outlook message files and returns their email content as LangChain Document objects. |
| `SpfxLoader` | 3 | SpfxLoader document loader wrapper. Loads SharePoint document-library content through the SharePoint loader, including full-library and folder-scoped retrieval paths. |
| `PowerPointLoader` | 3 | PowerPointLoader document loader wrapper. Loads PowerPoint presentation files through the unstructured PowerPoint loader and returns slide content as LangChain Document objects. |
| `OneDriveDocLoader` | 2 | OneDriveDocLoader document loader wrapper. Loads OneDrive document content by drive, folder path, or object identifiers through the OneDrive loader. |
| `EmailLoader` | 2 | EmailLoader document loader wrapper. Loads email files through the unstructured email loader, including optional attachment processing. |
| `JsonLoader` | 2 | JsonLoader document loader wrapper. Loads JSON or JSON Lines files through JSONLoader using the configured jq schema and text-content settings. |
| `GithubLoader` | 2 | GithubLoader document loader wrapper. Loads repository files through GithubFileLoader using a repository, branch, GitHub API URL, and file-extension filter. |
| `XmlLoader` | 4 | XmlLoader document loader wrapper. Loads XML files as both unstructured documents and parsed element trees for XPath-based extraction workflows. |
| `PubMedSearchLoader` | 2 | PubMedSearchLoader document loader wrapper. Queries PubMed through the LangChain PubMed loader and returns biomedical literature results as LangChain Document objects. |
| `OpenCityLoader` | 2 | OpenCityLoader document loader wrapper. Loads open city dataset records through OpenCityDataLoader and returns civic dataset content as LangChain Document objects. |
| `JupyterNotebookLoader` | 2 | JupyterNotebookLoader document loader wrapper. Loads Jupyter notebooks through NotebookLoader with configurable output, traceback, newline, and output-length handling. |
| `GoogleCloudFileLoader` | 2 | GoogleCloudFileLoader document loader wrapper. Loads a single Google Cloud Storage blob through GCSFileLoader and returns the object content as LangChain Document objects. |
| `AwsFileLoader` | 2 | AwsFileLoader document loader wrapper. Loads a single Amazon S3 object through S3FileLoader with optional AWS credential and region settings. |
| `GoogleSpeechToTextLoader` | 2 | GoogleSpeechToTextLoader document loader wrapper. Loads audio transcription output through SpeechToTextLoader using a Google Cloud project, file path, and optional recognition configuration. |
| `GoogleBucketLoader` | 2 | GoogleBucketLoader document loader wrapper. Loads Google Cloud Storage bucket directories through GCSDirectoryLoader with optional prefix and failure-continuation behavior. |
| `AwsBucketLoader` | 2 | AwsBucketLoader document loader wrapper. Loads Amazon S3 bucket directories through S3DirectoryLoader with optional prefix, credentials, region, and endpoint settings. |

## `Loader`

Loader document loader wrapper. Provides shared path validation, path expansion, document loading support, and document splitting behavior used by concrete LangChain loader wrappers.

| Method | Signature | Purpose |
|---|---|---|
| `verify_exists()` | `verify_exists( path: str ) -> str \| None` | Validate a local file path. Validates that a supplied local path points to an existing file before a loader attempts to read it. The method stores the verified path on the instance and returns the normalized path for subsequent loader construction. str \| None: Validated or generated string value. Error: Re-raised after the original exception is wrapped and written to the application logger. FileNotFoundError: Raised when a local file path or pattern does not resolve to an existing file. |
| `resolve_paths()` | `resolve_paths( pattern: str ) -> List[str] \| None` | Resolve file paths or glob patterns. Expands a direct file path or glob pattern into concrete existing files. The method records candidate and resolved paths so batch-oriented loaders can operate on verified filesystem inputs. List[str] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. FileNotFoundError: Raised when a local file path or pattern does not resolve to an existing file. |
| `load_documents()` | `load_documents( path: str, encoding: Optional[str], csv_args: Optional[Dict[str, Any]], source_column: Optional[str] ) -> List[Document] \| None` | Load CSV-style documents. Loads CSV-style source content into LangChain Document objects using the configured path, encoding, CSV options, and source-column settings. The method stores the active loader and loaded documents for downstream splitting. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split_documents()` | `split_documents( docs: List[Document], chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split document collections. Splits a supplied list of LangChain Document objects into smaller chunks using RecursiveCharacterTextSplitter. The method stores chunking settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `TextLoader`

TextLoader document loader wrapper. Loads local plain-text files into LangChain Document objects and prepares those documents for chunking workflows.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( path: str, encoding: Optional[str] = None ) -> List[Document] \| None` | Load source content. Loads a local text file into LangChain Document objects. The method validates the path, applies the optional encoding, constructs TextDocLoader, stores the loader state, and returns loaded text documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `CsvLoader`

CsvLoader document loader wrapper. Loads comma-separated or delimiter-separated files into LangChain Document objects with configurable encoding, source-column, delimiter, and quote-character behavior.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( path: str, encoding: Optional[str] = 'utf-8', source_column: Optional[str] = None, delimiter: str = ',', quotechar: str = '"' ) -> List[Document] \| None` | Load source content. Loads a CSV file into LangChain Document objects. The method validates the file path, builds CSV parsing options from delimiter and quote-character settings, records optional source-column metadata, and returns the parsed rows as documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `WebLoader`

WebLoader document loader wrapper. Loads documents from one or more web pages, with optional recursive URL traversal and same-domain filtering for bounded web ingestion workflows.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( urls: str \| List[str] ) -> List[Document] \| None` | Load source content. Loads web content from one or more URLs. The method chooses between recursive crawling and static page loading based on instance configuration, stores request state, and returns the loaded web documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. ValueError: Raised when a required value is missing, blank, or outside the supported range. |
| `load_recursive()` | `load_recursive( url: str, depth: int = 2, max_time: int = 10, ignore: bool = True ) -> List[Document] \| None` | Load web documents recursively. Recursively loads documents from a seed URL using RecursiveUrlLoader. The method records crawl settings, loads reachable content to the configured depth, and optionally filters results to the original domain. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `load_pages()` | `load_pages( urls: List[str], depth: int = 2, timeout: int = 10, ignore: bool = True, progress: bool = True ) -> List[Document] \| None` | Load static web pages. Loads one or more static web pages through WebBaseLoader. The method records the URL list and request settings before returning the loaded page documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. ValueError: Raised when a required value is missing, blank, or outside the supported range. |

## `PdfReader`

PdfReader document loader wrapper. Loads PDF files with PyPDFLoader and provides a base PDF reading path for simpler page or single-document extraction workflows.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( path: str, mode: str = 'single' ) -> List[Document] \| None` | Load source content. Loads a PDF file through PyPDFLoader using the requested mode. The method validates the file path, stores the extraction mode, constructs the loader, and returns PDF page or single-document output. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `PdfLoader`

PdfLoader document loader wrapper. Extends PDF loading with extraction-mode, image-inclusion, image-format, and chunk-size settings for richer PDF ingestion workflows.

| Method | Signature | Purpose |
|---|---|---|
| `mode_options()` | `mode_options(  ) -> List[str]` | Return loading mode options. Returns the supported loading mode names exposed by the wrapper. These values can be used by UIs, examples, and validation logic to keep selectable options aligned with the active loader. List[str]: Loaded or split LangChain Document objects. |
| `extraction_options()` | `extraction_options(  ) -> List[str]` | Return PDF extraction options. Returns the supported PDF extraction mode names. The values identify how PyPDFLoader should parse text from the source PDF. List[str]: Loaded or split LangChain Document objects. |
| `image_options()` | `image_options(  ) -> List[str]` | Return PDF image output options. Returns the supported image-output formats used when PDF image extraction is enabled. The values control how extracted image references are embedded in document content. List[str]: Loaded or split LangChain Document objects. |
| `load()` | `load( path: str, mode: str = 'single', extract: str = 'plain', include: bool = False, format: str = 'markdown-img' ) -> List[Document]` | Load source content. Loads a PDF file with configurable text extraction and optional image extraction. The method validates the path, configures PyPDFLoader options, falls back to text-only loading when image parsing fails, and returns loaded PDF documents. List[Document]: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `ExcelLoader`

ExcelLoader document loader wrapper. Loads Excel workbooks through the unstructured Excel loader and exposes the loaded workbook content as LangChain Document objects.

| Method | Signature | Purpose |
|---|---|---|
| `mode_options()` | `mode_options(  ) -> List[str]` | Return loading mode options. Returns the supported loading mode names exposed by the wrapper. These values can be used by UIs, examples, and validation logic to keep selectable options aligned with the active loader. List[str]: Loaded or split LangChain Document objects. |
| `load()` | `load( path: str, mode: str = 'elements', has_headers: bool = True ) -> List[Document]` | Load source content. Loads an Excel workbook into LangChain Document objects. The method validates the path, stores workbook parsing settings, constructs UnstructuredExcelLoader, and returns extracted workbook content. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped & written to the logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. ValueError: Raised when a required value is missing, blank, or outside the supported range. |

## `WordLoader`

WordLoader document loader wrapper. Loads Microsoft Word documents through Docx2txtLoader and returns the extracted document text as LangChain Document objects.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( path: str ) -> List[Document] \| None` | Load source content. Loads a Word document into LangChain Document objects. The method validates the local path, constructs Docx2txtLoader, and returns extracted document text. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. ValueError: Raised when a required value is missing, blank, or outside the supported range. |

## `MarkdownLoader`

MarkdownLoader document loader wrapper. Loads local Markdown files with the unstructured Markdown loader and returns parsed content as LangChain Document objects.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( path: str ) -> List[Document] \| None` | Load source content. Loads a Markdown file into LangChain Document objects. The method validates the path, constructs UnstructuredMarkdownLoader, and returns parsed Markdown content. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `HtmlLoader`

HtmlLoader document loader wrapper. Loads local HTML files with the unstructured HTML loader and returns parsed page content as LangChain Document objects.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( path: str ) -> List[Document] \| None` | Load source content. Loads a local HTML file into LangChain Document objects. The method validates the path, constructs UnstructuredHTMLLoader, and returns extracted HTML content. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. ValueError: Raised when a required value is missing, blank, or outside the supported range. |

## `ArXivLoader`

ArXivLoader document loader wrapper. Queries ArXiv through the LangChain ArxivLoader and returns scholarly search results as LangChain Document objects.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( question: str ) -> List[Document] \| None` | Load source content. Runs an ArXiv query and loads matching scholarly records as LangChain Document objects. The method stores the query, configures the ArxivLoader character limit, and returns the retrieved documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `WikiLoader`

WikiLoader document loader wrapper. Queries Wikipedia through the LangChain WikipediaLoader and returns encyclopedia search results as LangChain Document objects.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( question: str ) -> List[Document] \| None` | Load source content. Runs a Wikipedia query and loads matching encyclopedia records as LangChain Document objects. The method stores the query and retrieval limits before returning the retrieved documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `GoogleDriveLoader`

GoogleDriveLoader document loader wrapper. Loads files or folders from Google Drive through the Google Drive loader and returns accessible Drive content as LangChain Document objects.

| Method | Signature | Purpose |
|---|---|---|
| `file_options()` | `file_options(  ) -> List[str]` | Return Google Drive file options. Returns the supported Google Drive file target names exposed by the wrapper. These values describe the Drive-backed file categories expected by the loader workflow. List[str]: Loaded or split LangChain Document objects. |
| `load_file()` | `load_file( file_id: str, recursive: bool = False ) -> List[Document] \| None` | Load a provider file. Loads a single provider-backed file into LangChain Document objects. The method stores the selected file identifier and recursion flag before constructing the backing loader. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `load_folder()` | `load_folder( folder_id: str, recursive: bool = False ) -> List[Document] \| None` | Load provider folder content. Loads documents from a provider folder or document-library folder. The method records the folder identifiers, constructs the backing loader, and returns the loaded documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `OutlookLoader`

OutlookLoader document loader wrapper. Loads Outlook message files and returns their email content as LangChain Document objects.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( path: str ) -> List[Document] \| None` | Load source content. Loads an Outlook message file into LangChain Document objects. The method validates the local message path, constructs OutlookMessageLoader, and returns extracted email content. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `SpfxLoader`

SpfxLoader document loader wrapper. Loads SharePoint document-library content through the SharePoint loader, including full-library and folder-scoped retrieval paths.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( library_id: str ) -> List[Document] \| None` | Load source content. Loads SharePoint document-library content into LangChain Document objects. The method records library or folder identifiers, configures SharePointLoader, and returns retrieved documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `load_folder()` | `load_folder( library_id: str, folder_id: str ) -> List[Document] \| None` | Load provider folder content. Loads documents from a provider folder or document-library folder. The method records the folder identifiers, constructs the backing loader, and returns the loaded documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `PowerPointLoader`

PowerPointLoader document loader wrapper. Loads PowerPoint presentation files through the unstructured PowerPoint loader and returns slide content as LangChain Document objects.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( path: str, mode: str = 'single' ) -> List[Document] \| None` | Load source content. Loads a PowerPoint file into LangChain Document objects. The method validates the path, sets the extraction mode, constructs UnstructuredPowerPointLoader, and returns slide content. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `load_multiple()` | `load_multiple( path: str ) -> List[Document] \| None` | Load multiple presentation elements. Loads PowerPoint content using the loader mode intended for multiple-document or multi-element extraction. The method validates the file path and stores the loaded presentation documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `OneDriveDocLoader`

OneDriveDocLoader document loader wrapper. Loads OneDrive document content by drive, folder path, or object identifiers through the OneDrive loader.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( drive_id: str, folder_path: Optional[str] = None, object_ids: Optional[List[str]] = None, auth_with_token: bool = True ) -> List[Document] \| None` | Load source content. Loads OneDrive documents by drive identifier, folder path, or object identifiers. The method builds loader keyword arguments from optional inputs, constructs OneDriveLoader, and returns loaded documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `EmailLoader`

EmailLoader document loader wrapper. Loads email files through the unstructured email loader, including optional attachment processing.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( path: str, mode: str = 'single', attachments: bool = True ) -> List[Document] \| None` | Load source content. Loads an email file into LangChain Document objects. The method validates the path, configures email mode and attachment handling, constructs UnstructuredEmailLoader, and returns parsed email content. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `JsonLoader`

JsonLoader document loader wrapper. Loads JSON or JSON Lines files through JSONLoader using the configured jq schema and text-content settings.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( filepath: str, is_text: bool = True, is_lines: bool = False ) -> List[Document]` | Load source content. Loads JSON content into LangChain Document objects using the configured jq schema. The method validates the file path, records JSON parsing flags, constructs JSONLoader, and returns extracted document content. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. ValueError: Raised when a required value is missing, blank, or outside the supported range. |

## `GithubLoader`

GithubLoader document loader wrapper. Loads repository files through GithubFileLoader using a repository, branch, GitHub API URL, and file-extension filter.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( url: str, repo: str, branch: str, filetype: str = '.md' ) -> List[Document]` | Load source content. Loads files from a GitHub repository through GithubFileLoader. The method records repository, branch, API URL, and file-extension filter values before returning matching repository documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. ValueError: Raised when a required value is missing, blank, or outside the supported range. |

## `XmlLoader`

XmlLoader document loader wrapper. Loads XML files as both unstructured documents and parsed element trees for XPath-based extraction workflows.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( filepath: str ) -> List[Document] \| None` | Load source content. Loads an XML file through UnstructuredXMLLoader and returns parsed XML content as LangChain Document objects. The method validates the path, constructs the loader, and stores loaded documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( size: int = 1000, amount: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. ValueError: Raised when a required value is missing, blank, or outside the supported range. |
| `load_tree()` | `load_tree( filepath: str ) -> etree._ElementTree \| None` | Parse an XML element tree. Parses a local XML file into an lxml element tree with recovery enabled. The method stores the tree, root element, and namespace mapping for later XPath extraction. etree._ElementTree \| None: Parsed XML element tree. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `get_elements()` | `get_elements( xpath: str ) -> List[etree._Element] \| None` | Return XML elements by XPath. Runs an XPath expression against the previously loaded XML root element. The method uses stored namespace metadata and returns matching lxml elements as a list. List[etree._Element] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. ValueError: Raised when a required value is missing, blank, or outside the supported range. |

## `PubMedSearchLoader`

PubMedSearchLoader document loader wrapper. Queries PubMed through the LangChain PubMed loader and returns biomedical literature results as LangChain Document objects.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( query: str, max_docs: int = 5 ) -> List[Document] \| None` | Load source content. Runs a PubMed query and loads matching biomedical literature records as LangChain Document objects. The method records the query and maximum result count before returning retrieved documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `OpenCityLoader`

OpenCityLoader document loader wrapper. Loads open city dataset records through OpenCityDataLoader and returns civic dataset content as LangChain Document objects.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( city_id: str, dataset_id: str, limit: int = 100 ) -> List[Document]` | Load source content. Loads records from an open city dataset into LangChain Document objects. The method validates city and dataset identifiers, enforces a positive limit, constructs OpenCityDataLoader, and returns dataset documents. List[Document]: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. ValueError: Raised when a required value is missing, blank, or outside the supported range. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document]` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document]: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `JupyterNotebookLoader`

JupyterNotebookLoader document loader wrapper. Loads Jupyter notebooks through NotebookLoader with configurable output, traceback, newline, and output-length handling.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( path: str, include_outputs: bool = False, max_output_length: int = 10, remove_newline: bool = False, traceback: bool = False ) -> List[Document] \| None` | Load source content. Loads a Jupyter notebook into LangChain Document objects. The method validates the notebook path, records output and traceback settings, constructs NotebookLoader, and returns notebook content. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `GoogleCloudFileLoader`

GoogleCloudFileLoader document loader wrapper. Loads a single Google Cloud Storage blob through GCSFileLoader and returns the object content as LangChain Document objects.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( project_name: str, bucket: str, blob: str ) -> List[Document] \| None` | Load source content. Loads a single Google Cloud Storage blob into LangChain Document objects. The method validates project, bucket, and blob values, constructs GCSFileLoader, and returns loaded object content. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `AwsFileLoader`

AwsFileLoader document loader wrapper. Loads a single Amazon S3 object through S3FileLoader with optional AWS credential and region settings.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( bucket: str, key: str, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None ) -> List[Document] \| None` | Load source content. Loads a single Amazon S3 object into LangChain Document objects. The method validates bucket and key values, applies optional AWS credentials and region settings, constructs S3FileLoader, and returns object content. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `GoogleSpeechToTextLoader`

GoogleSpeechToTextLoader document loader wrapper. Loads audio transcription output through SpeechToTextLoader using a Google Cloud project, file path, and optional recognition configuration.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( project_id: str, file_path: str, config: Optional[Dict[str, Any]] = None ) -> List[Document] \| None` | Load source content. Loads speech-to-text transcription output into LangChain Document objects. The method validates project and file values, applies optional recognition configuration, constructs SpeechToTextLoader, and returns transcription documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `GoogleBucketLoader`

GoogleBucketLoader document loader wrapper. Loads Google Cloud Storage bucket directories through GCSDirectoryLoader with optional prefix and failure-continuation behavior.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( project_name: str, bucket: str, prefix: Optional[str] = None, continue_on_failure: bool = False ) -> List[Document] \| None` | Load source content. Loads a Google Cloud Storage bucket directory into LangChain Document objects. The method validates project and bucket values, applies optional prefix and failure-continuation settings, constructs GCSDirectoryLoader, and returns loaded bucket documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |

## `AwsBucketLoader`

AwsBucketLoader document loader wrapper. Loads Amazon S3 bucket directories through S3DirectoryLoader with optional prefix, credentials, region, and endpoint settings.

| Method | Signature | Purpose |
|---|---|---|
| `load()` | `load( bucket: str, prefix: Optional[str] = None, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, aws_session_token: Optional[str] = None, region_name: Optional[str] = None, endpoint_url: Optional[str] = None ) -> List[Document] \| None` | Load source content. Loads an Amazon S3 bucket directory into LangChain Document objects. The method validates bucket input, applies optional prefix, credential, region, and endpoint settings, constructs S3DirectoryLoader, and returns loaded bucket documents. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
| `split()` | `split( chunk: int = 1000, overlap: int = 200 ) -> List[Document] \| None` | Split loaded documents. Splits the documents currently stored on the loader into smaller LangChain Document chunks. The method records chunk size and overlap settings before returning chunked documents for retrieval, embedding, or analysis workflows. List[Document] \| None: Loaded or split LangChain Document objects. Error: Re-raised after the original exception is wrapped and written to the application logger. |
