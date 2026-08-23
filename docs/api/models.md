# API Reference: `models.py`

`models.py` defines structured project models and existing Tool infrastructure, including `ToolDef`.

## Module Inventory

- **Classes:** 15
- **Top-level functions:** 5

## Module-Level Functions

| Function | Signature | Purpose |
|---|---|---|
| `throw_if()` | `throw_if( name: str, value: Any ) -> None` | Validate required argument. |
| `clean_docstring()` | `clean_docstring( value: Optional[str] ) -> str` | Clean callable documentation. |
| `python_type_to_json_schema()` | `python_type_to_json_schema( annotation: Any ) -> Dict[str, Any]` | Convert Python annotation to JSON Schema. |
| `build_parameter_schema()` | `build_parameter_schema( function: Callable[..., Any] ) -> Dict[str, Any]` | Build callable parameter schema. |
| `serialize_value()` | `serialize_value( value: Any ) -> Any` | Serialize runtime value. |

## Classes

| Class | Constructor | Public Methods | Functional Wrappers |
|---|---|---:|---:|
| [`Prompt`](#prompt) | `Prompt( )` | 0 | 0 |
| [`File`](#file) | `File( )` | 0 | 0 |
| [`Document`](#document) | `Document( )` | 0 | 0 |
| [`Message`](#message) | `Message( )` | 0 | 0 |
| [`Location`](#location) | `Location( )` | 0 | 0 |
| [`GeoCoordinates`](#geocoordinates) | `GeoCoordinates( )` | 0 | 0 |
| [`Forecast`](#forecast) | `Forecast( )` | 0 | 0 |
| [`Directions`](#directions) | `Directions( )` | 0 | 0 |
| [`SkyCoordinates`](#skycoordinates) | `SkyCoordinates( )` | 0 | 0 |
| [`Tool`](#tool) | `Tool( )` | 0 | 0 |
| [`Function`](#function) | `Function( )` | 0 | 0 |
| [`FileSearch`](#filesearch) | `FileSearch( )` | 0 | 0 |
| [`WebSearch`](#websearch) | `WebSearch( )` | 0 | 0 |
| [`ComputerUse`](#computeruse) | `ComputerUse( )` | 0 | 0 |
| [`ToolDef`](#tooldef) | `ToolDef( )` | 8 | 0 |

## `Prompt`

Prompt model.

```python
Prompt( )
```

**Source:** `models.py`, line 298

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `File`

File model.

```python
File( )
```

**Source:** `models.py`, line 318

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `Document`

Document model.

```python
Document( )
```

**Source:** `models.py`, line 342

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `Message`

Message model.

```python
Message( )
```

**Source:** `models.py`, line 355

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `Location`

Location model.

```python
Location( )
```

**Source:** `models.py`, line 372

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `GeoCoordinates`

GeoCoordinates model.

```python
GeoCoordinates( )
```

**Source:** `models.py`, line 392

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `Forecast`

Forecast model.

```python
Forecast( )
```

**Source:** `models.py`, line 410

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `Directions`

Directions model.

```python
Directions( )
```

**Source:** `models.py`, line 428

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `SkyCoordinates`

SkyCoordinates model.

```python
SkyCoordinates( )
```

**Source:** `models.py`, line 441

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `Tool`

Tool model.

```python
Tool( )
```

**Source:** `models.py`, line 456

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `Function`

Function model.

```python
Function( )
```

**Source:** `models.py`, line 471

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `FileSearch`

FileSearch model.

```python
FileSearch( )
```

**Source:** `models.py`, line 484

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `WebSearch`

WebSearch model.

```python
WebSearch( )
```

**Source:** `models.py`, line 499

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `ComputerUse`

ComputerUse model.

```python
ComputerUse( )
```

**Source:** `models.py`, line 514

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `ToolDef`

ToolDef model.

```python
ToolDef( )
```

**Source:** `models.py`, line 531

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `from_callable()` | `from_callable( cls: Any, function: Callable[..., Any], name: Optional[str] = None, description: Optional[str] = None, category: Optional[str] = None, strict: bool = True ) -> 'ToolDef'` | Create tool definition from callable. |
| `from_method()` | `from_method( cls: Any, target: Any, method: str, name: Optional[str] = None, description: Optional[str] = None, category: Optional[str] = None, strict: bool = True ) -> 'ToolDef'` | Create tool definition from object method. |
| `resolve_callable()` | `resolve_callable( self: Any ) -> Callable[..., Any]` | Resolve bound callable. |
| `call()` | `call( self: Any, arguments: Optional[Dict[str, Any]] = None ) -> Dict[str, Any]` | Execute bound tool callable. |
| `to_dict()` | `to_dict( self: Any ) -> Dict[str, Any]` | Export neutral tool dictionary. |
| `to_openai()` | `to_openai( self: Any ) -> Dict[str, Any]` | Export OpenAI tool schema. |
| `to_grok()` | `to_grok( self: Any ) -> Dict[str, Any]` | Export Grok tool schema. |
| `to_gemini()` | `to_gemini( self: Any ) -> Dict[str, Any]` | Export Gemini tool schema. |
