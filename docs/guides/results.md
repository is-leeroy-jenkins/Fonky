# Results and Data Shapes

Fonky preserves the result contract of the underlying implementation.

| Result | Typical use |
|---|---|
| `List[Document]` | loaders, retrieval, embeddings, chunking |
| `dict` | normalized provider responses |
| `list[dict]` | tabular/public-data records |
| `str` | extracted text |
| `list[str]` | scraper structures such as headings, links, cells, and images |

Normalize only at the application boundary when downstream code requires a uniform contract.
