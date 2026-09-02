# Development

## Source contract

Provider tool modules expose canonical Fonky implementations. New provider wrappers must not
duplicate retrieval, loading, scraping, or processing logic. Provider packages are peers: one
provider package must not depend on another provider package to expose canonical Fonky operations.

## Documentation contract

Public functions require:

- typed Python signatures;
- a summary line;
- `Purpose:`;
- Google-style `Args:` entries;
- `Returns:`;
- `Raises:` when applicable.

Example:

```python
def operation(
        value: str ) -> Any:
    """Run an operation.

    Purpose:
        Execute the operation through the canonical Fonky implementation.

    Args:
        value (str): Value used by the operation.

    Returns:
        Any: Result returned by the canonical implementation.
    """
```

## Provider validation

### OpenAI Agents SDK

Every GPT tool must construct successfully with `@function_tool`.

### Anthropic Claude

Every Claude tool must construct successfully with `@beta_tool`. The decorated callable must
delegate directly to the canonical Fonky implementation and must not import or unwrap tools from
another provider package.

Anthropic derives the tool input schema from the Python signature and documentation, so signature
semantics, concrete defaults, and required parameters must remain accurate. Automatic Tool Runner
usage additionally requires returned tool-result content to be a string or supported Anthropic
content block; structured Fonky results require explicit serialization by the calling application.

### Google ADK

Every Gemini tool must remain a plain callable that ADK can inspect and wrap.

### xAI

Every Grok executable wrapper must have one unique declaration object. Declaration variable names
use the `*_tool` naming contract.

### LangChain

Every LangChain tool must construct successfully with:

```python
@tool( parse_docstring=True )
```

The generated argument schema must match the Python signature and parsed documentation comments.

## Static validation

```powershell
python -m compileall .\fonky
```

Validate imports:

```powershell
python -c "import fonky.fetchers; import fonky.loaders; import fonky.scrapers; import fonky.processors; print('ok')"
```

Validate provider modules:

```powershell
python -c "import fonky.gpt.tools; import fonky.claude.tools; import fonky.gemini.tools; import fonky.grok.tools; import fonky.langchain.tools; print('ok')"
```

## Documentation validation

```powershell
mkdocs build --strict
```

A documentation change is incomplete when the MkDocs build fails, an API module cannot import, or
navigation points to a missing page.

## Extension checklist

1. Implement canonical functionality in the correct core module.
2. Add or update the shared models required by the operation.
3. Add provider wrappers only after the canonical implementation is complete.
4. Preserve the executable tool name across provider packages.
5. Keep provider adapters independent from one another and delegate directly to canonical modules.
6. Add xAI declaration naming only where a separate declaration object is required.
7. Update Google-style documentation comments.
8. Update the user guide when the operation introduces a new workflow.
9. Run provider validation.
10. Run `mkdocs build --strict`.
