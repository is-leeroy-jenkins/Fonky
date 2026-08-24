# Adding a Public Export

## Public Export Standard

A public export in `fonky.py` must:

- use literal `@tool(parse_docstring=True, error_on_invalid_docstring=True)`,
- have a typed signature,
- delegate to the owning implementation class,
- use a Google-style docstring with accurate `Args`, `Returns`, and `Raises`,
- avoid generic filler such as “Load source content” or “Result produced by the operation”.

## Minimal Pattern

```python
from langchain_core.tools import tool


@tool(
    parse_docstring=True,
    error_on_invalid_docstring=True
)
def operation( value: str ) -> dict:
    """Resolve the requested value.

    Args:
        value: Domain-specific input used by the operation.

    Returns:
        dict: Normalized operation result.
    """
    _instance = OwnerClass( )
    return _instance.operation( value=value )
```
