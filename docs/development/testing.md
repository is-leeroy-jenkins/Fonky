# Testing and Documentation

## Wrapper Route Tests

Test wrapper routing without depending on live external services:

- target class exists;
- target method exists;
- wrapper arguments match target keywords;
- defaults are intentionally compatible;
- return value propagates;
- exception propagation is preserved.

## Integration Tests

Keep live-provider tests separate because they depend on credentials, rate limits, network availability,
and changing external datasets.

## Documentation Validation

```powershell
mkdocs build --strict
```

Then verify:

- all navigation targets exist;
- local links resolve;
- examples use real current function names;
- configuration tables identify actual consumers and purpose;
- user-guide examples perform work rather than repeat signatures;
- diagrams explain engineering relationships rather than repository layout.
