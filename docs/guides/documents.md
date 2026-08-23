# Documents

Local and structured document ingestion for text, CSV, XML, PDF, Markdown, HTML, JSON, PowerPoint, Excel, Word, email, Outlook, SharePoint, notebooks, and related formats.

## Functional Operations

| Function | Signature | Purpose |
|---|---|---|
| `load_text()` | `load_text( path: str, encoding: Optional[str] = None ) -> Any` | Load source content. Provides direct module-level access to ``TextLoader.load`` using a fresh ``TextLoader`` instance. Any: Value returned by ``TextLoader.load``. |
| `load_csv()` | `load_csv( path: str, encoding: Optional[str] = 'utf-8', source_column: Optional[str] = None, delimiter: str = ',', quotechar: str = '"' ) -> Any` | Load source content. Provides direct module-level access to ``CsvLoader.load`` using a fresh ``CsvLoader`` instance. Any: Value returned by ``CsvLoader.load``. |
| `read_pdf()` | `read_pdf( path: str, mode: str = 'single' ) -> Any` | Load source content. Provides direct module-level access to ``PdfReader.load`` using a fresh ``PdfReader`` instance. Any: Value returned by ``PdfReader.load``. |
| `load_pdf()` | `load_pdf( path: str, mode: str = 'single', extract: str = 'plain', include: bool = False, format: str = 'markdown-img', size: int = 1000, overlap: int = 150, has_tables: bool = True ) -> Any` | Load source content. Provides direct module-level access to ``PdfLoader.load`` using a fresh ``PdfLoader`` instance. Any: Value returned by ``PdfLoader.load``. |
| `load_excel()` | `load_excel( path: str, mode: str = 'elements', has_headers: bool = True ) -> Any` | Load source content. Provides direct module-level access to ``ExcelLoader.load`` using a fresh ``ExcelLoader`` instance. Any: Value returned by ``ExcelLoader.load``. |
| `load_word()` | `load_word( path: str ) -> Any` | Load source content. Provides direct module-level access to ``WordLoader.load`` using a fresh ``WordLoader`` instance. Any: Value returned by ``WordLoader.load``. |
| `load_markdown()` | `load_markdown( path: str ) -> Any` | Load source content. Provides direct module-level access to ``MarkdownLoader.load`` using a fresh ``MarkdownLoader`` instance. Any: Value returned by ``MarkdownLoader.load``. |
| `load_html()` | `load_html( path: str ) -> Any` | Load source content. Provides direct module-level access to ``HtmlLoader.load`` using a fresh ``HtmlLoader`` instance. Any: Value returned by ``HtmlLoader.load``. |
| `load_outlook()` | `load_outlook( path: str ) -> Any` | Load source content. Provides direct module-level access to ``OutlookLoader.load`` using a fresh ``OutlookLoader`` instance. Any: Value returned by ``OutlookLoader.load``. |
| `load_spfx()` | `load_spfx( library_id: str ) -> Any` | Load source content. Provides direct module-level access to ``SpfxLoader.load`` using a fresh ``SpfxLoader`` instance. Any: Value returned by ``SpfxLoader.load``. |
| `load_spfx_folder()` | `load_spfx_folder( library_id: str, folder_id: str ) -> Any` | Load provider folder content. Provides direct module-level access to ``SpfxLoader.load_folder`` using a fresh ``SpfxLoader`` instance. Any: Value returned by ``SpfxLoader.load_folder``. |
| `load_powerpoint()` | `load_powerpoint( path: str, mode: str = 'single' ) -> Any` | Load source content. Provides direct module-level access to ``PowerPointLoader.load`` using a fresh ``PowerPointLoader`` instance. Any: Value returned by ``PowerPointLoader.load``. |
| `load_powerpoint_multiple()` | `load_powerpoint_multiple( path: str ) -> Any` | Load multiple presentation elements. Provides direct module-level access to ``PowerPointLoader.load_multiple`` using a fresh ``PowerPointLoader`` instance. Any: Value returned by ``PowerPointLoader.load_multiple``. |
| `load_email()` | `load_email( path: str, mode: str = 'single', attachments: bool = True ) -> Any` | Load source content. Provides direct module-level access to ``EmailLoader.load`` using a fresh ``EmailLoader`` instance. Any: Value returned by ``EmailLoader.load``. |
| `load_json()` | `load_json( filepath: str, is_text: bool = True, is_lines: bool = False ) -> Any` | Load source content. Provides direct module-level access to ``JsonLoader.load`` using a fresh ``JsonLoader`` instance. Any: Value returned by ``JsonLoader.load``. |
| `load_xml()` | `load_xml( filepath: str ) -> Any` | Load source content. Provides direct module-level access to ``XmlLoader.load`` using a fresh ``XmlLoader`` instance. Any: Value returned by ``XmlLoader.load``. |
| `load_xml_tree()` | `load_xml_tree( filepath: str ) -> Any` | Parse an XML element tree. Provides direct module-level access to ``XmlLoader.load_tree`` using a fresh ``XmlLoader`` instance. Any: Value returned by ``XmlLoader.load_tree``. |
| `load_jupyter_notebook()` | `load_jupyter_notebook( path: str, include_outputs: bool = False, max_output_length: int = 10, remove_newline: bool = False, traceback: bool = False ) -> Any` | Load source content. Provides direct module-level access to ``JupyterNotebookLoader.load`` using a fresh ``JupyterNotebookLoader`` instance. Any: Value returned by ``JupyterNotebookLoader.load``. |

## How to choose

Use the functional wrapper when one call completes the task. Use the implementation class when you need retained state, helper methods, or direct provider debugging.

## Operational considerations

- Local paths must exist and be readable.
- Format-specific parser dependencies must be installed.
- Chunking changes document boundaries and should match downstream retrieval needs.
- Stateful split workflows are better handled on a retained loader instance.

## Representative Functions

### `load_text()`

```python
# load_text( path: str, encoding: Optional[str] = None ) -> Any
```

Load source content. Provides direct module-level access to ``TextLoader.load`` using a fresh ``TextLoader`` instance. Any: Value returned by ``TextLoader.load``.

### `load_csv()`

```python
# load_csv( path: str, encoding: Optional[str] = 'utf-8', source_column: Optional[str] = None, delimiter: str = ',', quotechar: str = '"' ) -> Any
```

Load source content. Provides direct module-level access to ``CsvLoader.load`` using a fresh ``CsvLoader`` instance. Any: Value returned by ``CsvLoader.load``.

### `read_pdf()`

```python
# read_pdf( path: str, mode: str = 'single' ) -> Any
```

Load source content. Provides direct module-level access to ``PdfReader.load`` using a fresh ``PdfReader`` instance. Any: Value returned by ``PdfReader.load``.

### `load_pdf()`

```python
# load_pdf( path: str, mode: str = 'single', extract: str = 'plain', include: bool = False, format: str = 'markdown-img', size: int = 1000, overlap: int = 150, has_tables: bool = True ) -> Any
```

Load source content. Provides direct module-level access to ``PdfLoader.load`` using a fresh ``PdfLoader`` instance. Any: Value returned by ``PdfLoader.load``.

### `load_excel()`

```python
# load_excel( path: str, mode: str = 'elements', has_headers: bool = True ) -> Any
```

Load source content. Provides direct module-level access to ``ExcelLoader.load`` using a fresh ``ExcelLoader`` instance. Any: Value returned by ``ExcelLoader.load``.

### `load_word()`

```python
# load_word( path: str ) -> Any
```

Load source content. Provides direct module-level access to ``WordLoader.load`` using a fresh ``WordLoader`` instance. Any: Value returned by ``WordLoader.load``.

### `load_markdown()`

```python
# load_markdown( path: str ) -> Any
```

Load source content. Provides direct module-level access to ``MarkdownLoader.load`` using a fresh ``MarkdownLoader`` instance. Any: Value returned by ``MarkdownLoader.load``.

### `load_html()`

```python
# load_html( path: str ) -> Any
```

Load source content. Provides direct module-level access to ``HtmlLoader.load`` using a fresh ``HtmlLoader`` instance. Any: Value returned by ``HtmlLoader.load``.


See [Functional API](../api/fonky.md) for all signatures.
