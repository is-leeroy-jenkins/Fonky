# API — `models.py`

| Class | Public methods | Purpose |
|---|---:|---|
| `Prompt` | 0 | Prompt model. Represents a structured prompt bundle used to pass instructions, versioning details, output format hints, and a user question through Fonky workflows. The model provides a typed container for prompt metadata that can be serialized by Pydantic. |
| `File` | 0 | File model. Represents file metadata returned by provider APIs or managed by Fonky workflows. The model stores identity, lifecycle, size, object type, purpose, and filename fields in a consistent Pydantic structure. |
| `Document` | 0 | Document model. Represents a compact document-style payload containing summary and description text. The model is useful for normalized outputs where only high-level document metadata is required. |
| `Message` | 0 | Message model. Represents a normalized chat or tool message payload. The model stores role, content, message type, and optional structured data for conversational and provider-facing workflows. |
| `Location` | 0 | Location model. Represents a high-level location descriptor for tools that need city, region, country, timezone, or location type information. The model keeps user-location context in a provider- neutral shape. |
| `GeoCoordinates` | 0 | GeoCoordinates model. Represents geographic coordinates and optional timezone metadata for geospatial tools. The model stores latitude, longitude, coordinate type, and timezone in a serializable Pydantic container. |
| `Forecast` | 0 | Forecast model. Represents a simplified weather forecast response. The model stores forecast type, temperature, precipitation, and sky-condition values for tool outputs or normalized provider responses. |
| `Directions` | 0 | Directions model. Represents a simplified route or directions payload. The model stores route data and type metadata for mapping, navigation, or location-aware tool responses. |
| `SkyCoordinates` | 0 | SkyCoordinates model. Represents astronomical coordinate values used by sky, catalog, and observatory workflows. The model stores declination and right ascension in a typed, serializable structure. |
| `Tool` | 0 | Tool model. Represents the shared base descriptor for callable tools. The model stores a tool name, provider-facing type, and short description used by function-calling workflows. |
| `Function` | 0 | Function model. Extends the base tool descriptor with callable parameter schema and strictness metadata. The model represents a function-style tool declaration independent of any single provider. |
| `FileSearch` | 0 | FileSearch model. Represents configuration for a file-search tool. The model stores vector store identifiers, result limits, and optional filters for retrieval workflows. |
| `WebSearch` | 0 | WebSearch model. Represents configuration for a web-search tool. The model stores search context size and optional user-location metadata used by search-capable provider workflows. |
| `ComputerUse` | 0 | ComputerUse model. Represents configuration for a computer-use or UI-automation tool. The model stores display dimensions and execution environment metadata for provider tool declarations. |
| `ToolDef` | 8 | ToolDef model. Represents a provider-neutral tool definition bound to a Python callable or object method. The model stores callable metadata, generated parameter schema, provider conversion helpers, and execution behavior for unified tool dispatch. |

## `Prompt`

Prompt model. Represents a structured prompt bundle used to pass instructions, versioning details, output format hints, and a user question through Fonky workflows. The model provides a typed container for prompt metadata that can be serialized by Pydantic.

## `File`

File model. Represents file metadata returned by provider APIs or managed by Fonky workflows. The model stores identity, lifecycle, size, object type, purpose, and filename fields in a consistent Pydantic structure.

## `Document`

Document model. Represents a compact document-style payload containing summary and description text. The model is useful for normalized outputs where only high-level document metadata is required.

## `Message`

Message model. Represents a normalized chat or tool message payload. The model stores role, content, message type, and optional structured data for conversational and provider-facing workflows.

## `Location`

Location model. Represents a high-level location descriptor for tools that need city, region, country, timezone, or location type information. The model keeps user-location context in a provider- neutral shape.

## `GeoCoordinates`

GeoCoordinates model. Represents geographic coordinates and optional timezone metadata for geospatial tools. The model stores latitude, longitude, coordinate type, and timezone in a serializable Pydantic container.

## `Forecast`

Forecast model. Represents a simplified weather forecast response. The model stores forecast type, temperature, precipitation, and sky-condition values for tool outputs or normalized provider responses.

## `Directions`

Directions model. Represents a simplified route or directions payload. The model stores route data and type metadata for mapping, navigation, or location-aware tool responses.

## `SkyCoordinates`

SkyCoordinates model. Represents astronomical coordinate values used by sky, catalog, and observatory workflows. The model stores declination and right ascension in a typed, serializable structure.

## `Tool`

Tool model. Represents the shared base descriptor for callable tools. The model stores a tool name, provider-facing type, and short description used by function-calling workflows.

## `Function`

Function model. Extends the base tool descriptor with callable parameter schema and strictness metadata. The model represents a function-style tool declaration independent of any single provider.

## `FileSearch`

FileSearch model. Represents configuration for a file-search tool. The model stores vector store identifiers, result limits, and optional filters for retrieval workflows.

## `WebSearch`

WebSearch model. Represents configuration for a web-search tool. The model stores search context size and optional user-location metadata used by search-capable provider workflows.

## `ComputerUse`

ComputerUse model. Represents configuration for a computer-use or UI-automation tool. The model stores display dimensions and execution environment metadata for provider tool declarations.

## `ToolDef`

ToolDef model. Represents a provider-neutral tool definition bound to a Python callable or object method. The model stores callable metadata, generated parameter schema, provider conversion helpers, and execution behavior for unified tool dispatch.

| Method | Signature | Purpose |
|---|---|---|
| `from_callable()` | `from_callable( cls: Any, function: Callable[..., Any], name: Optional[str] = None, description: Optional[str] = None, category: Optional[str] = None, strict: bool = True ) -> 'ToolDef'` | Create tool definition from callable. Creates a provider-neutral tool definition from a standalone Python callable. The method derives the callable name, source module, description, parameter schema, strictness flag, and execution handler needed for later tool dispatch. Tool definition that wraps the supplied callable for provider-neutral use. Error: Raised after the underlying exception is wrapped with module, cause, and method metadata. |
| `from_method()` | `from_method( cls: Any, target: Any, method: str, name: Optional[str] = None, description: Optional[str] = None, category: Optional[str] = None, strict: bool = True ) -> 'ToolDef'` | Create tool definition from object method. Creates a provider-neutral tool definition from a method on an existing object instance. The method validates that the target member exists and is callable, then stores the target, method name, source class, source module, and generated parameter schema. Tool definition that resolves and wraps a named method on the supplied object instance. Error: Raised after the underlying exception is wrapped with module, cause, and method metadata. |
| `resolve_callable()` | `resolve_callable(  ) -> Callable[..., Any]` | Resolve bound callable. Resolves the executable Python callable represented by the tool definition. The method returns a direct handler when one is stored or retrieves the named method from the stored target object after validating the binding. Python callable bound to this tool definition. Error: Raised after the underlying exception is wrapped with module, cause, and method metadata. |
| `call()` | `call( arguments: Optional[Dict[str, Any]] = None ) -> Dict[str, Any]` | Execute bound tool callable. Executes the bound tool callable with keyword arguments and returns a neutral response envelope. The method serializes successful results and converts failures into structured error metadata without exposing provider-specific response objects. Dictionary containing execution status, serialized data, error information, and tool metadata. |
| `to_dict()` | `to_dict(  ) -> Dict[str, Any]` | Export neutral tool dictionary. Exports the tool definition as a provider-neutral dictionary for inspection, persistence, or application-level routing. The method includes schema fields, source metadata, method binding details, and category information. Provider-neutral dictionary representation of this tool definition. Error: Raised after the underlying exception is wrapped with module, cause, and method metadata. |
| `to_openai()` | `to_openai(  ) -> Dict[str, Any]` | Export OpenAI tool schema. Builds an OpenAI-compatible function tool declaration from the neutral tool definition. The method supplies a function name, description, parameters object, and strictness flag using safe defaults when optional schema fields are absent. OpenAI-compatible function-tool schema for this tool definition. Error: Raised after the underlying exception is wrapped with module, cause, and method metadata. |
| `to_grok()` | `to_grok(  ) -> Dict[str, Any]` | Export Grok tool schema. Builds a Grok-compatible function tool declaration using the same schema shape used for OpenAI function tools. The method preserves the neutral tool definition while reusing the shared provider conversion path. Grok-compatible function-tool schema for this tool definition. Error: Raised after the underlying exception is wrapped with module, cause, and method metadata. |
| `to_gemini()` | `to_gemini(  ) -> Dict[str, Any]` | Export Gemini tool schema. Builds a Gemini-compatible function declaration from the neutral tool definition. The method returns the function name, description, and parameters object in the schema shape expected by Gemini tool configuration. Gemini-compatible function declaration for this tool definition. Error: Raised after the underlying exception is wrapped with module, cause, and method metadata. |
