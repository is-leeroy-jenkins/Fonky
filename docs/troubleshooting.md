# Troubleshooting

## `ModuleNotFoundError` During Import

**Meaning:** the Python environment cannot import one of Fonky's dependencies.

```powershell
python -m pip install -r requirements.txt
python -c "from fonky import fonky"
```

Resolve import errors before testing credentials or network behavior.

## Provider Returns 401/403

**Meaning:** authentication failed or the credential lacks access.

Check the provider-specific variable in [Configuration](configuration.md). Do not print secrets while
debugging.

## Provider Times Out

Check network access, provider availability, and the call's `time`/timeout setting. Repeated timeouts
should not be interpreted as empty data.

## Scraper Returns an Empty List

The target page may contain no matching paragraphs/tables/headings/etc. Verify the page structure.
If the page is JavaScript-rendered, use a Playwright-capable path instead of assuming the selector is
wrong.

## PDF Loads Poorly

Try the extraction mode appropriate to the source. Scanned/image PDFs may need OCR; digitally created
PDFs usually work better with plain text extraction.

## Cloud Loader Cannot Authenticate

Separate three questions:

1. Is the SDK installed?
2. Can the SDK find credentials?
3. Does that identity have permission to the requested bucket/drive/object?

## Public Dataset Query Fails

Check the target dataset's current schema. Fonky can construct/submit provider queries, but dataset
field names and availability are controlled by the provider.

## MkDocs Build Fails

```powershell
mkdocs build --strict
```

Fix the first reported missing page, extension, plugin, or import error before addressing downstream
warnings.
