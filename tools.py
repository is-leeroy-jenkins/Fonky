'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                tools.py
      Author:                  Terry D. Eppler
      Created:                 08-23-2026

      Last Modified By:        Terry D. Eppler
      Last Modified On:        08-31-2026
  ******************************************************************************************
  <summary>
    Provides the OpenAI Agents SDK function-tool interface for Fonky.

    Purpose:
        Exposes individual OpenAI Agents SDK function tools over implementation classes in
        ``fetchers.py``, ``loaders.py``, ``scrapers.py``, and ``preprocessors.py``. Each public
        operation creates a fresh implementation instance, invokes the corresponding operation,
        and returns its result.
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from sentence_transformers import SentenceTransformer
import datetime as dt
from agents import function_tool

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

# --------- LOADERS IMPORTS ---------

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

# --------- SCRAPERS IMPORTS ---------

from .scrapers import WebExtractor
from .preprocessors import NltkParser
from .preprocessors import TextParser


@function_tool
def fetch_arxiv( question: str, max_documents: int | None=None, full_documents: bool | None=None,
		include_metadata: bool | None=None ) -> Any:
    """Retrieve ArXiv research documents.

    Purpose:
        Retrieve ArXiv research documents through ArXiv. The query text determines the records or
        documents matched by the provider. Result-count arguments bound the amount of data
        requested. Boolean options control retrieval depth or supplemental content.

    Args:
        question: Search text, lookup value, or provider query submitted by the caller.
        max_documents: Maximum number of documents to retrieve.
        full_documents: Whether to retrieve full document content instead of abbreviated search results.
        include_metadata: Whether provider metadata should be included with retrieved content.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = ArXiv( )
    return _instance.fetch( question=question, max_documents=max_documents,
	    full_documents=full_documents, include_metadata=include_metadata )

@function_tool
def fetch_google_drive( question: str, folder_id: str='root', results: int=10,
		template: str='gdrive-query', mime_type: str | None=None, mode: str='documents' ) -> Any:
    """Retrieve Google Drive documents.

    Purpose:
        Retrieve Google Drive documents through Google Drive. The query text determines the records
        or documents matched by the provider. Result-count arguments bound the amount of data
        requested.

    Args:
        question: Search text, lookup value, or provider query submitted by the caller.
        folder_id: Provider folder identifier that scopes the operation.
        results: Maximum number of search results to request.
        template: Provider query template used to construct the request.
        mime_type: Optional MIME type used to restrict matching files.
        mode: Operation mode used to select the provider or processing workflow.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleDrive( )
    return _instance.fetch( question=question, folder_id=folder_id, results=results,
	    template=template, mime_type=mime_type, mode=mode )

@function_tool
def fetch_wikipedia( question: str, language: str | None=None, max_documents: int | None=None,
		include_metadata: bool | None=None ) -> Any:
    """Retrieve Wikipedia documents.

    Purpose:
        Retrieve Wikipedia documents through Wikipedia. The query text determines the records or
        documents matched by the provider. Result-count arguments bound the amount of data
        requested. Boolean options control retrieval depth or supplemental content.

    Args:
        question: Search text, lookup value, or provider query submitted by the caller.
        language: Language code used for provider results or parsing.
        max_documents: Maximum number of documents to retrieve.
        include_metadata: Whether provider metadata should be included with retrieved content.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = Wikipedia( )
    return _instance.fetch( question=question, language=language, max_documents=max_documents,
	    include_metadata=include_metadata )

@function_tool
def fetch_news( endpoint: str='all', query: str='', language: str='en', categories: str='',
		exclude_categories: str='', locale: str='', domains: str='', exclude_domains: str='',
		source_ids: str='', exclude_source_ids: str='', published_after: str='',
		published_before: str='', published_on: str='', sort: str='published_at',
		limit: int=10, page: int=1, include_similar: bool=True,
		headlines_per_category: int=6, time: int=10, api_key: str | None=None ) -> Any:
    """Retrieve The News API article.

    Purpose:
        Retrieve The News API article through The News API. The query text determines the records or
        documents matched by the provider. Date and time arguments constrain the requested interval
        when supplied. Result-count arguments bound the amount of data requested. Boolean options
        control retrieval depth or supplemental content. When supplied, ``api_key`` overrides the
        configured provider credential for this request.

    Args:
        endpoint: Provider endpoint or endpoint family to request.
        query: Search text, lookup value, or provider query submitted by the caller.
        language: Language code used for provider results or parsing.
        categories: Comma-separated news categories used to include matching articles.
        exclude_categories: Filter value used to exclude categories from provider results.
        locale: Locale filter applied to news results.
        domains: Comma-separated source domains used to include matching news articles.
        exclude_domains: Filter value used to exclude domains from provider results.
        source_ids: Provider identifiers for the selected source.
        exclude_source_ids: Filter value used to exclude source ids from provider results.
        published_after: Earliest publication timestamp accepted by the news query.
        published_before: Latest publication timestamp accepted by the news query.
        published_on: Specific publication date used to restrict news results.
        sort: Provider-supported result ordering expression.
        limit: Maximum number of records or items to return.
        page: One-based result page to request.
        include_similar: Whether to include similar in the result.
        headlines_per_category: Maximum number of headlines returned for each category in headline mode.
        time: Request timeout in seconds.
        api_key: Optional credential override used for the active request.

    Returns:
        Dict[str, Any]: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = TheNews( )
    return _instance.fetch( endpoint=endpoint, query=query, language=language,
	    categories=categories, exclude_categories=exclude_categories, locale=locale,
	    domains=domains, exclude_domains=exclude_domains, source_ids=source_ids,
	    exclude_source_ids=exclude_source_ids, published_after=published_after,
	    published_before=published_before, published_on=published_on, sort=sort, limit=limit,
	    page=page, include_similar=include_similar, headlines_per_category=headlines_per_category,
	    time=time, api_key=api_key )

@function_tool
def fetch_google_search( keywords: str, results: int=10, start: int=1, exact_terms: str='',
		exclude_terms: str='', file_type: str='', date_restrict: str='', gl: str='', lr: str='',
		safe: str='off', search_type: str='', site_search: str='', site_search_filter: str='',
		sort: str='', img_size: str='', img_type: str='', img_color_type: str='',
		img_dominant_color: str='', time: int=10, api_key: str | None=None, cse_id: str | None=None ) -> Any:
    """Retrieve Google Custom Search.

    Purpose:
        Retrieve Google Custom Search through Google Custom Search. The query text determines the
        records or documents matched by the provider. Result-count arguments bound the amount of
        data requested. When supplied, ``api_key`` overrides the configured provider credential for
        this request.

    Args:
        keywords: Search text, lookup value, or provider query submitted by the caller.
        results: Maximum number of search results to request.
        start: Starting result position used for pagination.
        exact_terms: Phrase that must appear exactly in Google Custom Search results.
        exclude_terms: Terms that must not appear in Google Custom Search results.
        file_type: File-extension filter applied to Google Custom Search results.
        date_restrict: Google Custom Search date restriction expression.
        gl: Google country-code boost applied to search results.
        lr: Google language restriction expression.
        safe: Google SafeSearch setting.
        search_type: Google Custom Search result type; use the provider-supported image-search value when
            requesting images.
        site_search: Domain or site used to restrict Google Custom Search results.
        site_search_filter: Whether ``site_search`` is included or excluded by Google Custom Search.
        sort: Provider-supported result ordering expression.
        img_size: Image-size filter used for Google image search.
        img_type: Google image type filter.
        img_color_type: Google image color-type filter.
        img_dominant_color: Dominant-color filter used for Google image search.
        time: Request timeout in seconds.
        api_key: Optional credential override used for the active request.
        cse_id: Google Programmable Search Engine identifier.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleSearch( )
    return _instance.fetch( keywords=keywords, results=results, start=start,
	    exact_terms=exact_terms, exclude_terms=exclude_terms, file_type=file_type,
	    date_restrict=date_restrict, gl=gl, lr=lr, safe=safe, search_type=search_type,
	    site_search=site_search, site_search_filter=site_search_filter, sort=sort,
	    img_size=img_size, img_type=img_type, img_color_type=img_color_type,
	    img_dominant_color=img_dominant_color, time=time, api_key=api_key, cse_id=cse_id )

@function_tool
def fetch_gov_data( mode: str='search', query: str='', page_size: int=10, offset_mark: str='*',
		sort_field: str='score', sort_order: str='DESC', package_id: str='', collection: str='',
		start_date: str='', time: int=20 ) -> Any:
    """Retrieve Data.gov package and collection.

    Purpose:
        Retrieve Data.gov package and collection through Data.gov. Use ``mode`` to select among
        ``collection``, ``package_summary``, ``search``. The query text determines the records or
        documents matched by the provider. Date and time arguments constrain the requested interval
        when supplied. Result-count arguments bound the amount of data requested.

    Args:
        mode: Operation selector. Supported values detected in the implementation include
            ``collection``, ``package_summary``, ``search``.
        query: Search text, lookup value, or provider query submitted by the caller.
        page_size: Maximum number of records requested per page.
        offset_mark: Provider continuation marker used for paginated Data.gov search results.
        sort_field: Provider field used to order search results.
        sort_order: Sort direction applied to the provider search.
        package_id: Provider identifier for the selected package.
        collection: Provider collection identifier used to restrict results.
        start_date: Inclusive start date for the requested time range, in the provider-supported format.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GovData( )
    return _instance.fetch( mode=mode, query=query, page_size=page_size, offset_mark=offset_mark,
	    sort_field=sort_field, sort_order=sort_order, package_id=package_id, collection=collection,
	    start_date=start_date, time=time )


@function_tool
def fetch_congress( mode: str='congresses', congress: int=0, bill_type: str='', bill_number: int=0,
		law_type: str='', law_number: int=0, report_type: str='', report_number: int=0,
		offset: int=0, limit: int=20, sort: str='updateDate+desc', from_date_time: str='',
		to_date_time: str='', conference: bool=False, time: int=20 ) -> Any:
    """Retrieve Congress.gov legislative data.

    Purpose:
        Retrieve Congress.gov legislative data through Congress.gov. Use ``mode`` to select among
        ``bill_detail``, ``bills``, ``congresses``, ``law_detail``, ``laws``, ``report_detail``,
        ``reports``. Date and time arguments constrain the requested interval when supplied. Result-
        count arguments bound the amount of data requested.

    Args:
        mode: Operation selector. Supported values detected in the implementation include
            ``bill_detail``, ``bills``, ``congresses``, ``law_detail``, ``laws``, ``report_detail``,
            ``reports``.
        congress: Congress number used to scope legislative records.
        bill_type: Provider type selector for bill.
        bill_number: Legislative bill number used with the selected Congress and bill type.
        law_type: Provider type selector for law.
        law_number: Public or private law number used with the selected law type.
        report_type: Provider type selector for report.
        report_number: Committee report number used with the selected Congress and report type.
        offset: Zero-based result offset used for pagination.
        limit: Maximum number of records or items to return.
        sort: Provider-supported result ordering expression.
        from_date_time: Earliest provider update timestamp to include.
        to_date_time: Latest provider update timestamp to include.
        conference: Whether to restrict committee reports to conference reports.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = Congress( )
    return _instance.fetch( mode=mode, congress=congress, bill_type=bill_type, bill_number=bill_number, law_type=law_type, law_number=law_number, report_type=report_type, report_number=report_number, offset=offset, limit=limit, sort=sort, from_date_time=from_date_time, to_date_time=to_date_time, conference=conference, time=time )


@function_tool
def fetch_internet_archive( keywords: str, fields: List[str] | None=None, rows: int=10, page: int=1,
		sort: str='downloads desc', media_type: str='', collection: str='', time: int=20 ) -> Any:
    """Retrieve Internet Archive search and metadata.

    Purpose:
        Retrieve Internet Archive search and metadata through Internet Archive. The query text
        determines the records or documents matched by the provider. Result-count arguments bound
        the amount of data requested.

    Args:
        keywords: Search text, lookup value, or provider query submitted by the caller.
        fields: Comma-separated or provider-specific field selection.
        rows: Maximum number of rows to request.
        page: One-based result page to request.
        sort: Provider-supported result ordering expression.
        media_type: Provider type selector for media.
        collection: Provider collection identifier used to restrict results.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = InternetArchive( )
    return _instance.fetch( keywords=keywords, fields=fields, rows=rows, page=page, sort=sort, media_type=media_type, collection=collection, time=time )


@function_tool
def fetch_grokipedia( mode: str='search', query: str='', page: str='', limit: int=12,
		offset: int=0, include_content: bool=True ) -> Any:
    """Retrieve Grokipedia search and page.

    Purpose:
        Retrieve Grokipedia search and page through Grokipedia. The query text determines the
        records or documents matched by the provider. Result-count arguments bound the amount of
        data requested.

    Args:
        mode: Operation mode used to select the provider or processing workflow.
        query: Search text, lookup value, or provider query submitted by the caller.
        page: One-based result page to request.
        limit: Maximum number of records or items to return.
        offset: Zero-based result offset used for pagination.
        include_content: Whether to include content in the result.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = Grokipedia( )
    return _instance.fetch( mode=mode, query=query, page=page, limit=limit, offset=offset, include_content=include_content )


@function_tool
def load_arxiv( question: str ) -> Any:
    """Load ArXiv research documents.

    Purpose:
        Load ArXiv research documents using the ArXiv loader. The query text determines the records
        or documents matched by the provider.

    Args:
        question: Search query or prompt submitted to the backing loader.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = ArXivLoader( )
    return _instance.load( question=question )

@function_tool
def load_wikipedia( question: str ) -> Any:
    """Load Wikipedia articles.

    Purpose:
        Load Wikipedia articles using the Wikipedia loader. The query text determines the records or
        documents matched by the provider.

    Args:
        question: Search query or prompt submitted to the backing loader.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WikiLoader( )
    return _instance.load( question=question )


@function_tool
def fetch_naval_observatory( mode: str='celnav', date_value: str='', time_value: str='',
		latitude: float=0.0, longitude: float=0.0, location_label: str='', time: int=20 ) -> Any:
    """Retrieve U.S. Naval Observatory celestial-navigation data.

    Purpose:
        Retrieve U.S. Naval Observatory celestial-navigation data through U.S. Naval Observatory.
        Coordinate and bounding arguments constrain geographic scope when supported.

    Args:
        mode: Operation mode used to select the provider or processing workflow.
        date_value: Calendar date used by the selected provider operation.
        time_value: Clock time or timestamp used by the selected provider operation.
        latitude: Latitude in decimal degrees.
        longitude: Longitude in decimal degrees.
        location_label: Human-readable label associated with the supplied coordinates.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = NavalObservatory( )
    return _instance.fetch( mode=mode, date_value=date_value, time_value=time_value,
	    latitude=latitude, longitude=longitude, location_label=location_label, time=time )

@function_tool
def fetch_satellite_center( mode: str='observatories', query: str='', start_time: str='',
		end_time: str='', coordinate_systems: str='gse', resolution_factor: int=1, time: int=20 ) -> Any:
    """Retrieve SSC satellite observatory, ground-station, and location data.

    Purpose:
        Retrieve SSC satellite observatory, ground-station, and location data through NASA Satellite
        Situation Center. The query text determines the records or documents matched by the
        provider.

    Args:
        mode: Operation mode used to select the provider or processing workflow.
        query: Search text, lookup value, or provider query submitted by the caller.
        start_time: Beginning timestamp for the requested provider interval.
        end_time: Ending timestamp for the requested provider interval.
        coordinate_systems: Coordinate system or comma-separated coordinate systems requested from the satellite
            service.
        resolution_factor: Sampling resolution factor applied to returned satellite location data.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = SatelliteCenter( )
    return _instance.fetch( mode=mode, query=query, start_time=start_time, end_time=end_time,
	    coordinate_systems=coordinate_systems, resolution_factor=resolution_factor, time=time )

@function_tool
def fetch_nearby_objects( mode: str='close_approaches', start_date: str='', end_date: str='',
		query: str='', query_type: str='sstr', dist_max: str='10LD', body: str='Earth',
		sort: str='date', limit: int=20, dv: float=6.0, dur: int=360, stay: int=8,
		launch: str='2020-2045', h: float=26.0, occ: int=7, include_physical: bool=True,
		include_close_approaches: bool=True, ca_body: str='Earth',
		include_discovery: bool=True, time: int=20 ) -> Any:
    """Retrieve JPL SSD and CNEOS near-Earth object data.

    Purpose:
        Retrieve JPL SSD and CNEOS near-Earth object data through NASA/JPL near-Earth object
        services. The query text determines the records or documents matched by the provider. Date
        and time arguments constrain the requested interval when supplied. Result-count arguments
        bound the amount of data requested.

    Args:
        mode: Operation mode used to select the provider or processing workflow.
        start_date: Inclusive start date for the requested time range, in the provider-supported format.
        end_date: Inclusive end date for the requested time range, in the provider-supported format.
        query: Search text, lookup value, or provider query submitted by the caller.
        query_type: Provider type selector for query.
        dist_max: Maximum close-approach distance expression accepted by the JPL service.
        body: Solar-system body used as the reference object.
        sort: Provider-supported result ordering expression.
        limit: Maximum number of records or items to return.
        dv: Delta-v threshold or mission constraint used by the near-Earth object query.
        dur: Mission duration constraint, in days, used by the near-Earth object query.
        stay: Target stay-duration constraint, in days, used by the near-Earth object query.
        launch: Launch-year or launch-window expression used by the near-Earth object query.
        h: Absolute-magnitude threshold used by the near-Earth object query.
        occ: Opportunity-count or occurrence constraint used by the mission query.
        include_physical: Whether to include physical in the result.
        include_close_approaches: Whether to include close approaches in the result.
        ca_body: Reference body used for close-approach data.
        include_discovery: Whether to include discovery in the result.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = NearbyObjects( )
    return _instance.fetch( mode=mode, start_date=start_date, end_date=end_date, query=query, query_type=query_type, dist_max=dist_max, body=body, sort=sort, limit=limit, dv=dv, dur=dur, stay=stay, launch=launch, h=h, occ=occ, include_physical=include_physical, include_close_approaches=include_close_approaches, ca_body=ca_body, include_discovery=include_discovery, time=time )


@function_tool
def fetch_open_science( mode: str='dataset', query: str='', accession: str='',
		format_value: str='json', time: int=20 ) -> Any:
    """Retrieve NASA Open Science Data Repository resources.

    Purpose:
        Retrieve NASA Open Science Data Repository resources through NASA Open Science Data
        Repository. The query text determines the records or documents matched by the provider.

    Args:
        mode: Operation mode used to select the provider or processing workflow.
        query: Search text, lookup value, or provider query submitted by the caller.
        accession: Dataset accession identifier used to retrieve a specific Open Science resource.
        format_value: Provider output format.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = OpenScience( )
    return _instance.fetch( mode=mode, query=query, accession=accession,
	    format_value=format_value, time=time )


@function_tool
def fetch_space_weather( mode: str='cme', start_date: str='', end_date: str='', time: int=20,
		location: str='ALL', catalog: str='ALL', notification_type: str='all',
		most_accurate_only: bool=True, complete_entry_only: bool=True, speed: int=0,
		half_angle: int=0, keyword: str='', api_key: str | None=None ) -> Any:
    """Retrieve NASA DONKI space weather endpoints.

    Purpose:
        Retrieve NASA DONKI space weather endpoints through NASA DONKI. Date and time arguments
        constrain the requested interval when supplied. When supplied, ``api_key`` overrides the
        configured provider credential for this request.

    Args:
        mode: Operation mode used to select the provider or processing workflow.
        start_date: Inclusive start date for the requested time range, in the provider-supported format.
        end_date: Inclusive end date for the requested time range, in the provider-supported format.
        time: Request timeout in seconds.
        location: Place name, address, or location description resolved by the provider.
        catalog: Provider catalog filter.
        notification_type: Provider type selector for notification.
        most_accurate_only: Whether to restrict results to the provider-designated most accurate analyses.
        complete_entry_only: Whether to restrict results to complete provider entries.
        speed: Minimum or target speed constraint used by the space-weather query.
        half_angle: Half-angle constraint used by the space-weather query.
        keyword: Keyword used to filter provider records.
        api_key: Optional credential override used for the active request.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = SpaceWeather( )
    return _instance.fetch( mode=mode, start_date=start_date, end_date=end_date, time=time, location=location, catalog=catalog, notification_type=notification_type, most_accurate_only=most_accurate_only, complete_entry_only=complete_entry_only, speed=speed, half_angle=half_angle, keyword=keyword, api_key=api_key )


@function_tool
def fetch_astro_catalog( mode: str='object_query', query: str='', quantity: str='',
		attributes: str='', arguments: str='', ra: str='', dec: str='', radius: int=2,
		data_format: str='json', time: int=20 ) -> Any:
    """Retrieve Open Astronomy Catalog queries.

    Purpose:
        Retrieve Open Astronomy Catalog queries through Open Astronomy Catalog. The query text
        determines the records or documents matched by the provider.

    Args:
        mode: Operation mode used to select the provider or processing workflow.
        query: Search text, lookup value, or provider query submitted by the caller.
        quantity: Provider quantity or field requested from the catalog.
        attributes: Provider attributes requested for matching catalog records.
        arguments: Keyword arguments passed to the bound callable.
        ra: Right ascension value.
        dec: Declination value.
        radius: Search radius in the units specified by the operation.
        data_format: Provider output data format.
        time: Request timeout in seconds.

    Returns:
        Any: Provider-specific structured data produced by the retrieval operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = AstroCatalog( )
    return _instance.fetch( mode=mode, query=query, quantity=quantity, attributes=attributes,
	    arguments=arguments, ra=ra, dec=dec, radius=radius, data_format=data_format, time=time )


@function_tool
def fetch_astro_query( mode: str='object_search', query: str='', ra: str='', dec: str='',
		radius: float=0.5, radius_unit: str='deg', row_limit: int=100 ) -> Any:
    """Retrieve Simbad and astronomy object search operations.

    Purpose:
        Retrieve Simbad and astronomy object search operations through Astroquery/SIMBAD. The query
        text determines the records or documents matched by the provider. Result-count arguments
        bound the amount of data requested.

    Args:
        mode: Operation mode used to select the provider or processing workflow.
        query: Search text, lookup value, or provider query submitted by the caller.
        ra: Right ascension value.
        dec: Declination value.
        radius: Search radius in the units specified by the operation.
        radius_unit: Unit applied to the search radius.
        row_limit: Maximum number of rows returned by the astronomy query.

    Returns:
        Dict[str, Any]: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = AstroQuery( )
    return _instance.fetch( mode=mode, query=query, ra=ra, dec=dec, radius=radius,
	    radius_unit=radius_unit, row_limit=row_limit )


@function_tool
def fetch_star_map( mode: str='object_link', query: str='', ra: float=0.0, dec: float=0.0,
		zoom: int=5, image_source: str='DSS2', box_color: str='yellow', show_box: bool=True,
		show_grid: bool=True, show_lines: bool=True, show_boundaries: bool=True,
		show_const_names: bool=False, time: int=20 ) -> Any:
    """Retrieve astronomical object map links and imagery.

    Purpose:
        Retrieve astronomical object map links and imagery through astronomical map service. The
        query text determines the records or documents matched by the provider.

    Args:
        mode: Operation mode used to select the provider or processing workflow.
        query: Search text, lookup value, or provider query submitted by the caller.
        ra: Right ascension value.
        dec: Declination value.
        zoom: Map or chart zoom level.
        image_source: Imagery or survey source used to render the map or chart.
        box_color: Color used to draw the target box on generated map or chart output.
        show_box: Whether to display box in generated output.
        show_grid: Whether to display grid in generated output.
        show_lines: Whether to display lines in generated output.
        show_boundaries: Whether to display boundaries in generated output.
        show_const_names: Whether to display const names in generated output.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = StarMap( )
    return _instance.fetch( mode=mode, query=query, ra=ra, dec=dec, zoom=zoom,
	    image_source=image_source, box_color=box_color, show_box=show_box, show_grid=show_grid,
	    show_lines=show_lines, show_boundaries=show_boundaries,
	    show_const_names=show_const_names, time=time )


@function_tool
def fetch_star_chart( mode: str='object_chart', query: str='', ra: float=0.0,
		dec: float=0.0, zoom: int=5, image_source: str='DSS2', box_color: str='yellow',
		show_box: bool=True, show_grid: bool=True, show_lines: bool=True, show_boundaries: bool=True,
		show_const_names: bool=False, width: int=900, height: int=450,
		magnitude: float=7.5, time: int=20 ) -> Any:
    """Retrieve static star chart and coordinate chart generation.

    Purpose:
        Retrieve static star chart and coordinate chart generation through astronomical chart
        service. The query text determines the records or documents matched by the provider.

    Args:
        mode: Operation mode used to select the provider or processing workflow.
        query: Search text, lookup value, or provider query submitted by the caller.
        ra: Right ascension value.
        dec: Declination value.
        zoom: Map or chart zoom level.
        image_source: Imagery or survey source used to render the map or chart.
        box_color: Color used to draw the target box on generated map or chart output.
        show_box: Whether to display box in generated output.
        show_grid: Whether to display grid in generated output.
        show_lines: Whether to display lines in generated output.
        show_boundaries: Whether to display boundaries in generated output.
        show_const_names: Whether to display const names in generated output.
        width: Output image or chart width in pixels.
        height: Output image or chart height in pixels.
        magnitude: Limiting stellar magnitude used when rendering a chart.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = StarChart( )
    return _instance.fetch( mode=mode, query=query, ra=ra, dec=dec, zoom=zoom,
	    image_source=image_source, box_color=box_color, show_box=show_box, show_grid=show_grid,
	    show_lines=show_lines, show_boundaries=show_boundaries, show_const_names=show_const_names,
	    width=width, height=height, magnitude=magnitude, time=time )


@function_tool
def fetch_open_sky( mode: str='states_bbox', icao24: str='', airport: str='', begin: int | None=None,
		end: int | None=None, time_value: int | None=None, lamin: float | None=None,
		lomin: float | None=None, lamax: float | None=None, lomax: float | None=None,
		extended: bool=False, client_id: str | None=None, client_secret: str | None=None, time: int=20 ) -> Any:
    """Retrieve OpenSky Network aircraft, airport, and state-vector data.

    Purpose:
        Retrieve OpenSky Network aircraft, airport, and state-vector data through OpenSky Network.
        Use ``mode`` to select among ``arrivals_airport``, ``departures_airport``,
        ``flights_aircraft``, ``states_bbox``, ``track_aircraft``.

    Args:
        mode: Operation selector. Supported values detected in the implementation include
            ``arrivals_airport``, ``departures_airport``, ``flights_aircraft``, ``states_bbox``,
            ``track_aircraft``.
        icao24: 24-bit ICAO aircraft transponder address.
        airport: ICAO airport identifier used to query arrivals or departures.
        begin: Beginning Unix timestamp for the requested aviation interval.
        end: Ending Unix timestamp for the requested aviation interval.
        time_value: Clock time or timestamp used by the selected provider operation.
        lamin: Bounding-box minimum latitude in decimal degrees.
        lomin: Bounding-box minimum longitude in decimal degrees.
        lamax: Bounding-box maximum latitude in decimal degrees.
        lomax: Bounding-box maximum longitude in decimal degrees.
        extended: Whether extended OpenSky state-vector fields should be requested.
        client_id: Optional credential override used for the active request.
        client_secret: Optional credential override used for the active request.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = OpenSky( )
    return _instance.fetch( mode=mode, icao24=icao24, airport=airport, begin=begin, end=end, time_value=time_value, lamin=lamin, lomin=lomin, lamax=lamax, lomax=lomax, extended=extended, client_id=client_id, client_secret=client_secret, time=time )



@function_tool
def load_google_drive_file( file_id: str, recursive: bool=False ) -> Any:
    """Load a Google Drive file.

    Purpose:
        Load a Google Drive file using the Google Drive loader. Boolean options control retrieval
        depth or supplemental content.

    Args:
        file_id: Provider file identifier used to load a single file.
        recursive: Whether the loader should traverse nested provider or URL resources.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleDriveLoader( )
    return _instance.load_file( file_id=file_id, recursive=recursive )


@function_tool
def load_google_drive_folder( folder_id: str, recursive: bool=False ) -> Any:
    """Load documents from a Google Drive folder.

    Purpose:
        Load documents from a Google Drive folder using the Google Drive loader. Boolean options
        control retrieval depth or supplemental content.

    Args:
        folder_id: Provider folder identifier used to load folder contents.
        recursive: Whether the loader should traverse nested provider or URL resources.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleDriveLoader( )
    return _instance.load_folder( folder_id=folder_id, recursive=recursive )


@function_tool
def load_onedrive( drive_id: str, folder_path: Optional[str]=None,
		object_ids: Optional[List[str]]=None, auth_with_token: bool=True ) -> Any:
    """Load documents from OneDrive.

    Purpose:
        Load documents from OneDrive using the OneDrive loader.

    Args:
        drive_id: OneDrive drive identifier.
        folder_path: Optional folder path within the selected drive.
        object_ids: Optional provider object identifiers to load.
        auth_with_token: Whether token-based authentication should be used.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = OneDriveDocLoader( )
    return _instance.load( drive_id=drive_id, folder_path=folder_path, object_ids=object_ids, auth_with_token=auth_with_token )


@function_tool
def load_google_cloud_file( project_name: str, bucket: str, blob: str ) -> Any:
    """Load a Google Cloud Storage object.

    Purpose:
        Load a Google Cloud Storage object using the Google Cloud Storage loader.

    Args:
        project_name: Google Cloud project name used by the storage loader.
        bucket: Storage bucket name.
        blob: Cloud storage object name.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleCloudFileLoader( )
    return _instance.load( project_name=project_name, bucket=bucket, blob=blob )


@function_tool
def load_aws_file( bucket: str, key: str, aws_access_key_id: Optional[str]=None,
		aws_secret_access_key: Optional[str]=None, aws_session_token: Optional[str]=None,
		region_name: Optional[str]=None ) -> Any:
    """Load an Amazon S3 object.

    Purpose:
        Load an Amazon S3 object using the Amazon S3 file loader.

    Args:
        bucket: Storage bucket name.
        key: Amazon S3 object key.
        aws_access_key_id: Provider identifier for the selected aws access key.
        aws_secret_access_key: AWS credential or configuration value for secret access key.
        aws_session_token: AWS credential or configuration value for session token.
        region_name: Cloud region name used to configure the storage client.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = AwsFileLoader( )
    return _instance.load( bucket=bucket, key=key, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token, region_name=region_name )


@function_tool
def load_google_speech_to_text( project_id: str, file_path: str,
		config: Optional[Dict[str, Any]]=None ) -> Any:
    """Transcribe audio with Google Speech-to-Text.

    Purpose:
        Transcribe audio with Google Speech-to-Text using the Google Speech-to-Text loader.

    Args:
        project_id: Google Cloud project identifier used by the speech loader.
        file_path: Local filesystem path to the source file.
        config: Optional provider configuration mapping.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleSpeechToTextLoader( )
    return _instance.load( project_id=project_id, file_path=file_path, config=config )


@function_tool
def load_google_bucket( project_name: str, bucket: str, prefix: Optional[str]=None,
		continue_on_failure: bool=False ) -> Any:
    """Load documents from a Google Cloud Storage bucket.

    Purpose:
        Load documents from a Google Cloud Storage bucket using the Google Cloud Storage bucket
        loader.

    Args:
        project_name: Google Cloud project name used by the storage loader.
        bucket: Storage bucket name.
        prefix: Optional object-name prefix used to restrict cloud storage results.
        continue_on_failure: Whether loading should continue when an individual object fails.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleBucketLoader( )
    return _instance.load( project_name=project_name, bucket=bucket, prefix=prefix, continue_on_failure=continue_on_failure )


@function_tool
def load_aws_bucket( bucket: str, prefix: Optional[str]=None, aws_access_key_id: Optional[str]=None,
		aws_secret_access_key: Optional[str]=None, aws_session_token: Optional[str]=None,
		region_name: Optional[str]=None, endpoint_url: Optional[str]=None ) -> Any:
    """Load documents from an Amazon S3 bucket.

    Purpose:
        Load documents from an Amazon S3 bucket using the Amazon S3 bucket loader.

    Args:
        bucket: Storage bucket name.
        prefix: Optional object-name prefix used to restrict cloud storage results.
        aws_access_key_id: Provider identifier for the selected aws access key.
        aws_secret_access_key: AWS credential or configuration value for secret access key.
        aws_session_token: AWS credential or configuration value for session token.
        region_name: Cloud region name used to configure the storage client.
        endpoint_url: Optional alternate service endpoint URL.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = AwsBucketLoader( )
    return _instance.load( bucket=bucket, prefix=prefix, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token, region_name=region_name, endpoint_url=endpoint_url )



@function_tool
def fetch_census_data( mode: str='variables', year: str='2022', dataset: str='acs/acs5',
		fields: str='NAME,B01001_001E', geography_for: str='state:*', geography_in: str='',
		predicates: str='', time: int=20 ) -> Any:
    """Retrieve U.S. Census dataset and variable.

    Purpose:
        Retrieve U.S. Census dataset and variable through U.S. Census API. Use ``mode`` to select
        among ``data``, ``variables``.

    Args:
        mode: Operation selector. Supported values detected in the implementation include ``data``,
            ``variables``.
        year: Dataset or observation year requested from the provider.
        dataset: Provider dataset name or identifier.
        fields: Comma-separated or provider-specific field selection.
        geography_for: Census ``for`` geography clause defining the requested geography.
        geography_in: Optional Census ``in`` geography clause constraining the request.
        predicates: Additional Census query predicates appended to the request.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = CensusData( )
    return _instance.fetch( mode=mode, year=year, dataset=dataset, fields=fields, geography_for=geography_for, geography_in=geography_in, predicates=predicates, time=time )


@function_tool
def fetch_socrata( mode: str='rows', domain: str='data.cdc.gov', dataset_id: str='',
		select: str='', where: str='', order: str='', group: str='', limit: int=25,
		offset: int=0, time: int=20 ) -> Any:
    """Retrieve Socrata dataset metadata and row.

    Purpose:
        Retrieve Socrata dataset metadata and row through Socrata. Use ``mode`` to select among
        ``metadata``, ``rows``. Result-count arguments bound the amount of data requested.

    Args:
        mode: Operation selector. Supported values detected in the implementation include
            ``metadata``, ``rows``.
        domain: Provider domain or host containing the requested dataset.
        dataset_id: Provider dataset identifier.
        select: Socrata ``$select`` expression defining returned columns or calculations.
        where: Socrata ``$where`` filter expression.
        order: Provider-supported result ordering expression.
        group: Socrata ``$group`` expression used to aggregate rows.
        limit: Maximum number of records or items to return.
        offset: Zero-based result offset used for pagination.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = Socrata( )
    return _instance.fetch( mode=mode, domain=domain, dataset_id=dataset_id, select=select,
	    where=where, order=order, group=group, limit=limit, offset=offset, time=time )


@function_tool
def fetch_united_nations( mode: str='datasets', query_path: str='', time: int=20 ) -> Any:
    """Retrieve United Nations SDMX dataset and query.

    Purpose:
        Retrieve United Nations SDMX dataset and query through United Nations SDMX service. Use
        ``mode`` to select among ``datasets``, ``sdmx_query``.

    Args:
        mode: Operation selector. Supported values detected in the implementation include
            ``datasets``, ``sdmx_query``.
        query_path: Path identifying the query resource.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = UnitedNations( )
    return _instance.fetch( mode=mode, query_path=query_path, time=time )


@function_tool
def fetch_world_population( mode: str='catalog', query: str='', asset_path: str='',
		page: int=1, page_size: int=25, time: int=20 ) -> Any:
    """Retrieve WorldPop catalog and raster metadata.

    Purpose:
        Retrieve WorldPop catalog and raster metadata through WorldPop. Use ``mode`` to select among
        ``catalog``, ``raster_metadata``, ``search``. The query text determines the records or
        documents matched by the provider. Result-count arguments bound the amount of data
        requested.

    Args:
        mode: Operation selector. Supported values detected in the implementation include ``catalog``,
            ``raster_metadata``, ``search``.
        query: Search text, lookup value, or provider query submitted by the caller.
        asset_path: Path identifying the asset resource.
        page: One-based result page to request.
        page_size: Maximum number of records requested per page.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WorldPopulation( )
    return _instance.fetch( mode=mode, query=query, asset_path=asset_path, page=page,
	    page_size=page_size, time=time )


@function_tool
def load_open_city( city_id: str, dataset_id: str, limit: int=100 ) -> Any:
    """Load an Open City dataset.

    Purpose:
        Load an Open City dataset using the Open City Data loader. Result-count arguments bound the
        amount of data requested.

    Args:
        city_id: Provider identifier for the selected city.
        dataset_id: Provider dataset identifier.
        limit: Maximum number of records requested from the backing source.

    Returns:
        List[Document]: LangChain documents loaded from the requested source.

    Raises:
        ValueError: Raised when a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = OpenCityLoader( )
    return _instance.load( city_id=city_id, dataset_id=dataset_id, limit=limit )



@function_tool
def load_text( path: str, encoding: Optional[str]=None ) -> Any:
    """Load a plain-text file.

    Purpose:
        Load a plain-text file using the text loader.

    Args:
        path: Local file path used by the loader.
        encoding: Optional file encoding passed to the backing loader.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = TextLoader( )
    return _instance.load( path=path, encoding=encoding )


@function_tool
def load_csv( path: str, encoding: Optional[str]='utf-8', source_column: Optional[str]=None,
		delimiter: str=',', quotechar: str='"' ) -> Any:
    """Load a CSV file.

    Purpose:
        Load a CSV file using the CSV loader.

    Args:
        path: Local file path used by the loader.
        encoding: Optional file encoding passed to the backing loader.
        source_column: Optional CSV column whose value is stored as the document source.
        delimiter: Field delimiter used to parse delimited text.
        quotechar: Quote character used to parse delimited text.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = CsvLoader( )
    return _instance.load( path=path, encoding=encoding, source_column=source_column, delimiter=delimiter, quotechar=quotechar )


@function_tool
def read_pdf( path: str, mode: str='single' ) -> Any:
    """Read a PDF file.

    Purpose:
        Read a PDF file using the PDF reader.

    Args:
        path: Local file path used by the loader.
        mode: Operation mode used to select the provider or processing workflow.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = PdfReader( )
    return _instance.load( path=path, mode=mode )

@function_tool
def load_pdf( path: str, mode: str='single', extract: str='plain', include: bool=False,
		format: str='markdown-img', size: int=1000, overlap: int=150, has_tables: bool=True ) -> Any:
    """Load and extract a PDF file.

    Purpose:
        Load and extract a PDF file using the PDF loader.

    Args:
        path: Local file path used by the loader.
        mode: Operation mode used to select the provider or processing workflow.
        extract: PDF text-extraction strategy used by the underlying parser.
        include: Whether optional embedded content should be included.
        format: Output or embedded-image format requested from the loader.
        size: Maximum chunk size used for document splitting.
        overlap: Number of characters or tokens repeated between adjacent chunks.
        has_tables: Whether table-aware parsing or extraction should be enabled.

    Returns:
        List[Document]: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = PdfLoader( size=size, overlap=overlap, has_tables=has_tables )
    return _instance.load( path=path, mode=mode, extract=extract, include=include, format=format )


@function_tool
def load_excel( path: str, mode: str='elements', has_headers: bool=True ) -> Any:
    """Load an Excel workbook.

    Purpose:
        Load an Excel workbook using the Excel loader.

    Args:
        path: Local file path used by the loader.
        mode: Operation mode used to select the provider or processing workflow.
        has_headers: Whether the first spreadsheet row should be treated as column headers.

    Returns:
        List[Document]: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = ExcelLoader( )
    return _instance.load( path=path, mode=mode, has_headers=has_headers )


@function_tool
def load_word( path: str ) -> Any:
    """Load a Word document.

    Purpose:
        Load a Word document using the Word loader.

    Args:
        path: Local file path used by the loader.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WordLoader( )
    return _instance.load( path=path )


@function_tool
def load_markdown( path: str ) -> Any:
    """Load a Markdown document.

    Purpose:
        Load a Markdown document using the Markdown loader.

    Args:
        path: Local file path used by the loader.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = MarkdownLoader( )
    return _instance.load( path=path )


@function_tool
def load_html( path: str ) -> Any:
    """Load an HTML document.

    Purpose:
        Load an HTML document using the HTML loader.

    Args:
        path: Local file path used by the loader.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = HtmlLoader( )
    return _instance.load( path=path )


@function_tool
def load_outlook( path: str ) -> Any:
    """Load an Outlook message.

    Purpose:
        Load an Outlook message using the Outlook message loader.

    Args:
        path: Local file path used by the loader.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = OutlookLoader( )
    return _instance.load( path=path )


@function_tool
def load_spfx( library_id: str ) -> Any:
    """Load a SharePoint document library.

    Purpose:
        Load a SharePoint document library using the SharePoint loader.

    Args:
        library_id: SharePoint document-library identifier.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = SpfxLoader( )
    return _instance.load( library_id=library_id )


@function_tool
def load_spfx_folder( library_id: str, folder_id: str ) -> Any:
    """Load a SharePoint folder.

    Purpose:
        Load a SharePoint folder using the SharePoint loader.

    Args:
        library_id: SharePoint document-library identifier.
        folder_id: Provider folder identifier used to load folder contents.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = SpfxLoader( )
    return _instance.load_folder( library_id=library_id, folder_id=folder_id )


@function_tool
def load_powerpoint( path: str, mode: str='single' ) -> Any:
    """Load a PowerPoint presentation.

    Purpose:
        Load a PowerPoint presentation using the PowerPoint loader.

    Args:
        path: Local file path used by the loader.
        mode: Operation mode used to select the provider or processing workflow.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = PowerPointLoader( )
    return _instance.load( path=path, mode=mode )


@function_tool
def load_powerpoint_multiple( path: str ) -> Any:
    """Load multiple PowerPoint presentation elements.

    Purpose:
        Load multiple PowerPoint presentation elements using the PowerPoint loader.

    Args:
        path: Local file path used by the loader.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = PowerPointLoader( )
    return _instance.load_multiple( path=path )


@function_tool
def load_email( path: str, mode: str='single', attachments: bool=True ) -> Any:
    """Load an email message.

    Purpose:
        Load an email message using the email loader.

    Args:
        path: Local file path used by the loader.
        mode: Operation mode used to select the provider or processing workflow.
        attachments: Whether email attachments should be included when supported.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = EmailLoader( )
    return _instance.load( path=path, mode=mode, attachments=attachments )


@function_tool
def load_json( filepath: str, is_text: bool=True, is_lines: bool=False ) -> Any:
    """Load JSON content.

    Purpose:
        Load JSON content using the JSON loader.

    Args:
        filepath: Local file path used by the loader.
        is_text: Whether JSON values should be treated as text content.
        is_lines: Whether the JSON source uses JSON Lines format.

    Returns:
        List[Document]: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = JsonLoader( )
    return _instance.load( filepath=filepath, is_text=is_text, is_lines=is_lines )


@function_tool
def load_xml( filepath: str ) -> Any:
    """Load an XML document.

    Purpose:
        Load an XML document using the XML loader.

    Args:
        filepath: Local file path used by the loader.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = XmlLoader( )
    return _instance.load( filepath=filepath )


@function_tool
def load_xml_tree( filepath: str ) -> Any:
    """Parse an XML document tree.

    Purpose:
        Parse an XML document tree using the XML loader.

    Args:
        filepath: Local file path used by the loader.

    Returns:
        etree._ElementTree | None: XML elements matching the requested XPath expression.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = XmlLoader( )
    return _instance.load_tree( filepath=filepath )


@function_tool
def load_jupyter_notebook( path: str, include_outputs: bool=False, max_output_length: int=10,
		remove_newline: bool=False, traceback: bool=False ) -> Any:
    """Load a Jupyter notebook.

    Purpose:
        Load a Jupyter notebook using the Jupyter notebook loader. Boolean options control retrieval
        depth or supplemental content.

    Args:
        path: Local file path used by the loader.
        include_outputs: Whether notebook cell outputs should be included.
        max_output_length: Maximum notebook cell output length to retain.
        remove_newline: Whether newline characters should be removed from notebook output.
        traceback: Whether notebook traceback output should be included.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = JupyterNotebookLoader( )
    return _instance.load( path=path, include_outputs=include_outputs, max_output_length=max_output_length, remove_newline=remove_newline, traceback=traceback )


@function_tool
def fetch_google_weather_current( address: str, units_system: str='METRIC', language_code: str='en',
		time: int=10 ) -> Any:
    """Retrieve google weather current data.

    Purpose:
        Retrieve google weather current data through Google Weather.

    Args:
        address: Street address or place description used for geocoding, validation, or routing.
        units_system: Measurement unit system requested from the provider.
        language_code: BCP-47-style language code used for provider results.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleWeather( )
    return _instance.fetch_current( address=address, units_system=units_system, language_code=language_code, time=time )


@function_tool
def fetch_google_weather_hourly_forecast( address: str, hours: int=24, units_system: str='METRIC',
		language_code: str='en', time: int=10 ) -> Any:
    """Retrieve hourly forecast.

    Purpose:
        Retrieve hourly forecast through Google Weather.

    Args:
        address: Street address or place description used for geocoding, validation, or routing.
        hours: Number of hourly observations or forecast periods to request.
        units_system: Measurement unit system requested from the provider.
        language_code: BCP-47-style language code used for provider results.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleWeather( )
    return _instance.fetch_hourly_forecast( address=address, hours=hours, units_system=units_system, language_code=language_code, time=time )


@function_tool
def fetch_google_weather_daily_forecast( address: str, days: int=5, units_system: str='METRIC',
		language_code: str='en', time: int=10 ) -> Any:
    """Retrieve daily forecast.

    Purpose:
        Retrieve daily forecast through Google Weather.

    Args:
        address: Street address or place description used for geocoding, validation, or routing.
        days: Number of calendar days included in the requested interval.
        units_system: Measurement unit system requested from the provider.
        language_code: BCP-47-style language code used for provider results.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleWeather( )
    return _instance.fetch_daily_forecast( address=address, days=days, units_system=units_system, language_code=language_code, time=time )


@function_tool
def fetch_google_weather_hourly_history( address: str, hours: int=24, units_system: str='METRIC',
		language_code: str='en', time: int=10 ) -> Any:
    """Retrieve hourly history.

    Purpose:
        Retrieve hourly history through Google Weather.

    Args:
        address: Street address or place description used for geocoding, validation, or routing.
        hours: Number of hourly observations or forecast periods to request.
        units_system: Measurement unit system requested from the provider.
        language_code: BCP-47-style language code used for provider results.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleWeather( )
    return _instance.fetch_hourly_history( address=address, hours=hours, units_system=units_system, language_code=language_code, time=time )


@function_tool
def fetch_google_weather_alerts( address: str, language_code: str='en', time: int=10 ) -> Any:
    """Retrieve google weather alerts data.

    Purpose:
        Retrieve google weather alerts data through Google Weather.

    Args:
        address: Street address or place description used for geocoding, validation, or routing.
        language_code: BCP-47-style language code used for provider results.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleWeather( )
    return _instance.fetch_alerts( address=address, language_code=language_code, time=time )


@function_tool
def fetch_earth_observatory( mode: str='events', status: str='open', category: str='', source: str='',
		limit: int=20, days: int=30, start_date: str='', end_date: str='', time: int=20 ) -> Any:
    """Retrieve NASA EONET events, categories, sources, and layers.

    Purpose:
        Retrieve NASA EONET events, categories, sources, and layers through NASA EONET. Date and
        time arguments constrain the requested interval when supplied. Result-count arguments bound
        the amount of data requested.

    Args:
        mode: Operation mode used to select the provider or processing workflow.
        status: Provider status filter applied to returned records.
        category: Optional logical category retained in tool metadata.
        source: Provider source identifier used to restrict or classify results.
        limit: Maximum number of records or items to return.
        days: Number of calendar days included in the requested interval.
        start_date: Inclusive start date for the requested time range, in the provider-supported format.
        end_date: Inclusive end date for the requested time range, in the provider-supported format.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any]: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = EarthObservatory( )
    return _instance.fetch( mode=mode, status=status, category=category, source=source,
	    limit=limit, days=days, start_date=start_date, end_date=end_date, time=time )


@function_tool
def fetch_open_weather( location: str, mode: str='current', zone: str='auto', forecast_days: int=7,
		past_days: int=0, count: int=10 ) -> Any:
    """Retrieve Open-Meteo current and forecast weather.

    Purpose:
        Retrieve Open-Meteo current and forecast weather through Open-Meteo.

    Args:
        location: Place name, address, or location description resolved by the provider.
        mode: Operation mode used to select the provider or processing workflow.
        zone: Timezone identifier or automatic timezone-selection mode.
        forecast_days: Number of forecast days to request.
        past_days: Number of historical days to include with the weather request.
        count: Maximum number of matching locations or records to consider.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = OpenWeather( )
    return _instance.fetch( location=location, mode=mode, zone=zone, forecast_days=forecast_days,
	    past_days=past_days, count=count )


@function_tool
def fetch_historical_weather( location: str, date: dt.date, zone: str='auto', count: int=10 ) -> Any:
    """Retrieve historical weather archive.

    Purpose:
        Retrieve historical weather archive through Open-Meteo Archive.

    Args:
        location: Place name, address, or location description resolved by the provider.
        date: Date used by the provider or processing operation.
        zone: Timezone identifier or automatic timezone-selection mode.
        count: Maximum number of matching locations or records to consider.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = HistoricalWeather( )
    return _instance.fetch( location=location, date=date, zone=zone, count=count )


@function_tool
def fetch_usgs_earthquakes( mode: str='feed', feed: str='all_day.geojson', start_date: str='',
		end_date: str='', min_magnitude: float=1.0, max_magnitude: float=10.0,
		limit: int=25, order_by: str='time', event_type: str='earthquake', latitude: float | None=None,
		longitude: float | None=None, max_radius_km: float | None=None, time: int=20 ) -> Any:
    """Retrieve USGS earthquake feed and query.

    Purpose:
        Retrieve USGS earthquake feed and query through USGS Earthquake Hazards Program. Use
        ``mode`` to select among ``feed``, ``search``. Date and time arguments constrain the
        requested interval when supplied. Coordinate and bounding arguments constrain geographic
        scope when supported. Result-count arguments bound the amount of data requested.

    Args:
        mode: Operation selector. Supported values detected in the implementation include ``feed``,
            ``search``.
        feed: Predefined USGS earthquake feed name used when feed mode is selected.
        start_date: Inclusive start date for the requested time range, in the provider-supported format.
        end_date: Inclusive end date for the requested time range, in the provider-supported format.
        min_magnitude: Minimum earthquake magnitude to include in the result set.
        max_magnitude: Maximum earthquake magnitude to include in the result set.
        limit: Maximum number of records or items to return.
        order_by: Provider-supported field used to order results.
        event_type: USGS event type to include; ``earthquake`` is the default.
        latitude: Latitude in decimal degrees.
        longitude: Longitude in decimal degrees.
        max_radius_km: Maximum geographic search radius in kilometers.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = USGSEarthquakes( )
    return _instance.fetch( mode=mode, feed=feed, start_date=start_date, end_date=end_date,
	    min_magnitude=min_magnitude, max_magnitude=max_magnitude, limit=limit, order_by=order_by,
	    event_type=event_type, latitude=latitude, longitude=longitude,
	    max_radius_km=max_radius_km, time=time )


@function_tool
def fetch_usgs_water_data( mode: str='monitoring-locations', monitoring_location_id: str='',
		state_code: str='', county_code: str='', site_type: str='', parameter_code: str='',
		limit: int=25, time: int=20 ) -> Any:
    """Retrieve USGS water services records.

    Purpose:
        Retrieve USGS water services records through USGS Water Data. Use ``mode`` to select among
        ``latest-continuous``, ``latest-daily``, ``monitoring-locations``, ``time-series-metadata``.
        Result-count arguments bound the amount of data requested.

    Args:
        mode: Operation selector. Supported values detected in the implementation include ``latest-
            continuous``, ``latest-daily``, ``monitoring-locations``, ``time-series-metadata``.
        monitoring_location_id: USGS monitoring-location identifier used to target a specific site.
        state_code: State code used to restrict provider records.
        county_code: County code used to restrict provider records.
        site_type: USGS site-type code used to restrict monitoring locations.
        parameter_code: USGS parameter code identifying the measured property.
        limit: Maximum number of records or items to return.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = USGSWaterData( )
    return _instance.fetch( mode=mode, monitoring_location_id=monitoring_location_id, state_code=state_code, county_code=county_code, site_type=site_type, parameter_code=parameter_code, limit=limit, time=time )

@function_tool
def fetch_air_now( mode: str='current-zip', zip_code: str='', latitude: float | None=None,
		longitude: float | None=None, date: str='', distance: int=25, time: int=20 ) -> Any:
    """Retrieve AirNow current and forecast air quality data.

    Purpose:
        Retrieve AirNow current and forecast air quality data through AirNow. Use ``mode`` to select
        among ``current-latlon``, ``current-zip``, ``forecast-latlon``, ``forecast-zip``. Coordinate
        and bounding arguments constrain geographic scope when supported.

    Args:
        mode: Operation selector. Supported values detected in the implementation include ``current-
            latlon``, ``current-zip``, ``forecast-latlon``, ``forecast-zip``.
        zip_code: Provider code identifying or filtering zip.
        latitude: Latitude in decimal degrees.
        longitude: Longitude in decimal degrees.
        date: Date used by the provider or processing operation.
        distance: Maximum provider search distance, using the units defined by that service.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = AirNow( )
    return _instance.fetch( mode=mode, zip_code=zip_code, latitude=latitude, longitude=longitude, date=date, distance=distance, time=time )


@function_tool
def fetch_climate_data( mode: str='datasets', keyword: str='', dataset: str='', start_date: str='',
		end_date: str='', stations: str='', data_types: str='', limit: int=25,
		offset: int=0, time: int=20 ) -> Any:
    """Retrieve NOAA climate dataset and data records.

    Purpose:
        Retrieve NOAA climate dataset and data records through NOAA climate services. Use ``mode``
        to select among ``data``, ``datasets``. Date and time arguments constrain the requested
        interval when supplied. Result-count arguments bound the amount of data requested.

    Args:
        mode: Operation selector. Supported values detected in the implementation include ``data``,
            ``datasets``.
        keyword: Keyword used to filter provider records.
        dataset: Provider dataset name or identifier.
        start_date: Inclusive start date for the requested time range, in the provider-supported format.
        end_date: Inclusive end date for the requested time range, in the provider-supported format.
        stations: Station identifiers used to restrict climate observations.
        data_types: Climate data-type identifiers requested from the provider.
        limit: Maximum number of records or items to return.
        offset: Zero-based result offset used for pagination.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = ClimateData( )
    return _instance.fetch( mode=mode, keyword=keyword, dataset=dataset, start_date=start_date, end_date=end_date, stations=stations, data_types=data_types, limit=limit, offset=offset, time=time )


@function_tool
def fetch_eonet( mode: str='events', source: str='', category: str='', status: str='open',
		limit: int=25, days: int=30, start_date: str='', end_date: str='',
		bbox: str='', time: int=20 ) -> Any:
    """Retrieve NASA EONET environmental event data.

    Purpose:
        Retrieve NASA EONET environmental event data through NASA EONET. Use ``mode`` to select
        among ``categories``, ``events``. Date and time arguments constrain the requested interval
        when supplied. Coordinate and bounding arguments constrain geographic scope when supported.
        Result-count arguments bound the amount of data requested.

    Args:
        mode: Operation selector. Supported values detected in the implementation include
            ``categories``, ``events``.
        source: Provider source identifier used to restrict or classify results.
        category: Optional logical category retained in tool metadata.
        status: Provider status filter applied to returned records.
        limit: Maximum number of records or items to return.
        days: Number of calendar days included in the requested interval.
        start_date: Inclusive start date for the requested time range, in the provider-supported format.
        end_date: Inclusive end date for the requested time range, in the provider-supported format.
        bbox: Bounding box defining the geographic extent of the request.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = EoNet( )
    return _instance.fetch( mode=mode, source=source, category=category, status=status, limit=limit, days=days, start_date=start_date, end_date=end_date, bbox=bbox, time=time )


@function_tool
def fetch_envirofacts( table_name: str='TRI_FACILITY', state_code: str='',
		facility_name: str='', limit: int=25, time: int=20 ) -> Any:
    """Retrieve EPA Envirofacts table and facility records.

    Purpose:
        Retrieve EPA Envirofacts table and facility records through EPA Envirofacts. Result-count
        arguments bound the amount of data requested.

    Args:
        table_name: Envirofacts table or resource name to query.
        state_code: State code used to restrict provider records.
        facility_name: Facility-name filter applied to Envirofacts records.
        limit: Maximum number of records or items to return.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = EnviroFacts( )
    return _instance.fetch( table_name=table_name, state_code=state_code, facility_name=facility_name, limit=limit, time=time )


@function_tool
def fetch_tides_and_currents( mode: str='water-level', station_id: str='', begin_date: str='',
		end_date: str='', datum: str='MLLW', units: str='metric', time_zone: str='gmt',
		interval: str='hilo', time: int=20 ) -> Any:
    """Retrieve NOAA tides, currents, and station data.

    Purpose:
        Retrieve NOAA tides, currents, and station data through NOAA Tides & Currents. Use ``mode``
        to select among ``station``, ``tide-predictions``, ``water-level``. Date and time arguments
        constrain the requested interval when supplied.

    Args:
        mode: Operation selector. Supported values detected in the implementation include ``station``,
            ``tide-predictions``, ``water-level``.
        station_id: Provider identifier for the selected station.
        begin_date: Beginning date for the requested interval, in the provider-supported format.
        end_date: Inclusive end date for the requested time range, in the provider-supported format.
        datum: Vertical datum used for tide or water-level measurements.
        units: Unit system used for returned measurements.
        time_zone: Timezone used for returned tide or current timestamps.
        interval: Provider sampling or reporting interval.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = TidesAndCurrents( )
    return _instance.fetch( mode=mode, station_id=station_id, begin_date=begin_date, end_date=end_date, datum=datum, units=units, time_zone=time_zone, interval=interval, time=time )


@function_tool
def fetch_uv_index( mode: str='daily-zip', zip_code: str='', city: str='',
		state: str='', time: int=20 ) -> Any:
    """Retrieve EPA UV Index current and forecast data.

    Purpose:
        Retrieve EPA UV Index current and forecast data through EPA UV Index. Use ``mode`` to select
        among ``daily-city-state``, ``daily-zip``, ``hourly-city-state``, ``hourly-zip``.

    Args:
        mode: Operation selector. Supported values detected in the implementation include ``daily-
            city-state``, ``daily-zip``, ``hourly-city-state``, ``hourly-zip``.
        zip_code: Provider code identifying or filtering zip.
        city: City name used to locate or filter provider records.
        state: State name or abbreviation used to locate or filter provider records.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = UvIndex( )
    return _instance.fetch( mode=mode, zip_code=zip_code, city=city, state=state, time=time )


@function_tool
def fetch_purple_air( mode: str='sensors', sensor_index: int | None=None, nwlng: float | None=None,
		nwlat: float | None=None, selng: float | None=None, selat: float | None=None,
		location_type: int=0, max_age: int=0, modified_since: int=0, fields: str='',
		time: int=20 ) -> Any:
    """Retrieve PurpleAir sensor and air quality records.

    Purpose:
        Retrieve PurpleAir sensor and air quality records through PurpleAir. Use ``mode`` to select
        among ``sensor``, ``sensors``. Coordinate and bounding arguments constrain geographic scope
        when supported.

    Args:
        mode: Operation selector. Supported values detected in the implementation include ``sensor``,
            ``sensors``.
        sensor_index: PurpleAir sensor identifier.
        nwlng: Northwest bounding-box longitude in decimal degrees.
        nwlat: Northwest bounding-box latitude in decimal degrees.
        selng: Southeast bounding-box longitude in decimal degrees.
        selat: Southeast bounding-box latitude in decimal degrees.
        location_type: Provider type selector for location.
        max_age: Maximum age permitted by the operation.
        modified_since: Unix timestamp used to return PurpleAir sensors modified after the specified time.
        fields: Comma-separated or provider-specific field selection.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = PurpleAir( )
    return _instance.fetch( mode=mode, sensor_index=sensor_index, nwlng=nwlng, nwlat=nwlat, selng=selng, selat=selat, location_type=location_type, max_age=max_age, modified_since=modified_since, fields=fields, time=time )


@function_tool
def fetch_open_aq( mode: str='locations', location_id: int | None=None, parameter_id: int | None=None,
		country_id: int | None=None, coordinates: str='', radius: int=25000, providers_id: str='',
		parameters_id: str='', limit: int=25, page: int=1, time: int=20 ) -> Any:
    """Retrieve OpenAQ location, measurement, and air-quality records.

    Purpose:
        Retrieve OpenAQ location, measurement, and air-quality records through OpenAQ. Use ``mode``
        to select among ``countries``, ``latest``, ``locations``, ``parameter_latest``,
        ``parameters``, ``providers``. Coordinate and bounding arguments constrain geographic scope
        when supported. Result-count arguments bound the amount of data requested.

    Args:
        mode: Operation selector. Supported values detected in the implementation include
            ``countries``, ``latest``, ``locations``, ``parameter_latest``, ``parameters``,
            ``providers``.
        location_id: Provider identifier for the selected location.
        parameter_id: Provider identifier for the selected parameter.
        country_id: Provider identifier for the selected country.
        coordinates: Latitude/longitude coordinate string used by the provider.
        radius: Search radius in the units specified by the operation.
        providers_id: Provider identifier for the selected providers.
        parameters_id: Provider identifier for the selected parameters.
        limit: Maximum number of records or items to return.
        page: One-based result page to request.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = OpenAQ( )
    return _instance.fetch( mode=mode, location_id=location_id, parameter_id=parameter_id, country_id=country_id, coordinates=coordinates, radius=radius, providers_id=providers_id, parameters_id=parameters_id, limit=limit, page=page, time=time )


@function_tool
def fetch_firms( mode: str='area', source: str='VIIRS_SNPP_NRT', area_coordinates: str='world',
		day_range: int=1, date: str='', sensor: str='ALL', time: int=20 ) -> Any:
    """Retrieve NASA FIRMS active fire data.

    Purpose:
        Retrieve NASA FIRMS active fire data through NASA FIRMS. Use ``mode`` to select among
        ``area``, ``data-availability``.

    Args:
        mode: Operation selector. Supported values detected in the implementation include ``area``,
            ``data-availability``.
        source: Provider source identifier used to restrict or classify results.
        area_coordinates: FIRMS area-of-interest coordinates or ``world`` selector.
        day_range: Number of days included in the FIRMS active-fire request.
        date: Date used by the provider or processing operation.
        sensor: Sensor or instrument filter applied to provider results.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = Firms( )
    return _instance.fetch( mode=mode, source=source, area_coordinates=area_coordinates,
	    day_range=day_range, date=date, sensor=sensor, time=time )



@function_tool
def geocode_location( address: str ) -> Any:
    """Geocode location.

    Purpose:
        Geocode location using Google Maps.

    Args:
        address: Street address or place description used for geocoding, validation, or routing.

    Returns:
        Tuple[float, float]: Latitude and longitude coordinate pair.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleMaps( )
    return _instance.geocode_location( address=address )


@function_tool
def geocode_coordinates( lat: float, long: float ) -> Any:
    """Geocode coordinates.

    Purpose:
        Geocode coordinates using Google Maps. Coordinate and bounding arguments constrain
        geographic scope when supported.

    Args:
        lat: Latitude in decimal degrees.
        long: Longitude in decimal degrees.

    Returns:
        str | None: Text produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleMaps( )
    return _instance.geocode_coordinates( lat=lat, long=long )


@function_tool
def validate_address( address: List[str] ) -> Any:
    """Validate address.

    Purpose:
        Validate address using Google Maps.

    Args:
        address: Street address or place description used for geocoding, validation, or routing.

    Returns:
        Dict[Any, Any] | None: Structured mapping produced by the operation.

    Raises:
        TypeError: If a supplied value has an unsupported type.
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleMaps( )
    return _instance.validate_address( address=address )


@function_tool
def request_directions( origin: str, destination: str, mode: str='driving' ) -> Any:
    """Request directions.

    Purpose:
        Request directions using Google Maps.

    Args:
        origin: Starting address or place for a routing request.
        destination: Destination address or place for a routing request.
        mode: Operation mode used to select the provider or processing workflow.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleMaps( )
    return _instance.request_directions( origin=origin, destination=destination, mode=mode )


@function_tool
def fetch_global_imagery_wms_map( layer: str,
		image_date: str, bbox: Tuple[float, float, float, float],
		width: int=1200, height: int=600, projection: str='epsg4326', quality: str='best',
		image_format: str='image/png', transparent: bool=True, output_dir: str='python-examples',
		output_name: str='', time: int=20 ) -> Any:
    """Retrieve a WMS imagery map.

    Purpose:
        Retrieve a WMS imagery map through NASA Global Imagery Browse Services. Coordinate and
        bounding arguments constrain geographic scope when supported.

    Args:
        layer: Map or imagery layer identifier.
        image_date: Observation date used to select imagery.
        bbox: Bounding box defining the geographic extent of the request.
        width: Output image or chart width in pixels.
        height: Output image or chart height in pixels.
        projection: Coordinate reference system used for rendered imagery.
        quality: Imagery quality level requested from the mapping service.
        image_format: Output format requested for image.
        transparent: Whether the generated map image should use a transparent background.
        output_dir: Local directory where generated imagery is written.
        output_name: Optional filename for generated imagery.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GlobalImagery( )
    return _instance.fetch_wms_map( layer=layer, image_date=image_date, bbox=bbox, width=width, height=height, projection=projection, quality=quality, image_format=image_format, transparent=transparent, output_dir=output_dir, output_name=output_name, time=time )


@function_tool
def fetch_global_imagery_map_services(  ) -> Any:
    """Retrieve available imagery map services.

    Purpose:
        Retrieve available imagery map services through NASA Global Imagery Browse Services.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GlobalImagery( )
    return _instance.fetch_map_services(  )


@function_tool
def fetch_global_imagery_mercator_map( ccrs: Any | None=None ) -> Any:
    """Render a Mercator imagery map.

    Purpose:
        Render a Mercator imagery map through NASA Global Imagery Browse Services.

    Args:
        ccrs (Any): Optional Cartopy coordinate reference system used to construct the map.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GlobalImagery( )
    return _instance.fetch_mercator_map( ccrs=ccrs )

@function_tool
def fetch_google_geocoding( mode: str='forward', query: str='', latitude: float=0.0,
		longitude: float=0.0, place_id: str='', language: str='en', region: str='',
		result_type: str='', location_type: str='', time: int=10, api_key: Optional[str]=None ) -> Any:
    """Retrieve Google forward, reverse, and place geocoding.

    Purpose:
        Retrieve Google forward, reverse, and place geocoding through Google Geocoding. Use ``mode``
        to select among ``forward``, ``place``, ``reverse``. The query text determines the records
        or documents matched by the provider. Coordinate and bounding arguments constrain geographic
        scope when supported. When supplied, ``api_key`` overrides the configured provider
        credential for this request.

    Args:
        mode: Operation selector. Supported values detected in the implementation include ``forward``,
            ``place``, ``reverse``.
        query: Search text, lookup value, or provider query submitted by the caller.
        latitude: Latitude in decimal degrees.
        longitude: Longitude in decimal degrees.
        place_id: Provider identifier for the selected place.
        language: Language code used for provider results or parsing.
        region: Provider region filter or regional bias value.
        result_type: Provider type selector for result.
        location_type: Provider type selector for location.
        time: Request timeout in seconds.
        api_key: Optional credential override used for the active request.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GoogleGeocoding( )
    return _instance.fetch( mode=mode, query=query, latitude=latitude, longitude=longitude,
	    place_id=place_id, language=language, region=region, result_type=result_type,
	    location_type=location_type, time=time, api_key=api_key )


@function_tool
def fetch_usgs_national_map( mode: str='products', dataset: str='', q: str='', bbox: str='',
		prod_formats: str='', max_items: int=25, offset: int=0, time: int=20 ) -> Any:
    """Retrieve USGS National Map datasets and products.

    Purpose:
        Retrieve USGS National Map datasets and products through USGS The National Map. Use ``mode``
        to select among ``datasets``, ``products``. The query text determines the records or
        documents matched by the provider. Coordinate and bounding arguments constrain geographic
        scope when supported. Result-count arguments bound the amount of data requested.

    Args:
        mode: Operation selector. Supported values detected in the implementation include
            ``datasets``, ``products``.
        dataset: Provider dataset name or identifier.
        q: Free-text provider query used to search matching records.
        bbox: Bounding box defining the geographic extent of the request.
        prod_formats: Product-format filter applied to National Map results.
        max_items: Maximum number of records or items to return.
        offset: Zero-based result offset used for pagination.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = USGSTheNationalMap( )
    return _instance.fetch( mode=mode, dataset=dataset, q=q, bbox=bbox, prod_formats=prod_formats, max_items=max_items, offset=offset, time=time )


@function_tool
def fetch_usgs_sciencebase( mode: str='items', q: str='', item_id: str='', max_items: int=25,
		offset: int=0, fields: str='', time: int=20 ) -> Any:
    """Retrieve USGS ScienceBase items and catalog records.

    Purpose:
        Retrieve USGS ScienceBase items and catalog records through USGS ScienceBase. Use ``mode``
        to select among ``item``, ``items``. The query text determines the records or documents
        matched by the provider. Result-count arguments bound the amount of data requested.

    Args:
        mode: Operation selector. Supported values detected in the implementation include ``item``,
            ``items``.
        q: Free-text provider query used to search matching records.
        item_id: Provider identifier for the selected item.
        max_items: Maximum number of records or items to return.
        offset: Zero-based result offset used for pagination.
        fields: Comma-separated or provider-specific field selection.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = USGSScienceBase( )
    return _instance.fetch( mode=mode, q=q, item_id=item_id, max_items=max_items, offset=offset, fields=fields, time=time )

# ==========================================================================================
# ==========================================================================================


@function_tool
def fetch_health_data( mode: str='rows', domain: str='healthdata.gov', dataset_id: str='',
		select: str='', where: str='', order: str='', group: str='', limit: int=25,
		offset: int=0, time: int=20 ) -> Any:
    """Retrieve HealthData.gov Socrata metadata and rows.

    Purpose:
        Retrieve HealthData.gov Socrata metadata and rows through HealthData.gov. Use ``mode`` to
        select among ``metadata``, ``rows``. Result-count arguments bound the amount of data
        requested.

    Args:
        mode: Operation selector. Supported values detected in the implementation include
            ``metadata``, ``rows``.
        domain: Provider domain or host containing the requested dataset.
        dataset_id: Provider dataset identifier.
        select: Socrata ``$select`` expression defining returned columns or calculations.
        where: Socrata ``$where`` filter expression.
        order: Provider-supported result ordering expression.
        group: Socrata ``$group`` expression used to aggregate rows.
        limit: Maximum number of records or items to return.
        offset: Zero-based result offset used for pagination.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = HealthData( )
    return _instance.fetch( mode=mode, domain=domain, dataset_id=dataset_id, select=select, where=where, order=order, group=group, limit=limit, offset=offset, time=time )


@function_tool
def fetch_global_health_data( mode: str='indicator_registry', query_path: str='',
		fmt: str='json', time: int=20 ) -> Any:
    """Retrieve WHO global health indicator and Athena data.

    Purpose:
        Retrieve WHO global health indicator and Athena data through WHO Global Health. Use ``mode``
        to select among ``athena``, ``indicator_registry``.

    Args:
        mode: Operation selector. Supported values detected in the implementation include ``athena``,
            ``indicator_registry``.
        query_path: Path identifying the query resource.
        fmt: Provider response format, such as JSON or XML when supported.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GlobalHealthData( )
    return _instance.fetch( mode=mode, query_path=query_path, fmt=fmt, time=time )


@function_tool
def fetch_wonder( mode: str='metadata_template', dataset_id: str='D76',
		request_xml: str='', time: int=20 ) -> Any:
    """Retrieve CDC WONDER template and query submission.

    Purpose:
        Retrieve CDC WONDER template and query submission through CDC WONDER. Use ``mode`` to select
        among ``metadata_template``, ``query_xml``.

    Args:
        mode: Operation selector. Supported values detected in the implementation include
            ``metadata_template``, ``query_xml``.
        dataset_id: Provider dataset identifier.
        request_xml: CDC WONDER XML request document submitted for query execution.
        time: Request timeout in seconds.

    Returns:
        Dict[str, Any] | None: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = Wonder( )
    return _instance.fetch( mode=mode, dataset_id=dataset_id, request_xml=request_xml, time=time )


@function_tool
def load_pubmed( query: str, max_docs: int=5 ) -> Any:
    """Load PubMed research documents.

    Purpose:
        Load PubMed research documents using the PubMed loader. The query text determines the
        records or documents matched by the provider. Result-count arguments bound the amount of
        data requested.

    Args:
        query: Search query submitted to the backing loader.
        max_docs: Maximum number of documents requested from the backing service.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = PubMedSearchLoader( )
    return _instance.load( query=query, max_docs=max_docs )

# ==========================================================================================
# ==========================================================================================


@function_tool
def fetch_web_page( url: str, time: int=10 ) -> Any:
    """Retrieve HTTP web page retrieval and HTML extraction.

    Purpose:
        Retrieve HTTP web page retrieval and HTML extraction through web fetcher.

    Args:
        url: URL or URI value used as the request or parsing source.
        time: Request timeout in seconds.

    Returns:
        Result | None: Fonky result wrapper containing the provider or HTTP response.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebFetcher( )
    return _instance.fetch( url=url, time=time )


@function_tool
def convert_html_to_text( html: str ) -> Any:
    """Convert HTML to plain text.

    Purpose:
        Convert HTML to plain text using Fonky's web fetcher implementation.

    Args:
        html: Raw HTML content to parse or transform.

    Returns:
        str: Text produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebFetcher( )
    return _instance.html_to_text( html=html )


@function_tool
def extract_web_title( html: str ) -> Any:
    """Extract web title from the supplied content.

    Purpose:
        Extract web title from the supplied content using Fonky's web fetcher implementation.

    Args:
        html: Raw HTML content to parse or transform.

    Returns:
        str: Text produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebFetcher( )
    return _instance.extract_title( html=html )


@function_tool
def extract_web_links( base_url: str, html: str ) -> Any:
    """Extract web links from the supplied content.

    Purpose:
        Extract web links from the supplied content using Fonky's web fetcher implementation.

    Args:
        base_url: URL or URI value used as the request or parsing source.
        html: Raw HTML content to parse or transform.

    Returns:
        List[str]: Hyperlink values produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebFetcher( )
    return _instance.extract_links( base_url=base_url, html=html )


@function_tool
def extract_web_structured_data( url: str, html: str,
		selected_methods: Optional[List[str]]=None ) -> Any:
    """Extract structured data.

    Purpose:
        Extract structured data using Fonky's web fetcher implementation.

    Args:
        url: URL or URI value used as the request or parsing source.
        html: Raw HTML content to parse or transform.
        selected_methods: Extraction method names to execute against the supplied HTML.

    Returns:
        Dict[str, List[str]]: Text or identifier values produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebFetcher( )
    return _instance.extract_structured_data( url=url, html=html, selected_methods=selected_methods )


@function_tool
def crawl_web( seed_url: str, include_title: bool=True, include_basic_text: bool=True,
		include_raw_html: bool=False, selected_methods: Optional[List[str]]=None,
		recursive: bool=False, max_depth: int=1, max_pages: int=10, same_domain_only: bool=True,
		request_timeout: int=10, delay_seconds: float=0.25, max_bytes: int=1000000,
		headers: Optional[ Dict[ str, str ] ]=None, use_playwright: bool=False ) -> Any:
    """Crawl web pages from a seed URL.

    Purpose:
        Crawl web pages from a seed URL. Boolean options control retrieval depth or supplemental
        content.

    Args:
        seed_url: Starting URL for the crawl.
        include_title: Whether to include title in the result.
        include_basic_text: Whether to include basic text in the result.
        include_raw_html: Whether to include raw html in the result.
        selected_methods: Extraction method names to execute against the supplied HTML.
        recursive: Whether nested folders, links, or provider resources should be traversed.
        max_depth: Maximum recursion depth.
        max_pages: Maximum pages permitted by the operation.
        same_domain_only: Whether crawl traversal should remain on the seed URL domain.
        request_timeout: Request timeout in seconds.
        delay_seconds: Delay in seconds inserted between crawl requests.
        max_bytes: Maximum bytes permitted by the operation.
        headers: Optional HTTP headers applied to web requests.
        use_playwright: Whether browser-backed rendering should be used for dynamic pages.

    Returns:
        Dict[str, Any]: Structured mapping produced by the operation.

    Raises:
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebCrawler( headers=headers, use_playwright=use_playwright )
    return _instance.crawl( seed_url=seed_url, include_title=include_title,
	    include_basic_text=include_basic_text, include_raw_html=include_raw_html,
	    selected_methods=selected_methods, recursive=recursive, max_depth=max_depth,
	    max_pages=max_pages, same_domain_only=same_domain_only, request_timeout=request_timeout,
	    delay_seconds=delay_seconds, max_bytes=max_bytes )


@function_tool
def scrape_crawler_page( url: str, include_title: bool=True, include_basic_text: bool=True,
		include_raw_html: bool=False, selected_methods: Optional[List[str]]=None,
		request_timeout: int=10, max_bytes: int=1000000,
		headers: Optional[ Dict[ str, str ] ]=None, use_playwright: bool=False ) -> Any:
    """Extract crawler page from an HTML page.

    Purpose:
        Extract crawler page from an HTML page using Fonky's web crawler implementation.

    Args:
        url: URL or URI value used as the request or parsing source.
        include_title: Whether to include title in the result.
        include_basic_text: Whether to include basic text in the result.
        include_raw_html: Whether to include raw html in the result.
        selected_methods: Extraction method names to execute against the supplied HTML.
        request_timeout: Request timeout in seconds.
        max_bytes: Maximum bytes permitted by the operation.
        headers: Optional HTTP headers applied to web requests.
        use_playwright: Whether browser-backed rendering should be used for dynamic pages.

    Returns:
        Dict[str, Any]: Structured mapping produced by the operation.

    Raises:
        Exception: If the delegated implementation raises an operational failure.
    """
    _instance = WebCrawler( headers=headers, use_playwright=use_playwright )
    return _instance.scrape_page( url=url, include_title=include_title, include_basic_text=include_basic_text, include_raw_html=include_raw_html, selected_methods=selected_methods, request_timeout=request_timeout, max_bytes=max_bytes )


@function_tool
def render_web_page( url: str, timeout: int=15, headers: Optional[ Dict[ str, str ] ]=None,
		use_playwright: bool=False ) -> Any:
    """Render a dynamic web page with Playwright.

    Purpose:
        Render a dynamic web page with Playwright.

    Args:
        url: URL or URI value used as the request or parsing source.
        timeout: Request timeout in seconds.
        headers: Optional HTTP headers applied to web requests.
        use_playwright: Whether browser-backed rendering should be used for dynamic pages.

    Returns:
        str: Text produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebCrawler( headers=headers, use_playwright=use_playwright )
    return _instance.render_with_playwright( url=url, timeout=timeout )


@function_tool
def load_web( urls: str | List[str], recursive: bool=False, max_depth: int=2,
		prevent_outside: bool=True, timeout: int=10, ignore: bool=True, progress: bool=True ) -> Any:
    """Load web documents.

    Purpose:
        Load web documents using the web loader. Boolean options control retrieval depth or
        supplemental content.

    Args:
        urls: URL string or URL list used as web-loader input.
        recursive: Whether nested folders, links, or provider resources should be traversed.
        max_depth: Maximum recursion depth.
        prevent_outside: Whether recursive web loading should exclude pages outside the seed domain.
        timeout: Maximum time in seconds to wait for the operation.
        ignore: Whether individual loading failures should be skipped when supported.
        progress: Whether the underlying loader should report progress.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        ValueError: Raised when a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebLoader( recursive=recursive, max_depth=max_depth, prevent_outside=prevent_outside, timeout=timeout, ignore=ignore, progress=progress )
    return _instance.load( urls=urls )


@function_tool
def load_web_recursive( url: str, depth: int=2, max_time: int=10, ignore: bool=True ) -> Any:
    """Recursively load web documents.

    Purpose:
        Recursively load web documents using the web loader.

    Args:
        url: URL used by the web or repository loader.
        depth: Maximum recursion depth.
        max_time: Maximum request or crawl time in seconds.
        ignore: Whether individual loading failures should be skipped when supported.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebLoader( )
    return _instance.load_recursive( url=url, depth=depth, max_time=max_time, ignore=ignore )


@function_tool
def load_web_pages( urls: List[str], depth: int=2, timeout: int=10, ignore: bool=True,
		progress: bool=True ) -> Any:
    """Load static web pages.

    Purpose:
        Load static web pages using the web loader.

    Args:
        urls: URL string or URL list used as web-loader input.
        depth: Maximum recursion depth.
        timeout: Maximum time in seconds to wait for the operation.
        ignore: Whether individual loading failures should be skipped when supported.
        progress: Whether the underlying loader should report progress.

    Returns:
        List[Document] | None: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebLoader( )
    return _instance.load_pages( urls=urls, depth=depth, timeout=timeout, ignore=ignore, progress=progress )


@function_tool
def load_github( url: str, repo: str, branch: str, filetype: str='.md' ) -> Any:
    """Load files from a GitHub repository.

    Purpose:
        Load files from a GitHub repository using the GitHub loader.

    Args:
        url: URL used by the web or repository loader.
        repo: GitHub repository name or owner/repository path.
        branch: Repository branch to inspect.
        filetype: File suffix filter used when loading repository files.

    Returns:
        List[Document]: LangChain documents loaded from the requested source.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = GithubLoader( )
    return _instance.load( url=url, repo=repo, branch=branch, filetype=filetype )


@function_tool
def scrape_web_page( url: str, time: int=10 ) -> Any:
    """Fetch a web page for extraction.

    Purpose:
        Fetch a web page for extraction using Fonky's web extractor implementation.

    Args:
        url: Absolute URL to fetch.
        time: Request timeout in seconds.

    Returns:
        Result | None: Fonky result wrapper containing the provider or HTTP response.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebExtractor( )
    return _instance.scrape( url=url, time=time )


@function_tool
def scraper_html_to_text( html: str ) -> Any:
    """Convert HTML to plain text.

    Purpose:
        Convert HTML to plain text.

    Args:
        html: Raw HTML string to convert.

    Returns:
        str: Text produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebExtractor( )
    return _instance.html_to_text( html=html )


@function_tool
def scrape_paragraphs( uri: str ) -> Any:
    """Extract paragraph text.

    Purpose:
        Extract paragraph text using Fonky's web extractor implementation.

    Args:
        uri: Fully qualified URI of the target HTML document.

    Returns:
        List[str] | None: Paragraph text values produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebExtractor( )
    return _instance.scrape_paragraphs( uri=uri )


@function_tool
def scrape_lists( uri: str ) -> Any:
    """Extract list item text.

    Purpose:
        Extract list item text using Fonky's web extractor implementation.

    Args:
        uri: Fully qualified URI of the target HTML page.

    Returns:
        List[str] | None: Text or identifier values produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebExtractor( )
    return _instance.scrape_lists( uri=uri )


@function_tool
def scrape_tables( uri: str ) -> Any:
    """Extract table cell text.

    Purpose:
        Extract table cell text using Fonky's web extractor implementation.

    Args:
        uri: Fully qualified URI of the target HTML document.

    Returns:
        List[str] | None: Table cell text values produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebExtractor( )
    return _instance.scrape_tables( uri=uri )


@function_tool
def scrape_articles( uri: str ) -> Any:
    """Extract article text.

    Purpose:
        Extract article text using Fonky's web extractor implementation.

    Args:
        uri: Fully qualified URI of the target HTML page.

    Returns:
        List[str] | None: Text or identifier values produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebExtractor( )
    return _instance.scrape_articles( uri=uri )


@function_tool
def scrape_headings( uri: str ) -> Any:
    """Extract heading text.

    Purpose:
        Extract heading text using Fonky's web extractor implementation.

    Args:
        uri: Fully qualified URI of the target HTML document.

    Returns:
        List[str] | None: Heading text values produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebExtractor( )
    return _instance.scrape_headings( uri=uri )


@function_tool
def scrape_divisions( uri: str ) -> Any:
    """Extract division text.

    Purpose:
        Extract division text using Fonky's web extractor implementation.

    Args:
        uri: Fully qualified URI of the target HTML document.

    Returns:
        List[str] | None: Text or identifier values produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebExtractor( )
    return _instance.scrape_divisions( uri=uri )


@function_tool
def scrape_sections( uri: str ) -> Any:
    """Extract section text.

    Purpose:
        Extract section text using Fonky's web extractor implementation.

    Args:
        uri: Fully qualified URI of the target HTML document.

    Returns:
        List[str] | None: Text or identifier values produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebExtractor( )
    return _instance.scrape_sections( uri=uri )


@function_tool
def scrape_blockquotes( uri: str ) -> Any:
    """Extract blockquote text.

    Purpose:
        Extract blockquote text using Fonky's web extractor implementation.

    Args:
        uri: Fully qualified URI of the target HTML document.

    Returns:
        List[str] | None: Text or identifier values produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebExtractor( )
    return _instance.scrape_blockquotes( uri=uri )


@function_tool
def scrape_hyperlinks( uri: str ) -> Any:
    """Extract hyperlinks from an HTML page.

    Purpose:
        Extract hyperlinks from an HTML page using Fonky's web extractor implementation.

    Args:
        uri: Fully qualified URI of the target HTML page.

    Returns:
        List[str] | None: Hyperlink values produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebExtractor( )
    return _instance.scrape_hyperlinks( uri=uri )


@function_tool
def scrape_images( uri: str ) -> Any:
    """Extract image references.

    Purpose:
        Extract image references using Fonky's web extractor implementation.

    Args:
        uri: Fully qualified URI of the target HTML page.

    Returns:
        List[str] | None: Image references produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in
            the project error type.
    """
    _instance = WebExtractor( )
    return _instance.scrape_images( uri=uri )


@function_tool
def encode_image( path: str ) -> str:
    """Encode a local image as Base64 text.

    Purpose:
        Encode a local image as Base64 text using Fonky's provider implementation.

    Args:
        path: Local image path to encode.

    Returns:
        str: Text produced by the operation.

    Raises:
        Exception: If the delegated implementation raises an operational failure.
    """
    return _encode_image( path=path )

# ==========================================================================================
# PREPROCESSOR TOOLS
# ==========================================================================================

@function_tool
def preprocess_load_text( filepath: str ) -> str | None:
    """Read UTF-8 text from a local file and return the raw string.

    Purpose:
        Loads a local text file using UTF-8 with ignored decode errors so downstream cleaning routines
        can operate on a plain string. The method records the active file path and raises a project
        Error when the file cannot be read.

    Args:
        filepath: Path to the local source file.

    Returns:
        str | None: Processed text value when the operation succeeds.

    Raises:
        FileNotFoundError: If a required local file or matched path does not exist.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.load_text( filepath=filepath )

@function_tool
def preprocess_collapse_whitespace( text: str ) -> str | None:
    """Normalize spacing by lowercasing text and collapsing repeated whitespace.

    Purpose:
        Creates a compact lowercase representation of text by splitting on whitespace and joining
        tokens with single spaces. This prepares raw text for deterministic comparison, cleaning, and
        tokenization steps.

    Args:
        text: Text value to process.

    Returns:
        str | None: Processed text value when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.collapse_whitespace( text=text )

@function_tool
def preprocess_remove_punctuation( text: str ) -> str:
    """Strip punctuation from tokenized text while preserving word and spacing content.

    Purpose:
        Tokenizes lowercase text and removes punctuation marks from each token. The method preserves
        alphanumeric token content while returning a whitespace-joined string for later cleaning
        stages.

    Args:
        text: Text value to process.

    Returns:
        str: Processed text value produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.remove_punctuation( text=text )

@function_tool
def preprocess_normalize_text( text: str ) -> str | None:
    """Convert text to lowercase for stable downstream comparison and tokenization.

    Purpose:
        Converts text to lowercase without otherwise changing content. This provides a simple
        normalization stage for workflows that need case-insensitive matching or tokenization.

    Args:
        text: Text value to process.

    Returns:
        str | None: Processed text value when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.normalize_text( text=text )

@function_tool
def preprocess_remove_errors( text: str ) -> str:
    """Filter tokens against the NLTK English words corpus.

    Purpose:
        Uses the NLTK English words corpus as a vocabulary filter and keeps only tokens recognized by
        that corpus. This reduces obvious OCR, spelling, and parsing artifacts before later analysis.

    Args:
        text: Text value to process.

    Returns:
        str: Processed text value produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.remove_errors( text=text )

@function_tool
def preprocess_remove_fragments( text: str ) -> str | None:
    """Remove very short token fragments from normalized text.

    Purpose:
        Removes short text fragments that are unlikely to be useful lexical units. This helps reduce
        noise produced by OCR, markup stripping, punctuation removal, and aggressive token cleanup.

    Args:
        text: Text value to process.

    Returns:
        str | None: Processed text value when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.remove_fragments( text=text )

@function_tool
def preprocess_remove_symbols( text: str ) -> str | None:
    """Remove configured symbol characters from normalized text.

    Purpose:
        Removes characters listed in the parser symbol set from lowercase text. This produces cleaner
        text for tokenization, word-frequency generation, and embedding workflows.

    Args:
        text: Text value to process.

    Returns:
        str | None: Processed text value when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.remove_symbols( text=text )

@function_tool
def preprocess_remove_html( text: str ) -> str | None:
    """Extract visible text from HTML markup.

    Purpose:
        Parses HTML input with BeautifulSoup and extracts visible text content. This allows raw HTML
        fragments or pages to enter the same cleaning pipeline used for plain text.

    Args:
        text: Text value to process.

    Returns:
        str | None: Processed text value when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.remove_html( text=text )

@function_tool
def preprocess_remove_xml( text: str ) -> str:
    """Extract inner text from XML-like markup while recovering malformed fragments when possible.

    Purpose:
        Wraps XML-like text in a temporary root node, parses it with recovery enabled, and
        concatenates element text and tail content. This retains readable content while discarding
        markup structure.

    Args:
        text: Text value to process.

    Returns:
        str: Processed text value produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.remove_xml( text=text )

@function_tool
def preprocess_remove_markdown( text: str ) -> str | None:
    """Remove common Markdown links, image syntax, and formatting markers.

    Purpose:
        Removes common Markdown link, image, and inline-formatting syntax from lowercase text. This
        converts README-style or documentation-style content into cleaner text for downstream
        analysis.

    Args:
        text: Text value to process.

    Returns:
        str | None: Processed text value when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.remove_markdown( text=text )

@function_tool
def preprocess_remove_stopwords( text: str ) -> str | None:
    """Remove English stop words from tokenized text.

    Purpose:
        Tokenizes lowercase text and removes standard English stop words. This leaves a reduced token
        stream better suited for frequency analysis, vocabulary extraction, and embedding preparation.

    Args:
        text: Text value to process.

    Returns:
        str | None: Processed text value when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.remove_stopwords( text=text )

@function_tool
def preprocess_remove_encodings( text: str ) -> str | None:
    """Resolve HTML entities, normalize Unicode characters, and remove control characters.

    Purpose:
        Decodes common escaped sequences when possible, resolves HTML entities, normalizes Unicode to
        compatibility form, and strips control characters. This reduces text artifacts from scraped,
        copied, or encoded sources.

    Args:
        text: Text value to process.

    Returns:
        str | None: Processed text value when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.remove_encodings( text=text )

@function_tool
def preprocess_remove_headers( filepath: str, lines: int=50, headers: int=3, footers: int=3 ) -> str | None:
    """Detect and remove repeated page headers and footers from a text file.

    Purpose:
        Splits a text file into page-sized blocks and identifies repeated leading and trailing line
        groups. Matching header and footer blocks are removed to produce cleaner body text for
        analysis.

    Args:
        filepath: Path to the local source file.
        lines: Number of lines treated as one page during header and footer detection.
        headers: Number of leading lines considered as a repeated page header.
        footers: Number of trailing lines considered as a repeated page footer.

    Returns:
        str | None: Processed text value when the operation succeeds.

    Raises:
        FileNotFoundError: If a required local file or matched path does not exist.
        ValueError: If a required value is missing, blank, or outside the supported range.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.remove_headers( filepath=filepath, lines=lines, headers=headers, footers=footers )

@function_tool
def preprocess_remove_numbers( text: str ) -> str | None:
    """Remove decimal digits from text.

    Purpose:
        Removes digit sequences from lowercase text. This supports workflows that need lexical content
        without numeric values.

    Args:
        text: Text value to process.

    Returns:
        str | None: Processed text value when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.remove_numbers( text=text )

@function_tool
def preprocess_remove_numerals( text: str ) -> str | None:
    """Remove Roman-numeral patterns from text.

    Purpose:
        Applies the configured Roman-numeral expression to lowercase text and replaces matching
        numeral tokens with spaces. This reduces numbering artifacts in outlines, headings, and
        document sections.

    Args:
        text: Text value to process.

    Returns:
        str | None: Processed text value when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.remove_numerals( text=text )

@function_tool
def preprocess_remove_images( text: str ) -> str:
    """Remove Markdown image references, HTML image elements, and direct image URLs.

    Purpose:
        Removes Markdown image syntax, HTML image tags, and direct image URLs from text. This keeps
        descriptive text while excluding image-only references that do not support text processing.

    Args:
        text: Text value to process.

    Returns:
        str: Processed text value produced by the operation.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.remove_images( text=text )

@function_tool
def preprocess_tiktokenize( text: str, encoding: str='cl100k_base' ) -> DataFrame | None:
    """Encode text with a tiktoken tokenizer and return token identifiers as tabular data.

    Purpose:
        Encodes lowercase text using the requested tiktoken encoding and returns token identifiers in
        a pandas DataFrame. This supports token inspection and model-facing preprocessing workflows.

    Args:
        text: Text value to process.
        encoding: Tiktoken encoding name used for tokenization.

    Returns:
        DataFrame | None: Pandas DataFrame containing the processed output when the operation
        succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.tiktokenize( text=text, encoding=encoding )

@function_tool
def preprocess_split_sentences( text: str ) -> List[str] | None:
    """Split text into sentence strings using NLTK sentence tokenization.

    Purpose:
        Applies NLTK sentence tokenization to lowercase text and returns the resulting sentence list.
        This provides sentence boundaries for chunking, cleaning, and dataset generation workflows.

    Args:
        text: Text value to process.

    Returns:
        List[ str ] | None: List of processed text values when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.split_sentences( text=text )

@function_tool
def preprocess_split_pages( filepath: str, num: int=50 ) -> List[str] | None:
    """Split a text file into page-sized text blocks.

    Purpose:
        Reads a plain-text file and splits it into page-sized blocks using form-feed characters when
        available or fixed line counts otherwise. The resulting list can be used for page- level
        cleaning and analysis.

    Args:
        filepath: Path to the local source file.
        num: Number of lines used as the fallback page boundary.

    Returns:
        List[ str ] | None: List of processed text values when the operation succeeds.

    Raises:
        FileNotFoundError: If a required local file or matched path does not exist.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.split_pages( filepath=filepath, num=num )

@function_tool
def preprocess_split_paragraphs( filepath: str ) -> DataFrame | None:
    """Read a text file and return paragraph-like text blocks as tabular data.

    Purpose:
        Reads a text file and converts separated text blocks into a pandas DataFrame. The fallback
        Latin-1 branch preserves the ability to process files that fail UTF-8 decoding.

    Args:
        filepath: Path to the local source file.

    Returns:
        DataFrame | None: Pandas DataFrame containing the processed output when the operation
        succeeds.

    Raises:
        FileNotFoundError: If a required local file or matched path does not exist.
    """
    instance = TextParser( )
    return instance.split_paragraphs( filepath=filepath )

@function_tool
def preprocess_create_frequency_distribution( tokens: List[str] ) -> DataFrame | None:
    """Build a word-frequency table from a token sequence.

    Purpose:
        Counts token occurrences with NLTK frequency distribution support and returns a labeled pandas
        DataFrame. The output provides a simple word-frequency table for analysis and reporting.

    Args:
        tokens: Token sequence used by the processing operation.

    Returns:
        DataFrame | None: Pandas DataFrame containing the processed output when the operation
        succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.create_frequency_distribution( tokens=tokens )

@function_tool
def preprocess_create_vocabulary( tokens: List[str] ) -> Series | None:
    """Extract the vocabulary column from a token-frequency table.

    Purpose:
        Counts token occurrences and returns the unique token column as a pandas Series. This gives
        downstream routines a vocabulary list derived from the active token stream.

    Args:
        tokens: Token sequence used by the processing operation.

    Returns:
        Series | None: Pandas Series containing the processed output when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.create_vocabulary( tokens=tokens )

@function_tool
def preprocess_create_wordbag( tokens: List[str] ) -> DataFrame | None:
    """Build a bag-of-words table from a token sequence.

    Purpose:
        Builds a bag-of-words representation by extracting unique terms from the token frequency
        distribution. The returned DataFrame supports simple vocabulary inspection and feature
        preparation.

    Args:
        tokens: Token sequence used by the processing operation.

    Returns:
        DataFrame | None: Pandas DataFrame containing the processed output when the operation
        succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.create_wordbag( tokens=tokens )

@function_tool
def preprocess_create_vectors( tokens: List[str] ) -> DataFrame | None:
    """Create TF-IDF vectors for token values.

    Purpose:
        Builds one-token documents, fits a TF-IDF vectorizer, and maps each token to its vector
        representation. This supplies lightweight vector features for lexical comparison workflows.

    Args:
        tokens: Token sequence used by the processing operation.

    Returns:
        DataFrame | None: Pandas DataFrame containing the processed output when the operation
        succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.create_vectors( tokens=tokens )

@function_tool
def preprocess_clean_file( filepath: str ) -> str | None:
    """Apply the standard Fonky text-cleaning pipeline to a single file.

    Purpose:
        Runs a single file through the parser cleaning pipeline, including whitespace normalization,
        encoding cleanup, symbol removal, fragment filtering, lemmatization, and stop-word removal.
        The method returns the cleaned text instead of writing a file.

    Args:
        filepath: Path to the local source file.

    Returns:
        str | None: Processed text value when the operation succeeds.

    Raises:
        FileNotFoundError: If a required local file or matched path does not exist.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.clean_file( filepath=filepath )

@function_tool
def preprocess_clean_files( source: str, destination: str ) -> None:
    """Apply the standard Fonky text-cleaning pipeline to every file in a directory.

    Purpose:
        Processes every file in a source directory through the standard cleaning pipeline and writes
        cleaned text to a destination directory. This supports batch preparation of corpora before
        chunking or dataset creation.

    Args:
        source: Directory containing source text files.
        destination: Directory where generated output files are written.

    Returns:
        None: The operation completes without producing a return value.

    Raises:
        FileNotFoundError: If a required local file or matched path does not exist.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.clean_files( source=source, destination=destination )

@function_tool
def preprocess_chunk_files( source: str, destination: str ) -> None:
    """Split text files into sentence chunks and write chunked output files.

    Purpose:
        Reads each file in a source directory, splits text into sentences, and writes the resulting
        sentence sequence to matching output files. This prepares cleaned corpora for chunk-based
        downstream workflows.

    Args:
        source: Directory containing source text files.
        destination: Directory where generated output files are written.

    Returns:
        None: The operation completes without producing a return value.

    Raises:
        FileNotFoundError: If a required local file or matched path does not exist.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.chunk_files( source=source, destination=destination )

@function_tool
def preprocess_chunk_data( filepath: str, size: int=10 ) -> DataFrame | None:
    """Chunk a single text file into fixed-size word groups represented as tabular data.

    Purpose:
        Reads a single text file, filters recognized English alphabetic tokens, groups them into
        fixed-size chunks, and returns the chunk rows as a DataFrame. This provides a compact dataset-
        ready representation of token groups.

    Args:
        filepath: Path to the local source file.
        size: Maximum number of tokens or sentences grouped into each chunk.

    Returns:
        DataFrame | None: Pandas DataFrame containing the processed output when the operation
        succeeds.

    Raises:
        FileNotFoundError: If a required local file or matched path does not exist.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.chunk_data( filepath=filepath, size=size )

@function_tool
def preprocess_chunk_datasets( source: str, destination: str, size: int=10 ) -> DataFrame:
    """Clean and chunk a directory of text files into spreadsheet datasets.

    Purpose:
        Processes all text files in a directory through cleaning, tokenization, fixed-size chunking,
        and Excel export. This creates spreadsheet datasets suitable for review, labeling, or later
        ingestion.

    Args:
        source: Directory containing source text files.
        destination: Directory where generated output files are written.
        size: Maximum number of tokens or sentences grouped into each chunk.

    Returns:
        DataFrame: Pandas DataFrame containing the processed output.

    Raises:
        FileNotFoundError: If a required local file or matched path does not exist.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.chunk_datasets( source=source, destination=destination, size=size )

@function_tool
def preprocess_convert_jsonl( source: str, destination: str, size: int=10 ) -> None:
    """Convert text files into line-oriented JSON-like chunk output.

    Purpose:
        Splits text files into fixed-size token groups and writes each group using a JSON-like line-
        oriented representation. This supports quick conversion of raw text corpora into chunked
        training or testing artifacts.

    Args:
        source: Directory containing source text files.
        destination: Directory where generated output files are written.
        size: Maximum number of tokens or sentences grouped into each chunk.

    Returns:
        None: The operation completes without producing a return value.

    Raises:
        FileNotFoundError: If a required local file or matched path does not exist.
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.convert_jsonl( source=source, destination=destination, size=size )

@function_tool
def preprocess_encode_sentences( tokens: List[str], model: str='all-MiniLM-L6-v2' ) -> Tuple[List[str], np.ndarray]:
    """Generate sentence-transformer embeddings for normalized token values.

    Purpose:
        Lemmatizes token values and encodes them with a SentenceTransformer model. The returned tuple
        pairs token text with a NumPy embedding matrix for semantic-search workflows.

    Args:
        tokens: Token sequence used by the processing operation.
        model: Sentence-transformer model used to encode the query or token sequence.

    Returns:
        Tuple[ List[ str ], np.ndarray ]: Token values paired with the generated embedding matrix.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = TextParser( )
    return instance.encode_sentences( tokens=tokens, model=model )

@function_tool
def nltk_word_tokenizer( text: str ) -> List[str] | None:
    """Tokenize text into lowercased word tokens.

    Purpose:
        Lowercases text and tokenizes it into word tokens with NLTK. The resulting list is also stored
        on the parser instance for reuse by later NLTK operations.

    Args:
        text: Text value to process.

    Returns:
        List[ str ] | None: List of processed text values when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = NltkParser( )
    return instance.word_tokenizer( text=text )

@function_tool
def nltk_sentence_tokenizer( text: str ) -> List[str] | None:
    """Tokenize text into lowercased sentence strings.

    Purpose:
        Lowercases text and tokenizes it into sentence strings with NLTK. The resulting sentences are
        stored on the parser instance and returned to the caller.

    Args:
        text: Text value to process.

    Returns:
        List[ str ] | None: List of processed text values when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = NltkParser( )
    return instance.sentence_tokenizer( text=text )

@function_tool
def nltk_word_stemmer( text: str ) -> List[str] | None:
    """Stem lowercased word tokens with the configured Porter stemmer.

    Purpose:
        Lowercases text, tokenizes it, and applies Porter stemming to each non-empty token. This
        produces stemmed tokens for lexical normalization workflows.

    Args:
        text: Text value to process.

    Returns:
        List[ str ] | None: List of processed text values when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = NltkParser( )
    return instance.word_stemmer( text=text )

@function_tool
def nltk_word_lemmatizer( text: str ) -> List[str] | None:
    """Lemmatize lowercased word tokens with the configured WordNet lemmatizer.

    Purpose:
        Lowercases text, tokenizes it, and applies WordNet lemmatization to each non-empty token. This
        produces normalized lexical forms suitable for downstream analysis.

    Args:
        text: Text value to process.

    Returns:
        List[ str ] | None: List of processed text values when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = NltkParser( )
    return instance.word_lemmatizer( text=text )

@function_tool
def nltk_pos_tagger( text: str ) -> List[Tuple[str, str]] | None:
    """Assign part-of-speech tags to lowercased word tokens.

    Purpose:
        Lowercases and tokenizes text, then assigns NLTK part-of-speech tags to each token. The tagged
        sequence is stored on the instance and returned for syntactic analysis.

    Args:
        text: Text value to process.

    Returns:
        List[ Tuple[ str, str ] ] | None: List of text and label tuples when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = NltkParser( )
    return instance.pos_tagger( text=text )

@function_tool
def nltk_named_entity_recognition( text: str ) -> List[Tuple[str, str]] | None:
    """Extract named-entity text and entity labels from tagged tokens.

    Purpose:
        Lowercases text, tokenizes and tags it, then applies NLTK named-entity chunking. Entity text
        and labels are collected into tuples for downstream review or extraction workflows.

    Args:
        text: Text value to process.

    Returns:
        List[ Tuple[ str, str ] ] | None: List of text and label tuples when the operation succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = NltkParser( )
    return instance.named_entity_recognition( text=text )

@function_tool
def nltk_chunk_words( text: str, size: int=5 ) -> DataFrame | None:
    """Group word tokens into fixed-size chunks and return them as tabular data.

    Purpose:
        Tokenizes lowercase text into words, groups the tokens into fixed-size chunks, and returns a
        DataFrame of chunk strings. This provides a simple word-level chunking utility for downstream
        vector or dataset generation.

    Args:
        text: Text value to process.
        size: Maximum number of tokens or sentences grouped into each chunk.

    Returns:
        DataFrame | None: Pandas DataFrame containing the processed output when the operation
        succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = NltkParser( )
    return instance.chunk_words( text=text, size=size )

@function_tool
def nltk_chunk_sentences( text: str, size: int=15 ) -> DataFrame | None:
    """Group sentence tokens into fixed-size chunks and return them as tabular data.

    Purpose:
        Tokenizes lowercase text into sentences, groups the sentences into fixed-size chunks, and
        returns a DataFrame of chunk strings. This provides a sentence-level chunking utility for
        review or dataset preparation.

    Args:
        text: Text value to process.
        size: Maximum number of tokens or sentences grouped into each chunk.

    Returns:
        DataFrame | None: Pandas DataFrame containing the processed output when the operation
        succeeds.

    Raises:
        Error: If the implementation wraps a provider, parsing, filesystem, or processing failure in the
            project error type.
    """
    instance = NltkParser( )
    return instance.chunk_sentences( text=text, size=size )

@function_tool
def preprocess_semantic_search( query: str, tokens: List[ str ],
        model: str='all-MiniLM-L6-v2', top: int=5 ) -> List[ Tuple[ str, float ] ]:
    """Search token content by semantic similarity.

    Purpose:
        Creates sentence embeddings internally and returns the highest-scoring token matches for
        the supplied query. The wrapper keeps NumPy arrays and SentenceTransformer instances out
        of the agent-facing JSON schema.

    Args:
        query: Natural-language query used for semantic matching.
        tokens: Text values searched for semantic similarity.
        model: Sentence-transformer model name used to create embeddings.
        top: Maximum number of matches to return.

    Returns:
        List[Tuple[str, float]]: Highest-scoring text values and similarity scores.
    """
    instance = TextParser( )
    encoded = instance.encode_sentences( tokens=tokens, model=model )
    sentences, embeddings = encoded
    transformer = SentenceTransformer( model )
    return instance.semantic_search( query=query, tokens=sentences, embeddings=embeddings,
        model=transformer, top=top )

# ==========================================================================================
# PUBLIC EXPORTS
# ==========================================================================================

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
	'preprocess_load_text',
	'preprocess_collapse_whitespace',
	'preprocess_remove_punctuation',
	'preprocess_normalize_text',
	'preprocess_remove_errors',
	'preprocess_remove_fragments',
	'preprocess_remove_symbols',
	'preprocess_remove_html',
	'preprocess_remove_xml',
	'preprocess_remove_markdown',
	'preprocess_remove_stopwords',
	'preprocess_remove_encodings',
	'preprocess_remove_headers',
	'preprocess_remove_numbers',
	'preprocess_remove_numerals',
	'preprocess_remove_images',
	'preprocess_tiktokenize',
	'preprocess_split_sentences',
	'preprocess_split_pages',
	'preprocess_split_paragraphs',
	'preprocess_create_frequency_distribution',
	'preprocess_create_vocabulary',
	'preprocess_create_wordbag',
	'preprocess_create_vectors',
	'preprocess_clean_file',
	'preprocess_clean_files',
	'preprocess_chunk_files',
	'preprocess_chunk_data',
	'preprocess_chunk_datasets',
	'preprocess_convert_jsonl',
	'preprocess_encode_sentences',
	'nltk_word_tokenizer',
	'nltk_sentence_tokenizer',
	'nltk_word_stemmer',
	'nltk_word_lemmatizer',
	'nltk_pos_tagger',
	'nltk_named_entity_recognition',
	'nltk_chunk_words',
	'nltk_chunk_sentences',
	'preprocess_semantic_search',
]
