# Testing & Documentation

## Required Checks

```powershell
python -m pip check
pytest
mkdocs build --strict
```

## Static Assertions

- all public exports in `fonky.py` have literal `@tool(...)` decorators,
- every public export has a parseable Google-style docstring,
- `tools.py` groups, but does not recreate, those tool objects,
- every navigation page exists,
- every API page imports the intended module.

## Runtime Assertions

- public exports are `BaseTool` instances,
- domain groups contain unique members,
- `.get_input_schema()` succeeds for public tools,
- implementation classes execute independently for diagnostic use.
