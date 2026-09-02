# Provider Setup

## OpenAI Agents SDK

```python
from agents import Agent, Runner

from fonky.gpt.tools import fetch_arxiv
from fonky.gpt.tools import fetch_cse_search
from fonky.gpt.tools import fetch_wikipedia

agent = Agent(
    name='Research Assistant',
    instructions='Use the supplied Fonky tools when external retrieval is required.',
    tools=[
        fetch_arxiv,
        fetch_cse_search,
        fetch_wikipedia,
    ] )

result = Runner.run_sync(
    agent,
    'Research retrieval augmented generation.' )

print( result.final_output )
```

## Google ADK

```python
from google.adk.agents import Agent

from fonky.gemini.tools import fetch_arxiv
from fonky.gemini.tools import fetch_cse_search
from fonky.gemini.tools import fetch_wikipedia

agent = Agent(
    name='research_assistant',
    model='gemini-3.7-flash',
    instruction='Use the supplied Fonky tools when external retrieval is required.',
    tools=[
        fetch_arxiv,
        fetch_cse_search,
        fetch_wikipedia,
    ] )
```

Google ADK accepts the Fonky callables directly in the agent `tools` collection.

## xAI Grok

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

The `*_tool` object is the xAI declaration. The corresponding operationally-prefixed callable
executes the local Fonky implementation.

## LangChain

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

Invoke a LangChain tool directly:

```python
result = fetch_cse_search.invoke(
    {
        'keywords': 'federal appropriations law',
        'results': 5,
    } )

print( result )
```

Inspect the parsed tool schema:

```python
print( fetch_cse_search.args_schema.model_json_schema( ) )
```
