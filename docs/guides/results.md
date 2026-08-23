# Results and Return Shapes

Fonky intentionally preserves implementation-specific return values instead of wrapping every result
in a generic envelope.

| Family | Common Producers | Typical Use |
|---|---|---|
| `List[Document]` | Document/cloud/web loaders | Retrieval, embeddings, NLP, document analysis |
| `dict` | API fetchers | Metadata + structured provider response |
| `list[dict]` | Public-data APIs | Row/record processing, DataFrame conversion |
| `str` | HTML/text conversion | NLP and direct display |
| `list[str]` | Focused scrapers | Headings, links, paragraphs, table cells, images |
| file/image/provider object | Imagery/specialized integrations | Save, display, or provider-specific downstream work |

## Normalize at the Application Boundary

If your application requires one common contract, normalize results after Fonky returns them. Keeping
normalization outside the wrapper avoids throwing away provider-specific information prematurely.
