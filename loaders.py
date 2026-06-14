'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                loaders.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="loaders.py" company="Terry D. Eppler">

	     loaders.py
	     Copyright ©  2026  Terry Eppler

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
    Provides LangChain document-loader wrappers for local files, web pages, cloud storage,
    repositories, notebooks, structured data, office documents, email, XML, audio
    transcription, and research search services.

    Purpose:
        Centralizes document ingestion behavior for Fonky by validating loader inputs,
        configuring LangChain community loader instances, loading source content into
        LangChain Document objects, and splitting loaded documents into chunks for
        downstream retrieval, embedding, analysis, and tool-calling workflows.
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

import glob
import os
from typing import Any, Dict, List, Optional

from langchain_community.document_loaders import (
	ArxivLoader,
	Docx2txtLoader,
	GithubFileLoader,
	JSONLoader,
	NotebookLoader,
	OpenCityDataLoader,
	OutlookMessageLoader,
	PubMedLoader,
	PyPDFLoader,
	RecursiveUrlLoader,
	S3DirectoryLoader,
	S3FileLoader,
	TextLoader as TextDocLoader,
	UnstructuredEmailLoader,
	UnstructuredExcelLoader,
	UnstructuredHTMLLoader,
	UnstructuredMarkdownLoader,
	UnstructuredPowerPointLoader,
	UnstructuredXMLLoader,
	WebBaseLoader,
	WikipediaLoader,
)
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.onedrive import OneDriveLoader
from langchain_community.document_loaders.parsers import RapidOCRBlobParser
from langchain_community.document_loaders.sharepoint import SharePointLoader
from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from langchain_google_community import (
	GCSDirectoryLoader,
	GCSFileLoader,
	GoogleDriveLoader,
	SpeechToTextLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from lxml import etree

from boogr import Error, Logger

def throw_if( name: str, value: object ) -> None:
	"""Validate required argument values.

	Purpose:
		Validates a named value before a loader or helper uses it. The function rejects missing
		values and blank strings early so caller failures identify the specific argument that needs
		correction.

	Args:
		name (str): Name value used to configure the module.throw_if operation.
		value (object): Value value used to configure the module.throw_if operation.

	Raises:
		ValueError: Raised when a required value is missing, blank, or outside the supported range.
	"""
	if value is None:
		raise ValueError( f'Argument "{name}" cannot be None.' )
	
	if isinstance( value, str ) and not value.strip( ):
		raise ValueError( f'Argument "{name}" cannot be empty.' )

class Loader( ):
	"""Loader document loader wrapper.

	Purpose:
		Provides shared path validation, path expansion, document loading support, and document
		splitting behavior used by concrete LangChain loader wrappers.

	Attributes:
		documents (Optional[List[Document]]): Runtime state retained by the Loader wrapper.
		file_path (Optional[str]): Runtime state retained by the Loader wrapper.
		pattern (Optional[str]): Runtime state retained by the Loader wrapper.
		expanded (Optional[List[str]]): Runtime state retained by the Loader wrapper.
		candidates (Optional[List[str]]): Runtime state retained by the Loader wrapper.
		resolved (Optional[List[str]]): Runtime state retained by the Loader wrapper.
		loader (Optional[BaseLoader]): Runtime state retained by the Loader wrapper.
		splitter (Optional[RecursiveCharacterTextSplitter]): Runtime state retained by the Loader wrapper.
		chunk_size (Optional[int]): Runtime state retained by the Loader wrapper.
		overlap_amount (Optional[int]): Runtime state retained by the Loader wrapper.
	"""
	documents: Optional[ List[ Document ] ]
	file_path: Optional[ str ]
	pattern: Optional[ str ]
	expanded: Optional[ List[ str ] ]
	candidates: Optional[ List[ str ] ]
	resolved: Optional[ List[ str ] ]
	loader: Optional[ BaseLoader ]
	splitter: Optional[ RecursiveCharacterTextSplitter ]
	chunk_size: Optional[ int ]
	overlap_amount: Optional[ int ]
	
	def __init__( self ) -> None:
		"""Initialize the Loader instance.

		Purpose:
			Initializes Loader runtime state used by later loader operations. The constructor assigns
			default attributes and provider settings without loading external content.
		"""
		self.documents = [ ]
		self.candidates = [ ]
		self.resolved = [ ]
		self.expanded = [ ]
		self.file_path = None
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
	
	def verify_exists( self, path: str ) -> str | None:
		"""Validate a local file path.

		Purpose:
			Validates that a supplied local path points to an existing file before a loader attempts
			to read it. The method stores the verified path on the instance and returns the normalized
			path for subsequent loader construction.

		Args:
			path (str): Local file path used by the loader.

		Returns:
			str | None: Validated or generated string value.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
			FileNotFoundError: Raised when a local file path or pattern does not resolve to an existing file.
		"""
		try:
			throw_if( 'path', path )
			self.file_path = path
			if not os.path.isfile( self.file_path ):
				raise FileNotFoundError( f'File not found: {self.file_path}' )
			else:
				self.file_path = path
			return self.file_path
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'Loader'
			exception.method = 'verify_exists( self, path: str ) -> str'
			Logger( ).write( exception )
			raise exception
	
	def resolve_paths( self, pattern: str ) -> List[ str ] | None:
		"""Resolve file paths or glob patterns.

		Purpose:
			Expands a direct file path or glob pattern into concrete existing files. The method
			records candidate and resolved paths so batch-oriented loaders can operate on verified
			filesystem inputs.

		Args:
			pattern (str): Pattern value used to configure the Loader.resolve_paths operation.

		Returns:
			List[str] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
			FileNotFoundError: Raised when a local file path or pattern does not resolve to an existing file.
		"""
		try:
			throw_if( 'pattern', pattern )
			self.candidates.append( pattern )
			for p in self.candidates:
				if os.path.isfile( p ):
					self.resolved.append( p )
				else:
					for m in glob.glob( p ):
						if os.path.isfile( m ):
							self.resolved.append( m )
			
			if not self.resolved:
				raise FileNotFoundError( f'No files matched or existed for input: {pattern}' )
			return sorted( set( self.resolved ) )
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'Loader'
			exception.method = 'resolve_paths( self, pattern: str ) -> List[ str ]'
			Logger( ).write( exception )
			raise exception
	
	def load_documents( self, path: str, encoding: Optional[ str ],
			csv_args: Optional[ Dict[ str, Any ] ],
			source_column: Optional[ str ] ) -> List[ Document ] | None:
		"""Load CSV-style documents.

		Purpose:
			Loads CSV-style source content into LangChain Document objects using the configured path,
			encoding, CSV options, and source-column settings. The method stores the active loader and
			loaded documents for downstream splitting.

		Args:
			path (str): Local file path used by the loader.
			encoding (Optional[str]): Optional file encoding passed to the backing loader.
			csv_args (Optional[Dict[str, Any]]): Csv args value used to configure the Loader.load_documents operation.
			source_column (Optional[str]): Source column value used to configure the Loader.load_documents operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			self.file_path = self.verify_exists( path )
			self.encoding = encoding
			self.csv_args = csv_args
			self.source_column = source_column
			self.loader = BaseLoader( file_path=self.file_path, encoding=self.encoding,
				csv_args=self.csv_args, source_column=self.source_column )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'CSV'
			exception.method = 'load_documents( self, **kwargs )'
			Logger( ).write( exception )
			raise exception
	
	def split_documents( self, docs: List[ Document ], chunk: int = 1000, overlap: int = 200 ) -> \
			List[ Document ] | None:
		"""Split document collections.

		Purpose:
			Splits a supplied list of LangChain Document objects into smaller chunks using
			RecursiveCharacterTextSplitter. The method stores chunking settings before returning
			chunked documents for retrieval, embedding, or analysis workflows.

		Args:
			docs (List[Document]): Docs value used to configure the Loader.split_documents operation.
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'docs', docs )
			self.documents = docs
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
				model_name='gpt-4o', chunk_size=self.chunk_size, overlap=self.overlap_amount )
			return self.splitter.split_documents( documents=self.documents )
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'Loader'
			exception.method = ('split_documents( self, docs: List[ Document ], chunk: int=1000, '
			                    'overlap: int=200 ) -> List[ Document ]')
			Logger( ).write( exception )
			raise exception

class TextLoader( Loader ):
	"""TextLoader document loader wrapper.

	Purpose:
		Loads local plain-text files into LangChain Document objects and prepares those documents
		for chunking workflows.

	Attributes:
		loader (Optional[TextDocLoader]): Runtime state retained by the TextLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the TextLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the TextLoader wrapper.
		encoding (Optional[str]): Runtime state retained by the TextLoader wrapper.
	"""
	loader: Optional[ TextDocLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	encoding: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize the TextLoader instance.

		Purpose:
			Initializes TextLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.encoding = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'encoding',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	def load( self, path: str, encoding: Optional[ str ] = None ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads a local text file into LangChain Document objects. The method validates the path,
			applies the optional encoding, constructs TextDocLoader, stores the loader state, and
			returns loaded text documents.

		Args:
			path (str): Local file path used by the loader.
			encoding (Optional[str]): Optional file encoding passed to the backing loader.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'path', path )
			self.file_path = self.verify_exists( path )
			self.encoding = encoding
			if self.encoding:
				self.loader = TextDocLoader( file_path=self.file_path, encoding=self.encoding )
			else:
				self.loader = TextDocLoader( file_path=self.file_path )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'TextLoader'
			exception.method = 'load( self, path: str, encoding: Optional[ str ]=None ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'TextLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 )-> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class CsvLoader( Loader ):
	"""CsvLoader document loader wrapper.

	Purpose:
		Loads comma-separated or delimiter-separated files into LangChain Document objects with
		configurable encoding, source-column, delimiter, and quote-character behavior.

	Attributes:
		loader (Optional[CSVLoader]): Runtime state retained by the CsvLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the CsvLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the CsvLoader wrapper.
		encoding (Optional[str]): Runtime state retained by the CsvLoader wrapper.
		csv_args (Optional[Dict[str, Any]]): Runtime state retained by the CsvLoader wrapper.
		source_column (Optional[str]): Runtime state retained by the CsvLoader wrapper.
		delimiter (Optional[str]): Runtime state retained by the CsvLoader wrapper.
		quotechar (Optional[str]): Runtime state retained by the CsvLoader wrapper.
	"""
	loader: Optional[ CSVLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	encoding: Optional[ str ]
	csv_args: Optional[ Dict[ str, Any ] ]
	source_column: Optional[ str ]
	delimiter: Optional[ str ]
	quotechar: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize the CsvLoader instance.

		Purpose:
			Initializes CsvLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.loader = None
		self.file_path = None
		self.documents = [ ]
		self.encoding = None
		self.csv_args = None
		self.source_column = None
		self.delimiter = None
		self.quotechar = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader', 'file_path', 'documents', 'encoding',
		         'csv_args', 'source_column', 'delimiter', 'quotechar',
		         'chunk_size', 'overlap_amount', 'load', 'split',
		         'split_documents', ]
	
	def load( self, path: str, encoding: Optional[ str ] = 'utf-8',
			source_column: Optional[ str ] = None, delimiter: str = ',',
			quotechar: str = '"' ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads a CSV file into LangChain Document objects. The method validates the file path,
			builds CSV parsing options from delimiter and quote-character settings, records optional
			source-column metadata, and returns the parsed rows as documents.

		Args:
			path (str): Local file path used by the loader.
			encoding (Optional[str]): Optional file encoding passed to the backing loader.
			source_column (Optional[str]): Source column value used to configure the CsvLoader.load operation.
			delimiter (str): Delimiter value used to configure the CsvLoader.load operation.
			quotechar (str): Quotechar value used to configure the CsvLoader.load operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'path', path )
			self.file_path = self.verify_exists( path )
			self.encoding = encoding
			self.source_column = source_column
			self.delimiter = delimiter
			self.quotechar = quotechar
			self.csv_args = {
					'delimiter': self.delimiter,
					'quotechar': self.quotechar,
			}
			self.loader = CSVLoader(
				file_path=self.file_path,
				source_column=self.source_column,
				csv_args=self.csv_args,
				encoding=self.encoding
			)
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'Foo'
			exception.cause = 'CsvLoader'
			exception.method = (
					'load( self, path: str, encoding: Optional[ str ]="utf-8", '
					'source_column: Optional[ str ]=None, delimiter: str=",", '
					'quotechar: str=\'"\' ) -> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents,
				chunk=self.chunk_size, overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'Foo'
			exception.cause = 'CsvLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) '
					'-> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception

class WebLoader( Loader ):
	"""WebLoader document loader wrapper.

	Purpose:
		Loads documents from one or more web pages, with optional recursive URL traversal and
		same-domain filtering for bounded web ingestion workflows.

	Attributes:
		loader (Optional[RecursiveUrlLoader | WebBaseLoader]): Runtime state retained by the WebLoader wrapper.
		url (Optional[str]): Runtime state retained by the WebLoader wrapper.
		web_paths (Optional[str | List[str]]): Runtime state retained by the WebLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the WebLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the WebLoader wrapper.
		max_depth (Optional[int]): Runtime state retained by the WebLoader wrapper.
		tiemout (Optional[int]): Runtime state retained by the WebLoader wrapper.
		ignore (Optional[bool]): Runtime state retained by the WebLoader wrapper.
		with_progress (Optional[bool]): Runtime state retained by the WebLoader wrapper.
		recursive (Optional[bool]): Runtime state retained by the WebLoader wrapper.
		prevent_outside (Optional[bool]): Runtime state retained by the WebLoader wrapper.
	"""
	loader: Optional[ RecursiveUrlLoader | WebBaseLoader ]
	url: Optional[ str ]
	web_paths: Optional[ str | List[ str ] ]
	documents: Optional[ List[ Document ] ]
	file_path: Optional[ str ]
	max_depth: Optional[ int ]
	tiemout: Optional[ int ]
	ignore: Optional[ bool ]
	with_progress: Optional[ bool ]
	recursive: Optional[ bool ]
	prevent_outside: Optional[ bool ]
	
	def __init__( self, recursive: bool = False, max_depth: int = 2,
			prevent_outside: bool = True, timeout: int = 10,
			ignore: bool = True, progress: bool = True ) -> None:
		"""Initialize the WebLoader instance.

		Purpose:
			Initializes WebLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.

		Args:
			recursive (bool): Whether the loader should traverse nested provider or URL resources.
			max_depth (int): Max depth value used to configure the WebLoader.__init__ operation.
			prevent_outside (bool): Prevent outside value used to configure the WebLoader.__init__ operation.
			timeout (int): Timeout value used to configure the WebLoader.__init__ operation.
			ignore (bool): Ignore value used to configure the WebLoader.__init__ operation.
			progress (bool): Progress value used to configure the WebLoader.__init__ operation.
		"""
		super( ).__init__( )
		self.max_depth = max_depth
		self.tiemout = timeout
		self.url = None
		self.documents = None
		self.file_path = None
		self.web_paths = None
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.ignore = ignore
		self.with_progress = progress
		self.recursive = recursive
		self.prevent_outside = prevent_outside
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'max_depth',
		         'timeout',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'load_pages',
		         'load_recursive',
		         'split',
		         'urls',
		         'recursive',
		         'prevent_outside', ]
	
	def _same_domain_only( self, docs: List[ Document ], source_url: str ) -> List[
		                                                                          Document ] | None:
		"""Filter documents to the source domain.

		Purpose:
			Filters recursively loaded web documents so only pages from the original URL domain
			remain. The method inspects document metadata for source URLs and returns the subset that
			matches the seed domain.

		Args:
			docs (List[Document]): Docs value used to configure the WebLoader._same_domain_only operation.
			source_url (str): Source url value used to configure the WebLoader._same_domain_only operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'docs', docs )
			throw_if( 'source_url', source_url )
			
			from urllib.parse import urlparse
			
			_origin = urlparse( source_url ).netloc.lower( )
			_results = [ ]
			
			for d in docs:
				if not hasattr( d, 'metadata' ) or not isinstance( d.metadata, dict ):
					continue
				
				_source = d.metadata.get( 'source' ) or d.metadata.get( 'url' )
				if not isinstance( _source, str ) or not _source.strip( ):
					continue
				
				_netloc = urlparse( _source ).netloc.lower( )
				if _netloc == _origin:
					_results.append( d )
			
			return _results
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WebLoader'
			exception.method = ('_same_domain_only( self, docs: List[ Document ], '
			                    'source_url: str ) -> List[ Document ]')
			Logger( ).write( exception )
			raise exception
	
	def load( self, urls: str | List[ str ] ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads web content from one or more URLs. The method chooses between recursive crawling and
			static page loading based on instance configuration, stores request state, and returns the
			loaded web documents.

		Args:
			urls (str | List[str]): URL string or URL list used as web-loader input.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
			ValueError: Raised when a required value is missing, blank, or outside the supported range.
		"""
		try:
			throw_if( 'urls', urls )
			
			if self.recursive:
				if isinstance( urls, list ):
					if not urls:
						raise ValueError( 'No URLs were provided!' )
					self.url = urls[ 0 ]
				else:
					self.url = urls
				
				self.documents = self.load_recursive(
					url=self.url,
					depth=self.max_depth,
					max_time=self.tiemout,
					ignore=self.ignore
				)
				return self.documents
			else:
				if isinstance( urls, str ):
					self.web_paths = [ urls ]
				else:
					self.web_paths = urls
				
				self.documents = self.load_pages(
					urls=self.web_paths,
					depth=self.max_depth,
					timeout=self.tiemout,
					ignore=self.ignore,
					progress=self.with_progress
				)
				return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WebLoader'
			exception.method = 'load( self, urls: str | List[ str ] ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def load_recursive( self, url: str, depth: int = 2, max_time: int = 10,
			ignore: bool = True ) -> List[ Document ] | None:
		"""Load web documents recursively.

		Purpose:
			Recursively loads documents from a seed URL using RecursiveUrlLoader. The method records
			crawl settings, loads reachable content to the configured depth, and optionally filters
			results to the original domain.

		Args:
			url (str): URL used by the web or repository loader.
			depth (int): Depth value used to configure the WebLoader.load_recursive operation.
			max_time (int): Max time value used to configure the WebLoader.load_recursive operation.
			ignore (bool): Ignore value used to configure the WebLoader.load_recursive operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'url', url )
			self.url = url
			self.max_depth = depth
			self.tiemout = max_time
			self.ignore = ignore
			self.loader = RecursiveUrlLoader(
				self.url,
				max_depth=self.max_depth,
				timeout=self.tiemout,
				continue_on_failure=self.ignore
			)
			self.documents = self.loader.load( )
			
			if self.prevent_outside:
				self.documents = self._same_domain_only(
					docs=self.documents,
					source_url=self.url
				)
			
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WebLoader'
			exception.method = ('load_recursive( self, url: str, depth: int=2, '
			                    'max_time: int=10, ignore: bool=True ) -> List[ Document ]')
			Logger( ).write( exception )
			raise exception
	
	def load_pages( self, urls: List[ str ], depth: int = 2, timeout: int = 10,
			ignore: bool = True, progress: bool = True ) -> List[ Document ] | None:
		"""Load static web pages.

		Purpose:
			Loads one or more static web pages through WebBaseLoader. The method records the URL list
			and request settings before returning the loaded page documents.

		Args:
			urls (List[str]): URL string or URL list used as web-loader input.
			depth (int): Depth value used to configure the WebLoader.load_pages operation.
			timeout (int): Timeout value used to configure the WebLoader.load_pages operation.
			ignore (bool): Ignore value used to configure the WebLoader.load_pages operation.
			progress (bool): Progress value used to configure the WebLoader.load_pages operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'urls', urls )
			self.web_paths = urls
			self.max_depth = depth
			self.tiemout = timeout
			self.ignore = ignore
			self.with_progress = progress
			self.loader = WebBaseLoader(
				web_paths=self.web_paths,
				show_progress=self.with_progress,
				continue_on_failure=self.ignore
			)
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WebLoader'
			exception.method = ('load_pages( self, urls: List[ str ], depth: int=2, '
			                    'timeout: int=10, ignore: bool=True, '
			                    'progress: bool=True ) -> List[ Document ]')
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
			ValueError: Raised when a required value is missing, blank, or outside the supported range.
		"""
		try:
			if self.documents is None:
				raise ValueError( 'No documents loaded!' )
			
			self.chunk_size = chunk
			self.overlap_amount = overlap
			_documents = self.split_documents(
				docs=self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
			return _documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WebLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class PdfReader( Loader ):
	"""PdfReader document loader wrapper.

	Purpose:
		Loads PDF files with PyPDFLoader and provides a base PDF reading path for simpler page or
		single-document extraction workflows.

	Attributes:
		loader (Optional[PyPDFLoader]): Runtime state retained by the PdfReader wrapper.
		file_path (Optional[str]): Runtime state retained by the PdfReader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the PdfReader wrapper.
		mode (Optional[str]): Runtime state retained by the PdfReader wrapper.
	"""
	loader: Optional[ PyPDFLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	mode: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize the PdfReader instance.

		Purpose:
			Initializes PdfReader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.mode = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'mode',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	def load( self, path: str, mode: str = 'single' ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads a PDF file through PyPDFLoader using the requested mode. The method validates the
			file path, stores the extraction mode, constructs the loader, and returns PDF page or
			single-document output.

		Args:
			path (str): Local file path used by the loader.
			mode (str): Loader mode or dispatch mode used by the operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'path', path )
			self.file_path = self.verify_exists( path )
			self.mode = mode
			self.loader = PyPDFLoader( file_path=self.file_path, mode=self.mode )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'PdfLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents(
				self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'Foo'
			exception.cause = 'PdfReader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) '
					'-> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception

class PdfLoader( PdfReader ):
	"""PdfLoader document loader wrapper.

	Purpose:
		Extends PDF loading with extraction-mode, image-inclusion, image-format, and chunk-size
		settings for richer PDF ingestion workflows.

	Attributes:
		loader (Optional[PyPDFLoader]): Runtime state retained by the PdfLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the PdfLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the PdfLoader wrapper.
		mode (Optional[str]): Runtime state retained by the PdfLoader wrapper.
		extraction (Optional[str]): Runtime state retained by the PdfLoader wrapper.
		include_images (Optional[bool]): Runtime state retained by the PdfLoader wrapper.
		image_format (Optional[str]): Runtime state retained by the PdfLoader wrapper.
		custom_delimiter (Optional[str]): Runtime state retained by the PdfLoader wrapper.
		image_parser (Optional[RapidOCRBlobParser]): Runtime state retained by the PdfLoader wrapper.
	"""
	loader: Optional[ PyPDFLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	mode: Optional[ str ]
	extraction: Optional[ str ]
	include_images: Optional[ bool ]
	image_format: Optional[ str ]
	custom_delimiter: Optional[ str ]
	image_parser: Optional[ RapidOCRBlobParser ]
	
	def __init__( self, size: int = 1000, overlap: int = 150,
			has_tables: bool = True, include: bool = True ) -> None:
		"""Initialize the PdfLoader instance.

		Purpose:
			Initializes PdfLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.

		Args:
			size (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.
			has_tables (bool): Has tables value used to configure the PdfLoader.__init__ operation.
			include (bool): Include value used to configure the PdfLoader.__init__ operation.
		"""
		super( ).__init__( )
		self.enable_tables = has_tables
		self.include_images = include
		self.file_path = None
		self.documents = [ ]
		self.pattern = None
		self.chunk_size = size
		self.overlap_amount = overlap
		self.loader = None
		self.mode = None
		self.image_format = None
		self.custom_delimiter = None
	
	@property
	def mode_options( self ) -> List[ str ]:
		"""Return loading mode options.

		Purpose:
			Returns the supported loading mode names exposed by the wrapper. These values can be used
			by UIs, examples, and validation logic to keep selectable options aligned with the active
			loader.

		Returns:
			List[str]: Loaded or split LangChain Document objects.
		"""
		return [ 'page', 'single' ]
	
	@property
	def extraction_options( self ) -> List[ str ]:
		"""Return PDF extraction options.

		Purpose:
			Returns the supported PDF extraction mode names. The values identify how PyPDFLoader
			should parse text from the source PDF.

		Returns:
			List[str]: Loaded or split LangChain Document objects.
		"""
		return [ 'plain', 'layout' ]
	
	@property
	def image_options( self ) -> List[ str ]:
		"""Return PDF image output options.

		Purpose:
			Returns the supported image-output formats used when PDF image extraction is enabled. The
			values control how extracted image references are embedded in document content.

		Returns:
			List[str]: Loaded or split LangChain Document objects.
		"""
		return [ 'html-img', 'markdown-img', 'text-img' ]
	
	def load( self, path: str, mode: str = 'single', extract: str = 'plain',
			include: bool = False, format: str = 'markdown-img' ) -> List[ Document ]:
		"""Load source content.

		Purpose:
			Loads a PDF file with configurable text extraction and optional image extraction. The
			method validates the path, configures PyPDFLoader options, falls back to text-only loading
			when image parsing fails, and returns loaded PDF documents.

		Args:
			path (str): Local file path used by the loader.
			mode (str): Loader mode or dispatch mode used by the operation.
			extract (str): Extract value used to configure the PdfLoader.load operation.
			include (bool): Include value used to configure the PdfLoader.load operation.
			format (str): Format value used to configure the PdfLoader.load operation.

		Returns:
			List[Document]: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'path', path )
			self.file_path = self.verify_exists( path )
			self.mode = mode
			self.extraction = extract
			self.include_images = include
			self.image_format = format
			
			if self.include_images:
				try:
					self.image_parser = RapidOCRBlobParser( )
					self.loader = PyPDFLoader(
						file_path=self.file_path,
						mode=self.mode,
						extraction_mode=self.extraction,
						extract_images=self.include_images,
						images_inner_format=self.image_format,
						images_parser=self.image_parser )
					self.documents = self.loader.load( )
					return self.documents
				except Exception:
					self.loader = PyPDFLoader(
						file_path=self.file_path,
						mode=self.mode,
						extraction_mode=self.extraction )
					self.documents = self.loader.load( )
					return self.documents
			else:
				self.loader = PyPDFLoader(
					file_path=self.file_path,
					mode=self.mode,
					extraction_mode=self.extraction )
				self.documents = self.loader.load( )
				return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'PdfLoader'
			exception.method = 'load( self, path: str, mode: str=single, extract: str=plain ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class ExcelLoader( Loader ):
	"""ExcelLoader document loader wrapper.

	Purpose:
		Loads Excel workbooks through the unstructured Excel loader and exposes the loaded workbook
		content as LangChain Document objects.

	Attributes:
		loader (Optional[UnstructuredExcelLoader]): Runtime state retained by the ExcelLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the ExcelLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the ExcelLoader wrapper.
		mode (Optional[str]): Runtime state retained by the ExcelLoader wrapper.
		has_headers (Optional[bool]): Runtime state retained by the ExcelLoader wrapper.
	"""
	loader: Optional[ UnstructuredExcelLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	mode: Optional[ str ]
	has_headers: Optional[ bool ]
	
	def __init__( self ) -> None:
		"""Initialize the ExcelLoader instance.

		Purpose:
			Initializes ExcelLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.mode = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	@property
	def mode_options( self ) -> List[ str ]:
		"""Return loading mode options.

		Purpose:
			Returns the supported loading mode names exposed by the wrapper. These values can be used
			by UIs, examples, and validation logic to keep selectable options aligned with the active
			loader.

		Returns:
			List[str]: Loaded or split LangChain Document objects.
		"""
		return [ 'single', 'page' ]
	
	def load( self, path: str, mode: str = 'elements', has_headers: bool = True ) -> List[
		                                                                                 Document ] | None:
		"""Load source content.

		Purpose:
			Loads an Excel workbook into LangChain Document objects. The method validates the path,
			stores workbook parsing settings, constructs UnstructuredExcelLoader, and returns
			extracted workbook content.

		Args:
			path (str): Local file path used by the loader.
			mode (str): Loader mode or dispatch mode used by the operation.
			has_headers (bool): Has headers value used to configure the ExcelLoader.load operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'path', path )
			self.mode = mode
			self.has_headers = has_headers
			self.file_path = self.verify_exists( path )
			self.loader = UnstructuredExcelLoader( file_path=self.file_path, mode=self.mode )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'ExcelLoader'
			exception.method = 'load( self, **kwargs ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
			ValueError: Raised when a required value is missing, blank, or outside the supported range.
		"""
		try:
			if self.documents is None:
				raise ValueError( 'No documents loaded!' )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=overlap )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'ExcelLoader'
			exception.method = 'split( self,  **kwargs  ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class WordLoader( Loader ):
	"""WordLoader document loader wrapper.

	Purpose:
		Loads Microsoft Word documents through Docx2txtLoader and returns the extracted document
		text as LangChain Document objects.

	Attributes:
		loader (Optional[Docx2txtLoader]): Runtime state retained by the WordLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the WordLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the WordLoader wrapper.
	"""
	loader: Optional[ Docx2txtLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	
	def __init__( self ) -> None:
		"""Initialize the WordLoader instance.

		Purpose:
			Initializes WordLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.documents = None
		self.file_path = None
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	def load( self, path: str ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads a Word document into LangChain Document objects. The method validates the local
			path, constructs Docx2txtLoader, and returns extracted document text.

		Args:
			path (str): Local file path used by the loader.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'path', path )
			self.file_path = self.verify_exists( path )
			self.loader = Docx2txtLoader( self.file_path )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WordLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
			ValueError: Raised when a required value is missing, blank, or outside the supported range.
		"""
		try:
			if self.documents is None:
				raise ValueError( 'No documents loaded!' )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			_splits = self.split_documents( docs=self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return _splits
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WordLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class MarkdownLoader( Loader ):
	"""MarkdownLoader document loader wrapper.

	Purpose:
		Loads local Markdown files with the unstructured Markdown loader and returns parsed content
		as LangChain Document objects.

	Attributes:
		loader (Optional[UnstructuredMarkdownLoader]): Runtime state retained by the MarkdownLoader wrapper.
		file_path (str | None): Runtime state retained by the MarkdownLoader wrapper.
		documents (List[Document] | None): Runtime state retained by the MarkdownLoader wrapper.
	"""
	loader: Optional[ UnstructuredMarkdownLoader ]
	file_path: str | None
	documents: List[ Document ] | None
	
	def __init__( self ) -> None:
		"""Initialize the MarkdownLoader instance.

		Purpose:
			Initializes MarkdownLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	def load( self, path: str ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads a Markdown file into LangChain Document objects. The method validates the path,
			constructs UnstructuredMarkdownLoader, and returns parsed Markdown content.

		Args:
			path (str): Local file path used by the loader.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'path', path )
			self.file_path = self.verify_exists( path )
			self.loader = UnstructuredMarkdownLoader( file_path=self.file_path )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'MarkdownLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ] '
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			_documents = self.split_documents( docs=self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return _documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'MarkdownLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class HtmlLoader( Loader ):
	"""HtmlLoader document loader wrapper.

	Purpose:
		Loads local HTML files with the unstructured HTML loader and returns parsed page content as
		LangChain Document objects.

	Attributes:
		loader (Optional[UnstructuredHTMLLoader]): Runtime state retained by the HtmlLoader wrapper.
		file_path (str | None): Runtime state retained by the HtmlLoader wrapper.
		documents (List[Document] | None): Runtime state retained by the HtmlLoader wrapper.
	"""
	loader: Optional[ UnstructuredHTMLLoader ]
	file_path: str | None
	documents: List[ Document ] | None
	
	def __init__( self ) -> None:
		"""Initialize the HtmlLoader instance.

		Purpose:
			Initializes HtmlLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	def load( self, path: str ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads a local HTML file into LangChain Document objects. The method validates the path,
			constructs UnstructuredHTMLLoader, and returns extracted HTML content.

		Args:
			path (str): Local file path used by the loader.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'path', path )
			self.file_path = self.verify_exists( path )
			self.loader = UnstructuredHTMLLoader( file_path=self.file_path )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'HTML'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
			ValueError: Raised when a required value is missing, blank, or outside the supported range.
		"""
		try:
			if self.documents is None:
				raise ValueError( 'No documents loaded!' )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'HtmlLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class ArXivLoader( Loader ):
	"""ArXivLoader document loader wrapper.

	Purpose:
		Queries ArXiv through the LangChain ArxivLoader and returns scholarly search results as
		LangChain Document objects.

	Attributes:
		loader (Optional[ArxivLoader]): Runtime state retained by the ArXivLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the ArXivLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the ArXivLoader wrapper.
		max_documents (Optional[int]): Runtime state retained by the ArXivLoader wrapper.
		max_characters (Optional[int]): Runtime state retained by the ArXivLoader wrapper.
		include_metadata (Optional[bool]): Runtime state retained by the ArXivLoader wrapper.
		query (Optional[str]): Runtime state retained by the ArXivLoader wrapper.
	"""
	loader: Optional[ ArxivLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	max_documents: Optional[ int ]
	max_characters: Optional[ int ]
	include_metadata: Optional[ bool ]
	query: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize the ArXivLoader instance.

		Purpose:
			Initializes ArXivLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.query = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.max_documents = 2
		self.max_characters = 1000
		self.include_metadata = False
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'max_documents',
		         'max_characters',
		         'include_metadata',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	def load( self, question: str ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Runs an ArXiv query and loads matching scholarly records as LangChain Document objects.
			The method stores the query, configures the ArxivLoader character limit, and returns the
			retrieved documents.

		Args:
			question (str): Search query or prompt submitted to the backing loader.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'question', question )
			self.query = question
			self.loader = ArxivLoader( query=self.query,
				doc_content_chars_max=self.max_characters )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'ArxivLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'ArxivLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class WikiLoader( Loader ):
	"""WikiLoader document loader wrapper.

	Purpose:
		Queries Wikipedia through the LangChain WikipediaLoader and returns encyclopedia search
		results as LangChain Document objects.

	Attributes:
		loader (Optional[WikipediaLoader]): Runtime state retained by the WikiLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the WikiLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the WikiLoader wrapper.
		query (Optional[str]): Runtime state retained by the WikiLoader wrapper.
		max_documents (Optional[int]): Runtime state retained by the WikiLoader wrapper.
		max_characters (Optional[int]): Runtime state retained by the WikiLoader wrapper.
		include_all (Optional[bool]): Runtime state retained by the WikiLoader wrapper.
		query (Optional[str]): Runtime state retained by the WikiLoader wrapper.
	"""
	loader: Optional[ WikipediaLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	query: Optional[ str ]
	max_documents: Optional[ int ]
	max_characters: Optional[ int ]
	include_all: Optional[ bool ]
	query: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize the WikiLoader instance.

		Purpose:
			Initializes WikiLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.query = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.max_documents = 25
		self.max_characters = 4000
		self.include_all
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'max_documents',
		         'max_characters',
		         'include_all',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	def load( self, question: str ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Runs a Wikipedia query and loads matching encyclopedia records as LangChain Document
			objects. The method stores the query and retrieval limits before returning the retrieved
			documents.

		Args:
			question (str): Search query or prompt submitted to the backing loader.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'question', question )
			self.query = question
			self.loader = WikipediaLoader( query=self.query, max_documents=self.max_documents,
				load_all_available_meta=self.include_all,
				doc_content_chars_max=self.max_characters )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WikiLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WikiLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class GoogleDriveLoader( Loader ):
	"""GoogleDriveLoader document loader wrapper.

	Purpose:
		Loads files or folders from Google Drive through the Google Drive loader and returns
		accessible Drive content as LangChain Document objects.

	Attributes:
		loader (Optional[GoogleDriveLoader]): Runtime state retained by the GoogleDriveLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the GoogleDriveLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the GoogleDriveLoader wrapper.
		query (Optional[str]): Runtime state retained by the GoogleDriveLoader wrapper.
		file_id (Optional[str]): Runtime state retained by the GoogleDriveLoader wrapper.
		folder_id (Optional[str]): Runtime state retained by the GoogleDriveLoader wrapper.
		query (Optional[str]): Runtime state retained by the GoogleDriveLoader wrapper.
		is_recursive (Optional[bool]): Runtime state retained by the GoogleDriveLoader wrapper.
	"""
	loader: Optional[ GoogleDriveLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	query: Optional[ str ]
	file_id: Optional[ str ]
	folder_id: Optional[ str ]
	query: Optional[ str ]
	is_recursive: Optional[ bool ]
	
	def __init__( self ) -> None:
		"""Initialize the GoogleDriveLoader instance.

		Purpose:
			Initializes GoogleDriveLoader runtime state used by later loader operations. The
			constructor assigns default attributes and provider settings without loading external
			content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.query = None
		self.file_id = None
		self.folder_id = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.is_recursive = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'query',
		         'folder_id',
		         'file_id',
		         'is_recursive',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'load_folder',
		         'split', ]
	
	@property
	def file_options( self ) -> List[ str ]:
		"""Return Google Drive file options.

		Purpose:
			Returns the supported Google Drive file target names exposed by the wrapper. These values
			describe the Drive-backed file categories expected by the loader workflow.

		Returns:
			List[str]: Loaded or split LangChain Document objects.
		"""
		return [ 'document',
		         'sheet',
		         'pdf' ]
	
	def load_file( self, file_id: str, recursive: bool = False ) -> List[ Document ] | None:
		"""Load a provider file.

		Purpose:
			Loads a single provider-backed file into LangChain Document objects. The method stores the
			selected file identifier and recursion flag before constructing the backing loader.

		Args:
			file_id (str): Provider file identifier used to load a single file.
			recursive (bool): Whether the loader should traverse nested provider or URL resources.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'file_id', file_id )
			throw_if( 'recursive', recursive )
			self.file_id = file_id
			self.is_recursive = recursive
			self.loader = GoogleDriveLoader( file_ids=[ self.file_id ],
				recursive=self.is_recursive )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'Fonky'
			exception.cause = 'GoogleDriveLoader'
			exception.method = 'load_File( self, file_id: str ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def load_folder( self, folder_id: str, recursive: bool = False ) -> List[ Document ] | None:
		"""Load provider folder content.

		Purpose:
			Loads documents from a provider folder or document-library folder. The method records the
			folder identifiers, constructs the backing loader, and returns the loaded documents.

		Args:
			folder_id (str): Provider folder identifier used to load folder contents.
			recursive (bool): Whether the loader should traverse nested provider or URL resources.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'folder_id', folder_id )
			self.folder_id = folder_id
			self.is_recursive = recursive
			self.loader = GoogleDriveLoader( folder_id=self.folder_id, recursive=self.is_recursive )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'Fonky'
			exception.cause = 'GoogleDriveLoader'
			exception.method = 'load_folder( self, path: str ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'Fonky'
			exception.cause = 'GoogleDriveLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class OutlookLoader( Loader ):
	"""OutlookLoader document loader wrapper.

	Purpose:
		Loads Outlook message files and returns their email content as LangChain Document objects.

	Attributes:
		loader (Optional[OutlookMessageLoader]): Runtime state retained by the OutlookLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the OutlookLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the OutlookLoader wrapper.
		query (Optional[str]): Runtime state retained by the OutlookLoader wrapper.
		max_documents (Optional[int]): Runtime state retained by the OutlookLoader wrapper.
		max_characters (Optional[int]): Runtime state retained by the OutlookLoader wrapper.
		query (Optional[str]): Runtime state retained by the OutlookLoader wrapper.
	"""
	loader: Optional[ OutlookMessageLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	query: Optional[ str ]
	max_documents: Optional[ int ]
	max_characters: Optional[ int ]
	query: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize the OutlookLoader instance.

		Purpose:
			Initializes OutlookLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.query = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.max_documents = 2
		self.max_characters = 1000
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'max_charactes',
		         'max_documents',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	def load( self, path: str ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads an Outlook message file into LangChain Document objects. The method validates the
			local message path, constructs OutlookMessageLoader, and returns extracted email content.

		Args:
			path (str): Local file path used by the loader.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'path', path )
			self.file_path = self.verify_exists( path )
			self.loader = OutlookMessageLoader( file_path=self.file_path )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'OutlookLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'OutlookLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class SpfxLoader( Loader ):
	"""SpfxLoader document loader wrapper.

	Purpose:
		Loads SharePoint document-library content through the SharePoint loader, including
		full-library and folder-scoped retrieval paths.

	Attributes:
		loader (Optional[SharePointLoader]): Runtime state retained by the SpfxLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the SpfxLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the SpfxLoader wrapper.
		library_id (Optional[str]): Runtime state retained by the SpfxLoader wrapper.
		subsite_id (Optional[str]): Runtime state retained by the SpfxLoader wrapper.
		folder_id (Optional[str]): Runtime state retained by the SpfxLoader wrapper.
		object_ids (Optional[List[str]]): Runtime state retained by the SpfxLoader wrapper.
		query (Optional[str]): Runtime state retained by the SpfxLoader wrapper.
		with_token (Optional[bool]): Runtime state retained by the SpfxLoader wrapper.
		is_recursive (Optional[bool]): Runtime state retained by the SpfxLoader wrapper.
	"""
	loader: Optional[ SharePointLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	library_id: Optional[ str ]
	subsite_id: Optional[ str ]
	folder_id: Optional[ str ]
	object_ids: Optional[ List[ str ] ]
	query: Optional[ str ]
	with_token: Optional[ bool ]
	is_recursive: Optional[ bool ]
	
	def __init__( self ) -> None:
		"""Initialize the SpfxLoader instance.

		Purpose:
			Initializes SpfxLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.folder_id = None
		self.library_id = None
		self.subsite_id = None
		self.object_ids = [ ]
		self.with_token = None
		self.is_recursive = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'folder_id',
		         'library_id',
		         'subsite_id',
		         'object_id',
		         'with_token',
		         'is_recursive',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	def load( self, library_id: str ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads SharePoint document-library content into LangChain Document objects. The method
			records library or folder identifiers, configures SharePointLoader, and returns retrieved
			documents.

		Args:
			library_id (str): SharePoint document-library identifier.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'library_id', library_id )
			self.library_id = library_id
			self.is_recursive = True
			self.with_token = True
			self.loader = SharePointLoader( document_library_id=self.library_id,
				recursive=self.is_recursive, auth_with_token=self.with_token )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'SpfxLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def load_folder( self, library_id: str, folder_id: str ) -> List[ Document ] | None:
		"""Load provider folder content.

		Purpose:
			Loads documents from a provider folder or document-library folder. The method records the
			folder identifiers, constructs the backing loader, and returns the loaded documents.

		Args:
			library_id (str): SharePoint document-library identifier.
			folder_id (str): Provider folder identifier used to load folder contents.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'library_id', library_id )
			throw_if( 'folder_id', folder_id )
			self.library_id = library_id
			self.folder_id = folder_id
			self.loader = SharePointLoader( document_library_id=self.library_id,
				folder_id=self.folder_id )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'SpfxLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'SpfxLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class PowerPointLoader( Loader ):
	"""PowerPointLoader document loader wrapper.

	Purpose:
		Loads PowerPoint presentation files through the unstructured PowerPoint loader and returns
		slide content as LangChain Document objects.

	Attributes:
		loader (Optional[UnstructuredPowerPointLoader]): Runtime state retained by the PowerPointLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the PowerPointLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the PowerPointLoader wrapper.
		mode (Optional[str]): Runtime state retained by the PowerPointLoader wrapper.
		query (Optional[str]): Runtime state retained by the PowerPointLoader wrapper.
	"""
	loader: Optional[ UnstructuredPowerPointLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	mode: Optional[ str ]
	query: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize the PowerPointLoader instance.

		Purpose:
			Initializes PowerPointLoader runtime state used by later loader operations. The
			constructor assigns default attributes and provider settings without loading external
			content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.query = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.mode = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'query',
		         'mode',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	def load( self, path: str, mode: str = 'single' ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads a PowerPoint file into LangChain Document objects. The method validates the path,
			sets the extraction mode, constructs UnstructuredPowerPointLoader, and returns slide
			content.

		Args:
			path (str): Local file path used by the loader.
			mode (str): Loader mode or dispatch mode used by the operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'path', path )
			self.file_path = self.verify_exists( path )
			self.mode = mode
			self.loader = UnstructuredPowerPointLoader( file_path=self.file_path, mode=self.mode )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'PowerPointLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def load_multiple( self, path: str ) -> List[ Document ] | None:
		"""Load multiple presentation elements.

		Purpose:
			Loads PowerPoint content using the loader mode intended for multiple-document or
			multi-element extraction. The method validates the file path and stores the loaded
			presentation documents.

		Args:
			path (str): Local file path used by the loader.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'path', path )
			self.file_path = self.verify_exists( path )
			self.mode = 'multiple'
			self.loader = UnstructuredPowerPointLoader( file_path=self.file_path, mode=self.mode )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'PowerPointLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'PowerPointLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class OneDriveDocLoader( Loader ):
	"""OneDriveDocLoader document loader wrapper.

	Purpose:
		Loads OneDrive document content by drive, folder path, or object identifiers through the
		OneDrive loader.

	Attributes:
		loader (Optional[OneDriveLoader]): Runtime state retained by the OneDriveDocLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the OneDriveDocLoader wrapper.
		drive_id (Optional[str]): Runtime state retained by the OneDriveDocLoader wrapper.
		folder_path (Optional[str]): Runtime state retained by the OneDriveDocLoader wrapper.
		object_ids (Optional[List[str]]): Runtime state retained by the OneDriveDocLoader wrapper.
		auth_with_token (Optional[bool]): Runtime state retained by the OneDriveDocLoader wrapper.
	"""
	loader: Optional[ OneDriveLoader ]
	documents: Optional[ List[ Document ] ]
	drive_id: Optional[ str ]
	folder_path: Optional[ str ]
	object_ids: Optional[ List[ str ] ]
	auth_with_token: Optional[ bool ]
	
	def __init__( self ) -> None:
		"""Initialize the OneDriveDocLoader instance.

		Purpose:
			Initializes OneDriveDocLoader runtime state used by later loader operations. The
			constructor assigns default attributes and provider settings without loading external
			content.
		"""
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.drive_id = None
		self.folder_path = None
		self.object_ids = None
		self.auth_with_token = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [
				'loader',
				'documents',
				'drive_id',
				'folder_path',
				'object_ids',
				'auth_with_token',
				'chunk_size',
				'overlap_amount',
				'load',
				'split',
				'split_documents',
		]
	
	def load( self, drive_id: str, folder_path: Optional[ str ] = None,
			object_ids: Optional[ List[ str ] ] = None,
			auth_with_token: bool = True ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads OneDrive documents by drive identifier, folder path, or object identifiers. The
			method builds loader keyword arguments from optional inputs, constructs OneDriveLoader,
			and returns loaded documents.

		Args:
			drive_id (str): OneDrive drive identifier.
			folder_path (Optional[str]): Folder path value used to configure the OneDriveDocLoader.load operation.
			object_ids (Optional[List[str]]): Object ids value used to configure the OneDriveDocLoader.load operation.
			auth_with_token (bool): Auth with token value used to configure the OneDriveDocLoader.load operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'drive_id', drive_id )
			
			self.drive_id = drive_id
			self.folder_path = folder_path
			self.object_ids = object_ids
			self.auth_with_token = auth_with_token
			
			kwargs: Dict[ str, Any ] = {
					'drive_id': self.drive_id,
					'auth_with_token': self.auth_with_token,
			}
			
			if self.folder_path:
				kwargs[ 'folder_path' ] = self.folder_path
			
			if self.object_ids:
				kwargs[ 'object_ids' ] = self.object_ids
			
			self.loader = OneDriveLoader( **kwargs )
			self.documents = self.loader.load( )
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'OneDriveDocLoader'
			exception.method = (
					'load( self, drive_id: str, folder_path: Optional[ str ]=None, '
					'object_ids: Optional[ List[ str ] ]=None, auth_with_token: bool=True ) '
					'-> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'OneDriveDocLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception

class EmailLoader( Loader ):
	"""EmailLoader document loader wrapper.

	Purpose:
		Loads email files through the unstructured email loader, including optional attachment
		processing.

	Attributes:
		loader (Optional[UnstructuredEmailLoader]): Runtime state retained by the EmailLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the EmailLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the EmailLoader wrapper.
		has_attachments (Optional[bool]): Runtime state retained by the EmailLoader wrapper.
		mode (Optional[str]): Runtime state retained by the EmailLoader wrapper.
	"""
	loader: Optional[ UnstructuredEmailLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	has_attachments: Optional[ bool ]
	mode: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize the EmailLoader instance.

		Purpose:
			Initializes EmailLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.mode = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'has_attachments',
		         'mode',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	def load( self, path: str, mode: str = 'single', attachments: bool = True ) -> List[
		                                                                               Document ] | None:
		"""Load source content.

		Purpose:
			Loads an email file into LangChain Document objects. The method validates the path,
			configures email mode and attachment handling, constructs UnstructuredEmailLoader, and
			returns parsed email content.

		Args:
			path (str): Local file path used by the loader.
			mode (str): Loader mode or dispatch mode used by the operation.
			attachments (bool): Attachments value used to configure the EmailLoader.load operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'path', path )
			self.file_path = self.verify_exists( path )
			self.mode = mode
			self.has_attachments = attachments
			self.loader = UnstructuredEmailLoader( file_path=self.file_path, mode=self.mode,
				process_attachments=self.has_attachments )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'EmailLoader'
			exception.method = ('load( self, path: str, mode: str=elements, '
			                    'include_headers: bool=True ) -> List[ Document ]')
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'EmailLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class JsonLoader( Loader ):
	"""JsonLoader document loader wrapper.

	Purpose:
		Loads JSON or JSON Lines files through JSONLoader using the configured jq schema and
		text-content settings.

	Attributes:
		loader (Optional[JSONLoader]): Runtime state retained by the JsonLoader wrapper.
		file_path (str | None): Runtime state retained by the JsonLoader wrapper.
		jq (Optional[str]): Runtime state retained by the JsonLoader wrapper.
		is_text (Optional[bool]): Runtime state retained by the JsonLoader wrapper.
		is_lines (Optional[bool]): Runtime state retained by the JsonLoader wrapper.
		documents (List[Document] | None): Runtime state retained by the JsonLoader wrapper.
	"""
	loader: Optional[ JSONLoader ]
	file_path: str | None
	jq: Optional[ str ]
	is_text: Optional[ bool ]
	is_lines: Optional[ bool ]
	documents: List[ Document ] | None
	
	def __init__( self ) -> None:
		"""Initialize the JsonLoader instance.

		Purpose:
			Initializes JsonLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.is_text = None
		self.is_lines = None
		self.jq = '.messages[].content'
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	def load( self, filepath: str, is_text: bool = True, is_lines: bool = False ) -> List[
		                                                                                 Document ] | None:
		"""Load source content.

		Purpose:
			Loads JSON content into LangChain Document objects using the configured jq schema. The
			method validates the file path, records JSON parsing flags, constructs JSONLoader, and
			returns extracted document content.

		Args:
			filepath (str): Local file path used by the loader.
			is_text (bool): Is text value used to configure the JsonLoader.load operation.
			is_lines (bool): Is lines value used to configure the JsonLoader.load operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'filepath', filepath )
			self.file_path = self.verify_exists( filepath )
			self.is_text = is_text
			self.is_lines = is_lines
			self.loader = JSONLoader( file_path=self.file_path, jq_schema=self.jq,
				text_content=self.is_text, json_lines=self.is_lines )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'JsonLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
			ValueError: Raised when a required value is missing, blank, or outside the supported range.
		"""
		try:
			if self.documents is None:
				raise ValueError( 'No documents loaded!' )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'JsonLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class GithubLoader( Loader ):
	"""GithubLoader document loader wrapper.

	Purpose:
		Loads repository files through GithubFileLoader using a repository, branch, GitHub API URL,
		and file-extension filter.

	Attributes:
		loader (Optional[GithubFileLoader]): Runtime state retained by the GithubLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the GithubLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the GithubLoader wrapper.
		query (Optional[str]): Runtime state retained by the GithubLoader wrapper.
		max_documents (Optional[int]): Runtime state retained by the GithubLoader wrapper.
		max_characters (Optional[int]): Runtime state retained by the GithubLoader wrapper.
		include_all (Optional[bool]): Runtime state retained by the GithubLoader wrapper.
		query (Optional[str]): Runtime state retained by the GithubLoader wrapper.
		repo (Optional[str]): Runtime state retained by the GithubLoader wrapper.
		branch (Optional[str]): Runtime state retained by the GithubLoader wrapper.
		access_token (Optional[str]): Runtime state retained by the GithubLoader wrapper.
		github_url (Optional[str]): Runtime state retained by the GithubLoader wrapper.
		file_filter (Optional[str]): Runtime state retained by the GithubLoader wrapper.
	"""
	loader: Optional[ GithubFileLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	query: Optional[ str ]
	max_documents: Optional[ int ]
	max_characters: Optional[ int ]
	include_all: Optional[ bool ]
	query: Optional[ str ]
	repo: Optional[ str ]
	branch: Optional[ str ]
	access_token: Optional[ str ]
	github_url: Optional[ str ]
	file_filter: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize the GithubLoader instance.

		Purpose:
			Initializes GithubLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.query = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.max_documents = None
		self.max_characters = None
		self.include_all = None
		self.github_url = None
		self.repo = None
		self.branch = None
		self.file_filter = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [ 'loader',
		         'documents',
		         'splitter',
		         'pattern',
		         'file_path',
		         'expanded',
		         'candidates',
		         'resolved',
		         'chunk_size',
		         'overlap_amount',
		         'max_documents',
		         'max_characters',
		         'include_all',
		         'repo',
		         'branch',
		         'file_filter',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'split', ]
	
	def load( self, url: str, repo: str, branch: str, filetype: str = '.md' ) -> List[
		                                                                             Document ] | None:
		"""Load source content.

		Purpose:
			Loads files from a GitHub repository through GithubFileLoader. The method records
			repository, branch, API URL, and file-extension filter values before returning matching
			repository documents.

		Args:
			url (str): URL used by the web or repository loader.
			repo (str): GitHub repository name or owner/repository path.
			branch (str): Repository branch to inspect.
			filetype (str): File suffix filter used when loading repository files.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'url', url )
			self.github_url = url
			self.repo = repo
			self.branch = branch
			self.pattern = filetype
			self.file_filter = lambda file_path: file_path.endswith( self.pattern )
			self.loader = GithubFileLoader( repo=self.repo, branch=self.branch,
				github_api_url=self.github_url, file_filter=self.file_filter )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'GithubLoader'
			exception.method = 'load( self, **kwargs  ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
			ValueError: Raised when a required value is missing, blank, or outside the supported range.
		"""
		try:
			if self.documents is None:
				raise ValueError( 'No documents loaded!' )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'GithubLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			Logger( ).write( exception )
			raise exception

class XmlLoader( Loader ):
	"""XmlLoader document loader wrapper.

	Purpose:
		Loads XML files as both unstructured documents and parsed element trees for XPath-based
		extraction workflows.

	Attributes:
		file_path (Optional[str]): Runtime state retained by the XmlLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the XmlLoader wrapper.
		loader (Optional[UnstructuredXMLLoader]): Runtime state retained by the XmlLoader wrapper.
		splitter (Optional[RecursiveCharacterTextSplitter]): Runtime state retained by the XmlLoader wrapper.
		chunk_size (Optional[int]): Runtime state retained by the XmlLoader wrapper.
		overlap_amount (Optional[int]): Runtime state retained by the XmlLoader wrapper.
		xml_tree (Optional[etree._ElementTree]): Runtime state retained by the XmlLoader wrapper.
		xml_root (Optional[etree._Element]): Runtime state retained by the XmlLoader wrapper.
		xml_namespaces (Optional[Dict[str, str]]): Runtime state retained by the XmlLoader wrapper.
	"""
	
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	loader: Optional[ UnstructuredXMLLoader ]
	splitter: Optional[ RecursiveCharacterTextSplitter ]
	chunk_size: Optional[ int ]
	overlap_amount: Optional[ int ]
	xml_tree: Optional[ etree._ElementTree ]
	xml_root: Optional[ etree._Element ]
	xml_namespaces: Optional[ Dict[ str, str ] ]
	
	def __init__( self ) -> None:
		"""Initialize the XmlLoader instance.

		Purpose:
			Initializes XmlLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.loader = None
		self.splitter = None
		self.chunk_size = None
		self.overlap_amount = None
		self.xml_tree = None
		self.xml_root = None
		self.xml_namespaces = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [
				"loader",
				"documents",
				"splitter",
				"file_path",
				"expanded",
				"candidates",
				"resolved",
				"chunk_size",
				"overlap_amount",
				"xml_tree",
				"xml_root",
				"xml_namespaces",
				"verify_exists",
				"resolve_paths",
				"split_documents",
				"load",
				"split",
				"load_tree",
				"get_elements",
		]
	
	def load( self, filepath: str ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads an XML file through UnstructuredXMLLoader and returns parsed XML content as
			LangChain Document objects. The method validates the path, constructs the loader, and
			stores loaded documents.

		Args:
			filepath (str): Local file path used by the loader.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			self.file_path = self.verify_exists( filepath )
			self.loader = UnstructuredXMLLoader( file_path=self.file_path, mode="elements" )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = "chonky"
			exception.cause = "XmlLoader"
			exception.method = "load(self, filepath: str)"
			Logger( ).write( exception )
			raise exception
	
	def split( self, size: int = 1000, amount: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			size (int): Maximum chunk size used by the text splitter.
			amount (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
			ValueError: Raised when a required value is missing, blank, or outside the supported range.
		"""
		try:
			if self.documents is None:
				raise ValueError( "No documents loaded via load()." )
			self.chunk_size = size
			self.overlap_amount = amount
			split_docs = self.split_documents( docs=self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			
			return split_docs
		except Exception as e:
			exception = Error( e )
			exception.module = "chonky"
			exception.cause = "XmlLoader"
			exception.method = "split(self, size: int=1000, amount: int=200)"
			Logger( ).write( exception )
			raise exception
	
	def load_tree( self, filepath: str ) -> etree._ElementTree | None:
		"""Parse an XML element tree.

		Purpose:
			Parses a local XML file into an lxml element tree with recovery enabled. The method stores
			the tree, root element, and namespace mapping for later XPath extraction.

		Args:
			filepath (str): Local file path used by the loader.

		Returns:
			etree._ElementTree | None: Parsed XML element tree.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			self.file_path = self.verify_exists( filepath )
			parser = etree.XMLParser( recover=True, remove_comments=True, remove_blank_text=True )
			self.xml_tree = etree.parse( self.file_path, parser )
			self.xml_root = self.xml_tree.getroot( )
			self.xml_namespaces = {
					prefix if prefix is not None else "default": uri
					for prefix, uri in (self.xml_root.nsmap or { }).items( )
			}
			
			return self.xml_tree
		except Exception as e:
			exception = Error( e )
			exception.module = "chonky"
			exception.cause = "XmlLoader"
			exception.method = "load_tree(self, filepath: str)"
			Logger( ).write( exception )
			raise exception
	
	def get_elements( self, xpath: str ) -> List[ etree._Element ] | None:
		"""Return XML elements by XPath.

		Purpose:
			Runs an XPath expression against the previously loaded XML root element. The method uses
			stored namespace metadata and returns matching lxml elements as a list.

		Args:
			xpath (str): XPath expression evaluated against the loaded XML document.

		Returns:
			List[etree._Element] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
			ValueError: Raised when a required value is missing, blank, or outside the supported range.
		"""
		try:
			if self.xml_root is None:
				raise ValueError( "XML tree not loaded. Call load_tree() first." )
			elements = self.xml_root.xpath( xpath, namespaces=self.xml_namespaces )
			return list( elements )
		except Exception as e:
			exception = Error( e )
			exception.module = "chonky"
			exception.cause = "XmlLoader"
			exception.method = "get_elements(self, xpath: str)"
			Logger( ).write( exception )
			raise exception

class PubMedSearchLoader( Loader ):
	"""PubMedSearchLoader document loader wrapper.

	Purpose:
		Queries PubMed through the LangChain PubMed loader and returns biomedical literature
		results as LangChain Document objects.

	Attributes:
		loader (Optional[PubMedLoader]): Runtime state retained by the PubMedSearchLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the PubMedSearchLoader wrapper.
		query (Optional[str]): Runtime state retained by the PubMedSearchLoader wrapper.
		max_docs (Optional[int]): Runtime state retained by the PubMedSearchLoader wrapper.
	"""
	loader: Optional[ PubMedLoader ]
	documents: Optional[ List[ Document ] ]
	query: Optional[ str ]
	max_docs: Optional[ int ]
	
	def __init__( self ) -> None:
		"""Initialize the PubMedSearchLoader instance.

		Purpose:
			Initializes PubMedSearchLoader runtime state used by later loader operations. The
			constructor assigns default attributes and provider settings without loading external
			content.
		"""
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.query = None
		self.max_docs = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [
				'loader',
				'documents',
				'query',
				'max_docs',
				'chunk_size',
				'overlap_amount',
				'load',
				'split',
				'split_documents',
		]
	
	def load( self, query: str, max_docs: int = 5 ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Runs a PubMed query and loads matching biomedical literature records as LangChain Document
			objects. The method records the query and maximum result count before returning retrieved
			documents.

		Args:
			query (str): Search query submitted to the backing loader.
			max_docs (int): Maximum number of documents requested from the backing service.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'query', query )
			self.query = query
			self.max_docs = max_docs
			self.loader = PubMedLoader( query=self.query, load_max_docs=self.max_docs )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'PubMedSearchLoader'
			exception.method = (
					'load( self, query: str, max_docs: int=5 ) -> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents(
				self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'PubMedSearchLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception

class OpenCityLoader( Loader ):
	"""OpenCityLoader document loader wrapper.

	Purpose:
		Loads open city dataset records through OpenCityDataLoader and returns civic dataset
		content as LangChain Document objects.

	Attributes:
		loader (Optional[OpenCityDataLoader]): Runtime state retained by the OpenCityLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the OpenCityLoader wrapper.
		city_id (Optional[str]): Runtime state retained by the OpenCityLoader wrapper.
		dataset_id (Optional[str]): Runtime state retained by the OpenCityLoader wrapper.
		limit (Optional[int]): Runtime state retained by the OpenCityLoader wrapper.
	"""
	loader: Optional[ OpenCityDataLoader ]
	documents: Optional[ List[ Document ] ]
	city_id: Optional[ str ]
	dataset_id: Optional[ str ]
	limit: Optional[ int ]
	
	def __init__( self ) -> None:
		"""Initialize the OpenCityLoader instance.

		Purpose:
			Initializes OpenCityLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.loader = None
		self.documents = [ ]
		self.city_id = None
		self.dataset_id = None
		self.limit = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [
				'loader',
				'documents',
				'city_id',
				'dataset_id',
				'limit',
				'load',
				'split',
				'split_documents',
		]
	
	def load( self, city_id: str, dataset_id: str, limit: int = 100 ) -> List[ Document ]:
		"""Load source content.

		Purpose:
			Loads records from an open city dataset into LangChain Document objects. The method
			validates city and dataset identifiers, enforces a positive limit, constructs
			OpenCityDataLoader, and returns dataset documents.

		Args:
			city_id (str): City id value used to configure the OpenCityLoader.load operation.
			dataset_id (str): Dataset id value used to configure the OpenCityLoader.load operation.
			limit (int): Maximum number of records requested from the backing source.

		Returns:
			List[Document]: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
			ValueError: Raised when a required value is missing, blank, or outside the supported range.
		"""
		try:
			throw_if( 'city_id', city_id )
			throw_if( 'dataset_id', dataset_id )
			throw_if( 'limit', limit )
			
			if not isinstance( limit, int ) or limit < 1:
				raise ValueError( 'limit must be an integer greater than zero.' )
			
			self.city_id = city_id
			self.dataset_id = dataset_id
			self.limit = limit
			self.loader = OpenCityDataLoader(
				city_id=self.city_id,
				dataset_id=self.dataset_id,
				limit=self.limit
			)
			
			self.documents = self.loader.load( )
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'OpenCityLoader'
			exception.method = (
					'load( self, city_id: str, dataset_id: str, limit: int=100 ) '
					'-> List[ Document ]'
			)
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ]:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document]: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
				model_name='gpt-4o',
				chunk_size=self.chunk_size,
				chunk_overlap=self.overlap_amount
			)
			
			self.documents = self.splitter.split_documents( documents=self.documents )
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'OpenCityLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			)
			Logger( ).write( exception )
			raise exception

class JupyterNotebookLoader( Loader ):
	"""JupyterNotebookLoader document loader wrapper.

	Purpose:
		Loads Jupyter notebooks through NotebookLoader with configurable output, traceback,
		newline, and output-length handling.

	Attributes:
		loader (Optional[NotebookLoader]): Runtime state retained by the JupyterNotebookLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the JupyterNotebookLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the JupyterNotebookLoader wrapper.
		include_outputs (Optional[bool]): Runtime state retained by the JupyterNotebookLoader wrapper.
		max_output_length (Optional[int]): Runtime state retained by the JupyterNotebookLoader wrapper.
		remove_newline (Optional[bool]): Runtime state retained by the JupyterNotebookLoader wrapper.
		traceback (Optional[bool]): Runtime state retained by the JupyterNotebookLoader wrapper.
	"""
	loader: Optional[ NotebookLoader ]
	documents: Optional[ List[ Document ] ]
	file_path: Optional[ str ]
	include_outputs: Optional[ bool ]
	max_output_length: Optional[ int ]
	remove_newline: Optional[ bool ]
	traceback: Optional[ bool ]
	
	def __init__( self ) -> None:
		"""Initialize the JupyterNotebookLoader instance.

		Purpose:
			Initializes JupyterNotebookLoader runtime state used by later loader operations. The
			constructor assigns default attributes and provider settings without loading external
			content.
		"""
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.file_path = None
		self.include_outputs = None
		self.max_output_length = None
		self.remove_newline = None
		self.traceback = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [
				'loader',
				'documents',
				'file_path',
				'include_outputs',
				'max_output_length',
				'remove_newline',
				'traceback',
				'chunk_size',
				'overlap_amount',
				'load',
				'split',
				'split_documents',
		]
	
	def load( self, path: str, include_outputs: bool = False, max_output_length: int = 10,
			remove_newline: bool = False, traceback: bool = False ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads a Jupyter notebook into LangChain Document objects. The method validates the
			notebook path, records output and traceback settings, constructs NotebookLoader, and
			returns notebook content.

		Args:
			path (str): Local file path used by the loader.
			include_outputs (bool): Include outputs value used to configure the JupyterNotebookLoader.load operation.
			max_output_length (int): Max output length value used to configure the JupyterNotebookLoader.load operation.
			remove_newline (bool): Remove newline value used to configure the JupyterNotebookLoader.load operation.
			traceback (bool): Traceback value used to configure the JupyterNotebookLoader.load operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'path', path )
			self.file_path = self.verify_exists( path )
			self.include_outputs = include_outputs
			self.max_output_length = max_output_length
			self.remove_newline = remove_newline
			self.traceback = traceback
			
			self.loader = NotebookLoader(
				self.file_path,
				include_outputs=self.include_outputs,
				max_output_length=self.max_output_length,
				remove_newline=self.remove_newline,
				traceback=self.traceback
			)
			self.documents = self.loader.load( )
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'JupyterNotebookLoader'
			exception.method = (
					'load( self, path: str, include_outputs: bool=False, '
					'max_output_length: int=10, remove_newline: bool=False, '
					'traceback: bool=False ) -> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents(
				self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'JupyterNotebookLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception

class GoogleCloudFileLoader( Loader ):
	"""GoogleCloudFileLoader document loader wrapper.

	Purpose:
		Loads a single Google Cloud Storage blob through GCSFileLoader and returns the object
		content as LangChain Document objects.

	Attributes:
		loader (Optional[GCSFileLoader]): Runtime state retained by the GoogleCloudFileLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the GoogleCloudFileLoader wrapper.
		project_name (Optional[str]): Runtime state retained by the GoogleCloudFileLoader wrapper.
		bucket (Optional[str]): Runtime state retained by the GoogleCloudFileLoader wrapper.
		blob (Optional[str]): Runtime state retained by the GoogleCloudFileLoader wrapper.
	"""
	loader: Optional[ GCSFileLoader ]
	documents: Optional[ List[ Document ] ]
	project_name: Optional[ str ]
	bucket: Optional[ str ]
	blob: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize the GoogleCloudFileLoader instance.

		Purpose:
			Initializes GoogleCloudFileLoader runtime state used by later loader operations. The
			constructor assigns default attributes and provider settings without loading external
			content.
		"""
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.project_name = None
		self.bucket = None
		self.blob = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [
				'loader',
				'documents',
				'project_name',
				'bucket',
				'blob',
				'chunk_size',
				'overlap_amount',
				'load',
				'split',
				'split_documents',
		]
	
	def load( self, project_name: str, bucket: str, blob: str ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads a single Google Cloud Storage blob into LangChain Document objects. The method
			validates project, bucket, and blob values, constructs GCSFileLoader, and returns loaded
			object content.

		Args:
			project_name (str): Google Cloud project name used by the storage loader.
			bucket (str): Storage bucket name.
			blob (str): Cloud storage object name.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'project_name', project_name )
			throw_if( 'bucket', bucket )
			throw_if( 'blob', blob )
			self.project_name = project_name
			self.bucket = bucket
			self.blob = blob
			self.loader = GCSFileLoader( project_name=self.project_name, bucket=self.bucket,
				blob=self.blob )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'GoogleCloudStorageFileLoader'
			exception.method = (
					'load( self, project_name: str, bucket: str, blob: str ) '
					'-> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'GoogleCloudStorageFileLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception

class AwsFileLoader( Loader ):
	"""AwsFileLoader document loader wrapper.

	Purpose:
		Loads a single Amazon S3 object through S3FileLoader with optional AWS credential and
		region settings.

	Attributes:
		loader (Optional[S3FileLoader]): Runtime state retained by the AwsFileLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the AwsFileLoader wrapper.
		bucket (Optional[str]): Runtime state retained by the AwsFileLoader wrapper.
		key (Optional[str]): Runtime state retained by the AwsFileLoader wrapper.
		aws_access_key_id (Optional[str]): Runtime state retained by the AwsFileLoader wrapper.
		aws_secret_access_key (Optional[str]): Runtime state retained by the AwsFileLoader wrapper.
		aws_session_token (Optional[str]): Runtime state retained by the AwsFileLoader wrapper.
		region_name (Optional[str]): Runtime state retained by the AwsFileLoader wrapper.
	"""
	loader: Optional[ S3FileLoader ]
	documents: Optional[ List[ Document ] ]
	bucket: Optional[ str ]
	key: Optional[ str ]
	aws_access_key_id: Optional[ str ]
	aws_secret_access_key: Optional[ str ]
	aws_session_token: Optional[ str ]
	region_name: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize the AwsFileLoader instance.

		Purpose:
			Initializes AwsFileLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.bucket = None
		self.key = None
		self.aws_access_key_id = None
		self.aws_secret_access_key = None
		self.aws_session_token = None
		self.region_name = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [
				'loader',
				'documents',
				'bucket',
				'key',
				'aws_access_key_id',
				'aws_secret_access_key',
				'aws_session_token',
				'region_name',
				'chunk_size',
				'overlap_amount',
				'load',
				'split',
				'split_documents',
		]
	
	def load( self, bucket: str, key: str, aws_access_key_id: Optional[ str ] = None,
			aws_secret_access_key: Optional[ str ] = None,
			aws_session_token: Optional[ str ] = None,
			region_name: Optional[ str ] = None ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads a single Amazon S3 object into LangChain Document objects. The method validates
			bucket and key values, applies optional AWS credentials and region settings, constructs
			S3FileLoader, and returns object content.

		Args:
			bucket (str): Storage bucket name.
			key (str): Amazon S3 object key.
			aws_access_key_id (Optional[str]): Aws access key id value used to configure the AwsFileLoader.load operation.
			aws_secret_access_key (Optional[str]): Aws secret access key value used to configure the AwsFileLoader.load operation.
			aws_session_token (Optional[str]): Aws session token value used to configure the AwsFileLoader.load operation.
			region_name (Optional[str]): Region name value used to configure the AwsFileLoader.load operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'bucket', bucket )
			throw_if( 'key', key )
			
			self.bucket = bucket
			self.key = key
			self.aws_access_key_id = aws_access_key_id
			self.aws_secret_access_key = aws_secret_access_key
			self.aws_session_token = aws_session_token
			self.region_name = region_name
			
			kwargs: Dict[ str, Any ] = { }
			if self.aws_access_key_id:
				kwargs[ 'aws_access_key_id' ] = self.aws_access_key_id
			if self.aws_secret_access_key:
				kwargs[ 'aws_secret_access_key' ] = self.aws_secret_access_key
			if self.aws_session_token:
				kwargs[ 'aws_session_token' ] = self.aws_session_token
			if self.region_name:
				kwargs[ 'region_name' ] = self.region_name
			
			self.loader = S3FileLoader(
				self.bucket,
				self.key,
				**kwargs
			)
			self.documents = self.loader.load( )
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'AwsFileLoader'
			exception.method = (
					'load( self, bucket: str, key: str, '
					'aws_access_key_id: Optional[ str ]=None, '
					'aws_secret_access_key: Optional[ str ]=None, '
					'aws_session_token: Optional[ str ]=None, '
					'region_name: Optional[ str ]=None ) '
					'-> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'AwsFileLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) '
					'-> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception

class GoogleSpeechToTextLoader( Loader ):
	"""GoogleSpeechToTextLoader document loader wrapper.

	Purpose:
		Loads audio transcription output through SpeechToTextLoader using a Google Cloud project,
		file path, and optional recognition configuration.

	Attributes:
		loader (Optional[SpeechToTextLoader]): Runtime state retained by the GoogleSpeechToTextLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the GoogleSpeechToTextLoader wrapper.
		project_id (Optional[str]): Runtime state retained by the GoogleSpeechToTextLoader wrapper.
		file_path (Optional[str]): Runtime state retained by the GoogleSpeechToTextLoader wrapper.
		config (Optional[Dict[str, Any]]): Runtime state retained by the GoogleSpeechToTextLoader wrapper.
	"""
	loader: Optional[ SpeechToTextLoader ]
	documents: Optional[ List[ Document ] ]
	project_id: Optional[ str ]
	file_path: Optional[ str ]
	config: Optional[ Dict[ str, Any ] ]
	
	def __init__( self ) -> None:
		"""Initialize the GoogleSpeechToTextLoader instance.

		Purpose:
			Initializes GoogleSpeechToTextLoader runtime state used by later loader operations. The
			constructor assigns default attributes and provider settings without loading external
			content.
		"""
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.project_id = None
		self.file_path = None
		self.config = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [
				'loader',
				'documents',
				'project_id',
				'file_path',
				'config',
				'chunk_size',
				'overlap_amount',
				'load',
				'split',
				'split_documents',
		]
	
	def load( self, project_id: str, file_path: str,
			config: Optional[ Dict[ str, Any ] ] = None ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads speech-to-text transcription output into LangChain Document objects. The method
			validates project and file values, applies optional recognition configuration, constructs
			SpeechToTextLoader, and returns transcription documents.

		Args:
			project_id (str): Google Cloud project identifier used by the speech loader.
			file_path (str): File path value used to configure the GoogleSpeechToTextLoader.load operation.
			config (Optional[Dict[str, Any]]): Config value used to configure the GoogleSpeechToTextLoader.load operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'project_id', project_id )
			throw_if( 'file_path', file_path )
			
			self.project_id = project_id
			self.file_path = file_path
			self.config = config
			
			if self.config:
				self.loader = SpeechToTextLoader( project_id=self.project_id,
					file_path=self.file_path, config=self.config )
			else:
				self.loader = SpeechToTextLoader( project_id=self.project_id,
					file_path=self.file_path )
			
			self.documents = self.loader.load( )
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'GoogleSpeechToTextAudioLoader'
			exception.method = (
					'load( self, project_id: str, file_path: str, '
					'config: Optional[ Dict[ str, Any ] ]=None ) -> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents(
				self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'GoogleSpeechToTextAudioLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) '
					'-> List[ Document ] | None'
			)
			Logger( ).write( exception )
			raise exception

class GoogleBucketLoader( Loader ):
	"""GoogleBucketLoader document loader wrapper.

	Purpose:
		Loads Google Cloud Storage bucket directories through GCSDirectoryLoader with optional
		prefix and failure-continuation behavior.

	Attributes:
		loader (Optional[GCSDirectoryLoader]): Runtime state retained by the GoogleBucketLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the GoogleBucketLoader wrapper.
		project_name (Optional[str]): Runtime state retained by the GoogleBucketLoader wrapper.
		bucket (Optional[str]): Runtime state retained by the GoogleBucketLoader wrapper.
		prefix (Optional[str]): Runtime state retained by the GoogleBucketLoader wrapper.
		continue_on_failure (Optional[bool]): Runtime state retained by the GoogleBucketLoader wrapper.
	"""
	loader: Optional[ GCSDirectoryLoader ]
	documents: Optional[ List[ Document ] ]
	project_name: Optional[ str ]
	bucket: Optional[ str ]
	prefix: Optional[ str ]
	continue_on_failure: Optional[ bool ]
	
	def __init__( self ) -> None:
		"""Initialize the GoogleBucketLoader instance.

		Purpose:
			Initializes GoogleBucketLoader runtime state used by later loader operations. The
			constructor assigns default attributes and provider settings without loading external
			content.
		"""
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.project_name = None
		self.bucket = None
		self.prefix = None
		self.continue_on_failure = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [
				'loader',
				'documents',
				'project_name',
				'bucket',
				'prefix',
				'continue_on_failure',
				'chunk_size',
				'overlap_amount',
				'load',
				'split',
				'split_documents',
		]
	
	def load( self, project_name: str, bucket: str, prefix: Optional[ str ] = None,
			continue_on_failure: bool = False ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads a Google Cloud Storage bucket directory into LangChain Document objects. The method
			validates project and bucket values, applies optional prefix and failure-continuation
			settings, constructs GCSDirectoryLoader, and returns loaded bucket documents.

		Args:
			project_name (str): Google Cloud project name used by the storage loader.
			bucket (str): Storage bucket name.
			prefix (Optional[str]): Prefix value used to configure the GoogleBucketLoader.load operation.
			continue_on_failure (bool): Continue on failure value used to configure the GoogleBucketLoader.load operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'project_name', project_name )
			throw_if( 'bucket', bucket )
			self.project_name = project_name
			self.bucket = bucket
			self.prefix = prefix
			self.continue_on_failure = continue_on_failure
			kwargs: Dict[ str, Any ] = {
					'project_name': self.project_name,
					'bucket': self.bucket,
					'continue_on_failure': self.continue_on_failure,
			}
			
			if self.prefix:
				kwargs[ 'prefix' ] = self.prefix
			
			self.loader = GCSDirectoryLoader( **kwargs )
			self.documents = self.loader.load( )
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'GoogleBucketLoader'
			exception.method = 'load( self, *kwargs ) -> List[ Document ] | None'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'GoogleBucketLoader'
			exception.method = 'split( self, *args ) -> List[ Document ] | None'
			Logger( ).write( exception )
			raise exception

class AwsBucketLoader( Loader ):
	"""AwsBucketLoader document loader wrapper.

	Purpose:
		Loads Amazon S3 bucket directories through S3DirectoryLoader with optional prefix,
		credentials, region, and endpoint settings.

	Attributes:
		loader (Optional[S3DirectoryLoader]): Runtime state retained by the AwsBucketLoader wrapper.
		documents (Optional[List[Document]]): Runtime state retained by the AwsBucketLoader wrapper.
		bucket (Optional[str]): Runtime state retained by the AwsBucketLoader wrapper.
		prefix (Optional[str]): Runtime state retained by the AwsBucketLoader wrapper.
		aws_access_key_id (Optional[str]): Runtime state retained by the AwsBucketLoader wrapper.
		aws_secret_access_key (Optional[str]): Runtime state retained by the AwsBucketLoader wrapper.
		aws_session_token (Optional[str]): Runtime state retained by the AwsBucketLoader wrapper.
		region_name (Optional[str]): Runtime state retained by the AwsBucketLoader wrapper.
		endpoint_url (Optional[str]): Runtime state retained by the AwsBucketLoader wrapper.
	"""
	loader: Optional[ S3DirectoryLoader ]
	documents: Optional[ List[ Document ] ]
	bucket: Optional[ str ]
	prefix: Optional[ str ]
	aws_access_key_id: Optional[ str ]
	aws_secret_access_key: Optional[ str ]
	aws_session_token: Optional[ str ]
	region_name: Optional[ str ]
	endpoint_url: Optional[ str ]
	
	def __init__( self ) -> None:
		"""Initialize the AwsBucketLoader instance.

		Purpose:
			Initializes AwsBucketLoader runtime state used by later loader operations. The constructor
			assigns default attributes and provider settings without loading external content.
		"""
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.bucket = None
		self.prefix = None
		self.aws_access_key_id = None
		self.aws_secret_access_key = None
		self.aws_session_token = None
		self.region_name = None
		self.endpoint_url = None
	
	def __dir__( self ) -> List[ str ]:
		"""Return public member names.

		Purpose:
			Returns a stable list of attributes and callable members exposed by the wrapper. This
			supports predictable introspection, editor discovery, and API documentation output.

		Returns:
			List[str]: Stable public member names exposed by the wrapper.
		"""
		return [
				'loader',
				'documents',
				'bucket',
				'prefix',
				'aws_access_key_id',
				'aws_secret_access_key',
				'aws_session_token',
				'region_name',
				'endpoint_url',
				'chunk_size',
				'overlap_amount',
				'load',
				'split',
				'split_documents',
		]
	
	def load( self, bucket: str, prefix: Optional[ str ] = None,
			aws_access_key_id: Optional[ str ] = None,
			aws_secret_access_key: Optional[ str ] = None,
			aws_session_token: Optional[ str ] = None, region_name: Optional[ str ] = None,
			endpoint_url: Optional[ str ] = None ) -> List[ Document ] | None:
		"""Load source content.

		Purpose:
			Loads an Amazon S3 bucket directory into LangChain Document objects. The method validates
			bucket input, applies optional prefix, credential, region, and endpoint settings,
			constructs S3DirectoryLoader, and returns loaded bucket documents.

		Args:
			bucket (str): Storage bucket name.
			prefix (Optional[str]): Prefix value used to configure the AwsBucketLoader.load operation.
			aws_access_key_id (Optional[str]): Aws access key id value used to configure the AwsBucketLoader.load operation.
			aws_secret_access_key (Optional[str]): Aws secret access key value used to configure the AwsBucketLoader.load operation.
			aws_session_token (Optional[str]): Aws session token value used to configure the AwsBucketLoader.load operation.
			region_name (Optional[str]): Region name value used to configure the AwsBucketLoader.load operation.
			endpoint_url (Optional[str]): Endpoint url value used to configure the AwsBucketLoader.load operation.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'bucket', bucket )
			self.bucket = bucket
			self.prefix = prefix
			self.aws_access_key_id = aws_access_key_id
			self.aws_secret_access_key = aws_secret_access_key
			self.aws_session_token = aws_session_token
			self.region_name = region_name
			self.endpoint_url = endpoint_url
			kwargs: Dict[ str, Any ] = { }
			if self.prefix:
				kwargs[ 'prefix' ] = self.prefix
			if self.aws_access_key_id:
				kwargs[ 'aws_access_key_id' ] = self.aws_access_key_id
			if self.aws_secret_access_key:
				kwargs[ 'aws_secret_access_key' ] = self.aws_secret_access_key
			if self.aws_session_token:
				kwargs[ 'aws_session_token' ] = self.aws_session_token
			if self.region_name:
				kwargs[ 'region_name' ] = self.region_name
			if self.endpoint_url:
				kwargs[ 'endpoint_url' ] = self.endpoint_url
			
			self.loader = S3DirectoryLoader( self.bucket, **kwargs )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'AmazonBucketLoader'
			exception.method = 'load( self, bucket: str, **kwargs ) -> List[ Document ] | None'
			Logger( ).write( exception )
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		"""Split loaded documents.

		Purpose:
			Splits the documents currently stored on the loader into smaller LangChain Document
			chunks. The method records chunk size and overlap settings before returning chunked
			documents for retrieval, embedding, or analysis workflows.

		Args:
			chunk (int): Maximum chunk size used by the text splitter.
			overlap (int): Number of overlapping characters retained between adjacent chunks.

		Returns:
			List[Document] | None: Loaded or split LangChain Document objects.

		Raises:
			Error: Re-raised after the original exception is wrapped and written to the application logger.
		"""
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'AmazonBucketLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ] | None'
			Logger( ).write( exception )
			raise exception
