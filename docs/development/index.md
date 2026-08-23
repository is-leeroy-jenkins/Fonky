# Development Guide

## Extension workflow

1. Implement provider/file behavior in the appropriate implementation module.
2. Keep validation, request construction, parsing, and shaping in that implementation.
3. Add a thin wrapper in `fonky.py` when the operation belongs in the flat API.
4. Export the wrapper in `__all__`.
5. Test wrapper routing independently from provider integration.
6. Update domain and API documentation.
