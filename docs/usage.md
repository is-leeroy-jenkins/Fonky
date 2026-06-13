# ðŸ§° Usage

This page shows practical Fonky usage patterns with emphasis on the **AI tooling layer**: converting
existing Fonky functions and methods into structured tools, exporting those tools to
provider-compatible schemas, executing tool calls, and returning JSON-safe results.

Fonkyâ€™s AI tooling functionality is centered on `models.ToolDef`.



## ðŸŽ¯ What the AI Tooling Layer Does

Fonky does not require every loader, fetcher, scraper, or processor to be rewritten for an AI agent.
Instead, it wraps existing Python callables as structured tools.

The tooling flow is:

```text id="tooling_flow"
Python function or class method
    â†“
ToolDef
    â†“
JSON-schema parameter contract
    â†“
OpenAI, Gemini, or Grok-compatible schema
    â†“
Tool call arguments
    â†“
Fonky callable execution
    â†“
JSON-safe result envelope
```

The primary class is:

```python id="primary_tooling_import"
from models import ToolDef
```

For the current flat source layout, imports use root-level modules:

```python id="flat_usage_imports"
from models import ToolDef
from loaders import TextLoader
from processors import TextParser
```

If Fonky is later moved into a package folder, imports would become:

```python id="package_usage_imports"
from fonky.models import ToolDef
from fonky.loaders import TextLoader
from fonky.processors import TextParser
```



## ðŸ§  ToolDef Responsibilities

`ToolDef` performs five core jobs:

| Capability          | Description                                                                                               |
| ------------------- | --------------------------------------------------------------------------------------------------------- |
| Build tool metadata | Stores tool name, description, category, source module, source class, and method name.                    |
| Infer parameters    | Reads the callable signature and builds a JSON-schema-like parameter contract.                            |
| Export schemas      | Produces provider-compatible schema dictionaries for OpenAI, Gemini, and Grok-style tool calling.         |
| Execute calls       | Resolves and calls the underlying function or method with keyword arguments.                              |
| Serialize results   | Converts documents, Pydantic models, dictionaries, lists, and primitive values into JSON-safe structures. |



## ðŸ§ª Minimal Tool from a Plain Function

Start with a normal Python function:

```python id="plain_function_tool_source"
from models import ToolDef


def summarize_text(text: str, max_words: int = 50) -> str:
	"""Summarize text using a simple word limit.

	Purpose:
		Provides a small deterministic function that can be exposed as an AI-callable tool.

	Args:
		text (str): Source text to summarize.
		max_words (int): Maximum number of words to return.

	Returns:
		str: Truncated summary text.
	"""
	words = text.split()
	return " ".join(words[:max_words])
```

Wrap it as a `ToolDef`:

```python id="plain_function_tooldef"
tool = ToolDef.from_callable(
	function=summarize_text,
	name="summarize_text",
	description="Summarize text using a maximum word count.",
	category="text"
)

print(tool.to_dict())
```

Call it directly:

```python id="plain_function_tool_call"
result = tool.call(
	{
		"text": "Fonky exposes loaders, fetchers, scrapers, processors, and models as reusable AI tools.",
		"max_words": 8
	}
)

print("Succeeded:", result.get("ok"))
print("Tool:", result.get("name"))
print("Data:", result.get("data"))
print("Error:", result.get("error"))
```

Expected result shape:

```text id="plain_function_tool_result_shape"
{
    "ok": true,
    "name": "summarize_text",
    "data": "Fonky exposes loaders, fetchers, scrapers, processors, and",
    "error": null,
    "metadata": {
        "category": "text",
        "source_module": "...",
        "source_class": null,
        "method": null,
        "callable_name": "summarize_text"
    }
}
```



## ðŸ“„ Tool from a Fonky Loader Method

Fonky loaders can be exposed as AI-callable tools.

Create a test file:

```powershell id="create_usage_sample_file"
New-Item -ItemType Directory -Force .\data | Out-Null
"Fonky can load documents and expose the loader as an AI tool." | Set-Content .\data\sample.txt -Encoding UTF8
```

Create a tool from `TextLoader.load`:

```python id="text_loader_tooldef"
from loaders import TextLoader
from models import ToolDef

loader = TextLoader()

load_text_tool = ToolDef.from_method(
	target=loader,
	method="load",
	name="load_text_file",
	description="Load a local text file into document objects.",
	category="documents"
)

print(load_text_tool.to_dict())
```

Call the tool:

```python id="text_loader_tool_call"
result = load_text_tool.call(
	{
		"path": "data/sample.txt",
		"encoding": "utf-8"
	}
)

print("Succeeded:", result.get("ok"))

if result.get("ok"):
	data = result.get("data")
	for document in data:
		print("Metadata:", document.get("metadata"))
		print("Content:", document.get("page_content"))
		break
else:
	print("Error:", result.get("error"))
```

The returned `Document` objects are serialized into dictionaries with:

```text id="document_serialized_shape"
page_content
metadata
```



## âœ‚ï¸ Tool from a Document Split Method

A loader instance can also expose its split method after documents are loaded.

```python id="split_tool_example"
from loaders import TextLoader
from models import ToolDef

loader = TextLoader()

loader.load(
	path="data/sample.txt",
	encoding="utf-8"
)

split_tool = ToolDef.from_method(
	target=loader,
	method="split",
	name="split_loaded_documents",
	description="Split loaded documents into smaller chunks.",
	category="documents"
)

result = split_tool.call(
	{
		"chunk": 500,
		"overlap": 50
	}
)

print("Succeeded:", result.get("ok"))

if result.get("ok"):
	chunks = result.get("data")
	print("Chunk count:", len(chunks))

	for chunk in chunks:
		print(chunk.get("page_content"))
		break
else:
	print(result.get("error"))
```

This pattern allows an AI agent to call a loader first, then call a splitter against the same loader
instance.



## ðŸ§¹ Tool from a Text Processor

Fonky processors can be exposed as deterministic cleaning, normalization, tokenization, or chunking
tools.

Example using a text-cleaning method:

```python id="processor_tool_example"
from models import ToolDef
from processors import TextParser

parser = TextParser()

clean_tool = ToolDef.from_method(
	target=parser,
	method="clean_text",
	name="clean_text",
	description="Clean raw text for downstream analysis.",
	category="processors"
)

result = clean_tool.call(
	{
		"text": "  Fonky     cleans\n\ntext before analysis.  "
	}
)

print("Succeeded:", result.get("ok"))
print("Cleaned:", result.get("data"))
```

If the method name differs in the active `processors.py`, use the same pattern with the exact method
name exposed by that class.



## ðŸ§° Build a Small Tool Registry

A tool registry is a normal Python dictionary keyed by tool name.

```python id="tool_registry_example"
from loaders import TextLoader
from models import ToolDef


def count_words(text: str) -> int:
	"""Count words in a text value.

	Purpose:
		Provides a small deterministic utility that can be exposed to an AI agent.

	Args:
		text (str): Text to count.

	Returns:
		int: Number of whitespace-separated words.
	"""
	return len(text.split())


loader = TextLoader()

tools = [
	ToolDef.from_method(
		target=loader,
		method="load",
		name="load_text_file",
		description="Load a local text file into document objects.",
		category="documents"
	),
	ToolDef.from_callable(
		function=count_words,
		name="count_words",
		description="Count words in a text value.",
		category="text"
	)
]

tool_registry = {
	tool.name: tool
	for tool in tools
}

print("Available tools:")

for tool_name in tool_registry:
	print("-", tool_name)
```



## ðŸ“¦ Export Tool Schemas

Fonky can export tool schemas for different AI providers.

Create a tool:

```python id="create_exportable_tool"
from models import ToolDef


def lookup_policy_topic(topic: str, detail_level: str = "summary") -> dict:
	"""Look up a policy topic.

	Purpose:
		Provides a simple structured function that demonstrates schema generation for
		AI tool calling.

	Args:
		topic (str): Topic to look up.
		detail_level (str): Requested detail level.

	Returns:
		dict: Structured topic response.
	"""
	return {
		"topic": topic,
		"detail_level": detail_level,
		"summary": f"Prepared summary for {topic}."
	}


tool = ToolDef.from_callable(
	function=lookup_policy_topic,
	name="lookup_policy_topic",
	description="Look up a policy topic and return a structured summary.",
	category="policy"
)
```

Export a provider-neutral dictionary:

```python id="export_provider_neutral"
provider_neutral = tool.to_dict()

print(provider_neutral)
```

Export an OpenAI-compatible function tool schema:

```python id="export_openai_schema"
openai_schema = tool.to_openai()

print(openai_schema)
```

Export a Gemini-compatible function declaration:

```python id="export_gemini_schema"
gemini_schema = tool.to_gemini()

print(gemini_schema)
```

Export a Grok-compatible function tool schema:

```python id="export_grok_schema"
grok_schema = tool.to_grok()

print(grok_schema)
```



## ðŸ§¾ OpenAI-Compatible Schema Shape

`to_openai()` returns a schema shaped like:

```text id="openai_schema_shape"
{
    "type": "function",
    "function": {
        "name": "...",
        "description": "...",
        "parameters": {
            "type": "object",
            "properties": {
                "...": {
                    "type": "..."
                }
            },
            "required": [...]
        },
        "strict": true
    }
}
```

Example:

```python id="print_openai_schema"
schema = tool.to_openai()

function_block = schema.get("function")
parameters = function_block.get("parameters")

print("Tool name:", function_block.get("name"))
print("Description:", function_block.get("description"))
print("Required:", parameters.get("required"))
```



## ðŸ§¾ Gemini-Compatible Schema Shape

`to_gemini()` returns a function declaration shaped like:

```text id="gemini_schema_shape"
{
    "name": "...",
    "description": "...",
    "parameters": {
        "type": "object",
        "properties": {
            "...": {
                "type": "..."
            }
        },
        "required": [...]
    }
}
```

Example:

```python id="print_gemini_schema"
schema = tool.to_gemini()

print("Tool name:", schema.get("name"))
print("Parameters:", schema.get("parameters"))
```



## ðŸ§¾ Grok-Compatible Schema Shape

`to_grok()` currently follows the same function-tool shape as `to_openai()`.

```python id="print_grok_schema"
schema = tool.to_grok()

function_block = schema.get("function")

print("Tool name:", function_block.get("name"))
print("Description:", function_block.get("description"))
```



## ðŸ” Provider-Neutral Tool Dispatch

Most AI providers return a tool name and JSON arguments when the model chooses a tool. Fonky can
execute that request through a registry.

Example model-selected call payload:

```python id="model_selected_call_payload"
model_selected_call = {
	"name": "count_words",
	"arguments": {
		"text": "Fonky exposes Python methods as AI-callable tools."
	}
}
```

Dispatch the call:

```python id="provider_neutral_dispatch"
tool_name = model_selected_call.get("name")
arguments = model_selected_call.get("arguments") or { }

selected_tool = tool_registry.get(tool_name)

if selected_tool is None:
	result = {
		"ok": False,
		"name": tool_name,
		"data": None,
		"error": {
			"type": "ToolNotFound",
			"message": f"No registered tool named {tool_name}."
		},
		"metadata": { }
	}
else:
	result = selected_tool.call(arguments)

print(result)
```

This is the core integration point between an AI modelâ€™s tool-selection response and Fonkyâ€™s actual
Python execution layer.



## ðŸ¤– Minimal Agent-Style Loop

This example shows a provider-neutral agent loop. It does not depend on a specific model SDK.

```python id="minimal_agent_loop"
from models import ToolDef


def count_words(text: str) -> int:
	"""Count words in text.

	Purpose:
		Provides a deterministic word-count tool for an AI agent.

	Args:
		text (str): Text to count.

	Returns:
		int: Number of words.
	"""
	return len(text.split())


def uppercase_text(text: str) -> str:
	"""Uppercase text.

	Purpose:
		Provides a deterministic text transformation tool for an AI agent.

	Args:
		text (str): Text to transform.

	Returns:
		str: Uppercase text.
	"""
	return text.upper()


tools = [
	ToolDef.from_callable(
		function=count_words,
		name="count_words",
		description="Count words in text.",
		category="text"
	),
	ToolDef.from_callable(
		function=uppercase_text,
		name="uppercase_text",
		description="Convert text to uppercase.",
		category="text"
	)
]

tool_registry = {
	tool.name: tool
	for tool in tools
}

provider_tool_schemas = [
	tool.to_openai()
	for tool in tools
]

print("Tool schemas available to model:")
for schema in provider_tool_schemas:
	function_block = schema.get("function")
	print("-", function_block.get("name"))

model_selected_calls = [
	{
		"name": "count_words",
		"arguments": {
			"text": "Fonky provides AI-ready tooling."
		}
	},
	{
		"name": "uppercase_text",
		"arguments": {
			"text": "Fonky provides AI-ready tooling."
		}
	}
]

for selected_call in model_selected_calls:
	tool_name = selected_call.get("name")
	arguments = selected_call.get("arguments") or { }
	tool = tool_registry.get(tool_name)

	if tool is None:
		print("Missing tool:", tool_name)
		continue

	result = tool.call(arguments)
	print("Tool result:", result)
```



## ðŸ§  Tooling Pattern for Loader + Processor Workflows

This pattern exposes a loader and a text utility together.

```python id="loader_processor_toolkit"
from loaders import TextLoader
from models import ToolDef


def first_document_text(documents: list[dict]) -> str:
	"""Return the first serialized document text.

	Purpose:
		Extracts the first page_content value from a serialized document list.

	Args:
		documents (list[dict]): Serialized document dictionaries.

	Returns:
		str: First document text or an empty string.
	"""
	for document in documents:
		page_content = document.get("page_content")
		if page_content:
			return page_content

	return ""


loader = TextLoader()

load_text_file = ToolDef.from_method(
	target=loader,
	method="load",
	name="load_text_file",
	description="Load a local text file into document objects.",
	category="documents"
)

extract_first_text = ToolDef.from_callable(
	function=first_document_text,
	name="first_document_text",
	description="Extract the first page_content value from serialized document output.",
	category="documents"
)

load_result = load_text_file.call(
	{
		"path": "data/sample.txt",
		"encoding": "utf-8"
	}
)

if load_result.get("ok"):
	extract_result = extract_first_text.call(
		{
			"documents": load_result.get("data")
		}
	)

	print(extract_result.get("data"))
else:
	print(load_result.get("error"))
```



## ðŸŒ Tooling Pattern for Fetchers

Fetcher methods can be exposed the same way as loader methods.

Use the exact class and method available in your active `fetchers.py`.

```python id="fetcher_tool_pattern"
from models import ToolDef
from fetchers import SomeFetcherClass

fetcher = SomeFetcherClass()

fetch_tool = ToolDef.from_method(
	target=fetcher,
	method="some_fetch_method",
	name="fetch_external_data",
	description="Fetch external data using a Fonky fetcher method.",
	category="fetchers"
)

schema = fetch_tool.to_openai()

print(schema)
```

Call the tool with the methodâ€™s actual arguments:

```python id="fetcher_tool_call_pattern"
result = fetch_tool.call(
	{
		"query": "example",
		"limit": 10
	}
)

print("Succeeded:", result.get("ok"))

if result.get("ok"):
	print(result.get("data"))
else:
	print(result.get("error"))
```

Replace `SomeFetcherClass`, `some_fetch_method`, and the argument names with the actual class,
method, and signature from the API reference.



## ðŸ•¸ï¸ Tooling Pattern for Scrapers

Scraper methods can also be exposed as tools.

```python id="scraper_tool_pattern"
from models import ToolDef
from scrapers import WebExtractor

extractor = WebExtractor()

extract_text_tool = ToolDef.from_method(
	target=extractor,
	method="extract_text",
	name="extract_web_text",
	description="Extract readable text from a web page or HTML source.",
	category="web"
)

print(extract_text_tool.to_openai())
```

Call the tool with arguments matching the method signature:

```python id="scraper_tool_call_pattern"
result = extract_text_tool.call(
	{
		"url": "https://example.com"
	}
)

print("Succeeded:", result.get("ok"))
print("Data:", result.get("data"))
print("Error:", result.get("error"))
```

If your scraper method expects HTML instead of a URL, pass the correct argument name from the API
reference.



## ðŸ§¾ Validate Tool Schemas

Before sending tool schemas to an AI provider, inspect them locally.

```python id="validate_tool_schemas"
for tool in tools:
	print("Tool:", tool.name)
	print("Neutral:", tool.to_dict())
	print("OpenAI:", tool.to_openai())
	print("Gemini:", tool.to_gemini())
	print("Grok:", tool.to_grok())
	print()
```

Confirm:

```text id="schema_validation_points"
- Tool names are clear and unique.
- Descriptions explain what the tool does.
- Required arguments are correct.
- Optional arguments include defaults when available.
- Parameter types match the callable signature.
```



## ðŸ§ª Validate Tool Execution

Always test tools directly before connecting them to an AI model.

```python id="validate_tool_execution"
for tool in tools:
	print("Testing:", tool.name)
	print("Parameters:", tool.parameters)
```

Then call each tool with known-good arguments:

```python id="known_good_call_example"
result = tool.call(
	{
		"text": "Known good test input."
	}
)

print(result)
```

A successful result uses:

```text id="successful_tool_result"
ok = true
data = serialized result payload
error = null
```

A failed result uses:

```text id="failed_tool_result"
ok = false
data = null
error = error details
```



## ðŸ§¯ Handling Tool Failures

`ToolDef.call()` returns a structured failure envelope instead of crashing the agent loop.

Example:

```python id="tool_failure_example"
from models import ToolDef


def divide_numbers(numerator: float, denominator: float) -> float:
	"""Divide two numbers.

	Purpose:
		Demonstrates how tool execution failures are returned as structured envelopes.

	Args:
		numerator (float): Numerator value.
		denominator (float): Denominator value.

	Returns:
		float: Division result.
	"""
	return numerator / denominator


divide_tool = ToolDef.from_callable(
	function=divide_numbers,
	name="divide_numbers",
	description="Divide one number by another.",
	category="math"
)

result = divide_tool.call(
	{
		"numerator": 10,
		"denominator": 0
	}
)

print("Succeeded:", result.get("ok"))
print("Data:", result.get("data"))
print("Error:", result.get("error"))
```

Expected behavior:

```text id="tool_failure_expected"
ok is false
data is null
error contains the wrapped exception type and message
```



## ðŸ“¦ Serialization Behavior

Fonky serializes common result types before returning tool output.

| Result type                   | Serialized as                                 |
| ----------------------------- | --------------------------------------------- |
| `None`                        | `None`                                        |
| `str`, `int`, `float`, `bool` | Original primitive value                      |
| `dict`                        | JSON-safe dictionary                          |
| `list`, `tuple`, `set`        | JSON-safe list                                |
| LangChain-style `Document`    | Dictionary with `page_content` and `metadata` |
| Pydantic model                | Model dictionary                              |
| Object with `to_dict()`       | Dictionary returned by `to_dict()`            |
| Other object                  | String representation                         |

This allows AI tools to return data that can be sent back to a model or written to JSON.



## ðŸ” Tool Safety Practices

Use the following practices when exposing Fonky methods to AI models:

| Practice                     | Reason                                                            |
| ---------------------------- | ----------------------------------------------------------------- |
| Use clear tool names         | Models select tools by name and description.                      |
| Use narrow descriptions      | Avoid making a tool sound broader than it is.                     |
| Validate arguments           | Provider schemas help, but Python methods should still validate.  |
| Avoid dangerous side effects | Do not expose destructive actions unless explicitly controlled.   |
| Prefer read-only tools       | Loaders, fetchers, scrapers, and processors are safer defaults.   |
| Log handled exceptions       | Keep the explicit `Error` and `Logger` pattern in source methods. |
| Test directly first          | Confirm the tool works before giving it to a model.               |



## ðŸ§ª End-to-End AI Tooling Example

This example creates a mini toolkit that an AI model could use to load text and count words.

```python id="end_to_end_ai_tooling_example"
from loaders import TextLoader
from models import ToolDef


def count_words(text: str) -> int:
	"""Count words in text.

	Purpose:
		Counts whitespace-separated words in a text value.

	Args:
		text (str): Text to count.

	Returns:
		int: Word count.
	"""
	return len(text.split())


def document_text(documents: list[dict]) -> str:
	"""Extract text from serialized documents.

	Purpose:
		Returns the first available page_content value from serialized document output.

	Args:
		documents (list[dict]): Serialized document dictionaries.

	Returns:
		str: First document text or an empty string.
	"""
	for document in documents:
		page_content = document.get("page_content")
		if page_content:
			return page_content

	return ""


loader = TextLoader()

tools = [
	ToolDef.from_method(
		target=loader,
		method="load",
		name="load_text_file",
		description="Load a local UTF-8 text file into serialized document objects.",
		category="documents"
	),
	ToolDef.from_callable(
		function=document_text,
		name="document_text",
		description="Extract the first text value from serialized document objects.",
		category="documents"
	),
	ToolDef.from_callable(
		function=count_words,
		name="count_words",
		description="Count words in a text value.",
		category="text"
	)
]

registry = {
	tool.name: tool
	for tool in tools
}

provider_schemas = [
	tool.to_openai()
	for tool in tools
]

print("Schemas available to the model:")

for schema in provider_schemas:
	function_block = schema.get("function")
	print("-", function_block.get("name"))

load_result = registry.get("load_text_file").call(
	{
		"path": "data/sample.txt",
		"encoding": "utf-8"
	}
)

if not load_result.get("ok"):
	print(load_result.get("error"))
	raise SystemExit(1)

text_result = registry.get("document_text").call(
	{
		"documents": load_result.get("data")
	}
)

if not text_result.get("ok"):
	print(text_result.get("error"))
	raise SystemExit(1)

count_result = registry.get("count_words").call(
	{
		"text": text_result.get("data")
	}
)

print(count_result)
```



## âœ… Usage Checklist

Before connecting Fonky tools to an AI provider, confirm:

| Check                            | Command or action                                                |
| -------------------------------- | ---------------------------------------------------------------- |
| Source compiles                  | `python -m compileall .`                                         |
| Tool class imports               | `python -c "from models import ToolDef; print('ok')"`            |
| Target class imports             | `python -c "from loaders import TextLoader; print('ok')"`        |
| Tool schema prints               | Call `tool.to_openai()`, `tool.to_gemini()`, or `tool.to_grok()` |
| Tool executes directly           | Call `tool.call({...})` with known-good arguments                |
| Failure envelope works           | Call with bad arguments and confirm `ok` is `False`              |
| Tool names are unique            | Print all names from the registry                                |
| Provider integration is isolated | Keep provider SDK calls separate from Fonky tool execution       |



## âž¡ï¸ Next Step

Continue to [User Guide](user-guide.md) for longer workflow examples across loaders, fetchers,
processors, scrapers, and tool orchestration.

