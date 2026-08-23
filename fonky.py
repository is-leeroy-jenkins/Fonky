'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                fonky.py
      Author:                  Terry D. Eppler
      Created:                 08-23-2026

      Last Modified By:        Terry D. Eppler
      Last Modified On:        08-23-2026
  ******************************************************************************************
  <summary>
    Provides the module-level functional interface for Fonky fetchers, loaders, and scrapers.

    Purpose:
        Exposes thin domain-organized functions over the implementation classes in
        ``fetchers.py``, ``loaders.py``, and ``scrapers.py``. Each function creates a fresh
        implementation instance, invokes the corresponding operation, and returns its result.
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
import datetime as dt

# ==========================================================================================
# FETCHERS IMPORTS
# ==========================================================================================

from .fetchers import AirNow
from .fetchers import ArXiv
from .fetchers import AstroCatalog
from .fetchers import AstroQuery
from .fetchers import CensusData
from .fetchers import ClimateData
from .fetchers import Congress
from .fetchers import EarthObservatory
from .fetchers import EnviroFacts
from .fetchers import EoNet
from .fetchers import Firms
from .fetchers import GlobalHealthData
from .fetchers import GlobalImagery
from .fetchers import GoogleDrive
from .fetchers import GoogleGeocoding
from .fetchers import GoogleMaps
from .fetchers import GoogleSearch
from .fetchers import GoogleWeather
from .fetchers import GovData
from .fetchers import Grokipedia
from .fetchers import HealthData
from .fetchers import HistoricalWeather
from .fetchers import InternetArchive
from .fetchers import NavalObservatory
from .fetchers import NearbyObjects
from .fetchers import OpenAQ
from .fetchers import OpenScience
from .fetchers import OpenSky
from .fetchers import OpenWeather
from .fetchers import PurpleAir
from .fetchers import SatelliteCenter
from .fetchers import Socrata
from .fetchers import SpaceWeather
from .fetchers import StarChart
from .fetchers import StarMap
from .fetchers import TheNews
from .fetchers import TidesAndCurrents
from .fetchers import USGSEarthquakes
from .fetchers import USGSScienceBase
from .fetchers import USGSTheNationalMap
from .fetchers import USGSWaterData
from .fetchers import UnitedNations
from .fetchers import UvIndex
from .fetchers import WebCrawler
from .fetchers import WebFetcher
from .fetchers import Wikipedia
from .fetchers import Wonder
from .fetchers import WorldPopulation
from .fetchers import encode_image as _encode_image

# ==========================================================================================
# LOADERS IMPORTS
# ==========================================================================================

from .loaders import ArXivLoader
from .loaders import AwsBucketLoader
from .loaders import AwsFileLoader
from .loaders import CsvLoader
from .loaders import EmailLoader
from .loaders import ExcelLoader
from .loaders import GithubLoader
from .loaders import GoogleBucketLoader
from .loaders import GoogleCloudFileLoader
from .loaders import GoogleDriveLoader
from .loaders import GoogleSpeechToTextLoader
from .loaders import HtmlLoader
from .loaders import JsonLoader
from .loaders import JupyterNotebookLoader
from .loaders import MarkdownLoader
from .loaders import OneDriveDocLoader
from .loaders import OpenCityLoader
from .loaders import OutlookLoader
from .loaders import PdfLoader
from .loaders import PdfReader
from .loaders import PowerPointLoader
from .loaders import PubMedSearchLoader
from .loaders import SpfxLoader
from .loaders import TextLoader
from .loaders import WebLoader
from .loaders import WikiLoader
from .loaders import WordLoader
from .loaders import XmlLoader

# ==========================================================================================
# SCRAPERS IMPORTS
# ==========================================================================================

from .scrapers import WebExtractor

# ==========================================================================================
# ARCHIVES
# ==========================================================================================

def fetch_arxiv( question: str, max_documents: int=None, full_documents: bool=None,
		include_metadata: bool=None ) -> Any:
    """Fetch ArXiv research document retrieval.

    Purpose:
        Provides direct module-level access to ``ArXiv.fetch`` using a fresh ``ArXiv`` instance.

    Args:
        question (str): Value passed to ``ArXiv.fetch``.
        max_documents (int): Value passed to ``ArXiv.fetch``.
        full_documents (bool): Value passed to ``ArXiv.fetch``.
        include_metadata (bool): Value passed to ``ArXiv.fetch``.

    Returns:
        Any: Value returned by ``ArXiv.fetch``.
    """
    _instance = ArXiv( )
    return _instance.fetch( question=question, max_documents=max_documents,
	    full_documents=full_documents, include_metadata=include_metadata )

def fetch_google_drive( question: str, folder_id: str='root', results: int=10,
		template: str='gdrive-query', mime_type: str=None, mode: str='documents' ) -> Any:
    """Fetch Google Drive document retrieval.

    Purpose:
        Provides direct module-level access to ``GoogleDrive.fetch`` using a fresh ``GoogleDrive`` instance.

    Args:
        question (str): Value passed to ``GoogleDrive.fetch``.
        folder_id (str): Value passed to ``GoogleDrive.fetch``.
        results (int): Value passed to ``GoogleDrive.fetch``.
        template (str): Value passed to ``GoogleDrive.fetch``.
        mime_type (str): Value passed to ``GoogleDrive.fetch``.
        mode (str): Value passed to ``GoogleDrive.fetch``.

    Returns:
        Any: Value returned by ``GoogleDrive.fetch``.
    """
    _instance = GoogleDrive( )
    return _instance.fetch( question=question, folder_id=folder_id, results=results, template=template, mime_type=mime_type, mode=mode )

def fetch_wikipedia( question: str, language: str=None, max_documents: int=None,
		include_metadata: bool=None ) -> Any:
    """Fetch Wikipedia document retrieval.

    Purpose:
        Provides direct module-level access to ``Wikipedia.fetch`` using a fresh ``Wikipedia`` instance.

    Args:
        question (str): Value passed to ``Wikipedia.fetch``.
        language (str): Value passed to ``Wikipedia.fetch``.
        max_documents (int): Value passed to ``Wikipedia.fetch``.
        include_metadata (bool): Value passed to ``Wikipedia.fetch``.

    Returns:
        Any: Value returned by ``Wikipedia.fetch``.
    """
    _instance = Wikipedia( )
    return _instance.fetch( question=question, language=language, max_documents=max_documents, include_metadata=include_metadata )

def fetch_news( endpoint: str='all', query: str='', language: str='en', categories: str='',
		exclude_categories: str='', locale: str='', domains: str='', exclude_domains: str='',
		source_ids: str='', exclude_source_ids: str='', published_after: str='',
		published_before: str='', published_on: str='', sort: str='published_at',
		limit: int=10, page: int=1, include_similar: bool=True,
		headlines_per_category: int=6, time: int=10, api_key: str=None ) -> Any:
    """Fetch The News API article retrieval.

    Purpose:
        Provides direct module-level access to ``TheNews.fetch`` using a fresh ``TheNews`` instance.

    Args:
        endpoint (str): Value passed to ``TheNews.fetch``.
        query (str): Value passed to ``TheNews.fetch``.
        language (str): Value passed to ``TheNews.fetch``.
        categories (str): Value passed to ``TheNews.fetch``.
        exclude_categories (str): Value passed to ``TheNews.fetch``.
        locale (str): Value passed to ``TheNews.fetch``.
        domains (str): Value passed to ``TheNews.fetch``.
        exclude_domains (str): Value passed to ``TheNews.fetch``.
        source_ids (str): Value passed to ``TheNews.fetch``.
        exclude_source_ids (str): Value passed to ``TheNews.fetch``.
        published_after (str): Value passed to ``TheNews.fetch``.
        published_before (str): Value passed to ``TheNews.fetch``.
        published_on (str): Value passed to ``TheNews.fetch``.
        sort (str): Value passed to ``TheNews.fetch``.
        limit (int): Value passed to ``TheNews.fetch``.
        page (int): Value passed to ``TheNews.fetch``.
        include_similar (bool): Value passed to ``TheNews.fetch``.
        headlines_per_category (int): Value passed to ``TheNews.fetch``.
        time (int): Value passed to ``TheNews.fetch``.
        api_key (str): Value passed to ``TheNews.fetch``.

    Returns:
        Any: Value returned by ``TheNews.fetch``.
    """
    _instance = TheNews( )
    return _instance.fetch( endpoint=endpoint, query=query, language=language, categories=categories, exclude_categories=exclude_categories, locale=locale, domains=domains, exclude_domains=exclude_domains, source_ids=source_ids, exclude_source_ids=exclude_source_ids, published_after=published_after, published_before=published_before, published_on=published_on, sort=sort, limit=limit, page=page, include_similar=include_similar, headlines_per_category=headlines_per_category, time=time, api_key=api_key )

def fetch_google_search( keywords: str, results: int=10, start: int=1, exact_terms: str='',
		exclude_terms: str='', file_type: str='', date_restrict: str='', gl: str='', lr: str='',
		safe: str='off', search_type: str='', site_search: str='', site_search_filter: str='',
		sort: str='', img_size: str='', img_type: str='', img_color_type: str='',
		img_dominant_color: str='', time: int=10, api_key: str=None, cse_id: str=None ) -> Any:
    """Fetch Google Custom Search retrieval.

    Purpose:
        Provides direct module-level access to ``GoogleSearch.fetch`` using a fresh ``GoogleSearch`` instance.

    Args:
        keywords (str): Value passed to ``GoogleSearch.fetch``.
        results (int): Value passed to ``GoogleSearch.fetch``.
        start (int): Value passed to ``GoogleSearch.fetch``.
        exact_terms (str): Value passed to ``GoogleSearch.fetch``.
        exclude_terms (str): Value passed to ``GoogleSearch.fetch``.
        file_type (str): Value passed to ``GoogleSearch.fetch``.
        date_restrict (str): Value passed to ``GoogleSearch.fetch``.
        gl (str): Value passed to ``GoogleSearch.fetch``.
        lr (str): Value passed to ``GoogleSearch.fetch``.
        safe (str): Value passed to ``GoogleSearch.fetch``.
        search_type (str): Value passed to ``GoogleSearch.fetch``.
        site_search (str): Value passed to ``GoogleSearch.fetch``.
        site_search_filter (str): Value passed to ``GoogleSearch.fetch``.
        sort (str): Value passed to ``GoogleSearch.fetch``.
        img_size (str): Value passed to ``GoogleSearch.fetch``.
        img_type (str): Value passed to ``GoogleSearch.fetch``.
        img_color_type (str): Value passed to ``GoogleSearch.fetch``.
        img_dominant_color (str): Value passed to ``GoogleSearch.fetch``.
        time (int): Value passed to ``GoogleSearch.fetch``.
        api_key (str): Value passed to ``GoogleSearch.fetch``.
        cse_id (str): Value passed to ``GoogleSearch.fetch``.

    Returns:
        Any: Value returned by ``GoogleSearch.fetch``.
    """
    _instance = GoogleSearch( )
    return _instance.fetch( keywords=keywords, results=results, start=start, exact_terms=exact_terms, exclude_terms=exclude_terms, file_type=file_type, date_restrict=date_restrict, gl=gl, lr=lr, safe=safe, search_type=search_type, site_search=site_search, site_search_filter=site_search_filter, sort=sort, img_size=img_size, img_type=img_type, img_color_type=img_color_type, img_dominant_color=img_dominant_color, time=time, api_key=api_key, cse_id=cse_id )

def fetch_gov_data( mode: str='search', query: str='', page_size: int=10, offset_mark: str='*',
		sort_field: str='score', sort_order: str='DESC', package_id: str='', collection: str='',
		start_date: str='', time: int=20 ) -> Any:
    """Fetch Data.gov package and collection retrieval.

    Purpose:
        Provides direct module-level access to ``GovData.fetch`` using a fresh ``GovData`` instance.

    Args:
        mode (str): Value passed to ``GovData.fetch``.
        query (str): Value passed to ``GovData.fetch``.
        page_size (int): Value passed to ``GovData.fetch``.
        offset_mark (str): Value passed to ``GovData.fetch``.
        sort_field (str): Value passed to ``GovData.fetch``.
        sort_order (str): Value passed to ``GovData.fetch``.
        package_id (str): Value passed to ``GovData.fetch``.
        collection (str): Value passed to ``GovData.fetch``.
        start_date (str): Value passed to ``GovData.fetch``.
        time (int): Value passed to ``GovData.fetch``.

    Returns:
        Any: Value returned by ``GovData.fetch``.
    """
    _instance = GovData( )
    return _instance.fetch( mode=mode, query=query, page_size=page_size, offset_mark=offset_mark, sort_field=sort_field, sort_order=sort_order, package_id=package_id, collection=collection, start_date=start_date, time=time )

def fetch_congress( mode: str='congresses', congress: int=0, bill_type: str='', bill_number: int=0,
		law_type: str='', law_number: int=0, report_type: str='', report_number: int=0,
		offset: int=0, limit: int=20, sort: str='updateDate+desc', from_date_time: str='',
		to_date_time: str='', conference: bool=False, time: int=20 ) -> Any:
    """Fetch Congress.gov legislative data retrieval.

    Purpose:
        Provides direct module-level access to ``Congress.fetch`` using a fresh ``Congress`` instance.

    Args:
        mode (str): Value passed to ``Congress.fetch``.
        congress (int): Value passed to ``Congress.fetch``.
        bill_type (str): Value passed to ``Congress.fetch``.
        bill_number (int): Value passed to ``Congress.fetch``.
        law_type (str): Value passed to ``Congress.fetch``.
        law_number (int): Value passed to ``Congress.fetch``.
        report_type (str): Value passed to ``Congress.fetch``.
        report_number (int): Value passed to ``Congress.fetch``.
        offset (int): Value passed to ``Congress.fetch``.
        limit (int): Value passed to ``Congress.fetch``.
        sort (str): Value passed to ``Congress.fetch``.
        from_date_time (str): Value passed to ``Congress.fetch``.
        to_date_time (str): Value passed to ``Congress.fetch``.
        conference (bool): Value passed to ``Congress.fetch``.
        time (int): Value passed to ``Congress.fetch``.

    Returns:
        Any: Value returned by ``Congress.fetch``.
    """
    _instance = Congress( )
    return _instance.fetch( mode=mode, congress=congress, bill_type=bill_type, bill_number=bill_number, law_type=law_type, law_number=law_number, report_type=report_type, report_number=report_number, offset=offset, limit=limit, sort=sort, from_date_time=from_date_time, to_date_time=to_date_time, conference=conference, time=time )

def fetch_internet_archive( keywords: str, fields: List[str] | None=None, rows: int=10, page: int=1,
		sort: str='downloads desc', media_type: str='', collection: str='', time: int=20 ) -> Any:
    """Fetch Internet Archive search and metadata retrieval.

    Purpose:
        Provides direct module-level access to ``InternetArchive.fetch`` using a fresh ``InternetArchive`` instance.

    Args:
        keywords (str): Value passed to ``InternetArchive.fetch``.
        fields (List[str] | None): Value passed to ``InternetArchive.fetch``.
        rows (int): Value passed to ``InternetArchive.fetch``.
        page (int): Value passed to ``InternetArchive.fetch``.
        sort (str): Value passed to ``InternetArchive.fetch``.
        media_type (str): Value passed to ``InternetArchive.fetch``.
        collection (str): Value passed to ``InternetArchive.fetch``.
        time (int): Value passed to ``InternetArchive.fetch``.

    Returns:
        Any: Value returned by ``InternetArchive.fetch``.
    """
    _instance = InternetArchive( )
    return _instance.fetch( keywords=keywords, fields=fields, rows=rows, page=page, sort=sort, media_type=media_type, collection=collection, time=time )

def fetch_grokipedia( mode: str='search', query: str='', page: str='', limit: int=12,
		offset: int=0, include_content: bool=True ) -> Any:
    """Fetch Grokipedia search and page retrieval.

    Purpose:
        Provides direct module-level access to ``Grokipedia.fetch`` using a fresh ``Grokipedia`` instance.

    Args:
        mode (str): Value passed to ``Grokipedia.fetch``.
        query (str): Value passed to ``Grokipedia.fetch``.
        page (str): Value passed to ``Grokipedia.fetch``.
        limit (int): Value passed to ``Grokipedia.fetch``.
        offset (int): Value passed to ``Grokipedia.fetch``.
        include_content (bool): Value passed to ``Grokipedia.fetch``.

    Returns:
        Any: Value returned by ``Grokipedia.fetch``.
    """
    _instance = Grokipedia( )
    return _instance.fetch( mode=mode, query=query, page=page, limit=limit, offset=offset, include_content=include_content )

def load_arxiv( question: str ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``ArXivLoader.load`` using a fresh ``ArXivLoader`` instance.

    Args:
        question (str): Value passed to ``ArXivLoader.load``.

    Returns:
        Any: Value returned by ``ArXivLoader.load``.
    """
    _instance = ArXivLoader( )
    return _instance.load( question=question )

def load_wikipedia( question: str ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``WikiLoader.load`` using a fresh ``WikiLoader`` instance.

    Args:
        question (str): Value passed to ``WikiLoader.load``.

    Returns:
        Any: Value returned by ``WikiLoader.load``.
    """
    _instance = WikiLoader( )
    return _instance.load( question=question )

# ==========================================================================================
# ASTRONOMICAL
# ==========================================================================================

def fetch_naval_observatory( mode: str='celnav', date_value: str='', time_value: str='',
		latitude: float=0.0, longitude: float=0.0, location_label: str='', time: int=20 ) -> Any:
    """Fetch U.S. Naval Observatory celestial-navigation data.

    Purpose:
        Provides direct module-level access to ``NavalObservatory.fetch`` using a fresh ``NavalObservatory`` instance.

    Args:
        mode (str): Value passed to ``NavalObservatory.fetch``.
        date_value (str): Value passed to ``NavalObservatory.fetch``.
        time_value (str): Value passed to ``NavalObservatory.fetch``.
        latitude (float): Value passed to ``NavalObservatory.fetch``.
        longitude (float): Value passed to ``NavalObservatory.fetch``.
        location_label (str): Value passed to ``NavalObservatory.fetch``.
        time (int): Value passed to ``NavalObservatory.fetch``.

    Returns:
        Any: Value returned by ``NavalObservatory.fetch``.
    """
    _instance = NavalObservatory( )
    return _instance.fetch( mode=mode, date_value=date_value, time_value=time_value, latitude=latitude, longitude=longitude, location_label=location_label, time=time )

def fetch_satellite_center( mode: str='observatories', query: str='', start_time: str='',
		end_time: str='', coordinate_systems: str='gse', resolution_factor: int=1, time: int=20 ) -> Any:
    """Fetch SSC satellite observatory, ground-station, and location data.

    Purpose:
        Provides direct module-level access to ``SatelliteCenter.fetch`` using a fresh ``SatelliteCenter`` instance.

    Args:
        mode (str): Value passed to ``SatelliteCenter.fetch``.
        query (str): Value passed to ``SatelliteCenter.fetch``.
        start_time (str): Value passed to ``SatelliteCenter.fetch``.
        end_time (str): Value passed to ``SatelliteCenter.fetch``.
        coordinate_systems (str): Value passed to ``SatelliteCenter.fetch``.
        resolution_factor (int): Value passed to ``SatelliteCenter.fetch``.
        time (int): Value passed to ``SatelliteCenter.fetch``.

    Returns:
        Any: Value returned by ``SatelliteCenter.fetch``.
    """
    _instance = SatelliteCenter( )
    return _instance.fetch( mode=mode, query=query, start_time=start_time, end_time=end_time, coordinate_systems=coordinate_systems, resolution_factor=resolution_factor, time=time )

def fetch_nearby_objects( mode: str='close_approaches', start_date: str='', end_date: str='',
		query: str='', query_type: str='sstr', dist_max: str='10LD', body: str='Earth',
		sort: str='date', limit: int=20, dv: float=6.0, dur: int=360, stay: int=8,
		launch: str='2020-2045', h: float=26.0, occ: int=7, include_physical: bool=True, include_close_approaches: bool=True, ca_body: str='Earth', include_discovery: bool=True, time: int=20 ) -> Any:
    """Fetch JPL SSD and CNEOS near-Earth object data.

    Purpose:
        Provides direct module-level access to ``NearbyObjects.fetch`` using a fresh ``NearbyObjects`` instance.

    Args:
        mode (str): Value passed to ``NearbyObjects.fetch``.
        start_date (str): Value passed to ``NearbyObjects.fetch``.
        end_date (str): Value passed to ``NearbyObjects.fetch``.
        query (str): Value passed to ``NearbyObjects.fetch``.
        query_type (str): Value passed to ``NearbyObjects.fetch``.
        dist_max (str): Value passed to ``NearbyObjects.fetch``.
        body (str): Value passed to ``NearbyObjects.fetch``.
        sort (str): Value passed to ``NearbyObjects.fetch``.
        limit (int): Value passed to ``NearbyObjects.fetch``.
        dv (float): Value passed to ``NearbyObjects.fetch``.
        dur (int): Value passed to ``NearbyObjects.fetch``.
        stay (int): Value passed to ``NearbyObjects.fetch``.
        launch (str): Value passed to ``NearbyObjects.fetch``.
        h (float): Value passed to ``NearbyObjects.fetch``.
        occ (int): Value passed to ``NearbyObjects.fetch``.
        include_physical (bool): Value passed to ``NearbyObjects.fetch``.
        include_close_approaches (bool): Value passed to ``NearbyObjects.fetch``.
        ca_body (str): Value passed to ``NearbyObjects.fetch``.
        include_discovery (bool): Value passed to ``NearbyObjects.fetch``.
        time (int): Value passed to ``NearbyObjects.fetch``.

    Returns:
        Any: Value returned by ``NearbyObjects.fetch``.
    """
    _instance = NearbyObjects( )
    return _instance.fetch( mode=mode, start_date=start_date, end_date=end_date, query=query, query_type=query_type, dist_max=dist_max, body=body, sort=sort, limit=limit, dv=dv, dur=dur, stay=stay, launch=launch, h=h, occ=occ, include_physical=include_physical, include_close_approaches=include_close_approaches, ca_body=ca_body, include_discovery=include_discovery, time=time )

def fetch_open_science( mode: str='dataset', query: str='', accession: str='',
		format_value: str='json', time: int=20 ) -> Any:
    """Fetch NASA Open Science Data Repository resources.

    Purpose:
        Provides direct module-level access to ``OpenScience.fetch`` using a fresh ``OpenScience`` instance.

    Args:
        mode (str): Value passed to ``OpenScience.fetch``.
        query (str): Value passed to ``OpenScience.fetch``.
        accession (str): Value passed to ``OpenScience.fetch``.
        format_value (str): Value passed to ``OpenScience.fetch``.
        time (int): Value passed to ``OpenScience.fetch``.

    Returns:
        Any: Value returned by ``OpenScience.fetch``.
    """
    _instance = OpenScience( )
    return _instance.fetch( mode=mode, query=query, accession=accession, format_value=format_value, time=time )

def fetch_space_weather( mode: str='cme', start_date: str='', end_date: str='', time: int=20,
		location: str='ALL', catalog: str='ALL', notification_type: str='all', most_accurate_only: bool=True, complete_entry_only: bool=True, speed: int=0, half_angle: int=0, keyword: str='', api_key: str=None ) -> Any:
    """Fetch NASA DONKI space weather endpoints.

    Purpose:
        Provides direct module-level access to ``SpaceWeather.fetch`` using a fresh ``SpaceWeather`` instance.

    Args:
        mode (str): Value passed to ``SpaceWeather.fetch``.
        start_date (str): Value passed to ``SpaceWeather.fetch``.
        end_date (str): Value passed to ``SpaceWeather.fetch``.
        time (int): Value passed to ``SpaceWeather.fetch``.
        location (str): Value passed to ``SpaceWeather.fetch``.
        catalog (str): Value passed to ``SpaceWeather.fetch``.
        notification_type (str): Value passed to ``SpaceWeather.fetch``.
        most_accurate_only (bool): Value passed to ``SpaceWeather.fetch``.
        complete_entry_only (bool): Value passed to ``SpaceWeather.fetch``.
        speed (int): Value passed to ``SpaceWeather.fetch``.
        half_angle (int): Value passed to ``SpaceWeather.fetch``.
        keyword (str): Value passed to ``SpaceWeather.fetch``.
        api_key (str): Value passed to ``SpaceWeather.fetch``.

    Returns:
        Any: Value returned by ``SpaceWeather.fetch``.
    """
    _instance = SpaceWeather( )
    return _instance.fetch( mode=mode, start_date=start_date, end_date=end_date, time=time, location=location, catalog=catalog, notification_type=notification_type, most_accurate_only=most_accurate_only, complete_entry_only=complete_entry_only, speed=speed, half_angle=half_angle, keyword=keyword, api_key=api_key )

def fetch_astro_catalog( mode: str='object_query', query: str='', quantity: str='',
		attributes: str='', arguments: str='', ra: str='', dec: str='', radius: int=2,
		data_format: str='json', time: int=20 ) -> Any:
    """Fetch Open Astronomy Catalog queries.

    Purpose:
        Provides direct module-level access to ``AstroCatalog.fetch`` using a fresh ``AstroCatalog`` instance.

    Args:
        mode (str): Value passed to ``AstroCatalog.fetch``.
        query (str): Value passed to ``AstroCatalog.fetch``.
        quantity (str): Value passed to ``AstroCatalog.fetch``.
        attributes (str): Value passed to ``AstroCatalog.fetch``.
        arguments (str): Value passed to ``AstroCatalog.fetch``.
        ra (str): Value passed to ``AstroCatalog.fetch``.
        dec (str): Value passed to ``AstroCatalog.fetch``.
        radius (int): Value passed to ``AstroCatalog.fetch``.
        data_format (str): Value passed to ``AstroCatalog.fetch``.
        time (int): Value passed to ``AstroCatalog.fetch``.

    Returns:
        Any: Value returned by ``AstroCatalog.fetch``.
    """
    _instance = AstroCatalog( )
    return _instance.fetch( mode=mode, query=query, quantity=quantity, attributes=attributes, arguments=arguments, ra=ra, dec=dec, radius=radius, data_format=data_format, time=time )

def fetch_astro_query( mode: str='object_search', query: str='', ra: str='', dec: str='',
		radius: float=0.5, radius_unit: str='deg', row_limit: int=100 ) -> Any:
    """Fetch Simbad and astronomy object search operations.

    Purpose:
        Provides direct module-level access to ``AstroQuery.fetch`` using a fresh ``AstroQuery`` instance.

    Args:
        mode (str): Value passed to ``AstroQuery.fetch``.
        query (str): Value passed to ``AstroQuery.fetch``.
        ra (str): Value passed to ``AstroQuery.fetch``.
        dec (str): Value passed to ``AstroQuery.fetch``.
        radius (float): Value passed to ``AstroQuery.fetch``.
        radius_unit (str): Value passed to ``AstroQuery.fetch``.
        row_limit (int): Value passed to ``AstroQuery.fetch``.

    Returns:
        Any: Value returned by ``AstroQuery.fetch``.
    """
    _instance = AstroQuery( )
    return _instance.fetch( mode=mode, query=query, ra=ra, dec=dec, radius=radius, radius_unit=radius_unit, row_limit=row_limit )

def fetch_star_map( mode: str='object_link', query: str='', ra: float=0.0, dec: float=0.0,
		zoom: int=5, image_source: str='DSS2', box_color: str='yellow', show_box: bool=True,
		show_grid: bool=True, show_lines: bool=True, show_boundaries: bool=True,
		show_const_names: bool=False, time: int=20 ) -> Any:
    """Fetch astronomical object map links and imagery.

    Purpose:
        Provides direct module-level access to ``StarMap.fetch`` using a fresh ``StarMap`` instance.

    Args:
        mode (str): Value passed to ``StarMap.fetch``.
        query (str): Value passed to ``StarMap.fetch``.
        ra (float): Value passed to ``StarMap.fetch``.
        dec (float): Value passed to ``StarMap.fetch``.
        zoom (int): Value passed to ``StarMap.fetch``.
        image_source (str): Value passed to ``StarMap.fetch``.
        box_color (str): Value passed to ``StarMap.fetch``.
        show_box (bool): Value passed to ``StarMap.fetch``.
        show_grid (bool): Value passed to ``StarMap.fetch``.
        show_lines (bool): Value passed to ``StarMap.fetch``.
        show_boundaries (bool): Value passed to ``StarMap.fetch``.
        show_const_names (bool): Value passed to ``StarMap.fetch``.
        time (int): Value passed to ``StarMap.fetch``.

    Returns:
        Any: Value returned by ``StarMap.fetch``.
    """
    _instance = StarMap( )
    return _instance.fetch( mode=mode, query=query, ra=ra, dec=dec, zoom=zoom, image_source=image_source, box_color=box_color, show_box=show_box, show_grid=show_grid, show_lines=show_lines, show_boundaries=show_boundaries, show_const_names=show_const_names, time=time )

def fetch_star_chart( mode: str='object_chart', query: str='', ra: float=0.0,
		dec: float=0.0, zoom: int=5, image_source: str='DSS2', box_color: str='yellow',
		show_box: bool=True, show_grid: bool=True, show_lines: bool=True, show_boundaries: bool=True,
		show_const_names: bool=False, width: int=900, height: int=450,
		magnitude: float=7.5, time: int=20 ) -> Any:
    """Fetch static star chart and coordinate chart generation.

    Purpose:
        Provides direct module-level access to ``StarChart.fetch`` using a fresh ``StarChart`` instance.

    Args:
        mode (str): Value passed to ``StarChart.fetch``.
        query (str): Value passed to ``StarChart.fetch``.
        ra (float): Value passed to ``StarChart.fetch``.
        dec (float): Value passed to ``StarChart.fetch``.
        zoom (int): Value passed to ``StarChart.fetch``.
        image_source (str): Value passed to ``StarChart.fetch``.
        box_color (str): Value passed to ``StarChart.fetch``.
        show_box (bool): Value passed to ``StarChart.fetch``.
        show_grid (bool): Value passed to ``StarChart.fetch``.
        show_lines (bool): Value passed to ``StarChart.fetch``.
        show_boundaries (bool): Value passed to ``StarChart.fetch``.
        show_const_names (bool): Value passed to ``StarChart.fetch``.
        width (int): Value passed to ``StarChart.fetch``.
        height (int): Value passed to ``StarChart.fetch``.
        magnitude (float): Value passed to ``StarChart.fetch``.
        time (int): Value passed to ``StarChart.fetch``.

    Returns:
        Any: Value returned by ``StarChart.fetch``.
    """
    _instance = StarChart( )
    return _instance.fetch( mode=mode, query=query, ra=ra, dec=dec, zoom=zoom, image_source=image_source, box_color=box_color, show_box=show_box, show_grid=show_grid, show_lines=show_lines, show_boundaries=show_boundaries, show_const_names=show_const_names, width=width, height=height, magnitude=magnitude, time=time )

def fetch_open_sky( mode: str='states_bbox', icao24: str='', airport: str='', begin: int=None,
		end: int=None, time_value: int=None, lamin: float | None=None,
		lomin: float | None=None, lamax: float | None=None, lomax: float | None=None,
		extended: bool=False, client_id: str=None, client_secret: str=None, time: int=20 ) -> Any:
    """Fetch OpenSky Network aircraft, airport, and state-vector data.

    Purpose:
        Provides direct module-level access to ``OpenSky.fetch`` using a fresh ``OpenSky`` instance.

    Args:
        mode (str): Value passed to ``OpenSky.fetch``.
        icao24 (str): Value passed to ``OpenSky.fetch``.
        airport (str): Value passed to ``OpenSky.fetch``.
        begin (int): Value passed to ``OpenSky.fetch``.
        end (int): Value passed to ``OpenSky.fetch``.
        time_value (int): Value passed to ``OpenSky.fetch``.
        lamin (float | None): Value passed to ``OpenSky.fetch``.
        lomin (float | None): Value passed to ``OpenSky.fetch``.
        lamax (float | None): Value passed to ``OpenSky.fetch``.
        lomax (float | None): Value passed to ``OpenSky.fetch``.
        extended (bool): Value passed to ``OpenSky.fetch``.
        client_id (str): Value passed to ``OpenSky.fetch``.
        client_secret (str): Value passed to ``OpenSky.fetch``.
        time (int): Value passed to ``OpenSky.fetch``.

    Returns:
        Any: Value returned by ``OpenSky.fetch``.
    """
    _instance = OpenSky( )
    return _instance.fetch( mode=mode, icao24=icao24, airport=airport, begin=begin, end=end, time_value=time_value, lamin=lamin, lomin=lomin, lamax=lamax, lomax=lomax, extended=extended, client_id=client_id, client_secret=client_secret, time=time )

# ==========================================================================================
# CLOUD
# ==========================================================================================

def load_google_drive_file( file_id: str, recursive: bool=False ) -> Any:
    """Load a provider file.

    Purpose:
        Provides direct module-level access to ``GoogleDriveLoader.load_file`` using a fresh ``GoogleDriveLoader`` instance.

    Args:
        file_id (str): Value passed to ``GoogleDriveLoader.load_file``.
        recursive (bool): Value passed to ``GoogleDriveLoader.load_file``.

    Returns:
        Any: Value returned by ``GoogleDriveLoader.load_file``.
    """
    _instance = GoogleDriveLoader( )
    return _instance.load_file( file_id=file_id, recursive=recursive )

def load_google_drive_folder( folder_id: str, recursive: bool=False ) -> Any:
    """Load provider folder content.

    Purpose:
        Provides direct module-level access to ``GoogleDriveLoader.load_folder`` using a fresh ``GoogleDriveLoader`` instance.

    Args:
        folder_id (str): Value passed to ``GoogleDriveLoader.load_folder``.
        recursive (bool): Value passed to ``GoogleDriveLoader.load_folder``.

    Returns:
        Any: Value returned by ``GoogleDriveLoader.load_folder``.
    """
    _instance = GoogleDriveLoader( )
    return _instance.load_folder( folder_id=folder_id, recursive=recursive )

def load_onedrive( drive_id: str, folder_path: Optional[str]=None,
		object_ids: Optional[List[str]]=None, auth_with_token: bool=True ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``OneDriveDocLoader.load`` using a fresh ``OneDriveDocLoader`` instance.

    Args:
        drive_id (str): Value passed to ``OneDriveDocLoader.load``.
        folder_path (Optional[str]): Value passed to ``OneDriveDocLoader.load``.
        object_ids (Optional[List[str]]): Value passed to ``OneDriveDocLoader.load``.
        auth_with_token (bool): Value passed to ``OneDriveDocLoader.load``.

    Returns:
        Any: Value returned by ``OneDriveDocLoader.load``.
    """
    _instance = OneDriveDocLoader( )
    return _instance.load( drive_id=drive_id, folder_path=folder_path, object_ids=object_ids, auth_with_token=auth_with_token )

def load_google_cloud_file( project_name: str, bucket: str, blob: str ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``GoogleCloudFileLoader.load`` using a fresh ``GoogleCloudFileLoader`` instance.

    Args:
        project_name (str): Value passed to ``GoogleCloudFileLoader.load``.
        bucket (str): Value passed to ``GoogleCloudFileLoader.load``.
        blob (str): Value passed to ``GoogleCloudFileLoader.load``.

    Returns:
        Any: Value returned by ``GoogleCloudFileLoader.load``.
    """
    _instance = GoogleCloudFileLoader( )
    return _instance.load( project_name=project_name, bucket=bucket, blob=blob )

def load_aws_file( bucket: str, key: str, aws_access_key_id: Optional[str]=None,
		aws_secret_access_key: Optional[str]=None, aws_session_token: Optional[str]=None,
		region_name: Optional[str]=None ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``AwsFileLoader.load`` using a fresh ``AwsFileLoader`` instance.

    Args:
        bucket (str): Value passed to ``AwsFileLoader.load``.
        key (str): Value passed to ``AwsFileLoader.load``.
        aws_access_key_id (Optional[str]): Value passed to ``AwsFileLoader.load``.
        aws_secret_access_key (Optional[str]): Value passed to ``AwsFileLoader.load``.
        aws_session_token (Optional[str]): Value passed to ``AwsFileLoader.load``.
        region_name (Optional[str]): Value passed to ``AwsFileLoader.load``.

    Returns:
        Any: Value returned by ``AwsFileLoader.load``.
    """
    _instance = AwsFileLoader( )
    return _instance.load( bucket=bucket, key=key, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token, region_name=region_name )

def load_google_speech_to_text( project_id: str, file_path: str,
		config: Optional[Dict[str, Any]]=None ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``GoogleSpeechToTextLoader.load`` using a fresh ``GoogleSpeechToTextLoader`` instance.

    Args:
        project_id (str): Value passed to ``GoogleSpeechToTextLoader.load``.
        file_path (str): Value passed to ``GoogleSpeechToTextLoader.load``.
        config (Optional[Dict[str, Any]]): Value passed to ``GoogleSpeechToTextLoader.load``.

    Returns:
        Any: Value returned by ``GoogleSpeechToTextLoader.load``.
    """
    _instance = GoogleSpeechToTextLoader( )
    return _instance.load( project_id=project_id, file_path=file_path, config=config )

def load_google_bucket( project_name: str, bucket: str, prefix: Optional[str]=None,
		continue_on_failure: bool=False ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``GoogleBucketLoader.load`` using a fresh ``GoogleBucketLoader`` instance.

    Args:
        project_name (str): Value passed to ``GoogleBucketLoader.load``.
        bucket (str): Value passed to ``GoogleBucketLoader.load``.
        prefix (Optional[str]): Value passed to ``GoogleBucketLoader.load``.
        continue_on_failure (bool): Value passed to ``GoogleBucketLoader.load``.

    Returns:
        Any: Value returned by ``GoogleBucketLoader.load``.
    """
    _instance = GoogleBucketLoader( )
    return _instance.load( project_name=project_name, bucket=bucket, prefix=prefix, continue_on_failure=continue_on_failure )

def load_aws_bucket( bucket: str, prefix: Optional[str]=None, aws_access_key_id: Optional[str]=None,
		aws_secret_access_key: Optional[str]=None, aws_session_token: Optional[str]=None,
		region_name: Optional[str]=None, endpoint_url: Optional[str]=None ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``AwsBucketLoader.load`` using a fresh ``AwsBucketLoader`` instance.

    Args:
        bucket (str): Value passed to ``AwsBucketLoader.load``.
        prefix (Optional[str]): Value passed to ``AwsBucketLoader.load``.
        aws_access_key_id (Optional[str]): Value passed to ``AwsBucketLoader.load``.
        aws_secret_access_key (Optional[str]): Value passed to ``AwsBucketLoader.load``.
        aws_session_token (Optional[str]): Value passed to ``AwsBucketLoader.load``.
        region_name (Optional[str]): Value passed to ``AwsBucketLoader.load``.
        endpoint_url (Optional[str]): Value passed to ``AwsBucketLoader.load``.

    Returns:
        Any: Value returned by ``AwsBucketLoader.load``.
    """
    _instance = AwsBucketLoader( )
    return _instance.load( bucket=bucket, prefix=prefix, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token, region_name=region_name, endpoint_url=endpoint_url )

# ==========================================================================================
# DEMOGRAPHIC
# ==========================================================================================

def fetch_census_data( mode: str='variables', year: str='2022', dataset: str='acs/acs5',
		fields: str='NAME,B01001_001E', geography_for: str='state:*', geography_in: str='',
		predicates: str='', time: int=20 ) -> Any:
    """Fetch U.S. Census dataset and variable retrieval.

    Purpose:
        Provides direct module-level access to ``CensusData.fetch`` using a fresh ``CensusData`` instance.

    Args:
        mode (str): Value passed to ``CensusData.fetch``.
        year (str): Value passed to ``CensusData.fetch``.
        dataset (str): Value passed to ``CensusData.fetch``.
        fields (str): Value passed to ``CensusData.fetch``.
        geography_for (str): Value passed to ``CensusData.fetch``.
        geography_in (str): Value passed to ``CensusData.fetch``.
        predicates (str): Value passed to ``CensusData.fetch``.
        time (int): Value passed to ``CensusData.fetch``.

    Returns:
        Any: Value returned by ``CensusData.fetch``.
    """
    _instance = CensusData( )
    return _instance.fetch( mode=mode, year=year, dataset=dataset, fields=fields, geography_for=geography_for, geography_in=geography_in, predicates=predicates, time=time )

def fetch_socrata( mode: str='rows', domain: str='data.cdc.gov', dataset_id: str='',
		select: str='', where: str='', order: str='', group: str='', limit: int=25,
		offset: int=0, time: int=20 ) -> Any:
    """Fetch Socrata dataset metadata and row retrieval.

    Purpose:
        Provides direct module-level access to ``Socrata.fetch`` using a fresh ``Socrata`` instance.

    Args:
        mode (str): Value passed to ``Socrata.fetch``.
        domain (str): Value passed to ``Socrata.fetch``.
        dataset_id (str): Value passed to ``Socrata.fetch``.
        select (str): Value passed to ``Socrata.fetch``.
        where (str): Value passed to ``Socrata.fetch``.
        order (str): Value passed to ``Socrata.fetch``.
        group (str): Value passed to ``Socrata.fetch``.
        limit (int): Value passed to ``Socrata.fetch``.
        offset (int): Value passed to ``Socrata.fetch``.
        time (int): Value passed to ``Socrata.fetch``.

    Returns:
        Any: Value returned by ``Socrata.fetch``.
    """
    _instance = Socrata( )
    return _instance.fetch( mode=mode, domain=domain, dataset_id=dataset_id, select=select, where=where, order=order, group=group, limit=limit, offset=offset, time=time )

def fetch_united_nations( mode: str='datasets', query_path: str='', time: int=20 ) -> Any:
    """Fetch United Nations SDMX dataset and query retrieval.

    Purpose:
        Provides direct module-level access to ``UnitedNations.fetch`` using a fresh ``UnitedNations`` instance.

    Args:
        mode (str): Value passed to ``UnitedNations.fetch``.
        query_path (str): Value passed to ``UnitedNations.fetch``.
        time (int): Value passed to ``UnitedNations.fetch``.

    Returns:
        Any: Value returned by ``UnitedNations.fetch``.
    """
    _instance = UnitedNations( )
    return _instance.fetch( mode=mode, query_path=query_path, time=time )

def fetch_world_population( mode: str='catalog', query: str='', asset_path: str='',
		page: int=1, page_size: int=25, time: int=20 ) -> Any:
    """Fetch WorldPop catalog and raster metadata retrieval.

    Purpose:
        Provides direct module-level access to ``WorldPopulation.fetch`` using a fresh ``WorldPopulation`` instance.

    Args:
        mode (str): Value passed to ``WorldPopulation.fetch``.
        query (str): Value passed to ``WorldPopulation.fetch``.
        asset_path (str): Value passed to ``WorldPopulation.fetch``.
        page (int): Value passed to ``WorldPopulation.fetch``.
        page_size (int): Value passed to ``WorldPopulation.fetch``.
        time (int): Value passed to ``WorldPopulation.fetch``.

    Returns:
        Any: Value returned by ``WorldPopulation.fetch``.
    """
    _instance = WorldPopulation( )
    return _instance.fetch( mode=mode, query=query, asset_path=asset_path, page=page, page_size=page_size, time=time )

def load_open_city( city_id: str, dataset_id: str, limit: int=100 ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``OpenCityLoader.load`` using a fresh ``OpenCityLoader`` instance.

    Args:
        city_id (str): Value passed to ``OpenCityLoader.load``.
        dataset_id (str): Value passed to ``OpenCityLoader.load``.
        limit (int): Value passed to ``OpenCityLoader.load``.

    Returns:
        Any: Value returned by ``OpenCityLoader.load``.
    """
    _instance = OpenCityLoader( )
    return _instance.load( city_id=city_id, dataset_id=dataset_id, limit=limit )

# ==========================================================================================
# DOCUMENTS
# ==========================================================================================

def load_text( path: str, encoding: Optional[str]=None ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``TextLoader.load`` using a fresh ``TextLoader`` instance.

    Args:
        path (str): Value passed to ``TextLoader.load``.
        encoding (Optional[str]): Value passed to ``TextLoader.load``.

    Returns:
        Any: Value returned by ``TextLoader.load``.
    """
    _instance = TextLoader( )
    return _instance.load( path=path, encoding=encoding )

def load_csv( path: str, encoding: Optional[str]='utf-8', source_column: Optional[str]=None,
		delimiter: str=',', quotechar: str='"' ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``CsvLoader.load`` using a fresh ``CsvLoader`` instance.

    Args:
        path (str): Value passed to ``CsvLoader.load``.
        encoding (Optional[str]): Value passed to ``CsvLoader.load``.
        source_column (Optional[str]): Value passed to ``CsvLoader.load``.
        delimiter (str): Value passed to ``CsvLoader.load``.
        quotechar (str): Value passed to ``CsvLoader.load``.

    Returns:
        Any: Value returned by ``CsvLoader.load``.
    """
    _instance = CsvLoader( )
    return _instance.load( path=path, encoding=encoding, source_column=source_column, delimiter=delimiter, quotechar=quotechar )

def read_pdf( path: str, mode: str='single' ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``PdfReader.load`` using a fresh ``PdfReader`` instance.

    Args:
        path (str): Value passed to ``PdfReader.load``.
        mode (str): Value passed to ``PdfReader.load``.

    Returns:
        Any: Value returned by ``PdfReader.load``.
    """
    _instance = PdfReader( )
    return _instance.load( path=path, mode=mode )

def load_pdf( path: str, mode: str='single', extract: str='plain', include: bool=False,
		format: str='markdown-img', size: int=1000, overlap: int=150, has_tables: bool=True ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``PdfLoader.load`` using a fresh ``PdfLoader`` instance.

    Args:
        path (str): Value passed to ``PdfLoader.load``.
        mode (str): Value passed to ``PdfLoader.load``.
        extract (str): Value passed to ``PdfLoader.load``.
        include (bool): Value passed to ``PdfLoader.load``.
        format (str): Value passed to ``PdfLoader.load``.
        size (int): Value passed to ``PdfLoader.load``.
        overlap (int): Value passed to ``PdfLoader.load``.
        has_tables (bool): Value passed to ``PdfLoader.load``.

    Returns:
        Any: Value returned by ``PdfLoader.load``.
    """
    _instance = PdfLoader( size=size, overlap=overlap, has_tables=has_tables )
    return _instance.load( path=path, mode=mode, extract=extract, include=include, format=format )

def load_excel( path: str, mode: str='elements', has_headers: bool=True ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``ExcelLoader.load`` using a fresh ``ExcelLoader`` instance.

    Args:
        path (str): Value passed to ``ExcelLoader.load``.
        mode (str): Value passed to ``ExcelLoader.load``.
        has_headers (bool): Value passed to ``ExcelLoader.load``.

    Returns:
        Any: Value returned by ``ExcelLoader.load``.
    """
    _instance = ExcelLoader( )
    return _instance.load( path=path, mode=mode, has_headers=has_headers )

def load_word( path: str ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``WordLoader.load`` using a fresh ``WordLoader`` instance.

    Args:
        path (str): Value passed to ``WordLoader.load``.

    Returns:
        Any: Value returned by ``WordLoader.load``.
    """
    _instance = WordLoader( )
    return _instance.load( path=path )

def load_markdown( path: str ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``MarkdownLoader.load`` using a fresh ``MarkdownLoader`` instance.

    Args:
        path (str): Value passed to ``MarkdownLoader.load``.

    Returns:
        Any: Value returned by ``MarkdownLoader.load``.
    """
    _instance = MarkdownLoader( )
    return _instance.load( path=path )

def load_html( path: str ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``HtmlLoader.load`` using a fresh ``HtmlLoader`` instance.

    Args:
        path (str): Value passed to ``HtmlLoader.load``.

    Returns:
        Any: Value returned by ``HtmlLoader.load``.
    """
    _instance = HtmlLoader( )
    return _instance.load( path=path )

def load_outlook( path: str ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``OutlookLoader.load`` using a fresh ``OutlookLoader`` instance.

    Args:
        path (str): Value passed to ``OutlookLoader.load``.

    Returns:
        Any: Value returned by ``OutlookLoader.load``.
    """
    _instance = OutlookLoader( )
    return _instance.load( path=path )

def load_spfx( library_id: str ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``SpfxLoader.load`` using a fresh ``SpfxLoader`` instance.

    Args:
        library_id (str): Value passed to ``SpfxLoader.load``.

    Returns:
        Any: Value returned by ``SpfxLoader.load``.
    """
    _instance = SpfxLoader( )
    return _instance.load( library_id=library_id )

def load_spfx_folder( library_id: str, folder_id: str ) -> Any:
    """Load provider folder content.

    Purpose:
        Provides direct module-level access to ``SpfxLoader.load_folder`` using a fresh ``SpfxLoader`` instance.

    Args:
        library_id (str): Value passed to ``SpfxLoader.load_folder``.
        folder_id (str): Value passed to ``SpfxLoader.load_folder``.

    Returns:
        Any: Value returned by ``SpfxLoader.load_folder``.
    """
    _instance = SpfxLoader( )
    return _instance.load_folder( library_id=library_id, folder_id=folder_id )

def load_powerpoint( path: str, mode: str='single' ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``PowerPointLoader.load`` using a fresh ``PowerPointLoader`` instance.

    Args:
        path (str): Value passed to ``PowerPointLoader.load``.
        mode (str): Value passed to ``PowerPointLoader.load``.

    Returns:
        Any: Value returned by ``PowerPointLoader.load``.
    """
    _instance = PowerPointLoader( )
    return _instance.load( path=path, mode=mode )

def load_powerpoint_multiple( path: str ) -> Any:
    """Load multiple presentation elements.

    Purpose:
        Provides direct module-level access to ``PowerPointLoader.load_multiple`` using a fresh ``PowerPointLoader`` instance.

    Args:
        path (str): Value passed to ``PowerPointLoader.load_multiple``.

    Returns:
        Any: Value returned by ``PowerPointLoader.load_multiple``.
    """
    _instance = PowerPointLoader( )
    return _instance.load_multiple( path=path )

def load_email( path: str, mode: str='single', attachments: bool=True ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``EmailLoader.load`` using a fresh ``EmailLoader`` instance.

    Args:
        path (str): Value passed to ``EmailLoader.load``.
        mode (str): Value passed to ``EmailLoader.load``.
        attachments (bool): Value passed to ``EmailLoader.load``.

    Returns:
        Any: Value returned by ``EmailLoader.load``.
    """
    _instance = EmailLoader( )
    return _instance.load( path=path, mode=mode, attachments=attachments )

def load_json( filepath: str, is_text: bool=True, is_lines: bool=False ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``JsonLoader.load`` using a fresh ``JsonLoader`` instance.

    Args:
        filepath (str): Value passed to ``JsonLoader.load``.
        is_text (bool): Value passed to ``JsonLoader.load``.
        is_lines (bool): Value passed to ``JsonLoader.load``.

    Returns:
        Any: Value returned by ``JsonLoader.load``.
    """
    _instance = JsonLoader( )
    return _instance.load( filepath=filepath, is_text=is_text, is_lines=is_lines )

def load_xml( filepath: str ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``XmlLoader.load`` using a fresh ``XmlLoader`` instance.

    Args:
        filepath (str): Value passed to ``XmlLoader.load``.

    Returns:
        Any: Value returned by ``XmlLoader.load``.
    """
    _instance = XmlLoader( )
    return _instance.load( filepath=filepath )

def load_xml_tree( filepath: str ) -> Any:
    """Parse an XML element tree.

    Purpose:
        Provides direct module-level access to ``XmlLoader.load_tree`` using a fresh ``XmlLoader`` instance.

    Args:
        filepath (str): Value passed to ``XmlLoader.load_tree``.

    Returns:
        Any: Value returned by ``XmlLoader.load_tree``.
    """
    _instance = XmlLoader( )
    return _instance.load_tree( filepath=filepath )

def load_jupyter_notebook( path: str, include_outputs: bool=False, max_output_length: int=10,
		remove_newline: bool=False, traceback: bool=False ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``JupyterNotebookLoader.load`` using a fresh ``JupyterNotebookLoader`` instance.

    Args:
        path (str): Value passed to ``JupyterNotebookLoader.load``.
        include_outputs (bool): Value passed to ``JupyterNotebookLoader.load``.
        max_output_length (int): Value passed to ``JupyterNotebookLoader.load``.
        remove_newline (bool): Value passed to ``JupyterNotebookLoader.load``.
        traceback (bool): Value passed to ``JupyterNotebookLoader.load``.

    Returns:
        Any: Value returned by ``JupyterNotebookLoader.load``.
    """
    _instance = JupyterNotebookLoader( )
    return _instance.load( path=path, include_outputs=include_outputs, max_output_length=max_output_length, remove_newline=remove_newline, traceback=traceback )

# ==========================================================================================
# ENVIRONMENTAL
# ==========================================================================================

def fetch_google_weather_current( address: str, units_system: str='METRIC', language_code: str='en',
		time: int=10 ) -> Any:
    """Fetch current.

    Purpose:
        Provides direct module-level access to ``GoogleWeather.fetch_current`` using a fresh ``GoogleWeather`` instance.

    Args:
        address (str): Value passed to ``GoogleWeather.fetch_current``.
        units_system (str): Value passed to ``GoogleWeather.fetch_current``.
        language_code (str): Value passed to ``GoogleWeather.fetch_current``.
        time (int): Value passed to ``GoogleWeather.fetch_current``.

    Returns:
        Any: Value returned by ``GoogleWeather.fetch_current``.
    """
    _instance = GoogleWeather( )
    return _instance.fetch_current( address=address, units_system=units_system, language_code=language_code, time=time )

def fetch_google_weather_hourly_forecast( address: str, hours: int=24, units_system: str='METRIC',
		language_code: str='en', time: int=10 ) -> Any:
    """Fetch hourly forecast.

    Purpose:
        Provides direct module-level access to ``GoogleWeather.fetch_hourly_forecast`` using a fresh ``GoogleWeather`` instance.

    Args:
        address (str): Value passed to ``GoogleWeather.fetch_hourly_forecast``.
        hours (int): Value passed to ``GoogleWeather.fetch_hourly_forecast``.
        units_system (str): Value passed to ``GoogleWeather.fetch_hourly_forecast``.
        language_code (str): Value passed to ``GoogleWeather.fetch_hourly_forecast``.
        time (int): Value passed to ``GoogleWeather.fetch_hourly_forecast``.

    Returns:
        Any: Value returned by ``GoogleWeather.fetch_hourly_forecast``.
    """
    _instance = GoogleWeather( )
    return _instance.fetch_hourly_forecast( address=address, hours=hours, units_system=units_system, language_code=language_code, time=time )

def fetch_google_weather_daily_forecast( address: str, days: int=5, units_system: str='METRIC',
		language_code: str='en', time: int=10 ) -> Any:
    """Fetch daily forecast.

    Purpose:
        Provides direct module-level access to ``GoogleWeather.fetch_daily_forecast`` using a fresh ``GoogleWeather`` instance.

    Args:
        address (str): Value passed to ``GoogleWeather.fetch_daily_forecast``.
        days (int): Value passed to ``GoogleWeather.fetch_daily_forecast``.
        units_system (str): Value passed to ``GoogleWeather.fetch_daily_forecast``.
        language_code (str): Value passed to ``GoogleWeather.fetch_daily_forecast``.
        time (int): Value passed to ``GoogleWeather.fetch_daily_forecast``.

    Returns:
        Any: Value returned by ``GoogleWeather.fetch_daily_forecast``.
    """
    _instance = GoogleWeather( )
    return _instance.fetch_daily_forecast( address=address, days=days, units_system=units_system, language_code=language_code, time=time )

def fetch_google_weather_hourly_history( address: str, hours: int=24, units_system: str='METRIC',
		language_code: str='en', time: int=10 ) -> Any:
    """Fetch hourly history.

    Purpose:
        Provides direct module-level access to ``GoogleWeather.fetch_hourly_history`` using a fresh ``GoogleWeather`` instance.

    Args:
        address (str): Value passed to ``GoogleWeather.fetch_hourly_history``.
        hours (int): Value passed to ``GoogleWeather.fetch_hourly_history``.
        units_system (str): Value passed to ``GoogleWeather.fetch_hourly_history``.
        language_code (str): Value passed to ``GoogleWeather.fetch_hourly_history``.
        time (int): Value passed to ``GoogleWeather.fetch_hourly_history``.

    Returns:
        Any: Value returned by ``GoogleWeather.fetch_hourly_history``.
    """
    _instance = GoogleWeather( )
    return _instance.fetch_hourly_history( address=address, hours=hours, units_system=units_system, language_code=language_code, time=time )

def fetch_google_weather_alerts( address: str, language_code: str='en', time: int=10 ) -> Any:
    """Fetch alerts.

    Purpose:
        Provides direct module-level access to ``GoogleWeather.fetch_alerts`` using a fresh ``GoogleWeather`` instance.

    Args:
        address (str): Value passed to ``GoogleWeather.fetch_alerts``.
        language_code (str): Value passed to ``GoogleWeather.fetch_alerts``.
        time (int): Value passed to ``GoogleWeather.fetch_alerts``.

    Returns:
        Any: Value returned by ``GoogleWeather.fetch_alerts``.
    """
    _instance = GoogleWeather( )
    return _instance.fetch_alerts( address=address, language_code=language_code, time=time )

def fetch_earth_observatory( mode: str='events', status: str='open', category: str='', source: str='',
		limit: int=20, days: int=30, start_date: str='', end_date: str='', time: int=20 ) -> Any:
    """Fetch NASA EONET events, categories, sources, and layers.

    Purpose:
        Provides direct module-level access to ``EarthObservatory.fetch`` using a fresh ``EarthObservatory`` instance.

    Args:
        mode (str): Value passed to ``EarthObservatory.fetch``.
        status (str): Value passed to ``EarthObservatory.fetch``.
        category (str): Value passed to ``EarthObservatory.fetch``.
        source (str): Value passed to ``EarthObservatory.fetch``.
        limit (int): Value passed to ``EarthObservatory.fetch``.
        days (int): Value passed to ``EarthObservatory.fetch``.
        start_date (str): Value passed to ``EarthObservatory.fetch``.
        end_date (str): Value passed to ``EarthObservatory.fetch``.
        time (int): Value passed to ``EarthObservatory.fetch``.

    Returns:
        Any: Value returned by ``EarthObservatory.fetch``.
    """
    _instance = EarthObservatory( )
    return _instance.fetch( mode=mode, status=status, category=category, source=source,
	    limit=limit, days=days, start_date=start_date, end_date=end_date, time=time )

def fetch_open_weather( location: str, mode: str='current', zone: str='auto', forecast_days: int=7,
		past_days: int=0, count: int=10 ) -> Any:
    """Fetch Open-Meteo current and forecast weather retrieval.

    Purpose:
        Provides direct module-level access to ``OpenWeather.fetch`` using a fresh ``OpenWeather`` instance.

    Args:
        location (str): Value passed to ``OpenWeather.fetch``.
        mode (str): Value passed to ``OpenWeather.fetch``.
        zone (str): Value passed to ``OpenWeather.fetch``.
        forecast_days (int): Value passed to ``OpenWeather.fetch``.
        past_days (int): Value passed to ``OpenWeather.fetch``.
        count (int): Value passed to ``OpenWeather.fetch``.

    Returns:
        Any: Value returned by ``OpenWeather.fetch``.
    """
    _instance = OpenWeather( )
    return _instance.fetch( location=location, mode=mode, zone=zone, forecast_days=forecast_days,
	    past_days=past_days, count=count )

def fetch_historical_weather( location: str, date: dt.date, zone: str='auto', count: int=10 ) -> Any:
    """Fetch historical weather archive retrieval.

    Purpose:
        Provides direct module-level access to ``HistoricalWeather.fetch`` using a fresh ``HistoricalWeather`` instance.

    Args:
        location (str): Value passed to ``HistoricalWeather.fetch``.
        date (dt.date): Value passed to ``HistoricalWeather.fetch``.
        zone (str): Value passed to ``HistoricalWeather.fetch``.
        count (int): Value passed to ``HistoricalWeather.fetch``.

    Returns:
        Any: Value returned by ``HistoricalWeather.fetch``.
    """
    _instance = HistoricalWeather( )
    return _instance.fetch( location=location, date=date, zone=zone, count=count )

def fetch_usgs_earthquakes( mode: str='feed', feed: str='all_day.geojson', start_date: str='',
		end_date: str='', min_magnitude: float=1.0, max_magnitude: float=10.0,
		limit: int=25, order_by: str='time', event_type: str='earthquake', latitude: float | None=None,
		longitude: float | None=None, max_radius_km: float | None=None, time: int=20 ) -> Any:
    """Fetch USGS earthquake feed and query retrieval.

    Purpose:
        Provides direct module-level access to ``USGSEarthquakes.fetch`` using a fresh ``USGSEarthquakes`` instance.

    Args:
        mode (str): Value passed to ``USGSEarthquakes.fetch``.
        feed (str): Value passed to ``USGSEarthquakes.fetch``.
        start_date (str): Value passed to ``USGSEarthquakes.fetch``.
        end_date (str): Value passed to ``USGSEarthquakes.fetch``.
        min_magnitude (float): Value passed to ``USGSEarthquakes.fetch``.
        max_magnitude (float): Value passed to ``USGSEarthquakes.fetch``.
        limit (int): Value passed to ``USGSEarthquakes.fetch``.
        order_by (str): Value passed to ``USGSEarthquakes.fetch``.
        event_type (str): Value passed to ``USGSEarthquakes.fetch``.
        latitude (float | None): Value passed to ``USGSEarthquakes.fetch``.
        longitude (float | None): Value passed to ``USGSEarthquakes.fetch``.
        max_radius_km (float | None): Value passed to ``USGSEarthquakes.fetch``.
        time (int): Value passed to ``USGSEarthquakes.fetch``.

    Returns:
        Any: Value returned by ``USGSEarthquakes.fetch``.
    """
    _instance = USGSEarthquakes( )
    return _instance.fetch( mode=mode, feed=feed, start_date=start_date, end_date=end_date,
	    min_magnitude=min_magnitude, max_magnitude=max_magnitude, limit=limit, order_by=order_by,
	    event_type=event_type, latitude=latitude, longitude=longitude,
	    max_radius_km=max_radius_km, time=time )

def fetch_usgs_water_data( mode: str='monitoring-locations', monitoring_location_id: str='',
		state_code: str='', county_code: str='', site_type: str='', parameter_code: str='',
		limit: int=25, time: int=20 ) -> Any:
    """Fetch USGS water services records.

    Purpose:
        Provides direct module-level access to ``USGSWaterData.fetch`` using a fresh ``USGSWaterData`` instance.

    Args:
        mode (str): Value passed to ``USGSWaterData.fetch``.
        monitoring_location_id (str): Value passed to ``USGSWaterData.fetch``.
        state_code (str): Value passed to ``USGSWaterData.fetch``.
        county_code (str): Value passed to ``USGSWaterData.fetch``.
        site_type (str): Value passed to ``USGSWaterData.fetch``.
        parameter_code (str): Value passed to ``USGSWaterData.fetch``.
        limit (int): Value passed to ``USGSWaterData.fetch``.
        time (int): Value passed to ``USGSWaterData.fetch``.

    Returns:
        Any: Value returned by ``USGSWaterData.fetch``.
    """
    _instance = USGSWaterData( )
    return _instance.fetch( mode=mode, monitoring_location_id=monitoring_location_id, state_code=state_code, county_code=county_code, site_type=site_type, parameter_code=parameter_code, limit=limit, time=time )

def fetch_air_now( mode: str='current-zip', zip_code: str='', latitude: float | None=None,
		longitude: float | None=None, date: str='', distance: int=25, time: int=20 ) -> Any:
    """Fetch AirNow current and forecast air quality data.

    Purpose:
        Provides direct module-level access to ``AirNow.fetch`` using a fresh ``AirNow`` instance.

    Args:
        mode (str): Value passed to ``AirNow.fetch``.
        zip_code (str): Value passed to ``AirNow.fetch``.
        latitude (float | None): Value passed to ``AirNow.fetch``.
        longitude (float | None): Value passed to ``AirNow.fetch``.
        date (str): Value passed to ``AirNow.fetch``.
        distance (int): Value passed to ``AirNow.fetch``.
        time (int): Value passed to ``AirNow.fetch``.

    Returns:
        Any: Value returned by ``AirNow.fetch``.
    """
    _instance = AirNow( )
    return _instance.fetch( mode=mode, zip_code=zip_code, latitude=latitude, longitude=longitude, date=date, distance=distance, time=time )

def fetch_climate_data( mode: str='datasets', keyword: str='', dataset: str='', start_date: str='',
		end_date: str='', stations: str='', data_types: str='', limit: int=25,
		offset: int=0, time: int=20 ) -> Any:
    """Fetch NOAA climate dataset and data records.

    Purpose:
        Provides direct module-level access to ``ClimateData.fetch`` using a fresh ``ClimateData`` instance.

    Args:
        mode (str): Value passed to ``ClimateData.fetch``.
        keyword (str): Value passed to ``ClimateData.fetch``.
        dataset (str): Value passed to ``ClimateData.fetch``.
        start_date (str): Value passed to ``ClimateData.fetch``.
        end_date (str): Value passed to ``ClimateData.fetch``.
        stations (str): Value passed to ``ClimateData.fetch``.
        data_types (str): Value passed to ``ClimateData.fetch``.
        limit (int): Value passed to ``ClimateData.fetch``.
        offset (int): Value passed to ``ClimateData.fetch``.
        time (int): Value passed to ``ClimateData.fetch``.

    Returns:
        Any: Value returned by ``ClimateData.fetch``.
    """
    _instance = ClimateData( )
    return _instance.fetch( mode=mode, keyword=keyword, dataset=dataset, start_date=start_date, end_date=end_date, stations=stations, data_types=data_types, limit=limit, offset=offset, time=time )

def fetch_eonet( mode: str='events', source: str='', category: str='', status: str='open',
		limit: int=25, days: int=30, start_date: str='', end_date: str='',
		bbox: str='', time: int=20 ) -> Any:
    """Fetch NASA EONET environmental event data.

    Purpose:
        Provides direct module-level access to ``EoNet.fetch`` using a fresh ``EoNet`` instance.

    Args:
        mode (str): Value passed to ``EoNet.fetch``.
        source (str): Value passed to ``EoNet.fetch``.
        category (str): Value passed to ``EoNet.fetch``.
        status (str): Value passed to ``EoNet.fetch``.
        limit (int): Value passed to ``EoNet.fetch``.
        days (int): Value passed to ``EoNet.fetch``.
        start_date (str): Value passed to ``EoNet.fetch``.
        end_date (str): Value passed to ``EoNet.fetch``.
        bbox (str): Value passed to ``EoNet.fetch``.
        time (int): Value passed to ``EoNet.fetch``.

    Returns:
        Any: Value returned by ``EoNet.fetch``.
    """
    _instance = EoNet( )
    return _instance.fetch( mode=mode, source=source, category=category, status=status, limit=limit, days=days, start_date=start_date, end_date=end_date, bbox=bbox, time=time )

def fetch_envirofacts( table_name: str='TRI_FACILITY', state_code: str='',
		facility_name: str='', limit: int=25, time: int=20 ) -> Any:
    """Fetch EPA Envirofacts table and facility records.

    Purpose:
        Provides direct module-level access to ``EnviroFacts.fetch`` using a fresh ``EnviroFacts`` instance.

    Args:
        table_name (str): Value passed to ``EnviroFacts.fetch``.
        state_code (str): Value passed to ``EnviroFacts.fetch``.
        facility_name (str): Value passed to ``EnviroFacts.fetch``.
        limit (int): Value passed to ``EnviroFacts.fetch``.
        time (int): Value passed to ``EnviroFacts.fetch``.

    Returns:
        Any: Value returned by ``EnviroFacts.fetch``.
    """
    _instance = EnviroFacts( )
    return _instance.fetch( table_name=table_name, state_code=state_code, facility_name=facility_name, limit=limit, time=time )

def fetch_tides_and_currents( mode: str='water-level', station_id: str='', begin_date: str='',
		end_date: str='', datum: str='MLLW', units: str='metric', time_zone: str='gmt',
		interval: str='hilo', time: int=20 ) -> Any:
    """Fetch NOAA tides, currents, and station data.

    Purpose:
        Provides direct module-level access to ``TidesAndCurrents.fetch`` using a fresh ``TidesAndCurrents`` instance.

    Args:
        mode (str): Value passed to ``TidesAndCurrents.fetch``.
        station_id (str): Value passed to ``TidesAndCurrents.fetch``.
        begin_date (str): Value passed to ``TidesAndCurrents.fetch``.
        end_date (str): Value passed to ``TidesAndCurrents.fetch``.
        datum (str): Value passed to ``TidesAndCurrents.fetch``.
        units (str): Value passed to ``TidesAndCurrents.fetch``.
        time_zone (str): Value passed to ``TidesAndCurrents.fetch``.
        interval (str): Value passed to ``TidesAndCurrents.fetch``.
        time (int): Value passed to ``TidesAndCurrents.fetch``.

    Returns:
        Any: Value returned by ``TidesAndCurrents.fetch``.
    """
    _instance = TidesAndCurrents( )
    return _instance.fetch( mode=mode, station_id=station_id, begin_date=begin_date, end_date=end_date, datum=datum, units=units, time_zone=time_zone, interval=interval, time=time )

def fetch_uv_index( mode: str='daily-zip', zip_code: str='', city: str='',
		state: str='', time: int=20 ) -> Any:
    """Fetch EPA UV Index current and forecast data.

    Purpose:
        Provides direct module-level access to ``UvIndex.fetch`` using a fresh ``UvIndex`` instance.

    Args:
        mode (str): Value passed to ``UvIndex.fetch``.
        zip_code (str): Value passed to ``UvIndex.fetch``.
        city (str): Value passed to ``UvIndex.fetch``.
        state (str): Value passed to ``UvIndex.fetch``.
        time (int): Value passed to ``UvIndex.fetch``.

    Returns:
        Any: Value returned by ``UvIndex.fetch``.
    """
    _instance = UvIndex( )
    return _instance.fetch( mode=mode, zip_code=zip_code, city=city, state=state, time=time )

def fetch_purple_air( mode: str='sensors', sensor_index: int=None, nwlng: float | None=None,
		nwlat: float | None=None, selng: float | None=None, selat: float | None=None,
		location_type: int=0, max_age: int=0, modified_since: int=0, fields: str='',
		time: int=20 ) -> Any:
    """Fetch PurpleAir sensor and air quality records.

    Purpose:
        Provides direct module-level access to ``PurpleAir.fetch`` using a fresh ``PurpleAir`` instance.

    Args:
        mode (str): Value passed to ``PurpleAir.fetch``.
        sensor_index (int): Value passed to ``PurpleAir.fetch``.
        nwlng (float | None): Value passed to ``PurpleAir.fetch``.
        nwlat (float | None): Value passed to ``PurpleAir.fetch``.
        selng (float | None): Value passed to ``PurpleAir.fetch``.
        selat (float | None): Value passed to ``PurpleAir.fetch``.
        location_type (int): Value passed to ``PurpleAir.fetch``.
        max_age (int): Value passed to ``PurpleAir.fetch``.
        modified_since (int): Value passed to ``PurpleAir.fetch``.
        fields (str): Value passed to ``PurpleAir.fetch``.
        time (int): Value passed to ``PurpleAir.fetch``.

    Returns:
        Any: Value returned by ``PurpleAir.fetch``.
    """
    _instance = PurpleAir( )
    return _instance.fetch( mode=mode, sensor_index=sensor_index, nwlng=nwlng, nwlat=nwlat, selng=selng, selat=selat, location_type=location_type, max_age=max_age, modified_since=modified_since, fields=fields, time=time )

def fetch_open_aq( mode: str='locations', location_id: int=None, parameter_id: int=None,
		country_id: int=None, coordinates: str='', radius: int=25000, providers_id: str='',
		parameters_id: str='', limit: int=25, page: int=1, time: int=20 ) -> Any:
    """Fetch OpenAQ location, measurement, and air-quality records.

    Purpose:
        Provides direct module-level access to ``OpenAQ.fetch`` using a fresh ``OpenAQ`` instance.

    Args:
        mode (str): Value passed to ``OpenAQ.fetch``.
        location_id (int): Value passed to ``OpenAQ.fetch``.
        parameter_id (int): Value passed to ``OpenAQ.fetch``.
        country_id (int): Value passed to ``OpenAQ.fetch``.
        coordinates (str): Value passed to ``OpenAQ.fetch``.
        radius (int): Value passed to ``OpenAQ.fetch``.
        providers_id (str): Value passed to ``OpenAQ.fetch``.
        parameters_id (str): Value passed to ``OpenAQ.fetch``.
        limit (int): Value passed to ``OpenAQ.fetch``.
        page (int): Value passed to ``OpenAQ.fetch``.
        time (int): Value passed to ``OpenAQ.fetch``.

    Returns:
        Any: Value returned by ``OpenAQ.fetch``.
    """
    _instance = OpenAQ( )
    return _instance.fetch( mode=mode, location_id=location_id, parameter_id=parameter_id, country_id=country_id, coordinates=coordinates, radius=radius, providers_id=providers_id, parameters_id=parameters_id, limit=limit, page=page, time=time )

def fetch_firms( mode: str='area', source: str='VIIRS_SNPP_NRT', area_coordinates: str='world',
		day_range: int=1, date: str='', sensor: str='ALL', time: int=20 ) -> Any:
    """Fetch NASA FIRMS active fire data.

    Purpose:
        Provides direct module-level access to ``Firms.fetch`` using a fresh ``Firms`` instance.

    Args:
        mode (str): Value passed to ``Firms.fetch``.
        source (str): Value passed to ``Firms.fetch``.
        area_coordinates (str): Value passed to ``Firms.fetch``.
        day_range (int): Value passed to ``Firms.fetch``.
        date (str): Value passed to ``Firms.fetch``.
        sensor (str): Value passed to ``Firms.fetch``.
        time (int): Value passed to ``Firms.fetch``.

    Returns:
        Any: Value returned by ``Firms.fetch``.
    """
    _instance = Firms( )
    return _instance.fetch( mode=mode, source=source, area_coordinates=area_coordinates,
	    day_range=day_range, date=date, sensor=sensor, time=time )

# ==========================================================================================
# GEOSPATIAL
# ==========================================================================================

def geocode_location( address: str ) -> Any:
    """Geocode location.

    Purpose:
        Provides direct module-level access to ``GoogleMaps.geocode_location`` using a fresh ``GoogleMaps`` instance.

    Args:
        address (str): Value passed to ``GoogleMaps.geocode_location``.

    Returns:
        Any: Value returned by ``GoogleMaps.geocode_location``.
    """
    _instance = GoogleMaps( )
    return _instance.geocode_location( address=address )

def geocode_coordinates( lat: float, long: float ) -> Any:
    """Geocode coordinates.

    Purpose:
        Provides direct module-level access to ``GoogleMaps.geocode_coordinates`` using a fresh ``GoogleMaps`` instance.

    Args:
        lat (float): Value passed to ``GoogleMaps.geocode_coordinates``.
        long (float): Value passed to ``GoogleMaps.geocode_coordinates``.

    Returns:
        Any: Value returned by ``GoogleMaps.geocode_coordinates``.
    """
    _instance = GoogleMaps( )
    return _instance.geocode_coordinates( lat=lat, long=long )

def validate_address( address: List[str] ) -> Any:
    """Validate address.

    Purpose:
        Provides direct module-level access to ``GoogleMaps.validate_address`` using a fresh ``GoogleMaps`` instance.

    Args:
        address (List[str]): Value passed to ``GoogleMaps.validate_address``.

    Returns:
        Any: Value returned by ``GoogleMaps.validate_address``.
    """
    _instance = GoogleMaps( )
    return _instance.validate_address( address=address )

def request_directions( origin: str, destination: str, mode: str='driving' ) -> Any:
    """Request directions.

    Purpose:
        Provides direct module-level access to ``GoogleMaps.request_directions`` using a fresh ``GoogleMaps`` instance.

    Args:
        origin (str): Value passed to ``GoogleMaps.request_directions``.
        destination (str): Value passed to ``GoogleMaps.request_directions``.
        mode (str): Value passed to ``GoogleMaps.request_directions``.

    Returns:
        Any: Value returned by ``GoogleMaps.request_directions``.
    """
    _instance = GoogleMaps( )
    return _instance.request_directions( origin=origin, destination=destination, mode=mode )

def fetch_global_imagery_wms_map( layer: str,
		image_date: str, bbox: Tuple[float, float, float, float],
		width: int=1200, height: int=600, projection: str='epsg4326', quality: str='best',
		image_format: str='image/png', transparent: bool=True, output_dir: str='python-examples', output_name: str='', time: int=20 ) -> Any:
    """Fetch wms map.

    Purpose:
        Provides direct module-level access to ``GlobalImagery.fetch_wms_map`` using a fresh ``GlobalImagery`` instance.

    Args:
        layer (str): Value passed to ``GlobalImagery.fetch_wms_map``.
        image_date (str): Value passed to ``GlobalImagery.fetch_wms_map``.
        bbox (Tuple[float, float, float, float]): Value passed to ``GlobalImagery.fetch_wms_map``.
        width (int): Value passed to ``GlobalImagery.fetch_wms_map``.
        height (int): Value passed to ``GlobalImagery.fetch_wms_map``.
        projection (str): Value passed to ``GlobalImagery.fetch_wms_map``.
        quality (str): Value passed to ``GlobalImagery.fetch_wms_map``.
        image_format (str): Value passed to ``GlobalImagery.fetch_wms_map``.
        transparent (bool): Value passed to ``GlobalImagery.fetch_wms_map``.
        output_dir (str): Value passed to ``GlobalImagery.fetch_wms_map``.
        output_name (str): Value passed to ``GlobalImagery.fetch_wms_map``.
        time (int): Value passed to ``GlobalImagery.fetch_wms_map``.

    Returns:
        Any: Value returned by ``GlobalImagery.fetch_wms_map``.
    """
    _instance = GlobalImagery( )
    return _instance.fetch_wms_map( layer=layer, image_date=image_date, bbox=bbox, width=width, height=height, projection=projection, quality=quality, image_format=image_format, transparent=transparent, output_dir=output_dir, output_name=output_name, time=time )

def fetch_global_imagery_map_services(  ) -> Any:
    """Fetch map services.

    Purpose:
        Provides direct module-level access to ``GlobalImagery.fetch_map_services`` using a fresh ``GlobalImagery`` instance.

    Args:
        None.

    Returns:
        Any: Value returned by ``GlobalImagery.fetch_map_services``.
    """
    _instance = GlobalImagery( )
    return _instance.fetch_map_services(  )

def fetch_global_imagery_mercator_map( ccrs=None ) -> Any:
    """Fetch mercator map.

    Purpose:
        Provides direct module-level access to ``GlobalImagery.fetch_mercator_map`` using a fresh ``GlobalImagery`` instance.

    Args:
        ccrs (Any): Value passed to ``GlobalImagery.fetch_mercator_map``.

    Returns:
        Any: Value returned by ``GlobalImagery.fetch_mercator_map``.
    """
    _instance = GlobalImagery( )
    return _instance.fetch_mercator_map( ccrs=ccrs )

def fetch_google_geocoding( mode: str='forward', query: str='', latitude: float=0.0,
		longitude: float=0.0, place_id: str='', language: str='en', region: str='',
		result_type: str='', location_type: str='', time: int=10, api_key: Optional[str]=None ) -> Any:
    """Fetch Google forward, reverse, and place geocoding.

    Purpose:
        Provides direct module-level access to ``GoogleGeocoding.fetch`` using a fresh ``GoogleGeocoding`` instance.

    Args:
        mode (str): Value passed to ``GoogleGeocoding.fetch``.
        query (str): Value passed to ``GoogleGeocoding.fetch``.
        latitude (float): Value passed to ``GoogleGeocoding.fetch``.
        longitude (float): Value passed to ``GoogleGeocoding.fetch``.
        place_id (str): Value passed to ``GoogleGeocoding.fetch``.
        language (str): Value passed to ``GoogleGeocoding.fetch``.
        region (str): Value passed to ``GoogleGeocoding.fetch``.
        result_type (str): Value passed to ``GoogleGeocoding.fetch``.
        location_type (str): Value passed to ``GoogleGeocoding.fetch``.
        time (int): Value passed to ``GoogleGeocoding.fetch``.
        api_key (Optional[str]): Value passed to ``GoogleGeocoding.fetch``.

    Returns:
        Any: Value returned by ``GoogleGeocoding.fetch``.
    """
    _instance = GoogleGeocoding( )
    return _instance.fetch( mode=mode, query=query, latitude=latitude, longitude=longitude, place_id=place_id, language=language, region=region, result_type=result_type, location_type=location_type, time=time, api_key=api_key )

def fetch_usgs_national_map( mode: str='products', dataset: str='', q: str='', bbox: str='',
		prod_formats: str='', max_items: int=25, offset: int=0, time: int=20 ) -> Any:
    """Fetch USGS National Map datasets and products.

    Purpose:
        Provides direct module-level access to ``USGSTheNationalMap.fetch`` using a fresh ``USGSTheNationalMap`` instance.

    Args:
        mode (str): Value passed to ``USGSTheNationalMap.fetch``.
        dataset (str): Value passed to ``USGSTheNationalMap.fetch``.
        q (str): Value passed to ``USGSTheNationalMap.fetch``.
        bbox (str): Value passed to ``USGSTheNationalMap.fetch``.
        prod_formats (str): Value passed to ``USGSTheNationalMap.fetch``.
        max_items (int): Value passed to ``USGSTheNationalMap.fetch``.
        offset (int): Value passed to ``USGSTheNationalMap.fetch``.
        time (int): Value passed to ``USGSTheNationalMap.fetch``.

    Returns:
        Any: Value returned by ``USGSTheNationalMap.fetch``.
    """
    _instance = USGSTheNationalMap( )
    return _instance.fetch( mode=mode, dataset=dataset, q=q, bbox=bbox, prod_formats=prod_formats, max_items=max_items, offset=offset, time=time )

def fetch_usgs_sciencebase( mode: str='items', q: str='', item_id: str='', max_items: int=25,
		offset: int=0, fields: str='', time: int=20 ) -> Any:
    """Fetch USGS ScienceBase items and catalog records.

    Purpose:
        Provides direct module-level access to ``USGSScienceBase.fetch`` using a fresh ``USGSScienceBase`` instance.

    Args:
        mode (str): Value passed to ``USGSScienceBase.fetch``.
        q (str): Value passed to ``USGSScienceBase.fetch``.
        item_id (str): Value passed to ``USGSScienceBase.fetch``.
        max_items (int): Value passed to ``USGSScienceBase.fetch``.
        offset (int): Value passed to ``USGSScienceBase.fetch``.
        fields (str): Value passed to ``USGSScienceBase.fetch``.
        time (int): Value passed to ``USGSScienceBase.fetch``.

    Returns:
        Any: Value returned by ``USGSScienceBase.fetch``.
    """
    _instance = USGSScienceBase( )
    return _instance.fetch( mode=mode, q=q, item_id=item_id, max_items=max_items, offset=offset, fields=fields, time=time )

# ==========================================================================================
# HEALTH
# ==========================================================================================

def fetch_health_data( mode: str='rows', domain: str='healthdata.gov', dataset_id: str='',
		select: str='', where: str='', order: str='', group: str='', limit: int=25,
		offset: int=0, time: int=20 ) -> Any:
    """Fetch HealthData.gov Socrata metadata and rows.

    Purpose:
        Provides direct module-level access to ``HealthData.fetch`` using a fresh ``HealthData`` instance.

    Args:
        mode (str): Value passed to ``HealthData.fetch``.
        domain (str): Value passed to ``HealthData.fetch``.
        dataset_id (str): Value passed to ``HealthData.fetch``.
        select (str): Value passed to ``HealthData.fetch``.
        where (str): Value passed to ``HealthData.fetch``.
        order (str): Value passed to ``HealthData.fetch``.
        group (str): Value passed to ``HealthData.fetch``.
        limit (int): Value passed to ``HealthData.fetch``.
        offset (int): Value passed to ``HealthData.fetch``.
        time (int): Value passed to ``HealthData.fetch``.

    Returns:
        Any: Value returned by ``HealthData.fetch``.
    """
    _instance = HealthData( )
    return _instance.fetch( mode=mode, domain=domain, dataset_id=dataset_id, select=select, where=where, order=order, group=group, limit=limit, offset=offset, time=time )

def fetch_global_health_data( mode: str='indicator_registry', query_path: str='',
		fmt: str='json', time: int=20 ) -> Any:
    """Fetch WHO global health indicator and Athena data.

    Purpose:
        Provides direct module-level access to ``GlobalHealthData.fetch`` using a fresh ``GlobalHealthData`` instance.

    Args:
        mode (str): Value passed to ``GlobalHealthData.fetch``.
        query_path (str): Value passed to ``GlobalHealthData.fetch``.
        fmt (str): Value passed to ``GlobalHealthData.fetch``.
        time (int): Value passed to ``GlobalHealthData.fetch``.

    Returns:
        Any: Value returned by ``GlobalHealthData.fetch``.
    """
    _instance = GlobalHealthData( )
    return _instance.fetch( mode=mode, query_path=query_path, fmt=fmt, time=time )

def fetch_wonder( mode: str='metadata_template', dataset_id: str='D76',
		request_xml: str='', time: int=20 ) -> Any:
    """Fetch CDC WONDER template and query submission.

    Purpose:
        Provides direct module-level access to ``Wonder.fetch`` using a fresh ``Wonder`` instance.

    Args:
        mode (str): Value passed to ``Wonder.fetch``.
        dataset_id (str): Value passed to ``Wonder.fetch``.
        request_xml (str): Value passed to ``Wonder.fetch``.
        time (int): Value passed to ``Wonder.fetch``.

    Returns:
        Any: Value returned by ``Wonder.fetch``.
    """
    _instance = Wonder( )
    return _instance.fetch( mode=mode, dataset_id=dataset_id, request_xml=request_xml, time=time )

def load_pubmed( query: str, max_docs: int=5 ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``PubMedSearchLoader.load`` using a fresh ``PubMedSearchLoader`` instance.

    Args:
        query (str): Value passed to ``PubMedSearchLoader.load``.
        max_docs (int): Value passed to ``PubMedSearchLoader.load``.

    Returns:
        Any: Value returned by ``PubMedSearchLoader.load``.
    """
    _instance = PubMedSearchLoader( )
    return _instance.load( query=query, max_docs=max_docs )

# ==========================================================================================
# WEB
# ==========================================================================================

def fetch_web_page( url: str, time: int=10 ) -> Any:
    """Fetch HTTP web page retrieval and HTML extraction.

    Purpose:
        Provides direct module-level access to ``WebFetcher.fetch`` using a fresh ``WebFetcher`` instance.

    Args:
        url (str): Value passed to ``WebFetcher.fetch``.
        time (int): Value passed to ``WebFetcher.fetch``.

    Returns:
        Any: Value returned by ``WebFetcher.fetch``.
    """
    _instance = WebFetcher( )
    return _instance.fetch( url=url, time=time )

def convert_html_to_text( html: str ) -> Any:
    """HTML to text.

    Purpose:
        Provides direct module-level access to ``WebFetcher.html_to_text`` using a fresh ``WebFetcher`` instance.

    Args:
        html (str): Value passed to ``WebFetcher.html_to_text``.

    Returns:
        Any: Value returned by ``WebFetcher.html_to_text``.
    """
    _instance = WebFetcher( )
    return _instance.html_to_text( html=html )

def extract_web_title( html: str ) -> Any:
    """Extract title.

    Purpose:
        Provides direct module-level access to ``WebFetcher.extract_title`` using a fresh ``WebFetcher`` instance.

    Args:
        html (str): Value passed to ``WebFetcher.extract_title``.

    Returns:
        Any: Value returned by ``WebFetcher.extract_title``.
    """
    _instance = WebFetcher( )
    return _instance.extract_title( html=html )

def extract_web_links( base_url: str, html: str ) -> Any:
    """Extract links.

    Purpose:
        Provides direct module-level access to ``WebFetcher.extract_links`` using a fresh ``WebFetcher`` instance.

    Args:
        base_url (str): Value passed to ``WebFetcher.extract_links``.
        html (str): Value passed to ``WebFetcher.extract_links``.

    Returns:
        Any: Value returned by ``WebFetcher.extract_links``.
    """
    _instance = WebFetcher( )
    return _instance.extract_links( base_url=base_url, html=html )

def extract_web_structured_data( url: str, html: str,
		selected_methods: Optional[List[str]]=None ) -> Any:
    """Extract structured data.

    Purpose:
        Provides direct module-level access to ``WebFetcher.extract_structured_data`` using a fresh ``WebFetcher`` instance.

    Args:
        url (str): Value passed to ``WebFetcher.extract_structured_data``.
        html (str): Value passed to ``WebFetcher.extract_structured_data``.
        selected_methods (Optional[List[str]]): Value passed to ``WebFetcher.extract_structured_data``.

    Returns:
        Any: Value returned by ``WebFetcher.extract_structured_data``.
    """
    _instance = WebFetcher( )
    return _instance.extract_structured_data( url=url, html=html, selected_methods=selected_methods )

def crawl_web( seed_url: str, include_title: bool=True, include_basic_text: bool=True,
		include_raw_html: bool=False, selected_methods: Optional[List[str]]=None,
		recursive: bool=False, max_depth: int=1, max_pages: int=10, same_domain_only: bool=True,
		request_timeout: int=10, delay_seconds: float=0.25, max_bytes: int=1000000,
		headers: Optional[ Dict[ str, str ] ]=None, use_playwright: bool=False ) -> Any:
    """Crawl.

    Purpose:
        Provides direct module-level access to ``WebCrawler.crawl`` using a fresh ``WebCrawler`` instance.

    Args:
        seed_url (str): Value passed to ``WebCrawler.crawl``.
        include_title (bool): Value passed to ``WebCrawler.crawl``.
        include_basic_text (bool): Value passed to ``WebCrawler.crawl``.
        include_raw_html (bool): Value passed to ``WebCrawler.crawl``.
        selected_methods (Optional[List[str]]): Value passed to ``WebCrawler.crawl``.
        recursive (bool): Value passed to ``WebCrawler.crawl``.
        max_depth (int): Value passed to ``WebCrawler.crawl``.
        max_pages (int): Value passed to ``WebCrawler.crawl``.
        same_domain_only (bool): Value passed to ``WebCrawler.crawl``.
        request_timeout (int): Value passed to ``WebCrawler.crawl``.
        delay_seconds (float): Value passed to ``WebCrawler.crawl``.
        max_bytes (int): Value passed to ``WebCrawler.crawl``.
        headers (Optional[ Dict[ str, str ] ]): Value passed to ``WebCrawler.crawl``.
        use_playwright (bool): Value passed to ``WebCrawler.crawl``.

    Returns:
        Any: Value returned by ``WebCrawler.crawl``.
    """
    _instance = WebCrawler( headers=headers, use_playwright=use_playwright )
    return _instance.crawl( seed_url=seed_url, include_title=include_title, include_basic_text=include_basic_text, include_raw_html=include_raw_html, selected_methods=selected_methods, recursive=recursive, max_depth=max_depth, max_pages=max_pages, same_domain_only=same_domain_only, request_timeout=request_timeout, delay_seconds=delay_seconds, max_bytes=max_bytes )

def scrape_crawler_page( url: str, include_title: bool=True, include_basic_text: bool=True,
		include_raw_html: bool=False, selected_methods: Optional[List[str]]=None,
		request_timeout: int=10, max_bytes: int=1000000,
		headers: Optional[ Dict[ str, str ] ]=None, use_playwright: bool=False ) -> Any:
    """Scrape page.

    Purpose:
        Provides direct module-level access to ``WebCrawler.scrape_page`` using a fresh ``WebCrawler`` instance.

    Args:
        url (str): Value passed to ``WebCrawler.scrape_page``.
        include_title (bool): Value passed to ``WebCrawler.scrape_page``.
        include_basic_text (bool): Value passed to ``WebCrawler.scrape_page``.
        include_raw_html (bool): Value passed to ``WebCrawler.scrape_page``.
        selected_methods (Optional[List[str]]): Value passed to ``WebCrawler.scrape_page``.
        request_timeout (int): Value passed to ``WebCrawler.scrape_page``.
        max_bytes (int): Value passed to ``WebCrawler.scrape_page``.
        headers (Optional[ Dict[ str, str ] ]): Value passed to ``WebCrawler.scrape_page``.
        use_playwright (bool): Value passed to ``WebCrawler.scrape_page``.

    Returns:
        Any: Value returned by ``WebCrawler.scrape_page``.
    """
    _instance = WebCrawler( headers=headers, use_playwright=use_playwright )
    return _instance.scrape_page( url=url, include_title=include_title, include_basic_text=include_basic_text, include_raw_html=include_raw_html, selected_methods=selected_methods, request_timeout=request_timeout, max_bytes=max_bytes )

def render_web_page( url: str, timeout: int=15, headers: Optional[ Dict[ str, str ] ]=None,
		use_playwright: bool=False ) -> Any:
    """Render with playwright.

    Purpose:
        Provides direct module-level access to ``WebCrawler.render_with_playwright`` using a fresh ``WebCrawler`` instance.

    Args:
        url (str): Value passed to ``WebCrawler.render_with_playwright``.
        timeout (int): Value passed to ``WebCrawler.render_with_playwright``.
        headers (Optional[ Dict[ str, str ] ]): Value passed to ``WebCrawler.render_with_playwright``.
        use_playwright (bool): Value passed to ``WebCrawler.render_with_playwright``.

    Returns:
        Any: Value returned by ``WebCrawler.render_with_playwright``.
    """
    _instance = WebCrawler( headers=headers, use_playwright=use_playwright )
    return _instance.render_with_playwright( url=url, timeout=timeout )

def load_web( urls: str | List[str], recursive: bool=False, max_depth: int=2,
		prevent_outside: bool=True, timeout: int=10, ignore: bool=True, progress: bool=True ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``WebLoader.load`` using a fresh ``WebLoader`` instance.

    Args:
        urls (str | List[str]): Value passed to ``WebLoader.load``.
        recursive (bool): Value passed to ``WebLoader.load``.
        max_depth (int): Value passed to ``WebLoader.load``.
        prevent_outside (bool): Value passed to ``WebLoader.load``.
        timeout (int): Value passed to ``WebLoader.load``.
        ignore (bool): Value passed to ``WebLoader.load``.
        progress (bool): Value passed to ``WebLoader.load``.

    Returns:
        Any: Value returned by ``WebLoader.load``.
    """
    _instance = WebLoader( recursive=recursive, max_depth=max_depth, prevent_outside=prevent_outside, timeout=timeout, ignore=ignore, progress=progress )
    return _instance.load( urls=urls )

def load_web_recursive( url: str, depth: int=2, max_time: int=10, ignore: bool=True ) -> Any:
    """Load web documents recursively.

    Purpose:
        Provides direct module-level access to ``WebLoader.load_recursive`` using a fresh ``WebLoader`` instance.

    Args:
        url (str): Value passed to ``WebLoader.load_recursive``.
        depth (int): Value passed to ``WebLoader.load_recursive``.
        max_time (int): Value passed to ``WebLoader.load_recursive``.
        ignore (bool): Value passed to ``WebLoader.load_recursive``.

    Returns:
        Any: Value returned by ``WebLoader.load_recursive``.
    """
    _instance = WebLoader( )
    return _instance.load_recursive( url=url, depth=depth, max_time=max_time, ignore=ignore )

def load_web_pages( urls: List[str], depth: int=2, timeout: int=10, ignore: bool=True,
		progress: bool=True ) -> Any:
    """Load static web pages.

    Purpose:
        Provides direct module-level access to ``WebLoader.load_pages`` using a fresh ``WebLoader`` instance.

    Args:
        urls (List[str]): Value passed to ``WebLoader.load_pages``.
        depth (int): Value passed to ``WebLoader.load_pages``.
        timeout (int): Value passed to ``WebLoader.load_pages``.
        ignore (bool): Value passed to ``WebLoader.load_pages``.
        progress (bool): Value passed to ``WebLoader.load_pages``.

    Returns:
        Any: Value returned by ``WebLoader.load_pages``.
    """
    _instance = WebLoader( )
    return _instance.load_pages( urls=urls, depth=depth, timeout=timeout, ignore=ignore, progress=progress )

def load_github( url: str, repo: str, branch: str, filetype: str='.md' ) -> Any:
    """Load source content.

    Purpose:
        Provides direct module-level access to ``GithubLoader.load`` using a fresh ``GithubLoader`` instance.

    Args:
        url (str): Value passed to ``GithubLoader.load``.
        repo (str): Value passed to ``GithubLoader.load``.
        branch (str): Value passed to ``GithubLoader.load``.
        filetype (str): Value passed to ``GithubLoader.load``.

    Returns:
        Any: Value returned by ``GithubLoader.load``.
    """
    _instance = GithubLoader( )
    return _instance.load( url=url, repo=repo, branch=branch, filetype=filetype )

def scrape_web_page( url: str, time: int=10 ) -> Any:
    """Fetch a web page.

    Purpose:
        Provides direct module-level access to ``WebExtractor.scrape`` using a fresh ``WebExtractor`` instance.

    Args:
        url (str): Value passed to ``WebExtractor.scrape``.
        time (int): Value passed to ``WebExtractor.scrape``.

    Returns:
        Any: Value returned by ``WebExtractor.scrape``.
    """
    _instance = WebExtractor( )
    return _instance.scrape( url=url, time=time )

def scraper_html_to_text( html: str ) -> Any:
    """Convert HTML to plain text.

    Purpose:
        Provides direct module-level access to ``WebExtractor.html_to_text`` using a fresh ``WebExtractor`` instance.

    Args:
        html (str): Value passed to ``WebExtractor.html_to_text``.

    Returns:
        Any: Value returned by ``WebExtractor.html_to_text``.
    """
    _instance = WebExtractor( )
    return _instance.html_to_text( html=html )

def scrape_paragraphs( uri: str ) -> Any:
    """Extract paragraph text.

    Purpose:
        Provides direct module-level access to ``WebExtractor.scrape_paragraphs`` using a fresh ``WebExtractor`` instance.

    Args:
        uri (str): Value passed to ``WebExtractor.scrape_paragraphs``.

    Returns:
        Any: Value returned by ``WebExtractor.scrape_paragraphs``.
    """
    _instance = WebExtractor( )
    return _instance.scrape_paragraphs( uri=uri )

def scrape_lists( uri: str ) -> Any:
    """Extract list item text.

    Purpose:
        Provides direct module-level access to ``WebExtractor.scrape_lists`` using a fresh ``WebExtractor`` instance.

    Args:
        uri (str): Value passed to ``WebExtractor.scrape_lists``.

    Returns:
        Any: Value returned by ``WebExtractor.scrape_lists``.
    """
    _instance = WebExtractor( )
    return _instance.scrape_lists( uri=uri )

def scrape_tables( uri: str ) -> Any:
    """Extract table cell text.

    Purpose:
        Provides direct module-level access to ``WebExtractor.scrape_tables`` using a fresh ``WebExtractor`` instance.

    Args:
        uri (str): Value passed to ``WebExtractor.scrape_tables``.

    Returns:
        Any: Value returned by ``WebExtractor.scrape_tables``.
    """
    _instance = WebExtractor( )
    return _instance.scrape_tables( uri=uri )

def scrape_articles( uri: str ) -> Any:
    """Extract article text.

    Purpose:
        Provides direct module-level access to ``WebExtractor.scrape_articles`` using a fresh ``WebExtractor`` instance.

    Args:
        uri (str): Value passed to ``WebExtractor.scrape_articles``.

    Returns:
        Any: Value returned by ``WebExtractor.scrape_articles``.
    """
    _instance = WebExtractor( )
    return _instance.scrape_articles( uri=uri )

def scrape_headings( uri: str ) -> Any:
    """Extract heading text.

    Purpose:
        Provides direct module-level access to ``WebExtractor.scrape_headings`` using a fresh ``WebExtractor`` instance.

    Args:
        uri (str): Value passed to ``WebExtractor.scrape_headings``.

    Returns:
        Any: Value returned by ``WebExtractor.scrape_headings``.
    """
    _instance = WebExtractor( )
    return _instance.scrape_headings( uri=uri )

def scrape_divisions( uri: str ) -> Any:
    """Extract division text.

    Purpose:
        Provides direct module-level access to ``WebExtractor.scrape_divisions`` using a fresh ``WebExtractor`` instance.

    Args:
        uri (str): Value passed to ``WebExtractor.scrape_divisions``.

    Returns:
        Any: Value returned by ``WebExtractor.scrape_divisions``.
    """
    _instance = WebExtractor( )
    return _instance.scrape_divisions( uri=uri )

def scrape_sections( uri: str ) -> Any:
    """Extract section text.

    Purpose:
        Provides direct module-level access to ``WebExtractor.scrape_sections`` using a fresh ``WebExtractor`` instance.

    Args:
        uri (str): Value passed to ``WebExtractor.scrape_sections``.

    Returns:
        Any: Value returned by ``WebExtractor.scrape_sections``.
    """
    _instance = WebExtractor( )
    return _instance.scrape_sections( uri=uri )

def scrape_blockquotes( uri: str ) -> Any:
    """Extract blockquote text.

    Purpose:
        Provides direct module-level access to ``WebExtractor.scrape_blockquotes`` using a fresh ``WebExtractor`` instance.

    Args:
        uri (str): Value passed to ``WebExtractor.scrape_blockquotes``.

    Returns:
        Any: Value returned by ``WebExtractor.scrape_blockquotes``.
    """
    _instance = WebExtractor( )
    return _instance.scrape_blockquotes( uri=uri )

def scrape_hyperlinks( uri: str ) -> Any:
    """Extract hyperlinks.

    Purpose:
        Provides direct module-level access to ``WebExtractor.scrape_hyperlinks`` using a fresh ``WebExtractor`` instance.

    Args:
        uri (str): Value passed to ``WebExtractor.scrape_hyperlinks``.

    Returns:
        Any: Value returned by ``WebExtractor.scrape_hyperlinks``.
    """
    _instance = WebExtractor( )
    return _instance.scrape_hyperlinks( uri=uri )

def scrape_images( uri: str ) -> Any:
    """Extract image references.

    Purpose:
        Provides direct module-level access to ``WebExtractor.scrape_images`` using a fresh ``WebExtractor`` instance.

    Args:
        uri (str): Value passed to ``WebExtractor.scrape_images``.

    Returns:
        Any: Value returned by ``WebExtractor.scrape_images``.
    """
    _instance = WebExtractor( )
    return _instance.scrape_images( uri=uri )

def encode_image( path: str ) -> str:
    """Encode an image as Base64 text.

    Purpose:
        Provides direct module-level access to ``fetchers.encode_image``.

    Args:
        path (str): Local image path to encode.

    Returns:
        str: Base64-encoded image data.
    """
    return _encode_image( path=path )

# ==========================================================================================
# PUBLIC EXPORTS
# ==========================================================================================

__all__: List[ str ] = [ 'fetch_arxiv', 'fetch_google_drive', 'fetch_wikipedia', 'fetch_news',
		'fetch_google_search', 'fetch_gov_data', 'fetch_congress', 'fetch_internet_archive',
		'fetch_grokipedia', 'load_arxiv', 'load_wikipedia', 'fetch_naval_observatory',
		'fetch_satellite_center', 'fetch_nearby_objects', 'fetch_open_science',
		'fetch_space_weather', 'fetch_astro_catalog', 'fetch_astro_query', 'fetch_star_map',
		'fetch_star_chart', 'fetch_open_sky', 'load_google_drive_file', 'load_google_drive_folder',
		'load_onedrive', 'load_google_cloud_file', 'load_aws_file', 'load_google_speech_to_text',
		'load_google_bucket', 'load_aws_bucket', 'fetch_census_data', 'fetch_socrata',
		'fetch_united_nations', 'fetch_world_population', 'load_open_city', 'load_text', 'load_csv',
		'read_pdf', 'load_pdf', 'load_excel', 'load_word', 'load_markdown', 'load_html',
		'load_outlook', 'load_spfx', 'load_spfx_folder', 'load_powerpoint',
		'load_powerpoint_multiple', 'load_email', 'load_json', 'load_xml', 'load_xml_tree',
		'load_jupyter_notebook', 'fetch_google_weather_current',
		'fetch_google_weather_hourly_forecast', 'fetch_google_weather_daily_forecast',
		'fetch_google_weather_hourly_history', 'fetch_google_weather_alerts',
		'fetch_earth_observatory', 'fetch_open_weather', 'fetch_historical_weather',
		'fetch_usgs_earthquakes', 'fetch_usgs_water_data', 'fetch_air_now', 'fetch_climate_data',
		'fetch_eonet', 'fetch_envirofacts', 'fetch_tides_and_currents', 'fetch_uv_index',
		'fetch_purple_air', 'fetch_open_aq', 'fetch_firms', 'geocode_location',
		'geocode_coordinates', 'validate_address', 'request_directions',
		'fetch_global_imagery_wms_map', 'fetch_global_imagery_map_services',
		'fetch_global_imagery_mercator_map', 'fetch_google_geocoding', 'fetch_usgs_national_map',
		'fetch_usgs_sciencebase', 'fetch_health_data', 'fetch_global_health_data', 'fetch_wonder',
		'load_pubmed', 'fetch_web_page', 'convert_html_to_text', 'extract_web_title',
		'extract_web_links', 'extract_web_structured_data', 'crawl_web', 'scrape_crawler_page',
		'render_web_page', 'load_web', 'load_web_recursive', 'load_web_pages', 'load_github',
		'scrape_web_page', 'scraper_html_to_text', 'scrape_paragraphs', 'scrape_lists',
		'scrape_tables', 'scrape_articles', 'scrape_headings', 'scrape_divisions',
		'scrape_sections', 'scrape_blockquotes', 'scrape_hyperlinks', 'scrape_images',
		'encode_image', ]
