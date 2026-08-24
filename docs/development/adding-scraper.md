# Adding a Scraper

## Checklist

- implement extraction in `scrapers.py`,
- scope the scraper to a clear structural target,
- document the returned structure,
- verify behavior on representative HTML,
- expose a public tool only when the extraction is generally reusable.

## Scraper-Specific Concerns

- CSS/DOM target stability,
- missing-element handling,
- boilerplate removal,
- static versus rendered page assumptions.
