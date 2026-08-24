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
    Provides LangChain @tool integration for the Fonky functional API.

    Purpose:
        Exposes LangChain tool objects for the existing functions in ``fonky.py`` without
        introducing duplicate wrapper functions. Each public Fonky function is converted into
        a LangChain tool by applying the ``@tool`` decorator semantics directly to the
        remediated callable. This preserves the ordinary Python API in ``fonky.py`` while
        making agent-facing tool objects available from ``tools.py``.
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations
from typing import Dict, List, Tuple

from langchain_core.tools import BaseTool
from langchain_core.tools import tool

from . import fonky


def throw_if( name: str, value: object ) -> None:
    """Validate a required argument.

    Purpose:
        Rejects missing or empty values before they are used to select a LangChain tool
        domain or return a tool collection.

    Args:
        name: Argument name included in validation error messages.
        value: Runtime value to validate.

    Returns:
        None: The function only validates input.

    Raises:
        ValueError: If ``value`` is ``None``, blank, or an empty collection.
    """
    if value is None:
        raise ValueError( f'Argument "{name}" cannot be empty!' )

    if isinstance( value, str ) and not value.strip( ):
        raise ValueError( f'Argument "{name}" cannot be empty!' )

    if isinstance( value, (list, tuple, dict, set) ) and len( value ) == 0:
        raise ValueError( f'Argument "{name}" cannot be empty!' )


# ==========================================================================================
# TOOL BINDINGS
# ==========================================================================================

_fetch_arxiv = fonky.fetch_arxiv
fetch_arxiv = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_arxiv )

_fetch_google_drive = fonky.fetch_google_drive
fetch_google_drive = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_google_drive )

_fetch_wikipedia = fonky.fetch_wikipedia
fetch_wikipedia = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_wikipedia )

_fetch_news = fonky.fetch_news
fetch_news = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_news )

_fetch_google_search = fonky.fetch_google_search
fetch_google_search = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_google_search )

_fetch_gov_data = fonky.fetch_gov_data
fetch_gov_data = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_gov_data )

_fetch_congress = fonky.fetch_congress
fetch_congress = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_congress )

_fetch_internet_archive = fonky.fetch_internet_archive
fetch_internet_archive = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_internet_archive )

_fetch_grokipedia = fonky.fetch_grokipedia
fetch_grokipedia = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_grokipedia )

_load_arxiv = fonky.load_arxiv
load_arxiv = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_arxiv )

_load_wikipedia = fonky.load_wikipedia
load_wikipedia = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_wikipedia )

_fetch_naval_observatory = fonky.fetch_naval_observatory
fetch_naval_observatory = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_naval_observatory )

_fetch_satellite_center = fonky.fetch_satellite_center
fetch_satellite_center = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_satellite_center )

_fetch_nearby_objects = fonky.fetch_nearby_objects
fetch_nearby_objects = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_nearby_objects )

_fetch_open_science = fonky.fetch_open_science
fetch_open_science = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_open_science )

_fetch_space_weather = fonky.fetch_space_weather
fetch_space_weather = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_space_weather )

_fetch_astro_catalog = fonky.fetch_astro_catalog
fetch_astro_catalog = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_astro_catalog )

_fetch_astro_query = fonky.fetch_astro_query
fetch_astro_query = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_astro_query )

_fetch_star_map = fonky.fetch_star_map
fetch_star_map = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_star_map )

_fetch_star_chart = fonky.fetch_star_chart
fetch_star_chart = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_star_chart )

_fetch_open_sky = fonky.fetch_open_sky
fetch_open_sky = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_open_sky )

_load_google_drive_file = fonky.load_google_drive_file
load_google_drive_file = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_google_drive_file )

_load_google_drive_folder = fonky.load_google_drive_folder
load_google_drive_folder = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_google_drive_folder )

_load_onedrive = fonky.load_onedrive
load_onedrive = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_onedrive )

_load_google_cloud_file = fonky.load_google_cloud_file
load_google_cloud_file = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_google_cloud_file )

_load_aws_file = fonky.load_aws_file
load_aws_file = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_aws_file )

_load_google_speech_to_text = fonky.load_google_speech_to_text
load_google_speech_to_text = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_google_speech_to_text )

_load_google_bucket = fonky.load_google_bucket
load_google_bucket = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_google_bucket )

_load_aws_bucket = fonky.load_aws_bucket
load_aws_bucket = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_aws_bucket )

_fetch_census_data = fonky.fetch_census_data
fetch_census_data = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_census_data )

_fetch_socrata = fonky.fetch_socrata
fetch_socrata = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_socrata )

_fetch_united_nations = fonky.fetch_united_nations
fetch_united_nations = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_united_nations )

_fetch_world_population = fonky.fetch_world_population
fetch_world_population = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_world_population )

_load_open_city = fonky.load_open_city
load_open_city = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_open_city )

_load_text = fonky.load_text
load_text = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_text )

_load_csv = fonky.load_csv
load_csv = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_csv )

_read_pdf = fonky.read_pdf
read_pdf = tool( parse_docstring=True, error_on_invalid_docstring=True )( _read_pdf )

_load_pdf = fonky.load_pdf
load_pdf = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_pdf )

_load_excel = fonky.load_excel
load_excel = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_excel )

_load_word = fonky.load_word
load_word = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_word )

_load_markdown = fonky.load_markdown
load_markdown = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_markdown )

_load_html = fonky.load_html
load_html = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_html )

_load_outlook = fonky.load_outlook
load_outlook = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_outlook )

_load_spfx = fonky.load_spfx
load_spfx = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_spfx )

_load_spfx_folder = fonky.load_spfx_folder
load_spfx_folder = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_spfx_folder )

_load_powerpoint = fonky.load_powerpoint
load_powerpoint = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_powerpoint )

_load_powerpoint_multiple = fonky.load_powerpoint_multiple
load_powerpoint_multiple = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_powerpoint_multiple )

_load_email = fonky.load_email
load_email = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_email )

_load_json = fonky.load_json
load_json = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_json )

_load_xml = fonky.load_xml
load_xml = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_xml )

_load_xml_tree = fonky.load_xml_tree
load_xml_tree = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_xml_tree )

_load_jupyter_notebook = fonky.load_jupyter_notebook
load_jupyter_notebook = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_jupyter_notebook )

_fetch_google_weather_current = fonky.fetch_google_weather_current
fetch_google_weather_current = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_google_weather_current )

_fetch_google_weather_hourly_forecast = fonky.fetch_google_weather_hourly_forecast
fetch_google_weather_hourly_forecast = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_google_weather_hourly_forecast )

_fetch_google_weather_daily_forecast = fonky.fetch_google_weather_daily_forecast
fetch_google_weather_daily_forecast = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_google_weather_daily_forecast )

_fetch_google_weather_hourly_history = fonky.fetch_google_weather_hourly_history
fetch_google_weather_hourly_history = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_google_weather_hourly_history )

_fetch_google_weather_alerts = fonky.fetch_google_weather_alerts
fetch_google_weather_alerts = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_google_weather_alerts )

_fetch_earth_observatory = fonky.fetch_earth_observatory
fetch_earth_observatory = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_earth_observatory )

_fetch_open_weather = fonky.fetch_open_weather
fetch_open_weather = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_open_weather )

_fetch_historical_weather = fonky.fetch_historical_weather
fetch_historical_weather = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_historical_weather )

_fetch_usgs_earthquakes = fonky.fetch_usgs_earthquakes
fetch_usgs_earthquakes = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_usgs_earthquakes )

_fetch_usgs_water_data = fonky.fetch_usgs_water_data
fetch_usgs_water_data = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_usgs_water_data )

_fetch_air_now = fonky.fetch_air_now
fetch_air_now = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_air_now )

_fetch_climate_data = fonky.fetch_climate_data
fetch_climate_data = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_climate_data )

_fetch_eonet = fonky.fetch_eonet
fetch_eonet = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_eonet )

_fetch_envirofacts = fonky.fetch_envirofacts
fetch_envirofacts = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_envirofacts )

_fetch_tides_and_currents = fonky.fetch_tides_and_currents
fetch_tides_and_currents = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_tides_and_currents )

_fetch_uv_index = fonky.fetch_uv_index
fetch_uv_index = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_uv_index )

_fetch_purple_air = fonky.fetch_purple_air
fetch_purple_air = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_purple_air )

_fetch_open_aq = fonky.fetch_open_aq
fetch_open_aq = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_open_aq )

_fetch_firms = fonky.fetch_firms
fetch_firms = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_firms )

_geocode_location = fonky.geocode_location
geocode_location = tool( parse_docstring=True, error_on_invalid_docstring=True )( _geocode_location )

_geocode_coordinates = fonky.geocode_coordinates
geocode_coordinates = tool( parse_docstring=True, error_on_invalid_docstring=True )( _geocode_coordinates )

_validate_address = fonky.validate_address
validate_address = tool( parse_docstring=True, error_on_invalid_docstring=True )( _validate_address )

_request_directions = fonky.request_directions
request_directions = tool( parse_docstring=True, error_on_invalid_docstring=True )( _request_directions )

_fetch_global_imagery_wms_map = fonky.fetch_global_imagery_wms_map
fetch_global_imagery_wms_map = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_global_imagery_wms_map )

_fetch_global_imagery_map_services = fonky.fetch_global_imagery_map_services
fetch_global_imagery_map_services = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_global_imagery_map_services )

_fetch_global_imagery_mercator_map = fonky.fetch_global_imagery_mercator_map
fetch_global_imagery_mercator_map = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_global_imagery_mercator_map )

_fetch_google_geocoding = fonky.fetch_google_geocoding
fetch_google_geocoding = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_google_geocoding )

_fetch_usgs_national_map = fonky.fetch_usgs_national_map
fetch_usgs_national_map = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_usgs_national_map )

_fetch_usgs_sciencebase = fonky.fetch_usgs_sciencebase
fetch_usgs_sciencebase = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_usgs_sciencebase )

_fetch_health_data = fonky.fetch_health_data
fetch_health_data = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_health_data )

_fetch_global_health_data = fonky.fetch_global_health_data
fetch_global_health_data = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_global_health_data )

_fetch_wonder = fonky.fetch_wonder
fetch_wonder = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_wonder )

_load_pubmed = fonky.load_pubmed
load_pubmed = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_pubmed )

_fetch_web_page = fonky.fetch_web_page
fetch_web_page = tool( parse_docstring=True, error_on_invalid_docstring=True )( _fetch_web_page )

_convert_html_to_text = fonky.convert_html_to_text
convert_html_to_text = tool( parse_docstring=True, error_on_invalid_docstring=True )( _convert_html_to_text )

_extract_web_title = fonky.extract_web_title
extract_web_title = tool( parse_docstring=True, error_on_invalid_docstring=True )( _extract_web_title )

_extract_web_links = fonky.extract_web_links
extract_web_links = tool( parse_docstring=True, error_on_invalid_docstring=True )( _extract_web_links )

_extract_web_structured_data = fonky.extract_web_structured_data
extract_web_structured_data = tool( parse_docstring=True, error_on_invalid_docstring=True )( _extract_web_structured_data )

_crawl_web = fonky.crawl_web
crawl_web = tool( parse_docstring=True, error_on_invalid_docstring=True )( _crawl_web )

_scrape_crawler_page = fonky.scrape_crawler_page
scrape_crawler_page = tool( parse_docstring=True, error_on_invalid_docstring=True )( _scrape_crawler_page )

_render_web_page = fonky.render_web_page
render_web_page = tool( parse_docstring=True, error_on_invalid_docstring=True )( _render_web_page )

_load_web = fonky.load_web
load_web = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_web )

_load_web_recursive = fonky.load_web_recursive
load_web_recursive = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_web_recursive )

_load_web_pages = fonky.load_web_pages
load_web_pages = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_web_pages )

_load_github = fonky.load_github
load_github = tool( parse_docstring=True, error_on_invalid_docstring=True )( _load_github )

_scrape_web_page = fonky.scrape_web_page
scrape_web_page = tool( parse_docstring=True, error_on_invalid_docstring=True )( _scrape_web_page )

_scraper_html_to_text = fonky.scraper_html_to_text
scraper_html_to_text = tool( parse_docstring=True, error_on_invalid_docstring=True )( _scraper_html_to_text )

_scrape_paragraphs = fonky.scrape_paragraphs
scrape_paragraphs = tool( parse_docstring=True, error_on_invalid_docstring=True )( _scrape_paragraphs )

_scrape_lists = fonky.scrape_lists
scrape_lists = tool( parse_docstring=True, error_on_invalid_docstring=True )( _scrape_lists )

_scrape_tables = fonky.scrape_tables
scrape_tables = tool( parse_docstring=True, error_on_invalid_docstring=True )( _scrape_tables )

_scrape_articles = fonky.scrape_articles
scrape_articles = tool( parse_docstring=True, error_on_invalid_docstring=True )( _scrape_articles )

_scrape_headings = fonky.scrape_headings
scrape_headings = tool( parse_docstring=True, error_on_invalid_docstring=True )( _scrape_headings )

_scrape_divisions = fonky.scrape_divisions
scrape_divisions = tool( parse_docstring=True, error_on_invalid_docstring=True )( _scrape_divisions )

_scrape_sections = fonky.scrape_sections
scrape_sections = tool( parse_docstring=True, error_on_invalid_docstring=True )( _scrape_sections )

_scrape_blockquotes = fonky.scrape_blockquotes
scrape_blockquotes = tool( parse_docstring=True, error_on_invalid_docstring=True )( _scrape_blockquotes )

_scrape_hyperlinks = fonky.scrape_hyperlinks
scrape_hyperlinks = tool( parse_docstring=True, error_on_invalid_docstring=True )( _scrape_hyperlinks )

_scrape_images = fonky.scrape_images
scrape_images = tool( parse_docstring=True, error_on_invalid_docstring=True )( _scrape_images )

_encode_image = fonky.encode_image
encode_image = tool( parse_docstring=True, error_on_invalid_docstring=True )( _encode_image )

# ==========================================================================================
# DOMAIN GROUPS
# ==========================================================================================

ARCHIVES_TOOLS: Tuple[ BaseTool, ... ] = (fetch_arxiv, fetch_google_drive, fetch_wikipedia,
                                          fetch_news, fetch_google_search, fetch_gov_data,
                                          fetch_congress, fetch_internet_archive, fetch_grokipedia,
                                          load_arxiv, load_wikipedia,)

ASTRONOMICAL_TOOLS: Tuple[ BaseTool, ... ] = (fetch_naval_observatory, fetch_satellite_center,
                                              fetch_nearby_objects, fetch_open_science,
                                              fetch_space_weather, fetch_astro_catalog,
                                              fetch_astro_query, fetch_star_map, fetch_star_chart,
                                              fetch_open_sky,)

CLOUD_TOOLS: Tuple[ BaseTool, ... ] = (load_google_drive_file, load_google_drive_folder,
                                       load_onedrive, load_google_cloud_file, load_aws_file,
                                       load_google_speech_to_text, load_google_bucket,
                                       load_aws_bucket,)

DEMOGRAPHIC_TOOLS: Tuple[ BaseTool, ... ] = (fetch_census_data, fetch_socrata, fetch_united_nations,
                                             fetch_world_population, load_open_city,)

DOCUMENTS_TOOLS: Tuple[ BaseTool, ... ] = (load_text, load_csv, read_pdf, load_pdf, load_excel,
                                           load_word, load_markdown, load_html, load_outlook,
                                           load_spfx, load_spfx_folder, load_powerpoint,
                                           load_powerpoint_multiple, load_email, load_json,
                                           load_xml, load_xml_tree, load_jupyter_notebook,)

ENVIRONMENTAL_TOOLS: Tuple[ BaseTool, ... ] = (fetch_google_weather_current,
                                               fetch_google_weather_hourly_forecast,
                                               fetch_google_weather_daily_forecast,
                                               fetch_google_weather_hourly_history,
                                               fetch_google_weather_alerts, fetch_earth_observatory,
                                               fetch_open_weather, fetch_historical_weather,
                                               fetch_usgs_earthquakes, fetch_usgs_water_data,
                                               fetch_air_now, fetch_climate_data, fetch_eonet,
                                               fetch_envirofacts, fetch_tides_and_currents,
                                               fetch_uv_index, fetch_purple_air, fetch_open_aq,
                                               fetch_firms,)

GEOSPATIAL_TOOLS: Tuple[ BaseTool, ... ] = (geocode_location, geocode_coordinates, validate_address,
                                            request_directions, fetch_global_imagery_wms_map,
                                            fetch_global_imagery_map_services,
                                            fetch_global_imagery_mercator_map,
                                            fetch_google_geocoding, fetch_usgs_national_map,
                                            fetch_usgs_sciencebase,)

HEALTH_TOOLS: Tuple[ BaseTool, ... ] = (fetch_health_data, fetch_global_health_data, fetch_wonder,
                                        load_pubmed,)

WEB_TOOLS: Tuple[ BaseTool, ... ] = (fetch_web_page, convert_html_to_text, extract_web_title,
                                     extract_web_links, extract_web_structured_data, crawl_web,
                                     scrape_crawler_page, render_web_page, load_web,
                                     load_web_recursive, load_web_pages, load_github,
                                     scrape_web_page, scraper_html_to_text, scrape_paragraphs,
                                     scrape_lists, scrape_tables, scrape_articles, scrape_headings,
                                     scrape_divisions, scrape_sections, scrape_blockquotes,
                                     scrape_hyperlinks, scrape_images, encode_image,)

TOOL_DOMAINS: Dict[ str, Tuple[ BaseTool, ... ] ] = { 'archives': ARCHIVES_TOOLS,
		'astronomical': ASTRONOMICAL_TOOLS, 'cloud': CLOUD_TOOLS, 'demographic': DEMOGRAPHIC_TOOLS,
		'documents': DOCUMENTS_TOOLS, 'environmental': ENVIRONMENTAL_TOOLS,
		'geospatial': GEOSPATIAL_TOOLS, 'health': HEALTH_TOOLS, 'web': WEB_TOOLS, }


def get_domains( ) -> List[ str ]:
    """Return the supported Fonky LangChain tool domains.

    Purpose:
        Lists the public domain names used by the Fonky LangChain integration so calling
        code can populate configuration, UI controls, or agent-routing logic without
        duplicating domain identifiers.

    Returns:
        List[str]: Supported domain names in public API order.
    """
    return list( TOOL_DOMAINS.keys( ) )


def get_tools( domain: str ) -> List[ BaseTool ]:
    """Return the tool objects for one Fonky domain.

    Purpose:
        Supplies a bounded, workflow-specific set of LangChain tools for one Fonky domain.
        This keeps agent tool sets focused and avoids exposing all Fonky operations when an
        agent only needs one family of capabilities.

    Args:
        domain: Tool domain such as ``archives``, ``documents``, ``environmental``, or ``web``.

    Returns:
        List[BaseTool]: LangChain tool objects for the requested domain.

    Raises:
        ValueError: If ``domain`` is missing or unsupported.
    """
    throw_if( 'domain', domain )
    normalized = domain.strip( ).lower( )

    if normalized not in TOOL_DOMAINS:
        supported = ', '.join( TOOL_DOMAINS.keys( ) )
        raise ValueError(
            f'Unsupported Fonky tool domain "{domain}". Supported domains: {supported}.'
        )

    return list( TOOL_DOMAINS[ normalized ] )


def get_tool_names( domain: str ) -> List[ str ]:
    """Return the public tool names for one Fonky domain.

    Purpose:
        Supports discovery, documentation, and UI rendering without requiring caller code
        to introspect LangChain tool instances directly.

    Args:
        domain: Tool domain such as ``archives``, ``documents``, ``environmental``, or ``web``.

    Returns:
        List[str]: Public LangChain tool names for the requested domain.

    Raises:
        ValueError: If ``domain`` is missing or unsupported.
    """
    return [ tool.name for tool in get_tools( domain ) ]


__all__: List[ str ] = [
    'fetch_arxiv',
    'fetch_google_drive',
    'fetch_wikipedia',
    'fetch_news',
    'fetch_google_search',
    'fetch_gov_data',
    'fetch_congress',
    'fetch_internet_archive',
    'fetch_grokipedia',
    'load_arxiv',
    'load_wikipedia',
    'fetch_naval_observatory',
    'fetch_satellite_center',
    'fetch_nearby_objects',
    'fetch_open_science',
    'fetch_space_weather',
    'fetch_astro_catalog',
    'fetch_astro_query',
    'fetch_star_map',
    'fetch_star_chart',
    'fetch_open_sky',
    'load_google_drive_file',
    'load_google_drive_folder',
    'load_onedrive',
    'load_google_cloud_file',
    'load_aws_file',
    'load_google_speech_to_text',
    'load_google_bucket',
    'load_aws_bucket',
    'fetch_census_data',
    'fetch_socrata',
    'fetch_united_nations',
    'fetch_world_population',
    'load_open_city',
    'load_text',
    'load_csv',
    'read_pdf',
    'load_pdf',
    'load_excel',
    'load_word',
    'load_markdown',
    'load_html',
    'load_outlook',
    'load_spfx',
    'load_spfx_folder',
    'load_powerpoint',
    'load_powerpoint_multiple',
    'load_email',
    'load_json',
    'load_xml',
    'load_xml_tree',
    'load_jupyter_notebook',
    'fetch_google_weather_current',
    'fetch_google_weather_hourly_forecast',
    'fetch_google_weather_daily_forecast',
    'fetch_google_weather_hourly_history',
    'fetch_google_weather_alerts',
    'fetch_earth_observatory',
    'fetch_open_weather',
    'fetch_historical_weather',
    'fetch_usgs_earthquakes',
    'fetch_usgs_water_data',
    'fetch_air_now',
    'fetch_climate_data',
    'fetch_eonet',
    'fetch_envirofacts',
    'fetch_tides_and_currents',
    'fetch_uv_index',
    'fetch_purple_air',
    'fetch_open_aq',
    'fetch_firms',
    'geocode_location',
    'geocode_coordinates',
    'validate_address',
    'request_directions',
    'fetch_global_imagery_wms_map',
    'fetch_global_imagery_map_services',
    'fetch_global_imagery_mercator_map',
    'fetch_google_geocoding',
    'fetch_usgs_national_map',
    'fetch_usgs_sciencebase',
    'fetch_health_data',
    'fetch_global_health_data',
    'fetch_wonder',
    'load_pubmed',
    'fetch_web_page',
    'convert_html_to_text',
    'extract_web_title',
    'extract_web_links',
    'extract_web_structured_data',
    'crawl_web',
    'scrape_crawler_page',
    'render_web_page',
    'load_web',
    'load_web_recursive',
    'load_web_pages',
    'load_github',
    'scrape_web_page',
    'scraper_html_to_text',
    'scrape_paragraphs',
    'scrape_lists',
    'scrape_tables',
    'scrape_articles',
    'scrape_headings',
    'scrape_divisions',
    'scrape_sections',
    'scrape_blockquotes',
    'scrape_hyperlinks',
    'scrape_images',
    'encode_image',
    'ARCHIVES_TOOLS',
    'ASTRONOMICAL_TOOLS',
    'CLOUD_TOOLS',
    'DEMOGRAPHIC_TOOLS',
    'DOCUMENTS_TOOLS',
    'ENVIRONMENTAL_TOOLS',
    'GEOSPATIAL_TOOLS',
    'HEALTH_TOOLS',
    'WEB_TOOLS',
    'TOOL_DOMAINS',
    'get_domains',
    'get_tool_names',
    'get_tools',
]
