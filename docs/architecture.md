# Architecture

Fonky separates the public calling surface from provider-specific implementation behavior.

## Layers

| Layer | Responsibility |
|---|---|
| Consumer | Scripts, notebooks, applications, batch jobs, future Tools |
| `fonky.py` | 110 typed one-shot wrapper functions |
| `fetchers.py` | 49 remote/provider implementation classes |
| `loaders.py` | 29 document/cloud ingestion classes |
| `scrapers.py` | 2 focused HTML extraction classes |

## Wrapper lifecycle

A wrapper validates only its ordinary Python call contract, creates the appropriate implementation object, invokes the target method, and returns the underlying result. Provider validation remains in the implementation class.

## State

Functional calls create fresh instances. Multi-step workflows that depend on previously loaded documents or retained provider state should use a persistent implementation instance.

## Validation boundaries

Provider-specific limits belong in implementation classes. Google Search, for example, validates result and start bounds before issuing a request; mode-dispatching fetchers reject unsupported operations.

## Result contracts

Fonky intentionally preserves provider/loader result shapes instead of forcing a universal envelope. Typical outputs include dictionaries, row collections, text, extracted string collections, and LangChain `Document` objects.

## Error boundaries

Common failure classes are dependency errors, authentication/authorization failures, local filesystem errors, validation failures, timeouts, HTTP errors, malformed provider responses, and parse/extraction failures.
