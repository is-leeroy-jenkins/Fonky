# Astronomy & Space

Use this domain for celestial navigation, observatory/satellite data, near-Earth objects, NASA Open
Science, space weather, catalogs, object lookup, sky maps/charts, and OpenSky aviation data.

## Choose a Capability

| Task | Function | Typical Inputs |
|---|---|---|
| Celestial navigation/time-position data | `fetch_naval_observatory()` | mode, date/time, latitude/longitude |
| Observatory/ground-station/satellite data | `fetch_satellite_center()` | mode, query, time window, coordinate systems |
| NEO/fireball/NHATS data | `fetch_nearby_objects()` | mode, date range, body, distance, limits |
| NASA Open Science datasets | `fetch_open_science()` | dataset/metadata/assay/data mode, query/accession |
| Space-weather events | `fetch_space_weather()` | CME/flare/notification mode, dates, filters |
| Catalog/object/cone search | `fetch_astro_catalog()` | object query or sky coordinates |
| SIMBAD/astroquery operations | `fetch_astro_query()` | object/region search and row limits |
| Link/snapshot sky map | `fetch_star_map()` | object or coordinates, zoom, imagery controls |
| Rendered chart | `fetch_star_chart()` | object/coordinates plus chart dimensions/magnitude |
| Aircraft/airport/state data | `fetch_open_sky()` | mode, ICAO/airport/time/bounding box |

## Workflow — Near-Earth Objects During a Date Window

```python
from fonky import fonky

objects = fonky.fetch_nearby_objects(
    mode='close_approaches',
    start_date='2026-08-23',
    end_date='2026-08-30',
    dist_max='10LD',
    body='Earth',
    sort='date',
    limit=50
)
```

`dist_max='10LD'` expresses a close-approach distance filter in lunar-distance terms as accepted by
the underlying provider implementation.

## Workflow — Space Weather

```python
from fonky import fonky

cmes = fonky.fetch_space_weather(
    mode='cme',
    start_date='2026-08-01',
    end_date='2026-08-23',
    most_accurate_only=True,
    complete_entry_only=True
)
```

## Workflow — Star Chart for a Known Object

```python
from fonky import fonky

chart = fonky.fetch_star_chart(
    mode='object_chart',
    query='M31',
    zoom=5,
    image_source='DSS2',
    show_grid=True,
    show_lines=True,
    width=1200,
    height=700,
    magnitude=8.0
)
```

## Operational Notes

- Astronomy functionality has a heavier scientific dependency footprint than many other domains.
- Coordinate systems, date formats, units, and provider modes are not interchangeable across APIs.
- OpenSky authenticated calls may require client credentials; anonymous access can be more limited.
- Chart/map operations can return links, images, or provider-specific payloads rather than uniform records.
