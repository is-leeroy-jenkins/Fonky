# Documents & Files

**Tools:** 18

Examples use the Google ADK callable wrapper surface so each example is directly executable as ordinary Python.

## Tool Index

| Tool |
|---|
| [`load_text`](#load_text) |
| [`load_csv`](#load_csv) |
| [`read_pdf`](#read_pdf) |
| [`load_pdf`](#load_pdf) |
| [`load_excel`](#load_excel) |
| [`load_word`](#load_word) |
| [`load_markdown`](#load_markdown) |
| [`load_html`](#load_html) |
| [`load_outlook`](#load_outlook) |
| [`load_spfx`](#load_spfx) |
| [`load_spfx_folder`](#load_spfx_folder) |
| [`load_powerpoint`](#load_powerpoint) |
| [`load_powerpoint_multiple`](#load_powerpoint_multiple) |
| [`load_email`](#load_email) |
| [`load_json`](#load_json) |
| [`load_xml`](#load_xml) |
| [`load_xml_tree`](#load_xml_tree) |
| [`load_jupyter_notebook`](#load_jupyter_notebook) |

---

## `load_text`

Load a plain-text file.

### Signature

```python
def load_text( path: str, encoding: Optional[str]=None ) -> Any
```

### Purpose

Load a plain-text file using the text loader.

### Example

```python
from fonky.gemini.tools import load_text

result = load_text(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local file path used by the loader. |
| `encoding` | `Optional[str]` | Optional file encoding passed to the backing loader. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_csv`

Load a CSV file.

### Signature

```python
def load_csv( path: str, encoding: Optional[str]='utf-8', source_column: Optional[str]=None, delimiter: str=',', quotechar: str='"' ) -> Any
```

### Purpose

Load a CSV file using the CSV loader.

### Example

```python
from fonky.gemini.tools import load_csv

result = load_csv(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local file path used by the loader. |
| `encoding` | `Optional[str]` | Optional file encoding passed to the backing loader. |
| `source_column` | `Optional[str]` | Optional CSV column whose value is stored as the document source. |
| `delimiter` | `str` | Field delimiter used to parse delimited text. |
| `quotechar` | `str` | Quote character used to parse delimited text. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `read_pdf`

Read a PDF file.

### Signature

```python
def read_pdf( path: str, mode: str='single' ) -> Any
```

### Purpose

Read a PDF file using the PDF reader.

### Example

```python
from fonky.gemini.tools import read_pdf

result = read_pdf(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local file path used by the loader. |
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_pdf`

Load and extract a PDF file.

### Signature

```python
def load_pdf( path: str, mode: str='single', extract: str='plain', include: bool=False, format: str='markdown-img', size: int=1000, overlap: int=150, has_tables: bool=True ) -> Any
```

### Purpose

Load and extract a PDF file using the PDF loader.

### Example

```python
from fonky.gemini.tools import load_pdf

result = load_pdf(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local file path used by the loader. |
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `extract` | `str` | PDF text-extraction strategy used by the underlying parser. |
| `include` | `bool` | Whether optional embedded content should be included. |
| `format` | `str` | Output or embedded-image format requested from the loader. |
| `size` | `int` | Maximum chunk size used for document splitting. |
| `overlap` | `int` | Number of characters or tokens repeated between adjacent chunks. |
| `has_tables` | `bool` | Whether table-aware parsing or extraction should be enabled. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_excel`

Load an Excel workbook.

### Signature

```python
def load_excel( path: str, mode: str='elements', has_headers: bool=True ) -> Any
```

### Purpose

Load an Excel workbook using the Excel loader.

### Example

```python
from fonky.gemini.tools import load_excel

result = load_excel(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local file path used by the loader. |
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `has_headers` | `bool` | Whether the first spreadsheet row should be treated as column headers. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_word`

Load a Word document.

### Signature

```python
def load_word( path: str ) -> Any
```

### Purpose

Load a Word document using the Word loader.

### Example

```python
from fonky.gemini.tools import load_word

result = load_word(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local file path used by the loader. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_markdown`

Load a Markdown document.

### Signature

```python
def load_markdown( path: str ) -> Any
```

### Purpose

Load a Markdown document using the Markdown loader.

### Example

```python
from fonky.gemini.tools import load_markdown

result = load_markdown(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local file path used by the loader. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_html`

Load an HTML document.

### Signature

```python
def load_html( path: str ) -> Any
```

### Purpose

Load an HTML document using the HTML loader.

### Example

```python
from fonky.gemini.tools import load_html

result = load_html(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local file path used by the loader. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_outlook`

Load an Outlook message.

### Signature

```python
def load_outlook( path: str ) -> Any
```

### Purpose

Load an Outlook message using the Outlook message loader.

### Example

```python
from fonky.gemini.tools import load_outlook

result = load_outlook(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local file path used by the loader. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_spfx`

Load a SharePoint document library.

### Signature

```python
def load_spfx( library_id: str ) -> Any
```

### Purpose

Load a SharePoint document library using the SharePoint loader.

### Example

```python
from fonky.gemini.tools import load_spfx

result = load_spfx(
    library_id='library-id' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `library_id` | `str` | SharePoint document-library identifier. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_spfx_folder`

Load a SharePoint folder.

### Signature

```python
def load_spfx_folder( library_id: str, folder_id: str ) -> Any
```

### Purpose

Load a SharePoint folder using the SharePoint loader.

### Example

```python
from fonky.gemini.tools import load_spfx_folder

result = load_spfx_folder(
    library_id='library-id',
    folder_id='folder-id' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `library_id` | `str` | SharePoint document-library identifier. |
| `folder_id` | `str` | Provider folder identifier used to load folder contents. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_powerpoint`

Load a PowerPoint presentation.

### Signature

```python
def load_powerpoint( path: str, mode: str='single' ) -> Any
```

### Purpose

Load a PowerPoint presentation using the PowerPoint loader.

### Example

```python
from fonky.gemini.tools import load_powerpoint

result = load_powerpoint(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local file path used by the loader. |
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_powerpoint_multiple`

Load multiple PowerPoint presentation elements.

### Signature

```python
def load_powerpoint_multiple( path: str ) -> Any
```

### Purpose

Load multiple PowerPoint presentation elements using the PowerPoint loader.

### Example

```python
from fonky.gemini.tools import load_powerpoint_multiple

result = load_powerpoint_multiple(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local file path used by the loader. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_email`

Load an email message.

### Signature

```python
def load_email( path: str, mode: str='single', attachments: bool=True ) -> Any
```

### Purpose

Load an email message using the email loader.

### Example

```python
from fonky.gemini.tools import load_email

result = load_email(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local file path used by the loader. |
| `mode` | `str` | Operation mode used to select the provider or processing workflow. |
| `attachments` | `bool` | Whether email attachments should be included when supported. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_json`

Load JSON content.

### Signature

```python
def load_json( filepath: str, is_text: bool=True, is_lines: bool=False ) -> Any
```

### Purpose

Load JSON content using the JSON loader.

### Example

```python
from fonky.gemini.tools import load_json

result = load_json(
    filepath='data/input.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `filepath` | `str` | Local file path used by the loader. |
| `is_text` | `bool` | Whether JSON values should be treated as text content. |
| `is_lines` | `bool` | Whether the JSON source uses JSON Lines format. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_xml`

Load an XML document.

### Signature

```python
def load_xml( filepath: str ) -> Any
```

### Purpose

Load an XML document using the XML loader.

### Example

```python
from fonky.gemini.tools import load_xml

result = load_xml(
    filepath='data/input.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `filepath` | `str` | Local file path used by the loader. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_xml_tree`

Parse an XML document tree.

### Signature

```python
def load_xml_tree( filepath: str ) -> Any
```

### Purpose

Parse an XML document tree using the XML loader.

### Example

```python
from fonky.gemini.tools import load_xml_tree

result = load_xml_tree(
    filepath='data/input.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `filepath` | `str` | Local file path used by the loader. |

### Returns

Any: XML elements matching the requested XPath expression.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---

## `load_jupyter_notebook`

Load a Jupyter notebook.

### Signature

```python
def load_jupyter_notebook( path: str, include_outputs: bool=False, max_output_length: int=10, remove_newline: bool=False, traceback: bool=False ) -> Any
```

### Purpose

Load a Jupyter notebook using the Jupyter notebook loader. Boolean options control retrieval depth or supplemental content.

### Example

```python
from fonky.gemini.tools import load_jupyter_notebook

result = load_jupyter_notebook(
    path='data/sample.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `path` | `str` | Local file path used by the loader. |
| `include_outputs` | `bool` | Whether notebook cell outputs should be included. |
| `max_output_length` | `int` | Maximum notebook cell output length to retain. |
| `remove_newline` | `bool` | Whether newline characters should be removed from notebook output. |
| `traceback` | `bool` | Whether notebook traceback output should be included. |

### Returns

Any: LangChain documents loaded from the requested source.

### Raises

Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the project error type.

---
