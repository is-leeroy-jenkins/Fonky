# Geospatial & Mapping

Use the Geospatial domain to turn places into coordinates, coordinates into places, validate
addresses, obtain directions, retrieve imagery, and search USGS spatial catalogs.

## Workflow — Forward and Reverse Geocoding

```python
from fonky import fonky

location = fonky.geocode_location(
    address='1600 Pennsylvania Avenue NW, Washington, DC'
)

reverse = fonky.geocode_coordinates(
    lat=38.8977,
    long=-77.0365
)
```

## Workflow — Address Validation

```python
validated = fonky.validate_address(
    address=[
        '1600 Pennsylvania Avenue NW',
        'Washington, DC 20500'
    ]
)
```

## Workflow — Directions

```python
route = fonky.request_directions(
    origin='Arlington, VA',
    destination='Baltimore, MD',
    mode='driving'
)
```

## Workflow — USGS National Map

```python
products = fonky.fetch_usgs_national_map(
    mode='products',
    dataset='National Elevation Dataset (NED) 1/3 arc-second',
    q='Virginia',
    max_items=25,
    offset=0
)
```

## Imagery

`fetch_global_imagery_wms_map()` is the explicit map-image operation. It requires a WMS layer, image
date, geographic bounding box, output dimensions, projection, format, and output settings. Use the
service-discovery wrappers before hard-coding a layer you have not verified.

## Operational Notes

- Confirm latitude/longitude ordering for each provider.
- Geocoding results can be ambiguous; inspect normalized address and provider metadata.
- Directions modes are provider-defined.
- WMS imagery layers and available dates can change independently of Fonky.
- Large image dimensions increase network and memory cost.
