# Demographic & Public Data

![Demographic & Public Data](../images/fonky-gov-demo-health.png)

## Scope

Demographic workflows focus on census, international, civic, and public-data sources intended for statistics, public analysis, and comparative reporting.

## Key Operations

| Operation                | Primary Use                                           |
|--------------------------|-------------------------------------------------------|
| `fetch_census_data`      | retrieve census datasets or endpoint-backed results   |
| `fetch_socrata`          | retrieve public datasets exposed through Socrata      |
| `fetch_united_nations`   | retrieve UN and international public data             |
| `fetch_world_population` | retrieve world population or related demographic data |
| `load_open_city`         | ingest city/public-data source material               |

## Workflow Patterns

- retrieve public measures or dimensional datasets
- standardize records
- join with geographic or health context
- render tabular analysis or document summaries

## Notes

Prefer demographic tools when the primary output is a public statistic, civic dataset, or international demographic indicator.
