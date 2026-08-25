# Dependencies

### Validated Baseline

```text
langchain==1.3.16
langchain-core==1.6.0
langchain-community==0.4.2
langchain-text-splitters==1.1.2
langchain-google-community==5.0.0
langchain-googledrive==0.1.52
setuptools==81.0.0
```

### Dependency Groups

| Group            | Examples                                                       |
|------------------|----------------------------------------------------------------|
| LangChain core   | `langchain`, `langchain-core`, `langchain-community`           |
| provider clients | Google, AWS, weather, mapping, health, archive libraries       |
| document parsers | PDF, Office, HTML, XML, notebook, OCR-related packages         |
| scraper support  | HTML parsing, readability, crawling, browser or render support |
| documentation    | `mkdocs`, `mkdocstrings`, theme and plugin packages            |

### Verification

```powershell
python -m pip check
pytest
mkdocs build --strict
```

### Failure Classes

- missing provider library,
- conflicting LangChain versions,
- incompatible `setuptools`,
- parser/driver dependency gap,
- documentation import failure.
