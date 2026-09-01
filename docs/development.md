# Development

## Source contract

Provider tool modules expose canonical Fonky implementations. New provider wrappers must not
duplicate retrieval, loading, scraping, or processing logic.

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
python -c "import fonky.gpt.tools; import fonky.gemini.tools; import fonky.grok.tools; import fonky.langchain.tools; print('ok')"
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
5. Add xAI declaration naming only where a separate declaration object is required.
6. Update Google-style documentation comments.
7. Update the user guide when the operation introduces a new workflow.
8. Run provider validation.
9. Run `mkdocs build --strict`.
