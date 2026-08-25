'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                tools.py
      Author:                  Terry D. Eppler
      Created:                 08-24-2026

      Last Modified By:        Terry D. Eppler
      Last Modified On:        08-24-2026
  ******************************************************************************************
  <summary>
    Groups the LangChain tools defined directly in fonky.py.

    Purpose:
        Provides domain-scoped discovery helpers for the 110 public Fonky operations. This module
        does not decorate, wrap, or reimplement any provider operation. The literal ``@tool``
        decorators are defined on the public operations in ``fonky.py``.
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

from typing import Dict, List

from langchain_core.tools import BaseTool

from .fonky import fetch_arxiv
from .fonky import fetch_google_drive
from .fonky import fetch_wikipedia
from .fonky import fetch_news
from .fonky import fetch_google_search
from .fonky import fetch_gov_data
from .fonky import fetch_congress
from .fonky import fetch_internet_archive
from .fonky import fetch_grokipedia
from .fonky import load_arxiv
from .fonky import load_wikipedia
from .fonky import fetch_naval_observatory
from .fonky import fetch_satellite_center
from .fonky import fetch_nearby_objects
from .fonky import fetch_open_science
from .fonky import fetch_space_weather
from .fonky import fetch_astro_catalog
from .fonky import fetch_astro_query
from .fonky import fetch_star_map
from .fonky import fetch_star_chart
from .fonky import fetch_open_sky
from .fonky import load_google_drive_file
from .fonky import load_google_drive_folder
from .fonky import load_onedrive
from .fonky import load_google_cloud_file
from .fonky import load_aws_file
from .fonky import load_google_speech_to_text
from .fonky import load_google_bucket
from .fonky import load_aws_bucket
from .fonky import fetch_census_data
from .fonky import fetch_socrata
from .fonky import fetch_united_nations
from .fonky import fetch_world_population
from .fonky import load_open_city
from .fonky import load_text
from .fonky import load_csv
from .fonky import read_pdf
from .fonky import load_pdf
from .fonky import load_excel
from .fonky import load_word
from .fonky import load_markdown
from .fonky import load_html
from .fonky import load_outlook
from .fonky import load_spfx
from .fonky import load_spfx_folder
from .fonky import load_powerpoint
from .fonky import load_powerpoint_multiple
from .fonky import load_email
from .fonky import load_json
from .fonky import load_xml
from .fonky import load_xml_tree
from .fonky import load_jupyter_notebook
from .fonky import fetch_google_weather_current
from .fonky import fetch_google_weather_hourly_forecast
from .fonky import fetch_google_weather_daily_forecast
from .fonky import fetch_google_weather_hourly_history
from .fonky import fetch_google_weather_alerts
from .fonky import fetch_earth_observatory
from .fonky import fetch_open_weather
from .fonky import fetch_historical_weather
from .fonky import fetch_usgs_earthquakes
from .fonky import fetch_usgs_water_data
from .fonky import fetch_air_now
from .fonky import fetch_climate_data
from .fonky import fetch_eonet
from .fonky import fetch_envirofacts
from .fonky import fetch_tides_and_currents
from .fonky import fetch_uv_index
from .fonky import fetch_purple_air
from .fonky import fetch_open_aq
from .fonky import fetch_firms
from .fonky import geocode_location
from .fonky import geocode_coordinates
from .fonky import validate_address
from .fonky import request_directions
from .fonky import fetch_global_imagery_wms_map
from .fonky import fetch_global_imagery_map_services
from .fonky import fetch_global_imagery_mercator_map
from .fonky import fetch_google_geocoding
from .fonky import fetch_usgs_national_map
from .fonky import fetch_usgs_sciencebase
from .fonky import fetch_health_data
from .fonky import fetch_global_health_data
from .fonky import fetch_wonder
from .fonky import load_pubmed
from .fonky import fetch_web_page
from .fonky import convert_html_to_text
from .fonky import extract_web_title
from .fonky import extract_web_links
from .fonky import extract_web_structured_data
from .fonky import crawl_web
from .fonky import scrape_crawler_page
from .fonky import render_web_page
from .fonky import load_web
from .fonky import load_web_recursive
from .fonky import load_web_pages
from .fonky import load_github
from .fonky import scrape_web_page
from .fonky import scraper_html_to_text
from .fonky import scrape_paragraphs
from .fonky import scrape_lists
from .fonky import scrape_tables
from .fonky import scrape_articles
from .fonky import scrape_headings
from .fonky import scrape_divisions
from .fonky import scrape_sections
from .fonky import scrape_blockquotes
from .fonky import scrape_hyperlinks
from .fonky import scrape_images
from .fonky import encode_image

# ==========================================================================================
# DOMAIN GROUPS
# ==========================================================================================

TOOLS_BY_DOMAIN: Dict[ str, List[ BaseTool ] ] = {
		'archives': [ fetch_arxiv, fetch_google_drive, fetch_wikipedia, fetch_news,
				fetch_google_search, fetch_gov_data, fetch_congress, fetch_internet_archive,
				fetch_grokipedia, load_arxiv, load_wikipedia, ],
		'astronomical': [ fetch_naval_observatory, fetch_satellite_center, fetch_nearby_objects,
				fetch_open_science, fetch_space_weather, fetch_astro_catalog, fetch_astro_query,
				fetch_star_map, fetch_star_chart, fetch_open_sky, ],
		'cloud': [ load_google_drive_file, load_google_drive_folder, load_onedrive,
				load_google_cloud_file, load_aws_file, load_google_speech_to_text,
				load_google_bucket, load_aws_bucket, ],
		'demographic': [ fetch_census_data, fetch_socrata, fetch_united_nations,
				fetch_world_population, load_open_city, ],
		'documents': [ load_text, load_csv, read_pdf, load_pdf, load_excel, load_word,
				load_markdown, load_html, load_outlook, load_spfx, load_spfx_folder,
				load_powerpoint, load_powerpoint_multiple, load_email, load_json, load_xml,
				load_xml_tree, load_jupyter_notebook, ],
		'environmental': [ fetch_google_weather_current, fetch_google_weather_hourly_forecast,
				fetch_google_weather_daily_forecast, fetch_google_weather_hourly_history,
				fetch_google_weather_alerts, fetch_earth_observatory, fetch_open_weather,
				fetch_historical_weather, fetch_usgs_earthquakes, fetch_usgs_water_data,
				fetch_air_now, fetch_climate_data, fetch_eonet, fetch_envirofacts,
				fetch_tides_and_currents, fetch_uv_index, fetch_purple_air, fetch_open_aq,
				fetch_firms, ],
		'geospatial': [ geocode_location, geocode_coordinates, validate_address,
		                request_directions, fetch_global_imagery_wms_map,
		                fetch_global_imagery_map_services, fetch_global_imagery_mercator_map,
		                fetch_google_geocoding, fetch_usgs_national_map, fetch_usgs_sciencebase, ],
		'health': [ fetch_health_data, fetch_global_health_data, fetch_wonder, load_pubmed, ],
		'web': [ fetch_web_page, convert_html_to_text, extract_web_title, extract_web_links,
				extract_web_structured_data, crawl_web, scrape_crawler_page, render_web_page,
				load_web, load_web_recursive, load_web_pages, load_github, scrape_web_page,
				scraper_html_to_text, scrape_paragraphs, scrape_lists, scrape_tables,
				scrape_articles, scrape_headings, scrape_divisions, scrape_sections,
				scrape_blockquotes, scrape_hyperlinks, scrape_images, encode_image, ], }

def throw_if( name: str, value: object ) -> None:
	"""Validate a required processor argument.

	Purpose:
	    Validates that a required argument is present and non-empty before text processing begins. The
	    guard rejects ``None``, blank strings, and empty container values with an argument-specific
	    ``ValueError``.

	Args:
	    name: Argument name included in the validation error message.
	    value: Candidate value checked for ``None``, blank text, or an empty container.

	Returns:
	    None: Validation succeeds silently; invalid values raise ``ValueError``.

	Raises:
	    ValueError: If a required value is missing, blank, or outside the supported range.
	"""
	if value is None:
		raise ValueError( f'Argument "{name}" cannot be empty!' )
	if isinstance( value, str ) and (not value.strip( )):
		raise ValueError( f'Argument "{name}" cannot be empty!' )
	if isinstance( value, (list, tuple, dict, set) ) and len( value ) == 0:
		raise ValueError( f'Argument "{name}" cannot be empty!' )

def get_domains( ) -> List[ str ]:
    """Return the supported Fonky tool domains.

    Returns:
        List[str]: Sorted domain names available through ``TOOLS_BY_DOMAIN``.
    """
    return sorted( TOOLS_BY_DOMAIN.keys( ) )

def get_tools( domain: str ) -> List[ BaseTool ]:
    """Return LangChain tools assigned to a Fonky domain.

    Args:
        domain: Exact Fonky domain name.

    Returns:
        List[BaseTool]: LangChain tools assigned to the requested domain.

    Raises:
        KeyError: If ``domain`` is not a defined Fonky tool domain.
    """
    if domain not in TOOLS_BY_DOMAIN:
        raise KeyError( f'Unknown Fonky tool domain: {domain}' )

    return list( TOOLS_BY_DOMAIN[ domain ] )

def get_tool_names( domain: str ) -> List[ str ]:
    """Return tool names assigned to a Fonky domain.

    Args:
        domain: Exact Fonky domain name.

    Returns:
        List[str]: LangChain tool names assigned to the requested domain.

    Raises:
        KeyError: If ``domain`` is not a defined Fonky tool domain.
    """
    tools = get_tools( domain=domain )
    return [ tool.name for tool in tools ]

# ==========================================================================================
# PUBLIC EXPORTS
# ==========================================================================================

__all__: List[ str ] = [ 'TOOLS_BY_DOMAIN', 'get_domains', 'get_tools', 'get_tool_names' ]
