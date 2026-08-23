# Failure Handling

Common failure boundaries:

1. invalid arguments;
2. missing files;
3. missing Python dependencies;
4. missing/invalid credentials;
5. DNS/network failure;
6. timeout;
7. HTTP failure;
8. provider rate limiting;
9. malformed response;
10. parser/extractor failure.

Do not treat an exception as equivalent to a valid empty result.
