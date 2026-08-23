# Development

Fonky extensions should preserve the boundary between implementation behavior and the functional API.

## Normal Change Sequence

1. Implement or modify provider/file behavior in `fetchers.py`, `loaders.py`, or `scrapers.py`.
2. Add focused validation close to the provider operation.
3. Add a thin `fonky.py` wrapper only when a public one-shot operation is useful.
4. Add the wrapper to `__all__`.
5. Test the route independently from the live provider integration.
6. Add/update task-oriented guide content.
7. Update API reference and diagrams only when behavior/architecture changed.
8. Run package tests and `mkdocs build --strict`.

## Guides

- [Adding a Fetcher](adding-fetcher.md)
- [Adding a Loader](adding-loader.md)
- [Adding a Scraper](adding-scraper.md)
- [Adding a Wrapper](adding-wrapper.md)
- [Testing and Documentation](testing.md)
