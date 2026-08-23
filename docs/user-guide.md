# User Guide

This guide is organized around **what you are trying to accomplish**, not around the names of source
files or wrapper signatures.

## Choose a Workflow

| Area | Use When |
|---|---|
| [Archives](guides/archives.md) | You need research papers, search results, government/legislative data, news, or archival material. |
| [Astronomical](guides/astronomical.md) | You need astronomy catalogs, satellites, near-Earth objects, space weather, star charts, or aviation state data. |
| [Cloud](guides/cloud.md) | You need to ingest documents/audio from Google Drive, GCS, AWS S3, OneDrive, or Google Speech-to-Text. |
| [Demographic](guides/demographic.md) | You need Census, Socrata, UN, world-population, or municipal open-data retrieval. |
| [Documents](guides/documents.md) | You need to load local or enterprise documents into structured document objects. |
| [Environmental](guides/environmental.md) | You need weather, climate, air quality, fires, earthquakes, water, tides, UV, or environmental facility data. |
| [Geospatial](guides/geospatial.md) | You need geocoding, directions, imagery, National Map, or ScienceBase workflows. |
| [Health](guides/health.md) | You need HealthData, WHO/global-health, CDC WONDER, or PubMed retrieval. |
| [Web](guides/web.md) | You need HTTP retrieval, crawling, web-document loading, or structural HTML extraction. |

## Common Operating Sequence

1. Choose the domain and provider/format that matches the task.
2. Configure only the dependency and credential requirements for that path.
3. Use the functional wrapper when the task is one-shot.
4. Use the implementation class when the workflow needs retained state or helper methods.
5. Inspect the returned shape before downstream transformation.
6. Handle provider, file, parsing, and dependency failures explicitly.

## Cross-Cutting Guides

- [Choosing Functional vs Class Usage](guides/interface-selection.md)
- [Combining Capabilities](guides/composing-workflows.md)
- [Results and Return Shapes](guides/results.md)
- [Credentials and Dependencies](guides/dependencies.md)
- [Troubleshooting](troubleshooting.md)
