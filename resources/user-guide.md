# Fonky User Guide

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel
python -m pip install "setuptools==81.0.0"
python -m pip install -r requirements.txt
python -m pip check
python -m playwright install chromium
```

## Environment Variables

```powershell
$env:OPENAI_API_KEY = "..."
$env:GOOGLE_API_KEY = "..."
$env:GOOGLE_CSE_ID = "..."
$env:NASA_API_KEY = "..."
```

## Sample Data

```powershell
New-Item -ItemType Directory -Force .\data | Out-Null

"Fonky retrieves data, loads documents, scrapes web content, and preprocesses text." |
    Set-Content .\data\sample.txt -Encoding UTF8
```

```powershell
@"
name,category,value
Alpha,A,10
Beta,B,20
Gamma,A,30
"@ | Set-Content .\data\sample.csv -Encoding UTF8
```

```powershell
@"
{
  "messages": [
    {"content": "Fonky JSON loader example."},
    {"content": "Second JSON document."}
  ]
}
"@ | Set-Content .\data\messages.json -Encoding UTF8
```

# Direct Python API

## Text Loader

```python
from fonky.loaders import TextLoader

loader = TextLoader( )

documents = loader.load(
    path='data/sample.txt',
    encoding='utf-8' )

for document in documents:
    print( document.page_content )
```

## Text Splitter

```python
from fonky.loaders import TextLoader

loader = TextLoader( )
loader.load( path='data/sample.txt', encoding='utf-8' )

chunks = loader.split(
    chunk=500,
    overlap=50 )

for chunk in chunks:
    print( chunk.page_content )
```

## CSV Loader

```python
from fonky.loaders import CsvLoader

loader = CsvLoader( )

documents = loader.load(
    path='data/sample.csv',
    encoding='utf-8',
    source_column='name',
    delimiter=',',
    quotechar='"' )
```

## PDF Loader

```python
from fonky.loaders import PdfLoader

loader = PdfLoader( )

documents = loader.load(
    path='data/sample.pdf',
    mode='single',
    extract='plain',
    include=False,
    format='markdown-img' )
```

## Word Loader

```python
from fonky.loaders import WordLoader

loader = WordLoader( )
documents = loader.load( path='data/sample.docx' )
```

## Excel Loader

```python
from fonky.loaders import ExcelLoader

loader = ExcelLoader( )

documents = loader.load(
    path='data/sample.xlsx',
    mode='elements',
    has_headers=True )
```

## JSON Loader

```python
from fonky.loaders import JsonLoader

loader = JsonLoader( )

documents = loader.load(
    filepath='data/messages.json',
    is_text=True,
    is_lines=False )
```

## Markdown Loader

```python
from fonky.loaders import MarkdownLoader

loader = MarkdownLoader( )
documents = loader.load( path='README.md' )
```

## Jupyter Notebook Loader

```python
from fonky.loaders import JupyterNotebookLoader

loader = JupyterNotebookLoader( )

documents = loader.load(
    path='notebook/fonky.ipynb',
    include_outputs=True,
    max_output_length=200,
    remove_newline=False,
    traceback=False )
```

## Web Fetcher

```python
from fonky.fetchers import WebFetcher

fetcher = WebFetcher( )

result = fetcher.fetch(
    url='https://example.com',
    time=10 )

print( result.status_code )
print( result.url )
print( result.text[:500] )
```

## ArXiv Fetcher

```python
from fonky.fetchers import ArXiv

fetcher = ArXiv( )

documents = fetcher.fetch(
    question='retrieval augmented generation',
    max_documents=5,
    full_documents=False,
    include_metadata=True )
```

## Wikipedia Fetcher

```python
from fonky.fetchers import Wikipedia

fetcher = Wikipedia( )

documents = fetcher.fetch(
    question='federal budget process',
    max_documents=5,
    include_metadata=True )
```

## Paragraph Scraper

```python
from fonky.scrapers import WebExtractor

extractor = WebExtractor( )
paragraphs = extractor.scrape_paragraphs( uri='https://example.com' )
```

## Table Scraper

```python
from fonky.scrapers import WebExtractor

extractor = WebExtractor( )
tables = extractor.scrape_tables( uri='https://example.com' )
```

## Heading Scraper

```python
from fonky.scrapers import WebExtractor

extractor = WebExtractor( )
headings = extractor.scrape_headings( uri='https://example.com' )
```

## Text Normalization

```python
from fonky.preprocessors import TextParser

parser = TextParser( )
value = parser.normalize_text( text='Fonky PROVIDES reusable preprocessing.' )
print( value )
```

# OpenAI Agents SDK

## Minimal Agent

```python
from agents import Agent, Runner
from fonky.tools import fetch_arxiv

agent = Agent(
    name='Research Assistant',
    instructions='Use ArXiv for scholarly research.',
    tools=[
        fetch_arxiv,
    ] )

result = Runner.run_sync(
    agent,
    'Research retrieval augmented generation.' )

print( result.final_output )
```

## Multi-Tool Research Agent

```python
from agents import Agent, Runner

from fonky.tools import fetch_arxiv
from fonky.tools import fetch_google_search
from fonky.tools import fetch_wikipedia

agent = Agent(
    name='Research Assistant',
    instructions='Select the most appropriate source for each request.',
    tools=[
        fetch_arxiv,
        fetch_google_search,
        fetch_wikipedia,
    ] )

result = Runner.run_sync(
    agent,
    'Research retrieval augmented generation.' )

print( result.final_output )
```

## Async Agent

```python
import asyncio

from agents import Agent, Runner
from fonky.tools import fetch_wikipedia

async def main( ) -> None:
    agent = Agent(
        name='Reference Assistant',
        tools=[
            fetch_wikipedia,
        ] )

    result = await Runner.run(
        agent,
        'Explain the Congressional Budget and Impoundment Control Act.' )

    print( result.final_output )

asyncio.run( main( ) )
```

## Streaming Agent

```python
import asyncio

from agents import Agent, Runner
from fonky.tools import fetch_google_search

async def main( ) -> None:
    agent = Agent(
        name='Search Assistant',
        tools=[
            fetch_google_search,
        ] )

    result = Runner.run_streamed(
        agent,
        'Research current AI regulation.' )

    async for event in result.stream_events( ):
        print( event )

asyncio.run( main( ) )
```

## FunctionTool Schema

```python
import json

from agents import FunctionTool
from fonky.tools import fetch_arxiv

if isinstance( fetch_arxiv, FunctionTool ):
    print( fetch_arxiv.name )
    print( fetch_arxiv.description )
    print( json.dumps( fetch_arxiv.params_json_schema, indent=2 ) )
```

## Wrapped Function Test

```python
from fonky.tools import preprocess_normalize_text

value = preprocess_normalize_text.__wrapped__(
    text='  MULTIPLE    SPACES  ' )

print( value )
```

# Document Agents

## Text Agent

```python
from agents import Agent, Runner
from fonky.tools import load_text

agent = Agent( name='Text Analyst', tools=[load_text] )
result = Runner.run_sync( agent, 'Load data/sample.txt and summarize it.' )
print( result.final_output )
```

## PDF and Word Agent

```python
from agents import Agent, Runner
from fonky.tools import load_pdf, load_word

agent = Agent( name='Document Analyst', tools=[load_pdf, load_word] )
result = Runner.run_sync( agent, 'Load data/report.pdf and summarize it.' )
print( result.final_output )
```

## Structured File Agent

```python
from agents import Agent, Runner
from fonky.tools import load_csv, load_excel, load_json

agent = Agent( name='Structured Data Analyst', tools=[load_csv, load_excel, load_json] )
result = Runner.run_sync( agent, 'Load data/sample.csv and summarize it.' )
print( result.final_output )
```

# Preprocessing Tools

## Normalize Text

```python
from fonky.tools import preprocess_normalize_text

value = preprocess_normalize_text.__wrapped__( text='Fonky PROVIDES reusable preprocessing.' )
print( value )
```

## Collapse Whitespace

```python
from fonky.tools import preprocess_collapse_whitespace

value = preprocess_collapse_whitespace.__wrapped__( text='Fonky     collapses      whitespace.' )
print( value )
```

## Remove Punctuation

```python
from fonky.tools import preprocess_remove_punctuation

value = preprocess_remove_punctuation.__wrapped__( text='Budget, execution: obligations; outlays!' )
print( value )
```

## Remove Stop Words

```python
from fonky.tools import preprocess_remove_stopwords

value = preprocess_remove_stopwords.__wrapped__( text='The analyst reviewed the report and the data.' )
print( value )
```

## Split Sentences

```python
from fonky.tools import preprocess_split_sentences

sentences = preprocess_split_sentences.__wrapped__( text='Fonky loads documents. Fonky preprocesses text.' )
print( sentences )
```

## Tiktoken

```python
from fonky.tools import preprocess_tiktokenize

df_tokens = preprocess_tiktokenize.__wrapped__( text='Fonky tokenization example.', encoding='cl100k_base' )
print( df_tokens )
```

## Frequency Distribution

```python
from fonky.tools import preprocess_create_frequency_distribution

tokens = ['budget', 'budget', 'outlays', 'obligations', 'budget']
df_frequency = preprocess_create_frequency_distribution.__wrapped__( tokens=tokens )
print( df_frequency )
```

## Vocabulary

```python
from fonky.tools import preprocess_create_vocabulary

tokens = ['budget', 'obligations', 'outlays', 'budget']
series_vocabulary = preprocess_create_vocabulary.__wrapped__( tokens=tokens )
print( series_vocabulary )
```

## NLTK Word Tokenization

```python
from fonky.tools import nltk_word_tokenizer

tokens = nltk_word_tokenizer.__wrapped__( text='Fonky performs NLTK tokenization.' )
print( tokens )
```

## NLTK Lemmatization

```python
from fonky.tools import nltk_word_lemmatizer

lemmas = nltk_word_lemmatizer.__wrapped__( text='cars studies running analyzed' )
print( lemmas )
```

## NLTK POS Tagging

```python
from fonky.tools import nltk_pos_tagger

tags = nltk_pos_tagger.__wrapped__( text='The analyst reviewed the financial report.' )
print( tags )
```

## NLTK Named Entity Recognition

```python
from fonky.tools import nltk_named_entity_recognition

entities = nltk_named_entity_recognition.__wrapped__( text='NASA operates the Goddard Space Flight Center in Maryland.' )
print( entities )
```

## Semantic Search

```python
from fonky.tools import preprocess_semantic_search

matches = preprocess_semantic_search.__wrapped__(
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

# Web Agents

## Web Fetch Agent

```python
from agents import Agent, Runner
from fonky.tools import fetch_web_page

agent = Agent( name='Web Reader', tools=[fetch_web_page] )
result = Runner.run_sync( agent, 'Fetch https://example.com and summarize the page.' )
print( result.final_output )
```

## Web Extraction Agent

```python
from agents import Agent, Runner
from fonky.tools import scrape_headings, scrape_hyperlinks, scrape_paragraphs, scrape_tables

agent = Agent(
    name='Web Extractor',
    tools=[scrape_headings, scrape_paragraphs, scrape_tables, scrape_hyperlinks] )

result = Runner.run_sync( agent, 'Extract headings and hyperlinks from https://example.com.' )
print( result.final_output )
```

## Web Crawl Agent

```python
from agents import Agent, Runner
from fonky.tools import crawl_web

agent = Agent( name='Site Crawler', tools=[crawl_web] )
result = Runner.run_sync( agent, 'Crawl https://example.com at shallow depth.' )
print( result.final_output )
```

# Research Agents

## ArXiv

```python
from agents import Agent, Runner
from fonky.tools import fetch_arxiv

agent = Agent( name='Academic Researcher', tools=[fetch_arxiv] )
result = Runner.run_sync( agent, 'Find papers about tool-using language models.' )
print( result.final_output )
```

## Wikipedia

```python
from agents import Agent, Runner
from fonky.tools import fetch_wikipedia

agent = Agent( name='Reference Assistant', tools=[fetch_wikipedia] )
result = Runner.run_sync( agent, 'Explain the history of the U.S. Census Bureau.' )
print( result.final_output )
```

## Google Search

```python
from agents import Agent, Runner
from fonky.tools import fetch_google_search

agent = Agent( name='Search Assistant', tools=[fetch_google_search] )
result = Runner.run_sync( agent, 'Find public resources explaining federal appropriations law.' )
print( result.final_output )
```

## Congress.gov

```python
from agents import Agent, Runner
from fonky.tools import fetch_congress

agent = Agent( name='Legislative Research Assistant', tools=[fetch_congress] )
result = Runner.run_sync( agent, 'Retrieve recent bills from the 119th Congress.' )
print( result.final_output )
```

## Data.gov

```python
from agents import Agent, Runner
from fonky.tools import fetch_gov_data

agent = Agent( name='Federal Dataset Finder', tools=[fetch_gov_data] )
result = Runner.run_sync( agent, 'Find datasets related to federal spending.' )
print( result.final_output )
```

# Environmental Agents

## Open Weather

```python
from agents import Agent, Runner
from fonky.tools import fetch_open_weather

agent = Agent( name='Weather Assistant', tools=[fetch_open_weather] )
result = Runner.run_sync( agent, 'Retrieve current weather for Arlington, Virginia.' )
print( result.final_output )
```

## Google Weather

```python
from agents import Agent, Runner
from fonky.tools import fetch_google_weather_current, fetch_google_weather_daily_forecast, fetch_google_weather_hourly_forecast

agent = Agent(
    name='Weather Planning Assistant',
    tools=[fetch_google_weather_current, fetch_google_weather_hourly_forecast, fetch_google_weather_daily_forecast] )

result = Runner.run_sync( agent, 'Retrieve the daily forecast for Arlington, Virginia.' )
print( result.final_output )
```

## USGS Earthquakes

```python
from agents import Agent, Runner
from fonky.tools import fetch_usgs_earthquakes

agent = Agent( name='Earthquake Analyst', tools=[fetch_usgs_earthquakes] )
result = Runner.run_sync( agent, 'Retrieve recent earthquakes.' )
print( result.final_output )
```

## USGS Water Data

```python
from agents import Agent, Runner
from fonky.tools import fetch_usgs_water_data

agent = Agent( name='Water Data Analyst', tools=[fetch_usgs_water_data] )
result = Runner.run_sync( agent, 'Find USGS water monitoring locations in Virginia.' )
print( result.final_output )
```

## Air Quality

```python
from agents import Agent, Runner
from fonky.tools import fetch_air_now, fetch_open_aq

agent = Agent( name='Air Quality Analyst', tools=[fetch_air_now, fetch_open_aq] )
result = Runner.run_sync( agent, 'Retrieve air-quality data near ZIP Code 22201.' )
print( result.final_output )
```

# Geospatial Agents

## Geocoding

```python
from agents import Agent, Runner
from fonky.tools import geocode_location

agent = Agent( name='Geocoding Assistant', tools=[geocode_location] )
result = Runner.run_sync( agent, 'Geocode 1600 Pennsylvania Avenue NW, Washington, DC.' )
print( result.final_output )
```

## Reverse Geocoding

```python
from agents import Agent, Runner
from fonky.tools import geocode_coordinates

agent = Agent( name='Reverse Geocoder', tools=[geocode_coordinates] )
result = Runner.run_sync( agent, 'Reverse geocode latitude 38.8977 and longitude -77.0365.' )
print( result.final_output )
```

## Address Validation

```python
from agents import Agent, Runner
from fonky.tools import validate_address

agent = Agent( name='Address Validator', tools=[validate_address] )
result = Runner.run_sync( agent, 'Validate 1600 Pennsylvania Avenue NW, Washington, DC.' )
print( result.final_output )
```

## Directions

```python
from agents import Agent, Runner
from fonky.tools import request_directions

agent = Agent( name='Directions Assistant', tools=[request_directions] )
result = Runner.run_sync( agent, 'Get driving directions from Arlington, Virginia to Baltimore, Maryland.' )
print( result.final_output )
```

# Demographic and Health Agents

## Census

```python
from agents import Agent, Runner
from fonky.tools import fetch_census_data

agent = Agent( name='Census Analyst', tools=[fetch_census_data] )
result = Runner.run_sync( agent, 'Retrieve state population data.' )
print( result.final_output )
```

## Global Health

```python
from agents import Agent, Runner
from fonky.tools import fetch_global_health_data

agent = Agent( name='Global Health Analyst', tools=[fetch_global_health_data] )
result = Runner.run_sync( agent, 'Retrieve the global health indicator registry.' )
print( result.final_output )
```

## PubMed

```python
from agents import Agent, Runner
from fonky.tools import load_pubmed

agent = Agent( name='Biomedical Research Assistant', tools=[load_pubmed] )
result = Runner.run_sync( agent, 'Find literature about machine learning in clinical decision support.' )
print( result.final_output )
```

# Astronomy and Space Agents

## Astroquery

```python
from agents import Agent, Runner
from fonky.tools import fetch_astro_query

agent = Agent( name='Astronomy Assistant', tools=[fetch_astro_query] )
result = Runner.run_sync( agent, 'Look up M31.' )
print( result.final_output )
```

## Near-Earth Objects

```python
from agents import Agent, Runner
from fonky.tools import fetch_nearby_objects

agent = Agent( name='Near Earth Object Assistant', tools=[fetch_nearby_objects] )
result = Runner.run_sync( agent, 'Retrieve near-Earth close approaches.' )
print( result.final_output )
```

## Space Weather

```python
from agents import Agent, Runner
from fonky.tools import fetch_space_weather

agent = Agent( name='Space Weather Assistant', tools=[fetch_space_weather] )
result = Runner.run_sync( agent, 'Retrieve recent coronal mass ejection data.' )
print( result.final_output )
```

# Cloud and Repository Agents

## Google Drive

```python
from agents import Agent, Runner
from fonky.tools import load_google_drive_file

agent = Agent( name='Drive Document Assistant', tools=[load_google_drive_file] )
result = Runner.run_sync( agent, 'Load the requested Google Drive file.' )
print( result.final_output )
```

## AWS S3

```python
from agents import Agent, Runner
from fonky.tools import load_aws_file

agent = Agent( name='S3 Document Assistant', tools=[load_aws_file] )
result = Runner.run_sync( agent, 'Load the requested S3 object.' )
print( result.final_output )
```

## Google Cloud Storage

```python
from agents import Agent, Runner
from fonky.tools import load_google_cloud_file

agent = Agent( name='Cloud Storage Assistant', tools=[load_google_cloud_file] )
result = Runner.run_sync( agent, 'Load the requested Google Cloud Storage object.' )
print( result.final_output )
```

## GitHub

```python
from agents import Agent, Runner
from fonky.tools import load_github

agent = Agent( name='Repository Reader', tools=[load_github] )
result = Runner.run_sync( agent, 'Load Markdown files from the requested repository.' )
print( result.final_output )
```

# Combined Workflows

## Research and Normalize

```python
from agents import Agent, Runner
from fonky.tools import fetch_wikipedia, preprocess_normalize_text

agent = Agent( name='Research Preparation Assistant', tools=[fetch_wikipedia, preprocess_normalize_text] )
result = Runner.run_sync( agent, 'Retrieve a short explanation of the federal budget process and normalize the text.' )
print( result.final_output )
```

## Load and Normalize

```python
from agents import Agent, Runner
from fonky.tools import load_text, preprocess_normalize_text

agent = Agent( name='Document Preparation Assistant', tools=[load_text, preprocess_normalize_text] )
result = Runner.run_sync( agent, 'Load data/sample.txt and normalize the text.' )
print( result.final_output )
```

## Web Extraction Workflow

```python
from agents import Agent, Runner
from fonky.tools import fetch_web_page, scrape_headings, scrape_hyperlinks, scrape_paragraphs

agent = Agent(
    name='Web Content Analyst',
    tools=[fetch_web_page, scrape_headings, scrape_paragraphs, scrape_hyperlinks] )

result = Runner.run_sync( agent, 'Inspect https://example.com and return its headings and links.' )
print( result.final_output )
```

# Production Controls

## Tool Scope

```python
tools=[
    fetch_arxiv,
    fetch_wikipedia,
]
```

## Credentials

```text
Environment variables
Cloud workload identity
Provider credential chain
Secret manager
```

## Direct Deterministic Execution

```python
from fonky.loaders import PdfLoader

loader = PdfLoader( )

documents = loader.load(
    path='data/report.pdf',
    mode='single',
    extract='plain',
    include=False,
    format='markdown-img' )
```

## Agent-Selected Execution

```python
from agents import Agent
from fonky.tools import load_pdf, load_word

agent = Agent(
    name='Document Router',
    tools=[
        load_pdf,
        load_word,
    ] )
```

# Validation

## Compile

```powershell
python -m compileall .\fonky
```

## Core Imports

```powershell
python -c "from fonky.fetchers import ArXiv; from fonky.loaders import PdfLoader; from fonky.scrapers import WebExtractor; from fonky.preprocessors import TextParser; print('ok')"
```

## Tool Imports

```powershell
python -c "from fonky.tools import fetch_arxiv, load_pdf, scrape_tables, preprocess_normalize_text; print('ok')"
```

## Dependency Check

```powershell
python -m pip check
```

## Tool Count

```python
import inspect
import fonky.tools as tools

count = sum(
    1
    for _, value in inspect.getmembers( tools )
    if value.__class__.__name__ == 'FunctionTool'
)

print( count )
```

```text
150
```

## MkDocs

```powershell
mkdocs build
mkdocs serve
```

```text
http://127.0.0.1:8000/
```

# Reference Files

| File | Scope |
|---|---|
| `README.md` | Installation, architecture, configuration, validation |
| `Tools.md` | Complete tool signatures and API documentation |
| `user-guide.md` | Usage patterns and examples |
