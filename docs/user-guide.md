# User Guide

Fonky can be used as a flat functional library or as an object-oriented integration library.

## Prefer `fonky.py` When

- the operation is already represented by one of the 110 wrappers;
- you want a concise notebook/application call;
- you do not need persistent implementation-instance state;
- you want an ordinary typed callable suitable for later Tool adaptation.

## Prefer Classes Directly When

- you need implementation-specific methods not surfaced independently;
- you need persistent instance state;
- you are developing or debugging a provider integration.

## Wrapper Lifecycle

![Execution Workflow](images/fonky-workflow.png)

A wrapper owns its implementation instance for the duration of the call. This keeps cross-call state from being shared implicitly.

## Configuration

Configure only the providers you use. `config.py` reads credentials independently, so local loading does not require unrelated cloud, astronomy, or search credentials.

## Local, Cloud, and Remote Boundaries

### Local loaders
Require valid paths and format-specific dependencies.

### Cloud loaders
Additionally require cloud SDKs, authentication, and remote object identifiers.

### Remote fetchers
Additionally require network access and, for some providers, API credentials and rate-limit compliance.

## Return Values

The functional layer does not force heterogeneous providers into one response envelope. Check the wrapper annotation and target method before assuming a shape.

## Validation

Provider-specific validation remains in the implementation classes. The wrapper should not duplicate a second version of those rules.

## Errors

Errors originate from the implementation boundary. Several modules use `boogr.Error` and `boogr.Logger`; the wrapper layer does not replace that behavior.

## Extending the Functional API

1. Implement behavior in the appropriate implementation module.
2. Keep provider-specific validation, request, parsing, and response logic there.
3. Add a thin wrapper only if the operation belongs in the flat API.
4. Add the wrapper to `__all__`.
5. Add execution-path tests.
6. Update the source-derived documentation inventory.

## Reference

- [Functional API](api/fonky.md)
- [Fetchers](api/fetchers.md)
- [Loaders](api/loaders.md)
- [Scrapers](api/scrapers.md)
- [Architecture](architecture.md)
- [Configuration](configuration.md)
