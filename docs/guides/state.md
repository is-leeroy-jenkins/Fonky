# State

### Public Surface State Model

The public tool layer is intentionally short-lived.

- each `fonky.py` export creates a fresh implementation instance,
- provider configuration is resolved per invocation,
- `tools.py` returns already-defined tool objects and adds no execution state,
- downstream persistence belongs outside the public surface.

### When to Use Implementation Classes

Use a source-module class when you need:

- repeated calls with shared configuration,
- lower-level testing,
- provider debugging,
- stateful orchestration not appropriate for the one-shot public surface.
