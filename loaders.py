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
	"""Executes the throw_if operation for the module loader workflow.
	
	Purpose:
	    Provides the `throw_if` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
	
	Args:
	    name (str): Input value passed to the callable.
	    value (object): Input value passed to the callable.
	
	Raises:
	    Error: Raised when the wrapped operation fails and the exception is logged."""
	if value is None:
		raise ValueError( f'Argument "{name}" cannot be None.' )
	
	if isinstance( value, str ) and not value.strip( ):
		raise ValueError( f'Argument "{name}" cannot be empty.' )

class Loader( ):
	"""Loader loader wrapper.
	
	Purpose:
	    Documents the `Loader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
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
		"""Validates that a local file path exists before a loader attempts to read it.
		
		Purpose:
		    Provides the `verify_exists` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Resolves a direct file path or glob expression into existing local files.
		
		Purpose:
		    Provides the `resolve_paths` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    pattern (str): Input value passed to the callable.
		
		Returns:
		    List[str]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Loads CSV-style source content into LangChain Document objects using CSV loader options.
		
		Purpose:
		    Provides the `load_documents` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		    encoding (str): Input value passed to the callable.
		    csv_args (Dict[str, object]): Input value passed to the callable.
		    source_column (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits LangChain Document objects into smaller chunks with the configured recursive text splitter.
		
		Purpose:
		    Provides the `split_documents` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    docs (List[Document]): Input value passed to the callable.
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""TextLoader loader wrapper.
	
	Purpose:
	    Documents the `TextLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ TextDocLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	encoding: Optional[ str ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.encoding = None
	
	def __dir__( self ) -> List[ str ]:
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		    encoding (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""CsvLoader loader wrapper.
	
	Purpose:
	    Documents the `CsvLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ CSVLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	encoding: Optional[ str ]
	csv_args: Optional[ Dict[ str, Any ] ]
	source_column: Optional[ str ]
	delimiter: Optional[ str ]
	quotechar: Optional[ str ]
	
	def __init__( self ) -> None:
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
		return [ 'loader', 'file_path', 'documents', 'encoding',
		         'csv_args', 'source_column', 'delimiter', 'quotechar',
		         'chunk_size', 'overlap_amount', 'load', 'split',
		         'split_documents', ]
	
	def load( self, path: str, encoding: Optional[ str ] = 'utf-8',
			source_column: Optional[ str ] = None, delimiter: str = ',',
			quotechar: str = '"' ) -> List[ Document ] | None:
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		    encoding (str): Input value passed to the callable.
		    source_column (str): Input value passed to the callable.
		    delimiter (str): Input value passed to the callable.
		    quotechar (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""WebLoader loader wrapper.
	
	Purpose:
	    Documents the `WebLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
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
		"""Executes the __init__ operation for the WebLoader loader workflow.
		
		Purpose:
		    Initializes `WebLoader` instance state while preserving the constructor contract used by the application.
		
		Args:
		    recursive (bool): Input value passed to the callable.
		    max_depth (int): Input value passed to the callable.
		    prevent_outside (bool): Input value passed to the callable.
		    timeout (int): Input value passed to the callable.
		    ignore (bool): Input value passed to the callable.
		    progress (bool): Input value passed to the callable."""
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
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Filters recursively crawled documents to sources that match the original URL domain.
		
		Purpose:
		    Provides the `_same_domain_only` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    docs (List[Document]): Input value passed to the callable.
		    source_url (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    urls (str | List[str]): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Recursively loads documents from a starting URL.
		
		Purpose:
		    Provides the `load_recursive` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    url (str): Input value passed to the callable.
		    depth (int): Input value passed to the callable.
		    max_time (int): Input value passed to the callable.
		    ignore (bool): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Loads documents from one or more static web pages.
		
		Purpose:
		    Provides the `load_pages` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    urls (List[str]): Input value passed to the callable.
		    depth (int): Input value passed to the callable.
		    timeout (int): Input value passed to the callable.
		    ignore (bool): Input value passed to the callable.
		    progress (bool): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""PdfReader loader wrapper.
	
	Purpose:
	    Documents the `PdfReader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ PyPDFLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	mode: Optional[ str ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.mode = None
	
	def __dir__( self ) -> List[ str ]:
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		    mode (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""PdfLoader loader wrapper.
	
	Purpose:
	    Documents the `PdfLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
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
		"""Executes the __init__ operation for the PdfLoader loader workflow.
		
		Purpose:
		    Initializes `PdfLoader` instance state while preserving the constructor contract used by the application.
		
		Args:
		    size (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		    has_tables (bool): Input value passed to the callable.
		    include (bool): Input value passed to the callable."""
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
		"""Returns the supported loading mode names for the loader.
		
		Purpose:
		    Provides the `mode_options` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
		return [ 'page', 'single' ]
	
	@property
	def extraction_options( self ) -> List[ str ]:
		"""Returns the supported PDF extraction mode names.
		
		Purpose:
		    Provides the `extraction_options` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
		return [ 'plain', 'layout' ]
	
	@property
	def image_options( self ) -> List[ str ]:
		"""Returns the supported PDF image-output format names.
		
		Purpose:
		    Provides the `image_options` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
		return [ 'html-img', 'markdown-img', 'text-img' ]
	
	def load( self, path: str, mode: str = 'single', extract: str = 'plain',
			include: bool = False, format: str = 'markdown-img' ) -> List[ Document ]:
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		    mode (str): Input value passed to the callable.
		    extract (str): Input value passed to the callable.
		    include (bool): Input value passed to the callable.
		    format (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""ExcelLoader loader wrapper.
	
	Purpose:
	    Documents the `ExcelLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ UnstructuredExcelLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	mode: Optional[ str ]
	has_headers: Optional[ bool ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.mode = None
	
	def __dir__( self ) -> List[ str ]:
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Returns the supported loading mode names for the loader.
		
		Purpose:
		    Provides the `mode_options` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
		return [ 'single', 'page' ]
	
	def load( self, path: str, mode: str = 'elements', has_headers: bool = True ) -> List[
		                                                                                 Document ] | None:
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		    mode (str): Input value passed to the callable.
		    has_headers (bool): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""WordLoader loader wrapper.
	
	Purpose:
	    Documents the `WordLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ Docx2txtLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.documents = None
		self.file_path = None
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
	
	def __dir__( self ) -> List[ str ]:
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""MarkdownLoader loader wrapper.
	
	Purpose:
	    Documents the `MarkdownLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ UnstructuredMarkdownLoader ]
	file_path: str | None
	documents: List[ Document ] | None
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
	
	def __dir__( self ) -> List[ str ]:
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""HtmlLoader loader wrapper.
	
	Purpose:
	    Documents the `HtmlLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ UnstructuredHTMLLoader ]
	file_path: str | None
	documents: List[ Document ] | None
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
	
	def __dir__( self ) -> List[ str ]:
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""ArXivLoader loader wrapper.
	
	Purpose:
	    Documents the `ArXivLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ ArxivLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	max_documents: Optional[ int ]
	max_characters: Optional[ int ]
	include_metadata: Optional[ bool ]
	query: Optional[ str ]
	
	def __init__( self ) -> None:
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
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    question (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""WikiLoader loader wrapper.
	
	Purpose:
	    Documents the `WikiLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ WikipediaLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	query: Optional[ str ]
	max_documents: Optional[ int ]
	max_characters: Optional[ int ]
	include_all: Optional[ bool ]
	query: Optional[ str ]
	
	def __init__( self ) -> None:
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
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    question (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""GoogleDriveLoader loader wrapper.
	
	Purpose:
	    Documents the `GoogleDriveLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ GoogleDriveLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	query: Optional[ str ]
	file_id: Optional[ str ]
	folder_id: Optional[ str ]
	query: Optional[ str ]
	is_recursive: Optional[ bool ]
	
	def __init__( self ) -> None:
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
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Returns the supported Google Drive loading target names.
		
		Purpose:
		    Provides the `file_options` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
		return [ 'document',
		         'sheet',
		         'pdf' ]
	
	def load_file( self, file_id: str, recursive: bool = False ) -> List[ Document ] | None:
		"""Loads a single file from the backing provider.
		
		Purpose:
		    Provides the `load_file` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    file_id (str): Input value passed to the callable.
		    recursive (bool): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Loads documents from a provider folder or document-library folder.
		
		Purpose:
		    Provides the `load_folder` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    folder_id (str): Input value passed to the callable.
		    recursive (bool): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""OutlookLoader loader wrapper.
	
	Purpose:
	    Documents the `OutlookLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ OutlookMessageLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	query: Optional[ str ]
	max_documents: Optional[ int ]
	max_characters: Optional[ int ]
	query: Optional[ str ]
	
	def __init__( self ) -> None:
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
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""SpfxLoader loader wrapper.
	
	Purpose:
	    Documents the `SpfxLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
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
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    library_id (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Loads documents from a provider folder or document-library folder.
		
		Purpose:
		    Provides the `load_folder` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    library_id (str): Input value passed to the callable.
		    folder_id (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""PowerPointLoader loader wrapper.
	
	Purpose:
	    Documents the `PowerPointLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ UnstructuredPowerPointLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	mode: Optional[ str ]
	query: Optional[ str ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.query = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.mode = None
	
	def __dir__( self ) -> List[ str ]:
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		    mode (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Loads documents from a multi-document source using the loader’s existing path contract.
		
		Purpose:
		    Provides the `load_multiple` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""OneDriveDocLoader loader wrapper.
	
	Purpose:
	    Documents the `OneDriveDocLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ OneDriveLoader ]
	documents: Optional[ List[ Document ] ]
	drive_id: Optional[ str ]
	folder_path: Optional[ str ]
	object_ids: Optional[ List[ str ] ]
	auth_with_token: Optional[ bool ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.drive_id = None
		self.folder_path = None
		self.object_ids = None
		self.auth_with_token = None
	
	def __dir__( self ) -> List[ str ]:
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    drive_id (str): Input value passed to the callable.
		    folder_path (str): Input value passed to the callable.
		    object_ids (List[str]): Input value passed to the callable.
		    auth_with_token (bool): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""EmailLoader loader wrapper.
	
	Purpose:
	    Documents the `EmailLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ UnstructuredEmailLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	has_attachments: Optional[ bool ]
	mode: Optional[ str ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.pattern = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.mode = None
	
	def __dir__( self ) -> List[ str ]:
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		    mode (str): Input value passed to the callable.
		    attachments (bool): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""JsonLoader loader wrapper.
	
	Purpose:
	    Documents the `JsonLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ JSONLoader ]
	file_path: str | None
	jq: Optional[ str ]
	is_text: Optional[ bool ]
	is_lines: Optional[ bool ]
	documents: List[ Document ] | None
	
	def __init__( self ) -> None:
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
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    filepath (str): Input value passed to the callable.
		    is_text (bool): Input value passed to the callable.
		    is_lines (bool): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""GithubLoader loader wrapper.
	
	Purpose:
	    Documents the `GithubLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
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
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    url (str): Input value passed to the callable.
		    repo (str): Input value passed to the callable.
		    branch (str): Input value passed to the callable.
		    filetype (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""XmlLoader loader wrapper.
	
	Purpose:
	    Documents the `XmlLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	
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
		"""Returns the public attributes and callable members exposed by this loader wrapper.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    filepath (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    size (int): Input value passed to the callable.
		    amount (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Parses an XML file into an element tree.
		
		Purpose:
		    Provides the `load_tree` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    filepath (str): Input value passed to the callable.
		
		Returns:
		    etree._ElementTree: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Returns XML elements matching the supplied XPath expression.
		
		Purpose:
		    Provides the `get_elements` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    xpath (str): Input value passed to the callable.
		
		Returns:
		    List[etree._Element]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""PubMedSearchLoader loader wrapper.
	
	Purpose:
	    Documents the `PubMedSearchLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ PubMedLoader ]
	documents: Optional[ List[ Document ] ]
	query: Optional[ str ]
	max_docs: Optional[ int ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.query = None
		self.max_docs = None
	
	def __dir__( self ) -> List[ str ]:
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    query (str): Input value passed to the callable.
		    max_docs (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""OpenCityLoader loader wrapper.
	
	Purpose:
	    Documents the `OpenCityLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ OpenCityDataLoader ]
	documents: Optional[ List[ Document ] ]
	city_id: Optional[ str ]
	dataset_id: Optional[ str ]
	limit: Optional[ int ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.loader = None
		self.documents = [ ]
		self.city_id = None
		self.dataset_id = None
		self.limit = None
	
	def __dir__( self ) -> List[ str ]:
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    city_id (str): Input value passed to the callable.
		    dataset_id (str): Input value passed to the callable.
		    limit (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""JupyterNotebookLoader loader wrapper.
	
	Purpose:
	    Documents the `JupyterNotebookLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ NotebookLoader ]
	documents: Optional[ List[ Document ] ]
	file_path: Optional[ str ]
	include_outputs: Optional[ bool ]
	max_output_length: Optional[ int ]
	remove_newline: Optional[ bool ]
	traceback: Optional[ bool ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.file_path = None
		self.include_outputs = None
		self.max_output_length = None
		self.remove_newline = None
		self.traceback = None
	
	def __dir__( self ) -> List[ str ]:
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    path (str): Input value passed to the callable.
		    include_outputs (bool): Input value passed to the callable.
		    max_output_length (int): Input value passed to the callable.
		    remove_newline (bool): Input value passed to the callable.
		    traceback (bool): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""GoogleCloudFileLoader loader wrapper.
	
	Purpose:
	    Documents the `GoogleCloudFileLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ GCSFileLoader ]
	documents: Optional[ List[ Document ] ]
	project_name: Optional[ str ]
	bucket: Optional[ str ]
	blob: Optional[ str ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.project_name = None
		self.bucket = None
		self.blob = None
	
	def __dir__( self ) -> List[ str ]:
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    project_name (str): Input value passed to the callable.
		    bucket (str): Input value passed to the callable.
		    blob (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""AwsFileLoader loader wrapper.
	
	Purpose:
	    Documents the `AwsFileLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ S3FileLoader ]
	documents: Optional[ List[ Document ] ]
	bucket: Optional[ str ]
	key: Optional[ str ]
	aws_access_key_id: Optional[ str ]
	aws_secret_access_key: Optional[ str ]
	aws_session_token: Optional[ str ]
	region_name: Optional[ str ]
	
	def __init__( self ) -> None:
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    bucket (str): Input value passed to the callable.
		    key (str): Input value passed to the callable.
		    aws_access_key_id (str): Input value passed to the callable.
		    aws_secret_access_key (str): Input value passed to the callable.
		    aws_session_token (str): Input value passed to the callable.
		    region_name (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""GoogleSpeechToTextLoader loader wrapper.
	
	Purpose:
	    Documents the `GoogleSpeechToTextLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ SpeechToTextLoader ]
	documents: Optional[ List[ Document ] ]
	project_id: Optional[ str ]
	file_path: Optional[ str ]
	config: Optional[ Dict[ str, Any ] ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.project_id = None
		self.file_path = None
		self.config = None
	
	def __dir__( self ) -> List[ str ]:
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    project_id (str): Input value passed to the callable.
		    file_path (str): Input value passed to the callable.
		    config (Dict[str, object]): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""GoogleBucketLoader loader wrapper.
	
	Purpose:
	    Documents the `GoogleBucketLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	loader: Optional[ GCSDirectoryLoader ]
	documents: Optional[ List[ Document ] ]
	project_name: Optional[ str ]
	bucket: Optional[ str ]
	prefix: Optional[ str ]
	continue_on_failure: Optional[ bool ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.loader = None
		self.documents = None
		self.project_name = None
		self.bucket = None
		self.prefix = None
		self.continue_on_failure = None
	
	def __dir__( self ) -> List[ str ]:
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    project_name (str): Input value passed to the callable.
		    bucket (str): Input value passed to the callable.
		    prefix (str): Input value passed to the callable.
		    continue_on_failure (bool): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
	"""AwsBucketLoader loader wrapper.
	
	Purpose:
	    Documents the `AwsBucketLoader` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
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
		"""Loads source content into LangChain Document objects using the wrapped provider-specific loader.
		
		Purpose:
		    Provides the `load` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    bucket (str): Input value passed to the callable.
		    prefix (str): Input value passed to the callable.
		    aws_access_key_id (str): Input value passed to the callable.
		    aws_secret_access_key (str): Input value passed to the callable.
		    aws_session_token (str): Input value passed to the callable.
		    region_name (str): Input value passed to the callable.
		    endpoint_url (str): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
		"""Splits the currently loaded documents into smaller LangChain Document chunks.
		
		Purpose:
		    Provides the `split` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    chunk (int): Input value passed to the callable.
		    overlap (int): Input value passed to the callable.
		
		Returns:
		    List[Document]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
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
