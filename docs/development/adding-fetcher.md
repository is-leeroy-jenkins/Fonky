# Adding a Fetcher

A fetcher owns provider-specific behavior: endpoint construction, provider validation, authentication,
HTTP requests, pagination, parsing, and response shaping.

## Checklist

- Define a focused concrete class in `fetchers.py`.
- Validate provider modes and bounded numeric arguments before network calls.
- Keep credential lookup/configuration compatible with `config.py`.
- Use explicit timeouts.
- Normalize only what is necessary to make the provider usable without discarding valuable metadata.
- Wrap/log errors consistently with the existing module.
- Add a functional wrapper only after the implementation path works directly.
