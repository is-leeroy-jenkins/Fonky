# Adding a Loader

A loader owns source validation and conversion into document/result objects.

## Checklist

- Resolve and verify paths/sources.
- Use the format/provider library best suited to the source.
- Preserve useful source metadata.
- Decide whether the operation is one-shot or stateful.
- Support chunking only where it is meaningful.
- Make parser/OCR dependencies explicit.
- Test representative, empty, malformed, and large inputs.
