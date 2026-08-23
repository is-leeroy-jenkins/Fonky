# Credentials and Dependencies

Provider-backed workflows have two independent prerequisites: **Python dependencies** and
**authentication/configuration**.

## Missing Dependency

```text
ModuleNotFoundError: No module named 'astropy'
```

Resolve the active environment first. Credentials cannot fix an import failure.

## Missing Credential

Typical symptoms are provider 401/403 responses or provider-specific authentication exceptions.
Verify the environment variable, OAuth token, service-account file, or cloud credential chain.

## Browser Dependency

Playwright-backed retrieval requires both the Python package and an installed browser runtime.

## Scientific Dependencies

Astronomy and geospatial modules may import scientific libraries even when your current call uses
only one provider. Keep the project's dependency specification synchronized with the package imports.
