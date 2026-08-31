# 🧰 Fonky User Guide

## 📥 Import Tools

```python
from fonky.tools import fetch_arxiv
from fonky.tools import load_pdf
from fonky.tools import preprocess_normalize_text
from fonky.tools import scrape_tables
```

## 🤖 Register Tools with an Agent

```python
from agents import Agent

from fonky.tools import fetch_arxiv
from fonky.tools import fetch_wikipedia

agent = Agent(
    name='Research Assistant',
    instructions='Use the supplied Fonky tools when required.',
    tools=[
        fetch_arxiv,
        fetch_wikipedia,
    ] )
```

## ▶️ Run an Agent Synchronously

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
    'Find research on retrieval augmented generation.' )

print( result.final_output )
```

## ⏱️ Run an Agent Asynchronously

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

## 📡 Stream an Agent Run

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

## 🧩 Inspect a Tool Schema

```python
import json

from agents import FunctionTool

from fonky.tools import fetch_arxiv


if isinstance( fetch_arxiv, FunctionTool ):
    print( fetch_arxiv.name )
    print( fetch_arxiv.description )
    print( json.dumps( fetch_arxiv.params_json_schema, indent=2 ) )
```

## 🧪 Call the Wrapped Python Function Directly

```python
from fonky.tools import preprocess_normalize_text


value = preprocess_normalize_text.__wrapped__(
    text='  MULTIPLE    SPACES  ' )

print( value )
```

---

# 🔎 Research Tool Examples

## fetch_arxiv

```python
from agents import Agent, Runner

from fonky.tools import fetch_arxiv

agent = Agent(
    name='ArXiv Researcher',
    tools=[
        fetch_arxiv,
    ] )

result = Runner.run_sync(
    agent,
    'Search ArXiv for papers about retrieval augmented generation. Return five results.' )

print( result.final_output )
```

Direct wrapper test:

```python
from fonky.tools import fetch_arxiv

documents = fetch_arxiv.__wrapped__(
    question='retrieval augmented generation',
    max_documents=5,
    full_documents=False,
    include_metadata=True )

print( documents )
```

## fetch_wikipedia

```python
from agents import Agent, Runner

from fonky.tools import fetch_wikipedia

agent = Agent(
    name='Wikipedia Researcher',
    tools=[
        fetch_wikipedia,
    ] )

result = Runner.run_sync(
    agent,
    'Use Wikipedia to explain the U.S. Census Bureau.' )

print( result.final_output )
```

## fetch_google_search

```python
from agents import Agent, Runner

from fonky.tools import fetch_google_search

agent = Agent(
    name='Google Search Agent',
    tools=[
        fetch_google_search,
    ] )

result = Runner.run_sync(
    agent,
    'Find public resources explaining federal appropriations law.' )

print( result.final_output )
```

## fetch_gov_data

```python
from agents import Agent, Runner

from fonky.tools import fetch_gov_data

agent = Agent(
    name='Data.gov Agent',
    tools=[
        fetch_gov_data,
    ] )

result = Runner.run_sync(
    agent,
    'Find Data.gov datasets related to federal spending.' )

print( result.final_output )
```

## fetch_congress

```python
from agents import Agent, Runner

from fonky.tools import fetch_congress

agent = Agent(
    name='Congress.gov Agent',
    tools=[
        fetch_congress,
    ] )

result = Runner.run_sync(
    agent,
    'Retrieve recent bills from the 119th Congress.' )

print( result.final_output )
```

## fetch_internet_archive

```python
from agents import Agent, Runner

from fonky.tools import fetch_internet_archive

agent = Agent(
    name='Internet Archive Agent',
    tools=[
        fetch_internet_archive,
    ] )

result = Runner.run_sync(
    agent,
    'Search Internet Archive for historical federal budget materials.' )

print( result.final_output )
```

---

# 📄 Document Tool Examples

## load_text

```python
from agents import Agent, Runner

from fonky.tools import load_text

agent = Agent(
    name='Text File Agent',
    tools=[
        load_text,
    ] )

result = Runner.run_sync(
    agent,
    'Load data/sample.txt and summarize it.' )

print( result.final_output )
```

Direct wrapper test:

```python
from fonky.tools import load_text

documents = load_text.__wrapped__(
    path='data/sample.txt',
    encoding='utf-8' )

print( documents )
```

## load_pdf

```python
from agents import Agent, Runner

from fonky.tools import load_pdf

agent = Agent(
    name='PDF Agent',
    tools=[
        load_pdf,
    ] )

result = Runner.run_sync(
    agent,
    'Load data/report.pdf and summarize its findings.' )

print( result.final_output )
```

Direct wrapper test:

```python
from fonky.tools import load_pdf

documents = load_pdf.__wrapped__(
    path='data/report.pdf',
    mode='single',
    extract='plain',
    include=False,
    format='markdown-img' )

print( documents )
```

## load_word

```python
from agents import Agent, Runner

from fonky.tools import load_word

agent = Agent(
    name='Word Document Agent',
    tools=[
        load_word,
    ] )

result = Runner.run_sync(
    agent,
    'Load data/report.docx and summarize it.' )

print( result.final_output )
```

## load_csv

```python
from agents import Agent, Runner

from fonky.tools import load_csv

agent = Agent(
    name='CSV Agent',
    tools=[
        load_csv,
    ] )

result = Runner.run_sync(
    agent,
    'Load data/sample.csv and summarize the records.' )

print( result.final_output )
```

## load_excel

```python
from agents import Agent, Runner

from fonky.tools import load_excel

agent = Agent(
    name='Excel Agent',
    tools=[
        load_excel,
    ] )

result = Runner.run_sync(
    agent,
    'Load data/sample.xlsx and summarize the workbook content.' )

print( result.final_output )
```

## load_json

```python
from agents import Agent, Runner

from fonky.tools import load_json

agent = Agent(
    name='JSON Agent',
    tools=[
        load_json,
    ] )

result = Runner.run_sync(
    agent,
    'Load data/messages.json and summarize its content.' )

print( result.final_output )
```

## load_jupyter_notebook

```python
from agents import Agent, Runner

from fonky.tools import load_jupyter_notebook

agent = Agent(
    name='Notebook Agent',
    tools=[
        load_jupyter_notebook,
    ] )

result = Runner.run_sync(
    agent,
    'Load notebook/fonky.ipynb and summarize its cells and outputs.' )

print( result.final_output )
```

## Multi-Format Document Agent

```python
from agents import Agent, Runner

from fonky.tools import load_csv
from fonky.tools import load_excel
from fonky.tools import load_json
from fonky.tools import load_pdf
from fonky.tools import load_text
from fonky.tools import load_word

agent = Agent(
    name='Document Router',
    instructions='Select the appropriate loader for the requested file.',
    tools=[
        load_text,
        load_pdf,
        load_word,
        load_csv,
        load_excel,
        load_json,
    ] )

result = Runner.run_sync(
    agent,
    'Load data/report.pdf and summarize it.' )

print( result.final_output )
```

---

# 🌐 Web Tool Examples

## fetch_web_page

```python
from agents import Agent, Runner

from fonky.tools import fetch_web_page

agent = Agent(
    name='Web Fetch Agent',
    tools=[
        fetch_web_page,
    ] )

result = Runner.run_sync(
    agent,
    'Fetch https://example.com and summarize the page.' )

print( result.final_output )
```

## scrape_paragraphs

```python
from agents import Agent, Runner

from fonky.tools import scrape_paragraphs

agent = Agent(
    name='Paragraph Extractor',
    tools=[
        scrape_paragraphs,
    ] )

result = Runner.run_sync(
    agent,
    'Extract the paragraphs from https://example.com.' )

print( result.final_output )
```

Direct wrapper test:

```python
from fonky.tools import scrape_paragraphs

paragraphs = scrape_paragraphs.__wrapped__(
    uri='https://example.com' )

print( paragraphs )
```

## scrape_tables

```python
from agents import Agent, Runner

from fonky.tools import scrape_tables

agent = Agent(
    name='Table Extractor',
    tools=[
        scrape_tables,
    ] )

result = Runner.run_sync(
    agent,
    'Extract the tables from the supplied page.' )

print( result.final_output )
```

## scrape_headings

```python
from agents import Agent, Runner

from fonky.tools import scrape_headings

agent = Agent(
    name='Heading Extractor',
    tools=[
        scrape_headings,
    ] )

result = Runner.run_sync(
    agent,
    'Extract headings from https://example.com.' )

print( result.final_output )
```

## scrape_hyperlinks

```python
from agents import Agent, Runner

from fonky.tools import scrape_hyperlinks

agent = Agent(
    name='Hyperlink Extractor',
    tools=[
        scrape_hyperlinks,
    ] )

result = Runner.run_sync(
    agent,
    'Extract hyperlinks from https://example.com.' )

print( result.final_output )
```

## crawl_web

```python
from agents import Agent, Runner

from fonky.tools import crawl_web

agent = Agent(
    name='Crawler Agent',
    tools=[
        crawl_web,
    ] )

result = Runner.run_sync(
    agent,
    'Crawl https://example.com at shallow depth.' )

print( result.final_output )
```

## Combined Web Agent

```python
from agents import Agent, Runner

from fonky.tools import fetch_web_page
from fonky.tools import scrape_headings
from fonky.tools import scrape_hyperlinks
from fonky.tools import scrape_paragraphs
from fonky.tools import scrape_tables

agent = Agent(
    name='Web Analysis Agent',
    tools=[
        fetch_web_page,
        scrape_headings,
        scrape_paragraphs,
        scrape_tables,
        scrape_hyperlinks,
    ] )

result = Runner.run_sync(
    agent,
    'Inspect https://example.com and return its headings, paragraphs, tables, and links.' )

print( result.final_output )
```

---

# 🧹 Preprocessing Tool Examples

## preprocess_normalize_text

```python
from fonky.tools import preprocess_normalize_text

value = preprocess_normalize_text.__wrapped__(
    text='Fonky PROVIDES reusable preprocessing.' )

print( value )
```

## preprocess_collapse_whitespace

```python
from fonky.tools import preprocess_collapse_whitespace

value = preprocess_collapse_whitespace.__wrapped__(
    text='Fonky     collapses      repeated whitespace.' )

print( value )
```

## preprocess_remove_punctuation

```python
from fonky.tools import preprocess_remove_punctuation

value = preprocess_remove_punctuation.__wrapped__(
    text='Budget, execution: obligations; outlays!' )

print( value )
```

## preprocess_remove_stopwords

```python
from fonky.tools import preprocess_remove_stopwords

value = preprocess_remove_stopwords.__wrapped__(
    text='The analyst reviewed the report and the supporting data.' )

print( value )
```

## preprocess_split_sentences

```python
from fonky.tools import preprocess_split_sentences

sentences = preprocess_split_sentences.__wrapped__(
    text='Fonky loads documents. Fonky preprocesses text.' )

print( sentences )
```

## preprocess_tiktokenize

```python
from fonky.tools import preprocess_tiktokenize

df_tokens = preprocess_tiktokenize.__wrapped__(
    text='Fonky tokenization example.',
    encoding='cl100k_base' )

print( df_tokens )
```

## preprocess_create_frequency_distribution

```python
from fonky.tools import preprocess_create_frequency_distribution

df_frequency = preprocess_create_frequency_distribution.__wrapped__(
    tokens=[
        'budget',
        'budget',
        'outlays',
        'obligations',
        'budget',
    ] )

print( df_frequency )
```

## preprocess_create_vocabulary

```python
from fonky.tools import preprocess_create_vocabulary

series_vocabulary = preprocess_create_vocabulary.__wrapped__(
    tokens=[
        'budget',
        'obligations',
        'outlays',
        'budget',
    ] )

print( series_vocabulary )
```

## preprocess_semantic_search

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

## NLTK Tools

```python
from fonky.tools import nltk_named_entity_recognition
from fonky.tools import nltk_pos_tagger
from fonky.tools import nltk_word_lemmatizer
from fonky.tools import nltk_word_tokenizer

tokens = nltk_word_tokenizer.__wrapped__(
    text='NASA operates the Goddard Space Flight Center.' )

lemmas = nltk_word_lemmatizer.__wrapped__(
    text='cars studies running analyzed' )

tags = nltk_pos_tagger.__wrapped__(
    text='The analyst reviewed the financial report.' )

entities = nltk_named_entity_recognition.__wrapped__(
    text='NASA operates the Goddard Space Flight Center in Maryland.' )
```

## Preprocessing Agent

```python
from agents import Agent, Runner

from fonky.tools import preprocess_normalize_text
from fonky.tools import preprocess_remove_punctuation
from fonky.tools import preprocess_remove_stopwords
from fonky.tools import preprocess_split_sentences

agent = Agent(
    name='Preprocessing Agent',
    tools=[
        preprocess_normalize_text,
        preprocess_remove_punctuation,
        preprocess_remove_stopwords,
        preprocess_split_sentences,
    ] )

result = Runner.run_sync(
    agent,
    'Normalize this text, remove punctuation, remove stop words, and split it into sentences: '
    '"The analysts are reviewing the budget, and the financial reports."' )

print( result.final_output )
```

---

# 🌦️ Environmental Tool Examples

## fetch_open_weather

```python
from agents import Agent, Runner

from fonky.tools import fetch_open_weather

agent = Agent(
    name='Weather Agent',
    tools=[
        fetch_open_weather,
    ] )

result = Runner.run_sync(
    agent,
    'Retrieve current weather for Arlington, Virginia.' )

print( result.final_output )
```

## fetch_usgs_earthquakes

```python
from agents import Agent, Runner

from fonky.tools import fetch_usgs_earthquakes

agent = Agent(
    name='Earthquake Agent',
    tools=[
        fetch_usgs_earthquakes,
    ] )

result = Runner.run_sync(
    agent,
    'Retrieve recent earthquakes.' )

print( result.final_output )
```

## fetch_usgs_water_data

```python
from agents import Agent, Runner

from fonky.tools import fetch_usgs_water_data

agent = Agent(
    name='Water Data Agent',
    tools=[
        fetch_usgs_water_data,
    ] )

result = Runner.run_sync(
    agent,
    'Find USGS water monitoring locations in Virginia.' )

print( result.final_output )
```

## fetch_air_now

```python
from agents import Agent, Runner

from fonky.tools import fetch_air_now

agent = Agent(
    name='AirNow Agent',
    tools=[
        fetch_air_now,
    ] )

result = Runner.run_sync(
    agent,
    'Retrieve current air-quality observations for ZIP Code 22201.' )

print( result.final_output )
```

## fetch_open_aq

```python
from agents import Agent, Runner

from fonky.tools import fetch_open_aq

agent = Agent(
    name='OpenAQ Agent',
    tools=[
        fetch_open_aq,
    ] )

result = Runner.run_sync(
    agent,
    'Retrieve air-quality locations near Arlington, Virginia.' )

print( result.final_output )
```

---

# 🗺️ Geospatial Tool Examples

## geocode_location

```python
from agents import Agent, Runner

from fonky.tools import geocode_location

agent = Agent(
    name='Geocoding Agent',
    tools=[
        geocode_location,
    ] )

result = Runner.run_sync(
    agent,
    'Geocode 1600 Pennsylvania Avenue NW, Washington, DC.' )

print( result.final_output )
```

## geocode_coordinates

```python
from agents import Agent, Runner

from fonky.tools import geocode_coordinates

agent = Agent(
    name='Reverse Geocoding Agent',
    tools=[
        geocode_coordinates,
    ] )

result = Runner.run_sync(
    agent,
    'Reverse geocode latitude 38.8977 and longitude -77.0365.' )

print( result.final_output )
```

## validate_address

```python
from agents import Agent, Runner

from fonky.tools import validate_address

agent = Agent(
    name='Address Validation Agent',
    tools=[
        validate_address,
    ] )

result = Runner.run_sync(
    agent,
    'Validate 1600 Pennsylvania Avenue NW, Washington, DC.' )

print( result.final_output )
```

## request_directions

```python
from agents import Agent, Runner

from fonky.tools import request_directions

agent = Agent(
    name='Directions Agent',
    tools=[
        request_directions,
    ] )

result = Runner.run_sync(
    agent,
    'Get driving directions from Arlington, Virginia to Baltimore, Maryland.' )

print( result.final_output )
```

---

# 👥 Demographic and Health Tool Examples

## fetch_census_data

```python
from agents import Agent, Runner

from fonky.tools import fetch_census_data

agent = Agent(
    name='Census Agent',
    tools=[
        fetch_census_data,
    ] )

result = Runner.run_sync(
    agent,
    'Retrieve state population data.' )

print( result.final_output )
```

## fetch_socrata

```python
from agents import Agent, Runner

from fonky.tools import fetch_socrata

agent = Agent(
    name='Socrata Agent',
    tools=[
        fetch_socrata,
    ] )

result = Runner.run_sync(
    agent,
    'Retrieve records from the requested Socrata dataset.' )

print( result.final_output )
```

## fetch_global_health_data

```python
from agents import Agent, Runner

from fonky.tools import fetch_global_health_data

agent = Agent(
    name='Global Health Agent',
    tools=[
        fetch_global_health_data,
    ] )

result = Runner.run_sync(
    agent,
    'Retrieve the global health indicator registry.' )

print( result.final_output )
```

## load_pubmed

```python
from agents import Agent, Runner

from fonky.tools import load_pubmed

agent = Agent(
    name='PubMed Agent',
    tools=[
        load_pubmed,
    ] )

result = Runner.run_sync(
    agent,
    'Find biomedical literature about machine learning in clinical decision support.' )

print( result.final_output )
```

---

# 🔭 Astronomy and Space Tool Examples

## fetch_astro_query

```python
from agents import Agent, Runner

from fonky.tools import fetch_astro_query

agent = Agent(
    name='Astronomy Agent',
    tools=[
        fetch_astro_query,
    ] )

result = Runner.run_sync(
    agent,
    'Look up M31.' )

print( result.final_output )
```

## fetch_nearby_objects

```python
from agents import Agent, Runner

from fonky.tools import fetch_nearby_objects

agent = Agent(
    name='Near Earth Object Agent',
    tools=[
        fetch_nearby_objects,
    ] )

result = Runner.run_sync(
    agent,
    'Retrieve near-Earth close approaches.' )

print( result.final_output )
```

## fetch_space_weather

```python
from agents import Agent, Runner

from fonky.tools import fetch_space_weather

agent = Agent(
    name='Space Weather Agent',
    tools=[
        fetch_space_weather,
    ] )

result = Runner.run_sync(
    agent,
    'Retrieve recent coronal mass ejection data.' )

print( result.final_output )
```

---

# ☁️ Cloud and Repository Tool Examples

## load_google_drive_file

```python
from agents import Agent, Runner

from fonky.tools import load_google_drive_file

agent = Agent(
    name='Google Drive File Agent',
    tools=[
        load_google_drive_file,
    ] )

result = Runner.run_sync(
    agent,
    'Load the requested Google Drive file.' )

print( result.final_output )
```

## load_google_drive_folder

```python
from agents import Agent, Runner

from fonky.tools import load_google_drive_folder

agent = Agent(
    name='Google Drive Folder Agent',
    tools=[
        load_google_drive_folder,
    ] )

result = Runner.run_sync(
    agent,
    'Load documents from the requested Google Drive folder.' )

print( result.final_output )
```

## load_aws_file

```python
from agents import Agent, Runner

from fonky.tools import load_aws_file

agent = Agent(
    name='S3 File Agent',
    tools=[
        load_aws_file,
    ] )

result = Runner.run_sync(
    agent,
    'Load the requested S3 object.' )

print( result.final_output )
```

## load_aws_bucket

```python
from agents import Agent, Runner

from fonky.tools import load_aws_bucket

agent = Agent(
    name='S3 Bucket Agent',
    tools=[
        load_aws_bucket,
    ] )

result = Runner.run_sync(
    agent,
    'Load documents from the requested S3 prefix.' )

print( result.final_output )
```

## load_google_cloud_file

```python
from agents import Agent, Runner

from fonky.tools import load_google_cloud_file

agent = Agent(
    name='Google Cloud Storage Agent',
    tools=[
        load_google_cloud_file,
    ] )

result = Runner.run_sync(
    agent,
    'Load the requested Google Cloud Storage object.' )

print( result.final_output )
```

## load_github

```python
from agents import Agent, Runner

from fonky.tools import load_github

agent = Agent(
    name='GitHub Loader Agent',
    tools=[
        load_github,
    ] )

result = Runner.run_sync(
    agent,
    'Load Markdown files from the requested repository.' )

print( result.final_output )
```

---

# 🔗 Combined Tool Examples

## Research and Preprocessing

```python
from agents import Agent, Runner

from fonky.tools import fetch_wikipedia
from fonky.tools import preprocess_normalize_text

agent = Agent(
    name='Research Preparation Agent',
    tools=[
        fetch_wikipedia,
        preprocess_normalize_text,
    ] )

result = Runner.run_sync(
    agent,
    'Retrieve a short explanation of the federal budget process and normalize the text.' )

print( result.final_output )
```

## Load and Preprocess

```python
from agents import Agent, Runner

from fonky.tools import load_text
from fonky.tools import preprocess_normalize_text

agent = Agent(
    name='Document Preparation Agent',
    tools=[
        load_text,
        preprocess_normalize_text,
    ] )

result = Runner.run_sync(
    agent,
    'Load data/sample.txt and normalize the text.' )

print( result.final_output )
```

## Research Router

```python
from agents import Agent, Runner

from fonky.tools import fetch_arxiv
from fonky.tools import fetch_google_search
from fonky.tools import fetch_wikipedia

agent = Agent(
    name='Research Router',
    instructions=(
        'Use ArXiv for scholarly literature, Wikipedia for background, '
        'and Google Search for current web discovery.'
    ),
    tools=[
        fetch_arxiv,
        fetch_wikipedia,
        fetch_google_search,
    ] )

result = Runner.run_sync(
    agent,
    'Research retrieval augmented generation.' )

print( result.final_output )
```

## Environmental Router

```python
from agents import Agent, Runner

from fonky.tools import fetch_air_now
from fonky.tools import fetch_open_weather
from fonky.tools import fetch_usgs_earthquakes
from fonky.tools import fetch_usgs_water_data

agent = Agent(
    name='Environmental Data Router',
    tools=[
        fetch_open_weather,
        fetch_usgs_earthquakes,
        fetch_usgs_water_data,
        fetch_air_now,
    ] )

result = Runner.run_sync(
    agent,
    'Retrieve recent earthquake information.' )

print( result.final_output )
```

---

# ✅ Wrapper Validation

## Import Validation

```powershell
python -c "from fonky.tools import fetch_arxiv, load_pdf, scrape_tables, preprocess_normalize_text; print('ok')"
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

Expected:

```text
150
```

## Schema Validation

```python
import json

from agents import FunctionTool

from fonky.tools import fetch_arxiv

assert isinstance( fetch_arxiv, FunctionTool )

print( json.dumps(
    fetch_arxiv.params_json_schema,
    indent=2 ) )
```

## Direct Wrapper Validation

```python
from fonky.tools import preprocess_normalize_text

result = preprocess_normalize_text.__wrapped__(
    text='  TEST    VALUE  ' )

print( result )
```

## Agent Execution Validation

```python
from agents import Agent, Runner

from fonky.tools import preprocess_normalize_text

agent = Agent(
    name='Wrapper Validation Agent',
    tools=[
        preprocess_normalize_text,
    ] )

result = Runner.run_sync(
    agent,
    'Normalize the text "  TEST    VALUE  ".' )

print( result.final_output )
```

# 📚 Reference

```text
Tools.md
```
