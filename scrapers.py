'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                scrapers.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="scrapers.py" company="Terry D. Eppler">

	     scrapers.py
	     Copyright ©  2022  Terry Eppler

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
    Provides synchronous HTML scraping and extraction utilities for Fonky.

    Purpose:
        Defines lightweight scraper classes used to retrieve HTML pages and extract common
        structures such as paragraphs, lists, tables, articles, headings, divisions, sections,
        blockquotes, hyperlinks, and image references. The module complements the broader
        fetcher layer with focused extraction methods and standard wrapped exception logging.
  </summary>
  ******************************************************************************************
  '''
from __future__ import annotations

import re
from typing import Dict, List, Optional, Pattern

import requests
from bs4 import BeautifulSoup
from requests import Response
import config as cfg
from boogr import Error, Logger
from core import Result

def throw_if( name: str, value: object ) -> None:
	"""Validate a required value.

	Purpose:
		Provides a small guard for scraper inputs before HTTP requests or HTML extraction
		operations are attempted. The function rejects ``None`` values and blank strings so
		callers receive deterministic validation errors instead of downstream request or parser
		failures.

	Args:
		name (str): Name of the argument being validated.
		value (object): Value to validate.

	Raises:
		ValueError: Raised when ``value`` is ``None`` or an empty string.
	"""
	if value is None:
		raise ValueError( f'Argument "{name}" cannot be None.' )
	
	if isinstance( value, str ) and not value.strip( ):
		raise ValueError( f'Argument "{name}" cannot be empty.' )

class Extractor( ):
	"""Provide shared state for HTML extraction classes.

	Purpose:
		Defines the minimal base state used by concrete scraper implementations that retrieve
		raw HTML, parse it with BeautifulSoup, and store extracted text. The class provides a
		common inspection surface for extraction-oriented subclasses without performing network
		or parsing work by itself.

	Attributes:
		raw_html (Optional[str]): Raw HTML captured for extraction.
		extracted_text (Optional[str]): Extracted text generated from the source HTML.
		soup (Optional[BeautifulSoup]): Parsed BeautifulSoup document tree.
	"""
	raw_html: Optional[ str ]
	extracted_text: Optional[ str ]
	soup: Optional[ BeautifulSoup ]
	
	def __init__( self ):
		"""Initialize extraction state.

		Purpose:
			Initializes the base extractor fields to empty state so subclasses can store raw
			HTML, parsed HTML, and extracted text consistently during later scrape operations.
		"""
		self.raw_html = None
		self.extracted_text = None
		self.soup = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return extractor inspection names.

		Purpose:
			Provides a stable list of member names for interactive inspection, documentation,
			and simple tooling that displays extractor state.

		Returns:
			Ordered extractor member names.
		"""
		return [ 'raw_html', 'extract' ]

class WebExtractor( Extractor ):
	"""Fetch and extract selected structures from HTML pages.

	Purpose:
		Provides synchronous HTML retrieval through ``requests`` and extraction helpers for
		common HTML structures. The class stores request state, parser state, regular
		expressions, and headers so individual scrape methods can request a page and return
		only the requested type of extracted content.

	Attributes:
		soup (Optional[BeautifulSoup]): Parsed BeautifulSoup document tree.
		agents (Optional[str]): User-agent string loaded from configuration.
		url (Optional[str]): URL used for the active scrape request.
		html (Optional[str]): Raw HTML text retained by the extractor.
		re_tag (Optional[Pattern]): Compiled tag-removal regular expression.
		re_ws (Optional[Pattern]): Compiled whitespace-normalization regular expression.
		response (Optional[Response]): Most recent HTTP response.
	"""
	soup: Optional[ BeautifulSoup ]
	agents: Optional[ str ]
	url: Optional[ str ]
	html: Optional[ str ]
	re_tag: Optional[ Pattern ]
	re_ws: Optional[ Pattern ]
	response: Optional[ Response ]
	
	def __init__( self ) -> None:
		"""Initialize the web extractor.

		Purpose:
			Initializes request defaults, compiled regular expressions, response state, and
			HTTP headers used by synchronous HTML extraction methods. The constructor prepares
			the object for later network calls without performing any external request.
		"""
		super( ).__init__( )
		self.timeout = 10
		self.re_tag = re.compile( r'<[^>]+>' )
		self.re_ws = re.compile( r'\s+' )
		self.url = None
		self.html = None
		self.response = None
		self.headers = { }
		self.agents = cfg.AGENTS
		if 'User-Agent' not in self.headers:
			self.headers[ 'User-Agent' ] = self.agents
	
	def __dir__( self ) -> List[ str ]:
		"""Return web extractor inspection names.

		Purpose:
			Provides a stable ordering of public attributes and extraction methods for
			interactive inspection, debugging, and documentation tooling.

		Returns:
			Ordered attribute and method names exposed by the extractor.
		"""
		return [ 'agents',
		         'url',
		         'html',
		         'timeout',
		         'headers',
		         'fetch',
		         'html_to_text',
		         'scrape_images',
		         'scrape_hyperlinks',
		         'scrape_images',
		         'scrape_hyperlinks',
		         'scrape_blockquotes',
		         'scrape_sections',
		         'scrape_divisions',
		         'sracpe_headings',
		         'scrape_tables',
		         'scrape_lists',
		         'scrape_paragraphse', ]
	
	def scrape( self, url: str, time: int = 10 ) -> Result | None:
		"""Fetch a web page.

		Purpose:
			Performs a synchronous HTTP GET request for the supplied URL, stores the response
			and timeout state, validates HTTP success, and returns the canonical Fonky
			``Result`` wrapper for downstream inspection or serialization.

		Args:
			url (str): Absolute URL to fetch.
			time (int): Request timeout in seconds.

		Returns:
			Result wrapper for the successful HTTP response.

		Raises:
			Error: Re-raised after the exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'url', url )
			self.url = url
			self.timeout = time
			self.response = requests.get( url=self.url, headers=self.headers,
				timeout=self.timeout )
			self.response.raise_for_status( )
			self.result = Result( self.response )
			return self.result
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'scrapers'
			exception.cause = 'WebFetcher'
			exception.method = 'fetch( self, url: str, time: int=10  ) -> Result'
			Logger( ).write( exception )
			raise exception
	
	def html_to_text( self, html: str ) -> str:
		"""Convert HTML to plain text.

		Purpose:
			Removes script and style blocks, inserts spacing around common block-level tags,
			strips remaining HTML markup, and normalizes whitespace into compact readable text.

		Args:
			html (str): Raw HTML string to convert.

		Returns:
			Plain text extracted from the supplied HTML.

		Raises:
			Error: Re-raised after the exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'html', html )
			html = re.sub( r'<script[\s\S]*?</script>', ' ', html, flags=re.IGNORECASE )
			html = re.sub( r'<style[\s\S]*?</style>', ' ', html, flags=re.IGNORECASE )
			html = re.sub( r'</?(p|div|br|li|h[1-6])[^>]*>', '\n', html, flags=re.IGNORECASE )
			text = re.sub( self.re_tag, ' ', html )
			text = re.sub( self.re_ws, ' ', text ).strip( )
			return text
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'scrapers'
			exception.cause = 'WebFetchers'
			exception.method = 'html2text( )'
			Logger( ).write( exception )
			raise exception
	
	def scrape_paragraphs( self, uri: str ) -> List[ str ] | None:
		"""Extract paragraph text.

		Purpose:
			Fetches the target HTML document, parses it with BeautifulSoup, extracts readable
			text from all ``p`` elements, and returns only non-empty paragraph strings.

		Args:
			uri (str): Fully qualified URI of the target HTML document.

		Returns:
			Cleaned paragraph text entries.

		Raises:
			Error: Re-raised after the exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'uri', uri )
			self.response = requests.get( uri, timeout=10 )
			self.response.raise_for_status( )
			self.soup = BeautifulSoup( self.response.text, 'html.parser' )
			blocks = [ p.get_text( ' ', strip=True ) for p in self.soup.find_all( 'p' ) ]
			return [ b for b in blocks if b ]
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'scrapers'
			exception.cause = 'WebExtractor'
			exception.method = 'scrape_paragraphs( self, uri: str ) -> List[ str ]'
			Logger( ).write( exception )
			raise exception
	
	def scrape_lists( self, uri: str ) -> List[ str ] | None:
		"""Extract list item text.

		Purpose:
			Fetches the target HTML document, parses it with BeautifulSoup, extracts readable
			text from all ``li`` elements, and returns only non-empty list item strings.

		Args:
			uri (str): Fully qualified URI of the target HTML page.

		Returns:
			Clean list item text segments.

		Raises:
			Error: Re-raised after the exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'uri', uri )
			self.response = requests.get( uri, timeout=10 )
			self.response.raise_for_status( )
			self.soup = BeautifulSoup( self.response.text, 'html.parser' )
			items = [ li.get_text( ' ', strip=True ) for li in self.soup.find_all( 'li' ) ]
			return [ i for i in items if i ]
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'scrapers'
			exception.cause = 'WebExtractor'
			exception.method = 'scrape_lists( self, uri: str ) -> List[ str ]'
			Logger( ).write( exception )
			raise exception
	
	def scrape_tables( self, uri: str ) -> List[ str ] | None:
		"""Extract table cell text.

		Purpose:
			Fetches the target HTML document, parses all ``table`` structures, and returns a
			flattened list of readable text from ``td`` and ``th`` cells.

		Args:
			uri (str): Fully qualified URI of the target HTML document.

		Returns:
			Table cell values extracted from all table rows.

		Raises:
			Error: Re-raised after the exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'uri', uri )
			self.response = requests.get( uri, timeout=10 )
			self.response.raise_for_status( )
			self.soup = BeautifulSoup( self.response.text, 'html.parser' )
			_results: List[ str ] = [ ]
			for table in self.soup.find_all( 'table' ):
				for row in table.find_all( 'tr' ):
					for cell in row.find_all( [ 'td',
					                            'th' ] ):
						text = cell.get_text( ' ', strip=True )
						if text:
							_results.append( text )
			
			return _results
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'scrapers'
			exception.cause = 'WebExtractor'
			exception.method = 'scrape_tables( self, uri: str ) -> List[ str ]'
			Logger( ).write( exception )
			raise exception
	
	def scrape_articles( self, uri: str ) -> List[ str ] | None:
		"""Extract article text.

		Purpose:
			Fetches the target HTML page, parses it with BeautifulSoup, extracts consolidated
			readable text from each ``article`` element, and returns only non-empty article
			blocks.

		Args:
			uri (str): Fully qualified URI of the target HTML page.

		Returns:
			Article-level text blocks.

		Raises:
			Error: Re-raised after the exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'uri', uri )
			self.response = requests.get( uri, timeout=10 )
			self.response.raise_for_status( )
			self.soup = BeautifulSoup( self.response.text, 'html.parser' )
			blocks = [ art.get_text( " ", strip=True ) for art in self.soup.find_all( 'article' ) ]
			return [ b for b in blocks if b ]
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'scrapers'
			exception.cause = 'WebExtractor'
			exception.method = 'scrape_articles( self, uri: str ) -> List[ str ]'
			Logger( ).write( exception )
			raise exception
	
	def scrape_headings( self, uri: str ) -> List[ str ] | None:
		"""Extract heading text.

		Purpose:
			Fetches the target HTML document, parses it with BeautifulSoup, extracts readable
			text from heading tags ``h1`` through ``h6``, and returns only non-empty headings.

		Args:
			uri (str): Fully qualified URI of the target HTML document.

		Returns:
			Clean heading strings.

		Raises:
			Error: Re-raised after the exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'uri', uri )
			self.response = requests.get( uri, timeout=10 )
			self.response.raise_for_status( )
			self.soup = BeautifulSoup( self.response.text, 'html.parser' )
			heading_tags = [ 'h1',
			                 'h2',
			                 'h3',
			                 'h4',
			                 'h5',
			                 'h6' ]
			blocks = [ h.get_text( ' ', strip=True ) for h in self.soup.find_all( heading_tags ) ]
			return [ b for b in blocks if b ]
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'scrapers'
			exception.cause = 'WebExtractor'
			exception.method = 'scrape_headings( self, uri: str ) -> List[ str ]'
			Logger( ).write( exception )
			raise exception
	
	def scrape_divisions( self, uri: str ) -> List[ str ] | None:
		"""Extract division text.

		Purpose:
			Fetches the target HTML document, parses it with BeautifulSoup, extracts readable
			text from ``div`` elements, and returns only non-empty division text blocks.

		Args:
			uri (str): Fully qualified URI of the target HTML document.

		Returns:
			Clean division text blocks.

		Raises:
			Error: Re-raised after the exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'uri', uri )
			self.response = requests.get( uri, timeout=10 )
			self.response.raise_for_status( )
			self.soup = BeautifulSoup( self.response.text, 'html.parser' )
			blocks = [ div.get_text( " ", strip=True ) for div in self.soup.find_all( 'div' ) ]
			return [ b for b in blocks if b ]
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'scrapers'
			exception.cause = 'WebExtractor'
			exception.method = 'scrape_divisions( self, uri: str ) -> List[ str ]'
			Logger( ).write( exception )
			raise exception
	
	def scrape_sections( self, uri: str ) -> List[ str ] | None:
		"""Extract section text.

		Purpose:
			Fetches the target HTML document, parses it with BeautifulSoup, extracts readable
			text from ``section`` elements, and returns only non-empty section text blocks.

		Args:
			uri (str): Fully qualified URI of the target HTML document.

		Returns:
			Clean section text blocks.

		Raises:
			Error: Re-raised after the exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'uri', uri )
			self.response = requests.get( uri, timeout=10 )
			self.response.raise_for_status( )
			self.soup = BeautifulSoup( self.response.text, 'html.parser' )
			blocks = [ sec.get_text( " ", strip=True ) for sec in self.soup.find_all( 'section' ) ]
			return [ b for b in blocks if b ]
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'scrapers'
			exception.cause = 'WebExtractor'
			exception.method = 'scrape_sections( self, uri: str ) -> List[ str ]'
			Logger( ).write( exception )
			raise exception
	
	def scrape_blockquotes( self, uri: str ) -> List[ str ] | None:
		"""Extract blockquote text.

		Purpose:
			Fetches the target HTML document, parses it with BeautifulSoup, extracts readable
			text from ``blockquote`` elements, and returns only non-empty quoted text entries.

		Args:
			uri (str): Fully qualified URI of the target HTML document.

		Returns:
			Cleaned blockquote text entries.

		Raises:
			Error: Re-raised after the exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'uri', uri )
			self.response = requests.get( uri, timeout=10 )
			self.response.raise_for_status( )
			self.soup = BeautifulSoup( self.response.text, 'html.parser' )
			blocks = [ bq.get_text( ' ', strip=True ) for bq in self.soup.find_all( 'blockquote' ) ]
			return [ b for b in blocks if b ]
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'scrapers'
			exception.cause = 'WebExtractor'
			exception.method = 'scrape_blockquotes( self, uri: str ) -> List[ str ]'
			Logger( ).write( exception )
			raise exception
	
	def scrape_hyperlinks( self, uri: str ) -> List[ str ] | None:
		"""Extract hyperlinks.

		Purpose:
			Fetches the target HTML document, parses it with BeautifulSoup, extracts ``href``
			values from anchor tags, and returns only populated hyperlink values.

		Args:
			uri (str): Fully qualified URI of the target HTML page.

		Returns:
			Hyperlink paths or URLs extracted from anchor tags.

		Raises:
			Error: Re-raised after the exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'uri', uri )
			self.response = requests.get( uri, timeout=10 )
			self.response.raise_for_status( )
			self.soup = BeautifulSoup( self.response.text, 'html.parser' )
			links = [ a.get( 'href' ) for a in self.soup.find_all( 'a' ) if a.get( 'href' ) ]
			return links
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'scrapers'
			exception.cause = 'WebExtractor'
			exception.method = 'scrape_hyperlinks( self, uri: str ) -> List[ str ]'
			Logger( ).write( exception )
			raise exception
	
	def scrape_images( self, uri: str ) -> List[ str ] | None:
		"""Extract image references.

		Purpose:
			Fetches the target HTML document, parses it with BeautifulSoup, extracts ``src``
			values from image tags, and returns only populated image references.

		Args:
			uri (str): Fully qualified URI of the target HTML page.

		Returns:
			Image source values extracted from image tags.

		Raises:
			Error: Re-raised after the exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'uri', uri )
			self.response = requests.get( uri, timeout=10 )
			self.response.raise_for_status( )
			self.soup = BeautifulSoup( self.response.text, 'html.parser' )
			images = [ img.get( 'src' ) for img in self.soup.find_all( 'img' ) if img.get( 'src' ) ]
			return images
		except Exception as exc:
			exception = Error( exc )
			exception.module = 'scrapers'
			exception.cause = 'WebExtractor'
			exception.method = 'scrape_images( self, uri: str ) -> List[ str ] '
			Logger( ).write( exception )
			raise exception
	
	def create_schema( self, function: str, tool: str,
			description: str, parameters: dict, required: list[ str ] ) -> Dict[ str, str ] | None:
		"""Create a dynamic tool schema.

		Purpose:
			Constructs an OpenAI-style function tool schema from the supplied function name,
			service name, description, parameter schema, and required field list. The method
			validates required inputs and preserves the caller-provided JSON-schema fragments
			for individual parameters.

		Args:
			function (str): Function name exposed to the model or tool caller.
			tool (str): Underlying system or service wrapped by the function.
			description (str): Description of what the function does.
			parameters (dict): JSON-schema property definitions keyed by parameter name.
			required (list[str]): Required parameter names. When ``None``, all parameter keys are used.

		Returns:
			JSON-compatible dictionary defining the tool schema.

		Raises:
			ValueError: Raised when ``parameters`` is not a dictionary.
			Error: Re-raised after the exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'function', function )
			throw_if( 'tool', tool )
			throw_if( 'description', description )
			throw_if( 'parameters', parameters )
			if not isinstance( parameters, dict ):
				msg = 'parameters must be a dict of param_name → schema definitions.'
				raise ValueError( msg )
			func_name = function.strip( )
			tool_name = tool.strip( )
			desc = description.strip( )
			if required is None:
				required = list( parameters.keys( ) )
			_schema = \
				{
						'name': func_name,
						'description': f'{desc} This function uses the {tool_name} service.',
						'parameters':
							{
									'type': 'object',
									'properties': parameters,
									'required': required
							}
				}
			return _schema
		except Exception as e:
			exception = Error( e )
			exception.module = 'Foo'
			exception.cause = ''
			exception.method = ('create_schema( self, function: str, tool: str, description: str, '
			                    'parameters: dict, required: list[ str ] ) -> Dict[ str, str ]')
			Logger( ).write( exception )
			raise exception