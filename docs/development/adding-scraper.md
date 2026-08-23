# Adding a Scraper

A focused scraper should perform one clearly defined extraction.

## Checklist

1. Validate the URI.
2. Request with an explicit timeout.
3. Raise on HTTP failure.
4. Parse with the existing HTML stack.
5. Extract one meaningful structure.
6. Return a predictable Python result.
7. Log/wrap exceptions consistently.
8. Add a working user-guide example when the new capability changes user workflows.
