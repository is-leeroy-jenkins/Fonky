# 📘 User Guide

Fonky provides a reusable Python layer for retrieving external data, loading documents, scraping web
content, processing text, and exposing callable tools for agent-style workflows. This guide focuses
on practical examples that can be copied into scripts, notebooks, applications, and API services.


---

## 🧭 Overview

Fonky is organized around five primary workflows:

| Workflow                | Primary Modules            | Purpose                                                                                                          |
| ----------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Document loading        | `documents`, `loaders`     | Load files, cloud documents, notebooks, email, web pages, and structured data into LangChain `Document` objects. |
| Web extraction          | `web`, `scrapers`          | Fetch pages, parse HTML, extract links, tables, images, headings, paragraphs, and readable text.                 |
| Text processing         | `processors`               | Clean, normalize, tokenize, chunk, vectorize, and prepare text for retrieval or analysis.                        |
| External data retrieval | `fetchers`, export modules | Retrieve public, scientific, environmental, demographic, geospatial, astronomical, health, and web data.         |
| Tool orchestration      | `models`                   | Convert class methods or Python callables into structured provider-ready tool definitions.                       |

The common workflow is:

```text
Load or fetch data
    ↓
Normalize or clean content
    ↓
Chunk or transform documents
    ↓
Expose as structured tools or pass into downstream analysis
```

---

## ⚙️ Environment Setup

Activate the project environment:

```powershell
cd Fonky
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Install browser support when using browser-backed scraping:

```powershell
python -m playwright install chromium
```

Validate the package:

```powershell
python -m compileall .\fonky
```

---

## 🔐 Environment Variables

Fonky reads configuration from `config.py`. Set only the variables needed for the services you use.

Example PowerShell configuration:

```powershell
$env:OPENAI_API_KEY = "your-openai-api-key"
$env:GOOGLE_API_KEY = "your-google-api-key"
$env:GOOGLE_CSE_ID = "your-google-custom-search-engine-id"
$env:GOOGLE_WEATHER_API_KEY = "your-google-weather-api-key"
$env:NASA_API_KEY = "your-nasa-api-key"
$env:GOVINFO_API_KEY = "your-govinfo-api-key"
$env:CONGRESS_API_KEY = "your-congress-api-key"
$env:THENEWSAPI_API_KEY = "your-thenewsapi-key"
```

Exception logging defaults to:

```text
logging/Exceptions.db
```

The logging table defaults to:

```text
Exceptions
```

Override logging paths when needed:

```powershell
$env:LOG_DIR = "C:\Users\terry\source\repos\Fonky\logging"
$env:LOG_PATH = "C:\Users\terry\source\repos\Fonky\logging\Exceptions.db"
$env:LOG_FILE = "Exceptions"
```

---

## 📄 Loading Text Files

Use `TextLoader` for plain-text files.

```python
from fonky.documents import TextLoader

loader = TextLoader()

documents = loader.load(
	path="data/sample.txt",
	encoding="utf-8"
)

print("Document count:", len(documents))

for document_number, document in enumerate(documents, start=1):
	print("Document:", document_number)
	print("Metadata:", document.metadata)
	print("Content:", document.page_content)
	break
```

Split loaded text into retrieval-friendly chunks:

```python
from fonky.documents import TextLoader

loader = TextLoader()

documents = loader.load(
	path="data/sample.txt",
	encoding="utf-8"
)

chunks = loader.split(
	chunk=1000,
	overlap=200
)

print("Chunk count:", len(chunks))

for chunk_number, chunk in enumerate(chunks, start=1):
	print("Chunk:", chunk_number)
	print(chunk.page_content)
	break
```

---

## 📊 Loading CSV Files

Use `CsvLoader` for structured CSV data.

```python
from fonky.documents import CsvLoader

loader = CsvLoader()

documents = loader.load(
	path="data/records.csv",
	encoding="utf-8",
	source_column=None,
	delimiter=",",
	quotechar='"'
)

print("Document count:", len(documents))

for document_number, document in enumerate(documents, start=1):
	print("Document:", document_number)
	print(document.page_content)
	break
```

Use a source column when the CSV contains a field that identifies each record:

```python
from fonky.documents import CsvLoader

loader = CsvLoader()

documents = loader.load(
	path="data/records.csv",
	encoding="utf-8",
	source_column="RecordId",
	delimiter=",",
	quotechar='"'
)

for document_number, document in enumerate(documents, start=1):
	if document_number > 3:
		break
	
	print("Document:", document_number)
	print("Metadata:", document.metadata)
	print("Content:", document.page_content)
```

Split CSV records:

```python
from fonky.documents import CsvLoader

loader = CsvLoader()

documents = loader.load(
	path="data/records.csv",
	encoding="utf-8",
	source_column=None
)

chunks = loader.split(
	chunk=1200,
	overlap=150
)

print("Chunk count:", len(chunks))
```

---

## 📕 Loading PDF Files

Use `PdfLoader` for PDF documents.

```python
from fonky.documents import PdfLoader

loader = PdfLoader(
	size=1000,
	overlap=150,
	has_tables=True,
	include=True
)

documents = loader.load(
	path="data/report.pdf",
	mode="single",
	extract="plain",
	include=False,
	format="markdown-img"
)

print("Document count:", len(documents))

for document_number, document in enumerate(documents, start=1):
	print("Document:", document_number)
	print("Metadata:", document.metadata)
	print("Content:", document.page_content)
	break
```

Use page mode when page-level metadata is important:

```python
from fonky.documents import PdfLoader

loader = PdfLoader()

documents = loader.load(
	path="data/report.pdf",
	mode="page",
	extract="plain",
	include=False,
	format="markdown-img"
)

for page_number, document in enumerate(documents, start=1):
	if page_number > 3:
		break
	
	print("Page:", page_number)
	print("Metadata:", document.metadata)
	print("Content:", document.page_content)
```

Use layout extraction for PDFs where spacing and layout matter:

```python
from fonky.documents import PdfLoader

loader = PdfLoader()

documents = loader.load(
	path="data/report.pdf",
	mode="page",
	extract="layout",
	include=False,
	format="markdown-img"
)

for document in documents:
	print(document.page_content)
	break
```

---

## 📗 Loading Word Documents

Use `WordLoader` for `.docx` files.

```python
from fonky.documents import WordLoader

loader = WordLoader()

documents = loader.load(
	path="data/memo.docx"
)

print("Document count:", len(documents))

for document in documents:
	print(document.page_content)
	break
```

Split the document:

```python
from fonky.documents import WordLoader

loader = WordLoader()

documents = loader.load(
	path="data/memo.docx"
)

chunks = loader.split(
	chunk=1000,
	overlap=200
)

print("Chunk count:", len(chunks))
```

---

## 📙 Loading Markdown Files

Use `MarkdownLoader` for Markdown documentation.

```python
from fonky.documents import MarkdownLoader

loader = MarkdownLoader()

documents = loader.load(
	path="README.md"
)

for document in documents:
	print(document.page_content)
	break
```

Split Markdown into chunks:

```python
from fonky.documents import MarkdownLoader

loader = MarkdownLoader()

documents = loader.load(
	path="README.md"
)

chunks = loader.split(
	chunk=1500,
	overlap=250
)

for chunk_number, chunk in enumerate(chunks, start=1):
	if chunk_number > 3:
		break
	
	print("Chunk:", chunk_number)
	print(chunk.page_content)
```

---

## 🌐 Loading Web Pages

Use `WebLoader` for static web pages.

```python
from fonky.documents import WebLoader

loader = WebLoader(
	recursive=False,
	max_depth=2,
	prevent_outside=True,
	timeout=10,
	ignore=True,
	progress=True
)

documents = loader.load(
	urls="https://example.com"
)

print("Document count:", len(documents))

for document in documents:
	print("Metadata:", document.metadata)
	print("Content:", document.page_content)
	break
```

Load multiple pages:

```python
from fonky.documents import WebLoader

loader = WebLoader(
	recursive=False,
	progress=True
)

urls = (
	"https://example.com",
	"https://www.iana.org/domains/reserved"
)

documents = loader.load(
	urls=list(urls)
)

for document_number, document in enumerate(documents, start=1):
	print("Document:", document_number)
	print("Metadata:", document.metadata)
	print("Content:", document.page_content)
```

Recursively crawl a site:

```python
from fonky.documents import WebLoader

loader = WebLoader(
	recursive=True,
	max_depth=2,
	prevent_outside=True,
	timeout=10,
	ignore=True
)

documents = loader.load(
	urls="https://example.com"
)

print("Document count:", len(documents))
```

Split loaded web content:

```python
from fonky.documents import WebLoader

loader = WebLoader(
	recursive=False
)

documents = loader.load(
	urls="https://example.com"
)

chunks = loader.split(
	chunk=1000,
	overlap=200
)

print("Chunk count:", len(chunks))
```

---

## 🧾 Loading JSON Files

Use `JsonLoader` for JSON and JSON Lines files.

```python
from fonky.documents import JsonLoader

loader = JsonLoader()

documents = loader.load(
	filepath="data/sample.json",
	is_text=True,
	is_lines=False
)

print("Document count:", len(documents))

for document in documents:
	print(document.page_content)
	break
```

Load JSON Lines:

```python
from fonky.documents import JsonLoader

loader = JsonLoader()

documents = loader.load(
	filepath="data/sample.jsonl",
	is_text=True,
	is_lines=True
)

print("Document count:", len(documents))
```

---

## 🧮 Loading Excel Files

Use `ExcelLoader` for spreadsheet ingestion.

```python
from fonky.documents import ExcelLoader

loader = ExcelLoader()

documents = loader.load(
	path="data/workbook.xlsx",
	mode="elements",
	has_headers=True
)

print("Document count:", len(documents))

for document in documents:
	print(document.page_content)
	break
```

Split spreadsheet content:

```python
from fonky.documents import ExcelLoader

loader = ExcelLoader()

documents = loader.load(
	path="data/workbook.xlsx",
	mode="elements",
	has_headers=True
)

chunks = loader.split(
	chunk=1000,
	overlap=200
)

print("Chunk count:", len(chunks))
```

---

## 📽️ Loading PowerPoint Files

Use `PowerPointLoader` for `.ppt` or `.pptx` files.

```python
from fonky.documents import PowerPointLoader

loader = PowerPointLoader()

documents = loader.load(
	path="data/presentation.pptx",
	mode="single"
)

print("Document count:", len(documents))

for document in documents:
	print(document.page_content)
	break
```

Split slide content:

```python
from fonky.documents import PowerPointLoader

loader = PowerPointLoader()

documents = loader.load(
	path="data/presentation.pptx",
	mode="single"
)

chunks = loader.split(
	chunk=1000,
	overlap=200
)

print("Chunk count:", len(chunks))
```

---

## 📧 Loading Email and Outlook Files

Use `EmailLoader` for email documents:

```python
from fonky.documents import EmailLoader

loader = EmailLoader()

documents = loader.load(
	path="data/message.eml",
	mode="single",
	attachments=True
)

print("Document count:", len(documents))

for document in documents:
	print(document.page_content)
	break
```

Use `OutlookLoader` for Outlook message files:

```python
from fonky.documents import OutlookLoader

loader = OutlookLoader()

documents = loader.load(
	path="data/message.msg"
)

print("Document count:", len(documents))

for document in documents:
	print(document.page_content)
	break
```

---

## 🧬 Loading XML Files

Use `XmlLoader` for XML document loading and XPath operations.

```python
from fonky.documents import XmlLoader

loader = XmlLoader()

documents = loader.load(
	filepath="data/sample.xml"
)

print("Document count:", len(documents))

for document in documents:
	print(document.page_content)
	break
```

Parse an XML tree:

```python
from fonky.documents import XmlLoader

loader = XmlLoader()

tree = loader.load_tree(
	filepath="data/sample.xml"
)

elements = loader.get_elements(
	xpath="//record"
)

print("Element count:", len(elements))

for element_number, element in enumerate(elements, start=1):
	if element_number > 3:
		break
	
	print("Element:", element_number)
	print(element.tag)
```

---

## 📓 Loading Jupyter Notebooks

Use `JupyterNotebookLoader` for `.ipynb` files.

```python
from fonky.documents import JupyterNotebookLoader

loader = JupyterNotebookLoader()

documents = loader.load(
	path="notebook/fonkytown.ipynb",
	include_outputs=False,
	max_output_length=10,
	remove_newline=False,
	traceback=False
)

print("Document count:", len(documents))

for document in documents:
	print(document.page_content)
	break
```

---

## ☁️ Loading Cloud Documents

### Google Cloud Storage file

```python
from fonky.cloud import GoogleCloudFileLoader

loader = GoogleCloudFileLoader()

documents = loader.load(
	project_name="your-project-id",
	bucket="your-bucket-name",
	blob="path/to/file.txt"
)

print("Document count:", len(documents))
```

### Google Cloud Storage bucket

```python
from fonky.cloud import GoogleBucketLoader

loader = GoogleBucketLoader()

documents = loader.load(
	project_name="your-project-id",
	bucket="your-bucket-name",
	prefix="documents/",
	continue_on_failure=True
)

print("Document count:", len(documents))
```

### AWS S3 file

```python
from fonky.cloud import AwsFileLoader

loader = AwsFileLoader()

documents = loader.load(
	bucket="your-bucket-name",
	key="documents/sample.txt",
	region_name="us-east-1"
)

print("Document count:", len(documents))
```

### AWS S3 bucket

```python
from fonky.cloud import AwsBucketLoader

loader = AwsBucketLoader()

documents = loader.load(
	bucket="your-bucket-name",
	prefix="documents/",
	region_name="us-east-1"
)

print("Document count:", len(documents))
```

---

## 🔎 Loading Research and Knowledge Sources

### ArXiv

```python
from fonky.archives import ArXiv

archive = ArXiv(
	max_documents=3,
	max_characters=4000,
	include_metadata=True
)

documents = archive.fetch(
	question="retrieval augmented generation",
	max_documents=3,
	full_documents=False,
	include_metadata=True
)

for document_number, document in enumerate(documents, start=1):
	print("Document:", document_number)
	print("Metadata:", document.metadata)
	print("Content:", document.page_content)
```

### Wikipedia

```python
from fonky.archives import Wikipedia

wiki = Wikipedia(
	language="en",
	max_documents=3,
	max_characters=4000,
	include_metadata=True
)

documents = wiki.fetch(
	question="retrieval augmented generation",
	language="en",
	max_documents=3,
	include_metadata=True
)

for document_number, document in enumerate(documents, start=1):
	print("Document:", document_number)
	print("Metadata:", document.metadata)
	print("Content:", document.page_content)
```

### PubMed

```python
from fonky.documents import PubMedSearchLoader

loader = PubMedSearchLoader()

documents = loader.load(
	query="machine learning clinical decision support",
	max_docs=5
)

for document_number, document in enumerate(documents, start=1):
	print("Document:", document_number)
	print("Metadata:", document.metadata)
	print("Content:", document.page_content)
```

---

## 🧹 Cleaning Text

Use `TextParser` for text cleanup.

```python
from fonky.processors import TextParser

parser = TextParser()

raw_text = """
<html>
	<body>
		<h1>Example Document</h1>
		<p>This is sample text with numbers 12345, symbols @#$%, and extra spacing.</p>
	</body>
</html>
"""

cleaned = parser.remove_html(raw_text)
cleaned = parser.remove_numbers(cleaned)
cleaned = parser.remove_symbols(cleaned)
cleaned = parser.compress_whitespace(cleaned)

print(cleaned)
```

Remove Markdown:

```python
from fonky.processors import TextParser

parser = TextParser()

text = """
# Heading

This is bold text with a link to https://example.com.
"""

cleaned = parser.remove_markdown(text)

print(cleaned)
```

Remove stop words:

```python
from fonky.processors import TextParser

parser = TextParser()

text = "This is a sample sentence that contains common stop words."

tokens = parser.remove_stopwords(text)

for token in tokens:
	print(token)
```

Normalize text:

```python
from fonky.processors import TextParser

parser = TextParser()

text = "  This   Text   Has MIXED Case and Extra Spaces.  "

normalized = parser.normalize_text(text)

print(normalized)
```

---

## ✂️ Splitting and Chunking Text

Split text into sentences:

```python
from fonky.processors import TextParser

parser = TextParser()

text = "This is the first sentence. This is the second sentence. This is the third sentence."

sentences = parser.split_sentences(text)

for sentence in sentences:
	print(sentence)
```

Split text into paragraphs:

```python
from fonky.processors import TextParser

parser = TextParser()

text = """
First paragraph.

Second paragraph.

Third paragraph.
"""

paragraphs = parser.split_paragraphs(text)

for paragraph in paragraphs:
	print(paragraph)
```

Chunk raw text:

```python
from fonky.processors import TextParser

parser = TextParser()

text = "This is a long text value. " * 500

chunks = parser.chunk_text(
	text=text,
	chunk_size=1000,
	overlap=100
)

print("Chunk count:", len(chunks))

for chunk in chunks:
	print(chunk)
	break
```

---

## 📈 Frequency and Vector Representations

Create a frequency distribution:

```python
from fonky.processors import TextParser

parser = TextParser()

text = "data data model model model retrieval retrieval augmented generation"

frequency = parser.create_frequency_distribution(text)

print(frequency)
```

Create a vocabulary:

```python
from fonky.processors import TextParser

parser = TextParser()

text = "data model retrieval augmented generation model data"

vocabulary = parser.create_vocabulary(text)

print(vocabulary)
```

Create bag-of-words output:

```python
from fonky.processors import TextParser

parser = TextParser()

text = "data model retrieval augmented generation model data"

wordbag = parser.create_wordbag(text)

print(wordbag)
```

Create TF-IDF vectors:

```python
from fonky.processors import TextParser

parser = TextParser()

texts = (
	"data retrieval and model evaluation",
	"retrieval augmented generation with documents",
	"model evaluation with structured data"
)

tfidf = parser.create_tfidf(
	texts=list(texts)
)

print(tfidf)
```

---

## 🧠 NLP With NLTK

Use `NltkParser` for tokenization, stemming, lemmatization, part-of-speech tagging, named entity
recognition, and chunking.

```python
from fonky.processors import NltkParser

parser = NltkParser()

tokens = parser.word_tokenizer(
	text="Fonky loads documents and prepares data for analysis."
)

for token in tokens:
	print(token)
```

Sentence tokenization:

```python
from fonky.processors import NltkParser

parser = NltkParser()

sentences = parser.sentence_tokenizer(
	text="Fonky loads documents. It also processes text."
)

for sentence in sentences:
	print(sentence)
```

Stemming:

```python
from fonky.processors import NltkParser

parser = NltkParser()

words = (
	"running",
	"runner",
	"runs",
	"processed",
	"processing"
)

stems = parser.word_stemmer(
	words=list(words)
)

for stem in stems:
	print(stem)
```

Lemmatization:

```python
from fonky.processors import NltkParser

parser = NltkParser()

words = (
	"running",
	"documents",
	"models",
	"analyses"
)

lemmas = parser.word_lemmatizer(
	words=list(words)
)

for lemma in lemmas:
	print(lemma)
```

Part-of-speech tagging:

```python
from fonky.processors import NltkParser

parser = NltkParser()

tags = parser.pos_tagger(
	text="Fonky processes documents for retrieval workflows."
)

for tag in tags:
	print(tag)
```

Named entity recognition:

```python
from fonky.processors import NltkParser

parser = NltkParser()

entities = parser.named_entity_recognition(
	text="NASA and EPA published environmental data in Washington."
)

print(entities)
```

---

## 🌍 Web Extraction

Use `WebExtractor` for HTML parsing.

```python
from fonky.web import WebExtractor

extractor = WebExtractor()

html = """
<html>
	<body>
		<h1>Example Page</h1>
		<p>This is an example paragraph.</p>
		<a href="https://example.com/data">Data</a>
	</body>
</html>
"""

text = extractor.html_to_text(html)

print(text)
```

Extract links:

```python
from fonky.web import WebExtractor

extractor = WebExtractor()

html = """
<html>
	<body>
		<a href="https://example.com/data">Data</a>
		<a href="/about">About</a>
	</body>
</html>
"""

links = extractor.extract_links(
	html=html,
	base_url="https://example.com"
)

for link in links:
	print(link)
```

Extract headings:

```python
from fonky.web import WebExtractor

extractor = WebExtractor()

html = """
<html>
	<body>
		<h1>Main Title</h1>
		<h2>Section</h2>
	</body>
</html>
"""

headings = extractor.extract_headings(html)

for heading in headings:
	print(heading)
```

Extract tables:

```python
from fonky.web import WebExtractor

extractor = WebExtractor()

html = """
<table>
	<tr>
		<th>Name</th>
		<th>Value</th>
	</tr>
	<tr>
		<td>Alpha</td>
		<td>100</td>
	</tr>
</table>
"""

tables = extractor.extract_tables(html)

for table in tables:
	print(table)
```

---

## 🛠️ Structured Tool Creation

Fonky can convert functions and methods into structured tool definitions.

### Create a tool from a plain function

```python
from fonky.models import ToolDef

def add_numbers(left: int, right: int) -> int:
	"""Add two integers.

	Purpose:
		Adds two integer values and returns their sum.

	Args:
		left (int): Left integer.
		right (int): Right integer.

	Returns:
		Sum of the two input values.
	"""
	return left + right

tool = ToolDef.from_callable(
	function=add_numbers,
	name="add_numbers",
	category="utility"
)

schema = tool.to_openai()

print(schema)
```

Execute the tool:

```python
result = tool.call(
	{
		"left": 10,
		"right": 15
	}
)

print(result)
```

Expected result shape:

```python
{
	"ok": True,
	"name": "add_numbers",
	"data": 25,
	"error": None,
	"metadata": {
		"category": "utility",
		"source_module": "__main__",
		"source_class": None,
		"method": None,
		"callable_name": "add_numbers"
	}
}
```

---

## 🧰 Tool From a Loader Method

Create a structured tool from `TextLoader.load`:

```python
from fonky.documents import TextLoader
from fonky.models import ToolDef

loader = TextLoader()

tool = ToolDef.from_method(
	target=loader,
	method="load",
	name="load_text_file",
	category="documents"
)

schema = tool.to_openai()

print(schema)
```

Call it:

```python
result = tool.call(
	{
		"path": "data/sample.txt",
		"encoding": "utf-8"
	}
)

if result.get("ok"):
	data = result.get("data")
	for item in data:
		content = item.get("page_content")
		print(content)
		break
else:
	print(result.get("error"))
```

---

## 📕 Tool From a PDF Loader

```python
from fonky.documents import PdfLoader
from fonky.models import ToolDef

loader = PdfLoader()

tool = ToolDef.from_method(
	target=loader,
	method="load",
	name="load_pdf_file",
	category="documents"
)

result = tool.call(
	{
		"path": "data/report.pdf",
		"mode": "single",
		"extract": "plain",
		"include": False,
		"format": "markdown-img"
	}
)

if result.get("ok"):
	data = result.get("data")
	for item in data:
		content = item.get("page_content")
		print(content)
		break
else:
	print(result.get("error"))
```

---

## 🌐 Tool From a Web Loader

```python
from fonky.documents import WebLoader
from fonky.models import ToolDef

loader = WebLoader(
	recursive=False
)

tool = ToolDef.from_method(
	target=loader,
	method="load",
	name="load_web_page",
	category="documents"
)

result = tool.call(
	{
		"urls": "https://example.com"
	}
)

if result.get("ok"):
	data = result.get("data")
	for item in data:
		content = item.get("page_content")
		print(content)
		break
else:
	print(result.get("error"))
```

---

## 🔁 Export Tool Schemas

Export a single tool into multiple provider formats:

```python
from fonky.documents import TextLoader
from fonky.models import ToolDef

tool = ToolDef.from_method(
	target=TextLoader(),
	method="load",
	name="load_text_file",
	category="documents"
)

openai_schema = tool.to_openai()
gemini_schema = tool.to_gemini()
grok_schema = tool.to_grok()

print(openai_schema)
print(gemini_schema)
print(grok_schema)
```

---

## 🧪 Handling Tool Errors

When tool execution fails, `ToolDef.call()` returns a structured error envelope instead of throwing
the exception directly.

```python
from fonky.documents import TextLoader
from fonky.models import ToolDef

tool = ToolDef.from_method(
	target=TextLoader(),
	method="load",
	name="load_text_file",
	category="documents"
)

result = tool.call(
	{
		"path": "data/missing-file.txt",
		"encoding": "utf-8"
	}
)

print("Succeeded:", result.get("ok"))
print("Error:", result.get("error"))
```

Expected result shape:

```python
{
	"ok": False,
	"name": "load_text_file",
	"data": None,
	"error": {
		"type": "Error",
		"message": "..."
	},
	"metadata": {
		"category": "documents",
		"source_module": "fonky.loaders",
		"source_class": "TextLoader",
		"method": "load",
		"callable_name": "load"
	}
}
```

---

## 🪵 Exception Logging

Handled runtime exceptions use the explicit project logging pattern.

```python
except Exception as e:
	exception = Error(e)
	exception.module = "loaders"
	exception.cause = "TextLoader"
	exception.method = "load(self, path: str, encoding: Optional[str]=None) -> List[Document]"
	Logger().write(exception)
	raise exception
```

This writes the wrapped exception to the configured SQLite database.

Default database:

```text
logging/Exceptions.db
```

Default table:

```text
Exceptions
```

---

## 🧪 Validation Workflow

After regenerating source files, run:

```powershell
python -m py_compile .\fonky\boogr.py
python -m py_compile .\fonky\config.py
python -m py_compile .\fonky\core.py
python -m py_compile .\fonky\archives.py
python -m py_compile .\fonky\models.py
python -m py_compile .\fonky\processors.py
python -m py_compile .\fonky\loaders.py
python -m py_compile .\fonky\scrapers.py
python -m py_compile .\fonky\fetchers.py
```

Or compile the full package:

```powershell
python -m compileall .\fonky
```

---

## 📚 Building Documentation

Install MkDocs dependencies:

```powershell
python -m pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python pymdown-extensions
```

Build the site:

```powershell
mkdocs build
```

Serve locally:

```powershell
mkdocs serve
```

Then open:

```text
http://127.0.0.1:8000/
```

---

## 🚀 Deploying to GitHub Pages

Deploy with:

```powershell
mkdocs gh-deploy --force
```

Then configure GitHub Pages to serve the `gh-pages` branch.

Expected documentation URL:

```text
https://is-leeroy-jenkins.github.io/Fonky/
```

---

## ✅ Recommended Development Pattern

For new modules and methods:

1. Add a robust Google-style docstring.
2. Include a `Purpose:` section.
3. Use `Args:` for parameters.
4. Use `Returns:` only when a value is returned.
5. Avoid `Returns: None`.
6. Avoid `Returns: Any`.
7. Avoid underline-style section headings.
8. Preserve explicit exception logging.
9. Run `python -m py_compile`.
10. Run `mkdocs build`.

Recommended exception block:

```python
except Exception as e:
	exception = Error(e)
	exception.module = "module_name"
	exception.cause = "ClassName"
	exception.method = "method_name(self, arg: type) -> return_type"
	Logger().write(exception)
	raise exception
```

---

## 🧭 Next Steps

After replacing this page:

1. Run `mkdocs build`.
2. Confirm the `mkdocs_autorefs` warnings for `0` and `:1000` are gone.
3. Fix any remaining missing imports or mkdocstrings warnings.
4. Run `mkdocs serve`.
5. Review the rendered guide and API pages.
6. Deploy with `mkdocs gh-deploy --force`.
