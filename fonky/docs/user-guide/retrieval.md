# Retrieval

## Google Programmable Search Engine

```python
from fonky.gemini.tools import fetch_cse_search

results = fetch_cse_search(
    keywords='federal appropriations law',
    results=5 )

print( results )
```

## ArXiv

```python
from fonky.gemini.tools import fetch_arxiv

documents = fetch_arxiv(
    question='retrieval augmented generation',
    max_documents=5,
    full_documents=False,
    include_metadata=True )

print( documents )
```

## Wikipedia

```python
from fonky.gemini.tools import fetch_wikipedia

documents = fetch_wikipedia(
    question='Congressional Budget and Impoundment Control Act' )

print( documents )
```

## Data.gov

```python
from fonky.gemini.tools import fetch_gov_data

results = fetch_gov_data(
    mode='search',
    query='federal spending',
    page_size=10 )

print( results )
```

## Congress.gov

```python
from fonky.gemini.tools import fetch_congress

results = fetch_congress(
    mode='bills',
    congress=119,
    limit=10 )

print( results )
```

Provider packages expose the same retrieval operation names. Change only the provider import path
when the active agent framework changes.
