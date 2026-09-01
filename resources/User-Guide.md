![](https://github.com/is-leeroy-jenkins/Fonky/blob/main/resources/images/fonky-guide.png)

___

## 📥 Select a Provider Integration

### OpenAI Agents SDK

```python
from fonky.gpt import tools
```

### Google ADK

```python
from fonky.gemini import tools
```

### xAI Grok

```python
from fonky.grok import tools
```

### LangChain

```python
from fonky.langchain import tools
```

## 🔎 Research Agent

### OpenAI Agents SDK

```python
from agents import Agent, Runner

from fonky.gpt.tools import fetch_arxiv
from fonky.gpt.tools import fetch_cse_search
from fonky.gpt.tools import fetch_wikipedia

agent = Agent(
    name='Research Assistant',
    instructions='Use Fonky tools to retrieve external sources before answering.',
    tools=[
        fetch_arxiv,
        fetch_cse_search,
        fetch_wikipedia,
    ] )

result = Runner.run_sync(
    agent,
    'Research retrieval augmented generation and summarize the major approaches.' )

print( result.final_output )
```

### Google ADK

```python
from google.adk.agents import Agent

from fonky.gemini.tools import fetch_arxiv
from fonky.gemini.tools import fetch_cse_search
from fonky.gemini.tools import fetch_wikipedia

agent = Agent(
    name='research_assistant',
    model='gemini-3.7-flash',
    instruction='Use Fonky tools to retrieve external sources before answering.',
    tools=[
        fetch_arxiv,
        fetch_cse_search,
        fetch_wikipedia,
    ] )
```

### LangChain

```python
from fonky.langchain.tools import fetch_arxiv
from fonky.langchain.tools import fetch_cse_search
from fonky.langchain.tools import fetch_wikipedia

tools = [
    fetch_arxiv,
    fetch_cse_search,
    fetch_wikipedia,
]
```

## 🌐 Google Programmable Search Engine

### OpenAI

```python
from agents import Agent, Runner

from fonky.gpt.tools import fetch_cse_search

agent = Agent(
    name='Search Assistant',
    tools=[
        fetch_cse_search,
    ] )

result = Runner.run_sync(
    agent,
    'Find current public sources about federal appropriations law.' )

print( result.final_output )
```

### Gemini

```python
from google.adk.agents import Agent

from fonky.gemini.tools import fetch_cse_search

agent = Agent(
    name='search_assistant',
    model='gemini-3.7-flash',
    tools=[
        fetch_cse_search,
    ] )
```

### Grok

```python
from fonky.grok.tools import cse_search_tool
from fonky.grok.tools import fetch_cse_search

tools = [
    cse_search_tool,
]

result = fetch_cse_search(
    keywords='federal appropriations law',
    results=5 )

print( result )
```

### LangChain

```python
from fonky.langchain.tools import fetch_cse_search

result = fetch_cse_search.invoke(
    {
        'keywords': 'federal appropriations law',
        'results': 5,
    } )

print( result )
```

## 📄 Document Loading

### Text

```python
from fonky.gemini.tools import load_text

documents = load_text(
    path='data/sample.txt',
    encoding='utf-8' )

print( documents )
```

### PDF

```python
from fonky.gemini.tools import load_pdf

documents = load_pdf(
    path='data/report.pdf',
    mode='single',
    extract='plain',
    include=False,
    format='markdown-img' )

print( documents )
```

### Word

```python
from fonky.gemini.tools import load_word

documents = load_word(
    path='data/report.docx' )

print( documents )
```

### CSV

```python
from fonky.gemini.tools import load_csv

documents = load_csv(
    path='data/sample.csv' )

print( documents )
```

### Excel

```python
from fonky.gemini.tools import load_excel

documents = load_excel(
    path='data/sample.xlsx' )

print( documents )
```

## 🌐 Web Extraction

### Fetch a Page

```python
from fonky.gemini.tools import fetch_web_page

response = fetch_web_page(
    uri='https://example.com' )

print( response )
```

### Extract Paragraphs

```python
from fonky.gemini.tools import scrape_paragraphs

paragraphs = scrape_paragraphs(
    uri='https://example.com' )

print( paragraphs )
```

### Extract Tables

```python
from fonky.gemini.tools import scrape_tables

tables = scrape_tables(
    uri='https://example.com' )

print( tables )
```

### Crawl a Site

```python
from fonky.gemini.tools import crawl_web

pages = crawl_web(
    seed_url='https://example.com',
    recursive=True,
    max_depth=1,
    max_pages=10 )

print( pages )
```

## 🧹 Text Processing

### Normalize Text

```python
from fonky.gemini.tools import preprocess_normalize_text

value = preprocess_normalize_text(
    text='  MULTIPLE    SPACES  ' )

print( value )
```

### Remove Stopwords

```python
from fonky.gemini.tools import preprocess_remove_stopwords

value = preprocess_remove_stopwords(
    text='The analyst reviewed the report and the supporting data.' )

print( value )
```

### Split Sentences

```python
from fonky.gemini.tools import preprocess_split_sentences

sentences = preprocess_split_sentences(
    text='Fonky loads documents. Fonky processes text.' )

print( sentences )
```

### Semantic Search

```python
from fonky.gemini.tools import preprocess_semantic_search

matches = preprocess_semantic_search(
    query='federal spending',
    tokens=[
        'budget execution',
        'weather observations',
        'appropriations and obligations',
        'astronomy catalog',
        'outlay analysis',
    ],
    model='all-MiniLM-L6-v2',
    top=3 )

print( matches )
```

## 🧠 NLTK Processing

```python
from fonky.gemini.tools import nltk_named_entity_recognition
from fonky.gemini.tools import nltk_pos_tagger
from fonky.gemini.tools import nltk_word_lemmatizer
from fonky.gemini.tools import nltk_word_tokenizer

tokens = nltk_word_tokenizer(
    text='NASA operates the Goddard Space Flight Center.' )

lemmas = nltk_word_lemmatizer(
    text='cars studies running analyzed' )

tags = nltk_pos_tagger(
    text='The analyst reviewed the financial report.' )

entities = nltk_named_entity_recognition(
    text='NASA operates the Goddard Space Flight Center in Maryland.' )
```

## 🧩 LangChain Schema Parsing

```python
from fonky.langchain.tools import fetch_cse_search

print( fetch_cse_search.name )
print( fetch_cse_search.description )
print( fetch_cse_search.args_schema.model_json_schema( ) )
```

## 🧩 OpenAI Tool Schema

```python
import json

from agents import FunctionTool

from fonky.gpt.tools import fetch_arxiv

if isinstance( fetch_arxiv, FunctionTool ):
    print( fetch_arxiv.name )
    print( fetch_arxiv.description )
    print( json.dumps( fetch_arxiv.params_json_schema, indent=2 ) )
```

## 🏷️ Grok Declaration and Callable

```python
from fonky.grok.tools import arxiv_fetch_tool
from fonky.grok.tools import fetch_arxiv

tools = [
    arxiv_fetch_tool,
]

documents = fetch_arxiv(
    question='retrieval augmented generation',
    max_documents=5,
    full_documents=False,
    include_metadata=True )

print( documents )
```

## ✅ Validate Installation

```powershell
python -m compileall .\fonky
python -c "import fonky.gpt.tools; import fonky.gemini.tools; import fonky.grok.tools; import fonky.langchain.tools; print('ok')"
```
