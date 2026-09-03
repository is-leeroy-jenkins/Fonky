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

## Anthropic Claude

Fonky exposes native Anthropic tool definitions through `fonky.claude.tools`. Each public function
is decorated with `@beta_tool` and delegates directly to the canonical Fonky implementation.

```python
from anthropic import Anthropic

from fonky.claude.tools import fetch_arxiv
from fonky.claude.tools import fetch_cse_search
from fonky.claude.tools import fetch_wikipedia

client = Anthropic( )

tools = [
    fetch_arxiv.to_dict( ),
    fetch_cse_search.to_dict( ),
    fetch_wikipedia.to_dict( ),
]

response = client.beta.messages.create(
    model='claude-sonnet-4-6',
    max_tokens=4096,
    tools=tools,
    messages=[
        {
            'role': 'user',
            'content': 'Research retrieval augmented generation.',
        },
    ] )

print( response )
```

The `to_dict()` method returns the Anthropic tool declaration generated from the decorated Python
function's typed signature and documentation. When Claude returns a `tool_use` block, execute the
corresponding Fonky callable locally and return the result through the normal Anthropic tool-result
message flow.

!!! note "Structured tool results"
    Anthropic's automatic Tool Runner expects tool results to be strings or supported Anthropic
    content blocks. Fonky preserves the canonical return types of its tools, including dictionaries,
    DataFrames, NumPy arrays, and document collections. Serialize structured results before sending
    them back to Claude when using a workflow that requires Anthropic-compatible tool-result content.

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
