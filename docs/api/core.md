# API Reference: `core.py`

`core.py` defines the package core result structure and related utilities.

## Module Inventory

- **Classes:** 1
- **Top-level functions:** 1

## Module-Level Functions

| Function | Signature | Purpose |
|---|---|---|
| `throw_if()` | `throw_if( name: str, value: object ) -> None` | Validate a required value. |

## Classes

| Class | Constructor | Public Methods | Functional Wrappers |
|---|---|---:|---:|
| [`Result`](#result) | `Result( self: Any, response: Response ) -> None` | 2 | 0 |

## `Result`

Represent the result of an HTTP response.

```python
Result( self: Any, response: Response ) -> None
```

**Source:** `core.py`, line 73

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `to_dict()` | `to_dict( self: Any ) -> Dict[str, Any]` | Convert the result to a dictionary. |
| `has_html()` | `has_html( self: Any ) -> bool` | Indicate whether response text is available. |
