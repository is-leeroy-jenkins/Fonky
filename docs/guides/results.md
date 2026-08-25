# Results & Return Shapes

### Result Families

| Family | Typical Producer | Shape |
|---|---|---|
| provider records | fetchers | dictionaries, lists, normalized provider payloads |
| LangChain documents | loaders | `List[Document]`-like structures with content and metadata |
| extracted structures | scrapers | lists or dictionaries of headings, links, tables, paragraphs, images |
| metadata bundles | loaders / fetchers | source, timestamps, identifiers, provider descriptors |

### Reading Results

- inspect the top-level type,
- confirm presence of metadata,
- preserve source identifiers for provenance,
- convert to downstream schemas only after execution succeeds,
- keep scrape and fetch outputs distinct from loader document outputs.
