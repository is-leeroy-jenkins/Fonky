'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                fetchers.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file='fetchers.py' company='Terry D. Eppler'>

	     Foo is a python framework for web scraping information into ML pipelines.
	     Copyright ©  2025  Terry Eppler

     Permission is hereby granted, free of charge, to any person obtaining a copy
     of this software and associated documentation files (the “Software”),
     to deal in the Software without restriction,
     including without limitation the rights to use,
     copy, modify, merge, publish, distribute, sublicense,
     and/or sell copies of the Software,
     and to permit persons to whom the Software is furnished to do so,
     subject to the following conditions:

     The above copyright notice and this permission notice shall be included in all
     copies or substantial portions of the Software.

     THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
     INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT.
     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
     DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
     ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
     DEALINGS IN THE SOFTWARE.

     You can contact me at:  terryeppler@gmail.com or eppler.terry@epa.gov

  </copyright>
  <summary>
    fetchers.py
  </summary>
  ******************************************************************************************
  '''
from __future__ import annotations

import base64
import datetime as dt
import io
import re
import os
import urllib.parse
from pathlib import Path
import pandas as pd
from typing import Any, Dict, Optional, Pattern, List, Tuple
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import requests
from PIL.Image import Image
from astropy.coordinates import SkyCoord
from astropy.table import Table
from astropy import units as u
from astroquery.simbad import Simbad
from bs4 import BeautifulSoup
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import crawl4ai
import csv
from google import genai
from grokipedia_api import GrokipediaClient
from langchain_community.retrievers import ArxivRetriever, WikipediaRetriever
from langchain_core.documents import Document
from langchain_core.tools import Tool
from langchain_googledrive.retrievers import GoogleDriveRetriever
from playwright.sync_api import sync_playwright
from owslib.wms import WebMapService
from requests import Response
from sscws.sscws import SscWs
import time
import config as cfg
from boogr import Error
from core import Result
import xml.etree.ElementTree as ET

def throw_if( name: str, value: object ) -> None:
	"""Throw if.
	
	Purpose:
		Validates that a required argument is present before a fetcher operation continues. The
		function raises a ValueError for missing or empty required values so callers fail early
		with a clear argument name.
	
	Args:
		name (str): name value used by the throw if operation.
		value (object): value value used by the throw if operation.
	
	Raises:
		ValueError: Raised when a required argument is None or an empty string."""
	if value is None:
		raise ValueError( f'Argument "{name}" cannot be None.' )
	
	if isinstance( value, str ) and not value.strip( ):
		raise ValueError( f'Argument "{name}" cannot be empty.' )

def encode_image( path: str ) -> str:
	"""Encode image.
	
	Purpose:
		Reads an image file from disk and returns a base64-encoded string representation of its
		bytes. The function validates that a path was supplied before reading the file so image
		payloads can be embedded in request or tool workflows.
	
	Args:
		path (str): path value used by the encode image operation.
	
	Returns:
		str: Base64-encoded image data.
	
	Raises:
		Exception: Raised when validation or provider-specific failure conditions are
			encountered."""
	if path is None:
		raise ValueError( f"Argument '{path}' cannot be empty!" )
	else:
		data = Path( path ).read_bytes( )
		return base64.b64encode( data ).decode( "utf-8" )

class Fetcher:
	"""Fetcher fetcher.
	
	Purpose:
		Coordinates base fetcher operations within Fonky. The class stores provider
		configuration, request parameters, response payloads, and normalized result state so
		callers can access the service through a consistent fetcher interface.
	
	Attributes:
		timeout (Optional[int]): timeout state retained by the instance.
		headers (Optional[Dict[str, Any]]): headers state retained by the instance.
		response (Optional[Response]): response state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		result (Optional[Result]): result state retained by the instance.
		query (Optional[str]): query state retained by the instance."""
	timeout: Optional[ int ]
	headers: Optional[ Dict[ str, Any ] ]
	response: Optional[ Response ]
	url: Optional[ str ]
	result: Optional[ Result ]
	query: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize Fetcher.
		
		Purpose:
			Initializes the Fetcher instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		self.timeout = None
		self.headers = None
		self.response = None
		self.url = None
		self.result = None
		self.query = None
	
	def __dir__( self ) -> list[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			list[str]: Ordered public attribute and method names exposed by the object."""
		return [ 'timeout',
		         'headers',
		         'response',
		         'url',
		         'result',
		         'query',
		         'fetch' ]
	
	def fetch( self, query: str, url: str, time: int = 10 ) -> Result | None:
		"""Fetch base fetcher operations.
		
		Purpose:
			Retrieves base fetcher operations using validated arguments and the stored Fetcher
			runtime configuration. The method assembles request parameters, executes the provider
			call or dispatches to a specialized helper, records response state when applicable, and
			returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			query (str): Search text, lookup value, or provider query submitted by the caller.
			url (str): URL or URI value used as the request or parsing source.
			time (int): Request timeout in seconds.
		
		Returns:
			Result | None: Normalized provider response, result payload, or document collection
				returned by the operation.
		
		Raises:
			Exception: Raised when validation or provider-specific failure conditions are
				encountered."""
		raise NotImplementedError( 'Must be implemented by a subclass.' )

class WebFetcher( Fetcher ):
	"""Web Fetcher fetcher.
	
	Purpose:
		Coordinates HTTP web page retrieval and HTML extraction within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		soup (Optional[BeautifulSoup]): soup state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		html (Optional[str]): HTML state retained by the instance.
		text (Optional[str]): text state retained by the instance.
		source_url (Optional[str]): source URL state retained by the instance.
		source_html (Optional[str]): source HTML state retained by the instance.
		selected_methods (Optional[List[str]]): selected methods state retained by the instance.
		re_tag (Optional[Pattern]): re tag state retained by the instance.
		re_ws (Optional[Pattern]): re ws state retained by the instance.
		response (Optional[Response]): response state retained by the instance.
		result (Optional[Result]): result state retained by the instance.
		headers (Optional[Dict[str, Any]]): headers state retained by the instance.
		timeout (Optional[int]): timeout state retained by the instance."""
	soup: Optional[ BeautifulSoup ]
	agents: Optional[ str ]
	url: Optional[ str ]
	html: Optional[ str ]
	text: Optional[ str ]
	source_url: Optional[ str ]
	source_html: Optional[ str ]
	selected_methods: Optional[ List[ str ] ]
	re_tag: Optional[ Pattern ]
	re_ws: Optional[ Pattern ]
	response: Optional[ Response ]
	result: Optional[ Result ]
	headers: Optional[ Dict[ str, Any ] ]
	timeout: Optional[ int ]
	
	def __init__( self ) -> None:
		"""Initialize WebFetcher.
		
		Purpose:
			Initializes the WebFetcher instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.timeout = 10
		self.re_tag = re.compile( r'<[^>]+>' )
		self.re_ws = re.compile( r'\s+' )
		self.url = None
		self.html = None
		self.text = None
		self.source_url = None
		self.source_html = None
		self.selected_methods = None
		self.response = None
		self.result = None
		self.soup = None
		self.headers = { }
		self.agents = cfg.AGENTS
		
		self.headers[ 'User-Agent' ] = self.agents
		self.headers[ 'Accept' ] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'agents',
				'url',
				'html',
				'text',
				'source_url',
				'source_html',
				'selected_methods',
				'timeout',
				'headers',
				'response',
				'result',
				'soup',
				're_tag',
				're_ws',
				'fetch',
				'html_to_text',
				'coerce_items',
				'extract_title',
				'truncate_text',
				'normalize_url',
				'same_domain',
				'extract_links',
				'extract_structured_data',
				'scrape_headings',
				'scrape_paragraphs',
				'scrape_lists',
				'scrape_tables',
				'scrape_articles',
				'scrape_sections',
				'scrape_divisions',
				'scrape_blockquotes',
				'scrape_hyperlinks',
				'scrape_images',
				'create_schema'
		]
	
	def fetch( self, url: str, time: int = 10 ) -> Result | None:
		"""Fetch HTTP web page retrieval and HTML extraction.
		
		Purpose:
			Retrieves HTTP web page retrieval and HTML extraction using validated arguments and the
			stored WebFetcher runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			url (str): URL or URI value used as the request or parsing source.
			time (int): Request timeout in seconds.
		
		Returns:
			Result | None: Normalized provider response, result payload, or document collection
				returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'url', url )
			throw_if( 'time', time )
			self.url = str( url ).strip( )
			self.timeout = int( time )
			self.response = requests.get( url=self.url, headers=self.headers,
				timeout=self.timeout )
			self.response.raise_for_status( )
			self.html = self.response.text or ''
			self.soup = BeautifulSoup( self.html, 'html.parser' )
			self.result = Result( self.response )
			
			return self.result
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'fetch( self, *args, **kwargs ) -> Result | None'
			raise exception
	
	def html_to_text( self, html: str ) -> str:
		"""HTML to text.
		
		Purpose:
			Converts raw HTML into compact plain text by removing scripts, styles, markup, and
			repeated whitespace. The method prepares fetched web content for search, summarization,
			display, or downstream text processing.
		
		Args:
			html (str): HTML value used by the html to text operation.
		
		Returns:
			str: Plain-text representation of the supplied HTML content.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'html', html )
			self.source_html = str( html )
			self.text = re.sub( r'<script[\s\S]*?</script>', ' ', self.source_html,
				flags=re.IGNORECASE )
			self.text = re.sub( r'<style[\s\S]*?</style>', ' ', self.text,
				flags=re.IGNORECASE )
			self.text = re.sub( r'</?(p|div|br|li|h[1-6]|section|article|blockquote)[^>]*>', '\n',
				self.text, flags=re.IGNORECASE )
			self.text = re.sub( self.re_tag, ' ', self.text )
			self.text = re.sub( self.re_ws, ' ', self.text ).strip( )
			
			return self.text
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'html_to_text( self, *args, **kwargs ) -> str'
			raise exception
	
	def coerce_items( self, value: Any ) -> List[ str ]:
		"""Coerce items.
		
		Purpose:
			Coerces items into a predictable Python representation for downstream handling. The
			method prefers structured data when available and falls back to text or simple
			containers when the provider response cannot be represented more specifically.
		
		Args:
			value (object): value value used by the coerce items operation.
		
		Returns:
			List[str]: Result produced by the operation."""
		if value is None:
			return [ ]
		
		if isinstance( value, list ):
			return [
					str( item )
					for item in value
					if item is not None
			]
		
		return [
				str( value )
		]
	
	def extract_title( self, html: str ) -> str:
		"""Extract title.
		
		Purpose:
			Extracts title from the supplied source content and normalizes the result for downstream
			use. The method stores intermediate parsing state when needed and returns only the
			compact value required by callers.
		
		Args:
			html (str): HTML value used by the extract title operation.
		
		Returns:
			str: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'html', html )
			self.source_html = str( html )
			self.soup = BeautifulSoup( self.source_html, 'html.parser' )
			if self.soup.title and self.soup.title.string:
				return re.sub( r'\s+', ' ', self.soup.title.string ).strip( )
			
			match = re.search(
				r'<title[^>]*>(.*?)</title>',
				self.source_html,
				flags=re.IGNORECASE | re.DOTALL
			)
			
			if not match:
				return ''
			
			return re.sub( r'\s+', ' ', match.group( 1 ) ).strip( )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'extract_title( self, *args, **kwargs ) -> str'
			raise exception
	
	def truncate_text( self, text: str, limit: int = 12000 ) -> str:
		"""Truncate text.
		
		Purpose:
			Performs the truncate text operation for HTTP web page retrieval and HTML extraction.
			The method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			text (str): text value used by the truncate text operation.
			limit (int): limit value used by the truncate text operation.
		
		Returns:
			str: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'text', text )
			throw_if( 'limit', limit )
			self.text = str( text )
			self.limit = int( limit )
			if len( self.text ) <= self.limit:
				return self.text
			
			return self.text[ : self.limit ] + '\n\n... [truncated]'
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'truncate_text( self, *args, **kwargs ) -> str'
			raise exception
	
	def normalize_url( self, base_url: str, href: str ) -> str:
		"""Normalize url.
		
		Purpose:
			Converts url into the canonical format expected by the WebFetcher request workflow. The
			method standardizes caller input before it is used in endpoint paths, query parameters,
			filters, or response processing.
		
		Args:
			base_url (str): URL or URI value used as the request or parsing source.
			href (str): href value used by the normalize url operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing."""
		try:
			throw_if( 'base_url', base_url )
			throw_if( 'href', href )
			
			self.source_url = str( base_url ).strip( )
			self.href = str( href ).strip( )
			
			if self.href.startswith( ('mailto:', 'tel:', 'javascript:', '#') ):
				return ''
			
			self.absolute_url = urllib.parse.urljoin( self.source_url, self.href )
			self.parsed_url = urllib.parse.urlparse( self.absolute_url )
			
			if self.parsed_url.scheme not in ('http', 'https'):
				return ''
			
			if not self.parsed_url.netloc:
				return ''
			
			self.normalized_path = self.parsed_url.path or '/'
			self.normalized_url = self.parsed_url._replace(
				path=self.normalized_path,
				fragment='' )
			
			return self.normalized_url.geturl( )
		
		except Exception:
			return ''
	
	def same_domain( self, left_url: str, right_url: str ) -> bool:
		"""Same domain.
		
		Purpose:
			Performs the same domain operation for HTTP web page retrieval and HTML extraction. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			left_url (str): left URL value used by the same domain operation.
			right_url (str): right URL value used by the same domain operation.
		
		Returns:
			bool: Result produced by the operation."""
		try:
			throw_if( 'left_url', left_url )
			throw_if( 'right_url', right_url )
			
			self.left_url = str( left_url ).strip( )
			self.right_url = str( right_url ).strip( )
			self.left_host = urllib.parse.urlparse( self.left_url ).netloc.lower( )
			self.right_host = urllib.parse.urlparse( self.right_url ).netloc.lower( )
			
			return bool( self.left_host ) and self.left_host == self.right_host
		
		except Exception:
			return False
	
	def extract_links( self, base_url: str, html: str ) -> List[ str ]:
		"""Extract links.
		
		Purpose:
			Extracts links from the supplied source content and normalizes the result for downstream
			use. The method stores intermediate parsing state when needed and returns only the
			compact value required by callers.
		
		Args:
			base_url (str): URL or URI value used as the request or parsing source.
			html (str): HTML value used by the extract links operation.
		
		Returns:
			List[str]: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'base_url', base_url )
			throw_if( 'html', html )
			
			self.source_url = str( base_url ).strip( )
			self.source_html = str( html )
			self.soup = BeautifulSoup( self.source_html, 'html.parser' )
			self.results = [ ]
			self.seen = set( )
			
			for tag in self.soup.find_all( 'a', href=True ):
				self.candidate = self.normalize_url(
					self.source_url,
					tag.get( 'href', '' )
				)
				
				if self.candidate and self.candidate not in self.seen:
					self.seen.add( self.candidate )
					self.results.append( self.candidate )
			
			return self.results
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'extract_links( self, *args, **kwargs ) -> List[ str ]'
			raise exception
	
	def extract_structured_data( self, url: str, html: str,
			selected_methods: Optional[ List[ str ] ] = None ) -> Dict[ str, List[ str ] ]:
		"""Extract structured data.
		
		Purpose:
			Extracts structured data from the supplied source content and normalizes the result for
			downstream use. The method stores intermediate parsing state when needed and returns
			only the compact value required by callers.
		
		Args:
			url (str): URL or URI value used as the request or parsing source.
			html (str): HTML value used by the extract structured data operation.
			selected_methods (Optional[List[str]]): selected methods value used by the extract
				structured data operation.
		
		Returns:
			Dict[str, List[str]]: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'url', url )
			throw_if( 'html', html )
			self.source_url = str( url ).strip( )
			self.source_html = str( html )
			self.selected_methods = selected_methods or [ ]
			self.results = { }
			self.soup = BeautifulSoup( self.source_html, 'html.parser' )
			self.registry = {
					'scrape_headings': (
							'Headings',
							lambda: [
									tag.get_text( ' ', strip=True )
									for tag in self.soup.find_all(
										[ 'h1', 'h2', 'h3', 'h4', 'h5', 'h6' ]
									)
									if tag.get_text( ' ', strip=True )
							]
					),
					'scrape_paragraphs': (
							'Paragraphs',
							lambda: [
									tag.get_text( ' ', strip=True )
									for tag in self.soup.find_all( 'p' )
									if tag.get_text( ' ', strip=True )
							]
					),
					'scrape_lists': (
							'Lists',
							lambda: [
									tag.get_text( ' ', strip=True )
									for tag in self.soup.find_all( 'li' )
									if tag.get_text( ' ', strip=True )
							]
					),
					'scrape_tables': (
							'Tables',
							lambda: [
									cell.get_text( ' ', strip=True )
									for table in self.soup.find_all( 'table' )
									for row in table.find_all( 'tr' )
									for cell in row.find_all( [ 'td', 'th' ] )
									if cell.get_text( ' ', strip=True )
							]
					),
					'scrape_articles': (
							'Articles',
							lambda: [
									tag.get_text( ' ', strip=True )
									for tag in self.soup.find_all( 'article' )
									if tag.get_text( ' ', strip=True )
							]
					),
					'scrape_sections': (
							'Sections',
							lambda: [
									tag.get_text( ' ', strip=True )
									for tag in self.soup.find_all( 'section' )
									if tag.get_text( ' ', strip=True )
							]
					),
					'scrape_divisions': (
							'Divisions',
							lambda: [
									tag.get_text( ' ', strip=True )
									for tag in self.soup.find_all( 'div' )
									if tag.get_text( ' ', strip=True )
							]
					),
					'scrape_blockquotes': (
							'Blockquotes',
							lambda: [
									tag.get_text( ' ', strip=True )
									for tag in self.soup.find_all( 'blockquote' )
									if tag.get_text( ' ', strip=True )
							]
					),
					'scrape_hyperlinks': (
							'Hyperlinks',
							lambda: [
									self.normalize_url(
										self.source_url,
										tag.get( 'href', '' )
									)
									for tag in self.soup.find_all( 'a', href=True )
									if self.normalize_url(
										self.source_url,
										tag.get( 'href', '' )
									)
							]
					),
					'scrape_images': (
							'Images',
							lambda: [
									self.normalize_url(
										self.source_url,
										tag.get( 'src', '' )
									)
									for tag in self.soup.find_all( 'img', src=True )
									if self.normalize_url(
										self.source_url,
										tag.get( 'src', '' )
									)
							]
					),
			}
			
			for self.method_name in self.selected_methods:
				if self.method_name not in self.registry:
					continue
				
				self.label, self.extractor = self.registry[ self.method_name ]
				self.values = self.coerce_items( self.extractor( ) )
				self.deduped = [ ]
				self.seen = set( )
				for self.value in self.values:
					if self.value not in self.seen:
						self.seen.add( self.value )
						self.deduped.append( self.value )
				
				self.results[ self.label ] = self.deduped
			
			return self.results
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'extract_structured_data( self, *args, **kwargs ) -> Dict[ str, List[ str ] ]'
			raise exception
	
	def scrape_paragraphs( self, uri: str ) -> List[ str ] | None:
		"""Scrape paragraphs.
		
		Purpose:
			Scrapes paragraphs from a fetched HTML document through the configured web retrieval
			path. The method validates the requested URI, obtains page content, delegates structured
			extraction, and returns normalized text or link values.
		
		Args:
			uri (str): URL or URI value used as the request or parsing source.
		
		Returns:
			List[str] | None: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'uri', uri )
			self.url = str( uri ).strip( )
			self.fetch( self.url, time=int( self.timeout or 10 ) )
			return self.extract_structured_data(
				self.url, self.html or '', [ 'scrape_paragraphs' ] ).get( 'Paragraphs', [ ] )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'scrape_paragraphs( self, *args, **kwargs ) -> List[ str ] | None'
			raise exception
	
	def scrape_lists( self, uri: str ) -> List[ str ] | None:
		"""Scrape lists.
		
		Purpose:
			Scrapes lists from a fetched HTML document through the configured web retrieval path.
			The method validates the requested URI, obtains page content, delegates structured
			extraction, and returns normalized text or link values.
		
		Args:
			uri (str): URL or URI value used as the request or parsing source.
		
		Returns:
			List[str] | None: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'uri', uri )
			self.url = str( uri ).strip( )
			self.fetch( self.url, time=int( self.timeout or 10 ) )
			return self.extract_structured_data(
				self.url, self.html or '', [ 'scrape_lists' ] ).get( 'Lists', [ ] )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'scrape_lists( self, *args, **kwargs ) -> List[ str ] | None'
			raise exception
	
	def scrape_tables( self, uri: str ) -> List[ str ] | None:
		"""Scrape tables.
		
		Purpose:
			Scrapes tables from a fetched HTML document through the configured web retrieval path.
			The method validates the requested URI, obtains page content, delegates structured
			extraction, and returns normalized text or link values.
		
		Args:
			uri (str): URL or URI value used as the request or parsing source.
		
		Returns:
			List[str] | None: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'uri', uri )
			self.url = str( uri ).strip( )
			self.fetch( self.url, time=int( self.timeout or 10 ) )
			return self.extract_structured_data(
				self.url, self.html or '', [ 'scrape_tables' ] ).get( 'Tables', [ ] )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'scrape_tables( self, *args, **kwargs ) -> List[ str ] | None'
			raise exception
	
	def scrape_articles( self, uri: str ) -> List[ str ] | None:
		"""Scrape articles.
		
		Purpose:
			Scrapes articles from a fetched HTML document through the configured web retrieval path.
			The method validates the requested URI, obtains page content, delegates structured
			extraction, and returns normalized text or link values.
		
		Args:
			uri (str): URL or URI value used as the request or parsing source.
		
		Returns:
			List[str] | None: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'uri', uri )
			self.url = str( uri ).strip( )
			self.fetch( self.url, time=int( self.timeout or 10 ) )
			return self.extract_structured_data(
				self.url, self.html or '', [ 'scrape_articles' ] ).get( 'Articles', [ ] )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'scrape_articles( self, *args, **kwargs ) -> List[ str ] | None'
			raise exception
	
	def scrape_headings( self, uri: str ) -> List[ str ] | None:
		"""Scrape headings.
		
		Purpose:
			Scrapes headings from a fetched HTML document through the configured web retrieval path.
			The method validates the requested URI, obtains page content, delegates structured
			extraction, and returns normalized text or link values.
		
		Args:
			uri (str): URL or URI value used as the request or parsing source.
		
		Returns:
			List[str] | None: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'uri', uri )
			
			self.url = str( uri ).strip( )
			self.fetch( self.url, time=int( self.timeout or 10 ) )
			return self.extract_structured_data(
				self.url, self.html or '', [ 'scrape_headings' ] ).get( 'Headings', [ ] )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'scrape_headings( self, *args, **kwargs ) -> List[ str ] | None'
			raise exception
	
	def scrape_divisions( self, uri: str ) -> List[ str ] | None:
		"""Scrape divisions.
		
		Purpose:
			Scrapes divisions from a fetched HTML document through the configured web retrieval
			path. The method validates the requested URI, obtains page content, delegates structured
			extraction, and returns normalized text or link values.
		
		Args:
			uri (str): URL or URI value used as the request or parsing source.
		
		Returns:
			List[str] | None: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'uri', uri )
			self.url = str( uri ).strip( )
			self.fetch( self.url, time=int( self.timeout or 10 ) )
			return self.extract_structured_data(
				self.url, self.html or '', [ 'scrape_divisions' ] ).get( 'Divisions', [ ] )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'scrape_divisions( self, *args, **kwargs ) -> List[ str ] | None'
			raise exception
	
	def scrape_sections( self, uri: str ) -> List[ str ] | None:
		"""Scrape sections.
		
		Purpose:
			Scrapes sections from a fetched HTML document through the configured web retrieval path.
			The method validates the requested URI, obtains page content, delegates structured
			extraction, and returns normalized text or link values.
		
		Args:
			uri (str): URL or URI value used as the request or parsing source.
		
		Returns:
			List[str] | None: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'uri', uri )
			
			self.url = str( uri ).strip( )
			self.fetch( self.url, time=int( self.timeout or 10 ) )
			return self.extract_structured_data(
				self.url, self.html or '', [ 'scrape_sections' ] ).get( 'Sections', [ ] )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'scrape_sections( self, *args, **kwargs ) -> List[ str ] | None'
			raise exception
	
	def scrape_blockquotes( self, uri: str ) -> List[ str ] | None:
		"""Scrape blockquotes.
		
		Purpose:
			Scrapes blockquotes from a fetched HTML document through the configured web retrieval
			path. The method validates the requested URI, obtains page content, delegates structured
			extraction, and returns normalized text or link values.
		
		Args:
			uri (str): URL or URI value used as the request or parsing source.
		
		Returns:
			List[str] | None: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'uri', uri )
			self.url = str( uri ).strip( )
			self.fetch( self.url, time=int( self.timeout or 10 ) )
			return self.extract_structured_data(
				self.url, self.html or '', [ 'scrape_blockquotes' ] ).get( 'Blockquotes', [ ] )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'scrape_blockquotes( self, *args, **kwargs ) -> List[ str ] | None'
			raise exception
	
	def scrape_hyperlinks( self, uri: str ) -> List[ str ] | None:
		"""Scrape hyperlinks.
		
		Purpose:
			Scrapes hyperlinks from a fetched HTML document through the configured web retrieval
			path. The method validates the requested URI, obtains page content, delegates structured
			extraction, and returns normalized text or link values.
		
		Args:
			uri (str): URL or URI value used as the request or parsing source.
		
		Returns:
			List[str] | None: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'uri', uri )
			self.url = str( uri ).strip( )
			self.fetch( self.url, time=int( self.timeout or 10 ) )
			return self.extract_structured_data(
				self.url, self.html or '', [ 'scrape_hyperlinks' ] ).get( 'Hyperlinks', [ ] )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'scrape_hyperlinks( self, *args, **kwargs ) -> List[ str ] | None'
			raise exception
	
	def scrape_images( self, uri: str ) -> List[ str ] | None:
		"""Scrape images.
		
		Purpose:
			Scrapes images from a fetched HTML document through the configured web retrieval path.
			The method validates the requested URI, obtains page content, delegates structured
			extraction, and returns normalized text or link values.
		
		Args:
			uri (str): URL or URI value used as the request or parsing source.
		
		Returns:
			List[str] | None: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'uri', uri )
			self.url = str( uri ).strip( )
			self.fetch( self.url, time=int( self.timeout or 10 ) )
			return self.extract_structured_data(
				self.url, self.html or '', [ 'scrape_images' ] ).get( 'Images', [ ] )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'scrape_images( self, *args, **kwargs ) -> List[ str ] | None'
			raise exception
	
	def create_schema( self, function: str, tool: str, description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebFetcher'
			exception.method = 'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			raise exception

class WebCrawler( WebFetcher ):
	"""Web Crawler fetcher.
	
	Purpose:
		Coordinates bounded web crawling and optional browser-rendered scraping within Fonky.
		The class stores provider configuration, request parameters, response payloads, and
		normalized result state so callers can access the service through a consistent fetcher
		interface.
	
	Attributes:
		use_playwright (Optional[bool]): use playwright state retained by the instance.
		browser_context (Optional[Any]): browser context state retained by the instance.
		raw_url (Optional[str]): raw URL state retained by the instance.
		raw_html (Optional[str]): raw HTML state retained by the instance.
		pages (Optional[List[Dict[str, Any]]]): pages state retained by the instance.
		summary (Optional[Dict[str, Any]]): summary state retained by the instance.
		response (object): response state retained by the instance.
		headers (object): headers state retained by the instance."""
	use_playwright: Optional[ bool ]
	browser_context: Optional[ Any ]
	raw_url: Optional[ str ]
	raw_html: Optional[ str ]
	pages: Optional[ List[ Dict[ str, Any ] ] ]
	summary: Optional[ Dict[ str, Any ] ]
	
	def __init__( self, headers: Optional[ Dict[ str, str ] ] = None,
			use_playwright: bool = False ) -> None:
		"""Initialize WebCrawler.
		
		Purpose:
			Initializes the WebCrawler instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request.
		
		Args:
			headers (Optional[Dict[str, str]]): headers value used by the init operation.
			use_playwright (bool): use playwright value used by the init operation."""
		super( ).__init__( )
		self.browser_context = None
		self.raw_url = None
		self.raw_html = None
		self.response = None
		self.pages = [ ]
		self.summary = { }
		self.use_playwright = bool( use_playwright )
		
		if headers is not None:
			self.headers = headers
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = cfg.AGENTS
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [ 'use_playwright', 'browser_context', 'raw_url', 'raw_html', 'pages', 'summary',
		         'fetch', 'html_to_text', 'coerce_items', 'extract_title', 'truncate_text',
		         'normalize_url', 'same_domain', 'extract_links', 'extract_structured_data',
		         'render_with_playwright', 'scrape_page', 'crawl' ]
	
	def fetch( self, url: str, time: int = 10 ) -> Result | None:
		"""Fetch bounded web crawling and optional browser-rendered scraping.
		
		Purpose:
			Retrieves bounded web crawling and optional browser-rendered scraping using validated
			arguments and the stored WebCrawler runtime configuration. The method assembles request
			parameters, executes the provider call or dispatches to a specialized helper, records
			response state when applicable, and returns a normalized payload for downstream analysis
			or tool execution.
		
		Args:
			url (str): URL or URI value used as the request or parsing source.
			time (int): Request timeout in seconds.
		
		Returns:
			Result | None: Normalized provider response, result payload, or document collection
				returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'url', url )
			
			if self.use_playwright:
				self.url = str( url ).strip( )
				self.timeout = int( time )
				self.raw_url = self.url
				self.raw_html = self.render_with_playwright( self.url, timeout=self.timeout )
				self.html = self.raw_html or ''
				self.soup = BeautifulSoup( self.html, 'html.parser' )
				return None
			
			return super( ).fetch( url=url, time=time )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebCrawler'
			exception.method = 'fetch( self, url: str, time: int=10 ) -> Result | None'
			raise exception
	
	def render_with_playwright( self, url: str, timeout: int = 15 ) -> str:
		"""Render with playwright.
		
		Purpose:
			Performs the render with playwright operation for bounded web crawling and optional
			browser-rendered scraping. The method uses the class runtime state and supplied
			arguments to prepare, transform, dispatch, or package data for the broader Fonky
			fetching workflow.
		
		Args:
			url (str): URL or URI value used as the request or parsing source.
			timeout (int): Request timeout in seconds.
		
		Returns:
			str: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'url', url )
			
			with sync_playwright( ) as p:
				browser = p.chromium.launch( )
				page = browser.new_page( )
				page.goto( url, timeout=int( timeout ) * 1000 )
				page.wait_for_load_state( 'networkidle', timeout=int( timeout ) * 1000 )
				html = page.content( )
				browser.close( )
				return html
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebCrawler'
			exception.method = 'render_with_playwright( self, url: str, timeout: int=15 ) -> str'
			raise exception
	
	def scrape_page( self, url: str, include_title: bool = True, include_basic_text: bool = True,
			include_raw_html: bool = False, selected_methods: Optional[ List[ str ] ] = None,
			request_timeout: int = 10, max_bytes: int = 1000000 ) -> Dict[ str, Any ]:
		"""Scrape page.
		
		Purpose:
			Scrapes page from a fetched HTML document through the configured web retrieval path. The
			method validates the requested URI, obtains page content, delegates structured
			extraction, and returns normalized text or link values.
		
		Args:
			url (str): URL or URI value used as the request or parsing source.
			include_title (bool): include title value used by the scrape page operation.
			include_basic_text (bool): include basic text value used by the scrape page operation.
			include_raw_html (bool): include raw HTML value used by the scrape page operation.
			selected_methods (Optional[List[str]]): selected methods value used by the scrape page
				operation.
			request_timeout (int): Request timeout in seconds.
			max_bytes (int): max bytes value used by the scrape page operation.
		
		Returns:
			Dict[str, Any]: Extracted and normalized content values."""
		page_result: Dict[ str, Any ] = \
			{
					'url': url,
					'status_code': None,
					'encoding': None,
					'title': '',
					'plain_text': '',
					'raw_html': '',
					'links_discovered': [ ],
					'data': { },
					'errors': [ ],
					'content_bytes': 0,
					'truncated_by_max_bytes': False,
			}
		
		try:
			methods = selected_methods or [ ]
			self.fetch( url=url, time=int( request_timeout ) )
			raw_html = self.html or ''
			if self.response is not None:
				page_result[ 'status_code' ] = getattr( self.response, 'status_code', None )
				page_result[ 'encoding' ] = getattr( self.response, 'encoding', None )
			else:
				page_result[ 'status_code' ] = 200
				page_result[ 'encoding' ] = 'rendered'
			raw_bytes = raw_html.encode( 'utf-8', errors='ignore' )
			page_result[ 'content_bytes' ] = len( raw_bytes )
			
			if int( max_bytes ) > 0 and len( raw_bytes ) > int( max_bytes ):
				raw_html = raw_bytes[ : int( max_bytes ) ].decode( 'utf-8', errors='ignore' )
				page_result[ 'truncated_by_max_bytes' ] = True
				page_result[ 'errors' ].append(
					f'Response exceeded max bytes and was truncated to {int( max_bytes )} bytes.' )
			
			page_result[ 'links_discovered' ] = self.extract_links( url, raw_html )
			
			if include_title:
				page_result[ 'title' ] = self.extract_title( raw_html )
			
			if include_basic_text:
				try:
					page_result[ 'plain_text' ] = self.html_to_text( raw_html ) or ''
				except Exception as exc:
					page_result[ 'errors' ].append( f'Basic Text: {str( exc )}' )
			
			if include_raw_html:
				page_result[ 'raw_html' ] = raw_html
			
			page_result[ 'data' ] = self.extract_structured_data( url=url, html=raw_html,
				selected_methods=methods )
			return page_result
		except Exception as exc:
			page_result[ 'errors' ].append( f'Fetch: {str( exc )}' )
			return page_result
	
	def crawl( self, seed_url: str, include_title: bool = True, include_basic_text: bool = True,
			include_raw_html: bool = False, selected_methods: Optional[ List[ str ] ] = None,
			recursive: bool = False, max_depth: int = 1, max_pages: int = 10,
			same_domain_only: bool = True,
			request_timeout: int = 10, delay_seconds: float = 0.25,
			max_bytes: int = 1000000 ) -> Dict[ str, Any ]:
		"""Crawl.
		
		Purpose:
			Performs the crawl operation for bounded web crawling and optional browser-rendered
			scraping. The method uses the class runtime state and supplied arguments to prepare,
			transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			seed_url (str): seed URL value used by the crawl operation.
			include_title (bool): include title value used by the crawl operation.
			include_basic_text (bool): include basic text value used by the crawl operation.
			include_raw_html (bool): include raw HTML value used by the crawl operation.
			selected_methods (Optional[List[str]]): selected methods value used by the crawl
				operation.
			recursive (bool): recursive value used by the crawl operation.
			max_depth (int): max depth value used by the crawl operation.
			max_pages (int): max pages value used by the crawl operation.
			same_domain_only (bool): same domain only value used by the crawl operation.
			request_timeout (int): Request timeout in seconds.
			delay_seconds (float): delay seconds value used by the crawl operation.
			max_bytes (int): max bytes value used by the crawl operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'seed_url', seed_url )
			started_at = dt.datetime.now( )
			normalized_seed = self.normalize_url( seed_url, seed_url )
			if not normalized_seed:
				raise ValueError( 'A valid absolute URL is required.' )
			
			methods = selected_methods or [ ]
			queue: List[ Tuple[ str, int ] ] = [ (normalized_seed, 0) ]
			visited: set[ str ] = set( )
			enqueued: set[ str ] = { normalized_seed }
			skipped_urls: List[ str ] = [ ]
			pages: List[ Dict[ str, Any ] ] = [ ]
			
			index = 0
			while index < len( queue ) and len( pages ) < int( max_pages ):
				current_url, depth = queue[ index ]
				index += 1
				if current_url in visited:
					continue
				visited.add( current_url )
				page_result = self.scrape_page( url=current_url, include_title=include_title,
					include_basic_text=include_basic_text, include_raw_html=include_raw_html,
					selected_methods=methods, request_timeout=int( request_timeout ),
					max_bytes=int( max_bytes ) )
				
				page_result[ 'depth' ] = depth
				pages.append( page_result )
				if float( delay_seconds ) > 0 and index < len( queue ):
					time.sleep( float( delay_seconds ) )
				
				if not recursive:
					continue
				
				if depth >= int( max_depth ):
					continue
				
				discovered_links = page_result.get( 'links_discovered', [ ] ) or [ ]
				for next_url in discovered_links:
					if len( pages ) + (len( queue ) - index) >= int( max_pages ):
						break
					
					if not next_url or next_url in visited or next_url in enqueued:
						continue
					
					if same_domain_only and not self.same_domain( normalized_seed, next_url ):
						skipped_urls.append( next_url )
						continue
					
					queue.append( (next_url, depth + 1) )
					enqueued.add( next_url )
			
			finished_at = dt.datetime.now( )
			error_count = sum( len( page.get( 'errors', [ ] ) or [ ] ) for page in pages )
			total_bytes = sum( int( page.get( 'content_bytes', 0 ) or 0 ) for page in pages )
			self.pages = pages
			self.summary = {
					'mode': 'recursive' if recursive else 'single-page',
					'seed_url': normalized_seed,
					'pages_processed': len( pages ),
					'pages_visited': len( visited ),
					'pages_skipped': len( skipped_urls ),
					'pages_enqueued_remaining': max( 0, len( queue ) - index ),
					'errors': error_count,
					'total_content_bytes': total_bytes,
					'recursive_requested': bool( recursive ),
					'max_depth': int( max_depth ),
					'max_pages': int( max_pages ),
					'same_domain_only': bool( same_domain_only ),
					'request_timeout': int( request_timeout ),
					'delay_seconds': float( delay_seconds ),
					'max_bytes_per_page': int( max_bytes ),
					'use_playwright': bool( self.use_playwright ),
					'started_at': started_at.isoformat( ),
					'finished_at': finished_at.isoformat( ),
					'elapsed_seconds': round( (finished_at - started_at).total_seconds( ), 3 ),
					'visited_urls': list( visited ),
					'skipped_urls': skipped_urls,
			}
			
			return {
					'pages': self.pages,
					'summary': self.summary
			}
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'WebCrawler'
			exception.method = 'crawl( self, *args ) -> Dict[ str, Any ]'
			raise exception

class ArXiv( Fetcher ):
	"""Ar Xiv fetcher.
	
	Purpose:
		Coordinates ArXiv research document retrieval within Fonky. The class stores provider
		configuration, request parameters, response payloads, and normalized result state so
		callers can access the service through a consistent fetcher interface.
	
	Attributes:
		fetcher (Optional[ArxivRetriever]): fetcher state retained by the instance.
		documents (Optional[List[Document]]): documents state retained by the instance.
		max_documents (Optional[int]): max documents state retained by the instance.
		full_documents (Optional[bool]): full documents state retained by the instance.
		include_metadata (Optional[bool]): include metadata state retained by the instance.
		query (Optional[str]): query state retained by the instance."""
	fetcher: Optional[ ArxivRetriever ]
	documents: Optional[ List[ Document ] ]
	max_documents: Optional[ int ]
	full_documents: Optional[ bool ]
	include_metadata: Optional[ bool ]
	query: Optional[ str ]
	
	def __init__( self, max_documents: int = 5, full_documents: bool = False,
			include_metadata: bool = False ) -> None:
		"""Initialize ArXiv.
		
		Purpose:
			Initializes the ArXiv instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request.
		
		Args:
			max_documents (int): max documents value used by the init operation.
			full_documents (bool): full documents value used by the init operation.
			include_metadata (bool): include metadata value used by the init operation."""
		super( ).__init__( )
		self.fetcher = None
		self.documents = None
		self.query = None
		self.max_documents = max( 1, min( int( max_documents ), 300 ) )
		self.full_documents = bool( full_documents )
		self.include_metadata = bool( include_metadata )
	
	def fetch( self, question: str, max_documents: int = None,
			full_documents: bool = None, include_metadata: bool = None ) -> List[ Document ] | None:
		"""Fetch ArXiv research document retrieval.
		
		Purpose:
			Retrieves ArXiv research document retrieval using validated arguments and the stored
			ArXiv runtime configuration. The method assembles request parameters, executes the
			provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			question (str): Search text, lookup value, or provider query submitted by the caller.
			max_documents (int): max documents value used by the fetch operation.
			full_documents (bool): full documents value used by the fetch operation.
			include_metadata (bool): include metadata value used by the fetch operation.
		
		Returns:
			List[Document] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'question', question )
			self.query = question.strip( )
			max_docs = self.max_documents if max_documents is None else \
				max( 1, min( int( max_documents ), 300 ) )
			
			get_full = self.full_documents if full_documents is None else \
				bool( full_documents )
			
			load_meta = self.include_metadata if include_metadata is None else \
				bool( include_metadata )
			
			self.fetcher = ArxivRetriever( load_max_docs=max_docs, get_full_documents=get_full,
				load_all_available_meta=load_meta )
			
			self.documents = self.fetcher.invoke( self.query )
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ArXiv'
			exception.method = 'fetch( self, *kwargs ) -> List[ Document ]'
			raise exception

class GoogleDrive( Fetcher ):
	"""Google Drive fetcher.
	
	Purpose:
		Coordinates Google Drive document retrieval within Fonky. The class stores provider
		configuration, request parameters, response payloads, and normalized result state so
		callers can access the service through a consistent fetcher interface.
	
	Attributes:
		fetcher (Optional[GoogleDriveRetriever]): fetcher state retained by the instance.
		documents (Optional[List[Document]]): documents state retained by the instance.
		num_results (Optional[int]): num results state retained by the instance.
		folder_id (Optional[str]): folder ID state retained by the instance.
		template (Optional[str]): template state retained by the instance.
		query (Optional[str]): query state retained by the instance.
		mime_type (Optional[str]): mime type state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		credentials_path (Optional[str]): credentials path state retained by the instance.
		token_path (Optional[str]): token path state retained by the instance.
		retriever_kwargs (Optional[Dict[str, Any]]): retriever kwargs state retained by the
			instance.
		invoke_query (Optional[str]): invoke query state retained by the instance."""
	fetcher: Optional[ GoogleDriveRetriever ]
	documents: Optional[ List[ Document ] ]
	num_results: Optional[ int ]
	folder_id: Optional[ str ]
	template: Optional[ str ]
	query: Optional[ str ]
	mime_type: Optional[ str ]
	mode: Optional[ str ]
	credentials_path: Optional[ str ]
	token_path: Optional[ str ]
	retriever_kwargs: Optional[ Dict[ str, Any ] ]
	invoke_query: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize GoogleDrive.
		
		Purpose:
			Initializes the GoogleDrive instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.fetcher = None
		self.documents = [ ]
		self.query = ''
		self.template = 'gdrive-query'
		self.folder_id = cfg.GOOGLE_DRIVE_FOLDER_ID or 'root'
		self.num_results = 10
		self.mime_type = None
		self.mode = 'documents'
		self.credentials_path = cfg.GOOGLE_ACCOUNT_FILE
		self.token_path = cfg.GOOGLE_DRIVE_TOKEN_PATH
		self.retriever_kwargs = { }
		self.invoke_query = ''
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'fetcher',
				'documents',
				'num_results',
				'folder_id',
				'template',
				'query',
				'mime_type',
				'mode',
				'credentials_path',
				'token_path',
				'retriever_kwargs',
				'invoke_query',
				'mime_options',
				'template_options',
				'mode_options',
				'fetch'
		]
	
	@property
	def mime_options( self ) -> List[ str ]:
		"""Mime options.
		
		Purpose:
			Performs the mime options operation for Google Drive document retrieval. The method uses
			the class runtime state and supplied arguments to prepare, transform, dispatch, or
			package data for the broader Fonky fetching workflow.
		
		Returns:
			List[str]: Result produced by the operation."""
		return [
				'',
				'text/text',
				'text/plain',
				'text/html',
				'text/csv',
				'text/markdown',
				'image/png',
				'image/jpeg',
				'application/epub+zip',
				'application/pdf',
				'application/rtf',
				'application/vnd.google-apps.document',
				'application/vnd.google-apps.presentation',
				'application/vnd.google-apps.spreadsheet',
				'application/vnd.google.colaboratory',
				'application/vnd.openxmlformats-officedocument.presentationml.presentation',
				'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
		]
	
	@property
	def template_options( self ) -> List[ str ]:
		"""Template options.
		
		Purpose:
			Performs the template options operation for Google Drive document retrieval. The method
			uses the class runtime state and supplied arguments to prepare, transform, dispatch, or
			package data for the broader Fonky fetching workflow.
		
		Returns:
			List[str]: Result produced by the operation."""
		return [
				'gdrive-all-in-folder',
				'gdrive-query',
				'gdrive-by-name',
				'gdrive-query-in-folder',
				'gdrive-mime-type',
				'gdrive-mime-type-in-folder',
				'gdrive-query-with-mime-type',
				'gdrive-query-with-mime-type-and-folder',
		]
	
	@property
	def mode_options( self ) -> List[ str ]:
		"""Mode options.
		
		Purpose:
			Performs the mode options operation for Google Drive document retrieval. The method uses
			the class runtime state and supplied arguments to prepare, transform, dispatch, or
			package data for the broader Fonky fetching workflow.
		
		Returns:
			List[str]: Result produced by the operation."""
		return [
				'documents',
				'snippets'
		]
	
	def fetch( self, question: str, folder_id: str = 'root', results: int = 10,
			template: str = 'gdrive-query',
			mime_type: str = None, mode: str = 'documents' ) -> List[ Document ] | None:
		"""Fetch Google Drive document retrieval.
		
		Purpose:
			Retrieves Google Drive document retrieval using validated arguments and the stored
			GoogleDrive runtime configuration. The method assembles request parameters, executes the
			provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			question (str): Search text, lookup value, or provider query submitted by the caller.
			folder_id (str): folder ID value used by the fetch operation.
			results (int): results value used by the fetch operation.
			template (str): template value used by the fetch operation.
			mime_type (str): mime type value used by the fetch operation.
			mode (str): mode value used by the fetch operation.
		
		Returns:
			List[Document] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'template', template )
			throw_if( 'folder_id', folder_id )
			throw_if( 'results', results )
			throw_if( 'mode', mode )
			
			self.query = str( question or '' ).strip( )
			self.folder_id = str( folder_id or 'root' ).strip( ) or 'root'
			self.num_results = int( results )
			self.template = str( template ).strip( )
			self.mime_type = (
					str( mime_type ).strip( )
					if isinstance( mime_type, str ) and str( mime_type ).strip( )
					else None
			)
			self.mode = str( mode ).strip( )
			self.credentials_path = cfg.GOOGLE_ACCOUNT_FILE
			self.token_path = cfg.GOOGLE_DRIVE_TOKEN_PATH
			
			if self.num_results < 1 or self.num_results > 100:
				raise ValueError( 'results must be between 1 and 100.' )
			
			if self.template not in self.template_options:
				raise ValueError( f'Unsupported Google Drive template: {self.template}' )
			
			if self.mode not in self.mode_options:
				raise ValueError( f'Unsupported Google Drive mode: {self.mode}' )
			
			if self.mime_type and self.mime_type not in self.mime_options:
				raise ValueError( f'Unsupported Google Drive MIME type: {self.mime_type}' )
			
			self.invoke_query = self.query
			if not self.invoke_query:
				if self.template in (
							'gdrive-all-in-folder',
							'gdrive-mime-type',
							'gdrive-mime-type-in-folder'
				):
					self.invoke_query = '*'
				else:
					raise ValueError(
						'A query is required for the selected Google Drive template.'
					)
			
			self.retriever_kwargs = {
					'folder_id': self.folder_id,
					'template': self.template,
					'num_results': self.num_results,
					'mode': self.mode,
			}
			
			if self.mime_type:
				self.retriever_kwargs[ 'mime_type' ] = self.mime_type
			
			if self.credentials_path:
				self.retriever_kwargs[ 'credentials_path' ] = self.credentials_path
			
			if self.token_path:
				self.retriever_kwargs[ 'token_path' ] = self.token_path
			
			self.fetcher = GoogleDriveRetriever( **self.retriever_kwargs )
			self.documents = self.fetcher.invoke( self.invoke_query )
			
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GoogleDrive'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> List[ Document ] | None'
			)
			raise exception

class Wikipedia( Fetcher ):
	"""Wikipedia fetcher.
	
	Purpose:
		Coordinates Wikipedia document retrieval within Fonky. The class stores provider
		configuration, request parameters, response payloads, and normalized result state so
		callers can access the service through a consistent fetcher interface.
	
	Attributes:
		fetcher (Optional[WikipediaRetriever]): fetcher state retained by the instance.
		documents (Optional[List[Document]]): documents state retained by the instance.
		max_documents (Optional[int]): max documents state retained by the instance.
		include_metadata (Optional[bool]): include metadata state retained by the instance.
		language (Optional[str]): language state retained by the instance.
		query (Optional[str]): query state retained by the instance."""
	fetcher: Optional[ WikipediaRetriever ]
	documents: Optional[ List[ Document ] ]
	max_documents: Optional[ int ]
	include_metadata: Optional[ bool ]
	language: Optional[ str ]
	query: Optional[ str ]
	
	def __init__( self, language: str = 'en', max_documents: int = 5,
			include_metadata: bool = False ) -> None:
		"""Initialize Wikipedia.
		
		Purpose:
			Initializes the Wikipedia instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request.
		
		Args:
			language (str): language value used by the init operation.
			max_documents (int): max documents value used by the init operation.
			include_metadata (bool): include metadata value used by the init operation."""
		super( ).__init__( )
		self.fetcher = None
		self.documents = None
		self.query = None
		self.language = (language or 'en').strip( ) or 'en'
		self.max_documents = max( 1, min( int( max_documents ), 300 ) )
		self.include_metadata = bool( include_metadata )
	
	def fetch( self, question: str, language: str = None, max_documents: int = None,
			include_metadata: bool = None ) -> List[ Document ] | None:
		"""Fetch Wikipedia document retrieval.
		
		Purpose:
			Retrieves Wikipedia document retrieval using validated arguments and the stored
			Wikipedia runtime configuration. The method assembles request parameters, executes the
			provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			question (str): Search text, lookup value, or provider query submitted by the caller.
			language (str): language value used by the fetch operation.
			max_documents (int): max documents value used by the fetch operation.
			include_metadata (bool): include metadata value used by the fetch operation.
		
		Returns:
			List[Document] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'question', question )
			self.query = question.strip( )
			
			lang = self.language if language is None else \
				(language.strip( ) if language else 'en')
			
			max_docs = self.max_documents if max_documents is None else \
				max( 1, min( int( max_documents ), 300 ) )
			
			load_meta = self.include_metadata if include_metadata is None else \
				bool( include_metadata )
			
			self.fetcher = WikipediaRetriever( lang=lang, load_max_docs=max_docs,
				load_all_available_meta=load_meta )
			
			self.documents = self.fetcher.invoke( input=self.query )
			return self.documents
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'Wikipedia'
			exception.method = 'fetch( self, question: str, **kwargs ) -> List[ Document ]'
			raise exception

class TheNews( Fetcher ):
	"""The News fetcher.
	
	Purpose:
		Coordinates The News API article retrieval within Fonky. The class stores provider
		configuration, request parameters, response payloads, and normalized result state so
		callers can access the service through a consistent fetcher interface.
	
	Attributes:
		agents (Optional[str]): agents state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		response (Optional[Response]): response state retained by the instance.
		api_key (Optional[str]): API key state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		endpoint (Optional[str]): endpoint state retained by the instance.
		limit (Optional[int]): limit state retained by the instance.
		page (Optional[int]): page state retained by the instance.
		timeout (object): timeout state retained by the instance.
		result (object): result state retained by the instance.
		headers (object): headers state retained by the instance."""
	agents: Optional[ str ]
	url: Optional[ str ]
	response: Optional[ Response ]
	api_key: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	endpoint: Optional[ str ]
	limit: Optional[ int ]
	page: Optional[ int ]
	
	def __init__( self ) -> None:
		"""Initialize TheNews.
		
		Purpose:
			Initializes the TheNews instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.timeout = 10
		self.url = 'https://api.thenewsapi.com/v1/news'
		self.response = None
		self.result = None
		self.headers = { }
		self.params = { }
		self.endpoint = 'all'
		self.limit = 10
		self.page = 1
		self.api_key = cfg.THENEWS_API_KEY
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
		
		if 'Accept' not in self.headers:
			self.headers[ 'Accept' ] = 'application/json'
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [ 'api_key', 'url', 'timeout', 'headers', 'endpoint',
		         'limit', 'page', 'params', 'fetch', ]
	
	def fetch( self, endpoint: str = 'all', query: str = '', language: str = 'en',
			categories: str = '',
			exclude_categories: str = '', locale: str = '', domains: str = '',
			exclude_domains: str = '', source_ids: str = '', exclude_source_ids: str = '',
			published_after: str = '', published_before: str = '', published_on: str = '',
			sort: str = 'published_at', limit: int = 10, page: int = 1,
			include_similar: bool = True,
			headlines_per_category: int = 6, time: int = 10, api_key: str = None ) -> Dict[
		str, Any ]:
		"""Fetch The News API article retrieval.
		
		Purpose:
			Retrieves The News API article retrieval using validated arguments and the stored
			TheNews runtime configuration. The method assembles request parameters, executes the
			provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			endpoint (str): endpoint value used by the fetch operation.
			query (str): Search text, lookup value, or provider query submitted by the caller.
			language (str): language value used by the fetch operation.
			categories (str): categories value used by the fetch operation.
			exclude_categories (str): exclude categories value used by the fetch operation.
			locale (str): locale value used by the fetch operation.
			domains (str): domains value used by the fetch operation.
			exclude_domains (str): exclude domains value used by the fetch operation.
			source_ids (str): source IDs value used by the fetch operation.
			exclude_source_ids (str): exclude source IDs value used by the fetch operation.
			published_after (str): published after value used by the fetch operation.
			published_before (str): published before value used by the fetch operation.
			published_on (str): published on value used by the fetch operation.
			sort (str): sort value used by the fetch operation.
			limit (int): limit value used by the fetch operation.
			page (int): page value used by the fetch operation.
			include_similar (bool): include similar value used by the fetch operation.
			headlines_per_category (int): headlines per category value used by the fetch operation.
			time (int): Request timeout in seconds.
			api_key (str): Optional credential override used for the active request.
		
		Returns:
			Dict[str, Any]: Normalized provider response, result payload, or document collection
				returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.endpoint = (endpoint or 'all').strip( ).lower( )
			self.timeout = int( time )
			self.limit = max( 1, min( int( limit ), 50 ) )
			self.page = max( 1, int( page ) )
			active_key = (api_key or self.api_key or '').strip( )
			if not active_key:
				raise ValueError( 'The News API key is required.' )
			
			valid_endpoints = { 'all', 'top', 'headlines', 'sources' }
			if self.endpoint not in valid_endpoints:
				raise ValueError( f"Unsupported endpoint '{self.endpoint}'. "
				                  f"Supported endpoints: {', '.join( sorted( valid_endpoints ) )}." )
			
			self.params = { 'api_token': active_key }
			if self.endpoint in ('all', 'top'):
				if query and query.strip( ):
					self.params[ 'search' ] = query.strip( )
				
				if language and language.strip( ):
					self.params[ 'language' ] = language.strip( )
				
				if categories and categories.strip( ):
					self.params[ 'categories' ] = categories.strip( )
				
				if exclude_categories and exclude_categories.strip( ):
					self.params[ 'exclude_categories' ] = exclude_categories.strip( )
				
				if domains and domains.strip( ):
					self.params[ 'domains' ] = domains.strip( )
				
				if exclude_domains and exclude_domains.strip( ):
					self.params[ 'exclude_domains' ] = exclude_domains.strip( )
				
				if source_ids and source_ids.strip( ):
					self.params[ 'source_ids' ] = source_ids.strip( )
				
				if exclude_source_ids and exclude_source_ids.strip( ):
					self.params[ 'exclude_source_ids' ] = exclude_source_ids.strip( )
				
				if published_after and published_after.strip( ):
					self.params[ 'published_after' ] = published_after.strip( )
				
				if published_before and published_before.strip( ):
					self.params[ 'published_before' ] = published_before.strip( )
				
				if published_on and published_on.strip( ):
					self.params[ 'published_on' ] = published_on.strip( )
				
				if sort and sort.strip( ):
					self.params[ 'sort' ] = sort.strip( )
				
				self.params[ 'limit' ] = self.limit
				self.params[ 'page' ] = self.page
				if self.endpoint == 'top' and locale and locale.strip( ):
					self.params[ 'locale' ] = locale.strip( )
			
			elif self.endpoint == 'headlines':
				if locale and locale.strip( ):
					self.params[ 'locale' ] = locale.strip( )
				
				if domains and domains.strip( ):
					self.params[ 'domains' ] = domains.strip( )
				
				if exclude_domains and exclude_domains.strip( ):
					self.params[ 'exclude_domains' ] = exclude_domains.strip( )
				
				if source_ids and source_ids.strip( ):
					self.params[ 'source_ids' ] = source_ids.strip( )
				
				if exclude_source_ids and exclude_source_ids.strip( ):
					self.params[ 'exclude_source_ids' ] = exclude_source_ids.strip( )
				
				if language and language.strip( ):
					self.params[ 'language' ] = language.strip( )
				
				if published_on and published_on.strip( ):
					self.params[ 'published_on' ] = published_on.strip( )
				
				self.params[ 'headlines_per_category' ] = max( 1,
					min( int( headlines_per_category ), 10 ) )
				
				self.params[ 'include_similar' ] = \
					'true' if bool( include_similar ) else 'false'
			
			elif self.endpoint == 'sources':
				if categories and categories.strip( ):
					self.params[ 'categories' ] = categories.strip( )
				
				if exclude_categories and exclude_categories.strip( ):
					self.params[ 'exclude_categories' ] = exclude_categories.strip( )
				
				if language and language.strip( ):
					self.params[ 'language' ] = language.strip( )
				
				self.params[ 'page' ] = self.page
			
			request_url = f'{self.url}/{self.endpoint}'
			self.response = requests.get( url=request_url, params=self.params, headers=self.headers,
				timeout=self.timeout )
			
			self.response.raise_for_status( )
			return self.response.json( )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'TheNews'
			exception.method = 'fetch( self, **kwargs ) -> Dict[ str, Any ]'
			raise exception

class GoogleSearch( Fetcher ):
	"""Google Search fetcher.
	
	Purpose:
		Coordinates Google Custom Search retrieval within Fonky. The class stores provider
		configuration, request parameters, response payloads, and normalized result state so
		callers can access the service through a consistent fetcher interface.
	
	Attributes:
		keywords (Optional[str]): keywords state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		re_tag (Optional[Pattern]): re tag state retained by the instance.
		re_ws (Optional[Pattern]): re ws state retained by the instance.
		response (Optional[Response]): response state retained by the instance.
		api_key (Optional[str]): API key state retained by the instance.
		cse_id (Optional[str]): cse ID state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		results (Optional[int]): results state retained by the instance.
		start (Optional[int]): start state retained by the instance.
		exact_terms (Optional[str]): exact terms state retained by the instance.
		exclude_terms (Optional[str]): exclude terms state retained by the instance.
		file_type (Optional[str]): file type state retained by the instance.
		date_restrict (Optional[str]): date restrict state retained by the instance.
		gl (Optional[str]): gl state retained by the instance.
		lr (Optional[str]): lr state retained by the instance.
		safe (Optional[str]): safe state retained by the instance.
		search_type (Optional[str]): search type state retained by the instance.
		site_search (Optional[str]): site search state retained by the instance.
		site_search_filter (Optional[str]): site search filter state retained by the instance.
		sort (Optional[str]): sort state retained by the instance.
		img_size (Optional[str]): img size state retained by the instance.
		img_type (Optional[str]): img type state retained by the instance.
		img_color_type (Optional[str]): img color type state retained by the instance.
		img_dominant_color (Optional[str]): img dominant color state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		headers (object): headers state retained by the instance.
		timeout (object): timeout state retained by the instance."""
	keywords: Optional[ str ]
	url: Optional[ str ]
	re_tag: Optional[ Pattern ]
	re_ws: Optional[ Pattern ]
	response: Optional[ Response ]
	api_key: Optional[ str ]
	cse_id: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	results: Optional[ int ]
	start: Optional[ int ]
	exact_terms: Optional[ str ]
	exclude_terms: Optional[ str ]
	file_type: Optional[ str ]
	date_restrict: Optional[ str ]
	gl: Optional[ str ]
	lr: Optional[ str ]
	safe: Optional[ str ]
	search_type: Optional[ str ]
	site_search: Optional[ str ]
	site_search_filter: Optional[ str ]
	sort: Optional[ str ]
	img_size: Optional[ str ]
	img_type: Optional[ str ]
	img_color_type: Optional[ str ]
	img_dominant_color: Optional[ str ]
	agents: Optional[ str ]
	result: Optional[ Dict[ str, Any ] ]
	
	def __init__( self ) -> None:
		"""Initialize GoogleSearch.
		
		Purpose:
			Initializes the GoogleSearch instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.api_key = cfg.GOOGLE_API_KEY
		self.cse_id = cfg.GOOGLE_CSE_ID
		self.re_tag = re.compile( r'<[^>]+>' )
		self.re_ws = re.compile( r'\s+' )
		self.url = 'https://customsearch.googleapis.com/customsearch/v1'
		self.headers = { }
		self.timeout = 10
		self.keywords = None
		self.params = { }
		self.payload = { }
		self.response = None
		self.result = { }
		self.results = 10
		self.start = 1
		self.exact_terms = None
		self.exclude_terms = None
		self.file_type = None
		self.date_restrict = None
		self.gl = None
		self.lr = None
		self.safe = 'off'
		self.search_type = None
		self.site_search = None
		self.site_search_filter = None
		self.sort = None
		self.img_size = None
		self.img_type = None
		self.img_color_type = None
		self.img_dominant_color = None
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
		
		if 'Accept' not in self.headers:
			self.headers[ 'Accept' ] = 'application/json'
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'keywords',
				'url',
				'timeout',
				'headers',
				'fetch',
				'api_key',
				'response',
				'payload',
				'result',
				'cse_id',
				'params',
				'agents',
				'results',
				'start',
				'exact_terms',
				'exclude_terms',
				'file_type',
				'date_restrict',
				'gl',
				'lr',
				'safe',
				'search_type',
				'site_search',
				'site_search_filter',
				'sort',
				'img_size',
				'img_type',
				'img_color_type',
				'img_dominant_color'
		]
	
	def fetch( self, keywords: str, results: int = 10, start: int = 1, exact_terms: str = '',
			exclude_terms: str = '', file_type: str = '', date_restrict: str = '', gl: str = '',
			lr: str = '',
			safe: str = 'off', search_type: str = '', site_search: str = '',
			site_search_filter: str = '',
			sort: str = '', img_size: str = '', img_type: str = '', img_color_type: str = '',
			img_dominant_color: str = '', time: int = 10, api_key: str = None,
			cse_id: str = None ) -> Dict[ str, Any ] | None:
		"""Fetch Google Custom Search retrieval.
		
		Purpose:
			Retrieves Google Custom Search retrieval using validated arguments and the stored
			GoogleSearch runtime configuration. The method assembles request parameters, executes
			the provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			keywords (str): Search text, lookup value, or provider query submitted by the caller.
			results (int): results value used by the fetch operation.
			start (int): start value used by the fetch operation.
			exact_terms (str): exact terms value used by the fetch operation.
			exclude_terms (str): exclude terms value used by the fetch operation.
			file_type (str): file type value used by the fetch operation.
			date_restrict (str): date restrict value used by the fetch operation.
			gl (str): gl value used by the fetch operation.
			lr (str): lr value used by the fetch operation.
			safe (str): safe value used by the fetch operation.
			search_type (str): search type value used by the fetch operation.
			site_search (str): site search value used by the fetch operation.
			site_search_filter (str): site search filter value used by the fetch operation.
			sort (str): sort value used by the fetch operation.
			img_size (str): img size value used by the fetch operation.
			img_type (str): img type value used by the fetch operation.
			img_color_type (str): img color type value used by the fetch operation.
			img_dominant_color (str): img dominant color value used by the fetch operation.
			time (int): Request timeout in seconds.
			api_key (str): Optional credential override used for the active request.
			cse_id (str): cse ID value used by the fetch operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'keywords', keywords )
			throw_if( 'time', time )
			
			if api_key:
				self.api_key = str( api_key ).strip( )
			
			if cse_id:
				self.cse_id = str( cse_id ).strip( )
			
			throw_if( 'api_key', self.api_key )
			throw_if( 'cse_id', self.cse_id )
			
			self.timeout = int( time )
			self.keywords = str( keywords ).strip( )
			self.results = int( results )
			self.start = int( start )
			
			if self.results < 1:
				raise ValueError( 'results must be greater than or equal to 1.' )
			
			if self.results > 10:
				raise ValueError( 'results cannot exceed 10 for one Google Custom Search request.' )
			
			if self.start < 1:
				raise ValueError( 'start must be greater than or equal to 1.' )
			
			if self.start > 91:
				raise ValueError( 'start cannot exceed 91 when requesting up to 10 results.' )
			
			self.exact_terms = str( exact_terms or '' ).strip( )
			self.exclude_terms = str( exclude_terms or '' ).strip( )
			self.file_type = str( file_type or '' ).strip( )
			self.date_restrict = str( date_restrict or '' ).strip( )
			self.gl = str( gl or '' ).strip( )
			self.lr = str( lr or '' ).strip( )
			self.safe = str( safe or 'off' ).strip( )
			self.search_type = str( search_type or '' ).strip( )
			self.site_search = str( site_search or '' ).strip( )
			self.site_search_filter = str( site_search_filter or '' ).strip( )
			self.sort = str( sort or '' ).strip( )
			self.img_size = str( img_size or '' ).strip( )
			self.img_type = str( img_type or '' ).strip( )
			self.img_color_type = str( img_color_type or '' ).strip( )
			self.img_dominant_color = str( img_dominant_color or '' ).strip( )
			
			self.params = {
					'q': self.keywords,
					'key': self.api_key,
					'cx': self.cse_id,
					'num': self.results,
					'start': self.start,
					'safe': self.safe
			}
			
			if self.exact_terms:
				self.params[ 'exactTerms' ] = self.exact_terms
			
			if self.exclude_terms:
				self.params[ 'excludeTerms' ] = self.exclude_terms
			
			if self.file_type:
				self.params[ 'fileType' ] = self.file_type
			
			if self.date_restrict:
				self.params[ 'dateRestrict' ] = self.date_restrict
			
			if self.gl:
				self.params[ 'gl' ] = self.gl
			
			if self.lr:
				self.params[ 'lr' ] = self.lr
			
			if self.search_type:
				self.params[ 'searchType' ] = self.search_type
			
			if self.site_search:
				self.params[ 'siteSearch' ] = self.site_search
			
			if self.site_search_filter:
				self.params[ 'siteSearchFilter' ] = self.site_search_filter
			
			if self.sort:
				self.params[ 'sort' ] = self.sort
			
			if self.search_type.lower( ) == 'image':
				if self.img_size:
					self.params[ 'imgSize' ] = self.img_size
				
				if self.img_type:
					self.params[ 'imgType' ] = self.img_type
				
				if self.img_color_type:
					self.params[ 'imgColorType' ] = self.img_color_type
				
				if self.img_dominant_color:
					self.params[ 'imgDominantColor' ] = self.img_dominant_color
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			
			self.response.raise_for_status( )
			self.payload = self.response.json( )
			self.result = self.payload
			
			return self.result
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'GoogleSearch'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception

class GoogleMaps( Fetcher ):
	"""Google Maps fetcher.
	
	Purpose:
		Coordinates Google Maps geocoding, address validation, and directions within Fonky. The
		class stores provider configuration, request parameters, response payloads, and
		normalized result state so callers can access the service through a consistent fetcher
		interface.
	
	Attributes:
		file_path (Optional[str]): file path state retained by the instance.
		headers (Optional[Dict[str, Any]]): headers state retained by the instance.
		num_results (Optional[int]): num results state retained by the instance.
		api_key (Optional[str]): API key state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		latitude (Optional[float]): latitude state retained by the instance.
		longitude (Optional[float]): longitude state retained by the instance.
		coordinates (Optional[Tuple[float, float]]): coordinates state retained by the instance.
		address (Optional[str]): address state retained by the instance.
		address_lines (Optional[List[str]]): address lines state retained by the instance.
		origin (Optional[str]): origin state retained by the instance.
		destination (Optional[str]): destination state retained by the instance.
		directions (Optional[Dict[str, Any]]): directions state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Any]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		timeout (Optional[int]): timeout state retained by the instance.
		url (object): URL state retained by the instance.
		response (object): response state retained by the instance."""
	file_path: Optional[ str ]
	headers: Optional[ Dict[ str, Any ] ]
	num_results: Optional[ int ]
	api_key: Optional[ str ]
	mode: Optional[ str ]
	latitude: Optional[ float ]
	longitude: Optional[ float ]
	coordinates: Optional[ Tuple[ float, float ] ]
	address: Optional[ str ]
	address_lines: Optional[ List[ str ] ]
	origin: Optional[ str ]
	destination: Optional[ str ]
	directions: Optional[ Dict[ str, Any ] ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Any ]
	agents: Optional[ str ]
	timeout: Optional[ int ]
	
	def __init__( self ) -> None:
		"""Initialize GoogleMaps.
		
		Purpose:
			Initializes the GoogleMaps instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.api_key = cfg.GOOGLE_API_KEY
		self.headers = { }
		self.params = { }
		self.longitude = None
		self.latitude = None
		self.mode = None
		self.url = None
		self.file_path = None
		self.coordinates = None
		self.address = None
		self.address_lines = [ ]
		self.origin = None
		self.destination = None
		self.directions = { }
		self.response = None
		self.payload = { }
		self.result = None
		self.timeout = 10
		self.num_results = None
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
		
		if 'Accept' not in self.headers:
			self.headers[ 'Accept' ] = 'application/json'
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'file_path',
				'headers',
				'num_results',
				'api_key',
				'mode',
				'latitude',
				'longitude',
				'coordinates',
				'address',
				'address_lines',
				'origin',
				'destination',
				'directions',
				'params',
				'payload',
				'result',
				'agents',
				'timeout',
				'response',
				'url',
				'geocode_location',
				'geocode_coordinates',
				'validate_address',
				'request_directions',
				'create_schema'
		]
	
	def geocode_location( self, address: str ) -> Tuple[ float, float ]:
		"""Geocode location.
		
		Purpose:
			Performs the geocode location operation for Google Maps geocoding, address validation,
			and directions. The method uses the class runtime state and supplied arguments to
			prepare, transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			address (str): address value used by the geocode location operation.
		
		Returns:
			Tuple[float, float]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'address', address )
			self.mode = 'geocode_location'
			self.address = str( address ).strip( )
			self.url = 'https://maps.googleapis.com/maps/api/geocode/json'
			self.params = {
					'address': self.address,
					'key': self.api_key
			}
			
			self.response = requests.get( url=self.url, params=self.params, headers=self.headers,
				timeout=self.timeout )
			self.response.raise_for_status( )
			self.payload = self.response.json( )
			results = self.payload.get( 'results', [ ] ) if isinstance( self.payload,
				dict ) else [ ]
			
			if not results:
				raise ValueError( 'No geocoding results were returned for the supplied address.' )
			
			location = results[ 0 ].get( 'geometry', { } ).get( 'location', { } )
			self.latitude = float( location.get( 'lat' ) )
			self.longitude = float( location.get( 'lng' ) )
			self.coordinates = (self.latitude, self.longitude)
			self.result = self.coordinates
			
			return self.coordinates
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GoogleMaps'
			exception.method = (
					'geocode_location( self, *args, **kwargs ) -> Tuple[ float, float ]'
			)
			raise exception
	
	def geocode_coordinates( self, lat: float, long: float ) -> str | None:
		"""Geocode coordinates.
		
		Purpose:
			Performs the geocode coordinates operation for Google Maps geocoding, address
			validation, and directions. The method uses the class runtime state and supplied
			arguments to prepare, transform, dispatch, or package data for the broader Fonky
			fetching workflow.
		
		Args:
			lat (float): lat value used by the geocode coordinates operation.
			long (float): long value used by the geocode coordinates operation.
		
		Returns:
			str | None: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'api_key', self.api_key )
			throw_if( 'latitude', lat )
			throw_if( 'longitude', long )
			
			self.mode = 'geocode_coordinates'
			self.latitude = float( lat )
			self.longitude = float( long )
			self.coordinates = (self.latitude, self.longitude)
			self.url = 'https://maps.googleapis.com/maps/api/geocode/json'
			self.params = {
					'latlng': f'{self.latitude},{self.longitude}',
					'key': self.api_key
			}
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			self.payload = self.response.json( )
			results = self.payload.get( 'results', [ ] ) if isinstance( self.payload,
				dict ) else [ ]
			
			if not results:
				raise ValueError( 'No address results were returned for the supplied coordinates.' )
			
			self.address = str( results[ 0 ].get( 'formatted_address', '' ) )
			self.result = self.address
			
			return self.address
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GoogleMaps'
			exception.method = (
					'geocode_coordinates( self, *args, **kwargs ) -> str | None'
			)
			raise exception
	
	def validate_address( self, address: List[ str ] ) -> Dict[ Any, Any ] | None:
		"""Validate address.
		
		Purpose:
			Validates and normalizes address before it is used in Google Maps geocoding, address
			validation, and directions. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			address (List[str]): address value used by the validate address operation.
		
		Returns:
			Dict[Any, Any] | None: Validated address value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'api_key', self.api_key )
			throw_if( 'address', address )
			
			if not isinstance( address, list ):
				raise TypeError( 'address must be a list of address-line strings.' )
			
			self.mode = 'validate_address'
			self.url = 'https://addressvalidation.googleapis.com/v1:validateAddress'
			self.address_lines = [
					str( line ).strip( )
					for line in address
					if line is not None and str( line ).strip( )
			]
			
			if not self.address_lines:
				raise ValueError( 'At least one address line is required.' )
			
			self.params = {
					'key': self.api_key
			}
			self.payload = {
					'address': {
							'addressLines': self.address_lines
					}
			}
			
			self.response = requests.post(
				url=self.url,
				params=self.params,
				json=self.payload,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			self.result = self.response.json( )
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GoogleMaps'
			exception.method = (
					'validate_address( self, *args, **kwargs ) -> Dict[ Any, Any ] | None'
			)
			raise exception
	
	def request_directions( self, origin: str, destination: str,
			mode: str = 'driving' ) -> Dict[ str, Any ] | None:
		"""Request directions.
		
		Purpose:
			Performs the request directions operation for Google Maps geocoding, address validation,
			and directions. The method uses the class runtime state and supplied arguments to
			prepare, transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			origin (str): origin value used by the request directions operation.
			destination (str): destination value used by the request directions operation.
			mode (str): mode value used by the request directions operation.
		
		Returns:
			Dict[str, Any] | None: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'api_key', self.api_key )
			throw_if( 'origin', origin )
			throw_if( 'destination', destination )
			throw_if( 'mode', mode )
			
			self.mode = str( mode ).strip( ).lower( )
			self.origin = str( origin ).strip( )
			self.destination = str( destination ).strip( )
			self.url = 'https://maps.googleapis.com/maps/api/directions/json'
			self.params = {
					'origin': self.origin,
					'destination': self.destination,
					'mode': self.mode,
					'key': self.api_key
			}
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			self.payload = self.response.json( )
			routes = self.payload.get( 'routes', [ ] ) if isinstance( self.payload, dict ) else [ ]
			self.directions = routes[ 0 ] if routes else { }
			self.result = self.directions
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GoogleMaps'
			exception.method = (
					'request_directions( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f"{description.strip( )} This function uses the "
							f"{tool.strip( )} service."
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GoogleMaps'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class GoogleWeather( Fetcher ):
	"""Google Weather fetcher.
	
	Purpose:
		Coordinates Google Weather conditions, forecasts, history, and alerts within Fonky. The
		class stores provider configuration, request parameters, response payloads, and
		normalized result state so callers can access the service through a consistent fetcher
		interface.
	
	Attributes:
		gmaps (Optional[GoogleMaps]): gmaps state retained by the instance.
		headers (Optional[Dict[str, Any]]): headers state retained by the instance.
		api_key (Optional[str]): API key state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		latitude (Optional[float]): latitude state retained by the instance.
		longitude (Optional[float]): longitude state retained by the instance.
		coordinates (Optional[Tuple[float, float]]): coordinates state retained by the instance.
		address (Optional[str]): address state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		response (Optional[Response]): response state retained by the instance.
		payload (Optional[Dict[str, Any]]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		units_system (Optional[str]): units system state retained by the instance.
		language_code (Optional[str]): language code state retained by the instance.
		hours (Optional[int]): hours state retained by the instance.
		days (Optional[int]): days state retained by the instance.
		path (Optional[str]): path state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance."""
	gmaps: Optional[ GoogleMaps ]
	headers: Optional[ Dict[ str, Any ] ]
	api_key: Optional[ str ]
	mode: Optional[ str ]
	latitude: Optional[ float ]
	longitude: Optional[ float ]
	coordinates: Optional[ Tuple[ float, float ] ]
	address: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	response: Optional[ Response ]
	payload: Optional[ Dict[ str, Any ] ]
	result: Optional[ Dict[ str, Any ] ]
	units_system: Optional[ str ]
	language_code: Optional[ str ]
	hours: Optional[ int ]
	days: Optional[ int ]
	path: Optional[ str ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize GoogleWeather.
		
		Purpose:
			Initializes the GoogleWeather instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.api_key = cfg.GOOGLE_WEATHER_API_KEY
		self.headers = { }
		self.gmaps = GoogleMaps( )
		self.mode = None
		self.url = 'https://weather.googleapis.com/v1'
		self.longitude = 0.0
		self.latitude = 0.0
		self.coordinates = (0.0, 0.0)
		self.address = None
		self.params = { }
		self.response = None
		self.payload = { }
		self.result = { }
		self.timeout = 10
		self.units_system = 'METRIC'
		self.language_code = 'en'
		self.hours = None
		self.days = None
		self.path = None
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
		
		if 'Accept' not in self.headers:
			self.headers[ 'Accept' ] = 'application/json'
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'api_key',
				'url',
				'timeout',
				'headers',
				'gmaps',
				'mode',
				'latitude',
				'longitude',
				'coordinates',
				'address',
				'params',
				'response',
				'payload',
				'result',
				'units_system',
				'language_code',
				'hours',
				'days',
				'path',
				'agents',
				'resolve_coordinates',
				'request',
				'package_response',
				'fetch_current',
				'fetch_hourly_forecast',
				'fetch_daily_forecast',
				'fetch_hourly_history',
				'fetch_alerts'
		]
	
	def resolve_coordinates( self, address: str ) -> Tuple[ float, float ]:
		"""Resolve coordinates.
		
		Purpose:
			Performs the resolve coordinates operation for Google Weather conditions, forecasts,
			history, and alerts. The method uses the class runtime state and supplied arguments to
			prepare, transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			address (str): address value used by the resolve coordinates operation.
		
		Returns:
			Tuple[float, float]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'address', address )
			
			self.address = str( address ).strip( )
			lat, lng = self.gmaps.geocode_location( address=self.address )
			self.latitude = float( lat )
			self.longitude = float( lng )
			self.coordinates = (self.latitude, self.longitude)
			
			return self.coordinates
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'GoogleWeather'
			exception.method = 'resolve_coordinates( self, *args, **kwargs ) -> Tuple[ float, float ]'
			raise exception
	
	def request( self, path: str, params: Dict[ str, Any ], time: int = 10 ) -> Dict[
		                                                                            str, Any ] | None:
		"""Request Google Weather conditions, forecasts, history, and alerts.
		
		Purpose:
			Sends a provider request for Google Weather conditions, forecasts, history, and alerts
			after request parameters have been validated or prepared by the caller. The method
			stores request, response, and payload state on the instance so subsequent methods can
			package or inspect the result consistently.
		
		Args:
			path (str): path value used by the request operation.
			params (Dict[str, Any]): Request or schema parameter dictionary used by the operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'api_key', self.api_key )
			throw_if( 'path', path )
			throw_if( 'params', params )
			throw_if( 'time', time )
			
			self.path = str( path ).strip( ).lstrip( '/' )
			self.timeout = int( time )
			self.params = { }
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			for key, value in params.items( ):
				if value is None:
					continue
				
				if isinstance( value, str ) and not value.strip( ):
					continue
				
				self.params[ key ] = value
			
			self.params[ 'key' ] = self.api_key
			request_url = f'{self.url}/{self.path}'
			
			self.response = requests.get( url=request_url, params=self.params, headers=self.headers,
				timeout=self.timeout )
			
			self.response.raise_for_status( )
			self.payload = self.response.json( )
			self.result = {
					'mode': self.mode,
					'url': request_url,
					'params': self.params,
					'data': self.payload
			}
			
			return self.result
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'GoogleWeather'
			exception.method = 'request( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def package_response( self ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if not isinstance( self.result, dict ):
				self.result = { }
			
			if 'data' not in self.result:
				self.result = {
						'mode': self.mode,
						'url': f'{self.url}/{self.path}' if self.path else self.url,
						'params': self.params,
						'data': self.payload or { }
				}
			
			return self.result
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'GoogleWeather'
			exception.method = 'package_response( self ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_current( self, address: str, units_system: str = 'METRIC',
			language_code: str = 'en', time: int = 10 ) -> Dict[ str, Any ] | None:
		"""Fetch current.
		
		Purpose:
			Retrieves current using validated arguments and the stored GoogleWeather runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			address (str): address value used by the fetch current operation.
			units_system (str): units system value used by the fetch current operation.
			language_code (str): language code value used by the fetch current operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'address', address )
			throw_if( 'units_system', units_system )
			throw_if( 'language_code', language_code )
			throw_if( 'time', time )
			
			self.mode = 'current'
			self.units_system = str( units_system ).strip( )
			self.language_code = str( language_code ).strip( )
			self.timeout = int( time )
			self.latitude, self.longitude = self.resolve_coordinates( address )
			
			self.params = {
					'location.latitude': self.latitude,
					'location.longitude': self.longitude,
					'unitsSystem': self.units_system,
					'languageCode': self.language_code
			}
			
			self.request(
				path='currentConditions:lookup',
				params=self.params,
				time=self.timeout
			)
			
			return self.package_response( )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'GoogleWeather'
			exception.method = (
					'fetch_current( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_hourly_forecast( self, address: str, hours: int = 24,
			units_system: str = 'METRIC', language_code: str = 'en',
			time: int = 10 ) -> Dict[ str, Any ] | None:
		"""Fetch hourly forecast.
		
		Purpose:
			Retrieves hourly forecast using validated arguments and the stored GoogleWeather runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			address (str): address value used by the fetch hourly forecast operation.
			hours (int): hours value used by the fetch hourly forecast operation.
			units_system (str): units system value used by the fetch hourly forecast operation.
			language_code (str): language code value used by the fetch hourly forecast operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'address', address )
			throw_if( 'hours', hours )
			throw_if( 'units_system', units_system )
			throw_if( 'language_code', language_code )
			throw_if( 'time', time )
			
			self.mode = 'hourly_forecast'
			self.hours = int( hours )
			self.units_system = str( units_system ).strip( )
			self.language_code = str( language_code ).strip( )
			self.timeout = int( time )
			
			if self.hours < 1 or self.hours > 240:
				raise ValueError( 'hours must be between 1 and 240.' )
			
			self.latitude, self.longitude = self.resolve_coordinates( address )
			self.params = {
					'location.latitude': self.latitude,
					'location.longitude': self.longitude,
					'hours': self.hours,
					'unitsSystem': self.units_system,
					'languageCode': self.language_code
			}
			
			self.request(
				path='forecast/hours:lookup',
				params=self.params,
				time=self.timeout
			)
			
			return self.package_response( )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'GoogleWeather'
			exception.method = (
					'fetch_hourly_forecast( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_daily_forecast( self, address: str, days: int = 5,
			units_system: str = 'METRIC', language_code: str = 'en',
			time: int = 10 ) -> Dict[ str, Any ] | None:
		"""Fetch daily forecast.
		
		Purpose:
			Retrieves daily forecast using validated arguments and the stored GoogleWeather runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			address (str): address value used by the fetch daily forecast operation.
			days (int): days value used by the fetch daily forecast operation.
			units_system (str): units system value used by the fetch daily forecast operation.
			language_code (str): language code value used by the fetch daily forecast operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'address', address )
			throw_if( 'days', days )
			throw_if( 'units_system', units_system )
			throw_if( 'language_code', language_code )
			throw_if( 'time', time )
			
			self.mode = 'daily_forecast'
			self.days = int( days )
			self.units_system = str( units_system ).strip( )
			self.language_code = str( language_code ).strip( )
			self.timeout = int( time )
			
			if self.days < 1 or self.days > 10:
				raise ValueError( 'days must be between 1 and 10.' )
			
			self.latitude, self.longitude = self.resolve_coordinates( address )
			self.params = {
					'location.latitude': self.latitude,
					'location.longitude': self.longitude,
					'days': self.days,
					'unitsSystem': self.units_system,
					'languageCode': self.language_code
			}
			
			self.request(
				path='forecast/days:lookup',
				params=self.params,
				time=self.timeout
			)
			
			return self.package_response( )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'GoogleWeather'
			exception.method = (
					'fetch_daily_forecast( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_hourly_history( self, address: str, hours: int = 24,
			units_system: str = 'METRIC', language_code: str = 'en',
			time: int = 10 ) -> Dict[ str, Any ] | None:
		"""Fetch hourly history.
		
		Purpose:
			Retrieves hourly history using validated arguments and the stored GoogleWeather runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			address (str): address value used by the fetch hourly history operation.
			hours (int): hours value used by the fetch hourly history operation.
			units_system (str): units system value used by the fetch hourly history operation.
			language_code (str): language code value used by the fetch hourly history operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'address', address )
			throw_if( 'hours', hours )
			throw_if( 'units_system', units_system )
			throw_if( 'language_code', language_code )
			throw_if( 'time', time )
			
			self.mode = 'hourly_history'
			self.hours = int( hours )
			self.units_system = str( units_system ).strip( )
			self.language_code = str( language_code ).strip( )
			self.timeout = int( time )
			
			if self.hours < 1 or self.hours > 24:
				raise ValueError( 'hours must be between 1 and 24 for hourly history.' )
			
			self.latitude, self.longitude = self.resolve_coordinates( address )
			self.params = {
					'location.latitude': self.latitude,
					'location.longitude': self.longitude,
					'hours': self.hours,
					'unitsSystem': self.units_system,
					'languageCode': self.language_code
			}
			
			self.request(
				path='history/hours:lookup',
				params=self.params,
				time=self.timeout
			)
			
			return self.package_response( )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'GoogleWeather'
			exception.method = (
					'fetch_hourly_history( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_alerts( self, address: str, language_code: str = 'en',
			time: int = 10 ) -> Dict[ str, Any ] | None:
		"""Fetch alerts.
		
		Purpose:
			Retrieves alerts using validated arguments and the stored GoogleWeather runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			address (str): address value used by the fetch alerts operation.
			language_code (str): language code value used by the fetch alerts operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'address', address )
			throw_if( 'language_code', language_code )
			throw_if( 'time', time )
			
			self.mode = 'alerts'
			self.language_code = str( language_code ).strip( )
			self.timeout = int( time )
			self.latitude, self.longitude = self.resolve_coordinates( address )
			self.params = {
					'location.latitude': self.latitude,
					'location.longitude': self.longitude,
					'languageCode': self.language_code
			}
			
			self.request(
				path='publicAlerts:lookup',
				params=self.params,
				time=self.timeout
			)
			
			return self.package_response( )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'GoogleWeather'
			exception.method = (
					'fetch_alerts( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception

class NavalObservatory( Fetcher ):
	"""Naval Observatory fetcher.
	
	Purpose:
		Coordinates U.S. Naval Observatory celestial-navigation data within Fonky. The class
		stores provider configuration, request parameters, response payloads, and normalized
		result state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		date_value (Optional[str]): date value state retained by the instance.
		time_value (Optional[str]): time value state retained by the instance.
		latitude (Optional[float]): latitude state retained by the instance.
		longitude (Optional[float]): longitude state retained by the instance.
		location_label (Optional[str]): location label state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	url: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	date_value: Optional[ str ]
	time_value: Optional[ str ]
	latitude: Optional[ float ]
	longitude: Optional[ float ]
	location_label: Optional[ str ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize NavalObservatory.
		
		Purpose:
			Initializes the NavalObservatory instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.headers = { }
		self.base_url = 'https://aa.usno.navy.mil/api'
		self.url = None
		self.params = { }
		self.date_value = ''
		self.time_value = ''
		self.latitude = 38.9072
		self.longitude = -77.0369
		self.location_label = ''
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [ 'base_url', 'url', 'params', 'date_value', 'time_value', 'latitude', 'longitude',
		         'location_label', 'fetch_celnav', 'fetch', 'create_schema' ]
	
	def validate_date( self, date_value: str ) -> str:
		"""Validate date.
		
		Purpose:
			Validates and normalizes date before it is used in U.S. Naval Observatory
			celestial-navigation data. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			date_value (str): date value value used by the validate date operation.
		
		Returns:
			str: Validated date value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( date_value ).strip( )
			throw_if( 'date_value', value )
			dt.datetime.strptime( value, '%Y-%m-%d' )
			return value
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'NavalObservatory'
			exception.method = 'validate_date( self, date_value: str ) -> str'
			raise exception
	
	def validate_time( self, time_value: str ) -> str:
		"""Validate time.
		
		Purpose:
			Validates and normalizes time before it is used in U.S. Naval Observatory
			celestial-navigation data. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			time_value (str): time value value used by the validate time operation.
		
		Returns:
			str: Validated time value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( time_value ).strip( )
			throw_if( 'time_value', value )
			pattern = (r'^(?:[01]\d|2[0-3]):[0-5]\d'
			           r'(?:'
			           r':[0-5]\d(?:\.\d{1,6})?'
			           r')?$')
			
			if not re.fullmatch( pattern, value ):
				raise ValueError( "Invalid time format. Use HH:MM, HH:MM:SS, or HH:MM:SS.S" )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'NavalObservatory'
			exception.method = 'validate_time( self, time_value: str ) -> str'
			raise exception
	
	def validate_coordinates( self, latitude: float, longitude: float ) -> tuple[ float, float ]:
		"""Validate coordinates.
		
		Purpose:
			Validates and normalizes coordinates before it is used in U.S. Naval Observatory
			celestial-navigation data. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			latitude (float): latitude value used by the validate coordinates operation.
			longitude (float): longitude value used by the validate coordinates operation.
		
		Returns:
			tuple[float, float]: Validated coordinates value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			lat = float( latitude )
			lon = float( longitude )
			if lat < -90.0 or lat > 90.0:
				raise ValueError( 'Latitude must be between -90 and 90.' )
			
			if lon < -180.0 or lon > 180.0:
				raise ValueError( 'Longitude must be between -180 and 180.' )
			
			return lat, lon
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'NavalObservatory'
			exception.method = 'validate_coordinates( self, *params ) -> tuple[ float, float ]'
			raise exception
	
	def fetch_celnav( self, date_value: str, time_value: str, latitude: float,
			longitude: float, location_label: str = '', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch celnav.
		
		Purpose:
			Retrieves celnav using validated arguments and the stored NavalObservatory runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			date_value (str): date value value used by the fetch celnav operation.
			time_value (str): time value value used by the fetch celnav operation.
			latitude (float): latitude value used by the fetch celnav operation.
			longitude (float): longitude value used by the fetch celnav operation.
			location_label (str): location label value used by the fetch celnav operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.date_value = self.validate_date( date_value )
			self.time_value = self.validate_time( time_value )
			self.latitude, self.longitude = self.validate_coordinates( latitude=latitude,
				longitude=longitude )
			self.location_label = str( location_label or '' ).strip( )
			self.url = f'{self.base_url}/celnav'
			self.params = { 'date': self.date_value, 'time': self.time_value,
			                'coords': f'{self.latitude},{self.longitude}' }
			
			self.response = requests.get( url=self.url, params=self.params,
				headers=self.headers, timeout=int( time ) )
			self.response.raise_for_status( )
			payload = self.response.json( ) or { }
			
			return { 'mode': 'celnav', 'url': self.url, 'params': self.params,
			         'location_label': self.location_label, 'data': payload }
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'NavalObservatory'
			exception.method = 'fetch_celnav( self, *params ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch( self, mode: str = 'celnav', date_value: str = '',
			time_value: str = '', latitude: float = 0.0, longitude: float = 0.0,
			location_label: str = '', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch U.S. Naval Observatory celestial-navigation data.
		
		Purpose:
			Retrieves U.S. Naval Observatory celestial-navigation data using validated arguments and
			the stored NavalObservatory runtime configuration. The method assembles request
			parameters, executes the provider call or dispatches to a specialized helper, records
			response state when applicable, and returns a normalized payload for downstream analysis
			or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			date_value (str): date value value used by the fetch operation.
			time_value (str): time value value used by the fetch operation.
			latitude (float): latitude value used by the fetch operation.
			longitude (float): longitude value used by the fetch operation.
			location_label (str): location label value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			active_mode = str( mode or 'celnav' ).strip( ).lower( )
			if active_mode == 'celnav':
				return self.fetch_celnav( date_value=date_value, time_value=time_value,
					latitude=latitude, longitude=longitude, location_label=location_label,
					time=time )
			
			raise ValueError( 'Unsupported mode.' )
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'NavalObservatory'
			exception.method = 'fetch( self, **kwargs ) -> Dict[ str, Any ]'
			raise exception
	
	def create_schema( self, function: str, tool: str, description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} '
							f'This function uses the {tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'NavalObservatory'
			exception.method = 'create_schema( self, *params ) -> Dict[ str, str ]'
			raise exception

class SatelliteCenter( Fetcher ):
	"""Satellite Center fetcher.
	
	Purpose:
		Coordinates SSC satellite observatory, ground-station, and location data within Fonky.
		The class stores provider configuration, request parameters, response payloads, and
		normalized result state so callers can access the service through a consistent fetcher
		interface.
	
	Attributes:
		ssc (Optional[SscWs]): ssc state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		observatories (Optional[List[Dict[str, Any]]]): observatories state retained by the
			instance.
		ground_stations (Optional[List[Dict[str, Any]]]): ground stations state retained by the
			instance.
		timeout (Optional[int]): timeout state retained by the instance.
		headers (object): headers state retained by the instance.
		agents (object): agents state retained by the instance."""
	ssc: Optional[ SscWs ]
	url: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	observatories: Optional[ List[ Dict[ str, Any ] ] ]
	ground_stations: Optional[ List[ Dict[ str, Any ] ] ]
	timeout: Optional[ int ]
	
	def __init__( self ) -> None:
		"""Initialize SatelliteCenter.
		
		Purpose:
			Initializes the SatelliteCenter instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.ssc = None
		self.url = 'https://sscweb.gsfc.nasa.gov/WS/sscr/2'
		self.params = { }
		self.observatories = [ ]
		self.ground_stations = [ ]
		self.timeout = 20
		self.headers = { }
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
		
		if 'Accept' not in self.headers:
			self.headers[ 'Accept' ] = 'application/json'
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [ 'url', 'timeout', 'headers', 'fetch_observatories', 'fetch_ground_stations',
		         'fetch_locations', 'fetch', ]
	
	def fetch_observatories( self ) -> Dict[ str, Any ] | None:
		"""Fetch observatories.
		
		Purpose:
			Retrieves observatories using validated arguments and the stored SatelliteCenter runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.ssc = SscWs( user_agent=self.agents, timeout=self.timeout )
			result = self.ssc.get_observatories( )
			return result
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'SatelliteCenter'
			exception.method = 'fetch_observatories( self ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_ground_stations( self ) -> Dict[ str, Any ] | None:
		"""Fetch ground stations.
		
		Purpose:
			Retrieves ground stations using validated arguments and the stored SatelliteCenter
			runtime configuration. The method assembles request parameters, executes the provider
			call or dispatches to a specialized helper, records response state when applicable, and
			returns a normalized payload for downstream analysis or tool execution.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.ssc = SscWs( user_agent=self.agents, timeout=self.timeout )
			result = self.ssc.get_ground_stations( )
			return result
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'SatelliteCenter'
			exception.method = 'fetch_ground_stations( self ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_locations( self, observatories: str, start_time: str, end_time: str,
			coordinate_systems: str = 'gse', resolution_factor: int = 1,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch locations.
		
		Purpose:
			Retrieves locations using validated arguments and the stored SatelliteCenter runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			observatories (str): observatories value used by the fetch locations operation.
			start_time (str): start time value used by the fetch locations operation.
			end_time (str): end time value used by the fetch locations operation.
			coordinate_systems (str): coordinate systems value used by the fetch locations
				operation.
			resolution_factor (int): resolution factor value used by the fetch locations operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'observatories', observatories )
			throw_if( 'start_time', start_time )
			throw_if( 'end_time', end_time )
			self.timeout = int( time )
			obs = observatories.strip( )
			time_range = f'{start_time.strip( )},{end_time.strip( )}'
			coords = (coordinate_systems or 'gse').strip( )
			request_url = (f'{self.url}/locations/'
			               f'{obs}/'
			               f'{time_range}/'
			               f'{coords}/')
			
			self.params = { 'resolutionFactor': max( 1, int( resolution_factor ) ) }
			self.response = requests.get( url=request_url, params=self.params, headers=self.headers,
				timeout=self.timeout )
			
			self.response.raise_for_status( )
			return self.response.json( )
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'SatelliteCenter'
			exception.method = 'fetch_locations( self, *params ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch( self, mode: str = 'observatories', query: str = '', start_time: str = '',
			end_time: str = '',
			coordinate_systems: str = 'gse', resolution_factor: int = 1, time: int = 20 ) -> Dict[
				                                                                                 str, Any ] | None:
		"""Fetch SSC satellite observatory, ground-station, and location data.
		
		Purpose:
			Retrieves SSC satellite observatory, ground-station, and location data using validated
			arguments and the stored SatelliteCenter runtime configuration. The method assembles
			request parameters, executes the provider call or dispatches to a specialized helper,
			records response state when applicable, and returns a normalized payload for downstream
			analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			query (str): Search text, lookup value, or provider query submitted by the caller.
			start_time (str): start time value used by the fetch operation.
			end_time (str): end time value used by the fetch operation.
			coordinate_systems (str): coordinate systems value used by the fetch operation.
			resolution_factor (int): resolution factor value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			active_mode = (mode or 'observatories').strip( ).lower( )
			if active_mode == 'observatories':
				return self.fetch_observatories( )
			
			if active_mode == 'ground_stations':
				return self.fetch_ground_stations( )
			
			if active_mode == 'locations':
				return self.fetch_locations( observatories=query, start_time=start_time,
					end_time=end_time, coordinate_systems=coordinate_systems,
					resolution_factor=resolution_factor, time=time )
			
			raise ValueError( "Use 'observatories', 'ground_stations', or 'locations'." )
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'SatelliteCenter'
			exception.method = 'fetch( self, *kwargs ) -> Dict[ str, Any ]'
			raise exception

class EarthObservatory( Fetcher ):
	"""Earth Observatory fetcher.
	
	Purpose:
		Coordinates NASA EONET events, categories, sources, and layers within Fonky. The class
		stores provider configuration, request parameters, response payloads, and normalized
		result state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		status (Optional[str]): status state retained by the instance.
		category (Optional[str]): category state retained by the instance.
		source (Optional[str]): source state retained by the instance.
		days (Optional[int]): days state retained by the instance.
		limit (Optional[int]): limit state retained by the instance.
		start_date (Optional[str]): start date state retained by the instance.
		end_date (Optional[str]): end date state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	url: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	mode: Optional[ str ]
	status: Optional[ str ]
	category: Optional[ str ]
	source: Optional[ str ]
	days: Optional[ int ]
	limit: Optional[ int ]
	start_date: Optional[ str ]
	end_date: Optional[ str ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize EarthObservatory.
		
		Purpose:
			Initializes the EarthObservatory instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.headers = { }
		self.base_url = 'https://eonet.gsfc.nasa.gov/api/v3'
		self.url = None
		self.params = { }
		self.mode = 'events'
		self.status = 'open'
		self.category = ''
		self.source = ''
		self.days = 30
		self.limit = 20
		self.start_date = ''
		self.end_date = ''
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'url',
				'params',
				'mode',
				'status',
				'category',
				'source',
				'days',
				'limit',
				'start_date',
				'end_date',
				'fetch_events',
				'fetch_categories',
				'fetch_sources',
				'fetch_layers',
				'fetch',
				'create_schema'
		]
	
	def fetch_events( self, status: str = 'open', category: str = '', source: str = '',
			limit: int = 20,
			days: int = 30, start_date: str = '', end_date: str = '', time: int = 20 ) -> Dict[
		str, Any ]:
		"""Fetch events.
		
		Purpose:
			Retrieves events using validated arguments and the stored EarthObservatory runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			status (str): status value used by the fetch events operation.
			category (str): category value used by the fetch events operation.
			source (str): source value used by the fetch events operation.
			limit (int): limit value used by the fetch events operation.
			days (int): days value used by the fetch events operation.
			start_date (str): start date value used by the fetch events operation.
			end_date (str): end date value used by the fetch events operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any]: Normalized provider response, result payload, or document collection
				returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'events'
			self.status = str( status or 'open' ).strip( ).lower( )
			self.category = str( category or '' ).strip( )
			self.source = str( source or '' ).strip( )
			self.limit = int( limit )
			self.days = int( days )
			self.start_date = str( start_date or '' ).strip( )
			self.end_date = str( end_date or '' ).strip( )
			self.url = f'{self.base_url}/events'
			self.params = { }
			
			if self.status:
				self.params[ 'status' ] = self.status
			
			if self.category:
				self.params[ 'category' ] = self.category
			
			if self.source:
				self.params[ 'source' ] = self.source
			
			if self.limit > 0:
				self.params[ 'limit' ] = self.limit
			
			if self.start_date and self.end_date:
				self.params[ 'start' ] = self.start_date
				self.params[ 'end' ] = self.end_date
			elif self.days > 0:
				self.params[ 'days' ] = self.days
			
			self.response = requests.get( url=self.url, params=self.params, headers=self.headers,
				timeout=int( time ) )
			self.response.raise_for_status( )
			payload = self.response.json( ) or { }
			
			return {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'events': payload.get( 'events', [ ] ),
					'title': payload.get( 'title', '' ),
					'description': payload.get( 'description', '' )
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EarthObservatory'
			exception.method = 'fetch_events( self, **kwargs ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_categories( self, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch categories.
		
		Purpose:
			Retrieves categories using validated arguments and the stored EarthObservatory runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'categories'
			self.url = f'{self.base_url}/categories'
			self.params = { }
			self.response = requests.get( url=self.url, params=self.params, headers=self.headers,
				timeout=int( time ) )
			self.response.raise_for_status( )
			payload = self.response.json( ) or { }
			return {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'categories': payload.get( 'categories', [ ] ),
					'title': payload.get( 'title', '' ),
					'description': payload.get( 'description', '' )
			}
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EarthObservatory'
			exception.method = 'fetch_categories( self, time: int=20 ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_sources( self, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch sources.
		
		Purpose:
			Retrieves sources using validated arguments and the stored EarthObservatory runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'sources'
			self.url = f'{self.base_url}/sources'
			self.params = { }
			self.response = requests.get( url=self.url, params=self.params, headers=self.headers,
				timeout=int( time ) )
			self.response.raise_for_status( )
			payload = self.response.json( ) or { }
			return {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'sources': payload.get( 'sources', [ ] ),
					'title': payload.get( 'title', '' ),
					'description': payload.get( 'description', '' )
			}
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EarthObservatory'
			exception.method = 'fetch_sources( self, time: int=20 ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_layers( self, category: str = '', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch layers.
		
		Purpose:
			Retrieves layers using validated arguments and the stored EarthObservatory runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			category (str): category value used by the fetch layers operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'layers'
			self.category = str( category or '' ).strip( )
			if self.category:
				self.url = f'{self.base_url}/layers/{self.category}'
			else:
				self.url = f'{self.base_url}/layers'
			
			self.params = { }
			self.response = requests.get( url=self.url, params=self.params, headers=self.headers,
				timeout=int( time ) )
			self.response.raise_for_status( )
			payload = self.response.json( ) or { }
			return {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'category': self.category,
					'layers': payload.get( 'layers', [ ] ),
					'title': payload.get( 'title', '' ),
					'description': payload.get( 'description', '' )
			}
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EarthObservatory'
			exception.method = 'fetch_layers( self, c**kwargs ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch( self, mode: str = 'events', status: str = 'open', category: str = '',
			source: str = '', limit: int = 20,
			days: int = 30, start_date: str = '', end_date: str = '', time: int = 20 ) -> Dict[
		str, Any ]:
		"""Fetch NASA EONET events, categories, sources, and layers.
		
		Purpose:
			Retrieves NASA EONET events, categories, sources, and layers using validated arguments
			and the stored EarthObservatory runtime configuration. The method assembles request
			parameters, executes the provider call or dispatches to a specialized helper, records
			response state when applicable, and returns a normalized payload for downstream analysis
			or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			status (str): status value used by the fetch operation.
			category (str): category value used by the fetch operation.
			source (str): source value used by the fetch operation.
			limit (int): limit value used by the fetch operation.
			days (int): days value used by the fetch operation.
			start_date (str): start date value used by the fetch operation.
			end_date (str): end date value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any]: Normalized provider response, result payload, or document collection
				returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			active_mode = (mode or 'events').strip( ).lower( )
			if active_mode == 'events':
				return self.fetch_events( status=status, category=category, source=source,
					limit=limit, days=days, start_date=start_date, end_date=end_date, time=time )
			
			if active_mode == 'categories':
				return self.fetch_categories( time=time )
			
			if active_mode == 'sources':
				return self.fetch_sources( time=time )
			
			if active_mode == 'layers':
				return self.fetch_layers( category=category, time=time )
			
			raise ValueError( "Use 'events', 'categories', 'sources', or 'layers'." )
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'EarthObservatory'
			exception.method = 'fetch( self, **kwargs ) -> Dict[ str, Any ]'
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': f'{description.strip( )} This function uses the {tool.strip( )} service.',
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EarthObservatory'
			exception.method = (
					'create_schema( self, function: str, tool: str, description: str, '
					'parameters: dict, required: list[ str ] ) -> Dict[ str, str ]'
			)
			raise exception

class GlobalImagery( Fetcher ):
	"""Global Imagery fetcher.
	
	Purpose:
		Coordinates NASA GIBS WMS imagery and map service retrieval within Fonky. The class
		stores provider configuration, request parameters, response payloads, and normalized
		result state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		file_path (Optional[str]): file path state retained by the instance.
		api_key (Optional[str]): API key state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		latitude (Optional[float]): latitude state retained by the instance.
		longitude (Optional[float]): longitude state retained by the instance.
		coordinates (Optional[Tuple[float, float]]): coordinates state retained by the instance.
		calendar_date (Optional[dt.datetime]): calendar date state retained by the instance.
		julian_date (Optional[float]): julian date state retained by the instance.
		sidereal_time (Optional[str]): sidereal time state retained by the instance.
		utc_time (Optional[dt.time]): utc time state retained by the instance.
		local_time (Optional[dt.time]): local time state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		era (Optional[str]): era state retained by the instance.
		year (Optional[str]): year state retained by the instance.
		month (Optional[str]): month state retained by the instance.
		day (Optional[str]): day state retained by the instance.
		mode (object): mode state retained by the instance.
		fetcher (object): fetcher state retained by the instance.
		response (object): response state retained by the instance.
		result (object): result state retained by the instance.
		timeout (object): timeout state retained by the instance.
		agents (object): agents state retained by the instance.
		headers (object): headers state retained by the instance."""
	file_path: Optional[ str ]
	api_key: Optional[ str ]
	url: Optional[ str ]
	latitude: Optional[ float ]
	longitude: Optional[ float ]
	coordinates: Optional[ Tuple[ float, float ] ]
	calendar_date: Optional[ dt.datetime ]
	julian_date: Optional[ float ]
	sidereal_time: Optional[ str ]
	utc_time: Optional[ dt.time ]
	local_time: Optional[ dt.time ]
	params: Optional[ Dict[ str, Any ] ]
	era: Optional[ str ]
	year: Optional[ str ]
	month: Optional[ str ]
	day: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize GlobalImagery.
		
		Purpose:
			Initializes the GlobalImagery instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.api_key = cfg.NASA_API_KEY
		self.mode = None
		self.url = 'https://gibs.earthdata.nasa.gov/wms'
		self.file_path = None
		self.longitude = None
		self.latitude = None
		self.coordinates = None
		self.fetcher = None
		self.calendar_date = None
		self.julian_date = None
		self.sidereal_time = None
		self.local_time = None
		self.utc_time = None
		self.params = { }
		self.response = None
		self.result = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = { }
		self.headers[ 'User-Agent' ] = self.agents
		self.era = None
		self.year = None
		self.month = None
		self.day = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'file_path',
				'api_key',
				'url',
				'latitude',
				'longitude',
				'coordinates',
				'calendar_date',
				'julian_date',
				'sidereal_time',
				'utc_time',
				'local_time',
				'params',
				'response',
				'result',
				'mode',
				'timeout',
				'headers',
				'get_capabilities_url',
				'build_wms_url',
				'fetch_wms_map',
				'fetch_map_services',
				'fetch_mercator_map',
				'create_schema'
		]
	
	def get_capabilities_url( self, projection: str = 'epsg4326',
			quality: str = 'best', version: str = '1.1.1' ) -> str:
		"""Get capabilities url.
		
		Purpose:
			Performs the get capabilities url operation for NASA GIBS WMS imagery and map service
			retrieval. The method uses the class runtime state and supplied arguments to prepare,
			transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			projection (str): projection value used by the get capabilities url operation.
			quality (str): quality value used by the get capabilities url operation.
			version (str): version value used by the get capabilities url operation.
		
		Returns:
			str: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			projection_value = str( projection or 'epsg4326' ).strip( ).lower( )
			quality_value = str( quality or 'best' ).strip( ).lower( )
			version_value = str( version or '1.1.1' ).strip( )
			
			base_url = (
					f'https://gibs.earthdata.nasa.gov/wms/'
					f'{projection_value}/{quality_value}/wms.cgi'
			)
			
			params = {
					'SERVICE': 'WMS',
					'REQUEST': 'GetCapabilities',
					'VERSION': version_value
			}
			
			return f'{base_url}?{urllib.parse.urlencode( params )}'
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GlobalImagery'
			exception.method = (
					'get_capabilities_url( self, projection: str="epsg4326", '
					'quality: str="best", version: str="1.1.1" ) -> str'
			)
			raise exception
	
	def build_wms_url( self, layer: str, image_date: str, bbox: Tuple[ float, float, float, float ],
			width: int = 1200, height: int = 600, projection: str = 'epsg4326',
			quality: str = 'best', image_format: str = 'image/png',
			transparent: bool = True, version: str = '1.1.1' ) -> str:
		"""Build wms url.
		
		Purpose:
			Constructs wms url from validated inputs and stored runtime configuration. The method
			centralizes URL, parameter, or payload assembly so fetch operations can issue provider
			requests using a predictable structure.
		
		Args:
			layer (str): layer value used by the build wms url operation.
			image_date (str): image date value used by the build wms url operation.
			bbox (Tuple[float, float, float, float]): bbox value used by the build wms url
				operation.
			width (int): width value used by the build wms url operation.
			height (int): height value used by the build wms url operation.
			projection (str): projection value used by the build wms url operation.
			quality (str): quality value used by the build wms url operation.
			image_format (str): image format value used by the build wms url operation.
			transparent (bool): transparent value used by the build wms url operation.
			version (str): version value used by the build wms url operation.
		
		Returns:
			str: Constructed URL, query, payload, or request structure.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'layer', layer )
			throw_if( 'image_date', image_date )
			throw_if( 'bbox', bbox )
			
			if len( bbox ) != 4:
				raise ValueError( 'bbox must contain west, south, east, north.' )
			
			projection_value = str( projection or 'epsg4326' ).strip( ).lower( )
			quality_value = str( quality or 'best' ).strip( ).lower( )
			version_value = str( version or '1.1.1' ).strip( )
			
			west, south, east, north = [ float( value ) for value in bbox ]
			width_value = max( 1, int( width ) )
			height_value = max( 1, int( height ) )
			
			base_url = (
					f'https://gibs.earthdata.nasa.gov/wms/'
					f'{projection_value}/{quality_value}/wms.cgi'
			)
			
			params = {
					'SERVICE': 'WMS',
					'VERSION': version_value,
					'REQUEST': 'GetMap',
					'LAYERS': str( layer ).strip( ),
					'STYLES': '',
					'FORMAT': str( image_format or 'image/png' ).strip( ),
					'TRANSPARENT': str( bool( transparent ) ).lower( ),
					'SRS': 'EPSG:4326' if projection_value == 'epsg4326' else 'EPSG:3857',
					'BBOX': f'{west},{south},{east},{north}',
					'WIDTH': width_value,
					'HEIGHT': height_value,
					'TIME': str( image_date ).strip( )
			}
			
			self.params = params
			return f'{base_url}?{urllib.parse.urlencode( params )}'
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GlobalImagery'
			exception.method = (
					'build_wms_url( self, layer: str, image_date: str, '
					'bbox: Tuple[ float, float, float, float ], width: int=1200, '
					'height: int=600, projection: str="epsg4326", quality: str="best", '
					'image_format: str="image/png", transparent: bool=True, '
					'version: str="1.1.1" ) -> str'
			)
			raise exception
	
	def fetch_wms_map( self, layer: str, image_date: str,
			bbox: Tuple[ float, float, float, float ], width: int = 1200, height: int = 600,
			projection: str = 'epsg4326', quality: str = 'best',
			image_format: str = 'image/png', transparent: bool = True,
			output_dir: str = 'python-examples', output_name: str = '',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch wms map.
		
		Purpose:
			Retrieves wms map using validated arguments and the stored GlobalImagery runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			layer (str): layer value used by the fetch wms map operation.
			image_date (str): image date value used by the fetch wms map operation.
			bbox (Tuple[float, float, float, float]): bbox value used by the fetch wms map
				operation.
			width (int): width value used by the fetch wms map operation.
			height (int): height value used by the fetch wms map operation.
			projection (str): projection value used by the fetch wms map operation.
			quality (str): quality value used by the fetch wms map operation.
			image_format (str): image format value used by the fetch wms map operation.
			transparent (bool): transparent value used by the fetch wms map operation.
			output_dir (str): output dir value used by the fetch wms map operation.
			output_name (str): output name value used by the fetch wms map operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'wms_map'
			self.timeout = int( time )
			
			request_url = self.build_wms_url(
				layer=layer,
				image_date=image_date,
				bbox=bbox,
				width=width,
				height=height,
				projection=projection,
				quality=quality,
				image_format=image_format,
				transparent=transparent )
			
			directory = Path( output_dir or 'python-examples' )
			directory.mkdir( parents=True, exist_ok=True )
			
			if output_name:
				filename = output_name
			else:
				safe_layer = re.sub( r'[^A-Za-z0-9_\-]+', '_', str( layer ).strip( ) )
				safe_date = re.sub( r'[^0-9\-]+', '_', str( image_date ).strip( ) )
				extension = '.jpg' if image_format == 'image/jpeg' else '.png'
				filename = f'{safe_layer}_{safe_date}{extension}'
			
			self.file_path = str( directory / filename )
			self.url = request_url
			self.response = requests.get( request_url, headers=self.headers,
				timeout=self.timeout )
			self.response.raise_for_status( )
			
			content_type = self.response.headers.get( 'Content-Type', '' )
			if 'image' not in content_type.lower( ):
				message = (
						'NASA GIBS did not return an image. '
						f'Content-Type: {content_type}. '
						f'Response preview: {self.response.text[ :500 ]}'
				)
				raise ValueError( message )
			
			Path( self.file_path ).write_bytes( self.response.content )
			
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'image_path': self.file_path,
					'content_type': content_type,
					'status_code': self.response.status_code,
					'bytes': len( self.response.content ),
					'layer': layer,
					'image_date': image_date,
					'bbox': {
							'west': float( bbox[ 0 ] ),
							'south': float( bbox[ 1 ] ),
							'east': float( bbox[ 2 ] ),
							'north': float( bbox[ 3 ] )
					},
					'summary': {
							'rows': 1,
							'columns': 8,
							'description': 'NASA GIBS WMS image written to disk.'
					}
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GlobalImagery'
			exception.method = (
					'fetch_wms_map( self, layer: str, image_date: str, '
					'bbox: Tuple[ float, float, float, float ], width: int=1200, '
					'height: int=600, projection: str="epsg4326", quality: str="best", '
					'image_format: str="image/png", transparent: bool=True, '
					'output_dir: str="python-examples", output_name: str="", '
					'time: int=20 ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_map_services( self ) -> Dict[ str, Any ] | None:
		"""Fetch map services.
		
		Purpose:
			Retrieves map services using validated arguments and the stored GlobalImagery runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'fetch_map_services'
			return self.fetch_wms_map( layer='MODIS_Terra_CorrectedReflectance_TrueColor',
				image_date='2021-09-21', bbox=(-180.0, -90.0, 180.0, 90.0),
				width=1200, height=600, projection='epsg4326', quality='best',
				image_format='image/png', transparent=True, output_dir='python-examples',
				output_name='MODIS_Terra_CorrectedReflectance_TrueColor.png',
				time=20 )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GlobalImagery'
			exception.method = 'fetch_map_services( self ) -> Dict[ str, Any ] | None'
			raise exception
	
	def fetch_mercator_map( self, ccrs=None ) -> Dict[ str, Any ] | None:
		"""Fetch mercator map.
		
		Purpose:
			Retrieves mercator map using validated arguments and the stored GlobalImagery runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			ccrs (object): ccrs value used by the fetch mercator map operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'mercator_map'
			return self.fetch_wms_map(
				layer='Landsat_WELD_CorrectedReflectance_Bands157_Global_Annual',
				image_date='2000-12-01', bbox=(-8000000.0, -8000000.0, 8000000.0, 8000000.0),
				width=600, height=600, projection='epsg3857', quality='best',
				image_format='image/png', transparent=True, output_dir='python-examples',
				output_name='Landsat_WELD_CorrectedReflectance_Bands157_Global_Annual.png',
				time=20 )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GlobalImagery'
			exception.method = 'fetch_mercator_map( self, ccrs=None ) -> Dict[ str, Any ] | None'
			raise exception
	
	def create_schema( self, function: str, tool: str, description: str,
			parameters: dict, required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if not isinstance( parameters, dict ):
				raise ValueError( 'parameters must be a dict of parameter schema definitions.' )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': f'{description.strip( )} This function uses the {tool.strip( )} service.',
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GlobalImagery'
			exception.method = (
					'create_schema( self, function: str, tool: str, description: str, '
					'parameters: dict, required: list[ str ] ) -> Dict[ str, str ] | None'
			)
			raise exception

class NearbyObjects( Fetcher ):
	"""Nearby Objects fetcher.
	
	Purpose:
		Coordinates JPL SSD and CNEOS near-Earth object data within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		start_date (Optional[str]): start date state retained by the instance.
		end_date (Optional[str]): end date state retained by the instance.
		query (Optional[str]): query state retained by the instance.
		dist_max (Optional[str]): dist max state retained by the instance.
		body (Optional[str]): body state retained by the instance.
		sort (Optional[str]): sort state retained by the instance.
		limit (Optional[int]): limit state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	url: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	mode: Optional[ str ]
	start_date: Optional[ str ]
	end_date: Optional[ str ]
	query: Optional[ str ]
	dist_max: Optional[ str ]
	body: Optional[ str ]
	sort: Optional[ str ]
	limit: Optional[ int ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize NearbyObjects.
		
		Purpose:
			Initializes the NearbyObjects instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.headers = { }
		self.base_url = 'https://ssd-api.jpl.nasa.gov'
		self.url = None
		self.params = { }
		self.mode = 'close_approaches'
		self.start_date = ''
		self.end_date = ''
		self.query = ''
		self.dist_max = '10LD'
		self.body = 'Earth'
		self.sort = 'date'
		self.limit = 20
		self.agents = cfg.AGENTS
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'url',
				'params',
				'mode',
				'start_date',
				'end_date',
				'query',
				'dist_max',
				'body',
				'sort',
				'limit',
				'fetch_close_approaches',
				'fetch_object_lookup',
				'fetch_nhats_summary',
				'fetch_nhats_object',
				'fetch_fireballs',
				'fetch',
				'create_schema'
		]
	
	def fetch_close_approaches( self, start_date: str, end_date: str, dist_max: str = '10LD',
			body: str = 'Earth', sort: str = 'date', limit: int = 20, time: int = 20 ) -> Dict[
				                                                                              str, Any ] | None:
		"""Fetch close approaches.
		
		Purpose:
			Retrieves close approaches using validated arguments and the stored NearbyObjects
			runtime configuration. The method assembles request parameters, executes the provider
			call or dispatches to a specialized helper, records response state when applicable, and
			returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			start_date (str): start date value used by the fetch close approaches operation.
			end_date (str): end date value used by the fetch close approaches operation.
			dist_max (str): dist max value used by the fetch close approaches operation.
			body (str): body value used by the fetch close approaches operation.
			sort (str): sort value used by the fetch close approaches operation.
			limit (int): limit value used by the fetch close approaches operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'start_date', start_date )
			throw_if( 'end_date', end_date )
			self.mode = 'close_approaches'
			self.start_date = str( start_date ).strip( )
			self.end_date = str( end_date ).strip( )
			self.dist_max = str( dist_max or '10LD' ).strip( )
			self.body = str( body or 'Earth' ).strip( )
			self.sort = str( sort or 'date' ).strip( )
			self.limit = int( limit )
			self.url = f'{self.base_url}/cad.api'
			self.params = {
					'date-min': self.start_date,
					'date-max': self.end_date,
					'dist-max': self.dist_max,
					'body': self.body,
					'sort': self.sort,
					'limit': self.limit
			}
			self.response = requests.get( url=self.url, params=self.params, headers=self.headers,
				timeout=int( time ) )
			self.response.raise_for_status( )
			payload = self.response.json( ) or { }
			
			return {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'count': payload.get( 'count', 0 ),
					'fields': payload.get( 'fields', [ ] ),
					'data': payload.get( 'data', [ ] ),
					'signature': payload.get( 'signature', { } )
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'NearbyObjects'
			exception.method = 'fetch_close_approaches( self, **kwargs ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_object_lookup( self, query: str, query_type: str = 'sstr',
			include_physical: bool = True, include_close_approaches: bool = True,
			ca_body: str = 'Earth', include_discovery: bool = True,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch object lookup.
		
		Purpose:
			Retrieves object lookup using validated arguments and the stored NearbyObjects runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			query (str): Search text, lookup value, or provider query submitted by the caller.
			query_type (str): query type value used by the fetch object lookup operation.
			include_physical (bool): include physical value used by the fetch object lookup
				operation.
			include_close_approaches (bool): include close approaches value used by the fetch object
				lookup operation.
			ca_body (str): ca body value used by the fetch object lookup operation.
			include_discovery (bool): include discovery value used by the fetch object lookup
				operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'query', query )
			throw_if( 'query_type', query_type )
			self.mode = 'object_lookup'
			self.query = str( query ).strip( )
			active_type = str( query_type ).strip( ).lower( )
			if active_type not in [ 'sstr', 'spk', 'des' ]:
				raise ValueError( "query_type must be 'sstr', 'spk', or 'des'." )
			
			self.url = f'{self.base_url}/sbdb.api'
			self.params = {
					active_type: self.query,
					'phys-par': '1' if bool( include_physical ) else '0',
					'ca-data': '1' if bool( include_close_approaches ) else '0',
					'discovery': '1' if bool( include_discovery ) else '0'
			}
			
			if include_close_approaches and str( ca_body or '' ).strip( ):
				self.params[ 'ca-body' ] = str( ca_body ).strip( )
			
			self.response = requests.get( url=self.url, params=self.params, headers=self.headers,
				timeout=int( time ) )
			self.response.raise_for_status( )
			payload = self.response.json( ) or { }
			return {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'data': payload
			}
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'NearbyObjects'
			exception.method = 'fetch_object_lookup( self, **kwargs ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_nhats_summary( self, dv: float = 6.0, dur: int = 360, stay: int = 8,
			launch: str = '2020-2045',
			h: float = 26.0, occ: int = 7, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch nhats summary.
		
		Purpose:
			Retrieves nhats summary using validated arguments and the stored NearbyObjects runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			dv (float): dv value used by the fetch nhats summary operation.
			dur (int): dur value used by the fetch nhats summary operation.
			stay (int): stay value used by the fetch nhats summary operation.
			launch (str): launch value used by the fetch nhats summary operation.
			h (float): h value used by the fetch nhats summary operation.
			occ (int): occ value used by the fetch nhats summary operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'nhats_summary'
			self.url = f'{self.base_url}/nhats.api'
			self.params = {
					'dv': float( dv ),
					'dur': int( dur ),
					'stay': int( stay ),
					'launch': str( launch ).strip( ),
					'h': float( h ),
					'occ': int( occ )
			}
			
			self.response = requests.get( url=self.url, params=self.params, headers=self.headers,
				timeout=int( time ) )
			self.response.raise_for_status( )
			payload = self.response.json( ) or { }
			
			return {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'data': payload
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'NearbyObjects'
			exception.method = 'fetch_nhats_summary( self, **kwargs ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_nhats_object( self, designation: str, dv: float = 6.0, dur: int = 360, stay: int = 8,
			launch: str = '2020-2045', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch nhats object.
		
		Purpose:
			Retrieves nhats object using validated arguments and the stored NearbyObjects runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			designation (str): designation value used by the fetch nhats object operation.
			dv (float): dv value used by the fetch nhats object operation.
			dur (int): dur value used by the fetch nhats object operation.
			stay (int): stay value used by the fetch nhats object operation.
			launch (str): launch value used by the fetch nhats object operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'designation', designation )
			self.mode = 'nhats_object'
			self.query = str( designation ).strip( )
			self.url = f'{self.base_url}/nhats.api'
			self.params = {
					'des': self.query,
					'dv': float( dv ),
					'dur': int( dur ),
					'stay': int( stay ),
					'launch': str( launch ).strip( )
			}
			
			self.response = requests.get( url=self.url, params=self.params,
				headers=self.headers, timeout=int( time ) )
			self.response.raise_for_status( )
			payload = self.response.json( ) or { }
			
			return {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'data': payload
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'NearbyObjects'
			exception.method = 'fetch_nhats_object( self, **kwargs ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_fireballs( self, date_min: str = '', limit: int = 20, time: int = 20 ) -> Dict[
		                                                                                    str, Any ] | None:
		"""Fetch fireballs.
		
		Purpose:
			Retrieves fireballs using validated arguments and the stored NearbyObjects runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			date_min (str): date min value used by the fetch fireballs operation.
			limit (int): limit value used by the fetch fireballs operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'fireballs'
			self.url = f'{self.base_url}/fireball.api'
			self.params = { 'limit': int( limit ) }
			
			if str( date_min or '' ).strip( ):
				self.params[ 'date-min' ] = str( date_min ).strip( )
			
			self.response = requests.get( url=self.url, params=self.params, headers=self.headers,
				timeout=int( time ) )
			self.response.raise_for_status( )
			payload = self.response.json( ) or { }
			
			return {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'count': payload.get( 'count', 0 ),
					'fields': payload.get( 'fields', [ ] ),
					'data': payload.get( 'data', [ ] ),
					'signature': payload.get( 'signature', { } )
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'NearbyObjects'
			exception.method = 'fetch_fireballs( self, **kwargs ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch( self, mode: str = 'close_approaches', start_date: str = '',
			end_date: str = '', query: str = '', query_type: str = 'sstr',
			dist_max: str = '10LD', body: str = 'Earth', sort: str = 'date',
			limit: int = 20, dv: float = 6.0, dur: int = 360,
			stay: int = 8, launch: str = '2020-2045', h: float = 26.0,
			occ: int = 7, include_physical: bool = True,
			include_close_approaches: bool = True, ca_body: str = 'Earth',
			include_discovery: bool = True, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch JPL SSD and CNEOS near-Earth object data.
		
		Purpose:
			Retrieves JPL SSD and CNEOS near-Earth object data using validated arguments and the
			stored NearbyObjects runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			start_date (str): start date value used by the fetch operation.
			end_date (str): end date value used by the fetch operation.
			query (str): Search text, lookup value, or provider query submitted by the caller.
			query_type (str): query type value used by the fetch operation.
			dist_max (str): dist max value used by the fetch operation.
			body (str): body value used by the fetch operation.
			sort (str): sort value used by the fetch operation.
			limit (int): limit value used by the fetch operation.
			dv (float): dv value used by the fetch operation.
			dur (int): dur value used by the fetch operation.
			stay (int): stay value used by the fetch operation.
			launch (str): launch value used by the fetch operation.
			h (float): h value used by the fetch operation.
			occ (int): occ value used by the fetch operation.
			include_physical (bool): include physical value used by the fetch operation.
			include_close_approaches (bool): include close approaches value used by the fetch
				operation.
			ca_body (str): ca body value used by the fetch operation.
			include_discovery (bool): include discovery value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			active_mode = str( mode or 'close_approaches' ).strip( ).lower( )
			
			if active_mode == 'close_approaches':
				return self.fetch_close_approaches( start_date=start_date, end_date=end_date,
					dist_max=dist_max, body=body, sort=sort, limit=limit,
					time=time )
			
			if active_mode == 'object_lookup':
				return self.fetch_object_lookup( query=query, query_type=query_type,
					include_physical=include_physical,
					include_close_approaches=include_close_approaches, ca_body=ca_body,
					include_discovery=include_discovery, time=time )
			
			if active_mode == 'nhats_summary':
				return self.fetch_nhats_summary( dv=dv, dur=dur, stay=stay, launch=launch,
					h=h, occ=occ, time=time )
			
			if active_mode == 'nhats_object':
				return self.fetch_nhats_object( designation=query, dv=dv, dur=dur, stay=stay,
					launch=launch, time=time )
			
			if active_mode == 'fireballs':
				return self.fetch_fireballs( date_min=start_date, limit=limit,
					time=time )
			
			raise ValueError( "Unsupported mode." )
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'NearbyObjects'
			exception.method = 'fetch( self, **kwargs) -> Dict[ str, Any ]'
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': f'{description.strip( )} This function uses the {tool.strip( )} service.',
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'NearbyObjects'
			exception.method = (
					'create_schema( self, function: str, tool: str, description: str, '
					'parameters: dict, required: list[ str ] ) -> Dict[ str, str ]'
			)
			raise exception

class OpenScience( Fetcher ):
	"""Open Science fetcher.
	
	Purpose:
		Coordinates NASA Open Science Data Repository resources within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		query_text (Optional[str]): query text state retained by the instance.
		format_value (Optional[str]): format value state retained by the instance.
		size (Optional[int]): size state retained by the instance.
		endpoint (Optional[str]): endpoint state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	url: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	query_text: Optional[ str ]
	format_value: Optional[ str ]
	size: Optional[ int ]
	endpoint: Optional[ str ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize OpenScience.
		
		Purpose:
			Initializes the OpenScience instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.headers = { }
		self.base_url = 'https://visualization.osdr.nasa.gov/biodata/api'
		self.url = None
		self.params = { }
		self.query_text = ''
		self.format_value = 'json'
		self.size = 100
		self.endpoint = ''
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'url',
				'params',
				'query_text',
				'format_value',
				'size',
				'endpoint',
				'fetch_dataset',
				'fetch_metadata',
				'fetch_assays',
				'fetch_data',
				'fetch',
				'create_schema'
		]
	
	def validate_format( self, format_value: str ) -> str:
		"""Validate format.
		
		Purpose:
			Validates and normalizes format before it is used in NASA Open Science Data Repository
			resources. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			format_value (str): format value value used by the validate format operation.
		
		Returns:
			str: Validated format value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( format_value or 'json' ).strip( ).lower( )
			
			allowed = { 'json', 'csv', 'tsv', 'browser' }
			if value not in allowed:
				raise ValueError(
					"Unsupported format. Use one of: json, csv, tsv, browser."
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenScience'
			exception.method = 'validate_format( self, format_value: str ) -> str'
			raise exception
	
	def coerce_response( self, response: requests.Response ) -> Dict[ str, Any ] | str:
		"""Coerce response.
		
		Purpose:
			Coerces response into a predictable Python representation for downstream handling. The
			method prefers structured data when available and falls back to text or simple
			containers when the provider response cannot be represented more specifically.
		
		Args:
			response (requests.Response): response value used by the coerce response operation.
		
		Returns:
			Dict[str, Any] | str: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			content_type = str( response.headers.get( 'Content-Type', '' ) ).lower( )
			
			if 'application/json' in content_type:
				return response.json( )
			
			try:
				return response.json( )
			except Exception:
				return response.text
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenScience'
			exception.method = (
					'coerce_response( self, response: requests.Response ) '
					'-> Dict[ str, Any ] | str'
			)
			raise exception
	
	def fetch_dataset( self, accession: str, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch dataset.
		
		Purpose:
			Retrieves dataset using validated arguments and the stored OpenScience runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			accession (str): accession value used by the fetch dataset operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'accession', accession )
			value = str( accession ).strip( )
			self.endpoint = f'/v2/dataset/{value}/'
			self.url = f'{self.base_url}{self.endpoint}'
			self.params = { }
			self.response = requests.get( url=self.url, params=self.params, headers=self.headers,
				timeout=int( time ) )
			self.response.raise_for_status( )
			
			return {
					'mode': 'dataset',
					'url': self.url,
					'params': self.params,
					'data': self.coerce_response( self.response )
			}
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenScience'
			exception.method = 'fetch_dataset( self, **kwargs ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_metadata( self, query: str, format_value: str = 'json',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch metadata.
		
		Purpose:
			Retrieves metadata using validated arguments and the stored OpenScience runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			query (str): Search text, lookup value, or provider query submitted by the caller.
			format_value (str): format value value used by the fetch metadata operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'query', query )
			self.query_text = str( query ).strip( )
			self.format_value = self.validate_format( format_value )
			self.endpoint = '/v2/query/metadata/'
			self.url = f'{self.base_url}{self.endpoint}'
			self.params = { 'query': self.query_text, 'format': self.format_value }
			self.response = requests.get( url=self.url, params=self.params,
				headers=self.headers, timeout=int( time ) )
			self.response.raise_for_status( )
			
			return {
					'mode': 'metadata',
					'url': self.url,
					'params': self.params,
					'data': self.coerce_response( self.response )
			}
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenScience'
			exception.method = (
					'fetch_metadata( self, query: str, format_value: str=json, '
					'time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_assays( self, query: str, format_value: str = 'json',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch assays.
		
		Purpose:
			Retrieves assays using validated arguments and the stored OpenScience runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			query (str): Search text, lookup value, or provider query submitted by the caller.
			format_value (str): format value value used by the fetch assays operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'query', query )
			
			self.query_text = str( query ).strip( )
			self.format_value = self.validate_format( format_value )
			self.endpoint = '/v2/query/assays/'
			self.url = f'{self.base_url}{self.endpoint}'
			self.params = {
					'query': self.query_text,
					'format': self.format_value
			}
			
			self.response = requests.get( url=self.url, params=self.params, headers=self.headers,
				timeout=int( time ) )
			self.response.raise_for_status( )
			
			return {
					'mode': 'assays',
					'url': self.url,
					'params': self.params,
					'data': self.coerce_response( self.response )
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenScience'
			exception.method = (
					'fetch_assays( self, query: str, format_value: str=json, '
					'time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_data( self, query: str, format_value: str = 'json',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch data.
		
		Purpose:
			Retrieves data using validated arguments and the stored OpenScience runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			query (str): Search text, lookup value, or provider query submitted by the caller.
			format_value (str): format value value used by the fetch data operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'query', query )
			
			self.query_text = str( query ).strip( )
			self.format_value = self.validate_format( format_value )
			self.endpoint = '/v2/query/data/'
			self.url = f'{self.base_url}{self.endpoint}'
			self.params = {
					'query': self.query_text,
					'format': self.format_value
			}
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=int( time )
			)
			self.response.raise_for_status( )
			
			return {
					'mode': 'data',
					'url': self.url,
					'params': self.params,
					'data': self.coerce_response( self.response )
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenScience'
			exception.method = (
					'fetch_data( self, query: str, format_value: str=json, '
					'time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch( self, mode: str = 'dataset', query: str = '',
			accession: str = '', format_value: str = 'json',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch NASA Open Science Data Repository resources.
		
		Purpose:
			Retrieves NASA Open Science Data Repository resources using validated arguments and the
			stored OpenScience runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			query (str): Search text, lookup value, or provider query submitted by the caller.
			accession (str): accession value used by the fetch operation.
			format_value (str): format value value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			active_mode = str( mode or 'dataset' ).strip( ).lower( )
			
			if active_mode == 'dataset':
				return self.fetch_dataset(
					accession=accession,
					time=time
				)
			
			if active_mode == 'metadata':
				return self.fetch_metadata(
					query=query,
					format_value=format_value,
					time=time
				)
			
			if active_mode == 'assays':
				return self.fetch_assays(
					query=query,
					format_value=format_value,
					time=time
				)
			
			if active_mode == 'data':
				return self.fetch_data(
					query=query,
					format_value=format_value,
					time=time
				)
			
			raise ValueError(
				"Unsupported mode. Use one of: dataset, metadata, assays, data."
			)
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenScience'
			exception.method = (
					'fetch( self, mode: str=dataset, query: str=, accession: str=, '
					'format_value: str=json, time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} '
							f'This function uses the {tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenScience'
			exception.method = (
					'create_schema( self, function: str, tool: str, description: str, '
					'parameters: dict, required: list[ str ] ) -> Dict[ str, str ]'
			)
			raise exception

class SpaceWeather( Fetcher ):
	"""Space Weather fetcher.
	
	Purpose:
		Coordinates NASA DONKI space weather endpoints within Fonky. The class stores provider
		configuration, request parameters, response payloads, and normalized result state so
		callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		api_key (Optional[str]): API key state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		start_date (Optional[str]): start date state retained by the instance.
		end_date (Optional[str]): end date state retained by the instance.
		location (Optional[str]): location state retained by the instance.
		catalog (Optional[str]): catalog state retained by the instance.
		notification_type (Optional[str]): notification type state retained by the instance.
		limit_note (Optional[str]): limit note state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	api_key: Optional[ str ]
	url: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	mode: Optional[ str ]
	start_date: Optional[ str ]
	end_date: Optional[ str ]
	location: Optional[ str ]
	catalog: Optional[ str ]
	notification_type: Optional[ str ]
	limit_note: Optional[ str ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize SpaceWeather.
		
		Purpose:
			Initializes the SpaceWeather instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.headers = { }
		self.base_url = 'https://api.nasa.gov/DONKI'
		self.api_key = cfg.NASA_API_KEY
		self.url = None
		self.params = { }
		self.mode = 'cme'
		self.start_date = ''
		self.end_date = ''
		self.location = 'ALL'
		self.catalog = 'ALL'
		self.notification_type = 'all'
		self.limit_note = None
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'api_key',
				'url',
				'params',
				'mode',
				'start_date',
				'end_date',
				'location',
				'catalog',
				'notification_type',
				'fetch_endpoint',
				'fetch',
				'create_schema'
		]
	
	def fetch_endpoint( self, endpoint: str, start_date: str, end_date: str,
			time: int = 20, location: str = '', catalog: str = '',
			notification_type: str = '', most_accurate_only: bool = True,
			complete_entry_only: bool = True, speed: int = 0,
			half_angle: int = 0, keyword: str = '',
			api_key: str = None ) -> Dict[ str, Any ] | None:
		"""Fetch endpoint.
		
		Purpose:
			Retrieves endpoint using validated arguments and the stored SpaceWeather runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			endpoint (str): endpoint value used by the fetch endpoint operation.
			start_date (str): start date value used by the fetch endpoint operation.
			end_date (str): end date value used by the fetch endpoint operation.
			time (int): Request timeout in seconds.
			location (str): location value used by the fetch endpoint operation.
			catalog (str): catalog value used by the fetch endpoint operation.
			notification_type (str): notification type value used by the fetch endpoint operation.
			most_accurate_only (bool): most accurate only value used by the fetch endpoint
				operation.
			complete_entry_only (bool): complete entry only value used by the fetch endpoint
				operation.
			speed (int): speed value used by the fetch endpoint operation.
			half_angle (int): half angle value used by the fetch endpoint operation.
			keyword (str): keyword value used by the fetch endpoint operation.
			api_key (str): Optional credential override used for the active request.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'endpoint', endpoint )
			throw_if( 'start_date', start_date )
			throw_if( 'end_date', end_date )
			
			active_key = str( api_key or self.api_key or '' ).strip( )
			if not active_key:
				raise ValueError( 'NASA API key is required for DONKI requests.' )
			
			self.url = f'{self.base_url}/{endpoint}'
			self.params = {
					'startDate': str( start_date ).strip( ),
					'endDate': str( end_date ).strip( ),
					'api_key': active_key
			}
			
			if endpoint == 'IPS' and location.strip( ):
				self.params[ 'location' ] = location.strip( )
			
			if endpoint == 'IPS' and catalog.strip( ):
				self.params[ 'catalog' ] = catalog.strip( )
			
			if endpoint == 'CMEAnalysis':
				self.params[ 'mostAccurateOnly' ] = str( bool( most_accurate_only ) ).lower( )
				self.params[ 'completeEntryOnly' ] = str( bool( complete_entry_only ) ).lower( )
				self.params[ 'speed' ] = int( speed )
				self.params[ 'halfAngle' ] = int( half_angle )
				
				if catalog.strip( ):
					self.params[ 'catalog' ] = catalog.strip( )
				
				if keyword.strip( ):
					self.params[ 'keyword' ] = keyword.strip( )
			
			if endpoint == 'notifications' and notification_type.strip( ):
				self.params[ 'type' ] = notification_type.strip( )
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=int( time )
			)
			self.response.raise_for_status( )
			payload = self.response.json( )
			
			return {
					'mode': self.mode,
					'endpoint': endpoint,
					'url': self.url,
					'params': self.params,
					'data': payload
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'SpaceWeather'
			exception.method = (
					'fetch_endpoint( self, endpoint: str, start_date: str, end_date: str, '
					'time: int=20, location: str=, catalog: str=, notification_type: str=, '
					'most_accurate_only: bool=True, complete_entry_only: bool=True, '
					'speed: int=0, half_angle: int=0, keyword: str=, '
					'api_key: str|None=None ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch( self, mode: str = 'cme', start_date: str = '', end_date: str = '',
			time: int = 20, location: str = 'ALL', catalog: str = 'ALL',
			notification_type: str = 'all', most_accurate_only: bool = True,
			complete_entry_only: bool = True, speed: int = 0,
			half_angle: int = 0, keyword: str = '',
			api_key: str = None ) -> Dict[ str, Any ] | None:
		"""Fetch NASA DONKI space weather endpoints.
		
		Purpose:
			Retrieves NASA DONKI space weather endpoints using validated arguments and the stored
			SpaceWeather runtime configuration. The method assembles request parameters, executes
			the provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			start_date (str): start date value used by the fetch operation.
			end_date (str): end date value used by the fetch operation.
			time (int): Request timeout in seconds.
			location (str): location value used by the fetch operation.
			catalog (str): catalog value used by the fetch operation.
			notification_type (str): notification type value used by the fetch operation.
			most_accurate_only (bool): most accurate only value used by the fetch operation.
			complete_entry_only (bool): complete entry only value used by the fetch operation.
			speed (int): speed value used by the fetch operation.
			half_angle (int): half angle value used by the fetch operation.
			keyword (str): keyword value used by the fetch operation.
			api_key (str): Optional credential override used for the active request.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			active_mode = str( mode or 'cme' ).strip( ).lower( )
			self.mode = active_mode
			
			endpoint_map = {
					'cme': 'CME',
					'cme_analysis': 'CMEAnalysis',
					'gst': 'GST',
					'ips': 'IPS',
					'flr': 'FLR',
					'sep': 'SEP',
					'mpc': 'MPC',
					'rbe': 'RBE',
					'hss': 'HSS',
					'wsa_enlil': 'WSAEnlilSimulations',
					'notifications': 'notifications'
			}
			
			if active_mode not in endpoint_map:
				raise ValueError(
					"Unsupported mode. Use 'cme', 'cme_analysis', 'gst', 'ips', "
					"'flr', 'sep', 'mpc', 'rbe', 'hss', 'wsa_enlil', or 'notifications'."
				)
			
			return self.fetch_endpoint(
				endpoint=endpoint_map[ active_mode ],
				start_date=str( start_date ).strip( ),
				end_date=str( end_date ).strip( ),
				time=int( time ),
				location=str( location or 'ALL' ).strip( ),
				catalog=str( catalog or 'ALL' ).strip( ),
				notification_type=str( notification_type or 'all' ).strip( ),
				most_accurate_only=bool( most_accurate_only ),
				complete_entry_only=bool( complete_entry_only ),
				speed=int( speed ),
				half_angle=int( half_angle ),
				keyword=str( keyword or '' ).strip( ),
				api_key=api_key
			)
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'SpaceWeather'
			exception.method = (
					'fetch( self, mode: str=cme, start_date: str=, end_date: str=, '
					'time: int=20, location: str=ALL, catalog: str=ALL, '
					'notification_type: str=all, most_accurate_only: bool=True, '
					'complete_entry_only: bool=True, speed: int=0, half_angle: int=0, '
					'keyword: str=, api_key: str|None=None ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': f'{description.strip( )} This function uses the {tool.strip( )} service.',
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'SpaceWeather'
			exception.method = (
					'create_schema( self, function: str, tool: str, description: str, '
					'parameters: dict, required: list[ str ] ) -> Dict[ str, str ]'
			)
			raise exception

class AstroCatalog( Fetcher ):
	"""Astro Catalog fetcher.
	
	Purpose:
		Coordinates Open Astronomy Catalog queries within Fonky. The class stores provider
		configuration, request parameters, response payloads, and normalized result state so
		callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		format (Optional[str]): format state retained by the instance.
		name (Optional[str]): name state retained by the instance.
		declination (Optional[str]): declination state retained by the instance.
		right_ascension (Optional[str]): right ascension state retained by the instance.
		radius (Optional[int]): radius state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		headers (object): headers state retained by the instance.
		timeout (object): timeout state retained by the instance.
		agents (object): agents state retained by the instance."""
	base_url: Optional[ str ]
	format: Optional[ str ]
	name: Optional[ str ]
	declination: Optional[ str ]
	right_ascension: Optional[ str ]
	radius: Optional[ int ]
	params: Optional[ Dict[ str, Any ] ]
	
	def __init__( self ):
		"""Initialize AstroCatalog.
		
		Purpose:
			Initializes the AstroCatalog instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://api.astrocats.space'
		self.format = 'json'
		self.name = None
		self.right_ascension = None
		self.declination = None
		self.radius = None
		self.params = { }
		self.headers = { }
		self.timeout = 20
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
		
		if 'Accept' not in self.headers:
			self.headers[ 'Accept' ] = 'application/json'
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'timeout',
				'headers',
				'fetch_object',
				'cone_search',
				'fetch',
		]
	
	def normalize_attribute_path( self, quantity: str = '', attributes: str = '' ) -> str:
		"""Normalize attribute path.
		
		Purpose:
			Converts attribute path into the canonical format expected by the AstroCatalog request
			workflow. The method standardizes caller input before it is used in endpoint paths,
			query parameters, filters, or response processing.
		
		Args:
			quantity (str): quantity value used by the normalize attribute path operation.
			attributes (str): attributes value used by the normalize attribute path operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing."""
		parts: list[ str ] = [ ]
		if quantity and quantity.strip( ):
			parts.append( quantity.strip( ) )
		
		if attributes and attributes.strip( ):
			attr_parts = [ a.strip( ) for a in attributes.split( ',' ) if a.strip( ) ]
			parts.extend( attr_parts )
		
		return '/'.join( parts )
	
	def parse_argument( self, argument_string: str ) -> Dict[ str, Any ]:
		"""Parse argument.
		
		Purpose:
			Performs the parse argument operation for Open Astronomy Catalog queries. The method
			uses the class runtime state and supplied arguments to prepare, transform, dispatch, or
			package data for the broader Fonky fetching workflow.
		
		Args:
			argument_string (str): argument string value used by the parse argument operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation."""
		params: Dict[ str, Any ] = { }
		
		if not argument_string or not argument_string.strip( ):
			return params
		
		raw_items = re.split( r'[\n,]+', argument_string )
		items = [ item.strip( ) for item in raw_items if item and item.strip( ) ]
		
		for item in items:
			if '=' in item:
				k, v = item.split( '=', 1 )
				params[ k.strip( ) ] = v.strip( )
			else:
				params[ item ] = ''
		
		return params
	
	def request( self, route: str, params: Dict[ str, Any ] | None = None,
			time: int = 20 ) -> Any:
		"""Request Open Astronomy Catalog queries.
		
		Purpose:
			Sends a provider request for Open Astronomy Catalog queries after request parameters
			have been validated or prepared by the caller. The method stores request, response, and
			payload state on the instance so subsequent methods can package or inspect the result
			consistently.
		
		Args:
			route (str): route value used by the request operation.
			params (Dict[str, Any] | None): Request or schema parameter dictionary used by the
				operation.
			time (int): Request timeout in seconds.
		
		Returns:
			object: Normalized provider response, result payload, or document collection returned by
				the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.timeout = int( time )
			self.url = f'{self.base_url}/{route.lstrip( "/" )}'
			self.params = params or { }
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout )
			
			self.response.raise_for_status( )
			
			content_type = (self.response.headers.get( 'Content-Type', '' ) or '').lower( )
			if 'json' in content_type:
				return self.response.json( )
			
			return self.response.text
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'AstroCatalog'
			exception.method = 'request( self, route: str, params: Dict[ str, Any ] | None=None, time: int=20 ) -> Any'
			raise exception
	
	def fetch_object( self, name: str, quantity: str = '', attributes: str = '',
			arguments: str = '', data_format: str = 'json', time: int = 20 ) -> Any:
		"""Fetch object.
		
		Purpose:
			Retrieves object using validated arguments and the stored AstroCatalog runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			name (str): name value used by the fetch object operation.
			quantity (str): quantity value used by the fetch object operation.
			attributes (str): attributes value used by the fetch object operation.
			arguments (str): arguments value used by the fetch object operation.
			data_format (str): data format value used by the fetch object operation.
			time (int): Request timeout in seconds.
		
		Returns:
			object: Normalized provider response, result payload, or document collection returned by
				the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			self.name = name.strip( )
			self.format = (data_format or 'json').strip( ).lower( )
			
			route_parts = [ urllib.parse.quote( self.name ) ]
			attr_path = self.normalize_attribute_path( quantity, attributes )
			if attr_path:
				route_parts.append( attr_path )
			
			route = '/'.join( route_parts )
			params = self.parse_argument( arguments )
			
			if self.format:
				params[ 'format' ] = self.format
			
			return self.request( route=route, params=params, time=time )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'AstroCatalog'
			exception.method = (
					'fetch_object( self, name: str, quantity: str=, attributes: str=, '
					'arguments: str=, data_format: str=json, time: int=20 ) -> Any'
			)
			raise exception
	
	def cone_search( self, ra: str, dec: str, radius: int = 2, quantity: str = '',
			attributes: str = '', arguments: str = '', data_format: str = 'json',
			time: int = 20 ) -> Any:
		"""Cone search.
		
		Purpose:
			Performs the cone search operation for Open Astronomy Catalog queries. The method uses
			the class runtime state and supplied arguments to prepare, transform, dispatch, or
			package data for the broader Fonky fetching workflow.
		
		Args:
			ra (str): ra value used by the cone search operation.
			dec (str): dec value used by the cone search operation.
			radius (int): radius value used by the cone search operation.
			quantity (str): quantity value used by the cone search operation.
			attributes (str): attributes value used by the cone search operation.
			arguments (str): arguments value used by the cone search operation.
			data_format (str): data format value used by the cone search operation.
			time (int): Request timeout in seconds.
		
		Returns:
			object: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'ra', ra )
			throw_if( 'dec', dec )
			self.right_ascension = ra.strip( )
			self.declination = dec.strip( )
			self.radius = max( 1, int( radius ) )
			self.format = (data_format or 'json').strip( ).lower( )
			route = 'catalog'
			attr_path = self.normalize_attribute_path( quantity, attributes )
			if attr_path:
				route = f'{route}/{attr_path}'
			
			params = self.parse_argument( arguments )
			params[ 'ra' ] = self.right_ascension
			params[ 'dec' ] = self.declination
			params[ 'radius' ] = str( self.radius )
			if self.format:
				params[ 'format' ] = self.format
			
			return self.request( route=route, params=params, time=time )
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'AstroCatalog'
			exception.method = ('cone_search( self, ra: str, dec: str, radius: int=2, '
			                    'quantity: str=, attributes: str=, arguments: str=, '
			                    'data_format: str=json, time: int=20 ) -> Any')
			raise exception
	
	def fetch( self, mode: str = 'object_query', query: str = '', quantity: str = '',
			attributes: str = '', arguments: str = '', ra: str = '', dec: str = '',
			radius: int = 2, data_format: str = 'json', time: int = 20 ) -> Any:
		"""Fetch Open Astronomy Catalog queries.
		
		Purpose:
			Retrieves Open Astronomy Catalog queries using validated arguments and the stored
			AstroCatalog runtime configuration. The method assembles request parameters, executes
			the provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			query (str): Search text, lookup value, or provider query submitted by the caller.
			quantity (str): quantity value used by the fetch operation.
			attributes (str): attributes value used by the fetch operation.
			arguments (str): arguments value used by the fetch operation.
			ra (str): ra value used by the fetch operation.
			dec (str): dec value used by the fetch operation.
			radius (int): radius value used by the fetch operation.
			data_format (str): data format value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			object: Normalized provider response, result payload, or document collection returned by
				the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			active_mode = (mode or 'object_query').strip( ).lower( )
			
			if active_mode == 'object_query':
				return self.fetch_object(
					name=query,
					quantity=quantity,
					attributes=attributes,
					arguments=arguments,
					data_format=data_format,
					time=time )
			
			if active_mode == 'cone_search':
				return self.cone_search(
					ra=ra,
					dec=dec,
					radius=radius,
					quantity=quantity,
					attributes=attributes,
					arguments=arguments,
					data_format=data_format,
					time=time )
			
			raise ValueError( "Unsupported mode. Use 'object_query' or 'cone_search'." )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'AstroCatalog'
			exception.method = (
					'fetch( self, mode: str=object_query, query: str=, quantity: str=, '
					'attributes: str=, arguments: str=, ra: str=, dec: str=, '
					'radius: int=2, data_format: str=json, time: int=20 ) -> Any'
			)
			raise exception

class AstroQuery( Fetcher ):
	"""Astro Query fetcher.
	
	Purpose:
		Coordinates Simbad and astronomy object search operations within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		url (Optional[str]): URL state retained by the instance.
		radius (Optional[float]): radius state retained by the instance.
		name (Optional[str]): name state retained by the instance.
		declination (Optional[str]): declination state retained by the instance.
		right_ascension (Optional[str]): right ascension state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		row_limit (Optional[int]): row limit state retained by the instance.
		agents (object): agents state retained by the instance."""
	url: Optional[ str ]
	radius: Optional[ float ]
	name: Optional[ str ]
	declination: Optional[ str ]
	right_ascension: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	row_limit: Optional[ int ]
	
	def __init__( self ) -> None:
		"""Initialize AstroQuery.
		
		Purpose:
			Initializes the AstroQuery instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.url = None
		self.radius = None
		self.name = None
		self.right_ascension = None
		self.declination = None
		self.params = { }
		self.row_limit = 100
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'headers',
				'row_limit',
				'object_search',
				'object_ids',
				'region_search',
				'fetch',
		]
	
	def table_to_records( self, table: Table | None ) -> List[ Dict[ str, Any ] ]:
		"""Table to records.
		
		Purpose:
			Performs the table to records operation for Simbad and astronomy object search
			operations. The method uses the class runtime state and supplied arguments to prepare,
			transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			table (Table | None): table value used by the table to records operation.
		
		Returns:
			List[Dict[str, Any]]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if table is None:
				return [ ]
			
			records: List[ Dict[ str, Any ] ] = [ ]
			for row in table:
				record: Dict[ str, Any ] = { }
				for col in table.colnames:
					try:
						value = row[ col ]
						if hasattr( value, 'item' ):
							try:
								value = value.item( )
							except Exception:
								pass
						record[ str( col ) ] = str( value )
					except Exception:
						record[ str( col ) ] = ''
				records.append( record )
			
			return records
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'AstroQuery'
			exception.method = 'table_to_records( self, table: Table | None ) -> List[ Dict[ str, Any ] ]'
			raise exception
	
	def object_search( self, name: str, row_limit: int = 100 ) -> Dict[ str, Any ] | None:
		"""Object search.
		
		Purpose:
			Performs the object search operation for Simbad and astronomy object search operations.
			The method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			name (str): name value used by the object search operation.
			row_limit (int): row limit value used by the object search operation.
		
		Returns:
			Dict[str, Any] | None: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			self.name = name.strip( )
			self.row_limit = max( 1, int( row_limit ) )
			
			simbad = Simbad( )
			simbad.ROW_LIMIT = self.row_limit
			result_table = simbad.query_object( self.name )
			
			return {
					'mode': 'object_search',
					'query': self.name,
					'row_limit': self.row_limit,
					'columns': list( result_table.colnames ) if result_table is not None else [ ],
					'rows': self.table_to_records( result_table ),
			}
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'AstroQuery'
			exception.method = 'object_search( self, name: str, row_limit: int=100 ) -> Dict[ str, Any ]'
			raise exception
	
	def object_ids( self, name: str, row_limit: int = 100 ) -> Dict[ str, Any ] | None:
		"""Object IDs.
		
		Purpose:
			Performs the object ids operation for Simbad and astronomy object search operations. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			name (str): name value used by the object ids operation.
			row_limit (int): row limit value used by the object ids operation.
		
		Returns:
			Dict[str, Any] | None: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			self.name = name.strip( )
			self.row_limit = max( 1, int( row_limit ) )
			
			simbad = Simbad( )
			simbad.ROW_LIMIT = self.row_limit
			result_table = simbad.query_objectids( self.name )
			
			return {
					'mode': 'object_ids',
					'query': self.name,
					'row_limit': self.row_limit,
					'columns': list( result_table.colnames ) if result_table is not None else [ ],
					'rows': self.table_to_records( result_table ),
			}
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'AstroQuery'
			exception.method = 'object_ids( self, name: str, row_limit: int=100 ) -> Dict[ str, Any ]'
			raise exception
	
	def region_search( self, ra: str, dec: str, radius: float = 0.5,
			radius_unit: str = 'deg', row_limit: int = 100 ) -> Dict[ str, Any ] | None:
		"""Region search.
		
		Purpose:
			Performs the region search operation for Simbad and astronomy object search operations.
			The method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			ra (str): ra value used by the region search operation.
			dec (str): dec value used by the region search operation.
			radius (float): radius value used by the region search operation.
			radius_unit (str): radius unit value used by the region search operation.
			row_limit (int): row limit value used by the region search operation.
		
		Returns:
			Dict[str, Any] | None: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'ra', ra )
			throw_if( 'dec', dec )
			
			self.right_ascension = ra.strip( )
			self.declination = dec.strip( )
			self.radius = float( radius )
			self.row_limit = max( 1, int( row_limit ) )
			
			unit_map = {
					'deg': u.deg,
					'arcmin': u.arcmin,
					'arcsec': u.arcsec,
			}
			
			active_unit = unit_map.get( (radius_unit or 'deg').strip( ).lower( ), u.deg )
			
			coord = SkyCoord(
				ra=self.right_ascension,
				dec=self.declination,
				unit=(u.hourangle, u.deg) )
			
			simbad = Simbad( )
			simbad.ROW_LIMIT = self.row_limit
			result_table = simbad.query_region(
				coordinates=coord,
				radius=self.radius * active_unit )
			
			return {
					'mode': 'region_search',
					'ra': self.right_ascension,
					'dec': self.declination,
					'radius': self.radius,
					'radius_unit': (radius_unit or 'deg').strip( ).lower( ),
					'row_limit': self.row_limit,
					'columns': list( result_table.colnames ) if result_table is not None else [ ],
					'rows': self.table_to_records( result_table ),
			}
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'AstroQuery'
			exception.method = (
					'region_search( self, ra: str, dec: str, radius: float=0.5, '
					'radius_unit: str=deg, row_limit: int=100 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch( self, mode: str = 'object_search', query: str = '', ra: str = '', dec: str = '',
			radius: float = 0.5, radius_unit: str = 'deg', row_limit: int = 100 ) -> Dict[
				                                                                         str, Any ] | None:
		"""Fetch Simbad and astronomy object search operations.
		
		Purpose:
			Retrieves Simbad and astronomy object search operations using validated arguments and
			the stored AstroQuery runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			query (str): Search text, lookup value, or provider query submitted by the caller.
			ra (str): ra value used by the fetch operation.
			dec (str): dec value used by the fetch operation.
			radius (float): radius value used by the fetch operation.
			radius_unit (str): radius unit value used by the fetch operation.
			row_limit (int): row limit value used by the fetch operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			active_mode = (mode or 'object_search').strip( ).lower( )
			
			if active_mode == 'object_search':
				return self.object_search(
					name=query,
					row_limit=row_limit )
			
			if active_mode == 'object_ids':
				return self.object_ids(
					name=query,
					row_limit=row_limit )
			
			if active_mode == 'region_search':
				return self.region_search(
					ra=ra,
					dec=dec,
					radius=radius,
					radius_unit=radius_unit,
					row_limit=row_limit )
			
			raise ValueError(
				"Unsupported mode. Use 'object_search', 'object_ids', or 'region_search'."
			)
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'AstroQuery'
			exception.method = (
					'fetch( self, mode: str=object_search, query: str=, ra: str=, '
					'dec: str=, radius: float=0.5, radius_unit: str=deg, '
					'row_limit: int=100 ) -> Dict[ str, Any ]'
			)
			raise exception

class StarMap( Fetcher ):
	"""Star Map fetcher.
	
	Purpose:
		Coordinates astronomical object map links and imagery within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		snapshot_url (Optional[str]): snapshot URL state retained by the instance.
		image_source (Optional[str]): image source state retained by the instance.
		object (Optional[str]): object state retained by the instance.
		right_ascension (Optional[float]): right ascension state retained by the instance.
		declination (Optional[float]): declination state retained by the instance.
		box_color (Optional[str]): box color state retained by the instance.
		show_box (Optional[bool]): show box state retained by the instance.
		show_grid (Optional[bool]): show grid state retained by the instance.
		show_lines (Optional[bool]): show lines state retained by the instance.
		show_boundaries (Optional[bool]): show boundaries state retained by the instance.
		show_const_names (Optional[bool]): show const names state retained by the instance.
		zoom (Optional[int]): zoom state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance.
		agents (object): agents state retained by the instance."""
	base_url: Optional[ str ]
	snapshot_url: Optional[ str ]
	image_source: Optional[ str ]
	object: Optional[ str ]
	right_ascension: Optional[ float ]
	declination: Optional[ float ]
	box_color: Optional[ str ]
	show_box: Optional[ bool ]
	show_grid: Optional[ bool ]
	show_lines: Optional[ bool ]
	show_boundaries: Optional[ bool ]
	show_const_names: Optional[ bool ]
	zoom: Optional[ int ]
	params: Optional[ Dict[ str, Any ] ]
	
	def __init__( self ) -> None:
		"""Initialize StarMap.
		
		Purpose:
			Initializes the StarMap instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://www.sky-map.org/'
		self.snapshot_url = 'https://www.sky-map.org/snapshot'
		self.image_source = 'DSS2'
		self.object = None
		self.right_ascension = None
		self.declination = None
		self.box_color = 'yellow'
		self.show_box = True
		self.show_grid = True
		self.show_lines = True
		self.show_boundaries = True
		self.show_const_names = False
		self.zoom = 5
		self.params = { }
		self.timeout = 20
		self.headers = { }
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
		
		if 'Accept' not in self.headers:
			self.headers[
				'Accept' ] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'snapshot_url',
				'object',
				'right_ascension',
				'declination',
				'image_source',
				'zoom',
				'show_box',
				'show_grid',
				'show_lines',
				'show_boundaries',
				'show_const_names',
				'box_color',
				'params',
				'fetch_object_link',
				'fetch_coordinate_link',
				'fetch_snapshot',
				'fetch',
		]
	
	def normalize( self, value: bool ) -> str:
		"""Normalize.
		
		Purpose:
			Performs the normalize operation for astronomical object map links and imagery. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			value (bool): value value used by the normalize operation.
		
		Returns:
			str: Result produced by the operation."""
		return '1' if bool( value ) else '0'
	
	def extract_links( self, html: str, base_url: str ) -> Dict[ str, str ]:
		"""Extract links.
		
		Purpose:
			Extracts links from the supplied source content and normalizes the result for downstream
			use. The method stores intermediate parsing state when needed and returns only the
			compact value required by callers.
		
		Args:
			html (str): HTML value used by the extract links operation.
			base_url (str): URL or URI value used as the request or parsing source.
		
		Returns:
			Dict[str, str]: Extracted and normalized content values.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			links: Dict[ str, str ] = { }
			if not html or not isinstance( html, str ):
				return links
			
			pattern = re.compile(
				r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>\s*(jpeg|png|gif|bmp|tiff)\s*</a>',
				flags=re.IGNORECASE )
			
			for match in pattern.finditer( html ):
				href = match.group( 1 )
				label = match.group( 2 ).lower( )
				links[ label ] = urllib.parse.urljoin( base_url, href )
			
			return links
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'StarMap'
			exception.method = 'extract_links( self, html: str, base_url: str ) -> Dict[ str, str ]'
			raise exception
	
	def fetch_object_link( self, name: str, zoom: int = 5, box_color: str = 'yellow',
			show_box: bool = True, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch object link.
		
		Purpose:
			Retrieves object link using validated arguments and the stored StarMap runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			name (str): name value used by the fetch object link operation.
			zoom (int): zoom value used by the fetch object link operation.
			box_color (str): box color value used by the fetch object link operation.
			show_box (bool): show box value used by the fetch object link operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			
			self.object = name.strip( )
			self.zoom = max( 1, min( int( zoom ), 18 ) )
			self.box_color = box_color or 'yellow'
			self.show_box = bool( show_box )
			self.timeout = int( time )
			
			self.params = {
					'object': self.object,
					'show_box': self.normalize( self.show_box ),
					'zoom': str( self.zoom ),
					'box_color': self.box_color,
					'box_width': '50',
					'box_height': '50',
			}
			
			interactive_url = f'{self.base_url}?{urllib.parse.urlencode( self.params )}'
			
			self.response = requests.get(
				url=self.base_url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout )
			self.response.raise_for_status( )
			
			return {
					'mode': 'object_link',
					'object': self.object,
					'zoom': self.zoom,
					'params': self.params,
					'interactive_url': interactive_url,
					'status_code': self.response.status_code,
					'html_preview': self.response.text[ : 2000 ],
			}
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'StarMap'
			exception.method = (
					'fetch_object_link( self, name: str, zoom: int=5, box_color: str=yellow, '
					'show_box: bool=True, time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_coordinate_link( self, ra: float, dec: float, zoom: int = 5,
			box_color: str = 'yellow',
			show_box: bool = True, show_grid: bool = True, show_lines: bool = True,
			show_boundaries: bool = True, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch coordinate link.
		
		Purpose:
			Retrieves coordinate link using validated arguments and the stored StarMap runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			ra (float): ra value used by the fetch coordinate link operation.
			dec (float): dec value used by the fetch coordinate link operation.
			zoom (int): zoom value used by the fetch coordinate link operation.
			box_color (str): box color value used by the fetch coordinate link operation.
			show_box (bool): show box value used by the fetch coordinate link operation.
			show_grid (bool): show grid value used by the fetch coordinate link operation.
			show_lines (bool): show lines value used by the fetch coordinate link operation.
			show_boundaries (bool): show boundaries value used by the fetch coordinate link
				operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'ra', ra )
			throw_if( 'dec', dec )
			
			self.right_ascension = float( ra )
			self.declination = float( dec )
			self.zoom = max( 1, min( int( zoom ), 18 ) )
			self.box_color = box_color or 'yellow'
			self.show_box = bool( show_box )
			self.show_grid = bool( show_grid )
			self.show_lines = bool( show_lines )
			self.show_boundaries = bool( show_boundaries )
			self.timeout = int( time )
			
			self.params = {
					'ra': f'{self.right_ascension}',
					'de': f'{self.declination}',
					'show_box': self.normalize( self.show_box ),
					'zoom': str( self.zoom ),
					'box_color': self.box_color,
					'show_grid': self.normalize( self.show_grid ),
					'show_constellation_lines': self.normalize( self.show_lines ),
					'show_constellation_boundaries': self.normalize( self.show_boundaries ),
			}
			
			interactive_url = f'{self.base_url}?{urllib.parse.urlencode( self.params )}'
			
			self.response = requests.get(
				url=self.base_url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout )
			self.response.raise_for_status( )
			
			return {
					'mode': 'coordinate_link',
					'ra': self.right_ascension,
					'dec': self.declination,
					'zoom': self.zoom,
					'params': self.params,
					'interactive_url': interactive_url,
					'status_code': self.response.status_code,
					'html_preview': self.response.text[ : 2000 ],
			}
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'StarMap'
			exception.method = (
					'fetch_coordinate_link( self, ra: float, dec: float, zoom: int=5, '
					'box_color: str=yellow, show_box: bool=True, show_grid: bool=True, '
					'show_lines: bool=True, show_boundaries: bool=True, time: int=20 ) '
					'-> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_snapshot( self, ra: float, dec: float, zoom: int = 10, image_source: str = 'DSS2',
			show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True,
			show_const_names: bool = False, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch snapshot.
		
		Purpose:
			Retrieves snapshot using validated arguments and the stored StarMap runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			ra (float): ra value used by the fetch snapshot operation.
			dec (float): dec value used by the fetch snapshot operation.
			zoom (int): zoom value used by the fetch snapshot operation.
			image_source (str): image source value used by the fetch snapshot operation.
			show_grid (bool): show grid value used by the fetch snapshot operation.
			show_lines (bool): show lines value used by the fetch snapshot operation.
			show_boundaries (bool): show boundaries value used by the fetch snapshot operation.
			show_const_names (bool): show const names value used by the fetch snapshot operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'ra', ra )
			throw_if( 'dec', dec )
			
			self.right_ascension = float( ra )
			self.declination = float( dec )
			self.zoom = max( 1, min( int( zoom ), 18 ) )
			self.image_source = (image_source or 'DSS2').strip( )
			self.show_grid = bool( show_grid )
			self.show_lines = bool( show_lines )
			self.show_boundaries = bool( show_boundaries )
			self.show_const_names = bool( show_const_names )
			self.timeout = int( time )
			
			self.params = {
					'ra': f'{self.right_ascension}',
					'de': f'{self.declination}',
					'zoom': str( self.zoom ),
					'img_source': self.image_source,
					'show_grid': self.normalize( self.show_grid ),
					'show_constellation_lines': self.normalize( self.show_lines ),
					'show_constellation_boundaries': self.normalize( self.show_boundaries ),
					'show_const_names': self.normalize( self.show_const_names ),
			}
			
			page_url = f'{self.snapshot_url}?{urllib.parse.urlencode( self.params )}'
			
			self.response = requests.get(
				url=self.snapshot_url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout )
			self.response.raise_for_status( )
			
			image_links = self.extract_links(
				html=self.response.text,
				base_url=self.snapshot_url )
			
			return {
					'mode': 'snapshot',
					'ra': self.right_ascension,
					'dec': self.declination,
					'zoom': self.zoom,
					'image_source': self.image_source,
					'params': self.params,
					'snapshot_page_url': page_url,
					'image_links': image_links,
					'preferred_image_url': image_links.get( 'png' ) or image_links.get( 'jpeg',
						'' ),
					'status_code': self.response.status_code,
					'html_preview': self.response.text[ : 2000 ],
			}
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'StarMap'
			exception.method = (
					'fetch_snapshot( self, ra: float, dec: float, zoom: int=10, '
					'image_source: str=DSS2, show_grid: bool=True, show_lines: bool=True, '
					'show_boundaries: bool=True, show_const_names: bool=False, '
					'time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch( self, mode: str = 'object_link', query: str = '', ra: float = 0.0, dec: float = 0.0,
			zoom: int = 5, image_source: str = 'DSS2', box_color: str = 'yellow',
			show_box: bool = True,
			show_grid: bool = True, show_lines: bool = True, show_boundaries: bool = True,
			show_const_names: bool = False, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch astronomical object map links and imagery.
		
		Purpose:
			Retrieves astronomical object map links and imagery using validated arguments and the
			stored StarMap runtime configuration. The method assembles request parameters, executes
			the provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			query (str): Search text, lookup value, or provider query submitted by the caller.
			ra (float): ra value used by the fetch operation.
			dec (float): dec value used by the fetch operation.
			zoom (int): zoom value used by the fetch operation.
			image_source (str): image source value used by the fetch operation.
			box_color (str): box color value used by the fetch operation.
			show_box (bool): show box value used by the fetch operation.
			show_grid (bool): show grid value used by the fetch operation.
			show_lines (bool): show lines value used by the fetch operation.
			show_boundaries (bool): show boundaries value used by the fetch operation.
			show_const_names (bool): show const names value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			active_mode = (mode or 'object_link').strip( ).lower( )
			
			if active_mode == 'object_link':
				return self.fetch_object_link(
					name=query,
					zoom=zoom,
					box_color=box_color,
					show_box=show_box,
					time=time )
			
			if active_mode == 'coordinate_link':
				return self.fetch_coordinate_link(
					ra=ra,
					dec=dec,
					zoom=zoom,
					box_color=box_color,
					show_box=show_box,
					show_grid=show_grid,
					show_lines=show_lines,
					show_boundaries=show_boundaries,
					time=time )
			
			if active_mode == 'snapshot':
				return self.fetch_snapshot(
					ra=ra,
					dec=dec,
					zoom=zoom,
					image_source=image_source,
					show_grid=show_grid,
					show_lines=show_lines,
					show_boundaries=show_boundaries,
					show_const_names=show_const_names,
					time=time )
			
			raise ValueError(
				"Unsupported mode. Use 'object_link', 'coordinate_link', or 'snapshot'."
			)
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'StarMap'
			exception.method = (
					'fetch( self, mode: str=object_link, query: str=, ra: float=0.0, '
					'dec: float=0.0, zoom: int=5, image_source: str=DSS2, '
					'box_color: str=yellow, show_box: bool=True, show_grid: bool=True, '
					'show_lines: bool=True, show_boundaries: bool=True, '
					'show_const_names: bool=False, time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception

class GovData( Fetcher ):
	"""Gov Data fetcher.
	
	Purpose:
		Coordinates Data.gov package and collection retrieval within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		api_key (Optional[str]): API key state retained by the instance.
		base_url (Optional[str]): base URL state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Dict[str, Any]]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		query (Optional[str]): query state retained by the instance.
		page_size (Optional[int]): page size state retained by the instance.
		offset_mark (Optional[str]): offset mark state retained by the instance.
		sort_field (Optional[str]): sort field state retained by the instance.
		sort_order (Optional[str]): sort order state retained by the instance.
		package_id (Optional[str]): package ID state retained by the instance.
		collection (Optional[str]): collection state retained by the instance.
		start_date (Optional[str]): start date state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		headers (object): headers state retained by the instance."""
	api_key: Optional[ str ]
	base_url: Optional[ str ]
	url: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Dict[ str, Any ] ]
	result: Optional[ Dict[ str, Any ] ]
	mode: Optional[ str ]
	query: Optional[ str ]
	page_size: Optional[ int ]
	offset_mark: Optional[ str ]
	sort_field: Optional[ str ]
	sort_order: Optional[ str ]
	package_id: Optional[ str ]
	collection: Optional[ str ]
	start_date: Optional[ str ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize GovData.
		
		Purpose:
			Initializes the GovData instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.api_key = cfg.GOVINFO_API_KEY
		self.base_url = 'https://api.govinfo.gov'
		self.url = None
		self.params = { }
		self.payload = { }
		self.result = { }
		self.mode = 'search'
		self.query = ''
		self.page_size = 10
		self.offset_mark = '*'
		self.sort_field = 'score'
		self.sort_order = 'DESC'
		self.package_id = ''
		self.collection = ''
		self.start_date = ''
		self.response = None
		self.headers = {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'User-Agent': cfg.AGENTS
		}
		self.agents = cfg.AGENTS
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'api_key',
				'base_url',
				'url',
				'params',
				'payload',
				'result',
				'mode',
				'query',
				'page_size',
				'offset_mark',
				'sort_field',
				'sort_order',
				'package_id',
				'collection',
				'start_date',
				'response',
				'headers',
				'agents',
				'validate_page_size',
				'validate_sort_field',
				'validate_sort_order',
				'fetch_search',
				'fetch_package_summary',
				'fetch_collection',
				'fetch',
				'create_schema'
		]
	
	def validate_page_size( self, page_size: int ) -> int:
		"""Validate page size.
		
		Purpose:
			Validates and normalizes page size before it is used in Data.gov package and collection
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			page_size (int): page size value used by the validate page size operation.
		
		Returns:
			int: Validated page size value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'page_size', page_size )
			
			value = int( page_size )
			if value < 1 or value > 1000:
				raise ValueError( 'page_size must be between 1 and 1000.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GovData'
			exception.method = 'validate_page_size( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_sort_field( self, sort_field: str ) -> str:
		"""Validate sort field.
		
		Purpose:
			Validates and normalizes sort field before it is used in Data.gov package and collection
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			sort_field (str): sort field value used by the validate sort field operation.
		
		Returns:
			str: Validated sort field value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( sort_field or 'score' ).strip( )
			allowed = { 'score', 'lastModified' }
			
			if value not in allowed:
				raise ValueError(
					"Unsupported sort field. Use 'score' or 'lastModified'."
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GovData'
			exception.method = 'validate_sort_field( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_sort_order( self, sort_order: str ) -> str:
		"""Validate sort order.
		
		Purpose:
			Validates and normalizes sort order before it is used in Data.gov package and collection
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			sort_order (str): sort order value used by the validate sort order operation.
		
		Returns:
			str: Validated sort order value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( sort_order or 'DESC' ).strip( ).upper( )
			allowed = { 'ASC', 'DESC' }
			
			if value not in allowed:
				raise ValueError( "Unsupported sort order. Use 'ASC' or 'DESC'." )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GovData'
			exception.method = 'validate_sort_order( self, *args, **kwargs ) -> str'
			raise exception
	
	def fetch_search( self, query: str, page_size: int = 10, offset_mark: str = '*',
			sort_field: str = 'score', sort_order: str = 'DESC', time: int = 20 ) -> Dict[
				                                                                         str, Any ] | None:
		"""Fetch search.
		
		Purpose:
			Retrieves search using validated arguments and the stored GovData runtime configuration.
			The method assembles request parameters, executes the provider call or dispatches to a
			specialized helper, records response state when applicable, and returns a normalized
			payload for downstream analysis or tool execution.
		
		Args:
			query (str): Search text, lookup value, or provider query submitted by the caller.
			page_size (int): page size value used by the fetch search operation.
			offset_mark (str): offset mark value used by the fetch search operation.
			sort_field (str): sort field value used by the fetch search operation.
			sort_order (str): sort order value used by the fetch search operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'api_key', self.api_key )
			throw_if( 'query', query )
			throw_if( 'offset_mark', offset_mark )
			throw_if( 'time', time )
			
			self.mode = 'search'
			self.query = str( query ).strip( )
			self.page_size = self.validate_page_size( page_size )
			self.offset_mark = str( offset_mark or '*' ).strip( )
			self.sort_field = self.validate_sort_field( sort_field )
			self.sort_order = self.validate_sort_order( sort_order )
			self.timeout = int( time )
			self.url = f'{self.base_url}/search'
			self.params = {
					'api_key': self.api_key
			}
			self.payload = {
					'query': self.query,
					'pageSize': self.page_size,
					'offsetMark': self.offset_mark,
					'sorts': [
							{
									'field': self.sort_field,
									'sortOrder': self.sort_order
							}
					]
			}
			
			self.response = requests.post(
				url=self.url,
				params=self.params,
				json=self.payload,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'payload': self.payload,
					'data': self.response.json( )
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GovData'
			exception.method = 'fetch_search( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def fetch_package_summary( self, package_id: str, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch package summary.
		
		Purpose:
			Retrieves package summary using validated arguments and the stored GovData runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			package_id (str): package ID value used by the fetch package summary operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'api_key', self.api_key )
			throw_if( 'package_id', package_id )
			throw_if( 'time', time )
			
			self.mode = 'package_summary'
			self.package_id = str( package_id ).strip( )
			self.timeout = int( time )
			self.url = f'{self.base_url}/packages/{self.package_id}/summary'
			self.params = { 'api_key': self.api_key }
			self.payload = { }
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'payload': self.payload,
					'data': self.response.json( )
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GovData'
			exception.method = 'fetch_package_summary( self, *args, **kwargs ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_collection( self, collection: str, start_date: str, page_size: int = 10,
			offset_mark: str = '*', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch collection.
		
		Purpose:
			Retrieves collection using validated arguments and the stored GovData runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			collection (str): collection value used by the fetch collection operation.
			start_date (str): start date value used by the fetch collection operation.
			page_size (int): page size value used by the fetch collection operation.
			offset_mark (str): offset mark value used by the fetch collection operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'api_key', self.api_key )
			throw_if( 'collection', collection )
			throw_if( 'start_date', start_date )
			throw_if( 'offset_mark', offset_mark )
			throw_if( 'time', time )
			
			self.mode = 'collection'
			self.collection = str( collection ).strip( )
			self.start_date = str( start_date ).strip( )
			self.page_size = self.validate_page_size( page_size )
			self.offset_mark = str( offset_mark or '*' ).strip( )
			self.timeout = int( time )
			self.url = f'{self.base_url}/collections/{self.collection}/{self.start_date}'
			self.params = {
					'pageSize': self.page_size,
					'offsetMark': self.offset_mark,
					'api_key': self.api_key
			}
			self.payload = { }
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'payload': self.payload,
					'data': self.response.json( )
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GovData'
			exception.method = 'fetch_collection( self, *args, **kwargs ) -> Dict[ str, Any ] '
			raise exception
	
	def fetch( self, mode: str = 'search', query: str = '',
			page_size: int = 10, offset_mark: str = '*',
			sort_field: str = 'score', sort_order: str = 'DESC',
			package_id: str = '', collection: str = '',
			start_date: str = '', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch Data.gov package and collection retrieval.
		
		Purpose:
			Retrieves Data.gov package and collection retrieval using validated arguments and the
			stored GovData runtime configuration. The method assembles request parameters, executes
			the provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			query (str): Search text, lookup value, or provider query submitted by the caller.
			page_size (int): page size value used by the fetch operation.
			offset_mark (str): offset mark value used by the fetch operation.
			sort_field (str): sort field value used by the fetch operation.
			sort_order (str): sort order value used by the fetch operation.
			package_id (str): package ID value used by the fetch operation.
			collection (str): collection value used by the fetch operation.
			start_date (str): start date value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			self.mode = str( mode or 'search' ).strip( ).lower( )
			
			if self.mode == 'search':
				return self.fetch_search(
					query=query,
					page_size=page_size,
					offset_mark=offset_mark,
					sort_field=sort_field,
					sort_order=sort_order,
					time=time
				)
			
			if self.mode == 'package_summary':
				return self.fetch_package_summary(
					package_id=package_id,
					time=time
				)
			
			if self.mode == 'collection':
				return self.fetch_collection(
					collection=collection,
					start_date=start_date,
					page_size=page_size,
					offset_mark=offset_mark,
					time=time
				)
			
			raise ValueError(
				"Unsupported GovInfo mode. Use 'search', 'package_summary', or "
				"'collection'."
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GovData'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f"{description.strip( )} This function uses the "
							f"{tool.strip( )} service."
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GovData'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class StarChart( Fetcher ):
	"""Star Chart fetcher.
	
	Purpose:
		Coordinates static star chart and coordinate chart generation within Fonky. The class
		stores provider configuration, request parameters, response payloads, and normalized
		result state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		search_url (Optional[str]): search URL state retained by the instance.
		link_url (Optional[str]): link URL state retained by the instance.
		image_url (Optional[str]): image URL state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		query (Optional[str]): query state retained by the instance.
		ra (Optional[float]): ra state retained by the instance.
		dec (Optional[float]): dec state retained by the instance.
		zoom (Optional[int]): zoom state retained by the instance.
		image_source (Optional[str]): image source state retained by the instance.
		box_color (Optional[str]): box color state retained by the instance.
		show_box (Optional[bool]): show box state retained by the instance.
		show_grid (Optional[bool]): show grid state retained by the instance.
		show_lines (Optional[bool]): show lines state retained by the instance.
		show_boundaries (Optional[bool]): show boundaries state retained by the instance.
		show_const_names (Optional[bool]): show const names state retained by the instance.
		width (Optional[int]): width state retained by the instance.
		height (Optional[int]): height state retained by the instance.
		magnitude (Optional[float]): magnitude state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		headers (object): headers state retained by the instance."""
	search_url: Optional[ str ]
	link_url: Optional[ str ]
	image_url: Optional[ str ]
	url: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	mode: Optional[ str ]
	query: Optional[ str ]
	ra: Optional[ float ]
	dec: Optional[ float ]
	zoom: Optional[ int ]
	image_source: Optional[ str ]
	box_color: Optional[ str ]
	show_box: Optional[ bool ]
	show_grid: Optional[ bool ]
	show_lines: Optional[ bool ]
	show_boundaries: Optional[ bool ]
	show_const_names: Optional[ bool ]
	width: Optional[ int ]
	height: Optional[ int ]
	magnitude: Optional[ float ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize StarChart.
		
		Purpose:
			Initializes the StarChart instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.headers = { }
		self.search_url = 'https://server1.sky-map.org/search'
		self.link_url = 'https://www.sky-map.org/'
		self.image_url = 'https://server2.sky-map.org/map'
		self.url = None
		self.params = { }
		self.mode = 'object_chart'
		self.query = ''
		self.ra = 0.0
		self.dec = 0.0
		self.zoom = 5
		self.image_source = 'DSS2'
		self.box_color = 'yellow'
		self.show_box = True
		self.show_grid = True
		self.show_lines = True
		self.show_boundaries = True
		self.show_const_names = False
		self.width = 900
		self.height = 450
		self.magnitude = 7.5
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'search_url',
				'link_url',
				'image_url',
				'url',
				'params',
				'mode',
				'query',
				'ra',
				'dec',
				'zoom',
				'image_source',
				'box_color',
				'show_box',
				'show_grid',
				'show_lines',
				'show_boundaries',
				'show_const_names',
				'width',
				'height',
				'magnitude',
				'search_object',
				'fetch_object_chart',
				'fetch_coordinate_chart',
				'fetch_static_chart',
				'fetch',
				'create_schema'
		]
	
	def flag( self, value: bool, invert: bool = False ) -> int:
		"""Flag.
		
		Purpose:
			Performs the flag operation for static star chart and coordinate chart generation. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			value (bool): value value used by the flag operation.
			invert (bool): invert value used by the flag operation.
		
		Returns:
			int: Result produced by the operation."""
		if invert:
			return 0 if bool( value ) else 1
		
		return 1 if bool( value ) else 0
	
	def search_object( self, name: str, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Search object.
		
		Purpose:
			Performs the search object operation for static star chart and coordinate chart
			generation. The method uses the class runtime state and supplied arguments to prepare,
			transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			name (str): name value used by the search object operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			self.query = str( name ).strip( )
			self.url = self.search_url
			self.params = { 'star': self.query }
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=int( time )
			)
			self.response.raise_for_status( )
			
			root = ET.fromstring( self.response.text )
			status = root.findtext( 'status', default='' )
			verbiage = root.findtext( 'verbiage', default='' )
			star = root.find( 'star' )
			
			if star is None:
				return {
						'mode': 'object_search',
						'url': self.url,
						'params': self.params,
						'status': status,
						'verbiage': verbiage,
						'data': { }
				}
			
			result = {
					'id': star.attrib.get( 'id', '' ),
					'catalog_id': star.findtext( 'catId', default='' ),
					'constellation': star.findtext( 'constellation', default='' ),
					'ra': float( star.findtext( 'ra', default='0' ) ),
					'dec': float( star.findtext( 'de', default='0' ) ),
					'magnitude': star.findtext( 'mag', default='' )
			}
			
			self.ra = result[ 'ra' ]
			self.dec = result[ 'dec' ]
			
			return {
					'mode': 'object_search',
					'url': self.url,
					'params': self.params,
					'status': status,
					'verbiage': verbiage,
					'data': result
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'StarChart'
			exception.method = (
					'search_object( self, name: str, time: int=20 ) '
					'-> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_object_chart( self, name: str, zoom: int = 5, box_color: str = 'yellow',
			show_box: bool = True, image_source: str = '', time: int = 20 ) -> Dict[
				                                                                   str, Any ] | None:
		"""Fetch object chart.
		
		Purpose:
			Retrieves object chart using validated arguments and the stored StarChart runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			name (str): name value used by the fetch object chart operation.
			zoom (int): zoom value used by the fetch object chart operation.
			box_color (str): box color value used by the fetch object chart operation.
			show_box (bool): show box value used by the fetch object chart operation.
			image_source (str): image source value used by the fetch object chart operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			self.mode = 'object_chart'
			self.query = str( name ).strip( )
			self.zoom = int( zoom )
			self.box_color = str( box_color or 'yellow' ).strip( )
			self.show_box = bool( show_box )
			self.image_source = str( image_source or '' ).strip( )
			
			self.url = self.link_url
			self.params = {
					'object': self.query,
					'zoom': self.zoom,
					'show_box': self.flag( self.show_box ),
					'box_color': self.box_color
			}
			
			if self.image_source:
				self.params[ 'img_source' ] = self.image_source
			
			link = requests.Request( 'GET', self.url, params=self.params ).prepare( ).url
			
			search = self.search_object( name=self.query, time=time ) or { }
			
			return {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'chart_url': link,
					'search': search
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'StarChart'
			exception.method = (
					'fetch_object_chart( self, name: str, zoom: int=5, '
					'box_color: str=yellow, show_box: bool=True, image_source: str=, '
					'time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_coordinate_chart( self, ra: float, dec: float, zoom: int = 5,
			box_color: str = 'yellow', show_box: bool = True, show_grid: bool = True,
			show_lines: bool = True,
			show_boundaries: bool = True, image_source: str = '' ) -> Dict[ str, Any ] | None:
		"""Fetch coordinate chart.
		
		Purpose:
			Retrieves coordinate chart using validated arguments and the stored StarChart runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			ra (float): ra value used by the fetch coordinate chart operation.
			dec (float): dec value used by the fetch coordinate chart operation.
			zoom (int): zoom value used by the fetch coordinate chart operation.
			box_color (str): box color value used by the fetch coordinate chart operation.
			show_box (bool): show box value used by the fetch coordinate chart operation.
			show_grid (bool): show grid value used by the fetch coordinate chart operation.
			show_lines (bool): show lines value used by the fetch coordinate chart operation.
			show_boundaries (bool): show boundaries value used by the fetch coordinate chart
				operation.
			image_source (str): image source value used by the fetch coordinate chart operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'coordinate_chart'
			self.ra = float( ra )
			self.dec = float( dec )
			self.zoom = int( zoom )
			self.box_color = str( box_color or 'yellow' ).strip( )
			self.show_box = bool( show_box )
			self.show_grid = bool( show_grid )
			self.show_lines = bool( show_lines )
			self.show_boundaries = bool( show_boundaries )
			self.image_source = str( image_source or '' ).strip( )
			
			self.url = self.link_url
			self.params = {
					'ra': self.ra,
					'de': self.dec,
					'zoom': self.zoom,
					'show_box': self.flag( self.show_box ),
					'box_color': self.box_color,
					'show_grid': self.flag( self.show_grid, invert=True ),
					'show_constellation_lines': self.flag( self.show_lines, invert=True ),
					'show_constellation_boundaries': self.flag( self.show_boundaries, invert=True )
			}
			
			if self.image_source:
				self.params[ 'img_source' ] = self.image_source
			
			link = requests.Request( 'GET', self.url, params=self.params ).prepare( ).url
			
			return {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'chart_url': link
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'StarChart'
			exception.method = 'fetch_coordinate_chart( self, *args ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_static_chart( self, ra: float, dec: float, zoom: int = 5,
			image_source: str = 'DSS2', show_grid: bool = True, show_lines: bool = True,
			show_boundaries: bool = True, show_const_names: bool = False, width: int = 900,
			height: int = 450, magnitude: float = 7.5 ) -> Dict[ str, Any ] | None:
		"""Fetch static chart.
		
		Purpose:
			Retrieves static chart using validated arguments and the stored StarChart runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			ra (float): ra value used by the fetch static chart operation.
			dec (float): dec value used by the fetch static chart operation.
			zoom (int): zoom value used by the fetch static chart operation.
			image_source (str): image source value used by the fetch static chart operation.
			show_grid (bool): show grid value used by the fetch static chart operation.
			show_lines (bool): show lines value used by the fetch static chart operation.
			show_boundaries (bool): show boundaries value used by the fetch static chart operation.
			show_const_names (bool): show const names value used by the fetch static chart
				operation.
			width (int): width value used by the fetch static chart operation.
			height (int): height value used by the fetch static chart operation.
			magnitude (float): magnitude value used by the fetch static chart operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'static_chart'
			self.ra = float( ra )
			self.dec = float( dec )
			self.zoom = int( zoom )
			self.image_source = str( image_source or 'DSS2' ).strip( )
			self.show_grid = bool( show_grid )
			self.show_lines = bool( show_lines )
			self.show_boundaries = bool( show_boundaries )
			self.show_const_names = bool( show_const_names )
			self.width = int( width )
			self.height = int( height )
			self.magnitude = float( magnitude )
			
			self.url = self.image_url
			self.params = {
					'type': 'FULL',
					'w': self.width,
					'h': self.height,
					'ra': self.ra,
					'de': self.dec,
					'zoom': self.zoom,
					'mag': self.magnitude,
					'show_grid': self.flag( self.show_grid ),
					'grid_color': '404040',
					'grid_color_zero': '808080',
					'show_constellation_lines': self.flag( self.show_lines ),
					'show_constellation_boundaries': self.flag( self.show_boundaries ),
					'show_const_names': self.flag( self.show_const_names ),
					'img_source': self.image_source
			}
			
			image_link = requests.Request( 'GET', self.url, params=self.params ).prepare( ).url
			
			return {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'image_url': image_link
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'StarChart'
			exception.method = (
					'fetch_static_chart( self, ra: float, dec: float, zoom: int=5, '
					'image_source: str=DSS2, show_grid: bool=True, show_lines: bool=True, '
					'show_boundaries: bool=True, show_const_names: bool=False, '
					'width: int=900, height: int=450, magnitude: float=7.5 ) '
					'-> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch( self, mode: str = 'object_chart', query: str = '',
			ra: float = 0.0, dec: float = 0.0, zoom: int = 5,
			image_source: str = 'DSS2', box_color: str = 'yellow',
			show_box: bool = True, show_grid: bool = True,
			show_lines: bool = True, show_boundaries: bool = True,
			show_const_names: bool = False, width: int = 900,
			height: int = 450, magnitude: float = 7.5,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch static star chart and coordinate chart generation.
		
		Purpose:
			Retrieves static star chart and coordinate chart generation using validated arguments
			and the stored StarChart runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			query (str): Search text, lookup value, or provider query submitted by the caller.
			ra (float): ra value used by the fetch operation.
			dec (float): dec value used by the fetch operation.
			zoom (int): zoom value used by the fetch operation.
			image_source (str): image source value used by the fetch operation.
			box_color (str): box color value used by the fetch operation.
			show_box (bool): show box value used by the fetch operation.
			show_grid (bool): show grid value used by the fetch operation.
			show_lines (bool): show lines value used by the fetch operation.
			show_boundaries (bool): show boundaries value used by the fetch operation.
			show_const_names (bool): show const names value used by the fetch operation.
			width (int): width value used by the fetch operation.
			height (int): height value used by the fetch operation.
			magnitude (float): magnitude value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			active_mode = (mode or 'object_chart').strip( ).lower( )
			if active_mode == 'object_search':
				return self.search_object( name=query, time=time )
			if active_mode == 'object_chart':
				return self.fetch_object_chart( name=query, zoom=zoom, box_color=box_color,
					show_box=show_box, image_source=image_source if image_source != 'DSS2' else '',
					time=time )
			if active_mode == 'coordinate_chart':
				return self.fetch_coordinate_chart(
					ra=ra,
					dec=dec,
					zoom=zoom,
					box_color=box_color,
					show_box=show_box,
					show_grid=show_grid,
					show_lines=show_lines,
					show_boundaries=show_boundaries,
					image_source=image_source if image_source != 'DSS2' else '' )
			
			if active_mode == 'static_chart':
				return self.fetch_static_chart(
					ra=ra,
					dec=dec,
					zoom=zoom,
					image_source=image_source,
					show_grid=show_grid,
					show_lines=show_lines,
					show_boundaries=show_boundaries,
					show_const_names=show_const_names,
					width=width,
					height=height,
					magnitude=magnitude
				)
			
			raise ValueError(
				"Unsupported mode. Use 'object_search', 'object_chart', "
				"'coordinate_chart', or 'static_chart'."
			)
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'StarChart'
			exception.method = (
					'fetch( self, mode: str=object_chart, query: str=, ra: float=0.0, '
					'dec: float=0.0, zoom: int=5, image_source: str=DSS2, '
					'box_color: str=yellow, show_box: bool=True, show_grid: bool=True, '
					'show_lines: bool=True, show_boundaries: bool=True, '
					'show_const_names: bool=False, width: int=900, height: int=450, '
					'magnitude: float=7.5, time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': f'{description.strip( )} This function uses the {tool.strip( )} service.',
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'StarChart'
			exception.method = (
					'create_schema( self, function: str, tool: str, description: str, '
					'parameters: dict, required: list[ str ] ) -> Dict[ str, str ]'
			)
			raise exception

class Congress( Fetcher ):
	"""Congress fetcher.
	
	Purpose:
		Coordinates Congress.gov legislative data retrieval within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		api_key (Optional[str]): API key state retained by the instance.
		base_url (Optional[str]): base URL state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Dict[str, Any]]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		congress_number (Optional[int]): congress number state retained by the instance.
		bill_type (Optional[str]): bill type state retained by the instance.
		bill_number (Optional[int]): bill number state retained by the instance.
		law_type (Optional[str]): law type state retained by the instance.
		law_number (Optional[int]): law number state retained by the instance.
		report_type (Optional[str]): report type state retained by the instance.
		report_number (Optional[int]): report number state retained by the instance.
		offset (Optional[int]): offset state retained by the instance.
		limit (Optional[int]): limit state retained by the instance.
		sort (Optional[str]): sort state retained by the instance.
		from_date_time (Optional[str]): from date time state retained by the instance.
		to_date_time (Optional[str]): to date time state retained by the instance.
		conference (Optional[bool]): conference state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		headers (object): headers state retained by the instance."""
	api_key: Optional[ str ]
	base_url: Optional[ str ]
	url: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Dict[ str, Any ] ]
	result: Optional[ Dict[ str, Any ] ]
	mode: Optional[ str ]
	congress_number: Optional[ int ]
	bill_type: Optional[ str ]
	bill_number: Optional[ int ]
	law_type: Optional[ str ]
	law_number: Optional[ int ]
	report_type: Optional[ str ]
	report_number: Optional[ int ]
	offset: Optional[ int ]
	limit: Optional[ int ]
	sort: Optional[ str ]
	from_date_time: Optional[ str ]
	to_date_time: Optional[ str ]
	conference: Optional[ bool ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize Congress.
		
		Purpose:
			Initializes the Congress instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.api_key = cfg.CONGRESS_API_KEY
		self.base_url = 'https://api.congress.gov/v3'
		self.url = None
		self.params = { }
		self.payload = { }
		self.result = { }
		self.mode = 'congresses'
		self.congress_number = None
		self.bill_type = ''
		self.bill_number = None
		self.law_type = ''
		self.law_number = None
		self.report_type = ''
		self.report_number = None
		self.offset = 0
		self.limit = 20
		self.sort = 'updateDate+desc'
		self.from_date_time = ''
		self.to_date_time = ''
		self.conference = False
		self.response = None
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': cfg.AGENTS
		}
		self.agents = cfg.AGENTS
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'api_key',
				'base_url',
				'url',
				'params',
				'payload',
				'result',
				'mode',
				'congress_number',
				'bill_type',
				'bill_number',
				'law_type',
				'law_number',
				'report_type',
				'report_number',
				'offset',
				'limit',
				'sort',
				'from_date_time',
				'to_date_time',
				'conference',
				'response',
				'headers',
				'agents',
				'validate_limit',
				'validate_offset',
				'normalize_bill_type',
				'normalize_law_type',
				'normalize_report_type',
				'build_params',
				'request',
				'fetch_congresses',
				'fetch_bills',
				'fetch_bill',
				'fetch_laws',
				'fetch_law',
				'fetch_reports',
				'fetch_report',
				'fetch',
				'create_schema'
		]
	
	def validate_limit( self, limit: int ) -> int:
		"""Validate limit.
		
		Purpose:
			Validates and normalizes limit before it is used in Congress.gov legislative data
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			limit (int): limit value used by the validate limit operation.
		
		Returns:
			int: Validated limit value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'limit', limit )
			
			value = int( limit )
			if value < 1 or value > 250:
				raise ValueError( 'limit must be between 1 and 250.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = 'validate_limit( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_offset( self, offset: int ) -> int:
		"""Validate offset.
		
		Purpose:
			Validates and normalizes offset before it is used in Congress.gov legislative data
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			offset (int): offset value used by the validate offset operation.
		
		Returns:
			int: Validated offset value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if offset is None:
				raise ValueError( 'offset cannot be None.' )
			
			value = int( offset )
			if value < 0:
				raise ValueError( 'offset must be greater than or equal to 0.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = 'validate_offset( self, *args, **kwargs ) -> int'
			raise exception
	
	def normalize_bill_type( self, bill_type: str ) -> str:
		"""Normalize bill type.
		
		Purpose:
			Converts bill type into the canonical format expected by the Congress request workflow.
			The method standardizes caller input before it is used in endpoint paths, query
			parameters, filters, or response processing.
		
		Args:
			bill_type (str): bill type value used by the normalize bill type operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( bill_type or '' ).strip( ).lower( )
			throw_if( 'bill_type', value )
			
			allowed = {
					'hr',
					's',
					'hjres',
					'sjres',
					'hconres',
					'sconres',
					'hres',
					'sres'
			}
			
			if value not in allowed:
				raise ValueError(
					"Unsupported bill_type. Use 'hr', 's', 'hjres', 'sjres', "
					"'hconres', 'sconres', 'hres', or 'sres'."
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = 'normalize_bill_type( self, *args, **kwargs ) -> str'
			raise exception
	
	def normalize_law_type( self, law_type: str ) -> str:
		"""Normalize law type.
		
		Purpose:
			Converts law type into the canonical format expected by the Congress request workflow.
			The method standardizes caller input before it is used in endpoint paths, query
			parameters, filters, or response processing.
		
		Args:
			law_type (str): law type value used by the normalize law type operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( law_type or '' ).strip( ).lower( )
			throw_if( 'law_type', value )
			
			allowed = { 'pub', 'priv' }
			
			if value not in allowed:
				raise ValueError( "Unsupported law_type. Use 'pub' or 'priv'." )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = 'normalize_law_type( self, *args, **kwargs ) -> str'
			raise exception
	
	def normalize_report_type( self, report_type: str ) -> str:
		"""Normalize report type.
		
		Purpose:
			Converts report type into the canonical format expected by the Congress request
			workflow. The method standardizes caller input before it is used in endpoint paths,
			query parameters, filters, or response processing.
		
		Args:
			report_type (str): report type value used by the normalize report type operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( report_type or '' ).strip( ).lower( )
			throw_if( 'report_type', value )
			
			allowed = { 'hrpt', 'srpt', 'erpt' }
			
			if value not in allowed:
				raise ValueError(
					"Unsupported report_type. Use 'hrpt', 'srpt', or 'erpt'."
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = 'normalize_report_type( self, *args, **kwargs ) -> str'
			raise exception
	
	def build_params( self, limit: int = 20, offset: int = 0,
			sort: str = 'updateDate+desc' ) -> Dict[ str, Any ]:
		"""Build params.
		
		Purpose:
			Constructs params from validated inputs and stored runtime configuration. The method
			centralizes URL, parameter, or payload assembly so fetch operations can issue provider
			requests using a predictable structure.
		
		Args:
			limit (int): limit value used by the build params operation.
			offset (int): offset value used by the build params operation.
			sort (str): sort value used by the build params operation.
		
		Returns:
			Dict[str, Any]: Constructed URL, query, payload, or request structure.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'api_key', self.api_key )
			
			self.limit = self.validate_limit( limit )
			self.offset = self.validate_offset( offset )
			self.sort = str( sort or 'updateDate+desc' ).strip( )
			
			return {
					'api_key': self.api_key,
					'format': 'json',
					'limit': self.limit,
					'offset': self.offset,
					'sort': self.sort
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = (
					'build_params( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def request( self, mode: str, url: str, params: Dict[ str, Any ],
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Request Congress.gov legislative data retrieval.
		
		Purpose:
			Sends a provider request for Congress.gov legislative data retrieval after request
			parameters have been validated or prepared by the caller. The method stores request,
			response, and payload state on the instance so subsequent methods can package or inspect
			the result consistently.
		
		Args:
			mode (str): mode value used by the request operation.
			url (str): URL or URI value used as the request or parsing source.
			params (Dict[str, Any]): Request or schema parameter dictionary used by the operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			throw_if( 'url', url )
			throw_if( 'params', params )
			throw_if( 'time', time )
			
			self.mode = str( mode ).strip( )
			self.url = str( url ).strip( )
			self.timeout = int( time )
			self.params = params
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.json( )
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'data': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = (
					'request( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_congresses( self, limit: int = 20, offset: int = 0,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch congresses.
		
		Purpose:
			Retrieves congresses using validated arguments and the stored Congress runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			limit (int): limit value used by the fetch congresses operation.
			offset (int): offset value used by the fetch congresses operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.url = f'{self.base_url}/congress'
			self.params = self.build_params(
				limit=limit,
				offset=offset,
				sort='updateDate+desc'
			)
			
			return self.request(
				mode='congresses',
				url=self.url,
				params=self.params,
				time=time
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = (
					'fetch_congresses( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_bills( self, congress: int, bill_type: str = '',
			offset: int = 0, limit: int = 20, sort: str = 'updateDate+desc',
			from_date_time: str = '', to_date_time: str = '',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch bills.
		
		Purpose:
			Retrieves bills using validated arguments and the stored Congress runtime configuration.
			The method assembles request parameters, executes the provider call or dispatches to a
			specialized helper, records response state when applicable, and returns a normalized
			payload for downstream analysis or tool execution.
		
		Args:
			congress (int): congress value used by the fetch bills operation.
			bill_type (str): bill type value used by the fetch bills operation.
			offset (int): offset value used by the fetch bills operation.
			limit (int): limit value used by the fetch bills operation.
			sort (str): sort value used by the fetch bills operation.
			from_date_time (str): from date time value used by the fetch bills operation.
			to_date_time (str): to date time value used by the fetch bills operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'congress', congress )
			
			self.congress_number = int( congress )
			self.bill_type = str( bill_type or '' ).strip( ).lower( )
			self.from_date_time = str( from_date_time or '' ).strip( )
			self.to_date_time = str( to_date_time or '' ).strip( )
			
			if self.bill_type:
				self.bill_type = self.normalize_bill_type( self.bill_type )
				self.url = f'{self.base_url}/bill/{self.congress_number}/{self.bill_type}'
			else:
				self.url = f'{self.base_url}/bill/{self.congress_number}'
			
			self.params = self.build_params(
				limit=limit,
				offset=offset,
				sort=sort
			)
			
			if self.from_date_time:
				self.params[ 'fromDateTime' ] = self.from_date_time
			
			if self.to_date_time:
				self.params[ 'toDateTime' ] = self.to_date_time
			
			return self.request(
				mode='bills',
				url=self.url,
				params=self.params,
				time=time
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = (
					'fetch_bills( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_bill( self, congress: int, bill_type: str, bill_number: int,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch bill.
		
		Purpose:
			Retrieves bill using validated arguments and the stored Congress runtime configuration.
			The method assembles request parameters, executes the provider call or dispatches to a
			specialized helper, records response state when applicable, and returns a normalized
			payload for downstream analysis or tool execution.
		
		Args:
			congress (int): congress value used by the fetch bill operation.
			bill_type (str): bill type value used by the fetch bill operation.
			bill_number (int): bill number value used by the fetch bill operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'congress', congress )
			throw_if( 'bill_type', bill_type )
			throw_if( 'bill_number', bill_number )
			
			self.congress_number = int( congress )
			self.bill_type = self.normalize_bill_type( bill_type )
			self.bill_number = int( bill_number )
			self.url = (
					f'{self.base_url}/bill/{self.congress_number}/'
					f'{self.bill_type}/{self.bill_number}'
			)
			self.params = {
					'api_key': self.api_key,
					'format': 'json'
			}
			
			return self.request(
				mode='bill_detail',
				url=self.url,
				params=self.params,
				time=time
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = (
					'fetch_bill( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_laws( self, congress: int, law_type: str = '',
			offset: int = 0, limit: int = 20,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch laws.
		
		Purpose:
			Retrieves laws using validated arguments and the stored Congress runtime configuration.
			The method assembles request parameters, executes the provider call or dispatches to a
			specialized helper, records response state when applicable, and returns a normalized
			payload for downstream analysis or tool execution.
		
		Args:
			congress (int): congress value used by the fetch laws operation.
			law_type (str): law type value used by the fetch laws operation.
			offset (int): offset value used by the fetch laws operation.
			limit (int): limit value used by the fetch laws operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'congress', congress )
			
			self.congress_number = int( congress )
			self.law_type = str( law_type or '' ).strip( ).lower( )
			
			if self.law_type:
				self.law_type = self.normalize_law_type( self.law_type )
				self.url = f'{self.base_url}/law/{self.congress_number}/{self.law_type}'
			else:
				self.url = f'{self.base_url}/law/{self.congress_number}'
			
			self.params = self.build_params(
				limit=limit,
				offset=offset,
				sort='updateDate+desc'
			)
			
			return self.request(
				mode='laws',
				url=self.url,
				params=self.params,
				time=time
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = (
					'fetch_laws( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_law( self, congress: int, law_type: str,
			law_number: int, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch law.
		
		Purpose:
			Retrieves law using validated arguments and the stored Congress runtime configuration.
			The method assembles request parameters, executes the provider call or dispatches to a
			specialized helper, records response state when applicable, and returns a normalized
			payload for downstream analysis or tool execution.
		
		Args:
			congress (int): congress value used by the fetch law operation.
			law_type (str): law type value used by the fetch law operation.
			law_number (int): law number value used by the fetch law operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'congress', congress )
			throw_if( 'law_type', law_type )
			throw_if( 'law_number', law_number )
			
			self.congress_number = int( congress )
			self.law_type = self.normalize_law_type( law_type )
			self.law_number = int( law_number )
			self.url = (
					f'{self.base_url}/law/{self.congress_number}/'
					f'{self.law_type}/{self.law_number}'
			)
			self.params = {
					'api_key': self.api_key,
					'format': 'json'
			}
			
			return self.request(
				mode='law_detail',
				url=self.url,
				params=self.params,
				time=time
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = (
					'fetch_law( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_reports( self, congress: int, report_type: str = '',
			offset: int = 0, limit: int = 20, conference: bool = False,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch reports.
		
		Purpose:
			Retrieves reports using validated arguments and the stored Congress runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			congress (int): congress value used by the fetch reports operation.
			report_type (str): report type value used by the fetch reports operation.
			offset (int): offset value used by the fetch reports operation.
			limit (int): limit value used by the fetch reports operation.
			conference (bool): conference value used by the fetch reports operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'congress', congress )
			
			self.congress_number = int( congress )
			self.report_type = str( report_type or '' ).strip( ).lower( )
			self.conference = bool( conference )
			
			if self.report_type:
				self.report_type = self.normalize_report_type( self.report_type )
				self.url = (
						f'{self.base_url}/committee-report/'
						f'{self.congress_number}/{self.report_type}'
				)
			else:
				self.url = f'{self.base_url}/committee-report/{self.congress_number}'
			
			self.params = self.build_params(
				limit=limit,
				offset=offset,
				sort='updateDate+desc'
			)
			self.params[ 'conference' ] = str( self.conference ).lower( )
			
			return self.request(
				mode='reports',
				url=self.url,
				params=self.params,
				time=time
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = (
					'fetch_reports( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_report( self, congress: int, report_type: str,
			report_number: int, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch report.
		
		Purpose:
			Retrieves report using validated arguments and the stored Congress runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			congress (int): congress value used by the fetch report operation.
			report_type (str): report type value used by the fetch report operation.
			report_number (int): report number value used by the fetch report operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'congress', congress )
			throw_if( 'report_type', report_type )
			throw_if( 'report_number', report_number )
			
			self.congress_number = int( congress )
			self.report_type = self.normalize_report_type( report_type )
			self.report_number = int( report_number )
			self.url = (
					f'{self.base_url}/committee-report/{self.congress_number}/'
					f'{self.report_type}/{self.report_number}'
			)
			self.params = {
					'api_key': self.api_key,
					'format': 'json'
			}
			
			return self.request(
				mode='report_detail',
				url=self.url,
				params=self.params,
				time=time
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = (
					'fetch_report( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'congresses', congress: int = 0,
			bill_type: str = '', bill_number: int = 0, law_type: str = '',
			law_number: int = 0, report_type: str = '',
			report_number: int = 0, offset: int = 0, limit: int = 20,
			sort: str = 'updateDate+desc', from_date_time: str = '',
			to_date_time: str = '', conference: bool = False,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch Congress.gov legislative data retrieval.
		
		Purpose:
			Retrieves Congress.gov legislative data retrieval using validated arguments and the
			stored Congress runtime configuration. The method assembles request parameters, executes
			the provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			congress (int): congress value used by the fetch operation.
			bill_type (str): bill type value used by the fetch operation.
			bill_number (int): bill number value used by the fetch operation.
			law_type (str): law type value used by the fetch operation.
			law_number (int): law number value used by the fetch operation.
			report_type (str): report type value used by the fetch operation.
			report_number (int): report number value used by the fetch operation.
			offset (int): offset value used by the fetch operation.
			limit (int): limit value used by the fetch operation.
			sort (str): sort value used by the fetch operation.
			from_date_time (str): from date time value used by the fetch operation.
			to_date_time (str): to date time value used by the fetch operation.
			conference (bool): conference value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			self.mode = str( mode or 'congresses' ).strip( ).lower( )
			
			if self.mode == 'congresses':
				return self.fetch_congresses(
					limit=limit,
					offset=offset,
					time=time
				)
			
			if self.mode == 'bills':
				return self.fetch_bills(
					congress=congress,
					bill_type=bill_type,
					offset=offset,
					limit=limit,
					sort=sort,
					from_date_time=from_date_time,
					to_date_time=to_date_time,
					time=time
				)
			
			if self.mode == 'bill_detail':
				return self.fetch_bill(
					congress=congress,
					bill_type=bill_type,
					bill_number=bill_number,
					time=time
				)
			
			if self.mode == 'laws':
				return self.fetch_laws(
					congress=congress,
					law_type=law_type,
					offset=offset,
					limit=limit,
					time=time
				)
			
			if self.mode == 'law_detail':
				return self.fetch_law(
					congress=congress,
					law_type=law_type,
					law_number=law_number,
					time=time
				)
			
			if self.mode == 'reports':
				return self.fetch_reports(
					congress=congress,
					report_type=report_type,
					offset=offset,
					limit=limit,
					conference=conference,
					time=time
				)
			
			if self.mode == 'report_detail':
				return self.fetch_report(
					congress=congress,
					report_type=report_type,
					report_number=report_number,
					time=time
				)
			
			raise ValueError(
				"Unsupported Congress mode. Use 'congresses', 'bills', "
				"'bill_detail', 'laws', 'law_detail', 'reports', or 'report_detail'."
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f"{description.strip( )} This function uses the "
							f"{tool.strip( )} service."
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Congress'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class InternetArchive( Fetcher ):
	"""Internet Archive fetcher.
	
	Purpose:
		Coordinates Internet Archive search and metadata retrieval within Fonky. The class
		stores provider configuration, request parameters, response payloads, and normalized
		result state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		keywords (Optional[str]): keywords state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		response (Optional[Response]): response state retained by the instance.
		fields (Optional[List[str]]): fields state retained by the instance.
		rows (Optional[int]): rows state retained by the instance.
		page (Optional[int]): page state retained by the instance.
		sort (Optional[str]): sort state retained by the instance.
		media_type (Optional[str]): media type state retained by the instance.
		collection (Optional[str]): collection state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		headers (object): headers state retained by the instance.
		timeout (object): timeout state retained by the instance."""
	keywords: Optional[ str ]
	url: Optional[ str ]
	response: Optional[ Response ]
	fields: Optional[ List[ str ] ]
	rows: Optional[ int ]
	page: Optional[ int ]
	sort: Optional[ str ]
	media_type: Optional[ str ]
	collection: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize InternetArchive.
		
		Purpose:
			Initializes the InternetArchive instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.url = 'https://archive.org/advancedsearch.php'
		self.headers = { }
		self.timeout = 20
		self.keywords = ''
		self.params = { }
		self.fields = [
				'identifier',
				'title',
				'creator',
				'mediatype',
				'collection',
				'publicdate',
				'description'
		]
		self.rows = 10
		self.page = 1
		self.sort = 'downloads desc'
		self.media_type = ''
		self.collection = ''
		self.response = None
		self.agents = cfg.AGENTS
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
		
		if 'Accept' not in self.headers:
			self.headers[ 'Accept' ] = 'application/json'
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'keywords',
				'url',
				'timeout',
				'headers',
				'fields',
				'rows',
				'page',
				'sort',
				'media_type',
				'collection',
				'params',
				'agents',
				'fetch',
				'create_schema'
		]
	
	def validate_rows( self, rows: int ) -> int:
		"""Validate rows.
		
		Purpose:
			Validates and normalizes rows before it is used in Internet Archive search and metadata
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			rows (int): rows value used by the validate rows operation.
		
		Returns:
			int: Validated rows value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = int( rows )
			if value < 1 or value > 100:
				raise ValueError( 'rows must be between 1 and 100.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'InternetArchive'
			exception.method = 'validate_rows( self, rows: int ) -> int'
			raise exception
	
	def validate_page( self, page: int ) -> int:
		"""Validate page.
		
		Purpose:
			Validates and normalizes page before it is used in Internet Archive search and metadata
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			page (int): page value used by the validate page operation.
		
		Returns:
			int: Validated page value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = int( page )
			if value < 1:
				raise ValueError( 'page must be greater than or equal to 1.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'InternetArchive'
			exception.method = 'validate_page( self, page: int ) -> int'
			raise exception
	
	def build_query( self, keywords: str, media_type: str = '',
			collection: str = '' ) -> str:
		"""Build query.
		
		Purpose:
			Constructs query from validated inputs and stored runtime configuration. The method
			centralizes URL, parameter, or payload assembly so fetch operations can issue provider
			requests using a predictable structure.
		
		Args:
			keywords (str): Search text, lookup value, or provider query submitted by the caller.
			media_type (str): media type value used by the build query operation.
			collection (str): collection value used by the build query operation.
		
		Returns:
			str: Constructed URL, query, payload, or request structure.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'keywords', keywords )
			
			parts: List[ str ] = [ f'({str( keywords ).strip( )})' ]
			
			if media_type and str( media_type ).strip( ):
				parts.append( f'AND mediatype:({str( media_type ).strip( )})' )
			
			if collection and str( collection ).strip( ):
				parts.append( f'AND collection:({str( collection ).strip( )})' )
			
			return ' '.join( parts )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'InternetArchive'
			exception.method = (
					'build_query( self, keywords: str, media_type: str=, '
					'collection: str= ) -> str'
			)
			raise exception
	
	def fetch( self, keywords: str, fields: List[ str ] | None = None,
			rows: int = 10, page: int = 1, sort: str = 'downloads desc',
			media_type: str = '', collection: str = '',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch Internet Archive search and metadata retrieval.
		
		Purpose:
			Retrieves Internet Archive search and metadata retrieval using validated arguments and
			the stored InternetArchive runtime configuration. The method assembles request
			parameters, executes the provider call or dispatches to a specialized helper, records
			response state when applicable, and returns a normalized payload for downstream analysis
			or tool execution.
		
		Args:
			keywords (str): Search text, lookup value, or provider query submitted by the caller.
			fields (List[str] | None): fields value used by the fetch operation.
			rows (int): rows value used by the fetch operation.
			page (int): page value used by the fetch operation.
			sort (str): sort value used by the fetch operation.
			media_type (str): media type value used by the fetch operation.
			collection (str): collection value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.keywords = str( keywords ).strip( )
			throw_if( 'keywords', self.keywords )
			
			self.timeout = int( time )
			self.rows = self.validate_rows( rows )
			self.page = self.validate_page( page )
			self.sort = str( sort or 'downloads desc' ).strip( )
			self.media_type = str( media_type or '' ).strip( )
			self.collection = str( collection or '' ).strip( )
			
			active_fields = fields if fields else self.fields
			if not isinstance( active_fields, list ) or not active_fields:
				raise ValueError( 'fields must be a non-empty list of field names.' )
			
			query_text = self.build_query(
				keywords=self.keywords,
				media_type=self.media_type,
				collection=self.collection
			)
			
			self.params = {
					'q': query_text,
					'fl[]': active_fields,
					'rows': self.rows,
					'page': self.page,
					'sort[]': self.sort,
					'output': 'json'
			}
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			payload = self.response.json( ) or { }
			
			return {
					'mode': 'advanced_search',
					'url': self.url,
					'params': self.params,
					'data': payload
			}
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'InternetArchive'
			exception.method = (
					'fetch( self, keywords: str, fields: List[ str ] | None=None, '
					'rows: int=10, page: int=1, sort: str=downloads desc, '
					'media_type: str=, collection: str=, time: int=20 ) '
					'-> Dict[ str, Any ]'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} '
							f'This function uses the {tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'InternetArchive'
			exception.method = (
					'create_schema( self, function: str, tool: str, description: str, '
					'parameters: dict, required: list[ str ] ) -> Dict[ str, str ]'
			)
			raise exception

class OpenWeather( Fetcher ):
	"""Open Weather fetcher.
	
	Purpose:
		Coordinates Open-Meteo current and forecast weather retrieval within Fonky. The class
		stores provider configuration, request parameters, response payloads, and normalized
		result state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		geocode_url (Optional[str]): geocode URL state retained by the instance.
		forecast_url (Optional[str]): forecast URL state retained by the instance.
		location (Optional[str]): location state retained by the instance.
		latitude (Optional[float]): latitude state retained by the instance.
		longitude (Optional[float]): longitude state retained by the instance.
		timezone (Optional[str]): timezone state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		current_metrics (Optional[List[str]]): current metrics state retained by the instance.
		hourly_metrics (Optional[List[str]]): hourly metrics state retained by the instance.
		daily_metrics (Optional[List[str]]): daily metrics state retained by the instance.
		windspeed_unit (Optional[str]): windspeed unit state retained by the instance.
		temperature_unit (Optional[str]): temperature unit state retained by the instance.
		precipitation_unit (Optional[str]): precipitation unit state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		geocode_params (Optional[Dict[str, Any]]): geocode params state retained by the
			instance.
		result_limit (Optional[int]): result limit state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		headers (object): headers state retained by the instance."""
	geocode_url: Optional[ str ]
	forecast_url: Optional[ str ]
	location: Optional[ str ]
	latitude: Optional[ float ]
	longitude: Optional[ float ]
	timezone: Optional[ str ]
	mode: Optional[ str ]
	current_metrics: Optional[ List[ str ] ]
	hourly_metrics: Optional[ List[ str ] ]
	daily_metrics: Optional[ List[ str ] ]
	windspeed_unit: Optional[ str ]
	temperature_unit: Optional[ str ]
	precipitation_unit: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	geocode_params: Optional[ Dict[ str, Any ] ]
	result_limit: Optional[ int ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize OpenWeather.
		
		Purpose:
			Initializes the OpenWeather instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.headers = { }
		self.agents = cfg.AGENTS
		self.location = None
		self.latitude = None
		self.longitude = None
		self.timezone = 'auto'
		self.mode = 'current'
		self.result_limit = 10
		self.geocode_url = 'https://geocoding-api.open-meteo.com/v1/search'
		self.forecast_url = 'https://api.open-meteo.com/v1/forecast'
		self.temperature_unit = 'fahrenheit'
		self.windspeed_unit = 'kn'
		self.precipitation_unit = 'inch'
		self.geocode_params = None
		self.params = None
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
		
		self.current_metrics = [
				'temperature_2m',
				'relative_humidity_2m',
				'apparent_temperature',
				'is_day',
				'precipitation',
				'rain',
				'showers',
				'snowfall',
				'weather_code',
				'cloud_cover',
				'pressure_msl',
				'surface_pressure',
				'wind_speed_10m',
				'wind_direction_10m',
				'wind_gusts_10m'
		]
		
		self.hourly_metrics = [
				'temperature_2m',
				'relative_humidity_2m',
				'apparent_temperature',
				'precipitation_probability',
				'precipitation',
				'rain',
				'showers',
				'snowfall',
				'weather_code',
				'cloud_cover',
				'pressure_msl',
				'surface_pressure',
				'visibility',
				'wind_speed_10m',
				'wind_direction_10m',
				'wind_gusts_10m'
		]
		
		self.daily_metrics = [
				'weather_code',
				'temperature_2m_max',
				'temperature_2m_min',
				'apparent_temperature_max',
				'apparent_temperature_min',
				'sunrise',
				'sunset',
				'daylight_duration',
				'sunshine_duration',
				'precipitation_sum',
				'rain_sum',
				'showers_sum',
				'snowfall_sum',
				'precipitation_hours',
				'precipitation_probability_max',
				'wind_speed_10m_max',
				'wind_gusts_10m_max',
				'wind_direction_10m_dominant'
		]
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'geocode_url',
				'forecast_url',
				'location',
				'latitude',
				'longitude',
				'timezone',
				'mode',
				'current_metrics',
				'hourly_metrics',
				'daily_metrics',
				'windspeed_unit',
				'temperature_unit',
				'precipitation_unit',
				'params',
				'geocode_params',
				'result_limit',
				'geocode_location',
				'fetch',
				'fetch_current',
				'fetch_hourly',
				'fetch_daily',
				'create_schema'
		]
	
	def geocode_location( self, location: str, count: int = 10 ) -> Dict[ str, Any ] | None:
		"""Geocode location.
		
		Purpose:
			Performs the geocode location operation for Open-Meteo current and forecast weather
			retrieval. The method uses the class runtime state and supplied arguments to prepare,
			transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			location (str): location value used by the geocode location operation.
			count (int): count value used by the geocode location operation.
		
		Returns:
			Dict[str, Any] | None: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'location', location )
			self.location = location.strip( )
			self.geocode_params = {
					'name': self.location,
					'count': int( count )
			}
			
			self.url = self.geocode_url
			self.response = requests.get(
				self.url,
				params=self.geocode_params,
				headers=self.headers,
				timeout=20
			)
			self.response.raise_for_status( )
			
			payload = self.response.json( ) or { }
			results = payload.get( 'results', [ ] ) or [ ]
			
			if not results:
				return None
			
			selected = results[ 0 ]
			self.latitude = selected.get( 'latitude', None )
			self.longitude = selected.get( 'longitude', None )
			
			resolved_timezone = selected.get( 'timezone', None )
			if resolved_timezone:
				self.timezone = resolved_timezone
			
			return selected
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenWeather'
			exception.method = (
					'geocode_location( self, location: str, count: int=10 ) '
					'-> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_current( self, lat: float, long: float, zone: str = 'auto',
			past_days: int = 0 ) -> Dict[ str, Any ] | None:
		"""Fetch current.
		
		Purpose:
			Retrieves current using validated arguments and the stored OpenWeather runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			lat (float): lat value used by the fetch current operation.
			long (float): long value used by the fetch current operation.
			zone (str): zone value used by the fetch current operation.
			past_days (int): past days value used by the fetch current operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'lat', lat )
			throw_if( 'long', long )
			throw_if( 'zone', zone )
			
			self.mode = 'current'
			self.latitude = float( lat )
			self.longitude = float( long )
			self.timezone = str( zone or 'auto' ).strip( )
			
			self.params = {
					'latitude': self.latitude,
					'longitude': self.longitude,
					'current': self.current_metrics,
					'timezone': self.timezone,
					'temperature_unit': self.temperature_unit,
					'wind_speed_unit': self.windspeed_unit,
					'precipitation_unit': self.precipitation_unit,
					'past_days': int( past_days )
			}
			
			self.url = self.forecast_url
			self.response = requests.get(
				self.url,
				params=self.params,
				headers=self.headers,
				timeout=30
			)
			self.response.raise_for_status( )
			
			payload = self.response.json( ) or { }
			
			return {
					'mode': self.mode,
					'location': self.location,
					'latitude': payload.get( 'latitude', self.latitude ),
					'longitude': payload.get( 'longitude', self.longitude ),
					'timezone': payload.get( 'timezone', self.timezone ),
					'url': self.url,
					'params': self.params,
					'data': payload
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenWeather'
			exception.method = (
					'fetch_current( self, lat: float, long: float, zone: str=auto, '
					'past_days: int=0 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_hourly( self, lat: float, long: float, zone: str = 'auto',
			forecast_days: int = 7, past_days: int = 0 ) -> Dict[ str, Any ] | None:
		"""Fetch hourly.
		
		Purpose:
			Retrieves hourly using validated arguments and the stored OpenWeather runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			lat (float): lat value used by the fetch hourly operation.
			long (float): long value used by the fetch hourly operation.
			zone (str): zone value used by the fetch hourly operation.
			forecast_days (int): forecast days value used by the fetch hourly operation.
			past_days (int): past days value used by the fetch hourly operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'lat', lat )
			throw_if( 'long', long )
			throw_if( 'zone', zone )
			
			self.mode = 'hourly'
			self.latitude = float( lat )
			self.longitude = float( long )
			self.timezone = str( zone or 'auto' ).strip( )
			
			self.params = {
					'latitude': self.latitude,
					'longitude': self.longitude,
					'hourly': self.hourly_metrics,
					'timezone': self.timezone,
					'forecast_days': int( forecast_days ),
					'past_days': int( past_days ),
					'temperature_unit': self.temperature_unit,
					'wind_speed_unit': self.windspeed_unit,
					'precipitation_unit': self.precipitation_unit
			}
			
			self.url = self.forecast_url
			self.response = requests.get(
				self.url,
				params=self.params,
				headers=self.headers,
				timeout=30
			)
			self.response.raise_for_status( )
			
			payload = self.response.json( ) or { }
			
			return {
					'mode': self.mode,
					'location': self.location,
					'latitude': payload.get( 'latitude', self.latitude ),
					'longitude': payload.get( 'longitude', self.longitude ),
					'timezone': payload.get( 'timezone', self.timezone ),
					'url': self.url,
					'params': self.params,
					'data': payload
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenWeather'
			exception.method = (
					'fetch_hourly( self, lat: float, long: float, zone: str=auto, '
					'forecast_days: int=7, past_days: int=0 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_daily( self, lat: float, long: float, zone: str = 'auto',
			forecast_days: int = 7, past_days: int = 0 ) -> Dict[ str, Any ] | None:
		"""Fetch daily.
		
		Purpose:
			Retrieves daily using validated arguments and the stored OpenWeather runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			lat (float): lat value used by the fetch daily operation.
			long (float): long value used by the fetch daily operation.
			zone (str): zone value used by the fetch daily operation.
			forecast_days (int): forecast days value used by the fetch daily operation.
			past_days (int): past days value used by the fetch daily operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'lat', lat )
			throw_if( 'long', long )
			throw_if( 'zone', zone )
			
			self.mode = 'daily'
			self.latitude = float( lat )
			self.longitude = float( long )
			self.timezone = str( zone or 'auto' ).strip( )
			
			self.params = {
					'latitude': self.latitude,
					'longitude': self.longitude,
					'daily': self.daily_metrics,
					'timezone': self.timezone,
					'forecast_days': int( forecast_days ),
					'past_days': int( past_days ),
					'temperature_unit': self.temperature_unit,
					'wind_speed_unit': self.windspeed_unit,
					'precipitation_unit': self.precipitation_unit
			}
			
			self.url = self.forecast_url
			self.response = requests.get(
				self.url,
				params=self.params,
				headers=self.headers,
				timeout=30
			)
			self.response.raise_for_status( )
			
			payload = self.response.json( ) or { }
			
			return {
					'mode': self.mode,
					'location': self.location,
					'latitude': payload.get( 'latitude', self.latitude ),
					'longitude': payload.get( 'longitude', self.longitude ),
					'timezone': payload.get( 'timezone', self.timezone ),
					'url': self.url,
					'params': self.params,
					'data': payload
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenWeather'
			exception.method = (
					'fetch_daily( self, lat: float, long: float, zone: str=auto, '
					'forecast_days: int=7, past_days: int=0 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch( self, location: str, mode: str = 'current', zone: str = 'auto',
			forecast_days: int = 7, past_days: int = 0,
			count: int = 10 ) -> Dict[ str, Any ] | None:
		"""Fetch Open-Meteo current and forecast weather retrieval.
		
		Purpose:
			Retrieves Open-Meteo current and forecast weather retrieval using validated arguments
			and the stored OpenWeather runtime configuration. The method assembles request
			parameters, executes the provider call or dispatches to a specialized helper, records
			response state when applicable, and returns a normalized payload for downstream analysis
			or tool execution.
		
		Args:
			location (str): location value used by the fetch operation.
			mode (str): mode value used by the fetch operation.
			zone (str): zone value used by the fetch operation.
			forecast_days (int): forecast days value used by the fetch operation.
			past_days (int): past days value used by the fetch operation.
			count (int): count value used by the fetch operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'location', location )
			throw_if( 'mode', mode )
			throw_if( 'zone', zone )
			
			selected = self.geocode_location( location=location, count=count )
			
			if not selected:
				return {
						'location': location,
						'mode': mode,
						'message': 'No geocoding results found.',
						'data': { }
				}
			
			lat = selected.get( 'latitude', None )
			long = selected.get( 'longitude', None )
			
			if lat is None or long is None:
				return {
						'location': location,
						'mode': mode,
						'message': 'Geocoding returned no usable coordinates.',
						'geocoding': selected,
						'data': { }
				}
			
			active_mode = str( mode ).strip( ).lower( )
			if active_mode == 'current':
				result = self.fetch_current(
					lat=float( lat ),
					long=float( long ),
					zone=str( zone or 'auto' ).strip( ),
					past_days=int( past_days )
				) or { }
			
			elif active_mode == 'hourly':
				result = self.fetch_hourly(
					lat=float( lat ),
					long=float( long ),
					zone=str( zone or 'auto' ).strip( ),
					forecast_days=int( forecast_days ),
					past_days=int( past_days )
				) or { }
			
			elif active_mode == 'daily':
				result = self.fetch_daily(
					lat=float( lat ),
					long=float( long ),
					zone=str( zone or 'auto' ).strip( ),
					forecast_days=int( forecast_days ),
					past_days=int( past_days )
				) or { }
			
			else:
				raise ValueError(
					"Unsupported mode. Use 'current', 'hourly', or 'daily'."
				)
			
			result[ 'geocoding' ] = selected
			return result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenWeather'
			exception.method = (
					'fetch( self, location: str, mode: str=current, zone: str=auto, '
					'forecast_days: int=7, past_days: int=0, count: int=10 ) '
					'-> Dict[ str, Any ]'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': f"{description.strip( )} This function uses the {tool.strip( )} service.",
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenWeather'
			exception.method = (
					'create_schema( self, function: str, tool: str, description: str, '
					'parameters: dict, required: list[ str ] ) -> Dict[ str, str ]'
			)
			raise exception

class HistoricalWeather( Fetcher ):
	"""Historical Weather fetcher.
	
	Purpose:
		Coordinates historical weather archive retrieval within Fonky. The class stores provider
		configuration, request parameters, response payloads, and normalized result state so
		callers can access the service through a consistent fetcher interface.
	
	Attributes:
		geocode_url (Optional[str]): geocode URL state retained by the instance.
		archive_url (Optional[str]): archive URL state retained by the instance.
		location (Optional[str]): location state retained by the instance.
		latitude (Optional[float]): latitude state retained by the instance.
		longitude (Optional[float]): longitude state retained by the instance.
		timezone (Optional[str]): timezone state retained by the instance.
		target_date (Optional[dt.date]): target date state retained by the instance.
		daily_metrics (Optional[List[str]]): daily metrics state retained by the instance.
		hourly_metrics (Optional[List[str]]): hourly metrics state retained by the instance.
		windspeed_unit (Optional[str]): windspeed unit state retained by the instance.
		temperature_unit (Optional[str]): temperature unit state retained by the instance.
		precipitation_unit (Optional[str]): precipitation unit state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		geocode_params (Optional[Dict[str, Any]]): geocode params state retained by the
			instance.
		result_limit (Optional[int]): result limit state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		headers (object): headers state retained by the instance."""
	geocode_url: Optional[ str ]
	archive_url: Optional[ str ]
	location: Optional[ str ]
	latitude: Optional[ float ]
	longitude: Optional[ float ]
	timezone: Optional[ str ]
	target_date: Optional[ dt.date ]
	daily_metrics: Optional[ List[ str ] ]
	hourly_metrics: Optional[ List[ str ] ]
	windspeed_unit: Optional[ str ]
	temperature_unit: Optional[ str ]
	precipitation_unit: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	geocode_params: Optional[ Dict[ str, Any ] ]
	result_limit: Optional[ int ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize HistoricalWeather.
		
		Purpose:
			Initializes the HistoricalWeather instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.headers = { }
		self.agents = cfg.AGENTS
		self.location = None
		self.latitude = None
		self.longitude = None
		self.timezone = 'auto'
		self.target_date = None
		self.result_limit = 10
		self.geocode_url = 'https://geocoding-api.open-meteo.com/v1/search'
		self.archive_url = 'https://archive-api.open-meteo.com/v1/archive'
		self.temperature_unit = 'fahrenheit'
		self.windspeed_unit = 'kn'
		self.precipitation_unit = 'inch'
		self.geocode_params = None
		self.params = None
		
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
		
		self.daily_metrics = [
				'weather_code',
				'temperature_2m_max',
				'temperature_2m_min',
				'apparent_temperature_max',
				'apparent_temperature_min',
				'sunrise',
				'sunset',
				'daylight_duration',
				'sunshine_duration',
				'precipitation_sum',
				'rain_sum',
				'showers_sum',
				'snowfall_sum',
				'precipitation_hours',
				'wind_speed_10m_max',
				'wind_gusts_10m_max',
				'wind_direction_10m_dominant'
		]
		
		self.hourly_metrics = [
				'temperature_2m',
				'relative_humidity_2m',
				'apparent_temperature',
				'precipitation',
				'rain',
				'showers',
				'snowfall',
				'weather_code',
				'cloud_cover',
				'pressure_msl',
				'surface_pressure',
				'wind_speed_10m',
				'wind_direction_10m',
				'wind_gusts_10m'
		]
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'geocode_url',
				'archive_url',
				'location',
				'latitude',
				'longitude',
				'timezone',
				'target_date',
				'daily_metrics',
				'hourly_metrics',
				'windspeed_unit',
				'temperature_unit',
				'precipitation_unit',
				'params',
				'geocode_params',
				'result_limit',
				'fetch',
				'geocode_location',
				'fetch_historical',
				'create_schema'
		]
	
	def geocode_location( self, location: str, count: int = 10 ) -> Dict[ str, Any ] | None:
		"""Geocode location.
		
		Purpose:
			Performs the geocode location operation for historical weather archive retrieval. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			location (str): location value used by the geocode location operation.
			count (int): count value used by the geocode location operation.
		
		Returns:
			Dict[str, Any] | None: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'location', location )
			self.location = location.strip( )
			self.geocode_params = {
					'name': self.location,
					'count': int( count )
			}
			
			self.url = self.geocode_url
			self.response = requests.get(
				self.url,
				params=self.geocode_params,
				headers=self.headers,
				timeout=20
			)
			self.response.raise_for_status( )
			
			payload = self.response.json( ) or { }
			results = payload.get( 'results', [ ] ) or [ ]
			
			if not results:
				return None
			
			selected = results[ 0 ]
			self.latitude = selected.get( 'latitude', None )
			self.longitude = selected.get( 'longitude', None )
			
			resolved_timezone = selected.get( 'timezone', None )
			if resolved_timezone:
				self.timezone = resolved_timezone
			
			return selected
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'HistoricalWeather'
			exception.method = (
					'geocode_location( self, location: str, count: int=10 ) '
					'-> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_historical( self, lat: float, long: float, date: dt.date,
			zone: str = 'auto' ) -> Dict[ str, Any ] | None:
		"""Fetch historical.
		
		Purpose:
			Retrieves historical using validated arguments and the stored HistoricalWeather runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			lat (float): lat value used by the fetch historical operation.
			long (float): long value used by the fetch historical operation.
			date (dt.date): date value used by the fetch historical operation.
			zone (str): zone value used by the fetch historical operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'lat', lat )
			throw_if( 'long', long )
			throw_if( 'date', date )
			throw_if( 'zone', zone )
			
			self.latitude = float( lat )
			self.longitude = float( long )
			self.target_date = date
			self.timezone = zone.strip( ) if zone else 'auto'
			
			self.params = {
					'latitude': self.latitude,
					'longitude': self.longitude,
					'start_date': self.target_date.isoformat( ),
					'end_date': self.target_date.isoformat( ),
					'timezone': self.timezone,
					'daily': self.daily_metrics,
					'hourly': self.hourly_metrics,
					'temperature_unit': self.temperature_unit,
					'wind_speed_unit': self.windspeed_unit,
					'precipitation_unit': self.precipitation_unit
			}
			
			self.url = self.archive_url
			self.response = requests.get(
				self.url,
				params=self.params,
				headers=self.headers,
				timeout=30
			)
			self.response.raise_for_status( )
			
			payload = self.response.json( ) or { }
			
			return {
					'location': self.location,
					'latitude': self.latitude,
					'longitude': self.longitude,
					'timezone': payload.get( 'timezone', self.timezone ),
					'date': self.target_date.isoformat( ),
					'url': self.url,
					'params': self.params,
					'data': payload
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'HistoricalWeather'
			exception.method = (
					'fetch_historical( self, lat: float, long: float, date: dt.date, '
					'zone: str=auto ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch( self, location: str, date: dt.date,
			zone: str = 'auto', count: int = 10 ) -> Dict[ str, Any ] | None:
		"""Fetch historical weather archive retrieval.
		
		Purpose:
			Retrieves historical weather archive retrieval using validated arguments and the stored
			HistoricalWeather runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			location (str): location value used by the fetch operation.
			date (dt.date): date value used by the fetch operation.
			zone (str): zone value used by the fetch operation.
			count (int): count value used by the fetch operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'location', location )
			throw_if( 'date', date )
			throw_if( 'zone', zone )
			
			selected = self.geocode_location( location=location, count=count )
			
			if not selected:
				return {
						'location': location,
						'date': date.isoformat( ),
						'message': 'No geocoding results found.',
						'data': { }
				}
			
			lat = selected.get( 'latitude', None )
			long = selected.get( 'longitude', None )
			
			if lat is None or long is None:
				return {
						'location': location,
						'date': date.isoformat( ),
						'message': 'Geocoding returned no usable coordinates.',
						'geocoding': selected,
						'data': { }
				}
			
			result = self.fetch_historical(
				lat=float( lat ),
				long=float( long ),
				date=date,
				zone=str( zone or 'auto' ).strip( )
			) or { }
			
			result[ 'geocoding' ] = selected
			return result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'HistoricalWeather'
			exception.method = (
					'fetch( self, location: str, date: dt.date, zone: str=auto, '
					'count: int=10 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': f"{description.strip( )} This function uses the {tool.strip( )} service.",
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'HistoricalWeather'
			exception.method = (
					'create_schema( self, function: str, tool: str, description: str, '
					'parameters: dict, required: list[ str ] ) -> Dict[ str, str ]'
			)
			raise exception

class Grokipedia( Fetcher ):
	"""Grokipedia fetcher.
	
	Purpose:
		Coordinates Grokipedia search and page retrieval within Fonky. The class stores provider
		configuration, request parameters, response payloads, and normalized result state so
		callers can access the service through a consistent fetcher interface.
	
	Attributes:
		api_key (Optional[str]): API key state retained by the instance.
		client (Optional[GrokipediaClient]): client state retained by the instance.
		query (Optional[str]): query state retained by the instance.
		page (Optional[str]): page state retained by the instance.
		limit (Optional[int]): limit state retained by the instance.
		offset (Optional[int]): offset state retained by the instance.
		include_content (Optional[bool]): include content state retained by the instance.
		response (Optional[Dict[str, Any]]): response state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		url (object): URL state retained by the instance.
		headers (object): headers state retained by the instance.
		timeout (object): timeout state retained by the instance."""
	api_key: Optional[ str ]
	client: Optional[ GrokipediaClient ]
	query: Optional[ str ]
	page: Optional[ str ]
	limit: Optional[ int ]
	offset: Optional[ int ]
	include_content: Optional[ bool ]
	response: Optional[ Dict[ str, Any ] ]
	params: Optional[ Dict[ str, Any ] ]
	result: Optional[ Dict[ str, Any ] ]
	
	def __init__( self ) -> None:
		"""Initialize Grokipedia.
		
		Purpose:
			Initializes the Grokipedia instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.api_key = cfg.XAI_API_KEY
		self.url = None
		self.client = None
		self.query = ''
		self.page = ''
		self.response = None
		self.params = { }
		self.result = { }
		self.limit = 12
		self.offset = 0
		self.include_content = True
		self.headers = { }
		self.timeout = 20
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'api_key',
				'client',
				'query',
				'page',
				'limit',
				'offset',
				'include_content',
				'response',
				'params',
				'result',
				'fetch_search',
				'fetch_page',
				'fetch',
				'create_schema'
		]
	
	def fetch_search( self, query: str, limit: int = 12,
			offset: int = 0 ) -> Dict[ str, Any ] | None:
		"""Fetch search.
		
		Purpose:
			Retrieves search using validated arguments and the stored Grokipedia runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			query (str): Search text, lookup value, or provider query submitted by the caller.
			limit (int): limit value used by the fetch search operation.
			offset (int): offset value used by the fetch search operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'query', query )
			throw_if( 'limit', limit )
			throw_if( 'offset', offset )
			
			self.query = str( query ).strip( )
			self.limit = int( limit )
			self.offset = int( offset )
			self.client = GrokipediaClient( )
			self.url = 'grokipedia.search'
			self.params = {
					'query': self.query,
					'limit': self.limit,
					'offset': self.offset
			}
			
			self.response = self.client.search(
				query=self.query,
				limit=self.limit,
				offset=self.offset
			)
			
			self.result = {
					'mode': 'search',
					'url': self.url,
					'params': self.params,
					'api_key_configured': bool( str( self.api_key or '' ).strip( ) ),
					'data': self.response
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Grokipedia'
			exception.method = 'fetch_search( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def fetch_page( self, page: str,
			include_content: bool = True ) -> Dict[ str, Any ] | None:
		"""Fetch page.
		
		Purpose:
			Retrieves page using validated arguments and the stored Grokipedia runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			page (str): page value used by the fetch page operation.
			include_content (bool): include content value used by the fetch page operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'page', page )
			
			self.page = str( page ).strip( )
			self.include_content = bool( include_content )
			self.client = GrokipediaClient( )
			self.url = 'grokipedia.get_page'
			self.params = {
					'page': self.page,
					'include_content': self.include_content
			}
			
			self.response = self.client.get_page(
				self.page,
				include_content=self.include_content
			)
			
			self.result = {
					'mode': 'page',
					'url': self.url,
					'params': self.params,
					'api_key_configured': bool( str( self.api_key or '' ).strip( ) ),
					'data': self.response
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Grokipedia'
			exception.method = 'fetch_page( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def fetch( self, mode: str = 'search', query: str = '', page: str = '',
			limit: int = 12, offset: int = 0,
			include_content: bool = True ) -> Dict[ str, Any ] | None:
		"""Fetch Grokipedia search and page retrieval.
		
		Purpose:
			Retrieves Grokipedia search and page retrieval using validated arguments and the stored
			Grokipedia runtime configuration. The method assembles request parameters, executes the
			provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			query (str): Search text, lookup value, or provider query submitted by the caller.
			page (str): page value used by the fetch operation.
			limit (int): limit value used by the fetch operation.
			offset (int): offset value used by the fetch operation.
			include_content (bool): include content value used by the fetch operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			mode_value = str( mode or 'search' ).strip( ).lower( )
			
			if mode_value == 'search':
				return self.fetch_search( query=query, limit=limit, offset=offset )
			
			if mode_value == 'page':
				return self.fetch_page( page=page, include_content=include_content )
			
			raise ValueError( "Unsupported Grokipedia mode. Use 'search' or 'page'." )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Grokipedia'
			exception.method = 'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} '
							f'This function uses the {tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Grokipedia'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class GoogleGeocoding( Fetcher ):
	"""Google Geocoding fetcher.
	
	Purpose:
		Coordinates Google forward, reverse, and place geocoding within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		api_key (Optional[str]): API key state retained by the instance.
		url (Optional[str]): URL state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		query (Optional[str]): query state retained by the instance.
		latitude (Optional[float]): latitude state retained by the instance.
		longitude (Optional[float]): longitude state retained by the instance.
		place_id (Optional[str]): place ID state retained by the instance.
		language (Optional[str]): language state retained by the instance.
		region (Optional[str]): region state retained by the instance.
		result_type (Optional[str]): result type state retained by the instance.
		location_type (Optional[str]): location type state retained by the instance.
		timeout (Optional[int]): timeout state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		response (object): response state retained by the instance.
		headers (object): headers state retained by the instance."""
	api_key: Optional[ str ]
	url: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	mode: Optional[ str ]
	query: Optional[ str ]
	latitude: Optional[ float ]
	longitude: Optional[ float ]
	place_id: Optional[ str ]
	language: Optional[ str ]
	region: Optional[ str ]
	result_type: Optional[ str ]
	location_type: Optional[ str ]
	timeout: Optional[ int ]
	agents: Optional[ str ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	
	def __init__( self ) -> None:
		"""Initialize GoogleGeocoding.
		
		Purpose:
			Initializes the GoogleGeocoding instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.api_key = cfg.GOOGLE_API_KEY
		self.url = 'https://maps.googleapis.com/maps/api/geocode/json'
		self.params = { }
		self.mode = 'forward'
		self.query = ''
		self.latitude = None
		self.longitude = None
		self.place_id = ''
		self.language = 'en'
		self.region = ''
		self.result_type = ''
		self.location_type = ''
		self.timeout = 10
		self.agents = cfg.AGENTS
		self.response = None
		self.payload = { }
		self.result = { }
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'api_key',
				'url',
				'params',
				'mode',
				'query',
				'latitude',
				'longitude',
				'place_id',
				'language',
				'region',
				'result_type',
				'location_type',
				'timeout',
				'agents',
				'response',
				'payload',
				'result',
				'request',
				'fetch_forward',
				'fetch_reverse',
				'fetch_place',
				'fetch',
				'create_schema'
		]
	
	def request( self, params: Dict[ str, Any ], time: int = 10,
			api_key: Optional[ str ] = None ) -> Dict[ str, Any ] | None:
		"""Request Google forward, reverse, and place geocoding.
		
		Purpose:
			Sends a provider request for Google forward, reverse, and place geocoding after request
			parameters have been validated or prepared by the caller. The method stores request,
			response, and payload state on the instance so subsequent methods can package or inspect
			the result consistently.
		
		Args:
			params (Dict[str, Any]): Request or schema parameter dictionary used by the operation.
			time (int): Request timeout in seconds.
			api_key (Optional[str]): Optional credential override used for the active request.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'params', params )
			throw_if( 'time', time )
			
			if api_key:
				self.api_key = str( api_key ).strip( )
			
			throw_if( 'api_key', self.api_key )
			
			self.timeout = int( time )
			self.params = { }
			
			for key, value in (params or { }).items( ):
				if value is None:
					continue
				
				if isinstance( value, str ) and not value.strip( ):
					continue
				
				self.params[ key ] = value
			
			self.params[ 'key' ] = self.api_key
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			
			self.response.raise_for_status( )
			self.payload = self.response.json( )
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'status': self.payload.get( 'status', '' ) if isinstance( self.payload,
						dict ) else '',
					'results': self.payload.get( 'results', [ ] )
					if isinstance( self.payload, dict )
					else [ ],
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GoogleGeocoding'
			exception.method = (
					'request( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_forward( self, query: str, language: str = 'en',
			region: str = '', time: int = 10,
			api_key: Optional[ str ] = None ) -> Dict[ str, Any ] | None:
		"""Fetch forward.
		
		Purpose:
			Retrieves forward using validated arguments and the stored GoogleGeocoding runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			query (str): Search text, lookup value, or provider query submitted by the caller.
			language (str): language value used by the fetch forward operation.
			region (str): region value used by the fetch forward operation.
			time (int): Request timeout in seconds.
			api_key (Optional[str]): Optional credential override used for the active request.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'query', query )
			throw_if( 'time', time )
			
			self.mode = 'forward'
			self.query = str( query ).strip( )
			self.language = str( language or 'en' ).strip( )
			self.region = str( region or '' ).strip( )
			self.timeout = int( time )
			self.params = {
					'address': self.query,
					'language': self.language
			}
			
			if self.region:
				self.params[ 'region' ] = self.region
			
			return self.request(
				params=self.params,
				time=self.timeout,
				api_key=api_key
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GoogleGeocoding'
			exception.method = (
					'fetch_forward( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_reverse( self, latitude: float, longitude: float,
			language: str = 'en', result_type: str = '',
			location_type: str = '', time: int = 10,
			api_key: Optional[ str ] = None ) -> Dict[ str, Any ] | None:
		"""Fetch reverse.
		
		Purpose:
			Retrieves reverse using validated arguments and the stored GoogleGeocoding runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			latitude (float): latitude value used by the fetch reverse operation.
			longitude (float): longitude value used by the fetch reverse operation.
			language (str): language value used by the fetch reverse operation.
			result_type (str): result type value used by the fetch reverse operation.
			location_type (str): location type value used by the fetch reverse operation.
			time (int): Request timeout in seconds.
			api_key (Optional[str]): Optional credential override used for the active request.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'latitude', latitude )
			throw_if( 'longitude', longitude )
			throw_if( 'time', time )
			
			self.mode = 'reverse'
			self.latitude = float( latitude )
			self.longitude = float( longitude )
			self.language = str( language or 'en' ).strip( )
			self.result_type = str( result_type or '' ).strip( )
			self.location_type = str( location_type or '' ).strip( )
			self.timeout = int( time )
			self.params = {
					'latlng': f'{self.latitude},{self.longitude}',
					'language': self.language
			}
			
			if self.result_type:
				self.params[ 'result_type' ] = self.result_type
			
			if self.location_type:
				self.params[ 'location_type' ] = self.location_type
			
			return self.request(
				params=self.params,
				time=self.timeout,
				api_key=api_key
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GoogleGeocoding'
			exception.method = (
					'fetch_reverse( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_place( self, place_id: str, language: str = 'en',
			region: str = '', time: int = 10,
			api_key: Optional[ str ] = None ) -> Dict[ str, Any ] | None:
		"""Fetch place.
		
		Purpose:
			Retrieves place using validated arguments and the stored GoogleGeocoding runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			place_id (str): place ID value used by the fetch place operation.
			language (str): language value used by the fetch place operation.
			region (str): region value used by the fetch place operation.
			time (int): Request timeout in seconds.
			api_key (Optional[str]): Optional credential override used for the active request.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'place_id', place_id )
			throw_if( 'time', time )
			
			self.mode = 'place'
			self.place_id = str( place_id ).strip( )
			self.language = str( language or 'en' ).strip( )
			self.region = str( region or '' ).strip( )
			self.timeout = int( time )
			self.params = {
					'place_id': self.place_id,
					'language': self.language
			}
			
			if self.region:
				self.params[ 'region' ] = self.region
			
			return self.request(
				params=self.params,
				time=self.timeout,
				api_key=api_key
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GoogleGeocoding'
			exception.method = (
					'fetch_place( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'forward', query: str = '',
			latitude: float = 0.0, longitude: float = 0.0,
			place_id: str = '', language: str = 'en', region: str = '',
			result_type: str = '', location_type: str = '', time: int = 10,
			api_key: Optional[ str ] = None ) -> Dict[ str, Any ] | None:
		"""Fetch Google forward, reverse, and place geocoding.
		
		Purpose:
			Retrieves Google forward, reverse, and place geocoding using validated arguments and the
			stored GoogleGeocoding runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			query (str): Search text, lookup value, or provider query submitted by the caller.
			latitude (float): latitude value used by the fetch operation.
			longitude (float): longitude value used by the fetch operation.
			place_id (str): place ID value used by the fetch operation.
			language (str): language value used by the fetch operation.
			region (str): region value used by the fetch operation.
			result_type (str): result type value used by the fetch operation.
			location_type (str): location type value used by the fetch operation.
			time (int): Request timeout in seconds.
			api_key (Optional[str]): Optional credential override used for the active request.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			self.mode = str( mode ).strip( ).lower( )
			
			if self.mode == 'forward':
				return self.fetch_forward(
					query=query,
					language=language,
					region=region,
					time=time,
					api_key=api_key
				)
			
			if self.mode == 'reverse':
				return self.fetch_reverse(
					latitude=latitude,
					longitude=longitude,
					language=language,
					result_type=result_type,
					location_type=location_type,
					time=time,
					api_key=api_key
				)
			
			if self.mode == 'place':
				return self.fetch_place(
					place_id=place_id,
					language=language,
					region=region,
					time=time,
					api_key=api_key
				)
			
			raise ValueError( "Unsupported geocoding mode. Use 'forward', 'reverse', or 'place'." )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GoogleGeocoding'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f"{description.strip( )} This function uses the "
							f"{tool.strip( )} service."
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GoogleGeocoding'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class CensusData( Fetcher ):
	"""Census Data fetcher.
	
	Purpose:
		Coordinates U.S. Census dataset and variable retrieval within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		api_key (Optional[str]): API key state retained by the instance.
		base_url (Optional[str]): base URL state retained by the instance.
		year (Optional[str]): year state retained by the instance.
		dataset (Optional[str]): dataset state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		fields (Optional[List[str]]): fields state retained by the instance.
		geography_for (Optional[str]): geography for state retained by the instance.
		geography_in (Optional[str]): geography in state retained by the instance.
		predicates (Optional[Dict[str, Any]]): predicates state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	api_key: Optional[ str ]
	base_url: Optional[ str ]
	year: Optional[ str ]
	dataset: Optional[ str ]
	mode: Optional[ str ]
	fields: Optional[ List[ str ] ]
	geography_for: Optional[ str ]
	geography_in: Optional[ str ]
	predicates: Optional[ Dict[ str, Any ] ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize CensusData.
		
		Purpose:
			Initializes the CensusData instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.api_key = cfg.CENSUS_API_KEY
		self.base_url = 'https://api.census.gov/data'
		self.year = None
		self.dataset = None
		self.mode = None
		self.fields = [ ]
		self.geography_for = None
		self.geography_in = None
		self.predicates = { }
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents,
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'api_key',
				'base_url',
				'year',
				'dataset',
				'mode',
				'fields',
				'geography_for',
				'geography_in',
				'predicates',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'normalize_fields',
				'parse_predicates',
				'shape_table',
				'fetch_variables',
				'fetch_data',
				'fetch',
				'create_schema'
		]
	
	def normalize_fields( self, fields: str ) -> str:
		"""Normalize fields.
		
		Purpose:
			Converts fields into the canonical format expected by the CensusData request workflow.
			The method standardizes caller input before it is used in endpoint paths, query
			parameters, filters, or response processing.
		
		Args:
			fields (str): fields value used by the normalize fields operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'fields', fields )
			
			self.fields = [
					field.strip( )
					for field in str( fields ).split( ',' )
					if field and field.strip( )
			]
			
			if not self.fields:
				raise ValueError( 'At least one Census field is required.' )
			
			return ','.join( self.fields )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'CensusData'
			exception.method = 'normalize_fields( self, *args, **kwargs ) -> str'
			raise exception
	
	def parse_predicates( self, predicates: str = '' ) -> Dict[ str, Any ]:
		"""Parse predicates.
		
		Purpose:
			Performs the parse predicates operation for U.S. Census dataset and variable retrieval.
			The method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			predicates (str): predicates value used by the parse predicates operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.predicates = { }
			text = str( predicates or '' ).strip( )
			
			if not text:
				return self.predicates
			
			for line in text.splitlines( ):
				clean = str( line or '' ).strip( )
				
				if not clean:
					continue
				
				if '=' not in clean:
					raise ValueError(
						'Each Census predicate line must use key=value format.'
					)
				
				key, value = clean.split( '=', 1 )
				key = key.strip( )
				value = value.strip( )
				
				throw_if( 'predicate key', key )
				throw_if( 'predicate value', value )
				
				self.predicates[ key ] = value
			
			return self.predicates
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'CensusData'
			exception.method = (
					'parse_predicates( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def shape_table( self, rows: List[ Any ] ) -> Dict[ str, Any ]:
		"""Shape table.
		
		Purpose:
			Transforms raw provider records into table structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			rows (List[Any]): rows value used by the shape table operation.
		
		Returns:
			Dict[str, Any]: Normalized rows or summary structures created from provider response
				records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if not rows:
				return {
						'columns': [ ],
						'rows': [ ],
						'count': 0,
				}
			
			headers = rows[ 0 ] if isinstance( rows[ 0 ], list ) else [ ]
			data_rows = rows[ 1: ] if len( rows ) > 1 else [ ]
			records: List[ Dict[ str, Any ] ] = [ ]
			
			for row in data_rows:
				if isinstance( row, list ) and headers:
					records.append(
						{
								headers[ index ]: row[ index ] if index < len( row ) else ''
								for index in range( len( headers ) )
						}
					)
			
			return {
					'columns': headers,
					'rows': records,
					'count': len( records ),
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'CensusData'
			exception.method = (
					'shape_table( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_variables( self, year: str, dataset: str,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch variables.
		
		Purpose:
			Retrieves variables using validated arguments and the stored CensusData runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			year (str): year value used by the fetch variables operation.
			dataset (str): dataset value used by the fetch variables operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'year', year )
			throw_if( 'dataset', dataset )
			throw_if( 'time', time )
			self.mode = 'variables'
			self.year = str( year ).strip( )
			self.dataset = str( dataset ).strip( ).strip( '/' )
			self.timeout = int( time )
			self.url = f'{self.base_url}/{self.year}/{self.dataset}/variables.json'
			self.params = { }
			
			if self.api_key:
				self.params[ 'key' ] = self.api_key
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.json( )
			self.result = {
					'mode': self.mode,
					'url': self.response.url,
					'params': self.params,
					'data': self.payload,
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'CensusData'
			exception.method = (
					'fetch_variables( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_data( self, year: str, dataset: str, fields: str,
			geography_for: str = '', geography_in: str = '',
			predicates: str = '', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch data.
		
		Purpose:
			Retrieves data using validated arguments and the stored CensusData runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			year (str): year value used by the fetch data operation.
			dataset (str): dataset value used by the fetch data operation.
			fields (str): fields value used by the fetch data operation.
			geography_for (str): geography for value used by the fetch data operation.
			geography_in (str): geography in value used by the fetch data operation.
			predicates (str): predicates value used by the fetch data operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'year', year )
			throw_if( 'dataset', dataset )
			throw_if( 'fields', fields )
			throw_if( 'geography_for', geography_for )
			throw_if( 'time', time )
			
			self.mode = 'data'
			self.year = str( year ).strip( )
			self.dataset = str( dataset ).strip( ).strip( '/' )
			self.geography_for = str( geography_for or '' ).strip( )
			self.geography_in = str( geography_in or '' ).strip( )
			self.predicates = self.parse_predicates( predicates )
			self.timeout = int( time )
			self.url = f'{self.base_url}/{self.year}/{self.dataset}'
			self.params = {
					'get': self.normalize_fields( fields ),
					'for': self.geography_for,
			}
			
			if self.geography_in:
				self.params[ 'in' ] = self.geography_in
			
			if self.predicates:
				self.params.update( self.predicates )
			
			if self.api_key:
				self.params[ 'key' ] = self.api_key
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.json( )
			self.result = {
					'mode': self.mode,
					'url': self.response.url,
					'params': self.params,
					'data': self.shape_table( self.payload ),
					'raw': self.payload,
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'CensusData'
			exception.method = (
					'fetch_data( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'variables', year: str = '2022',
			dataset: str = 'acs/acs5', fields: str = 'NAME,B01001_001E',
			geography_for: str = 'state:*', geography_in: str = '',
			predicates: str = '', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch U.S. Census dataset and variable retrieval.
		
		Purpose:
			Retrieves U.S. Census dataset and variable retrieval using validated arguments and the
			stored CensusData runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			year (str): year value used by the fetch operation.
			dataset (str): dataset value used by the fetch operation.
			fields (str): fields value used by the fetch operation.
			geography_for (str): geography for value used by the fetch operation.
			geography_in (str): geography in value used by the fetch operation.
			predicates (str): predicates value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			self.mode = str( mode ).strip( ).lower( )
			
			if self.mode == 'variables':
				return self.fetch_variables(
					year=year,
					dataset=dataset,
					time=time
				)
			
			if self.mode == 'data':
				return self.fetch_data(
					year=year,
					dataset=dataset,
					fields=fields,
					geography_for=geography_for,
					geography_in=geography_in,
					predicates=predicates,
					time=time
				)
			
			raise ValueError( "Unsupported Census mode. Use 'variables' or 'data'." )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'CensusData'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f"{description.strip( )} This function uses the "
							f"{tool.strip( )} service."
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'CensusData'
			exception.method = 'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			raise exception

class Socrata( Fetcher ):
	"""Socrata fetcher.
	
	Purpose:
		Coordinates Socrata dataset metadata and row retrieval within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		api_key (Optional[str]): API key state retained by the instance.
		base_url (Optional[str]): base URL state retained by the instance.
		metadata_url (Optional[str]): metadata URL state retained by the instance.
		domain (Optional[str]): domain state retained by the instance.
		dataset_id (Optional[str]): dataset ID state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		select_clause (Optional[str]): select clause state retained by the instance.
		where_clause (Optional[str]): where clause state retained by the instance.
		order_clause (Optional[str]): order clause state retained by the instance.
		group_clause (Optional[str]): group clause state retained by the instance.
		limit_value (Optional[int]): limit value state retained by the instance.
		offset_value (Optional[int]): offset value state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	api_key: Optional[ str ]
	base_url: Optional[ str ]
	metadata_url: Optional[ str ]
	domain: Optional[ str ]
	dataset_id: Optional[ str ]
	mode: Optional[ str ]
	select_clause: Optional[ str ]
	where_clause: Optional[ str ]
	order_clause: Optional[ str ]
	group_clause: Optional[ str ]
	limit_value: Optional[ int ]
	offset_value: Optional[ int ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize Socrata.
		
		Purpose:
			Initializes the Socrata instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.api_key = cfg.SOCRATA_API_KEY
		self.base_url = 'https://{domain}/resource/{dataset}.json'
		self.metadata_url = 'https://{domain}/api/views/{dataset}.json'
		self.domain = None
		self.dataset_id = None
		self.mode = 'rows'
		self.select_clause = ''
		self.where_clause = ''
		self.order_clause = ''
		self.group_clause = ''
		self.limit_value = 25
		self.offset_value = 0
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents
		}
		
		if self.api_key:
			self.headers[ 'X-App-Token' ] = self.api_key
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'api_key',
				'base_url',
				'metadata_url',
				'domain',
				'dataset_id',
				'mode',
				'select_clause',
				'where_clause',
				'order_clause',
				'group_clause',
				'limit_value',
				'offset_value',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'normalize_domain',
				'normalize_dataset_id',
				'validate_limit',
				'validate_offset',
				'fetch_metadata',
				'fetch_rows',
				'fetch',
				'create_schema'
		]
	
	def normalize_domain( self, domain: str ) -> str:
		"""Normalize domain.
		
		Purpose:
			Converts domain into the canonical format expected by the Socrata request workflow. The
			method standardizes caller input before it is used in endpoint paths, query parameters,
			filters, or response processing.
		
		Args:
			domain (str): domain value used by the normalize domain operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'domain', domain )
			
			value = str( domain ).strip( )
			value = value.replace( 'https://', '' ).replace( 'http://', '' ).strip( '/' )
			
			if not value or '.' not in value:
				raise ValueError( 'domain must be a valid Socrata portal domain.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Socrata'
			exception.method = 'normalize_domain( self, *args, **kwargs ) -> str'
			raise exception
	
	def normalize_dataset_id( self, dataset_id: str ) -> str:
		"""Normalize dataset id.
		
		Purpose:
			Converts dataset id into the canonical format expected by the Socrata request workflow.
			The method standardizes caller input before it is used in endpoint paths, query
			parameters, filters, or response processing.
		
		Args:
			dataset_id (str): dataset ID value used by the normalize dataset id operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'dataset_id', dataset_id )
			
			value = str( dataset_id ).strip( )
			value = value.replace( '.json', '' ).strip( '/' )
			
			if not value:
				raise ValueError( 'dataset_id cannot be empty.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Socrata'
			exception.method = 'normalize_dataset_id( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_limit( self, limit: int ) -> int:
		"""Validate limit.
		
		Purpose:
			Validates and normalizes limit before it is used in Socrata dataset metadata and row
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			limit (int): limit value used by the validate limit operation.
		
		Returns:
			int: Validated limit value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'limit', limit )
			
			value = int( limit )
			if value < 1 or value > 50000:
				raise ValueError( 'limit must be between 1 and 50000.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Socrata'
			exception.method = 'validate_limit( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_offset( self, offset: int ) -> int:
		"""Validate offset.
		
		Purpose:
			Validates and normalizes offset before it is used in Socrata dataset metadata and row
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			offset (int): offset value used by the validate offset operation.
		
		Returns:
			int: Validated offset value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if offset is None:
				raise ValueError( 'offset cannot be None.' )
			
			value = int( offset )
			if value < 0:
				raise ValueError( 'offset must be greater than or equal to 0.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Socrata'
			exception.method = 'validate_offset( self, *args, **kwargs ) -> int'
			raise exception
	
	def fetch_metadata( self, domain: str, dataset_id: str,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch metadata.
		
		Purpose:
			Retrieves metadata using validated arguments and the stored Socrata runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			domain (str): domain value used by the fetch metadata operation.
			dataset_id (str): dataset ID value used by the fetch metadata operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'time', time )
			
			self.mode = 'metadata'
			self.domain = self.normalize_domain( domain )
			self.dataset_id = self.normalize_dataset_id( dataset_id )
			self.timeout = int( time )
			self.url = self.metadata_url.format(
				domain=self.domain,
				dataset=self.dataset_id
			)
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			if self.api_key:
				self.headers[ 'X-App-Token' ] = self.api_key
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			self.payload = self.response.json( )
			self.result = {
					'mode': self.mode,
					'url': self.response.url,
					'params': self.params,
					'data': self.payload,
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Socrata'
			exception.method = (
					'fetch_metadata( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_rows( self, domain: str, dataset_id: str, select: str = '',
			where: str = '', order: str = '', group: str = '',
			limit: int = 25, offset: int = 0,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch rows.
		
		Purpose:
			Retrieves rows using validated arguments and the stored Socrata runtime configuration.
			The method assembles request parameters, executes the provider call or dispatches to a
			specialized helper, records response state when applicable, and returns a normalized
			payload for downstream analysis or tool execution.
		
		Args:
			domain (str): domain value used by the fetch rows operation.
			dataset_id (str): dataset ID value used by the fetch rows operation.
			select (str): select value used by the fetch rows operation.
			where (str): where value used by the fetch rows operation.
			order (str): order value used by the fetch rows operation.
			group (str): group value used by the fetch rows operation.
			limit (int): limit value used by the fetch rows operation.
			offset (int): offset value used by the fetch rows operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'time', time )
			
			self.mode = 'rows'
			self.domain = self.normalize_domain( domain )
			self.dataset_id = self.normalize_dataset_id( dataset_id )
			self.select_clause = str( select or '' ).strip( )
			self.where_clause = str( where or '' ).strip( )
			self.order_clause = str( order or '' ).strip( )
			self.group_clause = str( group or '' ).strip( )
			self.limit_value = self.validate_limit( limit )
			self.offset_value = self.validate_offset( offset )
			self.timeout = int( time )
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			self.url = self.base_url.format(
				domain=self.domain,
				dataset=self.dataset_id
			)
			self.params = {
					'$limit': self.limit_value,
					'$offset': self.offset_value,
			}
			
			if self.select_clause:
				self.params[ '$select' ] = self.select_clause
			
			if self.where_clause:
				self.params[ '$where' ] = self.where_clause
			
			if self.order_clause:
				self.params[ '$order' ] = self.order_clause
			
			if self.group_clause:
				self.params[ '$group' ] = self.group_clause
			
			if self.api_key:
				self.headers[ 'X-App-Token' ] = self.api_key
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			self.payload = self.response.json( )
			self.result = {
					'mode': self.mode,
					'url': self.response.url,
					'params': self.params,
					'count': len( self.payload ) if isinstance( self.payload, list ) else 0,
					'data': self.payload,
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Socrata'
			exception.method = (
					'fetch_rows( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'rows', domain: str = 'data.cdc.gov',
			dataset_id: str = '', select: str = '', where: str = '',
			order: str = '', group: str = '', limit: int = 25,
			offset: int = 0, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch Socrata dataset metadata and row retrieval.
		
		Purpose:
			Retrieves Socrata dataset metadata and row retrieval using validated arguments and the
			stored Socrata runtime configuration. The method assembles request parameters, executes
			the provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			domain (str): domain value used by the fetch operation.
			dataset_id (str): dataset ID value used by the fetch operation.
			select (str): select value used by the fetch operation.
			where (str): where value used by the fetch operation.
			order (str): order value used by the fetch operation.
			group (str): group value used by the fetch operation.
			limit (int): limit value used by the fetch operation.
			offset (int): offset value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			self.mode = str( mode or 'rows' ).strip( ).lower( )
			
			if self.mode == 'metadata':
				return self.fetch_metadata(
					domain=domain,
					dataset_id=dataset_id,
					time=time
				)
			
			if self.mode == 'rows':
				return self.fetch_rows(
					domain=domain,
					dataset_id=dataset_id,
					select=select,
					where=where,
					order=order,
					group=group,
					limit=limit,
					offset=offset,
					time=time
				)
			
			raise ValueError( "Unsupported Socrata mode. Use 'metadata' or 'rows'." )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Socrata'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f"{description.strip( )} This function uses the "
							f"{tool.strip( )} service."
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Socrata'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class HealthData( Fetcher ):
	"""Health Data fetcher.
	
	Purpose:
		Coordinates HealthData.gov Socrata metadata and rows within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		api_key (Optional[str]): API key state retained by the instance.
		base_url (Optional[str]): base URL state retained by the instance.
		metadata_url (Optional[str]): metadata URL state retained by the instance.
		domain (Optional[str]): domain state retained by the instance.
		dataset_id (Optional[str]): dataset ID state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		select_clause (Optional[str]): select clause state retained by the instance.
		where_clause (Optional[str]): where clause state retained by the instance.
		order_clause (Optional[str]): order clause state retained by the instance.
		group_clause (Optional[str]): group clause state retained by the instance.
		limit_value (Optional[int]): limit value state retained by the instance.
		offset_value (Optional[int]): offset value state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	api_key: Optional[ str ]
	base_url: Optional[ str ]
	metadata_url: Optional[ str ]
	domain: Optional[ str ]
	dataset_id: Optional[ str ]
	mode: Optional[ str ]
	select_clause: Optional[ str ]
	where_clause: Optional[ str ]
	order_clause: Optional[ str ]
	group_clause: Optional[ str ]
	limit_value: Optional[ int ]
	offset_value: Optional[ int ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize HealthData.
		
		Purpose:
			Initializes the HealthData instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.api_key = cfg.HEALTHDATA_API_KEY
		self.base_url = 'https://{domain}/resource/{dataset}.json'
		self.metadata_url = 'https://{domain}/api/views/{dataset}.json'
		self.domain = 'healthdata.gov'
		self.dataset_id = ''
		self.mode = 'rows'
		self.select_clause = ''
		self.where_clause = ''
		self.order_clause = ''
		self.group_clause = ''
		self.limit_value = 25
		self.offset_value = 0
		self.params = { }
		self.payload = [ ]
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents,
		}
		
		if self.api_key:
			self.headers[ 'X-App-Token' ] = self.api_key
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'api_key',
				'base_url',
				'metadata_url',
				'domain',
				'dataset_id',
				'mode',
				'select_clause',
				'where_clause',
				'order_clause',
				'group_clause',
				'limit_value',
				'offset_value',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'normalize_domain',
				'normalize_dataset_id',
				'validate_limit',
				'validate_offset',
				'fetch_metadata',
				'fetch_rows',
				'fetch',
				'create_schema'
		]
	
	def normalize_domain( self, domain: str ) -> str:
		"""Normalize domain.
		
		Purpose:
			Converts domain into the canonical format expected by the HealthData request workflow.
			The method standardizes caller input before it is used in endpoint paths, query
			parameters, filters, or response processing.
		
		Args:
			domain (str): domain value used by the normalize domain operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'domain', domain )
			
			value = str( domain ).strip( )
			value = value.replace( 'https://', '' ).replace( 'http://', '' ).strip( '/' )
			
			if not value or '.' not in value:
				raise ValueError( 'domain must be a valid HealthData.gov portal domain.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'HealthData'
			exception.method = 'normalize_domain( self, *args, **kwargs ) -> str'
			raise exception
	
	def normalize_dataset_id( self, dataset_id: str ) -> str:
		"""Normalize dataset id.
		
		Purpose:
			Converts dataset id into the canonical format expected by the HealthData request
			workflow. The method standardizes caller input before it is used in endpoint paths,
			query parameters, filters, or response processing.
		
		Args:
			dataset_id (str): dataset ID value used by the normalize dataset id operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'dataset_id', dataset_id )
			
			value = str( dataset_id ).strip( )
			value = value.replace( '.json', '' ).strip( '/' )
			
			if not value:
				raise ValueError( 'dataset_id cannot be empty.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'HealthData'
			exception.method = 'normalize_dataset_id( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_limit( self, limit: int ) -> int:
		"""Validate limit.
		
		Purpose:
			Validates and normalizes limit before it is used in HealthData.gov Socrata metadata and
			rows. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			limit (int): limit value used by the validate limit operation.
		
		Returns:
			int: Validated limit value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'limit', limit )
			
			value = int( limit )
			if value < 1 or value > 50000:
				raise ValueError( 'limit must be between 1 and 50000.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'HealthData'
			exception.method = 'validate_limit( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_offset( self, offset: int ) -> int:
		"""Validate offset.
		
		Purpose:
			Validates and normalizes offset before it is used in HealthData.gov Socrata metadata and
			rows. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			offset (int): offset value used by the validate offset operation.
		
		Returns:
			int: Validated offset value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if offset is None:
				raise ValueError( 'offset cannot be None.' )
			
			value = int( offset )
			if value < 0:
				raise ValueError( 'offset must be greater than or equal to 0.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'HealthData'
			exception.method = 'validate_offset( self, *args, **kwargs ) -> int'
			raise exception
	
	def fetch_metadata( self, domain: str, dataset_id: str,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch metadata.
		
		Purpose:
			Retrieves metadata using validated arguments and the stored HealthData runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			domain (str): domain value used by the fetch metadata operation.
			dataset_id (str): dataset ID value used by the fetch metadata operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'time', time )
			
			self.mode = 'metadata'
			self.domain = self.normalize_domain( domain )
			self.dataset_id = self.normalize_dataset_id( dataset_id )
			self.timeout = int( time )
			self.url = self.metadata_url.format(
				domain=self.domain,
				dataset=self.dataset_id
			)
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			if self.api_key:
				self.headers[ 'X-App-Token' ] = self.api_key
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			self.payload = self.response.json( )
			self.result = {
					'mode': self.mode,
					'url': self.response.url,
					'params': self.params,
					'data': self.payload,
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'HealthData'
			exception.method = (
					'fetch_metadata( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_rows( self, domain: str, dataset_id: str, select: str = '',
			where: str = '', order: str = '', group: str = '',
			limit: int = 25, offset: int = 0,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch rows.
		
		Purpose:
			Retrieves rows using validated arguments and the stored HealthData runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			domain (str): domain value used by the fetch rows operation.
			dataset_id (str): dataset ID value used by the fetch rows operation.
			select (str): select value used by the fetch rows operation.
			where (str): where value used by the fetch rows operation.
			order (str): order value used by the fetch rows operation.
			group (str): group value used by the fetch rows operation.
			limit (int): limit value used by the fetch rows operation.
			offset (int): offset value used by the fetch rows operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'time', time )
			
			self.mode = 'rows'
			self.domain = self.normalize_domain( domain )
			self.dataset_id = self.normalize_dataset_id( dataset_id )
			self.select_clause = str( select or '' ).strip( )
			self.where_clause = str( where or '' ).strip( )
			self.order_clause = str( order or '' ).strip( )
			self.group_clause = str( group or '' ).strip( )
			self.limit_value = self.validate_limit( limit )
			self.offset_value = self.validate_offset( offset )
			self.timeout = int( time )
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			self.url = self.base_url.format(
				domain=self.domain,
				dataset=self.dataset_id
			)
			self.params = {
					'$limit': self.limit_value,
					'$offset': self.offset_value,
			}
			
			if self.select_clause:
				self.params[ '$select' ] = self.select_clause
			
			if self.where_clause:
				self.params[ '$where' ] = self.where_clause
			
			if self.order_clause:
				self.params[ '$order' ] = self.order_clause
			
			if self.group_clause:
				self.params[ '$group' ] = self.group_clause
			
			if self.api_key:
				self.headers[ 'X-App-Token' ] = self.api_key
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			self.payload = self.response.json( )
			self.result = {
					'mode': self.mode,
					'url': self.response.url,
					'params': self.params,
					'count': len( self.payload ) if isinstance( self.payload, list ) else 0,
					'data': self.payload,
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'HealthData'
			exception.method = (
					'fetch_rows( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'rows', domain: str = 'healthdata.gov',
			dataset_id: str = '', select: str = '', where: str = '',
			order: str = '', group: str = '', limit: int = 25,
			offset: int = 0, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch HealthData.gov Socrata metadata and rows.
		
		Purpose:
			Retrieves HealthData.gov Socrata metadata and rows using validated arguments and the
			stored HealthData runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			domain (str): domain value used by the fetch operation.
			dataset_id (str): dataset ID value used by the fetch operation.
			select (str): select value used by the fetch operation.
			where (str): where value used by the fetch operation.
			order (str): order value used by the fetch operation.
			group (str): group value used by the fetch operation.
			limit (int): limit value used by the fetch operation.
			offset (int): offset value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			self.mode = str( mode or 'rows' ).strip( ).lower( )
			
			if self.mode == 'metadata':
				return self.fetch_metadata(
					domain=domain,
					dataset_id=dataset_id,
					time=time
				)
			
			if self.mode == 'rows':
				return self.fetch_rows(
					domain=domain,
					dataset_id=dataset_id,
					select=select,
					where=where,
					order=order,
					group=group,
					limit=limit,
					offset=offset,
					time=time
				)
			
			raise ValueError( "Unsupported HealthData mode. Use 'metadata' or 'rows'." )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'HealthData'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f"{description.strip( )} This function uses the "
							f"{tool.strip( )} service."
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'HealthData'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class GlobalHealthData( Fetcher ):
	"""Global Health Data fetcher.
	
	Purpose:
		Coordinates WHO global health indicator and Athena data within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		api_key (Optional[str]): API key state retained by the instance.
		base_url (Optional[str]): base URL state retained by the instance.
		athena_base_url (Optional[str]): athena base URL state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		query_path (Optional[str]): query path state retained by the instance.
		fmt (Optional[str]): fmt state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	api_key: Optional[ str ]
	base_url: Optional[ str ]
	athena_base_url: Optional[ str ]
	mode: Optional[ str ]
	query_path: Optional[ str ]
	fmt: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize GlobalHealthData.
		
		Purpose:
			Initializes the GlobalHealthData instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.api_key = cfg.WHO_API_KEY
		self.base_url = 'https://www.who.int/data/gho'
		self.athena_base_url = 'https://ghoapi.azureedge.net/api'
		self.mode = 'indicator_registry'
		self.query_path = ''
		self.fmt = 'json'
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents,
		}
		
		if self.api_key:
			self.headers[ 'X-API-Key' ] = self.api_key
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'api_key',
				'base_url',
				'athena_base_url',
				'mode',
				'query_path',
				'fmt',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'normalize_query_path',
				'fetch_indicator_registry',
				'fetch_athena',
				'fetch',
				'create_schema'
		]
	
	def normalize_query_path( self, query_path: str ) -> str:
		"""Normalize query path.
		
		Purpose:
			Converts query path into the canonical format expected by the GlobalHealthData request
			workflow. The method standardizes caller input before it is used in endpoint paths,
			query parameters, filters, or response processing.
		
		Args:
			query_path (str): query path value used by the normalize query path operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'query_path', query_path )
			
			value = str( query_path ).strip( ).lstrip( '/' )
			
			if not value:
				raise ValueError( "Argument 'query_path' cannot be empty!" )
			
			if value.startswith( 'http://' ) or value.startswith( 'https://' ):
				raise ValueError( 'query_path must be a path segment, not a full URL.' )
			
			if '..' in value:
				raise ValueError( 'query_path cannot contain parent-directory markers.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GlobalHealthData'
			exception.method = 'normalize_query_path( self, *args, **kwargs ) -> str'
			raise exception
	
	def fetch_indicator_registry( self, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch indicator registry.
		
		Purpose:
			Retrieves indicator registry using validated arguments and the stored GlobalHealthData
			runtime configuration. The method assembles request parameters, executes the provider
			call or dispatches to a specialized helper, records response state when applicable, and
			returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'time', time )
			
			self.mode = 'indicator_registry'
			self.timeout = int( time )
			self.url = f'{self.base_url}/indicator-metadata-registry'
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			if self.api_key:
				self.headers[ 'X-API-Key' ] = self.api_key
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			content_type = str( self.response.headers.get( 'Content-Type', '' ) ).lower( )
			
			if 'application/json' in content_type:
				self.payload = self.response.json( )
			else:
				self.payload = {
						'html': self.response.text,
				}
			
			self.result = {
					'mode': self.mode,
					'url': self.response.url,
					'params': self.params,
					'data': self.payload,
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GlobalHealthData'
			exception.method = (
					'fetch_indicator_registry( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_athena( self, query_path: str, fmt: str = 'json',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch athena.
		
		Purpose:
			Retrieves athena using validated arguments and the stored GlobalHealthData runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			query_path (str): query path value used by the fetch athena operation.
			fmt (str): fmt value used by the fetch athena operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'query_path', query_path )
			throw_if( 'time', time )
			
			self.mode = 'athena'
			self.query_path = self.normalize_query_path( query_path )
			self.fmt = str( fmt or 'json' ).strip( )
			self.timeout = int( time )
			self.url = f'{self.athena_base_url}/{self.query_path}'
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			if self.fmt:
				self.params[ '$format' ] = self.fmt
			
			if self.api_key:
				self.headers[ 'X-API-Key' ] = self.api_key
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			content_type = str( self.response.headers.get( 'Content-Type', '' ) ).lower( )
			
			if 'application/json' in content_type:
				self.payload = self.response.json( )
			else:
				self.payload = {
						'text': self.response.text,
				}
			
			self.result = {
					'mode': self.mode,
					'url': self.response.url,
					'params': self.params,
					'data': self.payload,
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GlobalHealthData'
			exception.method = (
					'fetch_athena( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'indicator_registry', query_path: str = '',
			fmt: str = 'json', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch WHO global health indicator and Athena data.
		
		Purpose:
			Retrieves WHO global health indicator and Athena data using validated arguments and the
			stored GlobalHealthData runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			query_path (str): query path value used by the fetch operation.
			fmt (str): fmt value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			self.mode = str( mode or 'indicator_registry' ).strip( ).lower( )
			
			if self.mode == 'indicator_registry':
				return self.fetch_indicator_registry(
					time=time
				)
			
			if self.mode == 'athena':
				return self.fetch_athena(
					query_path=query_path,
					fmt=fmt,
					time=time
				)
			
			raise ValueError(
				"Unsupported WHO Global Health mode. Use 'indicator_registry' or "
				"'athena'."
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GlobalHealthData'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f"{description.strip( )} This function uses the "
							f"{tool.strip( )} service."
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'GlobalHealthData'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class UnitedNations( Fetcher ):
	"""United Nations fetcher.
	
	Purpose:
		Coordinates United Nations SDMX dataset and query retrieval within Fonky. The class
		stores provider configuration, request parameters, response payloads, and normalized
		result state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		catalog_url (Optional[str]): catalog URL state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		query_path (Optional[str]): query path state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	catalog_url: Optional[ str ]
	mode: Optional[ str ]
	query_path: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize UnitedNations.
		
		Purpose:
			Initializes the UnitedNations instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://data.un.org/Handlers/DownloadHandler.ashx'
		self.catalog_url = 'https://data.un.org/Handlers/DownloadHandler.ashx'
		self.mode = 'datasets'
		self.query_path = ''
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json, text/json, text/csv, text/xml, */*',
				'User-Agent': self.agents
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'catalog_url',
				'mode',
				'query_path',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'normalize_query_path',
				'fetch_datasets',
				'fetch_sdmx_query',
				'fetch',
				'create_schema'
		]
	
	def normalize_query_path( self, query_path: str ) -> str:
		"""Normalize query path.
		
		Purpose:
			Converts query path into the canonical format expected by the UnitedNations request
			workflow. The method standardizes caller input before it is used in endpoint paths,
			query parameters, filters, or response processing.
		
		Args:
			query_path (str): query path value used by the normalize query path operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'query_path', query_path )
			
			value = str( query_path ).strip( ).lstrip( '/' )
			
			if not value:
				raise ValueError( 'query_path cannot be empty.' )
			
			if value.startswith( 'http://' ) or value.startswith( 'https://' ):
				raise ValueError( 'query_path must be a path segment, not a full URL.' )
			
			if '..' in value:
				raise ValueError( 'query_path cannot contain parent-directory markers.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UnitedNations'
			exception.method = 'normalize_query_path( self, *args, **kwargs ) -> str'
			raise exception
	
	def fetch_datasets( self, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch datasets.
		
		Purpose:
			Retrieves datasets using validated arguments and the stored UnitedNations runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'time', time )
			
			self.mode = 'datasets'
			self.timeout = int( time )
			self.url = self.catalog_url
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			content_type = str( self.response.headers.get( 'Content-Type', '' ) ).lower( )
			
			if 'application/json' in content_type or 'text/json' in content_type:
				self.payload = self.response.json( )
			else:
				self.payload = {
						'text': self.response.text
				}
			
			self.result = {
					'mode': self.mode,
					'url': self.response.url,
					'params': self.params,
					'data': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UnitedNations'
			exception.method = (
					'fetch_datasets( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_sdmx_query( self, query_path: str,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch sdmx query.
		
		Purpose:
			Retrieves sdmx query using validated arguments and the stored UnitedNations runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			query_path (str): query path value used by the fetch sdmx query operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'query_path', query_path )
			throw_if( 'time', time )
			
			self.mode = 'sdmx_query'
			self.query_path = self.normalize_query_path( query_path )
			self.timeout = int( time )
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			self.url = f'{self.base_url}/{self.query_path}'
			self.params = { }
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			content_type = str( self.response.headers.get( 'Content-Type', '' ) ).lower( )
			
			if 'application/json' in content_type or 'text/json' in content_type:
				self.payload = self.response.json( )
			else:
				self.payload = {
						'text': self.response.text
				}
			
			self.result = {
					'mode': self.mode,
					'url': self.response.url,
					'params': self.params,
					'data': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UnitedNations'
			exception.method = (
					'fetch_sdmx_query( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'datasets', query_path: str = '',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch United Nations SDMX dataset and query retrieval.
		
		Purpose:
			Retrieves United Nations SDMX dataset and query retrieval using validated arguments and
			the stored UnitedNations runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			query_path (str): query path value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			self.mode = str( mode or 'datasets' ).strip( ).lower( )
			
			if self.mode == 'datasets':
				return self.fetch_datasets(
					time=time
				)
			
			if self.mode == 'sdmx_query':
				return self.fetch_sdmx_query(
					query_path=query_path,
					time=time
				)
			
			raise ValueError( "Unsupported United Nations mode. Use 'datasets' or 'sdmx_query'." )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UnitedNations'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f"{description.strip( )} This function uses the "
							f"{tool.strip( )} service."
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UnitedNations'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class WorldPopulation( Fetcher ):
	"""World Population fetcher.
	
	Purpose:
		Coordinates WorldPop catalog and raster metadata retrieval within Fonky. The class
		stores provider configuration, request parameters, response payloads, and normalized
		result state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		stac_url (Optional[str]): stac URL state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		query_text (Optional[str]): query text state retained by the instance.
		asset_path (Optional[str]): asset path state retained by the instance.
		page (Optional[int]): page state retained by the instance.
		page_size (Optional[int]): page size state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	stac_url: Optional[ str ]
	mode: Optional[ str ]
	query_text: Optional[ str ]
	asset_path: Optional[ str ]
	page: Optional[ int ]
	page_size: Optional[ int ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize WorldPopulation.
		
		Purpose:
			Initializes the WorldPopulation instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://www.worldpop.org/rest'
		self.stac_url = 'https://worldpop.github.io/worldpop-stac'
		self.mode = 'catalog'
		self.query_text = ''
		self.asset_path = ''
		self.page = 1
		self.page_size = 25
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json, text/html, text/plain, */*',
				'User-Agent': self.agents
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'stac_url',
				'mode',
				'query_text',
				'asset_path',
				'page',
				'page_size',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'normalize_asset_path',
				'validate_page',
				'validate_page_size',
				'fetch_catalog',
				'search_catalog',
				'fetch_raster_metadata',
				'fetch',
				'create_schema'
		]
	
	def normalize_asset_path( self, asset_path: str ) -> str:
		"""Normalize asset path.
		
		Purpose:
			Converts asset path into the canonical format expected by the WorldPopulation request
			workflow. The method standardizes caller input before it is used in endpoint paths,
			query parameters, filters, or response processing.
		
		Args:
			asset_path (str): asset path value used by the normalize asset path operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'asset_path', asset_path )
			
			value = str( asset_path ).strip( ).lstrip( '/' )
			
			if not value:
				raise ValueError( "Argument 'asset_path' cannot be empty!" )
			
			if value.startswith( 'http://' ) or value.startswith( 'https://' ):
				raise ValueError( 'asset_path must be a path segment, not a full URL.' )
			
			if '..' in value:
				raise ValueError( 'asset_path cannot contain parent-directory markers.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'WorldPopulation'
			exception.method = 'normalize_asset_path( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_page( self, page: int ) -> int:
		"""Validate page.
		
		Purpose:
			Validates and normalizes page before it is used in WorldPop catalog and raster metadata
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			page (int): page value used by the validate page operation.
		
		Returns:
			int: Validated page value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'page', page )
			
			value = int( page )
			if value < 1:
				raise ValueError( 'page must be greater than or equal to 1.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'WorldPopulation'
			exception.method = 'validate_page( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_page_size( self, page_size: int ) -> int:
		"""Validate page size.
		
		Purpose:
			Validates and normalizes page size before it is used in WorldPop catalog and raster
			metadata retrieval. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			page_size (int): page size value used by the validate page size operation.
		
		Returns:
			int: Validated page size value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'page_size', page_size )
			
			value = int( page_size )
			if value < 1 or value > 500:
				raise ValueError( 'page_size must be between 1 and 500.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'WorldPopulation'
			exception.method = 'validate_page_size( self, *args, **kwargs ) -> int'
			raise exception
	
	def fetch_catalog( self, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch catalog.
		
		Purpose:
			Retrieves catalog using validated arguments and the stored WorldPopulation runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'time', time )
			
			self.mode = 'catalog'
			self.timeout = int( time )
			self.url = self.base_url
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			content_type = str( self.response.headers.get( 'Content-Type', '' ) ).lower( )
			
			if 'application/json' in content_type:
				self.payload = self.response.json( )
			else:
				self.payload = {
						'html': self.response.text
				}
			
			self.result = {
					'mode': self.mode,
					'url': self.response.url,
					'params': self.params,
					'data': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'WorldPopulation'
			exception.method = (
					'fetch_catalog( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def search_catalog( self, query: str = '', page: int = 1, page_size: int = 25,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Search catalog.
		
		Purpose:
			Performs the search catalog operation for WorldPop catalog and raster metadata
			retrieval. The method uses the class runtime state and supplied arguments to prepare,
			transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			query (str): Search text, lookup value, or provider query submitted by the caller.
			page (int): page value used by the search catalog operation.
			page_size (int): page size value used by the search catalog operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'query', query )
			throw_if( 'time', time )
			
			self.mode = 'search'
			self.query_text = str( query or '' ).strip( )
			self.page = self.validate_page( page )
			self.page_size = self.validate_page_size( page_size )
			self.timeout = int( time )
			self.url = f'{self.base_url}/search'
			self.params = {
					'q': self.query_text,
					'page': self.page,
					'page_size': self.page_size
			}
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			content_type = str( self.response.headers.get( 'Content-Type', '' ) ).lower( )
			
			if 'application/json' in content_type:
				self.payload = self.response.json( )
			else:
				self.payload = {
						'text': self.response.text
				}
			
			self.result = {
					'mode': self.mode,
					'url': self.response.url,
					'params': self.params,
					'data': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'WorldPopulation'
			exception.method = (
					'search_catalog( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_raster_metadata( self, asset_path: str,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch raster metadata.
		
		Purpose:
			Retrieves raster metadata using validated arguments and the stored WorldPopulation
			runtime configuration. The method assembles request parameters, executes the provider
			call or dispatches to a specialized helper, records response state when applicable, and
			returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			asset_path (str): asset path value used by the fetch raster metadata operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'asset_path', asset_path )
			throw_if( 'time', time )
			
			self.mode = 'raster_metadata'
			self.asset_path = self.normalize_asset_path( asset_path )
			self.timeout = int( time )
			self.url = f'{self.base_url}/{self.asset_path}'
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			content_type = str( self.response.headers.get( 'Content-Type', '' ) ).lower( )
			
			if 'application/json' in content_type:
				self.payload = self.response.json( )
			else:
				self.payload = {
						'text': self.response.text
				}
			
			self.result = {
					'mode': self.mode,
					'url': self.response.url,
					'params': self.params,
					'data': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'WorldPopulation'
			exception.method = (
					'fetch_raster_metadata( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'catalog', query: str = '',
			asset_path: str = '', page: int = 1, page_size: int = 25,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch WorldPop catalog and raster metadata retrieval.
		
		Purpose:
			Retrieves WorldPop catalog and raster metadata retrieval using validated arguments and
			the stored WorldPopulation runtime configuration. The method assembles request
			parameters, executes the provider call or dispatches to a specialized helper, records
			response state when applicable, and returns a normalized payload for downstream analysis
			or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			query (str): Search text, lookup value, or provider query submitted by the caller.
			asset_path (str): asset path value used by the fetch operation.
			page (int): page value used by the fetch operation.
			page_size (int): page size value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			self.mode = str( mode or 'catalog' ).strip( ).lower( )
			
			if self.mode == 'catalog':
				return self.fetch_catalog(
					time=time
				)
			
			if self.mode == 'search':
				return self.search_catalog(
					query=query,
					page=page,
					page_size=page_size,
					time=time
				)
			
			if self.mode == 'raster_metadata':
				return self.fetch_raster_metadata(
					asset_path=asset_path,
					time=time
				)
			
			raise ValueError(
				"Unsupported World Population mode. Use 'catalog', 'search', "
				"or 'raster_metadata'."
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'WorldPopulation'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f"{description.strip( )} This function uses the "
							f"{tool.strip( )} service."
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'WorldPopulation'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class Wonder( Fetcher ):
	"""Wonder fetcher.
	
	Purpose:
		Coordinates CDC WONDER template and query submission within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		dataset_id (Optional[str]): dataset ID state retained by the instance.
		request_xml (Optional[str]): request XML state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	mode: Optional[ str ]
	dataset_id: Optional[ str ]
	request_xml: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize Wonder.
		
		Purpose:
			Initializes the Wonder instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://wonder.cdc.gov/controller/datarequest'
		self.mode = 'metadata_template'
		self.dataset_id = 'D76'
		self.request_xml = ''
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/xml, text/xml, text/plain',
				'Content-Type': 'application/x-www-form-urlencoded',
				'User-Agent': self.agents,
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'mode',
				'dataset_id',
				'request_xml',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'normalize_dataset_id',
				'build_template',
				'fetch_template',
				'submit_query',
				'fetch',
				'create_schema'
		]
	
	def normalize_dataset_id( self, dataset_id: str ) -> str:
		"""Normalize dataset id.
		
		Purpose:
			Converts dataset id into the canonical format expected by the Wonder request workflow.
			The method standardizes caller input before it is used in endpoint paths, query
			parameters, filters, or response processing.
		
		Args:
			dataset_id (str): dataset ID value used by the normalize dataset id operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'dataset_id', dataset_id )
			
			value = str( dataset_id ).strip( ).upper( )
			
			if not re.fullmatch( r'D\d{1,4}', value ):
				raise ValueError(
					'CDC WONDER Dataset ID must use the format D followed by digits, '
					'such as D76.'
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Wonder'
			exception.method = 'normalize_dataset_id( self, *args, **kwargs ) -> str'
			raise exception
	
	def build_template( self, dataset_id: str = 'D76' ) -> str:
		"""Build template.
		
		Purpose:
			Constructs template from validated inputs and stored runtime configuration. The method
			centralizes URL, parameter, or payload assembly so fetch operations can issue provider
			requests using a predictable structure.
		
		Args:
			dataset_id (str): dataset ID value used by the build template operation.
		
		Returns:
			str: Constructed URL, query, payload, or request structure.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.dataset_id = self.normalize_dataset_id( dataset_id )
			self.request_xml = (
					f'<request>\n'
					f'  <request-parameters>\n'
					f'    <parameter>\n'
					f'      <name>accept_datause_restrictions</name>\n'
					f'      <value>true</value>\n'
					f'    </parameter>\n'
					f'    <parameter>\n'
					f'      <name>B_1</name>\n'
					f'      <value>{self.dataset_id}.V1</value>\n'
					f'    </parameter>\n'
					f'    <parameter>\n'
					f'      <name>M_1</name>\n'
					f'      <value>{self.dataset_id}.M1</value>\n'
					f'    </parameter>\n'
					f'    <parameter>\n'
					f'      <name>O_show_totals</name>\n'
					f'      <value>true</value>\n'
					f'    </parameter>\n'
					f'  </request-parameters>\n'
					f'</request>'
			)
			
			return self.request_xml
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Wonder'
			exception.method = 'build_template( self, *args, **kwargs ) -> str'
			raise exception
	
	def fetch_template( self, dataset_id: str = 'D76' ) -> Dict[ str, Any ] | None:
		"""Fetch template.
		
		Purpose:
			Retrieves template using validated arguments and the stored Wonder runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			dataset_id (str): dataset ID value used by the fetch template operation.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'metadata_template'
			self.dataset_id = self.normalize_dataset_id( dataset_id )
			self.url = f'{self.base_url}/{self.dataset_id}'
			self.params = {
					'dataset_id': self.dataset_id
			}
			self.payload = {
					'dataset_id': self.dataset_id,
					'request_xml': self.build_template( dataset_id=self.dataset_id ),
					'notes': (
							'CDC WONDER expects POST requests to '
							'https://wonder.cdc.gov/controller/datarequest/[database ID] '
							'with a request_xml parameter and acceptance of data-use restrictions.'
					),
			}
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'data': self.payload,
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Wonder'
			exception.method = (
					'fetch_template( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def submit_query( self, dataset_id: str, request_xml: str,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Submit query.
		
		Purpose:
			Performs the submit query operation for CDC WONDER template and query submission. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			dataset_id (str): dataset ID value used by the submit query operation.
			request_xml (str): request XML value used by the submit query operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'dataset_id', dataset_id )
			throw_if( 'request_xml', request_xml )
			throw_if( 'time', time )
			
			self.mode = 'query_xml'
			self.dataset_id = self.normalize_dataset_id( dataset_id )
			self.request_xml = str( request_xml ).strip( )
			self.timeout = int( time )
			self.url = f'{self.base_url}/{self.dataset_id}'
			self.params = {
					'request_xml': self.request_xml,
					'accept_datause_restrictions': 'true',
			}
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			self.response = requests.post(
				url=self.url,
				data=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			self.payload = {
					'xml': self.response.text,
			}
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': {
							'dataset_id': self.dataset_id,
							'accept_datause_restrictions': 'true',
					},
					'data': self.payload,
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Wonder'
			exception.method = (
					'submit_query( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'metadata_template', dataset_id: str = 'D76',
			request_xml: str = '', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch CDC WONDER template and query submission.
		
		Purpose:
			Retrieves CDC WONDER template and query submission using validated arguments and the
			stored Wonder runtime configuration. The method assembles request parameters, executes
			the provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			dataset_id (str): dataset ID value used by the fetch operation.
			request_xml (str): request XML value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			self.mode = str( mode or 'metadata_template' ).strip( ).lower( )
			
			if self.mode == 'metadata_template':
				return self.fetch_template(
					dataset_id=dataset_id
				)
			
			if self.mode == 'query_xml':
				return self.submit_query(
					dataset_id=dataset_id,
					request_xml=request_xml,
					time=time
				)
			
			raise ValueError(
				"Unsupported CDC WONDER mode. Use 'metadata_template' or 'query_xml'."
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Wonder'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if not isinstance( parameters, dict ):
				raise ValueError(
					'parameters must be a dict of param_name -> schema definition.'
				)
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Wonder'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class USGSEarthquakes( Fetcher ):
	"""U S G S Earthquakes fetcher.
	
	Purpose:
		Coordinates USGS earthquake feed and query retrieval within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		feed_url (Optional[str]): feed URL state retained by the instance.
		search_url (Optional[str]): search URL state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		feed (Optional[str]): feed state retained by the instance.
		start_date (Optional[str]): start date state retained by the instance.
		end_date (Optional[str]): end date state retained by the instance.
		min_magnitude (Optional[float]): min magnitude state retained by the instance.
		max_magnitude (Optional[float]): max magnitude state retained by the instance.
		limit (Optional[int]): limit state retained by the instance.
		order_by (Optional[str]): order by state retained by the instance.
		event_type (Optional[str]): event type state retained by the instance.
		latitude (Optional[float]): latitude state retained by the instance.
		longitude (Optional[float]): longitude state retained by the instance.
		max_radius_km (Optional[float]): max radius km state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Dict[str, Any]]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	feed_url: Optional[ str ]
	search_url: Optional[ str ]
	mode: Optional[ str ]
	feed: Optional[ str ]
	start_date: Optional[ str ]
	end_date: Optional[ str ]
	min_magnitude: Optional[ float ]
	max_magnitude: Optional[ float ]
	limit: Optional[ int ]
	order_by: Optional[ str ]
	event_type: Optional[ str ]
	latitude: Optional[ float ]
	longitude: Optional[ float ]
	max_radius_km: Optional[ float ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Dict[ str, Any ] ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize USGSEarthquakes.
		
		Purpose:
			Initializes the USGSEarthquakes instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.feed_url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary'
		self.search_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
		self.mode = 'feed'
		self.feed = 'all_day.geojson'
		self.start_date = ''
		self.end_date = ''
		self.min_magnitude = None
		self.max_magnitude = None
		self.limit = 25
		self.order_by = 'time'
		self.event_type = 'earthquake'
		self.latitude = None
		self.longitude = None
		self.max_radius_km = None
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/geo+json, application/json',
				'User-Agent': self.agents
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'feed_url',
				'search_url',
				'mode',
				'feed',
				'start_date',
				'end_date',
				'min_magnitude',
				'max_magnitude',
				'limit',
				'order_by',
				'event_type',
				'latitude',
				'longitude',
				'max_radius_km',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'validate_feed',
				'validate_limit',
				'validate_magnitude',
				'validate_order_by',
				'validate_latitude',
				'validate_longitude',
				'validate_radius',
				'to_iso_date',
				'epoch_millis_to_iso',
				'shape_feature_rows',
				'summarize_features',
				'package_response',
				'fetch_feed',
				'fetch_search',
				'fetch',
				'create_schema'
		]
	
	def validate_feed( self, feed: str ) -> str:
		"""Validate feed.
		
		Purpose:
			Validates and normalizes feed before it is used in USGS earthquake feed and query
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			feed (str): feed value used by the validate feed operation.
		
		Returns:
			str: Validated feed value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'feed', feed )
			
			value = str( feed ).strip( )
			allowed = {
					'all_hour.geojson',
					'all_day.geojson',
					'all_week.geojson',
					'all_month.geojson',
					'significant_hour.geojson',
					'significant_day.geojson',
					'significant_week.geojson',
					'significant_month.geojson',
					'4.5_hour.geojson',
					'4.5_day.geojson',
					'4.5_week.geojson',
					'4.5_month.geojson',
					'2.5_hour.geojson',
					'2.5_day.geojson',
					'2.5_week.geojson',
					'2.5_month.geojson',
					'1.0_hour.geojson',
					'1.0_day.geojson',
					'1.0_week.geojson',
					'1.0_month.geojson'
			}
			
			if value not in allowed:
				raise ValueError( f'Unsupported USGS earthquake feed: {value}' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = 'validate_feed( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_limit( self, limit: int ) -> int:
		"""Validate limit.
		
		Purpose:
			Validates and normalizes limit before it is used in USGS earthquake feed and query
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			limit (int): limit value used by the validate limit operation.
		
		Returns:
			int: Validated limit value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'limit', limit )
			
			value = int( limit )
			if value < 1 or value > 20000:
				raise ValueError( 'limit must be between 1 and 20000.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = 'validate_limit( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_magnitude( self, name: str, value: float ) -> float:
		"""Validate magnitude.
		
		Purpose:
			Validates and normalizes magnitude before it is used in USGS earthquake feed and query
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			name (str): name value used by the validate magnitude operation.
			value (float): value value used by the validate magnitude operation.
		
		Returns:
			float: Validated magnitude value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			throw_if( name, value )
			
			number = float( value )
			if number < 0.0 or number > 10.0:
				raise ValueError( f'{name} must be between 0.0 and 10.0.' )
			
			return number
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = 'validate_magnitude( self, *args, **kwargs ) -> float'
			raise exception
	
	def validate_order_by( self, order_by: str ) -> str:
		"""Validate order by.
		
		Purpose:
			Validates and normalizes order by before it is used in USGS earthquake feed and query
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			order_by (str): order by value used by the validate order by operation.
		
		Returns:
			str: Validated order by value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'order_by', order_by )
			
			value = str( order_by ).strip( ).lower( )
			allowed = {
					'time',
					'time-asc',
					'magnitude',
					'magnitude-asc'
			}
			
			if value not in allowed:
				raise ValueError(
					"order_by must be 'time', 'time-asc', 'magnitude', or "
					"'magnitude-asc'."
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = 'validate_order_by( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_latitude( self, latitude: float ) -> float:
		"""Validate latitude.
		
		Purpose:
			Validates and normalizes latitude before it is used in USGS earthquake feed and query
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			latitude (float): latitude value used by the validate latitude operation.
		
		Returns:
			float: Validated latitude value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'latitude', latitude )
			
			value = float( latitude )
			if value < -90.0 or value > 90.0:
				raise ValueError( 'latitude must be between -90 and 90.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = 'validate_latitude( self, *args, **kwargs ) -> float'
			raise exception
	
	def validate_longitude( self, longitude: float ) -> float:
		"""Validate longitude.
		
		Purpose:
			Validates and normalizes longitude before it is used in USGS earthquake feed and query
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			longitude (float): longitude value used by the validate longitude operation.
		
		Returns:
			float: Validated longitude value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'longitude', longitude )
			
			value = float( longitude )
			if value < -180.0 or value > 180.0:
				raise ValueError( 'longitude must be between -180 and 180.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = 'validate_longitude( self, *args, **kwargs ) -> float'
			raise exception
	
	def validate_radius( self, radius: float ) -> float:
		"""Validate radius.
		
		Purpose:
			Validates and normalizes radius before it is used in USGS earthquake feed and query
			retrieval. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			radius (float): radius value used by the validate radius operation.
		
		Returns:
			float: Validated radius value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'max_radius_km', radius )
			
			value = float( radius )
			if value < 0.0 or value > 20001.6:
				raise ValueError( 'max_radius_km must be between 0.0 and 20001.6.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = 'validate_radius( self, *args, **kwargs ) -> float'
			raise exception
	
	def to_iso_date( self, value: str ) -> str:
		"""Convert to iso date.
		
		Purpose:
			Performs the to iso date operation for USGS earthquake feed and query retrieval. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			value (str): value value used by the to iso date operation.
		
		Returns:
			str: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'date', value )
			return str( value ).strip( )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = 'to_iso_date( self, *args, **kwargs ) -> str'
			raise exception
	
	def epoch_millis_to_iso( self, value: Any ) -> str:
		"""Epoch millis to iso.
		
		Purpose:
			Performs the epoch millis to iso operation for USGS earthquake feed and query retrieval.
			The method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			value (object): value value used by the epoch millis to iso operation.
		
		Returns:
			str: Result produced by the operation."""
		try:
			if value is None:
				return ''
			
			return dt.datetime.fromtimestamp(
				float( value ) / 1000.0,
				tz=dt.timezone.utc
			).isoformat( )
		
		except Exception:
			return ''
	
	def shape_feature_rows( self, features: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape feature rows.
		
		Purpose:
			Transforms raw provider records into feature rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			features (List[Dict[str, Any]]): features value used by the shape feature rows
				operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for feature in features or [ ]:
				properties = feature.get( 'properties', { } ) or { }
				geometry = feature.get( 'geometry', { } ) or { }
				coordinates = geometry.get( 'coordinates', [ ] ) or [ ]
				
				longitude = coordinates[ 0 ] if len( coordinates ) > 0 else None
				latitude = coordinates[ 1 ] if len( coordinates ) > 1 else None
				depth = coordinates[ 2 ] if len( coordinates ) > 2 else None
				event_time = self.epoch_millis_to_iso( properties.get( 'time' ) )
				updated_time = self.epoch_millis_to_iso( properties.get( 'updated' ) )
				
				rows.append(
					{
							'Id': feature.get( 'id', '' ),
							'Magnitude': properties.get( 'mag', None ),
							'Place': properties.get( 'place', '' ),
							'Time': event_time,
							'Updated': updated_time,
							'Alert': properties.get( 'alert', '' ),
							'Status': properties.get( 'status', '' ),
							'Tsunami': properties.get( 'tsunami', None ),
							'Felt Reports': properties.get( 'felt', None ),
							'Depth (km)': depth,
							'Latitude': latitude,
							'Longitude': longitude,
							'Event Type': properties.get( 'type', '' ),
							'URL': properties.get( 'url', '' )
					}
				)
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = (
					'shape_feature_rows( self, *args, **kwargs ) -> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def summarize_features( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Summarize features.
		
		Purpose:
			Performs the summarize features operation for USGS earthquake feed and query retrieval.
			The method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the summarize features operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			count = len( rows or [ ] )
			max_magnitude = None
			strongest_place = ''
			most_recent = ''
			
			for row in rows or [ ]:
				magnitude = row.get( 'Magnitude', None )
				
				if magnitude is not None:
					try:
						if max_magnitude is None or float( magnitude ) > float( max_magnitude ):
							max_magnitude = float( magnitude )
							strongest_place = str( row.get( 'Place', '' ) )
					except Exception:
						pass
				
				if not most_recent and row.get( 'Time', '' ):
					most_recent = str( row.get( 'Time', '' ) )
			
			return {
					'count': count,
					'max_magnitude': max_magnitude,
					'strongest_place': strongest_place,
					'most_recent': most_recent
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = (
					'summarize_features( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def package_response( self ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			metadata = self.payload.get( 'metadata', { } ) or { }
			features = self.payload.get( 'features', [ ] ) or [ ]
			rows = self.shape_feature_rows( features )
			
			self.result = {
					'mode': self.mode,
					'feed': self.feed if self.mode == 'feed' else '',
					'url': self.url,
					'params': self.params,
					'title': metadata.get( 'title', '' ),
					'generated': metadata.get( 'generated', None ),
					'count': metadata.get( 'count', len( rows ) ),
					'bbox': self.payload.get( 'bbox', [ ] ),
					'summary': self.summarize_features( rows ),
					'rows': rows,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = 'package_response( self ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_feed( self, feed: str = 'all_day.geojson',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch feed.
		
		Purpose:
			Retrieves feed using validated arguments and the stored USGSEarthquakes runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			feed (str): feed value used by the fetch feed operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'time', time )
			
			self.mode = 'feed'
			self.feed = self.validate_feed( feed )
			self.timeout = int( time )
			self.params = { }
			self.url = f'{self.feed_url}/{self.feed}'
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			self.response = requests.get(
				url=self.url,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			self.payload = self.response.json( ) or { }
			
			return self.package_response( )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = (
					'fetch_feed( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_search( self, start_date: str, end_date: str,
			min_magnitude: float = 1.0, max_magnitude: float = 10.0,
			limit: int = 25, order_by: str = 'time',
			event_type: str = 'earthquake', latitude: float | None = None,
			longitude: float | None = None,
			max_radius_km: float | None = None,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch search.
		
		Purpose:
			Retrieves search using validated arguments and the stored USGSEarthquakes runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			start_date (str): start date value used by the fetch search operation.
			end_date (str): end date value used by the fetch search operation.
			min_magnitude (float): min magnitude value used by the fetch search operation.
			max_magnitude (float): max magnitude value used by the fetch search operation.
			limit (int): limit value used by the fetch search operation.
			order_by (str): order by value used by the fetch search operation.
			event_type (str): event type value used by the fetch search operation.
			latitude (float | None): latitude value used by the fetch search operation.
			longitude (float | None): longitude value used by the fetch search operation.
			max_radius_km (float | None): max radius km value used by the fetch search operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'start_date', start_date )
			throw_if( 'end_date', end_date )
			throw_if( 'event_type', event_type )
			throw_if( 'time', time )
			
			self.mode = 'search'
			self.feed = ''
			self.start_date = self.to_iso_date( start_date )
			self.end_date = self.to_iso_date( end_date )
			self.min_magnitude = self.validate_magnitude( 'min_magnitude', min_magnitude )
			self.max_magnitude = self.validate_magnitude( 'max_magnitude', max_magnitude )
			self.limit = self.validate_limit( limit )
			self.order_by = self.validate_order_by( order_by )
			self.event_type = str( event_type ).strip( )
			self.timeout = int( time )
			self.url = self.search_url
			
			if self.min_magnitude > self.max_magnitude:
				raise ValueError( 'min_magnitude must be less than or equal to max_magnitude.' )
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			self.params = {
					'format': 'geojson',
					'starttime': self.start_date,
					'endtime': self.end_date,
					'minmagnitude': self.min_magnitude,
					'maxmagnitude': self.max_magnitude,
					'limit': self.limit,
					'orderby': self.order_by,
					'eventtype': self.event_type
			}
			
			if (latitude is None) != (longitude is None):
				raise ValueError(
					'latitude and longitude must both be supplied for radial search.'
				)
			
			if latitude is not None and longitude is not None:
				self.latitude = self.validate_latitude( latitude )
				self.longitude = self.validate_longitude( longitude )
				self.params[ 'latitude' ] = self.latitude
				self.params[ 'longitude' ] = self.longitude
			
			if max_radius_km is not None:
				if self.latitude is None or self.longitude is None:
					raise ValueError(
						'max_radius_km requires both latitude and longitude.'
					)
				
				self.max_radius_km = self.validate_radius( max_radius_km )
				self.params[ 'maxradiuskm' ] = self.max_radius_km
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			
			self.payload = self.response.json( ) or { }
			
			return self.package_response( )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = (
					'fetch_search( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'feed', feed: str = 'all_day.geojson',
			start_date: str = '', end_date: str = '', min_magnitude: float = 1.0,
			max_magnitude: float = 10.0, limit: int = 25, order_by: str = 'time',
			event_type: str = 'earthquake', latitude: float | None = None,
			longitude: float | None = None, max_radius_km: float | None = None,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch USGS earthquake feed and query retrieval.
		
		Purpose:
			Retrieves USGS earthquake feed and query retrieval using validated arguments and the
			stored USGSEarthquakes runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			feed (str): feed value used by the fetch operation.
			start_date (str): start date value used by the fetch operation.
			end_date (str): end date value used by the fetch operation.
			min_magnitude (float): min magnitude value used by the fetch operation.
			max_magnitude (float): max magnitude value used by the fetch operation.
			limit (int): limit value used by the fetch operation.
			order_by (str): order by value used by the fetch operation.
			event_type (str): event type value used by the fetch operation.
			latitude (float | None): latitude value used by the fetch operation.
			longitude (float | None): longitude value used by the fetch operation.
			max_radius_km (float | None): max radius km value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			self.mode = str( mode or 'feed' ).strip( ).lower( )
			
			if self.mode == 'feed':
				return self.fetch_feed(
					feed=feed,
					time=time
				)
			
			if self.mode == 'search':
				return self.fetch_search(
					start_date=start_date,
					end_date=end_date,
					min_magnitude=min_magnitude,
					max_magnitude=max_magnitude,
					limit=limit,
					order_by=order_by,
					event_type=event_type,
					latitude=latitude,
					longitude=longitude,
					max_radius_km=max_radius_km,
					time=time
				)
			
			raise ValueError( "Unsupported USGS Earthquakes mode. Use 'feed' or 'search'." )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if not isinstance( parameters, dict ):
				raise ValueError(
					'parameters must be a dict of param_name -> schema definition.'
				)
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSEarthquakes'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class USGSWaterData( Fetcher ):
	"""U S G S Water Data fetcher.
	
	Purpose:
		Coordinates USGS water services records within Fonky. The class stores provider
		configuration, request parameters, response payloads, and normalized result state so
		callers can access the service through a consistent fetcher interface.
	
	Attributes:
		api_key (Optional[str]): API key state retained by the instance.
		base_url (Optional[str]): base URL state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		collection (Optional[str]): collection state retained by the instance.
		monitoring_location_id (Optional[str]): monitoring location ID state retained by the
			instance.
		state_code (Optional[str]): state code state retained by the instance.
		county_code (Optional[str]): county code state retained by the instance.
		site_type (Optional[str]): site type state retained by the instance.
		parameter_code (Optional[str]): parameter code state retained by the instance.
		limit (Optional[int]): limit state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	api_key: Optional[ str ]
	base_url: Optional[ str ]
	mode: Optional[ str ]
	collection: Optional[ str ]
	monitoring_location_id: Optional[ str ]
	state_code: Optional[ str ]
	county_code: Optional[ str ]
	site_type: Optional[ str ]
	parameter_code: Optional[ str ]
	limit: Optional[ int ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize USGSWaterData.
		
		Purpose:
			Initializes the USGSWaterData instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.api_key = cfg.USGS_WATERDATA_API_KEY
		self.base_url = 'https://api.waterdata.usgs.gov/ogcapi/v0/collections'
		self.mode = 'monitoring-locations'
		self.collection = None
		self.monitoring_location_id = ''
		self.state_code = ''
		self.county_code = ''
		self.site_type = ''
		self.parameter_code = ''
		self.limit = 25
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents
		}
		
		if self.api_key:
			self.headers[ 'X-API-Key' ] = self.api_key
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'api_key',
				'base_url',
				'mode',
				'collection',
				'monitoring_location_id',
				'state_code',
				'county_code',
				'site_type',
				'parameter_code',
				'limit',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'validate_collection',
				'validate_limit',
				'validate_parameter_code',
				'coalesce_records',
				'shape_monitoring_locations',
				'shape_time_series_metadata',
				'shape_latest_values',
				'summarize_rows',
				'package_response',
				'request',
				'fetch_monitoring_locations',
				'fetch_time_series_metadata',
				'fetch_latest_continuous',
				'fetch_latest_daily',
				'fetch',
				'create_schema'
		]
	
	def validate_collection( self, collection: str ) -> str:
		"""Validate collection.
		
		Purpose:
			Validates and normalizes collection before it is used in USGS water services records.
			The method converts incoming values to the expected representation, enforces visible
			range or format constraints, and returns the checked value for request construction.
		
		Args:
			collection (str): collection value used by the validate collection operation.
		
		Returns:
			str: Validated collection value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'collection', collection )
			
			value = str( collection ).strip( )
			allowed = {
					'monitoring-locations',
					'time-series-metadata',
					'latest-continuous',
					'latest-daily'
			}
			
			if value not in allowed:
				raise ValueError(
					'Unsupported USGS Water Data collection. Use '
					'monitoring-locations, time-series-metadata, latest-continuous, '
					'or latest-daily.'
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = 'validate_collection( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_limit( self, limit: int ) -> int:
		"""Validate limit.
		
		Purpose:
			Validates and normalizes limit before it is used in USGS water services records. The
			method converts incoming values to the expected representation, enforces visible range
			or format constraints, and returns the checked value for request construction.
		
		Args:
			limit (int): limit value used by the validate limit operation.
		
		Returns:
			int: Validated limit value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'limit', limit )
			
			value = int( limit )
			if value < 1 or value > 10000:
				raise ValueError( 'limit must be between 1 and 10000.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = 'validate_limit( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_parameter_code( self, parameter_code: str ) -> str:
		"""Validate parameter code.
		
		Purpose:
			Validates and normalizes parameter code before it is used in USGS water services
			records. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			parameter_code (str): parameter code value used by the validate parameter code
				operation.
		
		Returns:
			str: Validated parameter code value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( parameter_code or '' ).strip( )
			
			if value and not re.fullmatch( r'\d{5}', value ):
				raise ValueError( 'parameter_code must be a 5-digit USGS parameter code.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = 'validate_parameter_code( self, *args, **kwargs ) -> str'
			raise exception
	
	def coalesce_records( self, payload: Any ) -> List[ Dict[ str, Any ] ]:
		"""Coalesce records.
		
		Purpose:
			Performs the coalesce records operation for USGS water services records. The method uses
			the class runtime state and supplied arguments to prepare, transform, dispatch, or
			package data for the broader Fonky fetching workflow.
		
		Args:
			payload (object): payload value used by the coalesce records operation.
		
		Returns:
			List[Dict[str, Any]]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if payload is None:
				return [ ]
			
			if isinstance( payload, list ):
				return [
						item
						for item in payload
						if isinstance( item, dict )
				]
			
			if not isinstance( payload, dict ):
				return [ ]
			
			for key in [
					'features',
					'items',
					'results',
					'data',
					'value',
					'timeSeries',
					'observations'
			]:
				value = payload.get( key, None )
				
				if isinstance( value, list ):
					return [
							item
							for item in value
							if isinstance( item, dict )
					]
			
			return [ payload ]
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = (
					'coalesce_records( self, *args, **kwargs ) -> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_monitoring_locations( self,
			records: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape monitoring locations.
		
		Purpose:
			Transforms raw provider records into monitoring locations structures with consistent
			keys and row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			records (List[Dict[str, Any]]): records value used by the shape monitoring locations
				operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in records or [ ]:
				properties = item.get( 'properties', { } ) or item
				geometry = item.get( 'geometry', { } ) or { }
				coordinates = geometry.get( 'coordinates', [ ] ) or [ ]
				
				longitude = coordinates[ 0 ] if len( coordinates ) > 0 else (
						properties.get( 'longitude', None )
						or properties.get( 'dec_long_va', None )
				)
				latitude = coordinates[ 1 ] if len( coordinates ) > 1 else (
						properties.get( 'latitude', None )
						or properties.get( 'dec_lat_va', None )
				)
				
				rows.append(
					{
							'Monitoring Location ID': (
									properties.get( 'monitoring_location_id', None )
									or properties.get( 'monitoringLocationIdentifier', None )
									or properties.get( 'site_no', '' )
							),
							'Name': (
									properties.get( 'monitoring_location_name', None )
									or properties.get( 'monitoringLocationName', None )
									or properties.get( 'station_nm', '' )
							),
							'Site Type': (
									properties.get( 'site_type', None )
									or properties.get( 'siteType', None )
									or properties.get( 'site_tp_cd', '' )
							),
							'State Code': (
									properties.get( 'state_code', None )
									or properties.get( 'stateCode', None )
									or properties.get( 'state_cd', '' )
							),
							'County Code': (
									properties.get( 'county_code', None )
									or properties.get( 'countyCode', None )
									or properties.get( 'county_cd', '' )
							),
							'Latitude': latitude,
							'Longitude': longitude
					}
				)
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = (
					'shape_monitoring_locations( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_time_series_metadata( self,
			records: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape time series metadata.
		
		Purpose:
			Transforms raw provider records into time series metadata structures with consistent
			keys and row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			records (List[Dict[str, Any]]): records value used by the shape time series metadata
				operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in records or [ ]:
				properties = item.get( 'properties', { } ) or item
				
				rows.append(
					{
							'Monitoring Location ID': (
									properties.get( 'monitoring_location_id', None )
									or properties.get( 'monitoringLocationIdentifier', None )
									or properties.get( 'site_no', '' )
							),
							'Name': (
									properties.get( 'monitoring_location_name', None )
									or properties.get( 'monitoringLocationName', None )
									or properties.get( 'site_name', '' )
							),
							'Parameter Code': (
									properties.get( 'parameter_code', None )
									or properties.get( 'parameterCode', '' )
							),
							'Parameter Name': (
									properties.get( 'parameter_name', None )
									or properties.get( 'parameterName', '' )
							),
							'Statistic ID': (
									properties.get( 'statistic_id', None )
									or properties.get( 'statisticId', '' )
							),
							'Unit': (
									properties.get( 'unit_of_measure', None )
									or properties.get( 'unitOfMeasure', '' )
							),
							'Begin Time': (
									properties.get( 'begin_time', None )
									or properties.get( 'beginTime', '' )
							),
							'End Time': (
									properties.get( 'end_time', None )
									or properties.get( 'endTime', '' )
							)
					}
				)
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = (
					'shape_time_series_metadata( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_latest_values( self,
			records: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape latest values.
		
		Purpose:
			Transforms raw provider records into latest values structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			records (List[Dict[str, Any]]): records value used by the shape latest values operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in records or [ ]:
				properties = item.get( 'properties', { } ) or item
				
				rows.append(
					{
							'Monitoring Location ID': (
									properties.get( 'monitoring_location_id', None )
									or properties.get( 'monitoringLocationIdentifier', None )
									or properties.get( 'site_no', '' )
							),
							'Name': (
									properties.get( 'monitoring_location_name', None )
									or properties.get( 'monitoringLocationName', None )
									or properties.get( 'site_name', '' )
							),
							'Parameter Code': (
									properties.get( 'parameter_code', None )
									or properties.get( 'parameterCode', '' )
							),
							'Parameter Name': (
									properties.get( 'parameter_name', None )
									or properties.get( 'parameterName', '' )
							),
							'Statistic ID': (
									properties.get( 'statistic_id', None )
									or properties.get( 'statisticId', '' )
							),
							'Value': (
									properties.get( 'result_value', None )
									or properties.get( 'value', None )
									or properties.get( 'primary_value', '' )
							),
							'Unit': (
									properties.get( 'unit_of_measure', None )
									or properties.get( 'unitOfMeasure', '' )
							),
							'Time': (
									properties.get( 'time', None )
									or properties.get( 'result_time', None )
									or properties.get( 'resultTime', '' )
							),
							'Approval Status': (
									properties.get( 'approval_status', None )
									or properties.get( 'approvalStatus', '' )
							)
					}
				)
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = (
					'shape_latest_values( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def summarize_rows( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Summarize rows.
		
		Purpose:
			Performs the summarize rows operation for USGS water services records. The method uses
			the class runtime state and supplied arguments to prepare, transform, dispatch, or
			package data for the broader Fonky fetching workflow.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the summarize rows operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			count = len( rows or [ ] )
			first_location = ''
			first_parameter = ''
			first_value = ''
			first_time = ''
			
			if rows:
				first_location = str(
					rows[ 0 ].get( 'Name', '' )
					or rows[ 0 ].get( 'Monitoring Location ID', '' )
					or ''
				)
				first_parameter = str( rows[ 0 ].get( 'Parameter Name', '' ) or '' )
				first_value = str( rows[ 0 ].get( 'Value', '' ) or '' )
				first_time = str(
					rows[ 0 ].get( 'Time', '' )
					or rows[ 0 ].get( 'Begin Time', '' )
					or ''
				)
			
			return {
					'count': count,
					'first_location': first_location,
					'first_parameter': first_parameter,
					'first_value': first_value,
					'first_time': first_time
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = (
					'summarize_rows( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def package_response( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the package response operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'summary': self.summarize_rows( rows ),
					'rows': rows,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = (
					'package_response( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def request( self, collection: str, params: Dict[ str, Any ],
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Request USGS water services records.
		
		Purpose:
			Sends a provider request for USGS water services records after request parameters have
			been validated or prepared by the caller. The method stores request, response, and
			payload state on the instance so subsequent methods can package or inspect the result
			consistently.
		
		Args:
			collection (str): collection value used by the request operation.
			params (Dict[str, Any]): Request or schema parameter dictionary used by the operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'collection', collection )
			throw_if( 'params', params )
			throw_if( 'time', time )
			
			self.collection = self.validate_collection( collection )
			self.timeout = int( time )
			self.url = f'{self.base_url}/{self.collection}/items'
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			for key, value in params.items( ):
				if value is None:
					continue
				
				if isinstance( value, str ) and not value.strip( ):
					continue
				
				self.params[ key ] = value
			
			if self.api_key:
				self.headers[ 'X-API-Key' ] = self.api_key
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.json( ) or { }
			self.result = {
					'url': self.response.url,
					'params': self.params,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = (
					'request( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_monitoring_locations( self, monitoring_location_id: str = '',
			state_code: str = '', county_code: str = '', site_type: str = '',
			limit: int = 25, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch monitoring locations.
		
		Purpose:
			Retrieves monitoring locations using validated arguments and the stored USGSWaterData
			runtime configuration. The method assembles request parameters, executes the provider
			call or dispatches to a specialized helper, records response state when applicable, and
			returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			monitoring_location_id (str): monitoring location ID value used by the fetch monitoring
				locations operation.
			state_code (str): state code value used by the fetch monitoring locations operation.
			county_code (str): county code value used by the fetch monitoring locations operation.
			site_type (str): site type value used by the fetch monitoring locations operation.
			limit (int): limit value used by the fetch monitoring locations operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'limit', limit )
			throw_if( 'time', time )
			
			self.mode = 'monitoring-locations'
			self.monitoring_location_id = str( monitoring_location_id or '' ).strip( )
			self.state_code = str( state_code or '' ).strip( )
			self.county_code = str( county_code or '' ).strip( )
			self.site_type = str( site_type or '' ).strip( )
			self.limit = self.validate_limit( limit )
			self.timeout = int( time )
			
			self.request(
				collection='monitoring-locations',
				params={
						'monitoring_location_id': self.monitoring_location_id,
						'state_code': self.state_code,
						'county_code': self.county_code,
						'site_type': self.site_type,
						'limit': self.limit
				},
				time=self.timeout
			)
			
			records = self.coalesce_records( self.payload )
			rows = self.shape_monitoring_locations( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = (
					'fetch_monitoring_locations( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_time_series_metadata( self, monitoring_location_id: str = '',
			parameter_code: str = '', limit: int = 25,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch time series metadata.
		
		Purpose:
			Retrieves time series metadata using validated arguments and the stored USGSWaterData
			runtime configuration. The method assembles request parameters, executes the provider
			call or dispatches to a specialized helper, records response state when applicable, and
			returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			monitoring_location_id (str): monitoring location ID value used by the fetch time series
				metadata operation.
			parameter_code (str): parameter code value used by the fetch time series metadata
				operation.
			limit (int): limit value used by the fetch time series metadata operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'monitoring_location_id', monitoring_location_id )
			throw_if( 'limit', limit )
			throw_if( 'time', time )
			
			self.mode = 'time-series-metadata'
			self.monitoring_location_id = str( monitoring_location_id ).strip( )
			self.parameter_code = self.validate_parameter_code( parameter_code )
			self.limit = self.validate_limit( limit )
			self.timeout = int( time )
			
			self.request(
				collection='time-series-metadata',
				params={
						'monitoring_location_id': self.monitoring_location_id,
						'parameter_code': self.parameter_code,
						'limit': self.limit
				},
				time=self.timeout
			)
			
			records = self.coalesce_records( self.payload )
			rows = self.shape_time_series_metadata( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = (
					'fetch_time_series_metadata( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_latest_continuous( self, monitoring_location_id: str = '',
			parameter_code: str = '', limit: int = 25,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch latest continuous.
		
		Purpose:
			Retrieves latest continuous using validated arguments and the stored USGSWaterData
			runtime configuration. The method assembles request parameters, executes the provider
			call or dispatches to a specialized helper, records response state when applicable, and
			returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			monitoring_location_id (str): monitoring location ID value used by the fetch latest
				continuous operation.
			parameter_code (str): parameter code value used by the fetch latest continuous
				operation.
			limit (int): limit value used by the fetch latest continuous operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'monitoring_location_id', monitoring_location_id )
			throw_if( 'limit', limit )
			throw_if( 'time', time )
			
			self.mode = 'latest-continuous'
			self.monitoring_location_id = str( monitoring_location_id ).strip( )
			self.parameter_code = self.validate_parameter_code( parameter_code )
			self.limit = self.validate_limit( limit )
			self.timeout = int( time )
			
			self.request(
				collection='latest-continuous',
				params={
						'monitoring_location_id': self.monitoring_location_id,
						'parameter_code': self.parameter_code,
						'limit': self.limit
				},
				time=self.timeout
			)
			
			records = self.coalesce_records( self.payload )
			rows = self.shape_latest_values( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = (
					'fetch_latest_continuous( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_latest_daily( self, monitoring_location_id: str = '',
			parameter_code: str = '', limit: int = 25,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch latest daily.
		
		Purpose:
			Retrieves latest daily using validated arguments and the stored USGSWaterData runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			monitoring_location_id (str): monitoring location ID value used by the fetch latest
				daily operation.
			parameter_code (str): parameter code value used by the fetch latest daily operation.
			limit (int): limit value used by the fetch latest daily operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'monitoring_location_id', monitoring_location_id )
			throw_if( 'limit', limit )
			throw_if( 'time', time )
			
			self.mode = 'latest-daily'
			self.monitoring_location_id = str( monitoring_location_id ).strip( )
			self.parameter_code = self.validate_parameter_code( parameter_code )
			self.limit = self.validate_limit( limit )
			self.timeout = int( time )
			
			self.request(
				collection='latest-daily',
				params={
						'monitoring_location_id': self.monitoring_location_id,
						'parameter_code': self.parameter_code,
						'limit': self.limit
				},
				time=self.timeout
			)
			
			records = self.coalesce_records( self.payload )
			rows = self.shape_latest_values( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = (
					'fetch_latest_daily( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'monitoring-locations',
			monitoring_location_id: str = '', state_code: str = '',
			county_code: str = '', site_type: str = '',
			parameter_code: str = '', limit: int = 25,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch USGS water services records.
		
		Purpose:
			Retrieves USGS water services records using validated arguments and the stored
			USGSWaterData runtime configuration. The method assembles request parameters, executes
			the provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			monitoring_location_id (str): monitoring location ID value used by the fetch operation.
			state_code (str): state code value used by the fetch operation.
			county_code (str): county code value used by the fetch operation.
			site_type (str): site type value used by the fetch operation.
			parameter_code (str): parameter code value used by the fetch operation.
			limit (int): limit value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			self.mode = str( mode or 'monitoring-locations' ).strip( ).lower( )
			
			if self.mode == 'monitoring-locations':
				return self.fetch_monitoring_locations(
					monitoring_location_id=monitoring_location_id,
					state_code=state_code,
					county_code=county_code,
					site_type=site_type,
					limit=limit,
					time=time
				)
			
			if self.mode == 'time-series-metadata':
				return self.fetch_time_series_metadata(
					monitoring_location_id=monitoring_location_id,
					parameter_code=parameter_code,
					limit=limit,
					time=time
				)
			
			if self.mode == 'latest-continuous':
				return self.fetch_latest_continuous(
					monitoring_location_id=monitoring_location_id,
					parameter_code=parameter_code,
					limit=limit,
					time=time
				)
			
			if self.mode == 'latest-daily':
				return self.fetch_latest_daily(
					monitoring_location_id=monitoring_location_id,
					parameter_code=parameter_code,
					limit=limit,
					time=time
				)
			
			raise ValueError(
				'Unsupported USGS Water Data mode. Use monitoring-locations, '
				'time-series-metadata, latest-continuous, or latest-daily.'
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if not isinstance( parameters, dict ):
				raise ValueError(
					'parameters must be a dict of param_name -> schema definition.'
				)
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSWaterData'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class USGSTheNationalMap( Fetcher ):
	"""U S G S The National Map fetcher.
	
	Purpose:
		Coordinates USGS National Map datasets and products within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		endpoint (Optional[str]): endpoint state retained by the instance.
		dataset (Optional[str]): dataset state retained by the instance.
		query_text (Optional[str]): query text state retained by the instance.
		bbox (Optional[str]): bbox state retained by the instance.
		prod_formats (Optional[str]): prod formats state retained by the instance.
		max_items (Optional[int]): max items state retained by the instance.
		offset (Optional[int]): offset state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	mode: Optional[ str ]
	endpoint: Optional[ str ]
	dataset: Optional[ str ]
	query_text: Optional[ str ]
	bbox: Optional[ str ]
	prod_formats: Optional[ str ]
	max_items: Optional[ int ]
	offset: Optional[ int ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize USGSTheNationalMap.
		
		Purpose:
			Initializes the USGSTheNationalMap instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://tnmaccess.nationalmap.gov/api/v1'
		self.mode = 'products'
		self.endpoint = None
		self.dataset = ''
		self.query_text = ''
		self.bbox = ''
		self.prod_formats = ''
		self.max_items = 25
		self.offset = 0
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'mode',
				'endpoint',
				'dataset',
				'query_text',
				'bbox',
				'prod_formats',
				'max_items',
				'offset',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'validate_endpoint',
				'validate_max_items',
				'validate_offset',
				'validate_bbox',
				'coalesce_records',
				'shape_dataset_rows',
				'shape_product_rows',
				'summarize_rows',
				'package_response',
				'request',
				'fetch_datasets',
				'fetch_products',
				'fetch',
				'create_schema'
		]
	
	def validate_endpoint( self, endpoint: str ) -> str:
		"""Validate endpoint.
		
		Purpose:
			Validates and normalizes endpoint before it is used in USGS National Map datasets and
			products. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			endpoint (str): endpoint value used by the validate endpoint operation.
		
		Returns:
			str: Validated endpoint value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'endpoint', endpoint )
			
			value = str( endpoint ).strip( ).lower( )
			allowed = {
					'datasets',
					'products'
			}
			
			if value not in allowed:
				raise ValueError( "endpoint must be 'datasets' or 'products'." )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = 'validate_endpoint( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_max_items( self, max_items: int ) -> int:
		"""Validate max items.
		
		Purpose:
			Validates and normalizes max items before it is used in USGS National Map datasets and
			products. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			max_items (int): max items value used by the validate max items operation.
		
		Returns:
			int: Validated max items value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'max_items', max_items )
			
			value = int( max_items )
			if value < 1 or value > 500:
				raise ValueError( 'max_items must be between 1 and 500.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = 'validate_max_items( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_offset( self, offset: int ) -> int:
		"""Validate offset.
		
		Purpose:
			Validates and normalizes offset before it is used in USGS National Map datasets and
			products. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			offset (int): offset value used by the validate offset operation.
		
		Returns:
			int: Validated offset value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if offset is None:
				raise ValueError( 'offset cannot be None.' )
			
			value = int( offset )
			if value < 0 or value > 10000:
				raise ValueError( 'offset must be between 0 and 10000.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = 'validate_offset( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_bbox( self, bbox: str ) -> str:
		"""Validate bbox.
		
		Purpose:
			Validates and normalizes bbox before it is used in USGS National Map datasets and
			products. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			bbox (str): bbox value used by the validate bbox operation.
		
		Returns:
			str: Validated bbox value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( bbox or '' ).strip( )
			
			if not value:
				return ''
			
			parts = [
					part.strip( )
					for part in value.split( ',' )
			]
			
			if len( parts ) != 4:
				raise ValueError( 'bbox must use minx,miny,maxx,maxy format.' )
			
			numbers = [ float( part ) for part in parts ]
			minx, miny, maxx, maxy = numbers
			
			if minx >= maxx:
				raise ValueError( 'bbox minx must be less than maxx.' )
			
			if miny >= maxy:
				raise ValueError( 'bbox miny must be less than maxy.' )
			
			return ','.join( [ str( number ) for number in numbers ] )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = 'validate_bbox( self, *args, **kwargs ) -> str'
			raise exception
	
	def coalesce_records( self, payload: Any ) -> List[ Dict[ str, Any ] ]:
		"""Coalesce records.
		
		Purpose:
			Performs the coalesce records operation for USGS National Map datasets and products. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			payload (object): payload value used by the coalesce records operation.
		
		Returns:
			List[Dict[str, Any]]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if payload is None:
				return [ ]
			
			if isinstance( payload, list ):
				return [
						item
						for item in payload
						if isinstance( item, dict )
				]
			
			if not isinstance( payload, dict ):
				return [ ]
			
			for key in [ 'items', 'datasets', 'data', 'results', 'products' ]:
				value = payload.get( key, None )
				
				if isinstance( value, list ):
					return [
							item
							for item in value
							if isinstance( item, dict )
					]
			
			return [ payload ]
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = (
					'coalesce_records( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_dataset_rows( self,
			records: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape dataset rows.
		
		Purpose:
			Transforms raw provider records into dataset rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			records (List[Dict[str, Any]]): records value used by the shape dataset rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in records or [ ]:
				rows.append(
					{
							'Id': item.get( 'id', '' ),
							'Dataset': (
									item.get( 'sbDatasetTag', None )
									or item.get( 'dataset', None )
									or item.get( 'tag', '' )
							),
							'Name': (
									item.get( 'sbDatasetName', None )
									or item.get( 'name', '' )
							),
							'Category': item.get( 'category', '' ),
							'Type': item.get( 'type', '' ),
							'Description': (
									item.get( 'description', None )
									or item.get( 'summary', '' )
							)
					}
				)
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = (
					'shape_dataset_rows( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_product_rows( self,
			records: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape product rows.
		
		Purpose:
			Transforms raw provider records into product rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			records (List[Dict[str, Any]]): records value used by the shape product rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in records or [ ]:
				download_url = (
						item.get( 'downloadURL', None )
						or item.get( 'downloadUrl', None )
						or item.get( 'url', '' )
				)
				meta_url = (
						item.get( 'metaUrl', None )
						or item.get( 'metadataUrl', None )
						or item.get( 'metaURL', '' )
				)
				bbox = (
						item.get( 'bbox', None )
						or item.get( 'boundingBox', None )
						or item.get( 'extent', '' )
				)
				
				rows.append(
					{
							'Title': (
									item.get( 'title', None )
									or item.get( 'name', None )
									or item.get( 'displayName', '' )
							),
							'Dataset': (
									item.get( 'dataset', None )
									or item.get( 'datasets', None )
									or item.get( 'sourceDataSet', '' )
							),
							'Product Format': (
									item.get( 'format', None )
									or item.get( 'prodFormat', None )
									or item.get( 'productFormat', '' )
							),
							'Publication Date': (
									item.get( 'publicationDate', None )
									or item.get( 'dateCreated', None )
									or item.get( 'lastUpdated', '' )
							),
							'Size': (
									item.get( 'size', None )
									or item.get( 'filesize', None )
									or item.get( 'fileSize', '' )
							),
							'Download URL': download_url,
							'Metadata URL': meta_url,
							'Bounding Box': bbox
					}
				)
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = (
					'shape_product_rows( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def summarize_rows( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Summarize rows.
		
		Purpose:
			Performs the summarize rows operation for USGS National Map datasets and products. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the summarize rows operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			count = len( rows or [ ] )
			first_title = ''
			first_dataset = ''
			
			if rows:
				first_title = str(
					rows[ 0 ].get( 'Title', '' )
					or rows[ 0 ].get( 'Name', '' )
					or rows[ 0 ].get( 'Dataset', '' )
					or ''
				)
				first_dataset = str( rows[ 0 ].get( 'Dataset', '' ) or '' )
			
			return {
					'count': count,
					'first_title': first_title,
					'first_dataset': first_dataset
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = (
					'summarize_rows( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def package_response( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the package response operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'summary': self.summarize_rows( rows ),
					'rows': rows,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = (
					'package_response( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def request( self, endpoint: str, params: Dict[ str, Any ],
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Request USGS National Map datasets and products.
		
		Purpose:
			Sends a provider request for USGS National Map datasets and products after request
			parameters have been validated or prepared by the caller. The method stores request,
			response, and payload state on the instance so subsequent methods can package or inspect
			the result consistently.
		
		Args:
			endpoint (str): endpoint value used by the request operation.
			params (Dict[str, Any]): Request or schema parameter dictionary used by the operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'endpoint', endpoint )
			throw_if( 'params', params )
			throw_if( 'time', time )
			
			self.endpoint = self.validate_endpoint( endpoint )
			self.timeout = int( time )
			self.url = f'{self.base_url}/{self.endpoint}'
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			for key, value in params.items( ):
				if value is None:
					continue
				
				if isinstance( value, str ) and not value.strip( ):
					continue
				
				self.params[ key ] = value
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.json( ) or { }
			self.result = {
					'url': self.response.url,
					'params': self.params,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = (
					'request( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_datasets( self, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch datasets.
		
		Purpose:
			Retrieves datasets using validated arguments and the stored USGSTheNationalMap runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'time', time )
			
			self.mode = 'datasets'
			self.timeout = int( time )
			
			self.request(
				endpoint='datasets',
				params={ },
				time=self.timeout
			)
			
			records = self.coalesce_records( self.payload )
			rows = self.shape_dataset_rows( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = (
					'fetch_datasets( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_products( self, dataset: str = '', q: str = '',
			bbox: str = '', prod_formats: str = '', max_items: int = 25,
			offset: int = 0, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch products.
		
		Purpose:
			Retrieves products using validated arguments and the stored USGSTheNationalMap runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			dataset (str): dataset value used by the fetch products operation.
			q (str): q value used by the fetch products operation.
			bbox (str): bbox value used by the fetch products operation.
			prod_formats (str): prod formats value used by the fetch products operation.
			max_items (int): max items value used by the fetch products operation.
			offset (int): offset value used by the fetch products operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'max_items', max_items )
			throw_if( 'offset', offset )
			throw_if( 'time', time )
			
			self.mode = 'products'
			self.dataset = str( dataset or '' ).strip( )
			self.query_text = str( q or '' ).strip( )
			self.bbox = self.validate_bbox( bbox )
			self.prod_formats = str( prod_formats or '' ).strip( )
			self.max_items = self.validate_max_items( max_items )
			self.offset = self.validate_offset( offset )
			self.timeout = int( time )
			
			self.request(
				endpoint='products',
				params={
						'datasets': self.dataset,
						'q': self.query_text,
						'bbox': self.bbox,
						'prodFormats': self.prod_formats,
						'max': self.max_items,
						'offset': self.offset
				},
				time=self.timeout
			)
			
			records = self.coalesce_records( self.payload )
			rows = self.shape_product_rows( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = (
					'fetch_products( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'products', dataset: str = '',
			q: str = '', bbox: str = '', prod_formats: str = '',
			max_items: int = 25, offset: int = 0,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch USGS National Map datasets and products.
		
		Purpose:
			Retrieves USGS National Map datasets and products using validated arguments and the
			stored USGSTheNationalMap runtime configuration. The method assembles request
			parameters, executes the provider call or dispatches to a specialized helper, records
			response state when applicable, and returns a normalized payload for downstream analysis
			or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			dataset (str): dataset value used by the fetch operation.
			q (str): q value used by the fetch operation.
			bbox (str): bbox value used by the fetch operation.
			prod_formats (str): prod formats value used by the fetch operation.
			max_items (int): max items value used by the fetch operation.
			offset (int): offset value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			self.mode = str( mode or 'products' ).strip( ).lower( )
			
			if self.mode == 'datasets':
				return self.fetch_datasets(
					time=time
				)
			
			if self.mode == 'products':
				return self.fetch_products(
					dataset=dataset,
					q=q,
					bbox=bbox,
					prod_formats=prod_formats,
					max_items=max_items,
					offset=offset,
					time=time
				)
			
			raise ValueError( "Unsupported TNMAccess mode. Use 'datasets' or 'products'." )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = 'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def create_schema( self, function: str, tool: str, description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if not isinstance( parameters, dict ):
				raise ValueError( 'parameters must be a dict of param_name -> schema definition.' )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSTheNationalMap'
			exception.method = 'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			raise exception

class USGSScienceBase( Fetcher ):
	"""U S G S Science Base fetcher.
	
	Purpose:
		Coordinates USGS ScienceBase items and catalog records within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		endpoint (Optional[str]): endpoint state retained by the instance.
		item_id (Optional[str]): item ID state retained by the instance.
		query_text (Optional[str]): query text state retained by the instance.
		max_items (Optional[int]): max items state retained by the instance.
		offset (Optional[int]): offset state retained by the instance.
		fields (Optional[str]): fields state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Dict[str, Any]]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	mode: Optional[ str ]
	endpoint: Optional[ str ]
	item_id: Optional[ str ]
	query_text: Optional[ str ]
	max_items: Optional[ int ]
	offset: Optional[ int ]
	fields: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Dict[ str, Any ] ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize USGSScienceBase.
		
		Purpose:
			Initializes the USGSScienceBase instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://www.sciencebase.gov/catalog'
		self.mode = 'items'
		self.endpoint = None
		self.item_id = ''
		self.query_text = ''
		self.max_items = 25
		self.offset = 0
		self.fields = ''
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'mode',
				'endpoint',
				'item_id',
				'query_text',
				'max_items',
				'offset',
				'fields',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'validate_endpoint',
				'validate_max_items',
				'validate_offset',
				'coalesce_records',
				'shape_item_rows',
				'shape_single_item',
				'summarize_rows',
				'package_response',
				'request',
				'fetch_items',
				'fetch_item',
				'fetch',
				'create_schema'
		]
	
	def validate_endpoint( self, endpoint: str ) -> str:
		"""Validate endpoint.
		
		Purpose:
			Validates and normalizes endpoint before it is used in USGS ScienceBase items and
			catalog records. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			endpoint (str): endpoint value used by the validate endpoint operation.
		
		Returns:
			str: Validated endpoint value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'endpoint', endpoint )
			
			value = str( endpoint ).strip( ).strip( '/' )
			
			if not value:
				raise ValueError( 'endpoint cannot be empty.' )
			
			if value.startswith( 'http://' ) or value.startswith( 'https://' ):
				raise ValueError( 'endpoint must be a path segment, not a full URL.' )
			
			if '..' in value:
				raise ValueError( 'endpoint cannot contain parent-directory markers.' )
			
			if value != 'items' and not value.startswith( 'item/' ):
				raise ValueError( "endpoint must be 'items' or 'item/{id}'." )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSScienceBase'
			exception.method = 'validate_endpoint( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_max_items( self, max_items: int ) -> int:
		"""Validate max items.
		
		Purpose:
			Validates and normalizes max items before it is used in USGS ScienceBase items and
			catalog records. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			max_items (int): max items value used by the validate max items operation.
		
		Returns:
			int: Validated max items value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'max_items', max_items )
			
			value = int( max_items )
			if value < 1 or value > 1000:
				raise ValueError( 'max_items must be between 1 and 1000.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSScienceBase'
			exception.method = 'validate_max_items( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_offset( self, offset: int ) -> int:
		"""Validate offset.
		
		Purpose:
			Validates and normalizes offset before it is used in USGS ScienceBase items and catalog
			records. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			offset (int): offset value used by the validate offset operation.
		
		Returns:
			int: Validated offset value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if offset is None:
				raise ValueError( 'offset cannot be None.' )
			
			value = int( offset )
			if value < 0 or value > 150000:
				raise ValueError( 'offset must be between 0 and 150000.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSScienceBase'
			exception.method = 'validate_offset( self, *args, **kwargs ) -> int'
			raise exception
	
	def coalesce_records( self, payload: Any ) -> List[ Dict[ str, Any ] ]:
		"""Coalesce records.
		
		Purpose:
			Performs the coalesce records operation for USGS ScienceBase items and catalog records.
			The method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			payload (object): payload value used by the coalesce records operation.
		
		Returns:
			List[Dict[str, Any]]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if payload is None:
				return [ ]
			
			if isinstance( payload, list ):
				return [
						item
						for item in payload
						if isinstance( item, dict )
				]
			
			if not isinstance( payload, dict ):
				return [ ]
			
			for key in [ 'items', 'results', 'data' ]:
				value = payload.get( key, None )
				
				if isinstance( value, list ):
					return [
							item
							for item in value
							if isinstance( item, dict )
					]
			
			return [ payload ]
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSScienceBase'
			exception.method = (
					'coalesce_records( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_single_item( self, item: Dict[ str, Any ] ) -> Dict[ str, Any ]:
		"""Shape single item.
		
		Purpose:
			Transforms raw provider records into single item structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			item (Dict[str, Any]): item value used by the shape single item operation.
		
		Returns:
			Dict[str, Any]: Normalized rows or summary structures created from provider response
				records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if not isinstance( item, dict ):
				item = { }
			
			files = item.get( 'files', [ ] ) or [ ]
			file_count = len( files ) if isinstance( files, list ) else 0
			
			web_links = item.get( 'webLinks', [ ] ) or [ ]
			link_count = len( web_links ) if isinstance( web_links, list ) else 0
			
			contacts = item.get( 'contacts', [ ] ) or [ ]
			contact_count = len( contacts ) if isinstance( contacts, list ) else 0
			
			return {
					'Id': item.get( 'id', '' ),
					'Title': item.get( 'title', '' ),
					'Type': item.get( 'itemType', '' ),
					'Updated': (
							item.get( 'dateUpdated', None )
							or item.get( 'lastUpdated', '' )
					),
					'Summary': (
							item.get( 'summary', None )
							or item.get( 'body', '' )
					),
					'Has Spatial Metadata': item.get( 'spatial', None ) is not None,
					'File Count': file_count,
					'Web Link Count': link_count,
					'Contact Count': contact_count,
					'Raw Item': item
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSScienceBase'
			exception.method = (
					'shape_single_item( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def shape_item_rows( self,
			records: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape item rows.
		
		Purpose:
			Transforms raw provider records into item rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			records (List[Dict[str, Any]]): records value used by the shape item rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in records or [ ]:
				rows.append( self.shape_single_item( item ) )
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSScienceBase'
			exception.method = (
					'shape_item_rows( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def summarize_rows( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Summarize rows.
		
		Purpose:
			Performs the summarize rows operation for USGS ScienceBase items and catalog records.
			The method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the summarize rows operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			count = len( rows or [ ] )
			first_title = ''
			first_type = ''
			spatial_count = 0
			
			for row in rows or [ ]:
				if row.get( 'Has Spatial Metadata', False ):
					spatial_count += 1
			
			if rows:
				first_title = str( rows[ 0 ].get( 'Title', '' ) or '' )
				first_type = str( rows[ 0 ].get( 'Type', '' ) or '' )
			
			return {
					'count': count,
					'first_title': first_title,
					'first_type': first_type,
					'spatial_count': spatial_count
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSScienceBase'
			exception.method = (
					'summarize_rows( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def package_response( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the package response operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'summary': self.summarize_rows( rows ),
					'rows': rows,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSScienceBase'
			exception.method = (
					'package_response( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def request( self, endpoint: str,
			params: Optional[ Dict[ str, Any ] ] = None,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Request USGS ScienceBase items and catalog records.
		
		Purpose:
			Sends a provider request for USGS ScienceBase items and catalog records after request
			parameters have been validated or prepared by the caller. The method stores request,
			response, and payload state on the instance so subsequent methods can package or inspect
			the result consistently.
		
		Args:
			endpoint (str): endpoint value used by the request operation.
			params (Optional[Dict[str, Any]]): Request or schema parameter dictionary used by the
				operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'endpoint', endpoint )
			throw_if( 'time', time )
			
			self.endpoint = self.validate_endpoint( endpoint )
			self.timeout = int( time )
			self.url = f'{self.base_url}/{self.endpoint}'
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			for key, value in (params or { }).items( ):
				if value is None:
					continue
				
				if isinstance( value, str ) and not value.strip( ):
					continue
				
				self.params[ key ] = value
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.json( ) or { }
			self.result = {
					'url': self.response.url,
					'params': self.params,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSScienceBase'
			exception.method = 'request( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def fetch_items( self, q: str = '', max_items: int = 25,
			offset: int = 0, fields: str = '',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch items.
		
		Purpose:
			Retrieves items using validated arguments and the stored USGSScienceBase runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			q (str): q value used by the fetch items operation.
			max_items (int): max items value used by the fetch items operation.
			offset (int): offset value used by the fetch items operation.
			fields (str): fields value used by the fetch items operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'max_items', max_items )
			throw_if( 'offset', offset )
			throw_if( 'time', time )
			self.mode = 'items'
			self.query_text = str( q or '' ).strip( )
			self.max_items = self.validate_max_items( max_items )
			self.offset = self.validate_offset( offset )
			self.fields = str( fields or '' ).strip( )
			self.timeout = int( time )
			
			self.request( endpoint='items',
				params={
						'q': self.query_text,
						'max': self.max_items,
						'offset': self.offset,
						'fields': self.fields
				}, time=self.timeout )
			
			records = self.coalesce_records( self.payload )
			rows = self.shape_item_rows( records )
			return self.package_response( rows )
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSScienceBase'
			exception.method = 'fetch_items( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def fetch_item( self, item_id: str,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch item.
		
		Purpose:
			Retrieves item using validated arguments and the stored USGSScienceBase runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			item_id (str): item ID value used by the fetch item operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'item_id', item_id )
			throw_if( 'time', time )
			self.mode = 'item'
			self.item_id = str( item_id ).strip( )
			self.timeout = int( time )
			self.request( endpoint=f'item/{self.item_id}', params={ }, time=self.timeout )
			detail = self.shape_single_item( self.payload or { } )
			return self.package_response( [ detail ] )
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSScienceBase'
			exception.method = 'fetch_item( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def fetch( self, mode: str = 'items', q: str = '', item_id: str = '', max_items: int = 25,
			offset: int = 0, fields: str = '', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch USGS ScienceBase items and catalog records.
		
		Purpose:
			Retrieves USGS ScienceBase items and catalog records using validated arguments and the
			stored USGSScienceBase runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			q (str): q value used by the fetch operation.
			item_id (str): item ID value used by the fetch operation.
			max_items (int): max items value used by the fetch operation.
			offset (int): offset value used by the fetch operation.
			fields (str): fields value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			self.mode = str( mode or 'items' ).strip( ).lower( )
			if self.mode == 'items':
				return self.fetch_items( q=q, max_items=max_items, offset=offset, fields=fields,
					time=time )
			
			if self.mode == 'item':
				return self.fetch_item( item_id=item_id, time=time )
			
			raise ValueError( "Unsupported ScienceBase mode. Use 'items' or 'item'." )
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSScienceBase'
			exception.method = 'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			if not isinstance( parameters, dict ):
				raise ValueError( 'parameters must be a dict of param_name -> schema definition.' )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'USGSScienceBase'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class AirNow( Fetcher ):
	"""Air Now fetcher.
	
	Purpose:
		Coordinates AirNow current and forecast air quality data within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		api_key (Optional[str]): API key state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		timeout (Optional[int]): timeout state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		endpoint (Optional[str]): endpoint state retained by the instance.
		zip_code (Optional[str]): zip code state retained by the instance.
		latitude (Optional[float]): latitude state retained by the instance.
		longitude (Optional[float]): longitude state retained by the instance.
		date (Optional[str]): date state retained by the instance.
		distance (Optional[int]): distance state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		response (object): response state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	api_key: Optional[ str ]
	mode: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	timeout: Optional[ int ]
	agents: Optional[ str ]
	endpoint: Optional[ str ]
	zip_code: Optional[ str ]
	latitude: Optional[ float ]
	longitude: Optional[ float ]
	date: Optional[ str ]
	distance: Optional[ int ]
	result: Optional[ Dict[ str, Any ] ]
	
	def __init__( self ) -> None:
		"""Initialize AirNow.
		
		Purpose:
			Initializes the AirNow instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://www.airnowapi.org/aq'
		self.api_key = cfg.AIRNOW_API_KEY
		self.mode = 'current-zip'
		self.params = { }
		self.payload = [ ]
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.endpoint = None
		self.zip_code = None
		self.latitude = None
		self.longitude = None
		self.date = None
		self.distance = None
		self.response = None
		self.result = { }
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'api_key',
				'mode',
				'params',
				'payload',
				'timeout',
				'agents',
				'endpoint',
				'zip_code',
				'latitude',
				'longitude',
				'date',
				'distance',
				'response',
				'result',
				'request',
				'shape_rows',
				'summarize_rows',
				'package_response',
				'fetch_current_zip',
				'fetch_current_latlon',
				'fetch_forecast_zip',
				'fetch_forecast_latlon',
				'fetch',
				'create_schema'
		]
	
	def request( self, endpoint: str, params: Optional[ Dict[ str, Any ] ] = None,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Request AirNow current and forecast air quality data.
		
		Purpose:
			Sends a provider request for AirNow current and forecast air quality data after request
			parameters have been validated or prepared by the caller. The method stores request,
			response, and payload state on the instance so subsequent methods can package or inspect
			the result consistently.
		
		Args:
			endpoint (str): endpoint value used by the request operation.
			params (Optional[Dict[str, Any]]): Request or schema parameter dictionary used by the
				operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'api_key', self.api_key )
			throw_if( 'endpoint', endpoint )
			throw_if( 'time', time )
			
			self.endpoint = str( endpoint ).strip( )
			self.timeout = int( time )
			self.url = f'{self.base_url}/{self.endpoint}'
			self.params = { }
			
			for key, value in (params or { }).items( ):
				if value is None:
					continue
				
				if isinstance( value, str ) and not value.strip( ):
					continue
				
				self.params[ key ] = value
			
			self.params[ 'format' ] = 'application/json'
			self.params[ 'API_KEY' ] = self.api_key
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			
			self.response.raise_for_status( )
			self.payload = self.response.json( )
			self.result = {
					'url': self.url,
					'params': self.params,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'AirNow'
			exception.method = (
					'request( self, endpoint: str, params: Optional[ Dict[ str, Any ] ]=None, '
					'time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def shape_rows( self, records: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape rows.
		
		Purpose:
			Transforms raw provider records into rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			records (List[Dict[str, Any]]): records value used by the shape rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in records or [ ]:
				category = item.get( 'Category', { } ) or { }
				category_name = category.get( 'Name', '' ) if isinstance( category, dict ) else ''
				
				rows.append(
					{
							'Date Observed': item.get( 'DateObserved', '' ),
							'Hour Observed': item.get( 'HourObserved', '' ),
							'Local Time Zone': item.get( 'LocalTimeZone', '' ),
							'Reporting Area': item.get( 'ReportingArea', '' ),
							'State Code': item.get( 'StateCode', '' ),
							'Latitude': item.get( 'Latitude', None ),
							'Longitude': item.get( 'Longitude', None ),
							'Parameter Name': item.get( 'ParameterName', '' ),
							'AQI': item.get( 'AQI', None ),
							'Category': category_name,
							'Action Day': item.get( 'ActionDay', '' ),
							'Discussion': item.get( 'Discussion', '' )
					}
				)
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'AirNow'
			exception.method = (
					'shape_rows( self, records: List[ Dict[ str, Any ] ] ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def summarize_rows( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Summarize rows.
		
		Purpose:
			Performs the summarize rows operation for AirNow current and forecast air quality data.
			The method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the summarize rows operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			count = len( rows or [ ] )
			max_aqi = None
			dominant_parameter = ''
			top_category = ''
			reporting_area = ''
			
			for row in rows or [ ]:
				if not reporting_area and row.get( 'Reporting Area', '' ):
					reporting_area = str( row.get( 'Reporting Area', '' ) )
				
				aqi_value = row.get( 'AQI', None )
				
				try:
					if aqi_value is not None:
						if max_aqi is None or float( aqi_value ) > float( max_aqi ):
							max_aqi = float( aqi_value )
							dominant_parameter = str( row.get( 'Parameter Name', '' ) or '' )
							top_category = str( row.get( 'Category', '' ) or '' )
				
				except Exception:
					pass
			
			return {
					'count': count,
					'max_aqi': max_aqi,
					'dominant_parameter': dominant_parameter,
					'top_category': top_category,
					'reporting_area': reporting_area
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'AirNow'
			exception.method = (
					'summarize_rows( self, rows: List[ Dict[ str, Any ] ] ) '
					'-> Dict[ str, Any ]'
			)
			raise exception
	
	def package_response( self ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			records = self.result.get( 'raw', [ ] ) if isinstance( self.result, dict ) else [ ]
			records = records or [ ]
			rows = self.shape_rows( records )
			
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'summary': self.summarize_rows( rows ),
					'rows': rows,
					'raw': records
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'AirNow'
			exception.method = 'package_response( self ) -> Dict[ str, Any ]'
			raise exception
	
	def fetch_current_zip( self, zip_code: str, distance: int = 25,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch current zip.
		
		Purpose:
			Retrieves current zip using validated arguments and the stored AirNow runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			zip_code (str): zip code value used by the fetch current zip operation.
			distance (int): distance value used by the fetch current zip operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'zip_code', zip_code )
			throw_if( 'distance', distance )
			throw_if( 'time', time )
			
			self.mode = 'current-zip'
			self.zip_code = str( zip_code ).strip( )
			self.distance = int( distance )
			self.timeout = int( time )
			
			self.request(
				endpoint='observation/zipCode/current/',
				params={
						'zipCode': self.zip_code,
						'distance': self.distance
				},
				time=self.timeout
			)
			
			return self.package_response( )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'AirNow'
			exception.method = (
					'fetch_current_zip( self, zip_code: str, distance: int=25, '
					'time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_current_latlon( self, latitude: float, longitude: float,
			distance: int = 25, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch current latlon.
		
		Purpose:
			Retrieves current latlon using validated arguments and the stored AirNow runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			latitude (float): latitude value used by the fetch current latlon operation.
			longitude (float): longitude value used by the fetch current latlon operation.
			distance (int): distance value used by the fetch current latlon operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'latitude', latitude )
			throw_if( 'longitude', longitude )
			throw_if( 'distance', distance )
			throw_if( 'time', time )
			
			self.mode = 'current-latlon'
			self.latitude = float( latitude )
			self.longitude = float( longitude )
			self.distance = int( distance )
			self.timeout = int( time )
			
			self.request(
				endpoint='observation/latLong/current/',
				params={
						'latitude': self.latitude,
						'longitude': self.longitude,
						'distance': self.distance
				},
				time=self.timeout
			)
			
			return self.package_response( )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'AirNow'
			exception.method = (
					'fetch_current_latlon( self, latitude: float, longitude: float, '
					'distance: int=25, time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_forecast_zip( self, zip_code: str, date: str,
			distance: int = 25, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch forecast zip.
		
		Purpose:
			Retrieves forecast zip using validated arguments and the stored AirNow runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			zip_code (str): zip code value used by the fetch forecast zip operation.
			date (str): date value used by the fetch forecast zip operation.
			distance (int): distance value used by the fetch forecast zip operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'zip_code', zip_code )
			throw_if( 'date', date )
			throw_if( 'distance', distance )
			throw_if( 'time', time )
			
			self.mode = 'forecast-zip'
			self.zip_code = str( zip_code ).strip( )
			self.date = str( date ).strip( )
			self.distance = int( distance )
			self.timeout = int( time )
			
			self.request(
				endpoint='forecast/zipCode/',
				params={
						'zipCode': self.zip_code,
						'date': self.date,
						'distance': self.distance
				},
				time=self.timeout
			)
			
			return self.package_response( )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'AirNow'
			exception.method = (
					'fetch_forecast_zip( self, zip_code: str, date: str, distance: int=25, '
					'time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch_forecast_latlon( self, latitude: float, longitude: float,
			date: str, distance: int = 25, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch forecast latlon.
		
		Purpose:
			Retrieves forecast latlon using validated arguments and the stored AirNow runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			latitude (float): latitude value used by the fetch forecast latlon operation.
			longitude (float): longitude value used by the fetch forecast latlon operation.
			date (str): date value used by the fetch forecast latlon operation.
			distance (int): distance value used by the fetch forecast latlon operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'latitude', latitude )
			throw_if( 'longitude', longitude )
			throw_if( 'date', date )
			throw_if( 'distance', distance )
			throw_if( 'time', time )
			
			self.mode = 'forecast-latlon'
			self.latitude = float( latitude )
			self.longitude = float( longitude )
			self.date = str( date ).strip( )
			self.distance = int( distance )
			self.timeout = int( time )
			
			self.request(
				endpoint='forecast/latLong/',
				params={
						'latitude': self.latitude,
						'longitude': self.longitude,
						'date': self.date,
						'distance': self.distance
				},
				time=self.timeout
			)
			
			return self.package_response( )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'AirNow'
			exception.method = (
					'fetch_forecast_latlon( self, latitude: float, longitude: float, '
					'date: str, distance: int=25, time: int=20 ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def fetch( self, mode: str = 'current-zip', zip_code: str = '',
			latitude: float | None = None, longitude: float | None = None,
			date: str = '', distance: int = 25,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch AirNow current and forecast air quality data.
		
		Purpose:
			Retrieves AirNow current and forecast air quality data using validated arguments and the
			stored AirNow runtime configuration. The method assembles request parameters, executes
			the provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			zip_code (str): zip code value used by the fetch operation.
			latitude (float | None): latitude value used by the fetch operation.
			longitude (float | None): longitude value used by the fetch operation.
			date (str): date value used by the fetch operation.
			distance (int): distance value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			self.mode = str( mode ).strip( ).lower( )
			
			if self.mode == 'current-zip':
				return self.fetch_current_zip( zip_code, distance, time )
			
			if self.mode == 'current-latlon':
				return self.fetch_current_latlon( latitude, longitude, distance, time )
			
			if self.mode == 'forecast-zip':
				return self.fetch_forecast_zip( zip_code, date, distance, time )
			
			if self.mode == 'forecast-latlon':
				return self.fetch_forecast_latlon( latitude, longitude, date, distance, time )
			
			raise ValueError(
				"Unsupported AirNow mode. Expected 'current-zip', 'current-latlon', "
				"'forecast-zip', or 'forecast-latlon'."
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'AirNow'
			exception.method = (
					'fetch( self, mode: str, zip_code: str, latitude: float | None, '
					'longitude: float | None, date: str, distance: int, time: int ) '
					'-> Dict[ str, Any ]'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f"{description.strip( )} This function uses the "
							f"{tool.strip( )} service."
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'AirNow'
			exception.method = (
					'create_schema( self, function: str, tool: str, description: str, '
					'parameters: dict, required: list[ str ] ) -> Dict[ str, str ]'
			)
			raise exception

class ClimateData( Fetcher ):
	"""Climate Data fetcher.
	
	Purpose:
		Coordinates NOAA climate dataset and data records within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		data_url (Optional[str]): data URL state retained by the instance.
		search_url (Optional[str]): search URL state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		keyword (Optional[str]): keyword state retained by the instance.
		dataset (Optional[str]): dataset state retained by the instance.
		start_date (Optional[str]): start date state retained by the instance.
		end_date (Optional[str]): end date state retained by the instance.
		stations (Optional[str]): stations state retained by the instance.
		data_types (Optional[str]): data types state retained by the instance.
		limit (Optional[int]): limit state retained by the instance.
		offset (Optional[int]): offset state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	data_url: Optional[ str ]
	search_url: Optional[ str ]
	mode: Optional[ str ]
	keyword: Optional[ str ]
	dataset: Optional[ str ]
	start_date: Optional[ str ]
	end_date: Optional[ str ]
	stations: Optional[ str ]
	data_types: Optional[ str ]
	limit: Optional[ int ]
	offset: Optional[ int ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize ClimateData.
		
		Purpose:
			Initializes the ClimateData instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.data_url = 'https://www.ncei.noaa.gov/access/services/data/v1'
		self.search_url = 'https://www.ncei.noaa.gov/access/services/search/v1'
		self.mode = 'datasets'
		self.keyword = ''
		self.dataset = ''
		self.start_date = ''
		self.end_date = ''
		self.stations = ''
		self.data_types = ''
		self.limit = 25
		self.offset = 0
		self.params = { }
		self.payload = [ ]
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = { 'Accept': 'application/json', 'User-Agent': self.agents }
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'data_url',
				'search_url',
				'mode',
				'keyword',
				'dataset',
				'start_date',
				'end_date',
				'stations',
				'data_types',
				'limit',
				'offset',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'validate_limit',
				'validate_offset',
				'validate_date_range',
				'coalesce_records',
				'shape_dataset_rows',
				'shape_data_rows',
				'summarize_rows',
				'package_response',
				'request',
				'fetch_datasets',
				'fetch_data',
				'fetch',
				'create_schema'
		]
	
	def validate_limit( self, limit: int ) -> int:
		"""Validate limit.
		
		Purpose:
			Validates and normalizes limit before it is used in NOAA climate dataset and data
			records. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			limit (int): limit value used by the validate limit operation.
		
		Returns:
			int: Validated limit value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'limit', limit )
			
			value = int( limit )
			if value < 1 or value > 500:
				raise ValueError( 'limit must be between 1 and 500.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ClimateData'
			exception.method = 'validate_limit( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_offset( self, offset: int ) -> int:
		"""Validate offset.
		
		Purpose:
			Validates and normalizes offset before it is used in NOAA climate dataset and data
			records. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			offset (int): offset value used by the validate offset operation.
		
		Returns:
			int: Validated offset value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if offset is None:
				raise ValueError( 'offset cannot be None.' )
			
			value = int( offset )
			if value < 0 or value > 10000:
				raise ValueError( 'offset must be between 0 and 10000.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ClimateData'
			exception.method = 'validate_offset( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_date_range( self, start_date: str, end_date: str ) -> Tuple[ str, str ]:
		"""Validate date range.
		
		Purpose:
			Validates and normalizes date range before it is used in NOAA climate dataset and data
			records. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			start_date (str): start date value used by the validate date range operation.
			end_date (str): end date value used by the validate date range operation.
		
		Returns:
			Tuple[str, str]: Validated date range value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'start_date', start_date )
			throw_if( 'end_date', end_date )
			
			start_value = str( start_date ).strip( )
			end_value = str( end_date ).strip( )
			
			if start_value > end_value:
				raise ValueError( 'start_date must be on or before end_date.' )
			
			return start_value, end_value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ClimateData'
			exception.method = (
					'validate_date_range( self, *args, **kwargs ) -> Tuple[ str, str ]'
			)
			raise exception
	
	def coalesce_records( self, payload: Any ) -> List[ Dict[ str, Any ] ]:
		"""Coalesce records.
		
		Purpose:
			Performs the coalesce records operation for NOAA climate dataset and data records. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			payload (object): payload value used by the coalesce records operation.
		
		Returns:
			List[Dict[str, Any]]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if payload is None:
				return [ ]
			
			if isinstance( payload, list ):
				return [
						item
						for item in payload
						if isinstance( item, dict )
				]
			
			if not isinstance( payload, dict ):
				return [ ]
			
			for key in [ 'results', 'data', 'items', 'records' ]:
				value = payload.get( key, None )
				
				if isinstance( value, list ):
					return [
							item
							for item in value
							if isinstance( item, dict )
					]
			
			return [ payload ]
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ClimateData'
			exception.method = (
					'coalesce_records( self, *args, **kwargs ) -> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_dataset_rows( self,
			records: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape dataset rows.
		
		Purpose:
			Transforms raw provider records into dataset rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			records (List[Dict[str, Any]]): records value used by the shape dataset rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in records or [ ]:
				rows.append(
					{
							'Id': item.get( 'id', '' ),
							'Dataset': (
									item.get( 'dataset', None )
									or item.get( 'name', '' )
							),
							'Title': (
									item.get( 'title', None )
									or item.get( 'name', '' )
							),
							'Description': (
									item.get( 'description', None )
									or item.get( 'summary', '' )
							),
							'Start Date': item.get( 'startDate', '' ),
							'End Date': item.get( 'endDate', '' )
					}
				)
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ClimateData'
			exception.method = (
					'shape_dataset_rows( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_data_rows( self, records: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape data rows.
		
		Purpose:
			Transforms raw provider records into data rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			records (List[Dict[str, Any]]): records value used by the shape data rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in records or [ ]:
				row: Dict[ str, Any ] = { }
				
				for key, value in item.items( ):
					friendly_key = str( key ).replace( '_', ' ' ).title( )
					row[ friendly_key ] = value
				
				rows.append( row )
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ClimateData'
			exception.method = 'shape_data_rows( self, *args, **kwargs ) -> List[ Dict[ str, Any ]]'
			raise exception
	
	def summarize_rows( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Summarize rows.
		
		Purpose:
			Performs the summarize rows operation for NOAA climate dataset and data records. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the summarize rows operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			count = len( rows or [ ] )
			first_title = ''
			first_dataset = ''
			
			if rows:
				first_title = str(
					rows[ 0 ].get( 'Title', '' )
					or rows[ 0 ].get( 'Station', '' )
					or rows[ 0 ].get( 'Date', '' )
					or rows[ 0 ].get( 'Start Date', '' )
					or ''
				)
				first_dataset = str(
					rows[ 0 ].get( 'Dataset', '' )
					or rows[ 0 ].get( 'Datatype', '' )
					or rows[ 0 ].get( 'Data Type', '' )
					or ''
				)
			
			return {
					'count': count,
					'first_title': first_title,
					'first_dataset': first_dataset
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ClimateData'
			exception.method = 'summarize_rows( self, *args, **kwargs ) -> Dict[ str, Any ]'
			raise exception
	
	def package_response( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the package response operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'summary': self.summarize_rows( rows ),
					'rows': rows,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ClimateData'
			exception.method = (
					'package_response( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def request( self, url: str, params: Dict[ str, Any ], time: int = 20 ) -> Dict[
		                                                                           str, Any ] | None:
		"""Request NOAA climate dataset and data records.
		
		Purpose:
			Sends a provider request for NOAA climate dataset and data records after request
			parameters have been validated or prepared by the caller. The method stores request,
			response, and payload state on the instance so subsequent methods can package or inspect
			the result consistently.
		
		Args:
			url (str): URL or URI value used as the request or parsing source.
			params (Dict[str, Any]): Request or schema parameter dictionary used by the operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'url', url )
			throw_if( 'params', params )
			throw_if( 'time', time )
			
			self.url = str( url ).strip( )
			self.timeout = int( time )
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			for key, value in params.items( ):
				if value is None:
					continue
				
				if isinstance( value, str ) and not value.strip( ):
					continue
				
				self.params[ key ] = value
			
			self.response = requests.get( url=self.url, params=self.params, headers=self.headers,
				timeout=self.timeout )
			self.response.raise_for_status( )
			
			content_type = str( self.response.headers.get( 'Content-Type', '' ) ).lower( )
			if 'application/json' in content_type:
				self.payload = self.response.json( ) or { }
			else:
				self.payload = self.response.text or ''
			
			self.result = {
					'url': self.response.url,
					'params': self.params,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ClimateData'
			exception.method = 'request( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def fetch_datasets( self, keyword: str = '', start_date: str = '', end_date: str = '',
			limit: int = 25, offset: int = 0, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch datasets.
		
		Purpose:
			Retrieves datasets using validated arguments and the stored ClimateData runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			keyword (str): keyword value used by the fetch datasets operation.
			start_date (str): start date value used by the fetch datasets operation.
			end_date (str): end date value used by the fetch datasets operation.
			limit (int): limit value used by the fetch datasets operation.
			offset (int): offset value used by the fetch datasets operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'limit', limit )
			throw_if( 'offset', offset )
			throw_if( 'time', time )
			
			self.mode = 'datasets'
			self.keyword = str( keyword or '' ).strip( )
			self.start_date = str( start_date or '' ).strip( )
			self.end_date = str( end_date or '' ).strip( )
			self.limit = self.validate_limit( limit )
			self.offset = self.validate_offset( offset )
			self.timeout = int( time )
			if self.start_date and self.end_date:
				self.start_date, self.end_date = self.validate_date_range( self.start_date,
					self.end_date )
			
			self.request( url=f'{self.search_url}/datasets', params={
					'keyword': self.keyword,
					'startDate': self.start_date,
					'endDate': self.end_date,
					'limit': self.limit,
					'offset': self.offset
			},
				time=self.timeout )
			
			records = self.coalesce_records( self.payload )
			rows = self.shape_dataset_rows( records )
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ClimateData'
			exception.method = 'fetch_datasets( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def fetch_data( self, dataset: str, start_date: str, end_date: str, stations: str = '',
			data_types: str = '', limit: int = 25, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch data.
		
		Purpose:
			Retrieves data using validated arguments and the stored ClimateData runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			dataset (str): dataset value used by the fetch data operation.
			start_date (str): start date value used by the fetch data operation.
			end_date (str): end date value used by the fetch data operation.
			stations (str): stations value used by the fetch data operation.
			data_types (str): data types value used by the fetch data operation.
			limit (int): limit value used by the fetch data operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'dataset', dataset )
			throw_if( 'start_date', start_date )
			throw_if( 'end_date', end_date )
			throw_if( 'limit', limit )
			throw_if( 'time', time )
			
			self.mode = 'data'
			self.dataset = str( dataset ).strip( )
			self.start_date, self.end_date = self.validate_date_range( start_date, end_date )
			self.stations = str( stations or '' ).strip( )
			self.data_types = str( data_types or '' ).strip( )
			self.limit = self.validate_limit( limit )
			self.timeout = int( time )
			
			self.request( url=self.data_url,
				params={ 'dataset': self.dataset, 'startDate': self.start_date,
				         'endDate': self.end_date,
				         'stations': self.stations, 'dataTypes': self.data_types,
				         'format': 'json', 'limit': self.limit },
				time=self.timeout )
			
			records = self.coalesce_records( self.payload )
			rows = self.shape_data_rows( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ClimateData'
			exception.method = 'fetch_data( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def fetch( self, mode: str = 'datasets', keyword: str = '', dataset: str = '',
			start_date: str = '', end_date: str = '', stations: str = '', data_types: str = '',
			limit: int = 25, offset: int = 0, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch NOAA climate dataset and data records.
		
		Purpose:
			Retrieves NOAA climate dataset and data records using validated arguments and the stored
			ClimateData runtime configuration. The method assembles request parameters, executes the
			provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			keyword (str): keyword value used by the fetch operation.
			dataset (str): dataset value used by the fetch operation.
			start_date (str): start date value used by the fetch operation.
			end_date (str): end date value used by the fetch operation.
			stations (str): stations value used by the fetch operation.
			data_types (str): data types value used by the fetch operation.
			limit (int): limit value used by the fetch operation.
			offset (int): offset value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			self.mode = str( mode or 'datasets' ).strip( ).lower( )
			
			if self.mode == 'datasets':
				return self.fetch_datasets(
					keyword=keyword,
					start_date=start_date,
					end_date=end_date,
					limit=limit,
					offset=offset,
					time=time
				)
			
			if self.mode == 'data':
				return self.fetch_data( dataset=dataset, start_date=start_date, end_date=end_date,
					stations=stations, data_types=data_types, limit=limit, time=time )
			
			raise ValueError( "Unsupported ClimateData mode. Use 'datasets' or 'data'." )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ClimateData'
			exception.method = 'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			raise exception
	
	def create_schema( self, function: str, tool: str, description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if not isinstance( parameters, dict ):
				raise ValueError(
					'parameters must be a dict of param_name -> schema definition.'
				)
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'ClimateData'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class EoNet( Fetcher ):
	"""Eo Net fetcher.
	
	Purpose:
		Coordinates NASA EONET environmental event data within Fonky. The class stores provider
		configuration, request parameters, response payloads, and normalized result state so
		callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		endpoint (Optional[str]): endpoint state retained by the instance.
		source (Optional[str]): source state retained by the instance.
		category (Optional[str]): category state retained by the instance.
		status (Optional[str]): status state retained by the instance.
		limit (Optional[int]): limit state retained by the instance.
		days (Optional[int]): days state retained by the instance.
		start_date (Optional[str]): start date state retained by the instance.
		end_date (Optional[str]): end date state retained by the instance.
		bbox (Optional[str]): bbox state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	mode: Optional[ str ]
	endpoint: Optional[ str ]
	source: Optional[ str ]
	category: Optional[ str ]
	status: Optional[ str ]
	limit: Optional[ int ]
	days: Optional[ int ]
	start_date: Optional[ str ]
	end_date: Optional[ str ]
	bbox: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize EoNet.
		
		Purpose:
			Initializes the EoNet instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://eonet.gsfc.nasa.gov/api/v3'
		self.mode = 'events'
		self.endpoint = None
		self.source = ''
		self.category = ''
		self.status = 'open'
		self.limit = 25
		self.days = 30
		self.start_date = ''
		self.end_date = ''
		self.bbox = ''
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'mode',
				'endpoint',
				'source',
				'category',
				'status',
				'limit',
				'days',
				'start_date',
				'end_date',
				'bbox',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'validate_endpoint',
				'validate_status',
				'validate_limit',
				'validate_days',
				'validate_bbox',
				'validate_date_pair',
				'shape_event_rows',
				'shape_category_rows',
				'summarize_rows',
				'package_response',
				'request',
				'fetch_events',
				'fetch_categories',
				'fetch',
				'create_schema'
		]
	
	def validate_endpoint( self, endpoint: str ) -> str:
		"""Validate endpoint.
		
		Purpose:
			Validates and normalizes endpoint before it is used in NASA EONET environmental event
			data. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			endpoint (str): endpoint value used by the validate endpoint operation.
		
		Returns:
			str: Validated endpoint value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'endpoint', endpoint )
			
			value = str( endpoint ).strip( ).lower( )
			allowed = {
					'events',
					'categories'
			}
			
			if value not in allowed:
				raise ValueError( "endpoint must be 'events' or 'categories'." )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = 'validate_endpoint( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_status( self, status: str ) -> str:
		"""Validate status.
		
		Purpose:
			Validates and normalizes status before it is used in NASA EONET environmental event
			data. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			status (str): status value used by the validate status operation.
		
		Returns:
			str: Validated status value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'status', status )
			
			value = str( status ).strip( ).lower( )
			allowed = {
					'open',
					'closed',
					'all'
			}
			
			if value not in allowed:
				raise ValueError( "status must be 'open', 'closed', or 'all'." )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = 'validate_status( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_limit( self, limit: int ) -> int:
		"""Validate limit.
		
		Purpose:
			Validates and normalizes limit before it is used in NASA EONET environmental event data.
			The method converts incoming values to the expected representation, enforces visible
			range or format constraints, and returns the checked value for request construction.
		
		Args:
			limit (int): limit value used by the validate limit operation.
		
		Returns:
			int: Validated limit value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'limit', limit )
			
			value = int( limit )
			if value < 1 or value > 500:
				raise ValueError( 'limit must be between 1 and 500.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = 'validate_limit( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_days( self, days: int ) -> int:
		"""Validate days.
		
		Purpose:
			Validates and normalizes days before it is used in NASA EONET environmental event data.
			The method converts incoming values to the expected representation, enforces visible
			range or format constraints, and returns the checked value for request construction.
		
		Args:
			days (int): days value used by the validate days operation.
		
		Returns:
			int: Validated days value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'days', days )
			
			value = int( days )
			if value < 1 or value > 3650:
				raise ValueError( 'days must be between 1 and 3650.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = 'validate_days( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_bbox( self, bbox: str ) -> str:
		"""Validate bbox.
		
		Purpose:
			Validates and normalizes bbox before it is used in NASA EONET environmental event data.
			The method converts incoming values to the expected representation, enforces visible
			range or format constraints, and returns the checked value for request construction.
		
		Args:
			bbox (str): bbox value used by the validate bbox operation.
		
		Returns:
			str: Validated bbox value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( bbox or '' ).strip( )
			
			if not value:
				return ''
			
			parts = [
					part.strip( )
					for part in value.split( ',' )
			]
			
			if len( parts ) != 4:
				raise ValueError(
					'bbox must use min_lon,max_lat,max_lon,min_lat format.'
				)
			
			numbers = [ float( part ) for part in parts ]
			min_lon, max_lat, max_lon, min_lat = numbers
			
			if min_lon < -180.0 or min_lon > 180.0:
				raise ValueError( 'bbox min_lon must be between -180 and 180.' )
			
			if max_lon < -180.0 or max_lon > 180.0:
				raise ValueError( 'bbox max_lon must be between -180 and 180.' )
			
			if min_lat < -90.0 or min_lat > 90.0:
				raise ValueError( 'bbox min_lat must be between -90 and 90.' )
			
			if max_lat < -90.0 or max_lat > 90.0:
				raise ValueError( 'bbox max_lat must be between -90 and 90.' )
			
			if min_lon >= max_lon:
				raise ValueError( 'bbox min_lon must be less than max_lon.' )
			
			if min_lat >= max_lat:
				raise ValueError( 'bbox min_lat must be less than max_lat.' )
			
			return ','.join( [ str( number ) for number in numbers ] )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = 'validate_bbox( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_date_pair( self, start_date: str = '', end_date: str = '' ) -> Tuple[ str, str ]:
		"""Validate date pair.
		
		Purpose:
			Validates and normalizes date pair before it is used in NASA EONET environmental event
			data. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			start_date (str): start date value used by the validate date pair operation.
			end_date (str): end date value used by the validate date pair operation.
		
		Returns:
			Tuple[str, str]: Validated date pair value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			start_value = str( start_date or '' ).strip( )
			end_value = str( end_date or '' ).strip( )
			
			if bool( start_value ) != bool( end_value ):
				raise ValueError(
					'start_date and end_date must either both be supplied or both be blank.'
				)
			
			if start_value and end_value and start_value > end_value:
				raise ValueError( 'start_date must be on or before end_date.' )
			
			return start_value, end_value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = (
					'validate_date_pair( self, *args, **kwargs ) -> Tuple[ str, str ]'
			)
			raise exception
	
	def shape_event_rows( self,
			records: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape event rows.
		
		Purpose:
			Transforms raw provider records into event rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			records (List[Dict[str, Any]]): records value used by the shape event rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in records or [ ]:
				categories = item.get( 'categories', [ ] ) or [ ]
				sources = item.get( 'sources', [ ] ) or [ ]
				geometry = item.get( 'geometry', [ ] ) or [ ]
				last_geometry = geometry[ -1 ] if geometry else { }
				coordinates = last_geometry.get( 'coordinates', [ ] ) or [ ]
				geometry_type = str( last_geometry.get( 'type', '' ) or '' )
				latitude = None
				longitude = None
				
				if geometry_type.lower( ) == 'point' and isinstance( coordinates, list ):
					longitude = coordinates[ 0 ] if len( coordinates ) > 0 else None
					latitude = coordinates[ 1 ] if len( coordinates ) > 1 else None
				
				category_titles = ', '.join(
					[
							str( category.get( 'title', category.get( 'id', '' ) ) )
							for category in categories
							if isinstance( category, dict )
					]
				)
				source_ids = ', '.join(
					[
							str( source.get( 'id', source.get( 'title', '' ) ) )
							for source in sources
							if isinstance( source, dict )
					]
				)
				closed_date = str( item.get( 'closed', '' ) or '' )
				status = 'closed' if closed_date else 'open'
				
				rows.append(
					{
							'Id': item.get( 'id', '' ),
							'Title': item.get( 'title', '' ),
							'Status': status,
							'Closed Date': closed_date,
							'Categories': category_titles,
							'Sources': source_ids,
							'Geometry Count': len( geometry ),
							'Last Geometry Type': geometry_type,
							'Last Geometry Date': last_geometry.get( 'date', '' ),
							'Latitude': latitude,
							'Longitude': longitude,
							'Link': item.get( 'link', '' ),
							'Description': item.get( 'description', '' )
					}
				)
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = (
					'shape_event_rows( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_category_rows( self,
			records: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape category rows.
		
		Purpose:
			Transforms raw provider records into category rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			records (List[Dict[str, Any]]): records value used by the shape category rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in records or [ ]:
				rows.append(
					{
							'Id': item.get( 'id', '' ),
							'Title': item.get( 'title', '' ),
							'Description': item.get( 'description', '' ),
							'Link': item.get( 'link', '' )
					}
				)
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = (
					'shape_category_rows( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def summarize_rows( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Summarize rows.
		
		Purpose:
			Performs the summarize rows operation for NASA EONET environmental event data. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the summarize rows operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			count = len( rows or [ ] )
			open_count = 0
			first_title = ''
			first_categories = ''
			
			for row in rows or [ ]:
				if str( row.get( 'Status', '' ) ).lower( ) == 'open':
					open_count += 1
			
			if rows:
				first_title = str( rows[ 0 ].get( 'Title', '' ) or '' )
				first_categories = str( rows[ 0 ].get( 'Categories', '' ) or '' )
			
			return {
					'count': count,
					'open_count': open_count,
					'first_title': first_title,
					'first_categories': first_categories
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = (
					'summarize_rows( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def package_response( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the package response operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'summary': self.summarize_rows( rows ),
					'rows': rows,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = (
					'package_response( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def request( self, endpoint: str, params: Optional[ Dict[ str, Any ] ] = None,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Request NASA EONET environmental event data.
		
		Purpose:
			Sends a provider request for NASA EONET environmental event data after request
			parameters have been validated or prepared by the caller. The method stores request,
			response, and payload state on the instance so subsequent methods can package or inspect
			the result consistently.
		
		Args:
			endpoint (str): endpoint value used by the request operation.
			params (Optional[Dict[str, Any]]): Request or schema parameter dictionary used by the
				operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'endpoint', endpoint )
			throw_if( 'time', time )
			
			self.endpoint = self.validate_endpoint( endpoint )
			self.timeout = int( time )
			self.url = f'{self.base_url}/{self.endpoint}'
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			for key, value in (params or { }).items( ):
				if value is None:
					continue
				
				if isinstance( value, str ) and not value.strip( ):
					continue
				
				self.params[ key ] = value
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.json( ) or { }
			self.result = {
					'url': self.response.url,
					'params': self.params,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = (
					'request( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_events( self, source: str = '', category: str = '',
			status: str = 'open', limit: int = 25, days: int = 30,
			start_date: str = '', end_date: str = '', bbox: str = '',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch events.
		
		Purpose:
			Retrieves events using validated arguments and the stored EoNet runtime configuration.
			The method assembles request parameters, executes the provider call or dispatches to a
			specialized helper, records response state when applicable, and returns a normalized
			payload for downstream analysis or tool execution.
		
		Args:
			source (str): source value used by the fetch events operation.
			category (str): category value used by the fetch events operation.
			status (str): status value used by the fetch events operation.
			limit (int): limit value used by the fetch events operation.
			days (int): days value used by the fetch events operation.
			start_date (str): start date value used by the fetch events operation.
			end_date (str): end date value used by the fetch events operation.
			bbox (str): bbox value used by the fetch events operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'status', status )
			throw_if( 'limit', limit )
			throw_if( 'days', days )
			throw_if( 'time', time )
			
			self.mode = 'events'
			self.source = str( source or '' ).strip( )
			self.category = str( category or '' ).strip( )
			self.status = self.validate_status( status )
			self.limit = self.validate_limit( limit )
			self.days = self.validate_days( days )
			self.start_date, self.end_date = self.validate_date_pair(
				start_date=start_date,
				end_date=end_date
			)
			self.bbox = self.validate_bbox( bbox )
			self.timeout = int( time )
			
			self.request(
				endpoint='events',
				params={
						'source': self.source,
						'category': self.category,
						'status': self.status,
						'limit': self.limit,
						'days': self.days,
						'start': self.start_date,
						'end': self.end_date,
						'bbox': self.bbox
				},
				time=self.timeout
			)
			
			records = (
					self.payload.get( 'events', [ ] )
					if isinstance( self.payload, dict )
					else [ ]
			)
			rows = self.shape_event_rows( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = (
					'fetch_events( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_categories( self, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch categories.
		
		Purpose:
			Retrieves categories using validated arguments and the stored EoNet runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'time', time )
			
			self.mode = 'categories'
			self.timeout = int( time )
			
			self.request(
				endpoint='categories',
				params={ },
				time=self.timeout
			)
			
			records = (
					self.payload.get( 'categories', [ ] )
					if isinstance( self.payload, dict )
					else [ ]
			)
			rows = self.shape_category_rows( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = (
					'fetch_categories( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'events', source: str = '', category: str = '',
			status: str = 'open', limit: int = 25, days: int = 30,
			start_date: str = '', end_date: str = '', bbox: str = '',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch NASA EONET environmental event data.
		
		Purpose:
			Retrieves NASA EONET environmental event data using validated arguments and the stored
			EoNet runtime configuration. The method assembles request parameters, executes the
			provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			source (str): source value used by the fetch operation.
			category (str): category value used by the fetch operation.
			status (str): status value used by the fetch operation.
			limit (int): limit value used by the fetch operation.
			days (int): days value used by the fetch operation.
			start_date (str): start date value used by the fetch operation.
			end_date (str): end date value used by the fetch operation.
			bbox (str): bbox value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			self.mode = str( mode or 'events' ).strip( ).lower( )
			
			if self.mode == 'events':
				return self.fetch_events(
					source=source,
					category=category,
					status=status,
					limit=limit,
					days=days,
					start_date=start_date,
					end_date=end_date,
					bbox=bbox,
					time=time
				)
			
			if self.mode == 'categories':
				return self.fetch_categories(
					time=time
				)
			
			raise ValueError( "Unsupported EONET mode. Use 'events' or 'categories'." )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if not isinstance( parameters, dict ):
				raise ValueError(
					'parameters must be a dict of param_name -> schema definition.'
				)
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EoNet'
			exception.method = 'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			raise exception

class EnviroFacts( Fetcher ):
	"""Enviro Facts fetcher.
	
	Purpose:
		Coordinates EPA Envirofacts table and facility records within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		table_name (Optional[str]): table name state retained by the instance.
		state_code (Optional[str]): state code state retained by the instance.
		facility_name (Optional[str]): facility name state retained by the instance.
		limit (Optional[int]): limit state retained by the instance.
		path (Optional[str]): path state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	mode: Optional[ str ]
	table_name: Optional[ str ]
	state_code: Optional[ str ]
	facility_name: Optional[ str ]
	limit: Optional[ int ]
	path: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize EnviroFacts.
		
		Purpose:
			Initializes the EnviroFacts instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://data.epa.gov/efservice'
		self.mode = 'table'
		self.table_name = 'TRI_FACILITY'
		self.state_code = ''
		self.facility_name = ''
		self.limit = 25
		self.path = ''
		self.params = { }
		self.payload = [ ]
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'mode',
				'table_name',
				'state_code',
				'facility_name',
				'limit',
				'path',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'validate_table_name',
				'validate_state_code',
				'validate_limit',
				'resolve_table_path',
				'shape_rows',
				'summarize_rows',
				'package_response',
				'request',
				'fetch_table',
				'fetch',
				'create_schema'
		]
	
	def validate_table_name( self, table_name: str ) -> str:
		"""Validate table name.
		
		Purpose:
			Validates and normalizes table name before it is used in EPA Envirofacts table and
			facility records. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			table_name (str): table name value used by the validate table name operation.
		
		Returns:
			str: Validated table name value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'table_name', table_name )
			
			value = str( table_name ).strip( ).upper( )
			allowed = {
					'TRI_FACILITY',
					'TRI_RELEASE',
					'EF_W_EMISSIONS_SOURCE_GHG'
			}
			
			if value not in allowed:
				raise ValueError(
					'Unsupported Envirofacts table. Use TRI_FACILITY, TRI_RELEASE, '
					'or EF_W_EMISSIONS_SOURCE_GHG.'
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EnviroFacts'
			exception.method = 'validate_table_name( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_state_code( self, state_code: str = '' ) -> str:
		"""Validate state code.
		
		Purpose:
			Validates and normalizes state code before it is used in EPA Envirofacts table and
			facility records. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			state_code (str): state code value used by the validate state code operation.
		
		Returns:
			str: Validated state code value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( state_code or '' ).strip( ).upper( )
			
			if not value:
				return ''
			
			if not re.fullmatch( r'[A-Z]{2}', value ):
				raise ValueError( 'state_code must be blank or a two-letter code.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EnviroFacts'
			exception.method = 'validate_state_code( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_limit( self, limit: int ) -> int:
		"""Validate limit.
		
		Purpose:
			Validates and normalizes limit before it is used in EPA Envirofacts table and facility
			records. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			limit (int): limit value used by the validate limit operation.
		
		Returns:
			int: Validated limit value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'limit', limit )
			
			value = int( limit )
			if value < 1 or value > 500:
				raise ValueError( 'limit must be between 1 and 500.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EnviroFacts'
			exception.method = 'validate_limit( self, *args, **kwargs ) -> int'
			raise exception
	
	def resolve_table_path( self, table_name: str, state_code: str = '',
			facility_name: str = '', limit: int = 25 ) -> str:
		"""Resolve table path.
		
		Purpose:
			Performs the resolve table path operation for EPA Envirofacts table and facility
			records. The method uses the class runtime state and supplied arguments to prepare,
			transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			table_name (str): table name value used by the resolve table path operation.
			state_code (str): state code value used by the resolve table path operation.
			facility_name (str): facility name value used by the resolve table path operation.
			limit (int): limit value used by the resolve table path operation.
		
		Returns:
			str: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.table_name = self.validate_table_name( table_name )
			self.state_code = self.validate_state_code( state_code )
			self.facility_name = str( facility_name or '' ).strip( )
			self.limit = self.validate_limit( limit )
			
			segments: List[ str ] = [
					self.table_name
			]
			
			if self.state_code:
				if self.table_name == 'EF_W_EMISSIONS_SOURCE_GHG':
					segments.extend(
						[
								'STATE',
								self.state_code
						]
					)
				else:
					segments.extend(
						[
								'ST',
								self.state_code
						]
					)
			
			if self.facility_name:
				if self.table_name == 'EF_W_EMISSIONS_SOURCE_GHG':
					segments.extend(
						[
								'FACILITY_NAME',
								self.facility_name
						]
					)
				else:
					segments.extend(
						[
								'FACILITY_NAME',
								self.facility_name
						]
					)
			
			segments.extend(
				[
						'ROWS',
						str( self.limit ),
						'JSON'
				]
			)
			
			self.path = '/'.join(
				[
						urllib.parse.quote( str( segment ), safe='' )
						for segment in segments
				]
			)
			
			return self.path
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EnviroFacts'
			exception.method = (
					'resolve_table_path( self, *args, **kwargs ) -> str'
			)
			raise exception
	
	def shape_rows( self, records: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape rows.
		
		Purpose:
			Transforms raw provider records into rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			records (List[Dict[str, Any]]): records value used by the shape rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in records or [ ]:
				if not isinstance( item, dict ):
					continue
				
				row: Dict[ str, Any ] = { }
				
				for key, value in item.items( ):
					friendly_key = str( key ).replace( '_', ' ' ).title( )
					row[ friendly_key ] = value
				
				rows.append( row )
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EnviroFacts'
			exception.method = (
					'shape_rows( self, *args, **kwargs ) -> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def summarize_rows( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Summarize rows.
		
		Purpose:
			Performs the summarize rows operation for EPA Envirofacts table and facility records.
			The method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the summarize rows operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			count = len( rows or [ ] )
			first_facility = ''
			first_state = ''
			
			if rows:
				first_facility = str(
					rows[ 0 ].get( 'Facility Name', '' )
					or rows[ 0 ].get( 'Primary Name', '' )
					or rows[ 0 ].get( 'Name', '' )
					or ''
				)
				
				first_state = str(
					rows[ 0 ].get( 'State', '' )
					or rows[ 0 ].get( 'State Abbr', '' )
					or rows[ 0 ].get( 'St', '' )
					or ''
				)
			
			return {
					'count': count,
					'first_facility': first_facility,
					'first_state': first_state
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EnviroFacts'
			exception.method = (
					'summarize_rows( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def package_response( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the package response operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.result = {
					'mode': self.mode,
					'table_name': self.table_name,
					'url': self.url,
					'params': self.params,
					'summary': self.summarize_rows( rows ),
					'rows': rows,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EnviroFacts'
			exception.method = (
					'package_response( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def request( self, url: str, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Request EPA Envirofacts table and facility records.
		
		Purpose:
			Sends a provider request for EPA Envirofacts table and facility records after request
			parameters have been validated or prepared by the caller. The method stores request,
			response, and payload state on the instance so subsequent methods can package or inspect
			the result consistently.
		
		Args:
			url (str): URL or URI value used as the request or parsing source.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'url', url )
			throw_if( 'time', time )
			
			self.url = str( url ).strip( )
			self.timeout = int( time )
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			self.response = requests.get(
				url=self.url,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.json( )
			self.result = {
					'url': self.url,
					'params': self.params,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EnviroFacts'
			exception.method = (
					'request( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_table( self, table_name: str, state_code: str = '',
			facility_name: str = '', limit: int = 25,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch table.
		
		Purpose:
			Retrieves table using validated arguments and the stored EnviroFacts runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			table_name (str): table name value used by the fetch table operation.
			state_code (str): state code value used by the fetch table operation.
			facility_name (str): facility name value used by the fetch table operation.
			limit (int): limit value used by the fetch table operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'table_name', table_name )
			throw_if( 'limit', limit )
			throw_if( 'time', time )
			
			self.mode = 'table'
			self.path = self.resolve_table_path(
				table_name=table_name,
				state_code=state_code,
				facility_name=facility_name,
				limit=limit
			)
			self.params = {
					'table_name': self.table_name,
					'state_code': self.state_code,
					'facility_name': self.facility_name,
					'limit': self.limit
			}
			
			self.request(
				url=f'{self.base_url}/{self.path}',
				time=int( time )
			)
			
			records = self.payload if isinstance( self.payload, list ) else [ ]
			rows = self.shape_rows( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EnviroFacts'
			exception.method = (
					'fetch_table( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, table_name: str = 'TRI_FACILITY', state_code: str = '',
			facility_name: str = '', limit: int = 25,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch EPA Envirofacts table and facility records.
		
		Purpose:
			Retrieves EPA Envirofacts table and facility records using validated arguments and the
			stored EnviroFacts runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			table_name (str): table name value used by the fetch operation.
			state_code (str): state code value used by the fetch operation.
			facility_name (str): facility name value used by the fetch operation.
			limit (int): limit value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			return self.fetch_table(
				table_name=table_name,
				state_code=state_code,
				facility_name=facility_name,
				limit=limit,
				time=time
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EnviroFacts'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if not isinstance( parameters, dict ):
				raise ValueError(
					'parameters must be a dict of param_name -> schema definition.'
				)
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'EnviroFacts'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class TidesAndCurrents( Fetcher ):
	"""Tides And Currents fetcher.
	
	Purpose:
		Coordinates NOAA tides, currents, and station data within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		data_url (Optional[str]): data URL state retained by the instance.
		metadata_url (Optional[str]): metadata URL state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		station_id (Optional[str]): station ID state retained by the instance.
		begin_date (Optional[str]): begin date state retained by the instance.
		end_date (Optional[str]): end date state retained by the instance.
		datum (Optional[str]): datum state retained by the instance.
		units (Optional[str]): units state retained by the instance.
		time_zone (Optional[str]): time zone state retained by the instance.
		interval (Optional[str]): interval state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	data_url: Optional[ str ]
	metadata_url: Optional[ str ]
	mode: Optional[ str ]
	station_id: Optional[ str ]
	begin_date: Optional[ str ]
	end_date: Optional[ str ]
	datum: Optional[ str ]
	units: Optional[ str ]
	time_zone: Optional[ str ]
	interval: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize TidesAndCurrents.
		
		Purpose:
			Initializes the TidesAndCurrents instance with default configuration, request state,
			response placeholders, and provider-specific options. The constructor prepares the
			object for later method calls without executing an external provider request."""
		super( ).__init__( )
		self.data_url = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter'
		self.metadata_url = 'https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi'
		self.mode = 'water-level'
		self.station_id = ''
		self.begin_date = ''
		self.end_date = ''
		self.datum = 'MLLW'
		self.units = 'metric'
		self.time_zone = 'gmt'
		self.interval = 'hilo'
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'data_url',
				'metadata_url',
				'mode',
				'station_id',
				'begin_date',
				'end_date',
				'datum',
				'units',
				'time_zone',
				'interval',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'validate_mode',
				'validate_station_id',
				'validate_date_range',
				'validate_datum',
				'validate_units',
				'validate_time_zone',
				'validate_interval',
				'shape_station_rows',
				'shape_data_rows',
				'summarize_rows',
				'package_response',
				'request',
				'fetch_station',
				'fetch_water_level',
				'fetch_tide_predictions',
				'fetch',
				'create_schema'
		]
	
	def validate_mode( self, mode: str ) -> str:
		"""Validate mode.
		
		Purpose:
			Validates and normalizes mode before it is used in NOAA tides, currents, and station
			data. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			mode (str): mode value used by the validate mode operation.
		
		Returns:
			str: Validated mode value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			value = str( mode ).strip( ).lower( )
			allowed = {
					'station',
					'water-level',
					'tide-predictions'
			}
			
			if value not in allowed:
				raise ValueError(
					"Unsupported NOAA Tides & Currents mode. Use 'station', "
					"'water-level', or 'tide-predictions'."
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = 'validate_mode( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_station_id( self, station_id: str ) -> str:
		"""Validate station id.
		
		Purpose:
			Validates and normalizes station id before it is used in NOAA tides, currents, and
			station data. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			station_id (str): station ID value used by the validate station id operation.
		
		Returns:
			str: Validated station id value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'station_id', station_id )
			
			value = str( station_id ).strip( )
			
			if not re.fullmatch( r'[A-Za-z0-9_-]{3,20}', value ):
				raise ValueError(
					'station_id must contain 3 to 20 letters, digits, underscores, '
					'or hyphens.'
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = 'validate_station_id( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_date_range( self, begin_date: str, end_date: str ) -> Tuple[ str, str ]:
		"""Validate date range.
		
		Purpose:
			Validates and normalizes date range before it is used in NOAA tides, currents, and
			station data. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			begin_date (str): begin date value used by the validate date range operation.
			end_date (str): end date value used by the validate date range operation.
		
		Returns:
			Tuple[str, str]: Validated date range value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'begin_date', begin_date )
			throw_if( 'end_date', end_date )
			
			begin_value = str( begin_date ).strip( )
			end_value = str( end_date ).strip( )
			
			if not re.fullmatch( r'\d{8}', begin_value ):
				raise ValueError( 'begin_date must use YYYYMMDD format.' )
			
			if not re.fullmatch( r'\d{8}', end_value ):
				raise ValueError( 'end_date must use YYYYMMDD format.' )
			
			if begin_value > end_value:
				raise ValueError( 'begin_date must be on or before end_date.' )
			
			return begin_value, end_value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = (
					'validate_date_range( self, *args, **kwargs ) -> Tuple[ str, str ]'
			)
			raise exception
	
	def validate_datum( self, datum: str ) -> str:
		"""Validate datum.
		
		Purpose:
			Validates and normalizes datum before it is used in NOAA tides, currents, and station
			data. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			datum (str): datum value used by the validate datum operation.
		
		Returns:
			str: Validated datum value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'datum', datum )
			
			value = str( datum ).strip( ).upper( )
			allowed = {
					'MLLW',
					'MHHW',
					'MHW',
					'MTL',
					'MSL',
					'MLW',
					'NAVD',
					'STND'
			}
			
			if value not in allowed:
				raise ValueError(
					'datum must be one of MLLW, MHHW, MHW, MTL, MSL, MLW, NAVD, '
					'or STND.'
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = 'validate_datum( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_units( self, units: str ) -> str:
		"""Validate units.
		
		Purpose:
			Validates and normalizes units before it is used in NOAA tides, currents, and station
			data. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			units (str): units value used by the validate units operation.
		
		Returns:
			str: Validated units value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'units', units )
			
			value = str( units ).strip( ).lower( )
			allowed = {
					'metric',
					'english'
			}
			
			if value not in allowed:
				raise ValueError( "units must be 'metric' or 'english'." )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = 'validate_units( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_time_zone( self, time_zone: str ) -> str:
		"""Validate time zone.
		
		Purpose:
			Validates and normalizes time zone before it is used in NOAA tides, currents, and
			station data. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			time_zone (str): time zone value used by the validate time zone operation.
		
		Returns:
			str: Validated time zone value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'time_zone', time_zone )
			
			value = str( time_zone ).strip( ).lower( )
			allowed = {
					'gmt',
					'lst',
					'lst_ldt'
			}
			
			if value not in allowed:
				raise ValueError( "time_zone must be 'gmt', 'lst', or 'lst_ldt'." )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = 'validate_time_zone( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_interval( self, interval: str ) -> str:
		"""Validate interval.
		
		Purpose:
			Validates and normalizes interval before it is used in NOAA tides, currents, and station
			data. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			interval (str): interval value used by the validate interval operation.
		
		Returns:
			str: Validated interval value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'interval', interval )
			
			value = str( interval ).strip( ).lower( )
			allowed = {
					'hilo',
					'h',
					'1',
					'5',
					'6',
					'10',
					'15',
					'30',
					'60'
			}
			
			if value not in allowed:
				raise ValueError(
					"interval must be one of 'hilo', 'h', '1', '5', '6', '10', "
					"'15', '30', or '60'."
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = 'validate_interval( self, *args, **kwargs ) -> str'
			raise exception
	
	def shape_station_rows( self, payload: Dict[ str, Any ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape station rows.
		
		Purpose:
			Transforms raw provider records into station rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			payload (Dict[str, Any]): payload value used by the shape station rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			station = payload.get( 'stations', None ) if isinstance( payload, dict ) else None
			
			if isinstance( station, list ) and station:
				station = station[ 0 ]
			
			if not isinstance( station, dict ):
				station = payload if isinstance( payload, dict ) else { }
			
			row: Dict[ str, Any ] = {
					'Station Id': station.get( 'id', '' ),
					'Name': station.get( 'name', '' ),
					'State': station.get( 'state', '' ),
					'Latitude': station.get( 'lat', '' ),
					'Longitude': station.get( 'lng', '' ),
					'Time Zone': station.get( 'timezone', '' ),
					'Great Lakes': station.get( 'greatlakes', '' ),
					'Shef Id': station.get( 'shefcode', '' ),
					'Details Link': station.get( 'self', '' )
			}
			
			return [ row ]
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = (
					'shape_station_rows( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_data_rows( self, payload: Dict[ str, Any ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape data rows.
		
		Purpose:
			Transforms raw provider records into data rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			payload (Dict[str, Any]): payload value used by the shape data rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			if not isinstance( payload, dict ):
				return rows
			
			records = payload.get( 'data', None )
			
			if records is None:
				records = payload.get( 'predictions', [ ] )
			
			for item in records or [ ]:
				if not isinstance( item, dict ):
					continue
				
				row: Dict[ str, Any ] = { }
				
				for key, value in item.items( ):
					friendly_key = str( key ).replace( '_', ' ' ).title( )
					row[ friendly_key ] = value
				
				rows.append( row )
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = (
					'shape_data_rows( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def summarize_rows( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Summarize rows.
		
		Purpose:
			Performs the summarize rows operation for NOAA tides, currents, and station data. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the summarize rows operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			count = len( rows or [ ] )
			first_station = ''
			first_value = ''
			first_time = ''
			
			if rows:
				first_station = str(
					rows[ 0 ].get( 'Name', '' )
					or rows[ 0 ].get( 'Station Id', '' )
					or self.station_id
					or ''
				)
				first_value = str(
					rows[ 0 ].get( 'V', '' )
					or rows[ 0 ].get( 'Value', '' )
					or rows[ 0 ].get( 'Prediction', '' )
					or rows[ 0 ].get( 'Predicted Wl', '' )
					or ''
				)
				first_time = str(
					rows[ 0 ].get( 'T', '' )
					or rows[ 0 ].get( 'Time', '' )
					or rows[ 0 ].get( 'Date Time', '' )
					or ''
				)
			
			return {
					'count': count,
					'first_station': first_station,
					'first_value': first_value,
					'first_time': first_time
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = (
					'summarize_rows( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def package_response( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the package response operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.result = {
					'mode': self.mode,
					'station_id': self.station_id,
					'url': self.url,
					'params': self.params,
					'summary': self.summarize_rows( rows ),
					'rows': rows,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = (
					'package_response( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def request( self, url: str, params: Optional[ Dict[ str, Any ] ] = None,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Request NOAA tides, currents, and station data.
		
		Purpose:
			Sends a provider request for NOAA tides, currents, and station data after request
			parameters have been validated or prepared by the caller. The method stores request,
			response, and payload state on the instance so subsequent methods can package or inspect
			the result consistently.
		
		Args:
			url (str): URL or URI value used as the request or parsing source.
			params (Optional[Dict[str, Any]]): Request or schema parameter dictionary used by the
				operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'url', url )
			throw_if( 'time', time )
			
			self.url = str( url ).strip( )
			self.timeout = int( time )
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			for key, value in (params or { }).items( ):
				if value is None:
					continue
				
				if isinstance( value, str ) and not value.strip( ):
					continue
				
				self.params[ key ] = value
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.json( ) or { }
			self.result = {
					'url': self.response.url,
					'params': self.params,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = (
					'request( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_station( self, station_id: str,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch station.
		
		Purpose:
			Retrieves station using validated arguments and the stored TidesAndCurrents runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			station_id (str): station ID value used by the fetch station operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'station_id', station_id )
			throw_if( 'time', time )
			
			self.mode = 'station'
			self.station_id = self.validate_station_id( station_id )
			self.timeout = int( time )
			
			self.request(
				url=f'{self.metadata_url}/stations/{self.station_id}.json',
				params={ },
				time=self.timeout
			)
			
			rows = self.shape_station_rows( self.payload )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = (
					'fetch_station( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_water_level( self, station_id: str, begin_date: str,
			end_date: str, datum: str = 'MLLW', units: str = 'metric',
			time_zone: str = 'gmt', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch water level.
		
		Purpose:
			Retrieves water level using validated arguments and the stored TidesAndCurrents runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			station_id (str): station ID value used by the fetch water level operation.
			begin_date (str): begin date value used by the fetch water level operation.
			end_date (str): end date value used by the fetch water level operation.
			datum (str): datum value used by the fetch water level operation.
			units (str): units value used by the fetch water level operation.
			time_zone (str): time zone value used by the fetch water level operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'station_id', station_id )
			throw_if( 'begin_date', begin_date )
			throw_if( 'end_date', end_date )
			throw_if( 'time', time )
			
			self.mode = 'water-level'
			self.station_id = self.validate_station_id( station_id )
			self.begin_date, self.end_date = self.validate_date_range(
				begin_date,
				end_date
			)
			self.datum = self.validate_datum( datum )
			self.units = self.validate_units( units )
			self.time_zone = self.validate_time_zone( time_zone )
			self.timeout = int( time )
			
			self.request(
				url=self.data_url,
				params={
						'product': 'water_level',
						'application': 'Foo',
						'station': self.station_id,
						'begin_date': self.begin_date,
						'end_date': self.end_date,
						'datum': self.datum,
						'units': self.units,
						'time_zone': self.time_zone,
						'format': 'json'
				},
				time=self.timeout
			)
			
			rows = self.shape_data_rows( self.payload )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = (
					'fetch_water_level( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_tide_predictions( self, station_id: str, begin_date: str,
			end_date: str, datum: str = 'MLLW', units: str = 'metric',
			time_zone: str = 'gmt', interval: str = 'hilo',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch tide predictions.
		
		Purpose:
			Retrieves tide predictions using validated arguments and the stored TidesAndCurrents
			runtime configuration. The method assembles request parameters, executes the provider
			call or dispatches to a specialized helper, records response state when applicable, and
			returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			station_id (str): station ID value used by the fetch tide predictions operation.
			begin_date (str): begin date value used by the fetch tide predictions operation.
			end_date (str): end date value used by the fetch tide predictions operation.
			datum (str): datum value used by the fetch tide predictions operation.
			units (str): units value used by the fetch tide predictions operation.
			time_zone (str): time zone value used by the fetch tide predictions operation.
			interval (str): interval value used by the fetch tide predictions operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'station_id', station_id )
			throw_if( 'begin_date', begin_date )
			throw_if( 'end_date', end_date )
			throw_if( 'time', time )
			
			self.mode = 'tide-predictions'
			self.station_id = self.validate_station_id( station_id )
			self.begin_date, self.end_date = self.validate_date_range(
				begin_date,
				end_date
			)
			self.datum = self.validate_datum( datum )
			self.units = self.validate_units( units )
			self.time_zone = self.validate_time_zone( time_zone )
			self.interval = self.validate_interval( interval )
			self.timeout = int( time )
			
			self.request(
				url=self.data_url,
				params={
						'product': 'predictions',
						'application': 'Foo',
						'station': self.station_id,
						'begin_date': self.begin_date,
						'end_date': self.end_date,
						'datum': self.datum,
						'units': self.units,
						'time_zone': self.time_zone,
						'interval': self.interval,
						'format': 'json'
				},
				time=self.timeout
			)
			
			rows = self.shape_data_rows( self.payload )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = (
					'fetch_tide_predictions( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'water-level', station_id: str = '',
			begin_date: str = '', end_date: str = '', datum: str = 'MLLW',
			units: str = 'metric', time_zone: str = 'gmt',
			interval: str = 'hilo', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch NOAA tides, currents, and station data.
		
		Purpose:
			Retrieves NOAA tides, currents, and station data using validated arguments and the
			stored TidesAndCurrents runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			station_id (str): station ID value used by the fetch operation.
			begin_date (str): begin date value used by the fetch operation.
			end_date (str): end date value used by the fetch operation.
			datum (str): datum value used by the fetch operation.
			units (str): units value used by the fetch operation.
			time_zone (str): time zone value used by the fetch operation.
			interval (str): interval value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = self.validate_mode( mode )
			
			if self.mode == 'station':
				return self.fetch_station(
					station_id=station_id,
					time=time
				)
			
			if self.mode == 'water-level':
				return self.fetch_water_level(
					station_id=station_id,
					begin_date=begin_date,
					end_date=end_date,
					datum=datum,
					units=units,
					time_zone=time_zone,
					time=time
				)
			
			if self.mode == 'tide-predictions':
				return self.fetch_tide_predictions(
					station_id=station_id,
					begin_date=begin_date,
					end_date=end_date,
					datum=datum,
					units=units,
					time_zone=time_zone,
					interval=interval,
					time=time
				)
			
			raise ValueError(
				"Unsupported mode. Use 'station', 'water-level', or "
				"'tide-predictions'."
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if not isinstance( parameters, dict ):
				raise ValueError(
					'parameters must be a dict of param_name -> schema definition.'
				)
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'TidesAndCurrents'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class UvIndex( Fetcher ):
	"""UV Index fetcher.
	
	Purpose:
		Coordinates EPA UV Index current and forecast data within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		zip_code (Optional[str]): zip code state retained by the instance.
		city (Optional[str]): city state retained by the instance.
		state (Optional[str]): state state retained by the instance.
		endpoint (Optional[str]): endpoint state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	mode: Optional[ str ]
	zip_code: Optional[ str ]
	city: Optional[ str ]
	state: Optional[ str ]
	endpoint: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize UvIndex.
		
		Purpose:
			Initializes the UvIndex instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://enviro.epa.gov/enviro/efservice'
		self.mode = 'daily-zip'
		self.zip_code = ''
		self.city = ''
		self.state = ''
		self.endpoint = ''
		self.params = { }
		self.payload = [ ]
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'mode',
				'zip_code',
				'city',
				'state',
				'endpoint',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'validate_mode',
				'validate_zip_code',
				'validate_city',
				'validate_state',
				'shape_rows',
				'summarize_rows',
				'package_response',
				'request',
				'fetch_daily_zip',
				'fetch_daily_city_state',
				'fetch_hourly_zip',
				'fetch_hourly_city_state',
				'fetch',
				'create_schema'
		]
	
	def validate_mode( self, mode: str ) -> str:
		"""Validate mode.
		
		Purpose:
			Validates and normalizes mode before it is used in EPA UV Index current and forecast
			data. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			mode (str): mode value used by the validate mode operation.
		
		Returns:
			str: Validated mode value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			value = str( mode ).strip( ).lower( )
			allowed = {
					'daily-zip',
					'daily-city-state',
					'hourly-zip',
					'hourly-city-state'
			}
			
			if value not in allowed:
				raise ValueError(
					"Unsupported EPA UV Index mode. Use 'daily-zip', "
					"'daily-city-state', 'hourly-zip', or 'hourly-city-state'."
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = 'validate_mode( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_zip_code( self, zip_code: str ) -> str:
		"""Validate zip code.
		
		Purpose:
			Validates and normalizes zip code before it is used in EPA UV Index current and forecast
			data. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			zip_code (str): zip code value used by the validate zip code operation.
		
		Returns:
			str: Validated zip code value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'zip_code', zip_code )
			
			value = str( zip_code ).strip( )
			
			if not re.fullmatch( r'\d{5}(?:-\d{4})?', value ):
				raise ValueError( 'zip_code must be a valid 5-digit ZIP or ZIP+4 value.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = 'validate_zip_code( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_city( self, city: str ) -> str:
		"""Validate city.
		
		Purpose:
			Validates and normalizes city before it is used in EPA UV Index current and forecast
			data. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			city (str): city value used by the validate city operation.
		
		Returns:
			str: Validated city value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'city', city )
			
			value = str( city ).strip( )
			
			if not value:
				raise ValueError( 'city cannot be empty.' )
			
			if '/' in value or '\\' in value:
				raise ValueError( 'city cannot contain path separators.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = 'validate_city( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_state( self, state: str ) -> str:
		"""Validate state.
		
		Purpose:
			Validates and normalizes state before it is used in EPA UV Index current and forecast
			data. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			state (str): state value used by the validate state operation.
		
		Returns:
			str: Validated state value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'state', state )
			
			value = str( state ).strip( ).upper( )
			
			if not re.fullmatch( r'[A-Z]{2}', value ):
				raise ValueError( 'state must be a two-letter abbreviation.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = 'validate_state( self, *args, **kwargs ) -> str'
			raise exception
	
	def shape_rows( self, records: List[ Dict[ str, Any ] ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape rows.
		
		Purpose:
			Transforms raw provider records into rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			records (List[Dict[str, Any]]): records value used by the shape rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in records or [ ]:
				if not isinstance( item, dict ):
					continue
				
				row: Dict[ str, Any ] = { }
				
				for key, value in item.items( ):
					friendly_key = str( key ).replace( '_', ' ' ).title( )
					row[ friendly_key ] = value
				
				rows.append( row )
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = (
					'shape_rows( self, *args, **kwargs ) -> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def summarize_rows( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Summarize rows.
		
		Purpose:
			Performs the summarize rows operation for EPA UV Index current and forecast data. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the summarize rows operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			count = len( rows or [ ] )
			max_uv = None
			first_location = ''
			first_alert = ''
			
			for row in rows or [ ]:
				if not first_location:
					first_location = str(
						row.get( 'City', '' )
						or row.get( 'Zip', '' )
						or row.get( 'State', '' )
						or ''
					)
				
				if not first_alert:
					first_alert = str(
						row.get( 'Uv Alert', '' )
						or row.get( 'Alert', '' )
						or ''
					)
				
				uv_value = (
						row.get( 'Uv Value', None )
						or row.get( 'Index', None )
						or row.get( 'Uv Index', None )
				)
				
				try:
					if uv_value is not None and str( uv_value ).strip( ):
						if max_uv is None or float( uv_value ) > float( max_uv ):
							max_uv = float( uv_value )
				except Exception:
					pass
			
			return {
					'count': count,
					'max_uv': max_uv,
					'first_location': first_location,
					'first_alert': first_alert
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = (
					'summarize_rows( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def package_response( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the package response operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'summary': self.summarize_rows( rows ),
					'rows': rows,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = (
					'package_response( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def request( self, url: str, params: Dict[ str, Any ],
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Request EPA UV Index current and forecast data.
		
		Purpose:
			Sends a provider request for EPA UV Index current and forecast data after request
			parameters have been validated or prepared by the caller. The method stores request,
			response, and payload state on the instance so subsequent methods can package or inspect
			the result consistently.
		
		Args:
			url (str): URL or URI value used as the request or parsing source.
			params (Dict[str, Any]): Request or schema parameter dictionary used by the operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'url', url )
			throw_if( 'params', params )
			throw_if( 'time', time )
			
			self.url = str( url ).strip( )
			self.params = params
			self.timeout = int( time )
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			self.response = requests.get(
				url=self.url,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.json( ) or [ ]
			self.result = {
					'url': self.url,
					'params': self.params,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = (
					'request( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_daily_zip( self, zip_code: str,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch daily zip.
		
		Purpose:
			Retrieves daily zip using validated arguments and the stored UvIndex runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			zip_code (str): zip code value used by the fetch daily zip operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'zip_code', zip_code )
			throw_if( 'time', time )
			
			self.mode = 'daily-zip'
			self.zip_code = self.validate_zip_code( zip_code )
			self.endpoint = 'getEnvirofactsUVDAILY'
			self.timeout = int( time )
			self.params = {
					'zip_code': self.zip_code
			}
			self.url = (
					f'{self.base_url}/{self.endpoint}/ZIP/'
					f'{urllib.parse.quote( self.zip_code, safe="" )}/JSON'
			)
			
			self.request(
				url=self.url,
				params=self.params,
				time=self.timeout
			)
			
			records = self.payload if isinstance( self.payload, list ) else [ ]
			rows = self.shape_rows( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = (
					'fetch_daily_zip( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_daily_city_state( self, city: str, state: str,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch daily city state.
		
		Purpose:
			Retrieves daily city state using validated arguments and the stored UvIndex runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			city (str): city value used by the fetch daily city state operation.
			state (str): state value used by the fetch daily city state operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'city', city )
			throw_if( 'state', state )
			throw_if( 'time', time )
			
			self.mode = 'daily-city-state'
			self.city = self.validate_city( city )
			self.state = self.validate_state( state )
			self.endpoint = 'getEnvirofactsUVDAILY'
			self.timeout = int( time )
			self.params = {
					'city': self.city,
					'state': self.state
			}
			self.url = (
					f'{self.base_url}/{self.endpoint}/CITY/'
					f'{urllib.parse.quote( self.city, safe="" )}/STATE/'
					f'{urllib.parse.quote( self.state, safe="" )}/JSON'
			)
			
			self.request(
				url=self.url,
				params=self.params,
				time=self.timeout
			)
			
			records = self.payload if isinstance( self.payload, list ) else [ ]
			rows = self.shape_rows( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = (
					'fetch_daily_city_state( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_hourly_zip( self, zip_code: str,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch hourly zip.
		
		Purpose:
			Retrieves hourly zip using validated arguments and the stored UvIndex runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			zip_code (str): zip code value used by the fetch hourly zip operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'zip_code', zip_code )
			throw_if( 'time', time )
			
			self.mode = 'hourly-zip'
			self.zip_code = self.validate_zip_code( zip_code )
			self.endpoint = 'getEnvirofactsUVHOURLY'
			self.timeout = int( time )
			self.params = {
					'zip_code': self.zip_code
			}
			self.url = (
					f'{self.base_url}/{self.endpoint}/ZIP/'
					f'{urllib.parse.quote( self.zip_code, safe="" )}/JSON'
			)
			
			self.request(
				url=self.url,
				params=self.params,
				time=self.timeout
			)
			
			records = self.payload if isinstance( self.payload, list ) else [ ]
			rows = self.shape_rows( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = (
					'fetch_hourly_zip( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_hourly_city_state( self, city: str, state: str,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch hourly city state.
		
		Purpose:
			Retrieves hourly city state using validated arguments and the stored UvIndex runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			city (str): city value used by the fetch hourly city state operation.
			state (str): state value used by the fetch hourly city state operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'city', city )
			throw_if( 'state', state )
			throw_if( 'time', time )
			
			self.mode = 'hourly-city-state'
			self.city = self.validate_city( city )
			self.state = self.validate_state( state )
			self.endpoint = 'getEnvirofactsUVHOURLY'
			self.timeout = int( time )
			self.params = {
					'city': self.city,
					'state': self.state
			}
			self.url = (
					f'{self.base_url}/{self.endpoint}/CITY/'
					f'{urllib.parse.quote( self.city, safe="" )}/STATE/'
					f'{urllib.parse.quote( self.state, safe="" )}/JSON'
			)
			
			self.request(
				url=self.url,
				params=self.params,
				time=self.timeout
			)
			
			records = self.payload if isinstance( self.payload, list ) else [ ]
			rows = self.shape_rows( records )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = (
					'fetch_hourly_city_state( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'daily-zip', zip_code: str = '',
			city: str = '', state: str = '', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch EPA UV Index current and forecast data.
		
		Purpose:
			Retrieves EPA UV Index current and forecast data using validated arguments and the
			stored UvIndex runtime configuration. The method assembles request parameters, executes
			the provider call or dispatches to a specialized helper, records response state when
			applicable, and returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			zip_code (str): zip code value used by the fetch operation.
			city (str): city value used by the fetch operation.
			state (str): state value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = self.validate_mode( mode )
			
			if self.mode == 'daily-zip':
				return self.fetch_daily_zip(
					zip_code=zip_code,
					time=time
				)
			
			if self.mode == 'daily-city-state':
				return self.fetch_daily_city_state(
					city=city,
					state=state,
					time=time
				)
			
			if self.mode == 'hourly-zip':
				return self.fetch_hourly_zip(
					zip_code=zip_code,
					time=time
				)
			
			if self.mode == 'hourly-city-state':
				return self.fetch_hourly_city_state(
					city=city,
					state=state,
					time=time
				)
			
			raise ValueError(
				"Unsupported mode. Use 'daily-zip', 'daily-city-state', "
				"'hourly-zip', or 'hourly-city-state'."
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if not isinstance( parameters, dict ):
				raise ValueError(
					'parameters must be a dict of param_name -> schema definition.'
				)
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'UvIndex'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class PurpleAir( Fetcher ):
	"""Purple Air fetcher.
	
	Purpose:
		Coordinates PurpleAir sensor and air quality records within Fonky. The class stores
		provider configuration, request parameters, response payloads, and normalized result
		state so callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		api_key (Optional[str]): API key state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		endpoint (Optional[str]): endpoint state retained by the instance.
		sensor_index (Optional[int]): sensor index state retained by the instance.
		nwlng (Optional[float]): nwlng state retained by the instance.
		nwlat (Optional[float]): nwlat state retained by the instance.
		selng (Optional[float]): selng state retained by the instance.
		selat (Optional[float]): selat state retained by the instance.
		location_type (Optional[int]): location type state retained by the instance.
		max_age (Optional[int]): max age state retained by the instance.
		modified_since (Optional[int]): modified since state retained by the instance.
		fields (Optional[str]): fields state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	api_key: Optional[ str ]
	mode: Optional[ str ]
	endpoint: Optional[ str ]
	sensor_index: Optional[ int ]
	nwlng: Optional[ float ]
	nwlat: Optional[ float ]
	selng: Optional[ float ]
	selat: Optional[ float ]
	location_type: Optional[ int ]
	max_age: Optional[ int ]
	modified_since: Optional[ int ]
	fields: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize PurpleAir.
		
		Purpose:
			Initializes the PurpleAir instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://api.purpleair.com/v1'
		self.api_key = cfg.PURPLEAIR_API_KEY
		self.mode = 'sensors'
		self.endpoint = ''
		self.sensor_index = None
		self.nwlng = None
		self.nwlat = None
		self.selng = None
		self.selat = None
		self.location_type = 0
		self.max_age = 0
		self.modified_since = 0
		self.fields = ''
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents
		}
		
		if self.api_key:
			self.headers[ 'X-API-Key' ] = self.api_key
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'api_key',
				'mode',
				'endpoint',
				'sensor_index',
				'nwlng',
				'nwlat',
				'selng',
				'selat',
				'location_type',
				'max_age',
				'modified_since',
				'fields',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'validate_api_key',
				'validate_mode',
				'validate_endpoint',
				'validate_sensor_index',
				'validate_longitude',
				'validate_latitude',
				'validate_bbox',
				'validate_location_type',
				'validate_non_negative_integer',
				'normalize_fields',
				'shape_sensor_list_rows',
				'shape_sensor_detail_rows',
				'summarize_rows',
				'package_response',
				'request',
				'fetch_sensors',
				'fetch_sensor',
				'fetch',
				'create_schema'
		]
	
	def validate_api_key( self ) -> str:
		"""Validate api key.
		
		Purpose:
			Validates and normalizes api key before it is used in PurpleAir sensor and air quality
			records. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Returns:
			str: Validated api key value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'api_key', self.api_key )
			return str( self.api_key ).strip( )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = 'validate_api_key( self ) -> str'
			raise exception
	
	def validate_mode( self, mode: str ) -> str:
		"""Validate mode.
		
		Purpose:
			Validates and normalizes mode before it is used in PurpleAir sensor and air quality
			records. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			mode (str): mode value used by the validate mode operation.
		
		Returns:
			str: Validated mode value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			value = str( mode ).strip( ).lower( )
			allowed = {
					'sensors',
					'sensor'
			}
			
			if value not in allowed:
				raise ValueError( "Unsupported PurpleAir mode. Use 'sensors' or 'sensor'." )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = 'validate_mode( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_endpoint( self, endpoint: str ) -> str:
		"""Validate endpoint.
		
		Purpose:
			Validates and normalizes endpoint before it is used in PurpleAir sensor and air quality
			records. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			endpoint (str): endpoint value used by the validate endpoint operation.
		
		Returns:
			str: Validated endpoint value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'endpoint', endpoint )
			
			value = str( endpoint ).strip( ).strip( '/' )
			
			if value.startswith( 'http://' ) or value.startswith( 'https://' ):
				raise ValueError( 'endpoint must be a path segment, not a full URL.' )
			
			if '..' in value:
				raise ValueError( 'endpoint cannot contain parent-directory markers.' )
			
			if value != 'sensors' and not re.fullmatch( r'sensors/\d+', value ):
				raise ValueError( "endpoint must be 'sensors' or 'sensors/{sensor_index}'." )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = 'validate_endpoint( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_sensor_index( self, sensor_index: int ) -> int:
		"""Validate sensor index.
		
		Purpose:
			Validates and normalizes sensor index before it is used in PurpleAir sensor and air
			quality records. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			sensor_index (int): sensor index value used by the validate sensor index operation.
		
		Returns:
			int: Validated sensor index value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'sensor_index', sensor_index )
			
			value = int( sensor_index )
			if value < 1:
				raise ValueError( 'sensor_index must be greater than or equal to 1.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = 'validate_sensor_index( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_longitude( self, name: str, value: float ) -> float:
		"""Validate longitude.
		
		Purpose:
			Validates and normalizes longitude before it is used in PurpleAir sensor and air quality
			records. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			name (str): name value used by the validate longitude operation.
			value (float): value value used by the validate longitude operation.
		
		Returns:
			float: Validated longitude value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			throw_if( name, value )
			
			number = float( value )
			if number < -180.0 or number > 180.0:
				raise ValueError( f'{name} must be between -180 and 180.' )
			
			return number
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = 'validate_longitude( self, *args, **kwargs ) -> float'
			raise exception
	
	def validate_latitude( self, name: str, value: float ) -> float:
		"""Validate latitude.
		
		Purpose:
			Validates and normalizes latitude before it is used in PurpleAir sensor and air quality
			records. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			name (str): name value used by the validate latitude operation.
			value (float): value value used by the validate latitude operation.
		
		Returns:
			float: Validated latitude value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			throw_if( name, value )
			
			number = float( value )
			if number < -90.0 or number > 90.0:
				raise ValueError( f'{name} must be between -90 and 90.' )
			
			return number
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = 'validate_latitude( self, *args, **kwargs ) -> float'
			raise exception
	
	def validate_bbox( self, nwlng: float, nwlat: float,
			selng: float, selat: float ) -> Tuple[ float, float, float, float ]:
		"""Validate bbox.
		
		Purpose:
			Validates and normalizes bbox before it is used in PurpleAir sensor and air quality
			records. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			nwlng (float): nwlng value used by the validate bbox operation.
			nwlat (float): nwlat value used by the validate bbox operation.
			selng (float): selng value used by the validate bbox operation.
			selat (float): selat value used by the validate bbox operation.
		
		Returns:
			Tuple[float, float, float, float]: Validated bbox value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			nw_lng = self.validate_longitude( 'nwlng', nwlng )
			nw_lat = self.validate_latitude( 'nwlat', nwlat )
			se_lng = self.validate_longitude( 'selng', selng )
			se_lat = self.validate_latitude( 'selat', selat )
			
			if nw_lng >= se_lng:
				raise ValueError( 'nwlng must be less than selng.' )
			
			if nw_lat <= se_lat:
				raise ValueError( 'nwlat must be greater than selat.' )
			
			return nw_lng, nw_lat, se_lng, se_lat
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = (
					'validate_bbox( self, *args, **kwargs ) '
					'-> Tuple[ float, float, float, float ]'
			)
			raise exception
	
	def validate_location_type( self, location_type: int ) -> int:
		"""Validate location type.
		
		Purpose:
			Validates and normalizes location type before it is used in PurpleAir sensor and air
			quality records. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			location_type (int): location type value used by the validate location type operation.
		
		Returns:
			int: Validated location type value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'location_type', location_type if location_type == 0 else location_type )
			
			value = int( location_type )
			if value not in (0, 1):
				raise ValueError( 'location_type must be 0 or 1.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = 'validate_location_type( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_non_negative_integer( self, name: str, value: int ) -> int:
		"""Validate non negative integer.
		
		Purpose:
			Validates and normalizes non negative integer before it is used in PurpleAir sensor and
			air quality records. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			name (str): name value used by the validate non negative integer operation.
			value (int): value value used by the validate non negative integer operation.
		
		Returns:
			int: Validated non negative integer value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			
			if value is None:
				raise ValueError( f'{name} cannot be None.' )
			
			number = int( value )
			if number < 0:
				raise ValueError( f'{name} must be greater than or equal to 0.' )
			
			return number
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = (
					'validate_non_negative_integer( self, *args, **kwargs ) -> int'
			)
			raise exception
	
	def normalize_fields( self, fields: str, default_fields: str ) -> str:
		"""Normalize fields.
		
		Purpose:
			Converts fields into the canonical format expected by the PurpleAir request workflow.
			The method standardizes caller input before it is used in endpoint paths, query
			parameters, filters, or response processing.
		
		Args:
			fields (str): fields value used by the normalize fields operation.
			default_fields (str): default fields value used by the normalize fields operation.
		
		Returns:
			str: Canonical value prepared for request construction or response processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'default_fields', default_fields )
			
			selected = str( fields or '' ).strip( )
			
			if not selected:
				selected = str( default_fields ).strip( )
			
			field_list = [
					field.strip( )
					for field in selected.split( ',' )
					if field and field.strip( )
			]
			
			if not field_list:
				raise ValueError( 'At least one PurpleAir field is required.' )
			
			self.fields = ','.join( field_list )
			
			return self.fields
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = 'normalize_fields( self, *args, **kwargs ) -> str'
			raise exception
	
	def shape_sensor_list_rows( self,
			payload: Dict[ str, Any ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape sensor list rows.
		
		Purpose:
			Transforms raw provider records into sensor list rows structures with consistent keys
			and row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			payload (Dict[str, Any]): payload value used by the shape sensor list rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			if not isinstance( payload, dict ):
				return rows
			
			fields = payload.get( 'fields', [ ] ) or [ ]
			data = payload.get( 'data', [ ] ) or [ ]
			
			for record in data:
				if not isinstance( record, list ):
					continue
				
				sensor = {
						fields[ index ]: record[ index ] if index < len( record ) else None
						for index in range( len( fields ) )
				}
				
				rows.append(
					{
							'Sensor Index': sensor.get( 'sensor_index', None ),
							'Name': sensor.get( 'name', '' ),
							'PM2.5': sensor.get( 'pm2.5', None ),
							'Temperature': sensor.get( 'temperature', None ),
							'Humidity': sensor.get( 'humidity', None ),
							'Latitude': sensor.get( 'latitude', None ),
							'Longitude': sensor.get( 'longitude', None ),
							'Last Seen': sensor.get( 'last_seen', None ),
							'Location Type': sensor.get( 'location_type', None )
					}
				)
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = (
					'shape_sensor_list_rows( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_sensor_detail_rows( self,
			payload: Dict[ str, Any ] ) -> List[ Dict[ str, Any ] ]:
		"""Shape sensor detail rows.
		
		Purpose:
			Transforms raw provider records into sensor detail rows structures with consistent keys
			and row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			payload (Dict[str, Any]): payload value used by the shape sensor detail rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if not isinstance( payload, dict ):
				return [ ]
			
			sensor = payload.get( 'sensor', { } ) or { }
			
			row = {
					'Sensor Index': sensor.get( 'sensor_index', self.sensor_index ),
					'Name': sensor.get( 'name', '' ),
					'Model': sensor.get( 'model', '' ),
					'Hardware': sensor.get( 'hardware', '' ),
					'PM2.5 Cf 1 A': sensor.get( 'pm2.5_cf_1_a', None ),
					'PM2.5 Cf 1 B': sensor.get( 'pm2.5_cf_1_b', None ),
					'Temperature': sensor.get( 'temperature', None ),
					'Humidity': sensor.get( 'humidity', None ),
					'Pressure': sensor.get( 'pressure', None ),
					'Latitude': sensor.get( 'latitude', None ),
					'Longitude': sensor.get( 'longitude', None ),
					'Last Seen': sensor.get( 'last_seen', None ),
					'Firmware Version': sensor.get( 'firmware_version', '' ),
					'RSSI': sensor.get( 'rssi', None )
			}
			
			return [ row ]
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = (
					'shape_sensor_detail_rows( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def summarize_rows( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Summarize rows.
		
		Purpose:
			Performs the summarize rows operation for PurpleAir sensor and air quality records. The
			method uses the class runtime state and supplied arguments to prepare, transform,
			dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the summarize rows operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			count = len( rows or [ ] )
			max_pm25 = None
			first_name = ''
			
			for row in rows or [ ]:
				if not first_name:
					first_name = str(
						row.get( 'Name', '' )
						or row.get( 'Sensor Index', '' )
						or ''
					)
				
				pm25_value = row.get( 'PM2.5', None )
				
				if pm25_value is None:
					pm25_value = row.get( 'PM2.5 Cf 1 A', None )
				
				try:
					if pm25_value is not None and str( pm25_value ).strip( ):
						if max_pm25 is None or float( pm25_value ) > float( max_pm25 ):
							max_pm25 = float( pm25_value )
				except Exception:
					pass
			
			return {
					'count': count,
					'max_pm25': max_pm25,
					'first_name': first_name
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = (
					'summarize_rows( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def package_response( self, rows: List[ Dict[ str, Any ] ],
			params: Dict[ str, Any ] ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the package response operation.
			params (Dict[str, Any]): Request or schema parameter dictionary used by the operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': params,
					'summary': self.summarize_rows( rows ),
					'rows': rows,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = (
					'package_response( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def request( self, endpoint: str, params: Optional[ Dict[ str, Any ] ] = None,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Request PurpleAir sensor and air quality records.
		
		Purpose:
			Sends a provider request for PurpleAir sensor and air quality records after request
			parameters have been validated or prepared by the caller. The method stores request,
			response, and payload state on the instance so subsequent methods can package or inspect
			the result consistently.
		
		Args:
			endpoint (str): endpoint value used by the request operation.
			params (Optional[Dict[str, Any]]): Request or schema parameter dictionary used by the
				operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.validate_api_key( )
			self.endpoint = self.validate_endpoint( endpoint )
			throw_if( 'time', time )
			
			self.timeout = int( time )
			self.url = f'{self.base_url}/{self.endpoint}'
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			for key, value in (params or { }).items( ):
				if value is None:
					continue
				
				if isinstance( value, str ) and not value.strip( ):
					continue
				
				self.params[ key ] = value
			
			self.headers[ 'X-API-Key' ] = self.validate_api_key( )
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.json( ) or { }
			self.result = {
					'url': self.response.url,
					'params': self.params,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = (
					'request( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_sensors( self, nwlng: float, nwlat: float, selng: float, selat: float,
			location_type: int = 0, max_age: int = 0, modified_since: int = 0,
			fields: str = '', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch sensors.
		
		Purpose:
			Retrieves sensors using validated arguments and the stored PurpleAir runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			nwlng (float): nwlng value used by the fetch sensors operation.
			nwlat (float): nwlat value used by the fetch sensors operation.
			selng (float): selng value used by the fetch sensors operation.
			selat (float): selat value used by the fetch sensors operation.
			location_type (int): location type value used by the fetch sensors operation.
			max_age (int): max age value used by the fetch sensors operation.
			modified_since (int): modified since value used by the fetch sensors operation.
			fields (str): fields value used by the fetch sensors operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			default_fields = (
					'name,pm2.5,temperature,humidity,latitude,longitude,last_seen,'
					'location_type'
			)
			
			self.mode = 'sensors'
			self.nwlng, self.nwlat, self.selng, self.selat = self.validate_bbox(
				nwlng=nwlng,
				nwlat=nwlat,
				selng=selng,
				selat=selat
			)
			self.location_type = self.validate_location_type( location_type )
			self.max_age = self.validate_non_negative_integer( 'max_age', max_age )
			self.modified_since = self.validate_non_negative_integer(
				'modified_since',
				modified_since
			)
			self.fields = self.normalize_fields(
				fields=fields,
				default_fields=default_fields
			)
			self.timeout = int( time )
			
			self.request(
				endpoint='sensors',
				params={
						'fields': self.fields,
						'location_type': self.location_type,
						'nwlng': self.nwlng,
						'nwlat': self.nwlat,
						'selng': self.selng,
						'selat': self.selat,
						'max_age': self.max_age,
						'modified_since': self.modified_since
				},
				time=self.timeout
			)
			
			rows = self.shape_sensor_list_rows( self.payload )
			
			return self.package_response(
				rows=rows,
				params=self.params
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = (
					'fetch_sensors( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_sensor( self, sensor_index: int, fields: str = '',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch sensor.
		
		Purpose:
			Retrieves sensor using validated arguments and the stored PurpleAir runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			sensor_index (int): sensor index value used by the fetch sensor operation.
			fields (str): fields value used by the fetch sensor operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			default_fields = (
					'name,model,hardware,pm2.5_cf_1_a,pm2.5_cf_1_b,temperature,'
					'humidity,pressure,latitude,longitude,last_seen,firmware_version,rssi'
			)
			
			self.mode = 'sensor'
			self.sensor_index = self.validate_sensor_index( sensor_index )
			self.fields = self.normalize_fields(
				fields=fields,
				default_fields=default_fields
			)
			self.timeout = int( time )
			
			self.request(
				endpoint=f'sensors/{self.sensor_index}',
				params={
						'fields': self.fields
				},
				time=self.timeout
			)
			
			rows = self.shape_sensor_detail_rows( self.payload )
			
			return self.package_response(
				rows=rows,
				params={
						'sensor_index': self.sensor_index,
						'fields': self.fields
				}
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = (
					'fetch_sensor( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'sensors', sensor_index: int = None,
			nwlng: float | None = None, nwlat: float | None = None,
			selng: float | None = None, selat: float | None = None,
			location_type: int = 0, max_age: int = 0, modified_since: int = 0,
			fields: str = '', time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch PurpleAir sensor and air quality records.
		
		Purpose:
			Retrieves PurpleAir sensor and air quality records using validated arguments and the
			stored PurpleAir runtime configuration. The method assembles request parameters,
			executes the provider call or dispatches to a specialized helper, records response state
			when applicable, and returns a normalized payload for downstream analysis or tool
			execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			sensor_index (int): sensor index value used by the fetch operation.
			nwlng (float | None): nwlng value used by the fetch operation.
			nwlat (float | None): nwlat value used by the fetch operation.
			selng (float | None): selng value used by the fetch operation.
			selat (float | None): selat value used by the fetch operation.
			location_type (int): location type value used by the fetch operation.
			max_age (int): max age value used by the fetch operation.
			modified_since (int): modified since value used by the fetch operation.
			fields (str): fields value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = self.validate_mode( mode )
			
			if self.mode == 'sensors':
				return self.fetch_sensors(
					nwlng=nwlng,
					nwlat=nwlat,
					selng=selng,
					selat=selat,
					location_type=location_type,
					max_age=max_age,
					modified_since=modified_since,
					fields=fields,
					time=time
				)
			
			if self.mode == 'sensor':
				return self.fetch_sensor(
					sensor_index=sensor_index,
					fields=fields,
					time=time
				)
			
			raise ValueError( "Unsupported PurpleAir mode. Use 'sensors' or 'sensor'." )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if not isinstance( parameters, dict ):
				raise ValueError(
					'parameters must be a dict of param_name -> schema definition.'
				)
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'PurpleAir'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class OpenAQ( Fetcher ):
	"""Open A Q fetcher.
	
	Purpose:
		Coordinates OpenAQ location, measurement, and air-quality records within Fonky. The
		class stores provider configuration, request parameters, response payloads, and
		normalized result state so callers can access the service through a consistent fetcher
		interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		api_key (Optional[str]): API key state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		endpoint (Optional[str]): endpoint state retained by the instance.
		location_id (Optional[int]): location ID state retained by the instance.
		parameter_id (Optional[int]): parameter ID state retained by the instance.
		country_id (Optional[int]): country ID state retained by the instance.
		coordinates (Optional[str]): coordinates state retained by the instance.
		radius (Optional[int]): radius state retained by the instance.
		providers_id (Optional[str]): providers ID state retained by the instance.
		parameters_id (Optional[str]): parameters ID state retained by the instance.
		limit (Optional[int]): limit state retained by the instance.
		page (Optional[int]): page state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	api_key: Optional[ str ]
	mode: Optional[ str ]
	endpoint: Optional[ str ]
	location_id: Optional[ int ]
	parameter_id: Optional[ int ]
	country_id: Optional[ int ]
	coordinates: Optional[ str ]
	radius: Optional[ int ]
	providers_id: Optional[ str ]
	parameters_id: Optional[ str ]
	limit: Optional[ int ]
	page: Optional[ int ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize OpenAQ.
		
		Purpose:
			Initializes the OpenAQ instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://api.openaq.org/v3'
		self.api_key = cfg.OPENAQ_API_KEY
		self.mode = 'locations'
		self.endpoint = ''
		self.location_id = None
		self.parameter_id = None
		self.country_id = None
		self.coordinates = ''
		self.radius = 25000
		self.providers_id = ''
		self.parameters_id = ''
		self.limit = 25
		self.page = 1
		self.params = { }
		self.payload = { }
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents
		}
		
		if self.api_key:
			self.headers[ 'X-API-Key' ] = self.api_key
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'api_key',
				'mode',
				'endpoint',
				'location_id',
				'parameter_id',
				'country_id',
				'coordinates',
				'radius',
				'providers_id',
				'parameters_id',
				'limit',
				'page',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'validate_api_key',
				'validate_mode',
				'validate_endpoint',
				'validate_positive_integer',
				'validate_non_negative_integer',
				'validate_coordinates',
				'validate_radius',
				'coalesce_results',
				'shape_resource_rows',
				'shape_location_rows',
				'shape_latest_rows',
				'summarize_rows',
				'package_response',
				'request',
				'fetch_countries',
				'fetch_providers',
				'fetch_parameters',
				'fetch_parameter_latest',
				'fetch_locations',
				'fetch_latest',
				'fetch',
				'create_schema'
		]
	
	def validate_api_key( self ) -> str:
		"""Validate api key.
		
		Purpose:
			Validates and normalizes api key before it is used in OpenAQ location, measurement, and
			air-quality records. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Returns:
			str: Validated api key value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'api_key', self.api_key )
			return str( self.api_key ).strip( )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = 'validate_api_key( self ) -> str'
			raise exception
	
	def validate_mode( self, mode: str ) -> str:
		"""Validate mode.
		
		Purpose:
			Validates and normalizes mode before it is used in OpenAQ location, measurement, and
			air-quality records. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			mode (str): mode value used by the validate mode operation.
		
		Returns:
			str: Validated mode value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			value = str( mode ).strip( ).lower( )
			allowed = {
					'countries',
					'providers',
					'parameters',
					'parameter_latest',
					'locations',
					'latest'
			}
			
			if value not in allowed:
				raise ValueError(
					'Unsupported OpenAQ mode. Use countries, providers, parameters, '
					'parameter_latest, locations, or latest.'
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = 'validate_mode( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_endpoint( self, endpoint: str ) -> str:
		"""Validate endpoint.
		
		Purpose:
			Validates and normalizes endpoint before it is used in OpenAQ location, measurement, and
			air-quality records. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			endpoint (str): endpoint value used by the validate endpoint operation.
		
		Returns:
			str: Validated endpoint value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'endpoint', endpoint )
			
			value = str( endpoint ).strip( ).strip( '/' )
			
			if value.startswith( 'http://' ) or value.startswith( 'https://' ):
				raise ValueError( 'endpoint must be a path segment, not a full URL.' )
			
			if '..' in value:
				raise ValueError( 'endpoint cannot contain parent-directory markers.' )
			
			if not re.fullmatch(
					r'(countries|providers|parameters|locations|'
					r'parameters/\d+/latest|locations/\d+/latest)',
					value
			):
				raise ValueError(
					'Unsupported OpenAQ endpoint path.'
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = 'validate_endpoint( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_positive_integer( self, name: str, value: Any,
			maximum: int | None = None ) -> int:
		"""Validate positive integer.
		
		Purpose:
			Validates and normalizes positive integer before it is used in OpenAQ location,
			measurement, and air-quality records. The method converts incoming values to the
			expected representation, enforces visible range or format constraints, and returns the
			checked value for request construction.
		
		Args:
			name (str): name value used by the validate positive integer operation.
			value (object): value value used by the validate positive integer operation.
			maximum (int | None): maximum value used by the validate positive integer operation.
		
		Returns:
			int: Validated positive integer value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			throw_if( name, value )
			
			number = int( value )
			
			if number < 1:
				raise ValueError( f'{name} must be greater than or equal to 1.' )
			
			if maximum is not None and number > int( maximum ):
				raise ValueError( f'{name} must be less than or equal to {maximum}.' )
			
			return number
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'validate_positive_integer( self, *args, **kwargs ) -> int'
			)
			raise exception
	
	def validate_non_negative_integer( self, name: str, value: Any ) -> int:
		"""Validate non negative integer.
		
		Purpose:
			Validates and normalizes non negative integer before it is used in OpenAQ location,
			measurement, and air-quality records. The method converts incoming values to the
			expected representation, enforces visible range or format constraints, and returns the
			checked value for request construction.
		
		Args:
			name (str): name value used by the validate non negative integer operation.
			value (object): value value used by the validate non negative integer operation.
		
		Returns:
			int: Validated non negative integer value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			
			if value is None:
				raise ValueError( f'{name} cannot be None.' )
			
			number = int( value )
			
			if number < 0:
				raise ValueError( f'{name} must be greater than or equal to 0.' )
			
			return number
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'validate_non_negative_integer( self, *args, **kwargs ) -> int'
			)
			raise exception
	
	def validate_coordinates( self, coordinates: str = '' ) -> str:
		"""Validate coordinates.
		
		Purpose:
			Validates and normalizes coordinates before it is used in OpenAQ location, measurement,
			and air-quality records. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			coordinates (str): coordinates value used by the validate coordinates operation.
		
		Returns:
			str: Validated coordinates value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( coordinates or '' ).strip( )
			
			if not value:
				return ''
			
			parts = [
					part.strip( )
					for part in value.split( ',' )
			]
			
			if len( parts ) != 2:
				raise ValueError( 'coordinates must use latitude,longitude format.' )
			
			latitude = float( parts[ 0 ] )
			longitude = float( parts[ 1 ] )
			
			if latitude < -90.0 or latitude > 90.0:
				raise ValueError( 'coordinates latitude must be between -90 and 90.' )
			
			if longitude < -180.0 or longitude > 180.0:
				raise ValueError( 'coordinates longitude must be between -180 and 180.' )
			
			return f'{latitude},{longitude}'
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = 'validate_coordinates( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_radius( self, radius: int ) -> int:
		"""Validate radius.
		
		Purpose:
			Validates and normalizes radius before it is used in OpenAQ location, measurement, and
			air-quality records. The method converts incoming values to the expected representation,
			enforces visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			radius (int): radius value used by the validate radius operation.
		
		Returns:
			int: Validated radius value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = self.validate_positive_integer(
				name='radius',
				value=radius,
				maximum=100000
			)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = 'validate_radius( self, *args, **kwargs ) -> int'
			raise exception
	
	def coalesce_results( self, payload: Any ) -> List[ Dict[ str, Any ] ]:
		"""Coalesce results.
		
		Purpose:
			Performs the coalesce results operation for OpenAQ location, measurement, and
			air-quality records. The method uses the class runtime state and supplied arguments to
			prepare, transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			payload (object): payload value used by the coalesce results operation.
		
		Returns:
			List[Dict[str, Any]]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if payload is None:
				return [ ]
			
			if isinstance( payload, list ):
				return [
						item
						for item in payload
						if isinstance( item, dict )
				]
			
			if not isinstance( payload, dict ):
				return [ ]
			
			results = payload.get( 'results', [ ] )
			
			if isinstance( results, list ):
				return [
						item
						for item in results
						if isinstance( item, dict )
				]
			
			return [ ]
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'coalesce_results( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_resource_rows( self, payload: Any,
			resource_name: str ) -> List[ Dict[ str, Any ] ]:
		"""Shape resource rows.
		
		Purpose:
			Transforms raw provider records into resource rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			payload (object): payload value used by the shape resource rows operation.
			resource_name (str): resource name value used by the shape resource rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'resource_name', resource_name )
			
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in self.coalesce_results( payload ):
				row = {
						'Id': item.get( 'id', '' ),
						'Name': item.get( 'name', '' ),
						'Display Name': (
								item.get( 'displayName', None )
								or item.get( 'display_name', None )
								or item.get( 'name', '' )
						),
						'Code': item.get( 'code', '' ),
						'Resource': resource_name,
						'First Datetime': item.get( 'datetimeFirst', '' ),
						'Last Datetime': item.get( 'datetimeLast', '' )
				}
				
				parameters = item.get( 'parameters', [ ] )
				if isinstance( parameters, list ) and parameters:
					row[ 'Parameter Count' ] = len( parameters )
					row[ 'First Parameter' ] = (
							parameters[ 0 ].get( 'name', '' )
							if isinstance( parameters[ 0 ], dict )
							else ''
					)
				
				rows.append( row )
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'shape_resource_rows( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_location_rows( self, payload: Any ) -> List[ Dict[ str, Any ] ]:
		"""Shape location rows.
		
		Purpose:
			Transforms raw provider records into location rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			payload (object): payload value used by the shape location rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in self.coalesce_results( payload ):
				coordinates = item.get( 'coordinates', { } ) or { }
				country = item.get( 'country', { } ) or { }
				provider = item.get( 'provider', { } ) or item.get( 'owner', { } ) or { }
				parameters = item.get( 'parameters', [ ] ) or [ ]
				
				latitude = (
						coordinates.get( 'latitude', None )
						if isinstance( coordinates, dict )
						else None
				)
				longitude = (
						coordinates.get( 'longitude', None )
						if isinstance( coordinates, dict )
						else None
				)
				
				rows.append(
					{
							'Location Id': item.get( 'id', '' ),
							'Name': item.get( 'name', '' ),
							'Locality': item.get( 'locality', '' ),
							'Timezone': item.get( 'timezone', '' ),
							'Country': (
									country.get( 'name', '' )
									if isinstance( country, dict )
									else country
							),
							'Country Code': (
									country.get( 'code', '' )
									if isinstance( country, dict )
									else ''
							),
							'Provider': (
									provider.get( 'name', '' )
									if isinstance( provider, dict )
									else provider
							),
							'Parameter Count': (
									len( parameters )
									if isinstance( parameters, list )
									else 0
							),
							'First Parameter': (
									parameters[ 0 ].get( 'name', '' )
									if isinstance( parameters, list )
									   and parameters
									   and isinstance( parameters[ 0 ], dict )
									else ''
							),
							'Latitude': latitude,
							'Longitude': longitude,
							'First Datetime': item.get( 'datetimeFirst', '' ),
							'Last Datetime': item.get( 'datetimeLast', '' )
					}
				)
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'shape_location_rows( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def shape_latest_rows( self, payload: Any ) -> List[ Dict[ str, Any ] ]:
		"""Shape latest rows.
		
		Purpose:
			Transforms raw provider records into latest rows structures with consistent keys and
			row-oriented values. The method prepares service responses for display, export,
			analysis, or downstream processing without changing the provider request contract.
		
		Args:
			payload (object): payload value used by the shape latest rows operation.
		
		Returns:
			List[Dict[str, Any]]: Normalized rows or summary structures created from provider
				response records.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for item in self.coalesce_results( payload ):
				location = item.get( 'location', { } ) or { }
				parameter = item.get( 'parameter', { } ) or { }
				coordinates = item.get( 'coordinates', { } ) or { }
				period = item.get( 'period', { } ) or { }
				datetime_value = item.get( 'datetime', { } ) or item.get( 'date', { } ) or { }
				
				rows.append(
					{
							'Location Id': (
									location.get( 'id', '' )
									if isinstance( location, dict )
									else ''
							),
							'Name': (
									location.get( 'name', '' )
									if isinstance( location, dict )
									else ''
							),
							'Parameter': (
									parameter.get( 'name', '' )
									if isinstance( parameter, dict )
									else item.get( 'parameter', '' )
							),
							'Parameter Id': (
									parameter.get( 'id', '' )
									if isinstance( parameter, dict )
									else ''
							),
							'Value': item.get( 'value', '' ),
							'Unit': item.get( 'unit', '' ),
							'Datetime': (
									datetime_value.get( 'utc', '' )
									if isinstance( datetime_value, dict )
									else datetime_value
							),
							'Period Label': (
									period.get( 'label', '' )
									if isinstance( period, dict )
									else ''
							),
							'Latitude': (
									coordinates.get( 'latitude', None )
									if isinstance( coordinates, dict )
									else None
							),
							'Longitude': (
									coordinates.get( 'longitude', None )
									if isinstance( coordinates, dict )
									else None
							)
					}
				)
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'shape_latest_rows( self, *args, **kwargs ) '
					'-> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def summarize_rows( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Summarize rows.
		
		Purpose:
			Performs the summarize rows operation for OpenAQ location, measurement, and air-quality
			records. The method uses the class runtime state and supplied arguments to prepare,
			transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the summarize rows operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			count = len( rows or [ ] )
			first_result = ''
			first_parameter = ''
			first_country = ''
			
			if rows:
				first_result = str(
					rows[ 0 ].get( 'Name', '' )
					or rows[ 0 ].get( 'Display Name', '' )
					or rows[ 0 ].get( 'Location Id', '' )
					or rows[ 0 ].get( 'Id', '' )
					or ''
				)
				first_parameter = str(
					rows[ 0 ].get( 'First Parameter', '' )
					or rows[ 0 ].get( 'Parameter', '' )
					or ''
				)
				first_country = str(
					rows[ 0 ].get( 'Country', '' )
					or rows[ 0 ].get( 'Country Code', '' )
					or ''
				)
			
			return {
					'count': count,
					'first_result': first_result,
					'first_parameter': first_parameter,
					'first_country': first_country
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'summarize_rows( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def package_response( self, rows: List[ Dict[ str, Any ] ],
			params: Optional[ Dict[ str, Any ] ] = None ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the package response operation.
			params (Optional[Dict[str, Any]]): Request or schema parameter dictionary used by the
				operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': params if params is not None else self.params,
					'summary': self.summarize_rows( rows ),
					'rows': rows,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'package_response( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def request( self, endpoint: str, params: Optional[ Dict[ str, Any ] ] = None,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Request OpenAQ location, measurement, and air-quality records.
		
		Purpose:
			Sends a provider request for OpenAQ location, measurement, and air-quality records after
			request parameters have been validated or prepared by the caller. The method stores
			request, response, and payload state on the instance so subsequent methods can package
			or inspect the result consistently.
		
		Args:
			endpoint (str): endpoint value used by the request operation.
			params (Optional[Dict[str, Any]]): Request or schema parameter dictionary used by the
				operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.validate_api_key( )
			self.endpoint = self.validate_endpoint( endpoint )
			throw_if( 'time', time )
			
			self.timeout = int( time )
			self.url = f'{self.base_url}/{self.endpoint}'
			self.params = { }
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			for key, value in (params or { }).items( ):
				if value is None:
					continue
				
				if isinstance( value, str ) and not value.strip( ):
					continue
				
				self.params[ key ] = value
			
			self.headers[ 'X-API-Key' ] = self.validate_api_key( )
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.json( ) or { }
			self.result = {
					'url': self.response.url,
					'params': self.params,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'request( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_countries( self, providers_id: str = '', parameters_id: str = '',
			limit: int = 100, page: int = 1,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch countries.
		
		Purpose:
			Retrieves countries using validated arguments and the stored OpenAQ runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			providers_id (str): providers ID value used by the fetch countries operation.
			parameters_id (str): parameters ID value used by the fetch countries operation.
			limit (int): limit value used by the fetch countries operation.
			page (int): page value used by the fetch countries operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'countries'
			self.providers_id = str( providers_id or '' ).strip( )
			self.parameters_id = str( parameters_id or '' ).strip( )
			self.limit = self.validate_positive_integer( 'limit', limit, maximum=1000 )
			self.page = self.validate_positive_integer( 'page', page )
			self.timeout = int( time )
			
			self.request(
				endpoint='countries',
				params={
						'providers_id': self.providers_id,
						'parameters_id': self.parameters_id,
						'limit': self.limit,
						'page': self.page
				},
				time=self.timeout
			)
			
			rows = self.shape_resource_rows( self.payload, 'countries' )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'fetch_countries( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_providers( self, limit: int = 100, page: int = 1,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch providers.
		
		Purpose:
			Retrieves providers using validated arguments and the stored OpenAQ runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			limit (int): limit value used by the fetch providers operation.
			page (int): page value used by the fetch providers operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'providers'
			self.limit = self.validate_positive_integer( 'limit', limit, maximum=1000 )
			self.page = self.validate_positive_integer( 'page', page )
			self.timeout = int( time )
			
			self.request(
				endpoint='providers',
				params={
						'limit': self.limit,
						'page': self.page
				},
				time=self.timeout
			)
			
			rows = self.shape_resource_rows( self.payload, 'providers' )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'fetch_providers( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_parameters( self, limit: int = 100, page: int = 1,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch parameters.
		
		Purpose:
			Retrieves parameters using validated arguments and the stored OpenAQ runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			limit (int): limit value used by the fetch parameters operation.
			page (int): page value used by the fetch parameters operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'parameters'
			self.limit = self.validate_positive_integer( 'limit', limit, maximum=1000 )
			self.page = self.validate_positive_integer( 'page', page )
			self.timeout = int( time )
			
			self.request(
				endpoint='parameters',
				params={
						'limit': self.limit,
						'page': self.page
				},
				time=self.timeout
			)
			
			rows = self.shape_resource_rows( self.payload, 'parameters' )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'fetch_parameters( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_parameter_latest( self, parameter_id: int, limit: int = 100,
			page: int = 1, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch parameter latest.
		
		Purpose:
			Retrieves parameter latest using validated arguments and the stored OpenAQ runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			parameter_id (int): parameter ID value used by the fetch parameter latest operation.
			limit (int): limit value used by the fetch parameter latest operation.
			page (int): page value used by the fetch parameter latest operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'parameter_latest'
			self.parameter_id = self.validate_positive_integer(
				name='parameter_id',
				value=parameter_id
			)
			self.limit = self.validate_positive_integer( 'limit', limit, maximum=1000 )
			self.page = self.validate_positive_integer( 'page', page )
			self.timeout = int( time )
			
			self.request(
				endpoint=f'parameters/{self.parameter_id}/latest',
				params={
						'limit': self.limit,
						'page': self.page
				},
				time=self.timeout
			)
			
			rows = self.shape_latest_rows( self.payload )
			
			return self.package_response(
				rows=rows,
				params={
						'parameter_id': self.parameter_id,
						'limit': self.limit,
						'page': self.page
				}
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'fetch_parameter_latest( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_locations( self, country_id: int = None, coordinates: str = '',
			radius: int = 25000, providers_id: str = '', parameters_id: str = '',
			limit: int = 25, page: int = 1,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch locations.
		
		Purpose:
			Retrieves locations using validated arguments and the stored OpenAQ runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			country_id (int): country ID value used by the fetch locations operation.
			coordinates (str): coordinates value used by the fetch locations operation.
			radius (int): radius value used by the fetch locations operation.
			providers_id (str): providers ID value used by the fetch locations operation.
			parameters_id (str): parameters ID value used by the fetch locations operation.
			limit (int): limit value used by the fetch locations operation.
			page (int): page value used by the fetch locations operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'locations'
			self.country_id = (
					None
					if country_id is None
					else self.validate_positive_integer( 'country_id', country_id )
			)
			self.coordinates = self.validate_coordinates( coordinates )
			self.radius = self.validate_radius( radius )
			self.providers_id = str( providers_id or '' ).strip( )
			self.parameters_id = str( parameters_id or '' ).strip( )
			self.limit = self.validate_positive_integer( 'limit', limit, maximum=1000 )
			self.page = self.validate_positive_integer( 'page', page )
			self.timeout = int( time )
			
			self.request(
				endpoint='locations',
				params={
						'country_id': self.country_id,
						'coordinates': self.coordinates,
						'radius': self.radius,
						'providers_id': self.providers_id,
						'parameters_id': self.parameters_id,
						'limit': self.limit,
						'page': self.page
				},
				time=self.timeout
			)
			
			rows = self.shape_location_rows( self.payload )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'fetch_locations( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_latest( self, location_id: int,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch latest.
		
		Purpose:
			Retrieves latest using validated arguments and the stored OpenAQ runtime configuration.
			The method assembles request parameters, executes the provider call or dispatches to a
			specialized helper, records response state when applicable, and returns a normalized
			payload for downstream analysis or tool execution.
		
		Args:
			location_id (int): location ID value used by the fetch latest operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'latest'
			self.location_id = self.validate_positive_integer(
				name='location_id',
				value=location_id
			)
			self.timeout = int( time )
			
			self.request(
				endpoint=f'locations/{self.location_id}/latest',
				params={ },
				time=self.timeout
			)
			
			rows = self.shape_latest_rows( self.payload )
			
			return self.package_response(
				rows=rows,
				params={
						'location_id': self.location_id
				}
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'fetch_latest( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'locations', location_id: int = None,
			parameter_id: int = None, country_id: int = None,
			coordinates: str = '', radius: int = 25000,
			providers_id: str = '', parameters_id: str = '',
			limit: int = 25, page: int = 1,
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch OpenAQ location, measurement, and air-quality records.
		
		Purpose:
			Retrieves OpenAQ location, measurement, and air-quality records using validated
			arguments and the stored OpenAQ runtime configuration. The method assembles request
			parameters, executes the provider call or dispatches to a specialized helper, records
			response state when applicable, and returns a normalized payload for downstream analysis
			or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			location_id (int): location ID value used by the fetch operation.
			parameter_id (int): parameter ID value used by the fetch operation.
			country_id (int): country ID value used by the fetch operation.
			coordinates (str): coordinates value used by the fetch operation.
			radius (int): radius value used by the fetch operation.
			providers_id (str): providers ID value used by the fetch operation.
			parameters_id (str): parameters ID value used by the fetch operation.
			limit (int): limit value used by the fetch operation.
			page (int): page value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = self.validate_mode( mode )
			
			if self.mode == 'countries':
				return self.fetch_countries(
					providers_id=providers_id,
					parameters_id=parameters_id,
					limit=limit,
					page=page,
					time=time
				)
			
			if self.mode == 'providers':
				return self.fetch_providers(
					limit=limit,
					page=page,
					time=time
				)
			
			if self.mode == 'parameters':
				return self.fetch_parameters(
					limit=limit,
					page=page,
					time=time
				)
			
			if self.mode == 'parameter_latest':
				return self.fetch_parameter_latest(
					parameter_id=parameter_id,
					limit=limit,
					page=page,
					time=time
				)
			
			if self.mode == 'locations':
				return self.fetch_locations(
					country_id=country_id,
					coordinates=coordinates,
					radius=radius,
					providers_id=providers_id,
					parameters_id=parameters_id,
					limit=limit,
					page=page,
					time=time
				)
			
			if self.mode == 'latest':
				return self.fetch_latest(
					location_id=location_id,
					time=time
				)
			
			raise ValueError(
				'Unsupported OpenAQ mode. Use countries, providers, parameters, '
				'parameter_latest, locations, or latest.'
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if not isinstance( parameters, dict ):
				raise ValueError(
					'parameters must be a dict of param_name -> schema definition.'
				)
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'OpenAQ'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class Firms( Fetcher ):
	"""Firms fetcher.
	
	Purpose:
		Coordinates NASA FIRMS active fire data within Fonky. The class stores provider
		configuration, request parameters, response payloads, and normalized result state so
		callers can access the service through a consistent fetcher interface.
	
	Attributes:
		base_url (Optional[str]): base URL state retained by the instance.
		map_key (Optional[str]): map key state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		source (Optional[str]): source state retained by the instance.
		area_coordinates (Optional[str]): area coordinates state retained by the instance.
		day_range (Optional[int]): day range state retained by the instance.
		date (Optional[str]): date state retained by the instance.
		sensor (Optional[str]): sensor state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		timeout (object): timeout state retained by the instance.
		headers (object): headers state retained by the instance."""
	base_url: Optional[ str ]
	map_key: Optional[ str ]
	mode: Optional[ str ]
	source: Optional[ str ]
	area_coordinates: Optional[ str ]
	day_range: Optional[ int ]
	date: Optional[ str ]
	sensor: Optional[ str ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize Firms.
		
		Purpose:
			Initializes the Firms instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.base_url = 'https://firms.modaps.eosdis.nasa.gov/api'
		self.map_key = cfg.FIRMS_MAP_KEY
		self.mode = 'area'
		self.source = 'VIIRS_SNPP_NRT'
		self.area_coordinates = 'world'
		self.day_range = 1
		self.date = ''
		self.sensor = 'ALL'
		self.params = { }
		self.payload = ''
		self.result = { }
		self.response = None
		self.url = None
		self.timeout = 20
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'text/csv',
				'User-Agent': self.agents
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'base_url',
				'map_key',
				'mode',
				'source',
				'area_coordinates',
				'day_range',
				'date',
				'sensor',
				'params',
				'payload',
				'result',
				'response',
				'url',
				'timeout',
				'agents',
				'headers',
				'validate_map_key',
				'validate_mode',
				'validate_source',
				'validate_sensor',
				'validate_day_range',
				'validate_date',
				'validate_area_coordinates',
				'csv_to_rows',
				'summarize_rows',
				'package_response',
				'request_csv',
				'fetch_area',
				'fetch_data_availability',
				'fetch',
				'create_schema'
		]
	
	def validate_map_key( self ) -> str:
		"""Validate map key.
		
		Purpose:
			Validates and normalizes map key before it is used in NASA FIRMS active fire data. The
			method converts incoming values to the expected representation, enforces visible range
			or format constraints, and returns the checked value for request construction.
		
		Returns:
			str: Validated map key value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'map_key', self.map_key )
			return str( self.map_key ).strip( )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = 'validate_map_key( self ) -> str'
			raise exception
	
	def validate_mode( self, mode: str ) -> str:
		"""Validate mode.
		
		Purpose:
			Validates and normalizes mode before it is used in NASA FIRMS active fire data. The
			method converts incoming values to the expected representation, enforces visible range
			or format constraints, and returns the checked value for request construction.
		
		Args:
			mode (str): mode value used by the validate mode operation.
		
		Returns:
			str: Validated mode value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			value = str( mode ).strip( ).lower( )
			allowed = {
					'area',
					'data-availability'
			}
			
			if value not in allowed:
				raise ValueError(
					"Unsupported FIRMS mode. Use 'area' or 'data-availability'."
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = 'validate_mode( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_source( self, source: str ) -> str:
		"""Validate source.
		
		Purpose:
			Validates and normalizes source before it is used in NASA FIRMS active fire data. The
			method converts incoming values to the expected representation, enforces visible range
			or format constraints, and returns the checked value for request construction.
		
		Args:
			source (str): source value used by the validate source operation.
		
		Returns:
			str: Validated source value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'source', source )
			
			value = str( source ).strip( ).upper( )
			allowed = {
					'LANDSAT_NRT',
					'MODIS_NRT',
					'MODIS_SP',
					'VIIRS_NOAA20_NRT',
					'VIIRS_NOAA20_SP',
					'VIIRS_NOAA21_NRT',
					'VIIRS_SNPP_NRT',
					'VIIRS_SNPP_SP'
			}
			
			if value not in allowed:
				raise ValueError(
					'Unsupported FIRMS source. Use one of the app-supported '
					'LANDSAT, MODIS, or VIIRS source identifiers.'
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = 'validate_source( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_sensor( self, sensor: str ) -> str:
		"""Validate sensor.
		
		Purpose:
			Validates and normalizes sensor before it is used in NASA FIRMS active fire data. The
			method converts incoming values to the expected representation, enforces visible range
			or format constraints, and returns the checked value for request construction.
		
		Args:
			sensor (str): sensor value used by the validate sensor operation.
		
		Returns:
			str: Validated sensor value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'sensor', sensor )
			
			value = str( sensor ).strip( ).upper( )
			allowed = {
					'ALL',
					'LANDSAT',
					'MODIS',
					'VIIRS_SNPP',
					'VIIRS_NOAA20',
					'VIIRS_NOAA21'
			}
			
			if value not in allowed:
				raise ValueError(
					'Unsupported FIRMS sensor. Use ALL, LANDSAT, MODIS, '
					'VIIRS_SNPP, VIIRS_NOAA20, or VIIRS_NOAA21.'
				)
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = 'validate_sensor( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_day_range( self, day_range: int ) -> int:
		"""Validate day range.
		
		Purpose:
			Validates and normalizes day range before it is used in NASA FIRMS active fire data. The
			method converts incoming values to the expected representation, enforces visible range
			or format constraints, and returns the checked value for request construction.
		
		Args:
			day_range (int): day range value used by the validate day range operation.
		
		Returns:
			int: Validated day range value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'day_range', day_range )
			
			value = int( day_range )
			if value < 1 or value > 5:
				raise ValueError( 'day_range must be between 1 and 5.' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = 'validate_day_range( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_date( self, date: str = '' ) -> str:
		"""Validate date.
		
		Purpose:
			Validates and normalizes date before it is used in NASA FIRMS active fire data. The
			method converts incoming values to the expected representation, enforces visible range
			or format constraints, and returns the checked value for request construction.
		
		Args:
			date (str): date value used by the validate date operation.
		
		Returns:
			str: Validated date value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			value = str( date or '' ).strip( )
			
			if not value:
				return ''
			
			dt.datetime.strptime( value, '%Y-%m-%d' )
			
			return value
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = 'validate_date( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_area_coordinates( self, area_coordinates: str = 'world' ) -> str:
		"""Validate area coordinates.
		
		Purpose:
			Validates and normalizes area coordinates before it is used in NASA FIRMS active fire
			data. The method converts incoming values to the expected representation, enforces
			visible range or format constraints, and returns the checked value for request
			construction.
		
		Args:
			area_coordinates (str): area coordinates value used by the validate area coordinates
				operation.
		
		Returns:
			str: Validated area coordinates value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'area_coordinates', area_coordinates )
			
			value = str( area_coordinates ).strip( )
			
			if value.lower( ) == 'world':
				return 'world'
			
			parts = [
					part.strip( )
					for part in value.split( ',' )
			]
			
			if len( parts ) != 4:
				raise ValueError(
					'area_coordinates must be world or west,south,east,north.'
				)
			
			west, south, east, north = [ float( part ) for part in parts ]
			
			if west < -180.0 or west > 180.0:
				raise ValueError( 'west longitude must be between -180 and 180.' )
			
			if east < -180.0 or east > 180.0:
				raise ValueError( 'east longitude must be between -180 and 180.' )
			
			if south < -90.0 or south > 90.0:
				raise ValueError( 'south latitude must be between -90 and 90.' )
			
			if north < -90.0 or north > 90.0:
				raise ValueError( 'north latitude must be between -90 and 90.' )
			
			if west >= east:
				raise ValueError( 'west longitude must be less than east longitude.' )
			
			if south >= north:
				raise ValueError( 'south latitude must be less than north latitude.' )
			
			return f'{west:g},{south:g},{east:g},{north:g}'
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = (
					'validate_area_coordinates( self, *args, **kwargs ) -> str'
			)
			raise exception
	
	def csv_to_rows( self, csv_text: str ) -> List[ Dict[ str, Any ] ]:
		"""CSV to rows.
		
		Purpose:
			Performs the csv to rows operation for NASA FIRMS active fire data. The method uses the
			class runtime state and supplied arguments to prepare, transform, dispatch, or package
			data for the broader Fonky fetching workflow.
		
		Args:
			csv_text (str): CSV text value used by the csv to rows operation.
		
		Returns:
			List[Dict[str, Any]]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			text = str( csv_text or '' )
			
			if not text.strip( ):
				return [ ]
			
			reader = csv.DictReader( io.StringIO( text ) )
			rows: List[ Dict[ str, Any ] ] = [ ]
			
			for record in reader:
				if not isinstance( record, dict ):
					continue
				
				row: Dict[ str, Any ] = { }
				
				for key, value in record.items( ):
					friendly_key = str( key ).replace( '_', ' ' ).title( )
					row[ friendly_key ] = value
				
				rows.append( row )
			
			return rows
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = (
					'csv_to_rows( self, *args, **kwargs ) -> List[ Dict[ str, Any ] ]'
			)
			raise exception
	
	def summarize_rows( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Summarize rows.
		
		Purpose:
			Performs the summarize rows operation for NASA FIRMS active fire data. The method uses
			the class runtime state and supplied arguments to prepare, transform, dispatch, or
			package data for the broader Fonky fetching workflow.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the summarize rows operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			count = len( rows or [ ] )
			first_date = ''
			first_sensor = ''
			first_lat = ''
			first_lon = ''
			
			if rows:
				first_date = str(
					rows[ 0 ].get( 'Acq Date', '' )
					or rows[ 0 ].get( 'Date', '' )
					or rows[ 0 ].get( 'Start Date', '' )
					or ''
				)
				first_sensor = str(
					rows[ 0 ].get( 'Sensor', '' )
					or rows[ 0 ].get( 'Satellite', '' )
					or rows[ 0 ].get( 'Source', '' )
					or ''
				)
				first_lat = str( rows[ 0 ].get( 'Latitude', '' ) or '' )
				first_lon = str( rows[ 0 ].get( 'Longitude', '' ) or '' )
			
			return {
					'count': count,
					'first_date': first_date,
					'first_sensor': first_sensor,
					'first_lat': first_lat,
					'first_lon': first_lon
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = (
					'summarize_rows( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def package_response( self, rows: List[ Dict[ str, Any ] ] ) -> Dict[ str, Any ]:
		"""Package response.
		
		Purpose:
			Packages response into the app-facing response structure used by Fonky callers. The
			method combines stored mode, URL, parameters, and payload state into a normalized
			dictionary suitable for display, export, or tool output.
		
		Args:
			rows (List[Dict[str, Any]]): rows value used by the package response operation.
		
		Returns:
			Dict[str, Any]: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.result = {
					'mode': self.mode,
					'url': self.url,
					'params': self.params,
					'summary': self.summarize_rows( rows ),
					'rows': rows,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = (
					'package_response( self, *args, **kwargs ) -> Dict[ str, Any ]'
			)
			raise exception
	
	def request_csv( self, url: str, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Request CSV.
		
		Purpose:
			Performs the request csv operation for NASA FIRMS active fire data. The method uses the
			class runtime state and supplied arguments to prepare, transform, dispatch, or package
			data for the broader Fonky fetching workflow.
		
		Args:
			url (str): URL or URI value used as the request or parsing source.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.validate_map_key( )
			throw_if( 'url', url )
			throw_if( 'time', time )
			
			self.url = str( url ).strip( )
			self.timeout = int( time )
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			self.response = requests.get(
				url=self.url,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.text or ''
			self.result = {
					'url': self.url,
					'params': self.params,
					'raw': self.payload
			}
			
			return self.result
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = (
					'request_csv( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_area( self, source: str, area_coordinates: str = 'world',
			day_range: int = 1, date: str = '',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch area.
		
		Purpose:
			Retrieves area using validated arguments and the stored Firms runtime configuration. The
			method assembles request parameters, executes the provider call or dispatches to a
			specialized helper, records response state when applicable, and returns a normalized
			payload for downstream analysis or tool execution.
		
		Args:
			source (str): source value used by the fetch area operation.
			area_coordinates (str): area coordinates value used by the fetch area operation.
			day_range (int): day range value used by the fetch area operation.
			date (str): date value used by the fetch area operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'area'
			self.source = self.validate_source( source )
			self.area_coordinates = self.validate_area_coordinates( area_coordinates )
			self.day_range = self.validate_day_range( day_range )
			self.date = self.validate_date( date )
			self.timeout = int( time )
			self.params = {
					'source': self.source,
					'area_coordinates': self.area_coordinates,
					'day_range': self.day_range,
					'date': self.date
			}
			self.url = (
					f'{self.base_url}/area/csv/{self.validate_map_key( )}/'
					f'{self.source}/{self.area_coordinates}/{self.day_range}'
			)
			
			if self.date:
				self.url = f'{self.url}/{self.date}'
			
			self.request_csv(
				url=self.url,
				time=self.timeout
			)
			
			rows = self.csv_to_rows( self.payload )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = (
					'fetch_area( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_data_availability( self, sensor: str = 'ALL',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch data availability.
		
		Purpose:
			Retrieves data availability using validated arguments and the stored Firms runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			sensor (str): sensor value used by the fetch data availability operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'data-availability'
			self.sensor = self.validate_sensor( sensor )
			self.timeout = int( time )
			self.params = {
					'sensor': self.sensor
			}
			self.url = (
					f'{self.base_url}/data_availability/csv/'
					f'{self.validate_map_key( )}/{self.sensor}'
			)
			
			self.request_csv(
				url=self.url,
				time=self.timeout
			)
			
			rows = self.csv_to_rows( self.payload )
			
			return self.package_response( rows )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = (
					'fetch_data_availability( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'area', source: str = 'VIIRS_SNPP_NRT',
			area_coordinates: str = 'world', day_range: int = 1,
			date: str = '', sensor: str = 'ALL',
			time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch NASA FIRMS active fire data.
		
		Purpose:
			Retrieves NASA FIRMS active fire data using validated arguments and the stored Firms
			runtime configuration. The method assembles request parameters, executes the provider
			call or dispatches to a specialized helper, records response state when applicable, and
			returns a normalized payload for downstream analysis or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			source (str): source value used by the fetch operation.
			area_coordinates (str): area coordinates value used by the fetch operation.
			day_range (int): day range value used by the fetch operation.
			date (str): date value used by the fetch operation.
			sensor (str): sensor value used by the fetch operation.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = self.validate_mode( mode )
			
			if self.mode == 'area':
				return self.fetch_area(
					source=source,
					area_coordinates=area_coordinates,
					day_range=day_range,
					date=date,
					time=time
				)
			
			if self.mode == 'data-availability':
				return self.fetch_data_availability(
					sensor=sensor,
					time=time
				)
			
			raise ValueError( "Unsupported FIRMS mode. Use 'area' or 'data-availability'." )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			
			if not isinstance( parameters, dict ):
				raise ValueError(
					'parameters must be a dict of param_name -> schema definition.'
				)
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'fetchers'
			exception.cause = 'Firms'
			exception.method = (
					'create_schema( self, *args, **kwargs ) -> Dict[ str, str ] | None'
			)
			raise exception

class OpenSky( Fetcher ):
	"""Open Sky fetcher.
	
	Purpose:
		Coordinates OpenSky Network aircraft, airport, and state-vector data within Fonky. The
		class stores provider configuration, request parameters, response payloads, and
		normalized result state so callers can access the service through a consistent fetcher
		interface.
	
	Attributes:
		token_url (Optional[str]): token URL state retained by the instance.
		base_url (Optional[str]): base URL state retained by the instance.
		client_id (Optional[str]): client ID state retained by the instance.
		client_secret (Optional[str]): client secret state retained by the instance.
		access_token (Optional[str]): access token state retained by the instance.
		mode (Optional[str]): mode state retained by the instance.
		endpoint (Optional[str]): endpoint state retained by the instance.
		icao24 (Optional[str]): icao24 state retained by the instance.
		airport (Optional[str]): airport state retained by the instance.
		begin (Optional[int]): begin state retained by the instance.
		end (Optional[int]): end state retained by the instance.
		time_value (Optional[int]): time value state retained by the instance.
		lamin (Optional[float]): lamin state retained by the instance.
		lomin (Optional[float]): lomin state retained by the instance.
		lamax (Optional[float]): lamax state retained by the instance.
		lomax (Optional[float]): lomax state retained by the instance.
		extended (Optional[bool]): extended state retained by the instance.
		params (Optional[Dict[str, Any]]): params state retained by the instance.
		payload (Optional[Any]): payload state retained by the instance.
		result (Optional[Dict[str, Any]]): result state retained by the instance.
		agents (Optional[str]): agents state retained by the instance.
		timeout (object): timeout state retained by the instance.
		response (object): response state retained by the instance.
		url (object): URL state retained by the instance.
		headers (object): headers state retained by the instance."""
	token_url: Optional[ str ]
	base_url: Optional[ str ]
	client_id: Optional[ str ]
	client_secret: Optional[ str ]
	access_token: Optional[ str ]
	mode: Optional[ str ]
	endpoint: Optional[ str ]
	icao24: Optional[ str ]
	airport: Optional[ str ]
	begin: Optional[ int ]
	end: Optional[ int ]
	time_value: Optional[ int ]
	lamin: Optional[ float ]
	lomin: Optional[ float ]
	lamax: Optional[ float ]
	lomax: Optional[ float ]
	extended: Optional[ bool ]
	params: Optional[ Dict[ str, Any ] ]
	payload: Optional[ Any ]
	result: Optional[ Dict[ str, Any ] ]
	agents: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize OpenSky.
		
		Purpose:
			Initializes the OpenSky instance with default configuration, request state, response
			placeholders, and provider-specific options. The constructor prepares the object for
			later method calls without executing an external provider request."""
		super( ).__init__( )
		self.timeout = 20
		self.base_url = 'https://opensky-network.org/api'
		self.token_url = (
				'https://auth.opensky-network.org/auth/realms/opensky-network/'
				'protocol/openid-connect/token'
		)
		self.client_id = cfg.OPENSKY_API_CLIENT_ID
		self.client_secret = cfg.OPENSKY_API_CREDENTIALS
		self.access_token = None
		self.mode = 'states_bbox'
		self.endpoint = ''
		self.icao24 = ''
		self.airport = ''
		self.begin = None
		self.end = None
		self.time_value = None
		self.lamin = None
		self.lomin = None
		self.lamax = None
		self.lomax = None
		self.extended = False
		self.params = { }
		self.payload = None
		self.result = { }
		self.response = None
		self.url = None
		self.agents = cfg.AGENTS
		self.headers = {
				'Accept': 'application/json',
				'User-Agent': self.agents,
		}
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.
		
		Purpose:
			Returns a stable list of public attributes and methods exposed by the object. The method
			supports predictable introspection, documentation rendering, debugging, and
			user-interface option display.
		
		Returns:
			List[str]: Ordered public attribute and method names exposed by the object."""
		return [
				'timeout',
				'headers',
				'response',
				'url',
				'result',
				'query',
				'token_url',
				'base_url',
				'client_id',
				'client_secret',
				'access_token',
				'mode',
				'endpoint',
				'icao24',
				'airport',
				'begin',
				'end',
				'time_value',
				'lamin',
				'lomin',
				'lamax',
				'lomax',
				'extended',
				'params',
				'payload',
				'agents',
				'validate_mode',
				'validate_endpoint',
				'validate_icao24',
				'validate_airport',
				'validate_epoch',
				'validate_time_range',
				'validate_latitude',
				'validate_longitude',
				'validate_bbox',
				'assign_credentials',
				'authenticate',
				'request',
				'normalize_states',
				'normalize_flights',
				'normalize_track',
				'fetch_states',
				'fetch_flights_aircraft',
				'fetch_arrivals_airport',
				'fetch_departures_airport',
				'fetch_track_aircraft',
				'fetch',
				'create_schema'
		]
	
	def validate_mode( self, mode: str ) -> str:
		"""Validate mode.
		
		Purpose:
			Validates and normalizes mode before it is used in OpenSky Network aircraft, airport,
			and state-vector data. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			mode (str): mode value used by the validate mode operation.
		
		Returns:
			str: Validated mode value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'mode', mode )
			
			value = str( mode ).strip( ).lower( )
			allowed = {
					'states_bbox',
					'flights_aircraft',
					'arrivals_airport',
					'departures_airport',
					'track_aircraft'
			}
			
			if value not in allowed:
				raise ValueError(
					"Unsupported OpenSky mode. Use 'states_bbox', "
					"'flights_aircraft', 'arrivals_airport', "
					"'departures_airport', or 'track_aircraft'."
				)
			
			return value
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = 'validate_mode( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_endpoint( self, endpoint: str ) -> str:
		"""Validate endpoint.
		
		Purpose:
			Validates and normalizes endpoint before it is used in OpenSky Network aircraft,
			airport, and state-vector data. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			endpoint (str): endpoint value used by the validate endpoint operation.
		
		Returns:
			str: Validated endpoint value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'endpoint', endpoint )
			
			value = str( endpoint ).strip( )
			
			if value.startswith( 'http://' ) or value.startswith( 'https://' ):
				raise ValueError( 'endpoint must be a path segment, not a full URL.' )
			
			if '..' in value:
				raise ValueError( 'endpoint cannot contain parent-directory markers.' )
			
			allowed = {
					'/states/all',
					'/flights/aircraft',
					'/flights/arrival',
					'/flights/departure',
					'/tracks/all'
			}
			
			if value not in allowed:
				raise ValueError( 'Unsupported OpenSky endpoint path.' )
			
			return value
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = 'validate_endpoint( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_icao24( self, icao24: str ) -> str:
		"""Validate icao24.
		
		Purpose:
			Validates and normalizes icao24 before it is used in OpenSky Network aircraft, airport,
			and state-vector data. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			icao24 (str): icao24 value used by the validate icao24 operation.
		
		Returns:
			str: Validated icao24 value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'icao24', icao24 )
			
			value = str( icao24 ).strip( ).lower( )
			
			if not re.fullmatch( r'[0-9a-f]{6}', value ):
				raise ValueError( 'icao24 must be a six-character hexadecimal address.' )
			
			return value
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = 'validate_icao24( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_airport( self, airport: str ) -> str:
		"""Validate airport.
		
		Purpose:
			Validates and normalizes airport before it is used in OpenSky Network aircraft, airport,
			and state-vector data. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			airport (str): airport value used by the validate airport operation.
		
		Returns:
			str: Validated airport value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'airport', airport )
			
			value = str( airport ).strip( ).upper( )
			
			if not re.fullmatch( r'[A-Z0-9]{4}', value ):
				raise ValueError( 'airport must be a four-character ICAO airport code.' )
			
			return value
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = 'validate_airport( self, *args, **kwargs ) -> str'
			raise exception
	
	def validate_epoch( self, name: str, value: Any ) -> int:
		"""Validate epoch.
		
		Purpose:
			Validates and normalizes epoch before it is used in OpenSky Network aircraft, airport,
			and state-vector data. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			name (str): name value used by the validate epoch operation.
			value (object): value value used by the validate epoch operation.
		
		Returns:
			int: Validated epoch value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			throw_if( name, value )
			
			number = int( value )
			
			if number < 0:
				raise ValueError( f'{name} must be greater than or equal to 0.' )
			
			return number
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = 'validate_epoch( self, *args, **kwargs ) -> int'
			raise exception
	
	def validate_time_range( self, begin: int, end: int ) -> Tuple[ int, int ]:
		"""Validate time range.
		
		Purpose:
			Validates and normalizes time range before it is used in OpenSky Network aircraft,
			airport, and state-vector data. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			begin (int): begin value used by the validate time range operation.
			end (int): end value used by the validate time range operation.
		
		Returns:
			Tuple[int, int]: Validated time range value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			start = self.validate_epoch( 'begin', begin )
			stop = self.validate_epoch( 'end', end )
			
			if start > stop:
				raise ValueError( 'begin must be less than or equal to end.' )
			
			return start, stop
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = (
					'validate_time_range( self, *args, **kwargs ) -> Tuple[ int, int ]'
			)
			raise exception
	
	def validate_latitude( self, name: str, value: Any ) -> float:
		"""Validate latitude.
		
		Purpose:
			Validates and normalizes latitude before it is used in OpenSky Network aircraft,
			airport, and state-vector data. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			name (str): name value used by the validate latitude operation.
			value (object): value value used by the validate latitude operation.
		
		Returns:
			float: Validated latitude value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			throw_if( name, value )
			
			number = float( value )
			
			if number < -90.0 or number > 90.0:
				raise ValueError( f'{name} must be between -90 and 90.' )
			
			return number
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = 'validate_latitude( self, *args, **kwargs ) -> float'
			raise exception
	
	def validate_longitude( self, name: str, value: Any ) -> float:
		"""Validate longitude.
		
		Purpose:
			Validates and normalizes longitude before it is used in OpenSky Network aircraft,
			airport, and state-vector data. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			name (str): name value used by the validate longitude operation.
			value (object): value value used by the validate longitude operation.
		
		Returns:
			float: Validated longitude value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'name', name )
			throw_if( name, value )
			
			number = float( value )
			
			if number < -180.0 or number > 180.0:
				raise ValueError( f'{name} must be between -180 and 180.' )
			
			return number
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = 'validate_longitude( self, *args, **kwargs ) -> float'
			raise exception
	
	def validate_bbox( self, lamin: float, lomin: float,
			lamax: float, lomax: float ) -> Tuple[ float, float, float, float ]:
		"""Validate bbox.
		
		Purpose:
			Validates and normalizes bbox before it is used in OpenSky Network aircraft, airport,
			and state-vector data. The method converts incoming values to the expected
			representation, enforces visible range or format constraints, and returns the checked
			value for request construction.
		
		Args:
			lamin (float): lamin value used by the validate bbox operation.
			lomin (float): lomin value used by the validate bbox operation.
			lamax (float): lamax value used by the validate bbox operation.
			lomax (float): lomax value used by the validate bbox operation.
		
		Returns:
			Tuple[float, float, float, float]: Validated bbox value.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			min_lat = self.validate_latitude( 'lamin', lamin )
			min_lon = self.validate_longitude( 'lomin', lomin )
			max_lat = self.validate_latitude( 'lamax', lamax )
			max_lon = self.validate_longitude( 'lomax', lomax )
			
			if min_lat >= max_lat:
				raise ValueError( 'lamin must be less than lamax.' )
			
			if min_lon >= max_lon:
				raise ValueError( 'lomin must be less than lomax.' )
			
			return min_lat, min_lon, max_lat, max_lon
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = (
					'validate_bbox( self, *args, **kwargs ) '
					'-> Tuple[ float, float, float, float ]'
			)
			raise exception
	
	def assign_credentials( self, client_id: str = None,
			client_secret: str = None ) -> None:
		"""Assign credentials.
		
		Purpose:
			Performs the assign credentials operation for OpenSky Network aircraft, airport, and
			state-vector data. The method uses the class runtime state and supplied arguments to
			prepare, transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Args:
			client_id (str): Optional credential override used for the active request.
			client_secret (str): Optional credential override used for the active request.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if client_id is not None and str( client_id ).strip( ):
				self.client_id = str( client_id ).strip( )
			else:
				self.client_id = cfg.OPENSKY_API_CLIENT_ID
			
			if client_secret is not None and str( client_secret ).strip( ):
				self.client_secret = str( client_secret ).strip( )
			else:
				self.client_secret = cfg.OPENSKY_API_CREDENTIALS
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = (
					'assign_credentials( self, *args, **kwargs ) -> None'
			)
			raise exception
	
	def authenticate( self ) -> str | None:
		"""Authenticate.
		
		Purpose:
			Performs the authenticate operation for OpenSky Network aircraft, airport, and
			state-vector data. The method uses the class runtime state and supplied arguments to
			prepare, transform, dispatch, or package data for the broader Fonky fetching workflow.
		
		Returns:
			str | None: Result produced by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if not self.client_id or not self.client_secret:
				return None
			
			self.response = requests.post(
				url=self.token_url,
				data={
						'grant_type': 'client_credentials',
						'client_id': self.client_id,
						'client_secret': self.client_secret,
				},
				headers={
						'Accept': 'application/json',
						'User-Agent': self.agents,
				},
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			token_payload = self.response.json( ) or { }
			self.access_token = token_payload.get( 'access_token', None )
			
			if self.access_token:
				self.headers[ 'Authorization' ] = f'Bearer {self.access_token}'
			
			return self.access_token
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = 'authenticate( self ) -> str | None'
			raise exception
	
	def request( self, endpoint: str, params: Dict[ str, Any ] | None = None,
			client_id: str = None, client_secret: str = None ) -> Any:
		"""Request OpenSky Network aircraft, airport, and state-vector data.
		
		Purpose:
			Sends a provider request for OpenSky Network aircraft, airport, and state-vector data
			after request parameters have been validated or prepared by the caller. The method
			stores request, response, and payload state on the instance so subsequent methods can
			package or inspect the result consistently.
		
		Args:
			endpoint (str): endpoint value used by the request operation.
			params (Dict[str, Any] | None): Request or schema parameter dictionary used by the
				operation.
			client_id (str): Optional credential override used for the active request.
			client_secret (str): Optional credential override used for the active request.
		
		Returns:
			object: Normalized provider response, result payload, or document collection returned by
				the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.endpoint = self.validate_endpoint( endpoint )
			self.assign_credentials(
				client_id=client_id,
				client_secret=client_secret
			)
			self.authenticate( )
			
			self.url = f'{self.base_url}{self.endpoint}'
			self.params = { }
			
			for key, value in (params or { }).items( ):
				if value is None:
					continue
				
				if isinstance( value, str ) and not value.strip( ):
					continue
				
				self.params[ key ] = value
			
			self.response = requests.get(
				url=self.url,
				params=self.params,
				headers=self.headers,
				timeout=self.timeout
			)
			self.response.raise_for_status( )
			self.payload = self.response.json( )
			
			return self.payload
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = 'request( self, *args, **kwargs ) -> Any'
			raise exception
	
	def normalize_states( self, payload: Dict[ str, Any ] | None ) -> Dict[ str, Any ] | None:
		"""Normalize states.
		
		Purpose:
			Converts states into the canonical format expected by the OpenSky request workflow. The
			method standardizes caller input before it is used in endpoint paths, query parameters,
			filters, or response processing.
		
		Args:
			payload (Dict[str, Any] | None): payload value used by the normalize states operation.
		
		Returns:
			Dict[str, Any] | None: Canonical value prepared for request construction or response
				processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			states = [ ]
			
			if isinstance( payload, dict ):
				states = payload.get( 'states', [ ] ) or [ ]
			
			items: List[ Dict[ str, Any ] ] = [ ]
			
			for row in states:
				if not isinstance( row, list ):
					continue
				
				items.append(
					{
							'icao24': row[ 0 ] if len( row ) > 0 else None,
							'callsign': (
									str( row[ 1 ] ).strip( )
									if len( row ) > 1 and row[ 1 ] is not None
									else None
							),
							'origin_country': row[ 2 ] if len( row ) > 2 else None,
							'time_position': row[ 3 ] if len( row ) > 3 else None,
							'last_contact': row[ 4 ] if len( row ) > 4 else None,
							'longitude': row[ 5 ] if len( row ) > 5 else None,
							'latitude': row[ 6 ] if len( row ) > 6 else None,
							'baro_altitude_m': row[ 7 ] if len( row ) > 7 else None,
							'on_ground': row[ 8 ] if len( row ) > 8 else None,
							'velocity_mps': row[ 9 ] if len( row ) > 9 else None,
							'true_track_deg': row[ 10 ] if len( row ) > 10 else None,
							'vertical_rate_mps': row[ 11 ] if len( row ) > 11 else None,
							'sensors': row[ 12 ] if len( row ) > 12 else None,
							'geo_altitude_m': row[ 13 ] if len( row ) > 13 else None,
							'squawk': row[ 14 ] if len( row ) > 14 else None,
							'spi': row[ 15 ] if len( row ) > 15 else None,
							'position_source': row[ 16 ] if len( row ) > 16 else None,
					}
				)
			
			self.result = {
					'mode': 'states_bbox',
					'time': payload.get( 'time', None ) if isinstance( payload, dict ) else None,
					'count': len( items ),
					'items': items,
			}
			
			return self.result
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = (
					'normalize_states( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def normalize_flights( self, payload: List[ Dict[ str, Any ] ] | None,
			mode: str ) -> Dict[ str, Any ] | None:
		"""Normalize flights.
		
		Purpose:
			Converts flights into the canonical format expected by the OpenSky request workflow. The
			method standardizes caller input before it is used in endpoint paths, query parameters,
			filters, or response processing.
		
		Args:
			payload (List[Dict[str, Any]] | None): payload value used by the normalize flights
				operation.
			mode (str): mode value used by the normalize flights operation.
		
		Returns:
			Dict[str, Any] | None: Canonical value prepared for request construction or response
				processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			items: List[ Dict[ str, Any ] ] = [ ]
			
			for row in payload or [ ]:
				if not isinstance( row, dict ):
					continue
				
				items.append(
					{
							'icao24': row.get( 'icao24' ),
							'first_seen': row.get( 'firstSeen' ),
							'est_departure_airport': row.get( 'estDepartureAirport' ),
							'last_seen': row.get( 'lastSeen' ),
							'est_arrival_airport': row.get( 'estArrivalAirport' ),
							'callsign': row.get( 'callsign' ),
							'est_departure_airport_horiz_distance_m':
								row.get( 'estDepartureAirportHorizDistance' ),
							'est_departure_airport_vert_distance_m':
								row.get( 'estDepartureAirportVertDistance' ),
							'est_arrival_airport_horiz_distance_m':
								row.get( 'estArrivalAirportHorizDistance' ),
							'est_arrival_airport_vert_distance_m':
								row.get( 'estArrivalAirportVertDistance' ),
							'departure_airport_candidates_count':
								row.get( 'departureAirportCandidatesCount' ),
							'arrival_airport_candidates_count':
								row.get( 'arrivalAirportCandidatesCount' ),
					}
				)
			
			self.result = {
					'mode': mode,
					'count': len( items ),
					'items': items,
			}
			
			return self.result
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = (
					'normalize_flights( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def normalize_track( self, payload: Dict[ str, Any ] | None ) -> Dict[ str, Any ] | None:
		"""Normalize track.
		
		Purpose:
			Converts track into the canonical format expected by the OpenSky request workflow. The
			method standardizes caller input before it is used in endpoint paths, query parameters,
			filters, or response processing.
		
		Args:
			payload (Dict[str, Any] | None): payload value used by the normalize track operation.
		
		Returns:
			Dict[str, Any] | None: Canonical value prepared for request construction or response
				processing.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			if not payload:
				self.result = {
						'mode': 'track_aircraft',
						'icao24': None,
						'callsign': None,
						'start_time': None,
						'end_time': None,
						'count': 0,
						'items': [ ],
				}
				return self.result
			
			path = payload.get( 'path' ) or [ ]
			items: List[ Dict[ str, Any ] ] = [ ]
			
			for row in path:
				if not isinstance( row, list ):
					continue
				
				items.append(
					{
							'time': row[ 0 ] if len( row ) > 0 else None,
							'latitude': row[ 1 ] if len( row ) > 1 else None,
							'longitude': row[ 2 ] if len( row ) > 2 else None,
							'baro_altitude_m': row[ 3 ] if len( row ) > 3 else None,
							'true_track_deg': row[ 4 ] if len( row ) > 4 else None,
							'on_ground': row[ 5 ] if len( row ) > 5 else None,
					}
				)
			
			self.result = {
					'mode': 'track_aircraft',
					'icao24': payload.get( 'icao24' ),
					'callsign': payload.get( 'callsign' ) or payload.get( 'calllsign' ),
					'start_time': payload.get( 'startTime' ),
					'end_time': payload.get( 'endTime' ),
					'count': len( items ),
					'items': items,
			}
			
			return self.result
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = (
					'normalize_track( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_states( self, icao24: str = '', time_value: int = None,
			lamin: float | None = None, lomin: float | None = None,
			lamax: float | None = None, lomax: float | None = None,
			extended: bool = False, client_id: str = None,
			client_secret: str = None ) -> Dict[ str, Any ] | None:
		"""Fetch states.
		
		Purpose:
			Retrieves states using validated arguments and the stored OpenSky runtime configuration.
			The method assembles request parameters, executes the provider call or dispatches to a
			specialized helper, records response state when applicable, and returns a normalized
			payload for downstream analysis or tool execution.
		
		Args:
			icao24 (str): icao24 value used by the fetch states operation.
			time_value (int): time value value used by the fetch states operation.
			lamin (float | None): lamin value used by the fetch states operation.
			lomin (float | None): lomin value used by the fetch states operation.
			lamax (float | None): lamax value used by the fetch states operation.
			lomax (float | None): lomax value used by the fetch states operation.
			extended (bool): extended value used by the fetch states operation.
			client_id (str): Optional credential override used for the active request.
			client_secret (str): Optional credential override used for the active request.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'states_bbox'
			self.icao24 = self.validate_icao24( icao24 ) if str( icao24 or '' ).strip( ) else ''
			self.time_value = (
					self.validate_epoch( 'time_value', time_value )
					if time_value is not None
					else None
			)
			self.extended = bool( extended )
			
			self.params = { }
			
			if self.time_value is not None:
				self.params[ 'time' ] = self.time_value
			
			if self.icao24:
				self.params[ 'icao24' ] = self.icao24
			
			has_bbox = all(
				value is not None
				for value in [ lamin, lomin, lamax, lomax ]
			)
			
			partial_bbox = any(
				value is not None
				for value in [ lamin, lomin, lamax, lomax ]
			)
			
			if partial_bbox and not has_bbox:
				raise ValueError(
					'lamin, lomin, lamax, and lomax must all be supplied together.'
				)
			
			if has_bbox:
				self.lamin, self.lomin, self.lamax, self.lomax = self.validate_bbox(
					lamin=lamin,
					lomin=lomin,
					lamax=lamax,
					lomax=lomax
				)
				self.params[ 'lamin' ] = self.lamin
				self.params[ 'lomin' ] = self.lomin
				self.params[ 'lamax' ] = self.lamax
				self.params[ 'lomax' ] = self.lomax
			
			if self.extended:
				self.params[ 'extended' ] = 1
			
			self.payload = self.request(
				'/states/all',
				params=self.params,
				client_id=client_id,
				client_secret=client_secret
			)
			
			return self.normalize_states( self.payload )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = (
					'fetch_states( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_flights_aircraft( self, icao24: str, begin: int, end: int,
			client_id: str = None, client_secret: str = None ) -> Dict[ str, Any ] | None:
		"""Fetch flights aircraft.
		
		Purpose:
			Retrieves flights aircraft using validated arguments and the stored OpenSky runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			icao24 (str): icao24 value used by the fetch flights aircraft operation.
			begin (int): begin value used by the fetch flights aircraft operation.
			end (int): end value used by the fetch flights aircraft operation.
			client_id (str): Optional credential override used for the active request.
			client_secret (str): Optional credential override used for the active request.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'flights_aircraft'
			self.icao24 = self.validate_icao24( icao24 )
			self.begin, self.end = self.validate_time_range( begin, end )
			self.params = {
					'icao24': self.icao24,
					'begin': self.begin,
					'end': self.end,
			}
			
			self.payload = self.request(
				'/flights/aircraft',
				params=self.params,
				client_id=client_id,
				client_secret=client_secret
			)
			
			return self.normalize_flights( self.payload, self.mode )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = (
					'fetch_flights_aircraft( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_arrivals_airport( self, airport: str, begin: int, end: int,
			client_id: str = None, client_secret: str = None ) -> Dict[ str, Any ] | None:
		"""Fetch arrivals airport.
		
		Purpose:
			Retrieves arrivals airport using validated arguments and the stored OpenSky runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			airport (str): airport value used by the fetch arrivals airport operation.
			begin (int): begin value used by the fetch arrivals airport operation.
			end (int): end value used by the fetch arrivals airport operation.
			client_id (str): Optional credential override used for the active request.
			client_secret (str): Optional credential override used for the active request.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'arrivals_airport'
			self.airport = self.validate_airport( airport )
			self.begin, self.end = self.validate_time_range( begin, end )
			self.params = {
					'airport': self.airport,
					'begin': self.begin,
					'end': self.end,
			}
			
			self.payload = self.request(
				'/flights/arrival',
				params=self.params,
				client_id=client_id,
				client_secret=client_secret
			)
			
			return self.normalize_flights( self.payload, self.mode )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = (
					'fetch_arrivals_airport( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch_departures_airport( self, airport: str, begin: int, end: int,
			client_id: str = None, client_secret: str = None ) -> Dict[ str, Any ] | None:
		"""Fetch departures airport.
		
		Purpose:
			Retrieves departures airport using validated arguments and the stored OpenSky runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			airport (str): airport value used by the fetch departures airport operation.
			begin (int): begin value used by the fetch departures airport operation.
			end (int): end value used by the fetch departures airport operation.
			client_id (str): Optional credential override used for the active request.
			client_secret (str): Optional credential override used for the active request.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'departures_airport'
			self.airport = self.validate_airport( airport )
			self.begin, self.end = self.validate_time_range( begin, end )
			self.params = {
					'airport': self.airport,
					'begin': self.begin,
					'end': self.end,
			}
			
			self.payload = self.request(
				'/flights/departure',
				params=self.params,
				client_id=client_id,
				client_secret=client_secret
			)
			
			return self.normalize_flights( self.payload, self.mode )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = 'fetch_departures_airport( self, *args, **kwargs ) -> Dict[str, Any]'
			raise exception
	
	def fetch_track_aircraft( self, icao24: str, time_value: int = None,
			client_id: str = None, client_secret: str = None ) -> Dict[ str, Any ] | None:
		"""Fetch track aircraft.
		
		Purpose:
			Retrieves track aircraft using validated arguments and the stored OpenSky runtime
			configuration. The method assembles request parameters, executes the provider call or
			dispatches to a specialized helper, records response state when applicable, and returns
			a normalized payload for downstream analysis or tool execution.
		
		Args:
			icao24 (str): icao24 value used by the fetch track aircraft operation.
			time_value (int): time value value used by the fetch track aircraft operation.
			client_id (str): Optional credential override used for the active request.
			client_secret (str): Optional credential override used for the active request.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.mode = 'track_aircraft'
			self.icao24 = self.validate_icao24( icao24 )
			self.time_value = (self.validate_epoch( 'time_value', time_value )
			                   if time_value is not None else 0)
			self.params = { 'icao24': self.icao24, 'time': self.time_value, }
			
			self.payload = self.request( '/tracks/all', params=self.params, client_id=client_id,
				client_secret=client_secret )
			
			return self.normalize_track( self.payload )
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = (
					'fetch_track_aircraft( self, *args, **kwargs ) '
					'-> Dict[ str, Any ] | None'
			)
			raise exception
	
	def fetch( self, mode: str = 'states_bbox', icao24: str = '', airport: str = '',
			begin: int = None, end: int = None, time_value: int = None,
			lamin: float | None = None, lomin: float | None = None,
			lamax: float | None = None, lomax: float | None = None,
			extended: bool = False, client_id: str = None,
			client_secret: str = None, time: int = 20 ) -> Dict[ str, Any ] | None:
		"""Fetch OpenSky Network aircraft, airport, and state-vector data.
		
		Purpose:
			Retrieves OpenSky Network aircraft, airport, and state-vector data using validated
			arguments and the stored OpenSky runtime configuration. The method assembles request
			parameters, executes the provider call or dispatches to a specialized helper, records
			response state when applicable, and returns a normalized payload for downstream analysis
			or tool execution.
		
		Args:
			mode (str): mode value used by the fetch operation.
			icao24 (str): icao24 value used by the fetch operation.
			airport (str): airport value used by the fetch operation.
			begin (int): begin value used by the fetch operation.
			end (int): end value used by the fetch operation.
			time_value (int): time value value used by the fetch operation.
			lamin (float | None): lamin value used by the fetch operation.
			lomin (float | None): lomin value used by the fetch operation.
			lamax (float | None): lamax value used by the fetch operation.
			lomax (float | None): lomax value used by the fetch operation.
			extended (bool): extended value used by the fetch operation.
			client_id (str): Optional credential override used for the active request.
			client_secret (str): Optional credential override used for the active request.
			time (int): Request timeout in seconds.
		
		Returns:
			Dict[str, Any] | None: Normalized provider response, result payload, or document
				collection returned by the operation.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			self.timeout = int( time )
			self.mode = self.validate_mode( mode )
			
			if self.timeout < 1:
				raise ValueError( 'time must be greater than or equal to 1.' )
			
			if self.mode == 'states_bbox':
				return self.fetch_states(
					icao24=icao24,
					time_value=time_value,
					lamin=lamin,
					lomin=lomin,
					lamax=lamax,
					lomax=lomax,
					extended=extended,
					client_id=client_id,
					client_secret=client_secret
				)
			
			if self.mode == 'flights_aircraft':
				return self.fetch_flights_aircraft(
					icao24=icao24,
					begin=begin,
					end=end,
					client_id=client_id,
					client_secret=client_secret
				)
			
			if self.mode == 'arrivals_airport':
				return self.fetch_arrivals_airport(
					airport=airport,
					begin=begin,
					end=end,
					client_id=client_id,
					client_secret=client_secret
				)
			
			if self.mode == 'departures_airport':
				return self.fetch_departures_airport(
					airport=airport,
					begin=begin,
					end=end,
					client_id=client_id,
					client_secret=client_secret
				)
			
			if self.mode == 'track_aircraft':
				return self.fetch_track_aircraft(
					icao24=icao24,
					time_value=time_value,
					client_id=client_id,
					client_secret=client_secret
				)
			
			raise ValueError(
				"Unsupported mode. Use 'states_bbox', 'flights_aircraft', "
				"'arrivals_airport', 'departures_airport', or 'track_aircraft'."
			)
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = (
					'fetch( self, *args, **kwargs ) -> Dict[ str, Any ] | None'
			)
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict,
			required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create an AI tool schema.
		
		Purpose:
			Builds a compact function schema for exposing a fetcher operation to AI tool-calling
			workflows. The method combines the public function name, service label, description,
			parameter schema, and required-field list into the structure consumed by downstream tool
			registries.
		
		Args:
			function (str): function value used by the create schema operation.
			tool (str): tool value used by the create schema operation.
			description (str): description value used by the create schema operation.
			parameters (dict): Request or schema parameter dictionary used by the operation.
			required (list[str]): Parameter names that should be marked as required in the generated
				schema.
		
		Returns:
			Dict[str, str] | None: Function schema dictionary used by downstream AI tool-calling
				integrations.
		
		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application
				logger."""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			if not isinstance( parameters, dict ):
				raise ValueError( 'parameters must be a dict of param_name -> schema definition.' )
			
			if required is None:
				required = list( parameters.keys( ) )
			
			return {
					'name': function.strip( ),
					'description': (
							f'{description.strip( )} This function uses the '
							f'{tool.strip( )} service.'
					),
					'parameters': {
							'type': 'object',
							'properties': parameters,
							'required': required,
					}
			}
		
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'fetchers'
			exception.cause = 'OpenSky'
			exception.method = 'create_schema( self, *args, **kwargs ) -> Dict[ str, str ]'
			raise exception