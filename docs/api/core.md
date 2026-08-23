# API — `core.py`

## Classes

| Class | Public Methods | Purpose |
|---|---:|---|
| `Result` | 2 | Represent the result of an HTTP response. Stores the key fields from a ``requests.Response`` object in a small, stable container used by Fonky fetchers and scrapers. The class preserves the original response while exposing commonly inspected values such as URL, status code, text, encoding, and headers for serialization and downstream processing. |

## `Result`

Represent the result of an HTTP response. Stores the key fields from a ``requests.Response`` object in a small, stable container used by Fonky fetchers and scrapers. The class preserves the original response while exposing commonly inspected values such as URL, status code, text, encoding, and headers for serialization and downstream processing.

| Method | Signature | Purpose |
|---|---|---|
| `to_dict()` | `to_dict(  ) -> Dict[str, Any]` | Convert the result to a dictionary. Produces a plain dictionary representation of the response result for JSON-style serialization, testing, logging, or adapter output. Header values are copied into a new dictionary so downstream callers do not mutate the original response headers. Dictionary containing the URL, status code, text, encoding, and copied headers. |
| `has_html()` | `has_html(  ) -> bool` | Indicate whether response text is available. Reports whether the stored response text is represented as a string. This property provides a small compatibility flag for callers that need to decide whether text extraction or HTML-oriented processing can proceed. ``True`` when ``text`` is a string; otherwise ``False``. |

## Module Functions

| Function | Signature | Purpose |
|---|---|---|
| `throw_if()` | `throw_if( name: str, value: object ) -> None` | Validate a required value. Provides a lightweight guard for required arguments used by core and service-layer components. The function raises a clear ``ValueError`` when a required value is ``None`` so callers fail early before attempting provider calls, response handling, or serialization work. ValueError: Raised when ``value`` is ``None``. |
