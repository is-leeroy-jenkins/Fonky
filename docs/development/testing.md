# Testing and Validation

## Wrapper tests
Verify target class, target method, argument compatibility, return propagation, and failure propagation.

## Integration tests
Keep live-provider tests separate because they depend on credentials, network availability, rate limits, and external service behavior.

## Documentation
Run `python -m mkdocs build --strict` and validate links/navigation before release.
