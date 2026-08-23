# Archives & Research

Use this domain to **discover, retrieve, compare, and archive information from research, reference,
news, government, legislative, and historical sources**.

## Capability Selection

| Need | Use | Why |
|---|---|---|
| Scholarly paper discovery | `fetch_arxiv()` | Topic-oriented ArXiv retrieval with document/metadata controls. |
| Simple ArXiv document loading | `load_arxiv()` | Produces loader-style documents for downstream NLP/retrieval. |
| General reference lookup | `fetch_wikipedia()` / `load_wikipedia()` | Search/reference content with optional metadata. |
| Web discovery | `fetch_google_search()` | Fine-grained search constraints, site filtering, file types, image search, locale, safety. |
| News monitoring/research | `fetch_news()` | Endpoint, category, source, date, sort, and pagination controls. |
| Government data discovery | `fetch_gov_data()` | Search, package summary, and collection-oriented government data access. |
| Legislative research | `fetch_congress()` | Congresses, bills, laws, reports, date windows, and pagination. |
| Historical/archive research | `fetch_internet_archive()` | Search Internet Archive collections with fields, sorting, media type, and collection controls. |
| Grokipedia lookup | `fetch_grokipedia()` | Search/page retrieval with content and pagination controls. |
| Google Drive knowledge retrieval | `fetch_google_drive()` | Query Drive content by folder/template/MIME mode. |

## Workflow — Research a Topic Across Scholarly and General Sources

```python
from fonky import fonky

papers = fonky.fetch_arxiv(
    question='agentic retrieval augmented generation',
    max_documents=5,
    full_documents=False,
    include_metadata=True
)

reference = fonky.fetch_wikipedia(
    question='retrieval augmented generation',
    language='en',
    max_documents=3,
    include_metadata=True
)

web = fonky.fetch_google_search(
    keywords='agentic RAG evaluation',
    results=10,
    site_search='arxiv.org'
)
```

Use the three result sets for different purposes: papers for scholarly evidence, Wikipedia for quick
concept framing, and Google Search for discovery of additional sources. Do not merge the results
blindly; their metadata and trust characteristics differ.

## Workflow — Legislative Research

```python
from fonky import fonky

bills = fonky.fetch_congress(
    mode='bills',
    congress=119,
    limit=20,
    sort='updateDate+desc'
)
```

Use `mode` to select the Congress.gov resource family. Supply bill/law/report identifiers only for the
corresponding detail modes.

## Workflow — News by Topic and Time Window

```python
from fonky import fonky

articles = fonky.fetch_news(
    endpoint='all',
    query='wildfire smoke',
    language='en',
    published_after='2026-08-01',
    sort='published_at',
    limit=20,
    page=1
)
```

### Operational Notes

- These operations are network-bound.
- Search/news providers may enforce pagination and per-request result limits.
- Google Custom Search requires both an API key and CSE ID when not supplied explicitly.
- Congress and news APIs require provider credentials in normal authenticated use.
- Loader-style functions are preferable when the next step expects LangChain `Document` objects.

## API

See [Functional API](../api/fonky.md#archives) for exact signatures.
