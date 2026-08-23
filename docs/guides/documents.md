# Document Loading

The Documents domain converts local and enterprise document formats into usable Python/LangChain
document structures. It is one of Fonky's richest capability areas.

## Choose the Loader

| Source | Function | Use When |
|---|---|---|
| Plain text | `load_text()` | You need raw text as documents. |
| CSV | `load_csv()` | Each row should become structured document content. |
| PDF | `read_pdf()` | You need direct PDF reader output. |
| PDF | `load_pdf()` | You need loader-managed extraction, OCR/plain modes, images, tables, or chunk settings. |
| Excel | `load_excel()` | You need spreadsheet/sheet content. |
| Word | `load_word()` | You need DOCX text extraction. |
| Markdown | `load_markdown()` | You need Markdown source as documents. |
| HTML | `load_html()` | You need local HTML document loading. |
| Outlook | `load_outlook()` | You need Outlook message content. |
| SPFx | `load_spfx()` / `load_spfx_folder()` | You need SharePoint Framework library/folder content. |
| PowerPoint | `load_powerpoint()` / `load_powerpoint_multiple()` | You need slide content from one or multiple presentations. |
| Email | `load_email()` | You need email body and optionally attachments. |
| JSON | `load_json()` | You need JSON or JSON Lines content. |
| XML | `load_xml()` / `load_xml_tree()` | You need semantic XML documents or a structured XML tree. |
| Notebook | `load_jupyter_notebook()` | You need notebook cells and optionally outputs. |

## Workflow — PDF with Plain Extraction

```python
from fonky import fonky

documents = fonky.load_pdf(
    path='report.pdf',
    mode='single',
    extract='plain',
    include=False,
    format='markdown-img',
    size=1000,
    overlap=150,
    has_tables=True
)
```

### When to change the defaults

- Use OCR-oriented extraction when the PDF is image-based or text extraction is poor.
- Keep table handling enabled when tables materially affect the document meaning.
- Tune `size` and `overlap` to the downstream retrieval/embedding task; there is no universal optimal
  chunk size.

## Workflow — CSV with Source Metadata

```python
from fonky import fonky

documents = fonky.load_csv(
    path='records.csv',
    encoding='utf-8',
    source_column='record_id',
    delimiter=',',
    quotechar='"'
)
```

A source column is useful when downstream results must retain a row-level identifier.

## Workflow — Jupyter Notebook

```python
from fonky import fonky

documents = fonky.load_jupyter_notebook(
    path='analysis.ipynb',
    include_outputs=True,
    max_output_length=20,
    remove_newline=False,
    traceback=False
)
```

Avoid including large cell outputs unless the outputs are actually needed for downstream analysis.

## Workflow — Email with Attachments

```python
from fonky import fonky

documents = fonky.load_email(
    path='message.eml',
    mode='single',
    attachments=True
)
```

## Stateful Loader Workflows

The functional API is best for one-shot loading. Use a loader class directly when you need to retain
`self.documents` and perform later operations such as splitting on the same instance.

## Failure Modes

- missing/unreadable path;
- unsupported/corrupt file;
- missing format-specific dependency;
- OCR dependency not installed;
- parser failure on malformed content;
- excessive memory use on very large files;
- enterprise authentication failure for SPFx/Outlook-backed integrations.
