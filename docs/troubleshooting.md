# Troubleshooting

## Symptom Index

| Symptom | Likely Cause | First Check |
|---|---|---|
| tool import fails | missing LangChain dependency | `pip check` |
| provider call fails | missing/invalid credentials | environment variables and provider-specific auth |
| loader raises parse/driver error | missing library or unsupported file | loader dependency and file format |
| scraper returns sparse content | boilerplate-heavy or script-rendered page | use render/load path instead of static scrape |
| MkDocs API page is empty or shallow | page built from hand-written table instead of `mkdocstrings` | use source-driven API directives |
| `.invoke()` confusion | public export treated as plain function | confirm `fonky.py` names are `BaseTool` objects |

## Build Checks

```powershell
python -m pip check
pytest
mkdocs build --strict
```

## Fast Isolation

1. validate environment,
2. import the tool,
3. invoke with the smallest viable parameter set,
4. test the underlying implementation class if needed,
5. confirm provider configuration,
6. confirm documentation imports the intended module.
