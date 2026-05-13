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

	     name.py
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
    name.py
  </summary>
  ******************************************************************************************
'''
import arxiv
import docx2txt

from boogr import Error
import config as cfg
import glob
from langchain_community.chat_models import ChatOpenAI
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
from langchain_community.document_loaders import (
	CSVLoader,
	Docx2txtLoader,
	PyPDFLoader,
	JSONLoader,
	GithubFileLoader,
	UnstructuredExcelLoader,
	RecursiveUrlLoader,
	WebBaseLoader,
	YoutubeLoader,
	ArxivLoader,
	WikipediaLoader,
	UnstructuredEmailLoader,
	SharePointLoader,
	GoogleDriveLoader,
	UnstructuredPowerPointLoader,
	OutlookMessageLoader,
	OneDriveLoader,
	UnstructuredXMLLoader,
	PubMedLoader,
	OpenCityDataLoader,
	NotebookLoader,
	S3FileLoader,
)

from langchain_google_community import (GCSFileLoader, SpeechToTextLoader)
from langchain_community.document_loaders import S3DirectoryLoader
from langchain_google_community import GCSDirectoryLoader
from langchain_community.document_loaders.parsers import PyPDFParser
from langchain_core.document_loaders.base import BaseLoader
from langchain_community.document_loaders.parsers import RapidOCRBlobParser
import os
from pathlib import Path
import re
from typing import Optional, List, Dict, Any
import wikipedia
from lxml import etree

def throw_if( name: str, value: Any ) -> None:
	'''

		Purpose:
		-----------
		Simple guard which raises ValueError when `value` is falsy (None, empty).

		Parameters:
		-----------
		name (str): Variable name used in the raised message.
		value (Any): Value to validate.

		Returns:
		-----------
		None: Raises ValueError when `value` is falsy.

	'''
	if value is None:
		raise ValueError( f"Argument '{name}' cannot be empty!" )

class Loader( ):
	'''

		Purpose:
		--------
		Base class providing shared utilities for concrete loader wrappers.
		Encapsulates file validation, path resolution, concrete loader execution, and
		document splitting.

		Attributes:
		-----------
		documents - List[Document]
		file_path - str
		pattern - str
		expanded - List[str]
		candidates - List[str]
		resolved - List[str]
		loader - BaseLoader
		splitter - RecursiveCharacterTextSplitter | CharacterTextSplitter
		chunk_size - int
		overlap_amount - int

		Methods:
		--------
		verify_exists( self, path: str ) -> str
		resolve_paths( self, pattern: str ) -> List[str]
		load_documents( self, loader: BaseLoader ) -> List[Document]
		split_documents( self, docs: List[Document], chunk: int=1000,
			overlap: int=200 ) -> List[Document]
		validate_chunking( self, chunk: int, overlap: int ) -> None

	'''
	documents: Optional[ List[ Document ] ]
	file_path: Optional[ str ]
	pattern: Optional[ str ]
	expanded: Optional[ List[ str ] ]
	candidates: Optional[ List[ str ] ]
	resolved: Optional[ List[ str ] ]
	loader: Optional[ BaseLoader ]
	splitter: Optional[ RecursiveCharacterTextSplitter | CharacterTextSplitter ]
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
		self.splitter = None
	
	def verify_exists( self, path: str ) -> str:
		'''

			Purpose:
			--------
			Ensure the given file path exists before a concrete loader receives it.

			Parameters:
			-----------
			path (str): Path to a file on disk.

			Returns:
			--------
			str: Validated absolute file path.

		'''
		try:
			throw_if( 'path', path )
			
			if not isinstance( path, str ):
				raise TypeError( 'path must be a string.' )
			
			self.file_path = str( Path( path ).expanduser( ).resolve( ) )
			
			if not os.path.isfile( self.file_path ):
				raise FileNotFoundError( f'File not found: {self.file_path}' )
			
			return self.file_path
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'Loader'
			exception.method = 'verify_exists( self, path: str ) -> str'
			raise exception
	
	def resolve_paths( self, pattern: str ) -> List[ str ]:
		'''

			Purpose:
			--------
			Normalize a path or glob pattern to a de-duplicated list of existing file paths.

			Parameters:
			-----------
			pattern (str): Path pattern or file path.

			Returns:
			--------
			List[str]: Validated list of absolute file paths.

		'''
		try:
			throw_if( 'pattern', pattern )
			
			if not isinstance( pattern, str ):
				raise TypeError( 'pattern must be a string.' )
			
			self.pattern = pattern
			self.candidates = [ pattern ]
			self.resolved = [ ]
			
			for candidate in self.candidates:
				expanded = str( Path( candidate ).expanduser( ) )
				
				if os.path.isfile( expanded ):
					self.resolved.append( str( Path( expanded ).resolve( ) ) )
				else:
					for match in glob.glob( expanded ):
						if os.path.isfile( match ):
							self.resolved.append( str( Path( match ).resolve( ) ) )
			
			if not self.resolved:
				raise FileNotFoundError( f'No files matched or existed for input: {pattern}' )
			
			return sorted( set( self.resolved ) )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'Loader'
			exception.method = 'resolve_paths( self, pattern: str ) -> List[ str ]'
			raise exception
	
	def load_documents( self, loader: BaseLoader ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Load documents from a concrete LangChain loader instance.

			Parameters:
			-----------
			loader (BaseLoader): Concrete LangChain loader instance exposing load().

			Returns:
			--------
			List[Document]: Loaded LangChain Document objects.

		'''
		try:
			throw_if( 'loader', loader )
			
			if not hasattr( loader, 'load' ):
				raise TypeError( 'loader must expose a load() method.' )
			
			self.loader = loader
			self.documents = self.loader.load( )
			
			if self.documents is None:
				raise ValueError( 'loader returned no documents.' )
			
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'Loader'
			exception.method = 'load_documents( self, loader: BaseLoader ) -> List[ Document ]'
			raise exception
	
	def validate_chunking( self, chunk: int, overlap: int ) -> None:
		'''

			Purpose:
			--------
			Validate chunking parameters before a splitter is constructed.

			Parameters:
			-----------
			chunk (int): Maximum number of characters per chunk.
			overlap (int): Number of overlapping characters between chunks.

			Returns:
			--------
			None

		'''
		try:
			throw_if( 'chunk', chunk )
			throw_if( 'overlap', overlap )
			
			if not isinstance( chunk, int ):
				raise TypeError( 'chunk must be an integer.' )
			
			if not isinstance( overlap, int ):
				raise TypeError( 'overlap must be an integer.' )
			
			if chunk < 1:
				raise ValueError( 'chunk must be greater than zero.' )
			
			if overlap < 0:
				raise ValueError( 'overlap cannot be negative.' )
			
			if overlap >= chunk:
				raise ValueError( 'overlap must be less than chunk.' )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'Loader'
			exception.method = 'validate_chunking( self, chunk: int, overlap: int ) -> None'
			raise exception
	
	def split_documents( self, docs: List[ Document ], chunk: int = 1000,
			overlap: int = 200 ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Split long Document objects into smaller chunks.

			Parameters:
			-----------
			docs (List[Document]): Input LangChain Document objects.
			chunk (int): Maximum number of characters in each chunk.
			overlap (int): Overlapping characters between chunks.

			Returns:
			--------
			List[Document]: Re-chunked list of Document objects.

		'''
		try:
			throw_if( 'docs', docs )
			self.validate_chunking( chunk=chunk, overlap=overlap )
			
			if not isinstance( docs, list ):
				raise TypeError( 'docs must be a list of Document objects.' )
			
			self.documents = docs
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
			exception.cause = 'Loader'
			exception.method = (
					'split_documents( self, docs: List[ Document ], chunk: int=1000, '
					'overlap: int=200 ) -> List[ Document ]'
			)
			raise exception

class TextLoader( Loader ):
	'''

		Purpose:
		--------
		Class for loading text documents.

	'''
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	splitter: Optional[ RecursiveCharacterTextSplitter | CharacterTextSplitter ]
	raw_text: Optional[ str ]
	separator: Optional[ str ]
	length_function: Optional[ object ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.raw_text = None
		self.documents = [ ]
		self.separator = "\n\n"
		self.length_function = len
	
	def __dir__( self ) -> List[ str ]:
		'''

			Purpose:
			--------
			Return available members in a stable order.

			Parameters:
			-----------
			None

			Returns:
			--------
			List[str]: Available members.

		'''
		return [
				'documents',
				'splitter',
				'pattern',
				'file_path',
				'expanded',
				'candidates',
				'resolved',
				'chunk_size',
				'overlap_amount',
				'raw_text',
				'separator',
				'length_function',
				'verify_exists',
				'resolve_paths',
				'load_documents',
				'split_documents',
				'validate_chunking',
				'load',
				'split_tokens',
				'split_chars',
		]
	
	def load( self, filepath: str ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Load raw text from a file into a single LangChain Document.

			Parameters:
			-----------
			filepath (str): Path to the text file.

			Returns:
			--------
			List[Document]: Single-item list containing the loaded text document.

		'''
		try:
			throw_if( 'filepath', filepath )
			
			self.file_path = self.verify_exists( filepath )
			
			with open( self.file_path, mode='r', encoding='utf-8', errors='ignore' ) as handle:
				self.raw_text = handle.read( )
			
			self.documents = [
					Document(
						page_content=self.raw_text if isinstance( self.raw_text, str ) else '',
						metadata={
								'source': os.path.basename( self.file_path ),
								'loader': 'TextLoader',
								'path': self.file_path,
						}
					)
			]
			
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'TextLoader'
			exception.method = 'load( self, filepath: str ) -> List[ Document ]'
			raise exception
	
	def split_tokens( self, size: int = 1000, amount: int = 200 ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Split loaded text into token-aware chunks.

			Parameters:
			-----------
			size (int): Maximum chunk size.
			amount (int): Number of overlapping characters.

			Returns:
			--------
			List[Document]: Token-aware text chunks.

		'''
		try:
			self.validate_chunking( chunk=size, overlap=amount )
			
			if not isinstance( self.raw_text, str ) or not self.raw_text:
				raise ValueError( 'No text loaded. Call load() before split_tokens().' )
			
			self.chunk_size = size
			self.overlap_amount = amount
			self.splitter = CharacterTextSplitter.from_tiktoken_encoder(
				encoding_name='cl100k_base',
				chunk_size=self.chunk_size,
				chunk_overlap=self.overlap_amount
			)
			
			self.documents = self.splitter.create_documents( texts=[ self.raw_text ] )
			
			for document in self.documents:
				if not isinstance( getattr( document, 'metadata', None ), dict ):
					document.metadata = { }
				
				document.metadata.setdefault(
					'source',
					os.path.basename( self.file_path ) if self.file_path else ''
				)
				document.metadata[ 'loader' ] = 'TextLoader'
				document.metadata[ 'split_mode' ] = 'tokens'
			
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'TextLoader'
			exception.method = (
					'split_tokens( self, size: int=1000, amount: int=200 ) '
					'-> List[ Document ]'
			)
			raise exception
	
	def split_chars( self, size: int = 1000, amount: int = 200,
			seps: str = "\n\n" ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Split loaded text into character-aware chunks.

			Parameters:
			-----------
			size (int): Maximum chunk size.
			amount (int): Number of overlapping characters.
			seps (str): Separator used by the character splitter.

			Returns:
			--------
			List[Document]: Character-aware text chunks.

		'''
		try:
			self.validate_chunking( chunk=size, overlap=amount )
			throw_if( 'seps', seps )
			
			if not isinstance( self.raw_text, str ) or not self.raw_text:
				raise ValueError( 'No text loaded. Call load() before split_chars().' )
			
			self.chunk_size = size
			self.overlap_amount = amount
			self.separator = seps
			self.splitter = CharacterTextSplitter(
				separator=self.separator,
				chunk_size=self.chunk_size,
				chunk_overlap=self.overlap_amount,
				length_function=self.length_function
			)
			
			self.documents = self.splitter.create_documents( texts=[ self.raw_text ] )
			
			for document in self.documents:
				if not isinstance( getattr( document, 'metadata', None ), dict ):
					document.metadata = { }
				
				document.metadata.setdefault(
					'source',
					os.path.basename( self.file_path ) if self.file_path else ''
				)
				document.metadata[ 'loader' ] = 'TextLoader'
				document.metadata[ 'split_mode' ] = 'chars'
			
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'TextLoader'
			exception.method = (
					'split_chars( self, size: int=1000, amount: int=200, '
					'seps: str="\\n\\n" ) -> List[ Document ]'
			)
			raise exception

class CsvLoader( Loader ):
	'''

		Purpose:
		--------
		Provides CSVLoader functionality to parse CSV files into Document objects.

	'''
	loader: Optional[ CSVLoader ]
	documents: Optional[ List[ Document ] ]
	splitter: Optional[ RecursiveCharacterTextSplitter ]
	file_path: Optional[ str ]
	quote_char: Optional[ str ]
	csv_args: Optional[ Dict[ str, Any ] ]
	columns: Optional[ List[ str ] ]
	source_column: Optional[ str ]
	encoding: Optional[ str ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.columns = None
		self.csv_args = None
		self.documents = [ ]
		self.quote_char = '"'
		self.pattern = ','
		self.loader = None
		self.source_column = None
		self.encoding = None
	
	def __dir__( self ) -> List[ str ]:
		'''

			Purpose:
			--------
			Return available members in a stable order.

			Parameters:
			-----------
			None

			Returns:
			--------
			List[str]: Available members.

		'''
		return [
				'loader',
				'documents',
				'splitter',
				'pattern',
				'delimiter',
				'file_path',
				'expanded',
				'candidates',
				'resolved',
				'chunk_size',
				'overlap_amount',
				'verify_exists',
				'resolve_paths',
				'load_documents',
				'split_documents',
				'validate_chunking',
				'load',
				'split',
				'csv_args',
				'columns',
				'source_column',
				'encoding',
		]
	
	def load( self, filepath: str, columns: Optional[ List[ str ] ] = None,
			delimiter: str = ',', quotechar: str = '"',
			source_column: Optional[ str ] = None,
			encoding: Optional[ str ] = None ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Load a CSV file into LangChain Document objects.

			Parameters:
			-----------
			filepath (str): Path to the CSV file.
			columns (Optional[List[str]]): Optional list of content columns.
			delimiter (str): CSV delimiter character.
			quotechar (str): CSV quote character.
			source_column (Optional[str]): Optional source column name.
			encoding (Optional[str]): Optional file encoding.

			Returns:
			--------
			List[Document]: Parsed CSV documents.

		'''
		try:
			throw_if( 'filepath', filepath )
			throw_if( 'delimiter', delimiter )
			throw_if( 'quotechar', quotechar )
			
			self.file_path = self.verify_exists( filepath )
			self.columns = columns
			self.pattern = delimiter
			self.quote_char = quotechar
			self.source_column = source_column
			self.encoding = encoding
			self.csv_args = {
					'delimiter': self.pattern,
					'quotechar': self.quote_char,
			}
			
			if self.columns is not None and not isinstance( self.columns, list ):
				raise TypeError( 'columns must be None or a list of strings.' )
			
			self.loader = CSVLoader(
				file_path=self.file_path,
				source_column=self.source_column,
				csv_args=self.csv_args,
				encoding=self.encoding,
				content_columns=tuple( self.columns ) if self.columns else tuple( )
			)
			
			return self.load_documents( self.loader )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'CsvLoader'
			exception.method = (
					'load( self, filepath: str, columns: Optional[ List[ str ] ]=None, '
					'delimiter: str=",", quotechar: str=\'"\', '
					'source_column: Optional[ str ]=None, encoding: Optional[ str ]=None ) '
					'-> List[ Document ]'
			)
			raise exception
	
	def split( self, size: int = 1000, amount: int = 200 ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Split loaded CSV documents into smaller text chunks.

			Parameters:
			-----------
			size (int): Maximum number of characters per chunk.
			amount (int): Number of overlapping characters between chunks.

			Returns:
			--------
			List[Document]: List of split Document chunks.

		'''
		try:
			throw_if( 'documents', self.documents )
			self.validate_chunking( chunk=size, overlap=amount )
			
			self.chunk_size = size
			self.overlap_amount = amount
			return self.split_documents(
				docs=self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'CsvLoader'
			exception.method = (
					'split( self, size: int=1000, amount: int=200 ) -> List[ Document ]'
			)
			raise exception

class XmlLoader( Loader ):
	'''

		Purpose:
		--------
		Load XML files using UnstructuredXMLLoader for semantic documents and lxml for
		structured XML tree processing.

	'''
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
		self.documents = [ ]
		self.loader = None
		self.splitter = None
		self.xml_tree = None
		self.xml_root = None
		self.xml_namespaces = None
	
	def __dir__( self ) -> List[ str ]:
		'''

			Purpose:
			--------
			Return available members in a stable order.

			Parameters:
			-----------
			None

			Returns:
			--------
			List[str]: Available members.

		'''
		return [
				'loader',
				'documents',
				'splitter',
				'file_path',
				'expanded',
				'candidates',
				'resolved',
				'chunk_size',
				'overlap_amount',
				'xml_tree',
				'xml_root',
				'xml_namespaces',
				'verify_exists',
				'resolve_paths',
				'load_documents',
				'split_documents',
				'validate_chunking',
				'load',
				'split',
				'load_tree',
				'get_elements',
		]
	
	def load( self, filepath: str, mode: str = 'elements' ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Load an XML file using LangChain's UnstructuredXMLLoader.

			Parameters:
			-----------
			filepath (str): Path to the XML file.
			mode (str): Unstructured loader mode.

			Returns:
			--------
			List[Document]: Parsed LangChain Document objects.

		'''
		try:
			throw_if( 'filepath', filepath )
			throw_if( 'mode', mode )
			
			self.file_path = self.verify_exists( filepath )
			self.loader = UnstructuredXMLLoader( file_path=self.file_path, mode=mode )
			return self.load_documents( self.loader )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'XmlLoader'
			exception.method = (
					'load( self, filepath: str, mode: str="elements" ) -> List[ Document ]'
			)
			raise exception
	
	def split( self, size: int = 1000, amount: int = 200 ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Split loaded unstructured XML documents into smaller chunks.

			Parameters:
			-----------
			size (int): Maximum number of characters per chunk.
			amount (int): Number of overlapping characters between chunks.

			Returns:
			--------
			List[Document]: Split Document chunks.

		'''
		try:
			throw_if( 'documents', self.documents )
			self.validate_chunking( chunk=size, overlap=amount )
			
			self.chunk_size = size
			self.overlap_amount = amount
			return self.split_documents(
				docs=self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'XmlLoader'
			exception.method = (
					'split( self, size: int=1000, amount: int=200 ) -> List[ Document ]'
			)
			raise exception
	
	def load_tree( self, filepath: str ) -> etree._ElementTree:
		'''

			Purpose:
			--------
			Parse an XML file into a structured lxml ElementTree.

			Parameters:
			-----------
			filepath (str): Path to the XML file.

			Returns:
			--------
			etree._ElementTree: Parsed XML tree.

		'''
		try:
			throw_if( 'filepath', filepath )
			
			self.file_path = self.verify_exists( filepath )
			parser = etree.XMLParser( recover=True, remove_comments=True, remove_blank_text=True )
			self.xml_tree = etree.parse( self.file_path, parser )
			self.xml_root = self.xml_tree.getroot( )
			self.xml_namespaces = {
					prefix if prefix is not None else 'default': uri
					for prefix, uri in (self.xml_root.nsmap or { }).items( )
			}
			
			return self.xml_tree
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'XmlLoader'
			exception.method = 'load_tree( self, filepath: str ) -> etree._ElementTree'
			raise exception
	
	def get_elements( self, xpath: str ) -> List[ etree._Element ]:
		'''

			Purpose:
			--------
			Retrieve XML elements using an XPath expression against the loaded XML tree.

			Parameters:
			-----------
			xpath (str): XPath expression.

			Returns:
			--------
			List[etree._Element]: Matching XML elements.

		'''
		try:
			throw_if( 'xpath', xpath )
			
			if self.xml_root is None:
				raise ValueError( 'XML tree not loaded. Call load_tree() first.' )
			
			elements = self.xml_root.xpath( xpath, namespaces=self.xml_namespaces )
			return list( elements )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'XmlLoader'
			exception.method = 'get_elements( self, xpath: str ) -> List[ etree._Element ]'
			raise exception

class WebLoader( Loader ):
	'''

		Purpose:
		--------
		Load one or more webpages into LangChain Document objects, with optional
		recursive crawling support.

	'''
	loader: Optional[ RecursiveUrlLoader | WebBaseLoader ]
	url: Optional[ str ]
	web_paths: Optional[ str | List[ str ] ]
	documents: Optional[ List[ Document ] ]
	file_path: Optional[ str ]
	max_depth: Optional[ int ]
	timeout: Optional[ int ]
	ignore: Optional[ bool ]
	with_progress: Optional[ bool ]
	recursive: Optional[ bool ]
	prevent_outside: Optional[ bool ]
	
	def __init__( self, recursive: bool = False, max_depth: int = 2,
			prevent_outside: bool = True, timeout: int = 10,
			ignore: bool = True, progress: bool = True ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.loader = None
		self.url = None
		self.web_paths = None
		self.max_depth = max_depth
		self.timeout = timeout
		self.ignore = ignore
		self.with_progress = progress
		self.recursive = recursive
		self.prevent_outside = prevent_outside
	
	def __dir__( self ) -> List[ str ]:
		'''

			Purpose:
			--------
			Return available members in a stable order.

			Parameters:
			-----------
			None

			Returns:
			--------
			List[str]: Available members.

		'''
		return [
				'loader',
				'documents',
				'splitter',
				'pattern',
				'file_path',
				'expanded',
				'candidates',
				'resolved',
				'chunk_size',
				'overlap_amount',
				'url',
				'web_paths',
				'max_depth',
				'timeout',
				'ignore',
				'with_progress',
				'recursive',
				'prevent_outside',
				'verify_exists',
				'resolve_paths',
				'load_documents',
				'split_documents',
				'validate_chunking',
				'load',
				'load_pages',
				'load_recursive',
				'split',
		]
	
	def load( self, urls: str | List[ str ], depth: int = 2, timeout: int = 10,
			ignore: bool = True, progress: bool = True,
			prevent_outside: bool = True ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Load one or more webpages using either WebBaseLoader or RecursiveUrlLoader.

			Parameters:
			-----------
			urls (str | List[str]): One or more URLs to load.
			depth (int): Maximum recursive crawl depth.
			timeout (int): Request timeout in seconds.
			ignore (bool): Continue loading on fetch failure.
			progress (bool): Show progress while loading.
			prevent_outside (bool): Restrict recursive traversal to the starting domain.

			Returns:
			--------
			List[Document]: Loaded webpage documents.

		'''
		try:
			throw_if( 'urls', urls )
			throw_if( 'depth', depth )
			throw_if( 'timeout', timeout )
			
			if self.recursive:
				return self.load_recursive(
					urls=urls,
					depth=depth,
					timeout=timeout,
					ignore=ignore,
					prevent_outside=prevent_outside
				)
			
			return self.load_pages(
				urls=urls,
				timeout=timeout,
				ignore=ignore,
				progress=progress
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WebLoader'
			exception.method = (
					'load( self, urls: str | List[ str ], depth: int=2, '
					'timeout: int=10, ignore: bool=True, progress: bool=True, '
					'prevent_outside: bool=True ) -> List[ Document ]'
			)
			raise exception
	
	def load_pages( self, urls: str | List[ str ], timeout: int = 10,
			ignore: bool = True, progress: bool = True ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Load one or more web pages and convert them into Document objects.

			Parameters:
			-----------
			urls (str | List[str]): One or more URL strings to load.
			timeout (int): Maximum request timeout in seconds.
			ignore (bool): Whether fetch failures should be ignored.
			progress (bool): Whether WebBaseLoader should display progress.

			Returns:
			--------
			List[Document]: Parsed Document objects from fetched HTML content.

		'''
		try:
			throw_if( 'urls', urls )
			throw_if( 'timeout', timeout )
			
			self.web_paths = [ urls ] if isinstance( urls, str ) else list( urls )
			
			if not self.web_paths:
				raise ValueError( 'urls must contain at least one URL.' )
			
			self.timeout = timeout
			self.ignore = ignore
			self.with_progress = progress
			self.loader = WebBaseLoader(
				web_paths=self.web_paths,
				show_progress=self.with_progress,
				continue_on_failure=self.ignore,
				requests_kwargs={ 'timeout': self.timeout }
			)
			
			return self.load_documents( self.loader )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WebLoader'
			exception.method = (
					'load_pages( self, urls: str | List[ str ], timeout: int=10, '
					'ignore: bool=True, progress: bool=True ) -> List[ Document ]'
			)
			raise exception
	
	def load_recursive( self, urls: str | List[ str ], depth: int = 2,
			timeout: int = 10, ignore: bool = True,
			prevent_outside: bool = True ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Recursively crawl one starting URL and load discovered pages.

			Parameters:
			-----------
			urls (str | List[str]): Starting URL. If a list is provided, the first URL is used.
			depth (int): Maximum crawl depth.
			timeout (int): Request timeout in seconds.
			ignore (bool): Continue on crawl failures.
			prevent_outside (bool): Restrict traversal to the starting domain.

			Returns:
			--------
			List[Document]: Crawled documents.

		'''
		try:
			throw_if( 'urls', urls )
			throw_if( 'depth', depth )
			throw_if( 'timeout', timeout )
			
			if not isinstance( depth, int ) or depth < 1:
				raise ValueError( 'depth must be an integer greater than zero.' )
			
			self.url = urls[ 0 ] if isinstance( urls, list ) else urls
			
			if not self.url:
				raise ValueError( 'A starting URL is required.' )
			
			self.max_depth = depth
			self.timeout = timeout
			self.ignore = ignore
			self.prevent_outside = prevent_outside
			self.loader = RecursiveUrlLoader(
				url=self.url,
				max_depth=self.max_depth,
				timeout=self.timeout,
				continue_on_failure=self.ignore,
				prevent_outside=self.prevent_outside
			)
			
			return self.load_documents( self.loader )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WebLoader'
			exception.method = (
					'load_recursive( self, urls: str | List[ str ], depth: int=2, '
					'timeout: int=10, ignore: bool=True, prevent_outside: bool=True ) '
					'-> List[ Document ]'
			)
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Split loaded web documents into smaller chunks.

			Parameters:
			-----------
			chunk (int): Maximum number of characters per chunk.
			overlap (int): Number of overlapping characters between chunks.

			Returns:
			--------
			List[Document]: Chunked Document objects.

		'''
		try:
			throw_if( 'documents', self.documents )
			self.validate_chunking( chunk=chunk, overlap=overlap )
			
			self.chunk_size = chunk
			self.overlap_amount = overlap
			return self.split_documents(
				docs=self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WebLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			)
			raise exception

class PdfLoader( Loader ):
	'''

		Purpose:
		--------
		PDF loader with page-aware metadata, configurable loading modes, configurable
		extraction modes, and optional image extraction with OCR parsing.

	'''
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
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.loader = None
		self.mode = 'single'
		self.extraction = 'plain'
		self.include_images = include
		self.image_format = 'markdown-img'
		self.custom_delimiter = None
		self.image_parser = None
		self.chunk_size = size
		self.overlap_amount = overlap
	
	@property
	def mode_options( self ) -> List[ str ]:
		return [ 'single', 'page' ]
	
	@property
	def extraction_options( self ) -> List[ str ]:
		return [ 'plain', 'layout' ]
	
	@property
	def image_format_options( self ) -> List[ str ]:
		return [ 'html-img', 'markdown-img', 'text-img' ]
	
	def normalize_mode( self, mode: str ) -> str:
		'''

			Purpose:
			--------
			Normalize a PDF loading mode to a supported PyPDFLoader mode.

			Parameters:
			-----------
			mode (str): Requested loading mode.

			Returns:
			--------
			str: Normalized loading mode.

		'''
		try:
			throw_if( 'mode', mode )
			
			value = mode.strip( ).lower( )
			
			if value in [ 'pages', 'paged', 'elements' ]:
				return 'page'
			
			return value if value in self.mode_options else 'single'
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'PdfLoader'
			exception.method = 'normalize_mode( self, mode: str ) -> str'
			raise exception
	
	def normalize_extraction( self, extract: str ) -> str:
		'''

			Purpose:
			--------
			Normalize a PDF extraction mode.

			Parameters:
			-----------
			extract (str): Requested extraction mode.

			Returns:
			--------
			str: Normalized extraction mode.

		'''
		try:
			throw_if( 'extract', extract )
			
			value = extract.strip( ).lower( )
			return value if value in self.extraction_options else 'plain'
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'PdfLoader'
			exception.method = 'normalize_extraction( self, extract: str ) -> str'
			raise exception
	
	def normalize_image_format( self, format: str ) -> str:
		'''

			Purpose:
			--------
			Normalize a PDF image extraction output format.

			Parameters:
			-----------
			format (str): Requested image format.

			Returns:
			--------
			str: Normalized image format.

		'''
		try:
			throw_if( 'format', format )
			
			value = format.strip( ).lower( )
			
			if value == 'text':
				return 'text-img'
			
			return value if value in self.image_format_options else 'markdown-img'
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'PdfLoader'
			exception.method = 'normalize_image_format( self, format: str ) -> str'
			raise exception
	
	def load( self, filepath: str, mode: str = 'single', extract: str = 'plain',
			include: bool = False, format: str = 'markdown-img' ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Load a PDF file into LangChain Document objects.

			Parameters:
			-----------
			filepath (str): Path to the PDF file.
			mode (str): Loader mode.
			extract (str): Extraction mode.
			include (bool): Whether to extract images.
			format (str): Image inner format.

			Returns:
			--------
			List[Document]: Parsed PDF documents.

		'''
		try:
			throw_if( 'filepath', filepath )
			throw_if( 'mode', mode )
			throw_if( 'extract', extract )
			throw_if( 'format', format )
			
			self.file_path = self.verify_exists( filepath )
			self.mode = self.normalize_mode( mode )
			self.extraction = self.normalize_extraction( extract )
			self.include_images = include
			self.image_format = self.normalize_image_format( format )
			
			if self.include_images:
				self.image_parser = RapidOCRBlobParser( )
				self.loader = PyPDFLoader(
					file_path=self.file_path,
					mode=self.mode,
					extraction_mode=self.extraction,
					extract_images=self.include_images,
					images_inner_format=self.image_format,
					images_parser=self.image_parser
				)
			else:
				self.loader = PyPDFLoader(
					file_path=self.file_path,
					mode=self.mode,
					extraction_mode=self.extraction
				)
			
			return self.load_documents( self.loader )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'PdfLoader'
			exception.method = (
					'load( self, filepath: str, mode: str="single", extract: str="plain", '
					'include: bool=False, format: str="markdown-img" ) -> List[ Document ]'
			)
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Split loaded PDF documents into manageable text chunks.

			Parameters:
			-----------
			chunk (int): Maximum characters per chunk.
			overlap (int): Overlapping characters between chunks.

			Returns:
			--------
			List[Document]: Chunked list of PDF documents.

		'''
		try:
			throw_if( 'documents', self.documents )
			self.validate_chunking( chunk=chunk, overlap=overlap )
			
			self.chunk_size = chunk
			self.overlap_amount = overlap
			return self.split_documents(
				docs=self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'PdfLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			)
			raise exception

class ExcelLoader( Loader ):
	'''

		Purpose:
		--------
		Provides LangChain's UnstructuredExcelLoader functionality to parse Excel
		spreadsheets into Document objects.

	'''
	loader: Optional[ UnstructuredExcelLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	mode: Optional[ str ]
	has_headers: Optional[ bool ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.loader = None
		self.mode = 'single'
		self.has_headers = True
	
	@property
	def mode_options( self ) -> List[ str ]:
		return [ 'single', 'elements' ]
	
	def normalize_mode( self, mode: str ) -> str:
		'''

			Purpose:
			--------
			Normalize an Excel loading mode.

			Parameters:
			-----------
			mode (str): Requested loading mode.

			Returns:
			--------
			str: Normalized loading mode.

		'''
		try:
			throw_if( 'mode', mode )
			
			value = mode.strip( ).lower( )
			
			if value in [ 'page', 'paged' ]:
				return 'elements'
			
			return value if value in self.mode_options else 'single'
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'ExcelLoader'
			exception.method = 'normalize_mode( self, mode: str ) -> str'
			raise exception
	
	def load( self, path: str, mode: str = 'single',
			has_headers: bool = True ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Load and convert Excel data into LangChain Document objects.

			Parameters:
			-----------
			path (str): File path to the Excel spreadsheet.
			mode (str): Extraction mode.
			has_headers (bool): Preserved for compatibility.

			Returns:
			--------
			List[Document]: Parsed Document objects from Excel content.

		'''
		try:
			throw_if( 'path', path )
			throw_if( 'mode', mode )
			
			self.file_path = self.verify_exists( path )
			self.mode = self.normalize_mode( mode )
			self.has_headers = has_headers
			self.loader = UnstructuredExcelLoader( file_path=self.file_path, mode=self.mode )
			return self.load_documents( self.loader )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'ExcelLoader'
			exception.method = (
					'load( self, path: str, mode: str="single", has_headers: bool=True ) '
					'-> List[ Document ]'
			)
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Split loaded Excel documents into manageable chunks.

			Parameters:
			-----------
			chunk (int): Maximum characters per chunk.
			overlap (int): Characters overlapping between chunks.

			Returns:
			--------
			List[Document]: Chunked list of Document objects.

		'''
		try:
			throw_if( 'documents', self.documents )
			self.validate_chunking( chunk=chunk, overlap=overlap )
			
			self.chunk_size = chunk
			self.overlap_amount = overlap
			return self.split_documents(
				docs=self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'ExcelLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			)
			raise exception

class WordLoader( Loader ):
	'''

		Purpose:
		--------
		Load Microsoft Word .docx files using LangChain's Docx2txtLoader.

	'''
	loader: Optional[ Docx2txtLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.documents = [ ]
		self.file_path = None
		self.loader = None
	
	def load( self, path: str ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Load a Word document into LangChain Document objects.

			Parameters:
			-----------
			path (str): File path to a .docx document.

			Returns:
			--------
			List[Document]: Parsed Word document objects.

		'''
		try:
			throw_if( 'path', path )
			
			self.file_path = self.verify_exists( path )
			self.loader = Docx2txtLoader( file_path=self.file_path )
			return self.load_documents( self.loader )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WordLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Split loaded Word documents into manageable chunks.

			Parameters:
			-----------
			chunk (int): Maximum characters per chunk.
			overlap (int): Characters overlapping between chunks.

			Returns:
			--------
			List[Document]: Chunked list of Document objects.

		'''
		try:
			throw_if( 'documents', self.documents )
			self.validate_chunking( chunk=chunk, overlap=overlap )
			
			self.chunk_size = chunk
			self.overlap_amount = overlap
			return self.split_documents(
				docs=self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'WordLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			)
			raise exception

class MarkdownLoader( Loader ):
	'''

		Purpose:
		--------
		Load Markdown files using LangChain's UnstructuredMarkdownLoader.

	'''
	loader: Optional[ UnstructuredMarkdownLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	mode: Optional[ str ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.loader = None
		self.mode = 'single'
	
	@property
	def mode_options( self ) -> List[ str ]:
		return [ 'single', 'elements' ]
	
	def load( self, path: str, mode: str = 'single' ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Load a Markdown document into LangChain Document objects.

			Parameters:
			-----------
			path (str): File path to a Markdown document.
			mode (str): Unstructured loader mode.

			Returns:
			--------
			List[Document]: Parsed Markdown document objects.

		'''
		try:
			throw_if( 'path', path )
			throw_if( 'mode', mode )
			
			self.file_path = self.verify_exists( path )
			self.mode = mode if mode in self.mode_options else 'single'
			self.loader = UnstructuredMarkdownLoader( file_path=self.file_path, mode=self.mode )
			return self.load_documents( self.loader )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'MarkdownLoader'
			exception.method = (
					'load( self, path: str, mode: str="single" ) -> List[ Document ]'
			)
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Split loaded Markdown documents into manageable chunks.

			Parameters:
			-----------
			chunk (int): Maximum characters per chunk.
			overlap (int): Characters overlapping between chunks.

			Returns:
			--------
			List[Document]: Chunked list of Document objects.

		'''
		try:
			throw_if( 'documents', self.documents )
			self.validate_chunking( chunk=chunk, overlap=overlap )
			
			self.chunk_size = chunk
			self.overlap_amount = overlap
			return self.split_documents(
				docs=self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'MarkdownLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			)
			raise exception

class HtmlLoader( Loader ):
	'''

		Purpose:
		--------
		Load HTML files using LangChain's UnstructuredHTMLLoader.

	'''
	loader: Optional[ UnstructuredHTMLLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	mode: Optional[ str ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.loader = None
		self.mode = 'single'
	
	@property
	def mode_options( self ) -> List[ str ]:
		return [ 'single', 'elements' ]
	
	def __dir__( self ) -> List[ str ]:
		'''

			Purpose:
			--------
			Return available members in a stable order.

			Parameters:
			-----------
			None

			Returns:
			--------
			List[str]: Available members.

		'''
		return [
				'loader',
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
				'load_documents',
				'split_documents',
				'validate_chunking',
				'load',
				'split',
		]
	
	def load( self, path: str, mode: str = 'single' ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Load an HTML file and convert its contents into LangChain Document objects.

			Parameters:
			-----------
			path (str): Path to the HTML file.
			mode (str): Unstructured loader mode.

			Returns:
			--------
			List[Document]: List of Document objects parsed from HTML content.

		'''
		try:
			throw_if( 'path', path )
			throw_if( 'mode', mode )
			
			self.file_path = self.verify_exists( path )
			self.mode = mode if mode in self.mode_options else 'single'
			self.loader = UnstructuredHTMLLoader( file_path=self.file_path, mode=self.mode )
			return self.load_documents( self.loader )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'HtmlLoader'
			exception.method = (
					'load( self, path: str, mode: str="single" ) -> List[ Document ]'
			)
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Split loaded HTML documents into manageable text chunks.

			Parameters:
			-----------
			chunk (int): Maximum characters per chunk.
			overlap (int): Overlapping characters between chunks.

			Returns:
			--------
			List[Document]: Chunked list of LangChain Document objects.

		'''
		try:
			throw_if( 'documents', self.documents )
			self.validate_chunking( chunk=chunk, overlap=overlap )
			
			self.chunk_size = chunk
			self.overlap_amount = overlap
			return self.split_documents(
				docs=self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'HtmlLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			)
			raise exception

class JsonLoader( Loader ):
	'''

		Purpose:
		--------
		Wrap LangChain's JSONLoader to parse JSON and JSONL files into LangChain
		Document objects.

	'''
	loader: Optional[ JSONLoader ]
	file_path: Optional[ str ]
	jq_schema: Optional[ str ]
	content_key: Optional[ str ]
	text_content: Optional[ bool ]
	json_lines: Optional[ bool ]
	documents: Optional[ List[ Document ] ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = [ ]
		self.loader = None
		self.jq_schema = '.'
		self.content_key = None
		self.text_content = True
		self.json_lines = False
	
	def __dir__( self ) -> List[ str ]:
		'''

			Purpose:
			--------
			Return available members in a stable order.

			Parameters:
			-----------
			None

			Returns:
			--------
			List[str]: Available members.

		'''
		return [
				'loader',
				'documents',
				'file_path',
				'jq_schema',
				'content_key',
				'text_content',
				'json_lines',
				'chunk_size',
				'overlap_amount',
				'verify_exists',
				'resolve_paths',
				'load_documents',
				'split_documents',
				'validate_chunking',
				'load',
				'split',
		]
	
	def load( self, path: str, jq_schema: str = '.', content_key: Optional[ str ] = None,
			text_content: bool = True, json_lines: bool = False ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Load JSON or JSON Lines data into LangChain Document objects.

			Parameters:
			-----------
			path (str): File path to the JSON or JSONL file.
			jq_schema (str): jq expression used to select JSON content.
			content_key (Optional[str]): Optional key containing text content.
			text_content (bool): Whether selected content is already text.
			json_lines (bool): Whether the input file is JSON Lines.

			Returns:
			--------
			List[Document]: Parsed JSON document objects.

		'''
		try:
			throw_if( 'path', path )
			throw_if( 'jq_schema', jq_schema )
			
			self.file_path = self.verify_exists( path )
			self.jq_schema = jq_schema
			self.content_key = content_key
			self.text_content = text_content
			self.json_lines = json_lines
			self.loader = JSONLoader(
				file_path=self.file_path,
				jq_schema=self.jq_schema,
				content_key=self.content_key,
				text_content=self.text_content,
				json_lines=self.json_lines
			)
			
			return self.load_documents( self.loader )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'JsonLoader'
			exception.method = (
					'load( self, path: str, jq_schema: str=".", '
					'content_key: Optional[ str ]=None, text_content: bool=True, '
					'json_lines: bool=False ) -> List[ Document ]'
			)
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ]:
		'''

			Purpose:
			--------
			Split loaded JSON documents into manageable chunks.

			Parameters:
			-----------
			chunk (int): Maximum characters per chunk.
			overlap (int): Characters overlapping between chunks.

			Returns:
			--------
			List[Document]: Chunked list of Document objects.

		'''
		try:
			throw_if( 'documents', self.documents )
			self.validate_chunking( chunk=chunk, overlap=overlap )
			
			self.chunk_size = chunk
			self.overlap_amount = overlap
			return self.split_documents(
				docs=self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'JsonLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			)
			raise exception

class ArXivLoader( Loader ):
	'''

		Purpose:
		--------
		alaods documents from an open-access archive for 2 million scholarly articles in the
		fields of physics,  mathematics, computer science, quantitative biology,
		quantitative finance, statistics,  electrical engineering and systems science, and economics.

		Attributes:
		-----------
		documents - List[ Document ]
		file_path -  str
		pattern -  str
		expanded - List[ str ]
		candidates - List[ str ]
		resolved - List[ str ]
		splitter - RecursiveCharacterTextSplitter
		chunk_size - int
		overlap_amount - int

		Methods:
		--------
		verify_exists( self, path: str ) -> str;
		resolve_paths( self, pattern: str ) -> List[ str ];
		split_documents( self, docs: List[ Document ]  ) -> List[ Document ];
		load( path: str, mode: str ) -> List[ Document ];
		split( ) -> List[ Document ];

	'''
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
		self.max_documents = None
		self.max_characters = None
		self.include_metadata = False
	
	def __dir__( self ):
		'''

			Returns:
			--------
			A list of all available members.


		'''
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
	
	def load( self, query: str, max_chars: int = 1000 ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load an video file and convert its contents into LangChain Document objects.

			Parameters:
			-----------
			path (str): Path to the HTML (.html or .htm) file.

			Returns:
			--------
			List[Document]: List of Document objects parsed from HTML content.

		'''
		try:
			throw_if( 'query', query )
			self.query = query
			self.max_characters = max_chars
			self.loader = ArxivLoader( query=self.query, doc_content_chars_max=self.max_characters )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'ArxivLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Split loaded Youtube Transcript documents into manageable text chunks.

			Parameters:
			-----------
			chunk_size (int): Max characters per chunk.
			chunk_overlap (int): Overlapping characters between chunks.

			Returns:
			--------
			List[Document]: Chunked list of LangChain Document objects.

		'''
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
			exception.module = 'chonky'
			exception.cause = 'ArxivLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			raise exception

class WikiLoader( Loader ):
	'''

		Purpose:
		--------
		Provides WikipediaLoader functionality
		to fetch Wikipedia articles into Document objects.

	'''
	loader: Optional[ WikipediaLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	query: Optional[ str ]
	max_documents: Optional[ int ]
	max_characters: Optional[ int ]
	include_all: Optional[ bool ]
	
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
		self.include_all = False
	
	def __dir__( self ):
		'''

			Returns:
			--------
			A list of all available members.

		'''
		return [
				'loader',
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
				'split',
		]
	
	def load( self, query: str, max_docs: int = 25, max_chars: int = 4000,
			include_all: bool = False ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load Wikipedia search results into LangChain Document objects.

			Parameters:
			-----------
			query (str): Wikipedia search query.
			max_docs (int): Maximum number of documents to fetch.
			max_chars (int): Maximum number of characters per document.
			include_all (bool): Whether to include all available metadata.

			Returns:
			--------
			List[Document] | None: Wikipedia documents.

		'''
		try:
			throw_if( 'query', query )
			
			self.query = query
			self.max_documents = max_docs
			self.max_characters = max_chars
			self.include_all = include_all
			
			self.loader = WikipediaLoader(
				query=self.query,
				load_max_docs=self.max_documents,
				load_all_available_meta=self.include_all,
				doc_content_chars_max=self.max_characters
			)
			
			self.documents = self.loader.load( )
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'WikiLoader'
			exception.method = (
					'load( self, query: str, max_docs: int=25, max_chars: int=4000, '
					'include_all: bool=False ) -> List[ Document ] | None'
			)
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Split loaded Wikipedia documents into manageable text chunks.

			Parameters:
			-----------
			chunk (int): Maximum characters per chunk.
			overlap (int): Overlapping characters between chunks.

			Returns:
			--------
			List[Document] | None: Chunked Wikipedia documents.

		'''
		try:
			if self.documents is None:
				raise ValueError( 'No documents loaded!' )
			
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
			exception.module = 'chonky'
			exception.cause = 'WikiLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> '
					'List[ Document ] | None'
			)
			raise exception

class GithubLoader( Loader ):
	'''

		Purpose:
		--------
		Provides GitHub file loading functionality through LangChain's
		GithubFileLoader.

	'''
	loader: Optional[ GithubFileLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	repo: Optional[ str ]
	branch: Optional[ str ]
	access_token: Optional[ str ]
	github_url: Optional[ str ]
	file_filter: Optional[ object ]
	pattern: Optional[ str ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.github_url = None
		self.repo = None
		self.branch = None
		self.access_token = None
		self.file_filter = None
		self.pattern = None
	
	def __dir__( self ):
		'''

			Returns:
			--------
			A list of all available members.

		'''
		return [
				'loader',
				'documents',
				'splitter',
				'pattern',
				'file_path',
				'expanded',
				'candidates',
				'resolved',
				'chunk_size',
				'overlap_amount',
				'repo',
				'branch',
				'access_token',
				'github_url',
				'file_filter',
				'verify_exists',
				'resolve_paths',
				'split_documents',
				'load',
				'split',
		]
	
	def load( self, url: str, repo: str, branch: str, filetype: str = '.md',
			access_token: Optional[ str ] = None ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load filtered contents of a GitHub repository branch into LangChain
			Document objects.

			Parameters:
			-----------
			url (str): GitHub API URL.
			repo (str): Repository in owner/name format.
			branch (str): Branch name.
			filetype (str): File suffix filter such as '.py', '.md', or '.txt'.
			access_token (Optional[str]): GitHub personal access token.

			Returns:
			--------
			List[Document] | None: Loaded GitHub documents.

		'''
		try:
			throw_if( 'url', url )
			throw_if( 'repo', repo )
			throw_if( 'branch', branch )
			
			self.github_url = url
			self.repo = repo
			self.branch = branch
			self.access_token = access_token.strip( ) if isinstance( access_token,
				str ) and access_token.strip( ) else None
			self.pattern = filetype.strip( ) if isinstance( filetype,
				str ) and filetype.strip( ) else '.md'
			self.file_filter = lambda file_path: file_path.endswith( self.pattern )
			
			kwargs = {
					'repo': self.repo,
					'branch': self.branch,
					'github_api_url': self.github_url,
					'file_filter': self.file_filter,
			}
			
			if self.access_token:
				kwargs[ 'access_token' ] = self.access_token
			
			self.loader = GithubFileLoader( **kwargs )
			self.documents = self.loader.load( )
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'GithubLoader'
			exception.method = (
					'load( self, url: str, repo: str, branch: str, '
					'filetype: str=".md", access_token: Optional[ str ]=None ) '
					'-> List[ Document ] | None'
			)
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Split loaded GitHub documents into manageable text chunks.

			Parameters:
			-----------
			chunk (int): Max characters per chunk.
			overlap (int): Overlapping characters between chunks.

			Returns:
			--------
			List[Document] | None: Chunked GitHub documents.

		'''
		try:
			if self.documents is None:
				raise ValueError( 'No documents loaded!' )
			
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
			exception.module = 'chonky'
			exception.cause = 'GithubLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> '
					'List[ Document ] | None'
			)
			raise exception

class PowerPointLoader( Loader ):
	'''

		Purpose:
		--------
		Provides PowerPoint loading functionality
		to parse ppt files into Document objects.

		Attributes:
		-----------
		documents - List[ Document ]
		file_path - str
		pattern - str
		expanded - List[ str ]
		candidates - List[ str ]
		resolved - List[ str ]
		splitter - RecursiveCharacterTextSplitter
		chunk_size - int
		overlap_amount - int
		mode - str

		Methods:
		--------
		verify_exists( self, path: str ) -> str;
		resolve_paths( self, pattern: str ) -> List[ str ];
		split_documents( self, docs: List[ Document ] ) -> List[ Document ];
		load( path: str, mode: str ) -> List[ Document ];
		load_multiple( path: str ) -> List[ Document ];
		split( ) -> List[ Document ];

	'''
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
	
	def __dir__( self ):
		'''

			Returns:
			--------
			A list of all available members.

		'''
		return [
				'loader',
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
				'load_multiple',
				'split',
		]
	
	def _normalize_mode( self, mode: str ) -> str:
		'''

			Purpose:
			--------
			Normalize legacy or UI-provided PowerPoint modes to supported loader modes.

			Parameters:
			-----------
			mode (str): Incoming mode value.

			Returns:
			--------
			str: Supported PowerPoint loader mode.

		'''
		value = mode.strip( ).lower( ) if isinstance( mode, str ) else 'single'
		
		if value == 'multiple':
			return 'elements'
		
		if value not in [ 'single', 'elements' ]:
			return 'single'
		
		return value
	
	def load( self, path: str, mode: str = 'single' ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load PowerPoint slides and convert their content into LangChain Document objects.

			Parameters:
			-----------
			path (str): Path to the PowerPoint file.
			mode (str): Loading mode. Supported values are 'single' and 'elements'.
			            Legacy value 'multiple' is normalized to 'elements'.

			Returns:
			--------
			List[Document] | None: List of Document objects parsed from the PowerPoint file.

		'''
		try:
			throw_if( 'path', path )
			
			self.file_path = self.verify_exists( path )
			self.mode = self._normalize_mode( mode )
			self.loader = UnstructuredPowerPointLoader(
				file_path=self.file_path,
				mode=self.mode
			)
			self.documents = self.loader.load( )
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'PowerPointLoader'
			exception.method = (
					'load( self, path: str, mode: str="single" ) -> '
					'List[ Document ] | None'
			)
			raise exception
	
	def load_multiple( self, path: str ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Compatibility alias for the legacy non-single PowerPoint mode.

			Parameters:
			-----------
			path (str): Path to the PowerPoint file.

			Returns:
			--------
			List[Document] | None: List of Document objects parsed from the PowerPoint file.

		'''
		try:
			return self.load( path, mode='elements' )
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'PowerPointLoader'
			exception.method = 'load_multiple( self, path: str ) -> List[ Document ] | None'
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Split loaded PowerPoint documents into manageable text chunks.

			Parameters:
			-----------
			chunk (int): Max characters per chunk.
			overlap (int): Overlapping characters between chunks.

			Returns:
			--------
			List[Document] | None: Chunked list of LangChain Document objects.

		'''
		try:
			if self.documents is None:
				raise ValueError( 'No documents loaded!' )
			
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
			exception.module = 'chonky'
			exception.cause = 'PowerPointLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> '
					'List[ Document ] | None'
			)
			raise exception

class OutlookLoader( Loader ):
	'''

		Purpose:
		--------
		Provides the Arxiv loading functionality
		to parse video research papers into Document objects.

		Attributes:
		-----------
		documents - List[ Document ]
		file_path -  str
		pattern -  str
		expanded - List[ str ]
		candidates - List[ str ]
		resolved - List[ str ]
		splitter - RecursiveCharacterTextSplitter
		chunk_size - int
		overlap_amount - int

		Methods:
		--------
		verify_exists( self, path: str ) -> str;
		resolve_paths( self, pattern: str ) -> List[ str ];
		split_documents( self, docs: List[ Document ]  ) -> List[ Document ];
		load( path: str, mode: str ) -> List[ Document ];
		split( ) -> List[ Document ];

	'''
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
	
	def __dir__( self ):
		'''

			Returns:
			--------
			A list of all available members.


		'''
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
		'''

			Purpose:
			--------
			Load Outlook Message from a path converting contents into LangChain Document objects.

			Parameters:
			-----------
			path (str): Path to the HTML (.html or .htm) file.

			Returns:
			--------
			List[Document]: List of Document objects parsed from HTML content.

		'''
		try:
			throw_if( 'path', path )
			self.file_path = self.verify_exists( path )
			self.loader = OutlookMessageLoader( file_path=self.file_path )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'OutlookLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Split loaded Wikipedia search documents into manageable text chunks.

			Parameters:
			-----------
			chunk_size (int): Max characters per chunk.
			chunk_overlap (int): Overlapping characters between chunks.

			Returns:
			--------
			List[Document]: Chunked list of LangChain Document objects.

		'''
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'OutlookLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			raise exception

class WebCrawler( Loader ):
	'''

		Purpose:
		--------
		Load one or more webpages into LangChain Document objects, with optional
		recursive crawling support.

	'''
	loader: Optional[ RecursiveUrlLoader | WebBaseLoader ]
	url: Optional[ str ]
	web_paths: Optional[ str | List[ str ] ]
	documents: Optional[ List[ Document ] ]
	file_path: Optional[ str ]
	max_depth: Optional[ int ]
	timeout: Optional[ int ]
	ignore: Optional[ bool ]
	with_progress: Optional[ bool ]
	recursive: Optional[ bool ]
	prevent_outside: Optional[ bool ]
	
	def __init__( self, url: str, recursive: bool = False, max_depth: int = 2,
			prevent_outside: bool = True, timeout: int = 10,
			ignore: bool = True, progress: bool = True ) -> None:
		'''

			Purpose:
			--------
			Initialize a WebLoader instance for either single-page loading
			or recursive crawling.

			Parameters:
			-----------
			recursive (bool): Whether to use RecursiveUrlLoader.
			max_depth (int): Maximum crawl depth for recursive loading.
			prevent_outside (bool): Prevent traversal outside the starting domain.
			timeout (int): Request timeout in seconds.
			ignore (bool): Continue on failure when loading pages.
			progress (bool): Show progress during page loading.

			Returns:
			--------
			None

		'''
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.chunk_size = None
		self.overlap_amount = None
		self.url = url
		self.web_paths = None
		self.max_depth = max_depth
		self.timeout = timeout
		self.ignore = ignore
		self.with_progress = progress
		self.recursive = recursive
		self.prevent_outside = prevent_outside
		self.loader = RecursiveUrlLoader( url=self.url, max_depth=self.max_depth,
			timeout=self.timeout, continue_on_failure=self.ignore,
			prevent_outside=self.prevent_outside )
	
	def __dir__( self ):
		'''

			Returns:
			--------
			A list of all available members.

		'''
		return [
				'loader',
				'documents',
				'splitter',
				'pattern',
				'file_path',
				'expanded',
				'candidates',
				'resolved',
				'chunk_size',
				'overlap_amount',
				'url',
				'web_paths',
				'max_depth',
				'timeout',
				'ignore',
				'with_progress',
				'recursive',
				'prevent_outside',
				'verify_exists',
				'resolve_paths',
				'split_documents',
				'load',
				'load_pages',
				'split',
		]
	
	def load( self, urls: str | List[ str ], depth: int = 2, timeout: int = 10,
			ignore: bool = True, progress: bool = True,
			prevent_outside: bool = True ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load one or more webpages, using either WebBaseLoader or
			RecursiveUrlLoader depending on the instance configuration.

			Parameters:
			-----------
			urls (str | List[str]): One or more URLs to load.
			depth (int): Maximum recursive crawl depth.
			timeout (int): Request timeout in seconds.
			ignore (bool): Continue loading on fetch failure.
			progress (bool): Show progress while loading.
			prevent_outside (bool): Restrict recursive traversal to the starting domain.

			Returns:
			--------
			List[Document] | None: Loaded webpage documents.

		'''
		try:
			if self.recursive:
				return self.load_recursive(
					urls=urls,
					depth=depth,
					timeout=timeout,
					ignore=ignore,
					prevent_outside=prevent_outside
				)
			
			return self.load_pages(
				urls=urls,
				timeout=timeout,
				ignore=ignore,
				progress=progress
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'WebCrawler'
			exception.method = (
					'load( self, urls: str | List[ str ], depth: int=2, '
					'timeout: int=10, ignore: bool=True, progress: bool=True, '
					'prevent_outside: bool=True ) -> List[ Document ] | None'
			)
			raise exception
	
	def load_pages( self, urls: str | List[ str ], timeout: int = 10,
			ignore: bool = True, progress: bool = True ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load one or more web pages and convert them into Document objects.

			Parameters:
			-----------
			urls (str | List[str]): One or more URL strings to load.
			timeout (int): Maximum request timeout in seconds.
			ignore (bool): Whether fetch failures should be ignored.
			progress (bool): Whether WebBaseLoader should display progress.

			Returns:
			--------
			List[Document] | None: Parsed Document objects from fetched HTML content.

		'''
		try:
			throw_if( 'urls', urls )
			
			self.web_paths = [ urls ] if isinstance( urls, str ) else list( urls )
			self.timeout = timeout
			self.ignore = ignore
			self.with_progress = progress
			
			self.loader = WebBaseLoader(
				web_paths=self.web_paths,
				show_progress=self.with_progress,
				continue_on_failure=self.ignore,
				requests_kwargs={ 'timeout': self.timeout }
			)
			
			self.documents = self.loader.load( )
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'WebCrawler'
			exception.method = (
					'load_pages( self, urls: str | List[ str ], timeout: int=10, '
					'ignore: bool=True, progress: bool=True ) -> '
					'List[ Document ] | None'
			)
			raise exception
	
	def load_recursive( self, urls: str | List[ str ], depth: int = 2,
			timeout: int = 10, ignore: bool = True,
			prevent_outside: bool = True ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Recursively crawl one starting URL and load discovered pages.

			Parameters:
			-----------
			urls (str | List[str]): Starting URL. If a list is provided, the first URL is used.
			depth (int): Maximum crawl depth.
			timeout (int): Request timeout in seconds.
			ignore (bool): Continue on crawl failures.
			prevent_outside (bool): Restrict traversal to the starting domain.

			Returns:
			--------
			List[Document] | None: Crawled documents.

		'''
		try:
			throw_if( 'urls', urls )
			
			self.url = urls[ 0 ] if isinstance( urls, list ) else urls
			self.max_depth = depth
			self.timeout = timeout
			self.ignore = ignore
			self.prevent_outside = prevent_outside
			
			self.loader = RecursiveUrlLoader(
				url=self.url,
				max_depth=self.max_depth,
				timeout=self.timeout,
				continue_on_failure=self.ignore,
				prevent_outside=self.prevent_outside
			)
			
			self.documents = self.loader.load( )
			return self.documents
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'WebCrawler'
			exception.method = (
					'load_recursive( self, urls: str | List[ str ], depth: int=2, '
					'timeout: int=10, ignore: bool=True, prevent_outside: bool=True ) '
					'-> List[ Document ] | None'
			)
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Split loaded web documents into smaller chunks for downstream use.

			Parameters:
			-----------
			chunk (int): Maximum number of characters per chunk.
			overlap (int): Number of overlapping characters between chunks.

			Returns:
			--------
			List[Document] | None: Chunked Document objects.

		'''
		try:
			if self.documents is None:
				raise ValueError( 'No documents loaded!' )
			
			self.chunk_size = chunk
			self.overlap_amount = overlap
			return self.split_documents(
				docs=self.documents,
				chunk=self.chunk_size,
				overlap=self.overlap_amount
			)
		
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'WebCrawler'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> '
					'List[ Document ] | None'
			)
			raise exception

class SpfxLoader( Loader ):
	'''

		Purpose:
		--------
		Provides the Sharepoint loading functionality
		to parse video research papers into Document objects.

		Attributes:
		-----------
		documents - List[ Document ]
		file_path -  str
		pattern -  str
		expanded - List[ str ]
		candidates - List[ str ]
		resolved - List[ str ]
		splitter - RecursiveCharacterTextSplitter
		chunk_size - int
		overlap_amount - int
		loader - SharePointLoader
		library_id - str
		subsite_id - str
		folder_id - str
		object_ids - List[ str ]
		query - str
		with_token - bool
		is_recursive - bool

		Methods:
		--------
		verify_exists( self, path: str ) -> str;
		resolve_paths( self, pattern: str ) -> List[ str ];
		split_documents( self, docs: List[ Document ]  ) -> List[ Document ];
		load( path: str, mode: str ) -> List[ Document ];
		split( ) -> List[ Document ];

	'''
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
	
	def __dir__( self ):
		'''

			Returns:
			--------
			A list of all available members.


		'''
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
		'''

			Purpose:
			--------
			Load Sharepoint files and convert their contents into LangChain Document objects.

			Parameters:
			-----------
			path (str): Path to the HTML (.html or .htm) file.

			Returns:
			--------
			List[Document]: List of Document objects parsed from HTML content.

		'''
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
			exception.module = 'chonky'
			exception.cause = 'SpfxLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			raise exception
	
	def load_folder( self, library_id: str, folder_id: str ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load Sharepoint files and convert their contents into LangChain Document objects.

			Parameters:
			-----------
			path (str): Path to the HTML (.html or .htm) file.

			Returns:
			--------
			List[Document]: List of Document objects parsed from HTML content.

		'''
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
			exception.module = 'chonky'
			exception.cause = 'SpfxLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Split loaded Sharepoint file documents into manageable text chunks.

			Parameters:
			-----------
			chunk_size (int): Max characters per chunk.
			chunk_overlap (int): Overlapping characters between chunks.

			Returns:
			--------
			List[Document]: Chunked list of LangChain Document objects.

		'''
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'SpfxLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			raise exception

class OneDriveDocLoader( Loader ):
	'''

		Purpose:
		--------
		Provides OneDrvie loading functionality
		to parse contents into Document objects.

		Attributes:
		-----------
		documents - List[ Document ]
		file_path -  str
		pattern -  str
		expanded - List[ str ]
		candidates - List[ str ]
		resolved - List[ str ]
		splitter - RecursiveCharacterTextSplitter
		chunk_size - int
		overlap_amount - int

		Methods:
		--------
		verify_exists( self, path: str ) -> str;
		resolve_paths( self, pattern: str ) -> List[ str ];
		split_documents( self, docs: List[ Document ]  ) -> List[ Document ];
		load( path: str, mode: str ) -> List[ Document ];
		split( ) -> List[ Document ];

	'''
	loader: Optional[ OneDriveLoader ]
	file_path: Optional[ str ]
	documents: Optional[ List[ Document ] ]
	client_id: Optional[ str ]
	drive_id: Optional[ str ]
	client_secret: Optional[ str ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.file_path = None
		self.documents = None
		self.query = None
		self.chunk_size = None
		self.overlap_amount = None
		self.loader = None
		self.drive_id = None
		self.client_id = None
		self.client_secret = None
	
	def __dir__( self ):
		'''

			Returns:
			--------
			A list of all available members.


		'''
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
		         'drive_id',
		         'client_id',
		         'client_secret',
		         'verify_exists',
		         'resolve_paths',
		         'split_documents',
		         'load',
		         'load_folder',
		         'split', ]
	
	@property
	def file_options( self ):
		'''

			Returns:
			-------
			List[ str ] of file options

		'''
		return [ 'pdf', 'doc', 'docx', 'txt' ]
	
	def load( self, id: str ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load an onedrive file and convert its contents into LangChain Document objects.

			Parameters:
			-----------
			path (str): Path to the HTML (.html or .htm) file.

			Returns:
			--------
			List[Document]: List of Document objects parsed from HTML content.

		'''
		try:
			throw_if( 'id', id )
			self.drive_id = id
			self.loader = OneDriveLoader( drive_id=self.drive_id )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'WikiLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			raise exception
	
	def load_folder( self, id: str, path: str ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load an onedrive file and convert its contents into LangChain Document objects.

			Parameters:
			-----------
			path (str): Path to the HTML (.html or .htm) file.

			Returns:
			--------
			List[Document]: List of Document objects parsed from HTML content.

		'''
		try:
			throw_if( 'id', id )
			self.drive_id = id
			self.file_path = path
			self.loader = OneDriveLoader( drive_id=self.drive_id, folder_path=self.file_path )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'WikiLoader'
			exception.method = 'load( self, path: str ) -> List[ Document ]'
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Split loaded Wikipedia search documents into manageable text chunks.

			Parameters:
			-----------
			chunk_size (int): Max characters per chunk.
			chunk_overlap (int): Overlapping characters between chunks.

			Returns:
			--------
			List[Document]: Chunked list of LangChain Document objects.

		'''
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'WikiLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			raise exception

class GoogleLoader( Loader ):
	'''

		Purpose:
		--------
		Provides Google Drive loading functionality
		to parse contents into Document objects.

		Attributes:
		-----------
		documents - List[ Document ]
		file_path -  str
		pattern -  str
		expanded - List[ str ]
		candidates - List[ str ]
		resolved - List[ str ]
		splitter - RecursiveCharacterTextSplitter
		chunk_size - int
		overlap_amount - int

		Methods:
		--------
		verify_exists( self, path: str ) -> str;
		resolve_paths( self, pattern: str ) -> List[ str ];
		split_documents( self, docs: List[ Document ]  ) -> List[ Document ];
		load( path: str, mode: str ) -> List[ Document ];
		split( ) -> List[ Document ];

	'''
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
	
	def __dir__( self ):
		'''

			Returns:
			--------
			A list of all available members.


		'''
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
	def file_options( self ):
		'''

			Returns:
			-------
			List[ str ] of file options

		'''
		return [ 'document',
		         'sheet',
		         'pdf' ]
	
	def load_file( self, file_id: str, recursive: bool = False ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load an google drive file by id and convert its contents into LangChain Document objects.

			Parameters:
			-----------
			path (str): Path to the HTML (.html or .htm) file.

			Returns:
			--------
			List[Document]: List of Document objects parsed from HTML content.

		'''
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
			exception.module = 'chonky'
			exception.cause = 'GoogleDriveLoader'
			exception.method = 'load_File( self, file_id: str ) -> List[ Document ]'
			raise exception
	
	def load_folder( self, folder_id: str, recursive: bool = False ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load an google drive file and convert its contents into LangChain Document objects.

			Parameters:
			-----------
			path (str): Path to the HTML (.html or .htm) file.

			Returns:
			--------
			List[Document]: List of Document objects parsed from HTML content.

		'''
		try:
			throw_if( 'folder_id', folder_id )
			self.folder_id = folder_id
			self.is_recursive = recursive
			self.loader = GoogleDriveLoader( folder_id=self.folder_id, recursive=self.is_recursive )
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'GoogleDriveLoader'
			exception.method = 'load_folder( self, path: str ) -> List[ Document ]'
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Split loaded google drive documents into manageable text chunks.

			Parameters:
			-----------
			chunk_size (int): Max characters per chunk.
			chunk_overlap (int): Overlapping characters between chunks.

			Returns:
			--------
			List[Document]: Chunked list of LangChain Document objects.

		'''
		try:
			throw_if( 'documents', self.documents )
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'GoogleDriveLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			raise exception

class EmailLoader( Loader ):
	'''


		Purpose:
		--------
		Provides LangChain's UnstructuredEmailLoader functionality
		to parse email documents (*.eml) into documents.

		Attibutes:
		----------
		documents - List[ Document ]
		file_path -  str
		pattern -  str
		expanded - List[ str ]
		candidates - List[ str ]
		resolved - List[ str ]
		splitter - RecursiveCharacterTextSplitter
		chunk_size - int
		overlap_amount - int

		Methods:
		--------
		verify_exists( self, path: str ) -> str,
		resolve_paths( self, pattern: str ) -> List[ str ],
		split_documents( self, docs: List[ Document ]  ) -> List[ Document ]
		load( path: str, mode: str ) -> List[ Document ]
		split( ) -> List[ Document ]


	'''
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
	
	def __dir__( self ):
		'''

			Returns:
			--------
			A list of all available members.


		'''
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
	
	def load( self, path: str, mode: str = 'single', attachments: bool = True ) -> List[ Document ]:
		'''


			Purpose:
			--------
			Load and convert Email data (*.eml) into LangChain Document objects.

			Parameters:
			-----------
			path (str): File path to the Excel spreadsheet.
			mode (str): Extraction mode, either 'elements' or 'paged'.
			include_headers (bool): Whether to include column headers in parsing.

			Returns:
			--------
			List[Document]: List of parsed Document objects from Email content.


		'''
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
			exception.module = 'chonky'
			exception.cause = 'EmailLoader'
			exception.method = ('load( self, path: str, mode: str=elements, '
			                    'include_headers: bool=True ) -> List[ Document ]')
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		'''


			Purpose:
			--------
			Split loaded Email documents into manageable chunks.

			Parameters:
			-----------
			chunk_size (int): Maximum characters per chunk.
			chunk_overlap (int): Characters overlapping between chunks.

			Returns:
			--------
			List[Document]: Chunked and cleaned list of Document objects.


		'''
		try:
			self.chunk_size = chunk
			self.overlap_amount = overlap
			self.documents = self.split_documents( self.documents, chunk=self.chunk_size,
				overlap=self.overlap_amount )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'chonky'
			exception.cause = 'EmailLoader'
			exception.method = 'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ]'
			raise exception

class PubMedSearchLoader( Loader ):
	'''

		Purpose:
		--------
		Provides PubMed loading functionality for biomedical literature search results.

	'''
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
		'''

			Purpose:
			--------
			Load PubMed search results into LangChain Document objects.

			Parameters:
			-----------
			query (str): PubMed search query.
			max_docs (int): Maximum number of records to load.

			Returns:
			--------
			List[Document] | None: Loaded PubMed documents.

		'''
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
			raise exception

class OpenCityLoader( Loader ):
	'''

		Purpose:
		--------
		Provides Open City Data loading functionality backed by Socrata.

	'''
	loader: Optional[ OpenCityDataLoader ]
	documents: Optional[ List[ Document ] ]
	city_id: Optional[ str ]
	dataset_id: Optional[ str ]
	limit: Optional[ int ]
	
	def __init__( self ) -> None:
		super( ).__init__( )
		self.loader = None
		self.documents = None
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
				'chunk_size',
				'overlap_amount',
				'load',
				'split',
				'split_documents',
		]
	
	def load( self, city_id: str, dataset_id: str, limit: int = 100 ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load records from an Open City Data dataset into LangChain Document objects.

			Parameters:
			-----------
			city_id (str): City domain identifier such as 'data.sfgov.org'.
			dataset_id (str): Dataset identifier such as 'vw6y-z8j6'.
			limit (int): Maximum number of records to load.

			Returns:
			--------
			List[Document] | None: Loaded city data records.

		'''
		try:
			throw_if( 'city_id', city_id )
			throw_if( 'dataset_id', dataset_id )
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
					'-> List[ Document ] | None'
			)
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
			exception.cause = 'OpenCityLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) -> List[ Document ] | None'
			)
			raise exception

class JupyterNotebookLoader( Loader ):
	'''

		Purpose:
		--------
		Provides Jupyter Notebook loading functionality for .ipynb files.

	'''
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
		'''

			Purpose:
			--------
			Load a Jupyter notebook into LangChain Document objects.

			Parameters:
			-----------
			path (str): Path to the .ipynb notebook file.
			include_outputs (bool): Include cell outputs when True.
			max_output_length (int): Maximum output characters to include.
			remove_newline (bool): Remove newline characters when True.
			traceback (bool): Include traceback output when True.

			Returns:
			--------
			List[Document] | None: Loaded notebook document(s).

		'''
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
			raise exception

class GoogleCloudFileLoader( Loader ):
	'''

		Purpose:
		--------
		Provides Google Cloud Storage file loading functionality.

	'''
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
		'''

			Purpose:
			--------
			Load a single Google Cloud Storage object into LangChain Document objects.

			Parameters:
			-----------
			project_name (str): Google Cloud project name or ID.
			bucket (str): GCS bucket name.
			blob (str): GCS object name.

			Returns:
			--------
			List[Document] | None: Loaded document(s).

		'''
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
			raise exception

class AwsFileLoader( Loader ):
	'''

		Purpose:
		--------
		Provides AWS S3 file loading functionality.

	'''
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
			aws_secret_access_key: Optional[ str ] = None, aws_session_token: Optional[
				str ] = None,
			region_name: Optional[ str ] = None ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load a single AWS S3 object into LangChain Document objects.

			Parameters:
			-----------
			bucket (str): S3 bucket name.
			key (str): S3 object key.
			aws_access_key_id (Optional[str]): Optional AWS access key.
			aws_secret_access_key (Optional[str]): Optional AWS secret key.
			aws_session_token (Optional[str]): Optional AWS session token.
			region_name (Optional[str]): Optional AWS region.

			Returns:
			--------
			List[Document] | None: Loaded document(s).

		'''
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
			exception.cause = 'AwsFileLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) '
					'-> List[ Document ] | None'
			)
			raise exception

class GoogleSpeechToTextLoader( Loader ):
	'''

		Purpose:
		--------
		Provides Google Speech-to-Text loading functionality for audio transcription.

	'''
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
		'''

			Purpose:
			--------
			Transcribe audio with Google Cloud Speech-to-Text and load the transcript
			into LangChain Document objects.

			Parameters:
			-----------
			project_id (str): Google Cloud project ID.
			file_path (str): Local path or gs:// URI for the audio file.
			config (Optional[Dict[str, Any]]): Optional recognition config.

			Returns:
			--------
			List[Document] | None: Loaded transcript document(s).

		'''
		try:
			throw_if( 'project_id', project_id )
			throw_if( 'file_path', file_path )
			
			self.project_id = project_id
			self.file_path = file_path
			self.config = config
			
			if self.config:
				self.loader = SpeechToTextLoader(
					project_id=self.project_id,
					file_path=self.file_path,
					config=self.config
				)
			else:
				self.loader = SpeechToTextLoader(
					project_id=self.project_id,
					file_path=self.file_path
				)
			
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
			raise exception

class GoogleBucketLoader( Loader ):
	'''

		Purpose:
		--------
		Provides Google Cloud Storage bucket loading functionality using
		LangChain's GCSDirectoryLoader.

	'''
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
		'''

			Purpose:
			--------
			Load supported objects from a Google Cloud Storage bucket into
			LangChain Document objects.

			Parameters:
			-----------
			project_name (str):
				Google Cloud project name or project ID.

			bucket (str):
				Google Cloud Storage bucket name.

			prefix (Optional[str]):
				Optional object prefix / folder filter.

			continue_on_failure (bool):
				Continue when a single object fails to load.

			Returns:
			--------
			List[Document] | None:
				Loaded bucket documents.

		'''
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
			exception.method = (
					'load( self, project_name: str, bucket: str, '
					'prefix: Optional[ str ]=None, continue_on_failure: bool=False ) '
					'-> List[ Document ] | None'
			)
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Split loaded Google Cloud Storage bucket documents into smaller
			chunks for downstream processing.

			Parameters:
			-----------
			chunk (int):
				Maximum number of characters per chunk.

			overlap (int):
				Number of overlapping characters between chunks.

			Returns:
			--------
			List[Document] | None:
				Chunked Document objects.

		'''
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
			exception.cause = 'GoogleBucketLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) '
					'-> List[ Document ] | None'
			)
			raise exception

class AwsBucketLoader( Loader ):
	'''

		Purpose:
		--------
		Provides AWS S3 bucket/directory loading functionality using
		LangChain's S3DirectoryLoader.

	'''
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
	
	def load(
			self,
			bucket: str,
			prefix: Optional[ str ] = None,
			aws_access_key_id: Optional[ str ] = None,
			aws_secret_access_key: Optional[ str ] = None,
			aws_session_token: Optional[ str ] = None,
			region_name: Optional[ str ] = None,
			endpoint_url: Optional[ str ] = None ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Load all supported objects from an AWS S3 bucket or bucket prefix
			into LangChain Document objects.

			Parameters:
			-----------
			bucket (str): AWS S3 bucket name.
			prefix (Optional[str]): Optional key prefix used to restrict loaded
				objects to a virtual folder or subtree.
			aws_access_key_id (Optional[str]): Optional AWS access key ID.
			aws_secret_access_key (Optional[str]): Optional AWS secret access key.
			aws_session_token (Optional[str]): Optional AWS session token.
			region_name (Optional[str]): Optional AWS region name.
			endpoint_url (Optional[str]): Optional custom S3-compatible endpoint.

			Returns:
			--------
			List[Document] | None: Loaded bucket documents.

		'''
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
			
			self.loader = S3DirectoryLoader(
				self.bucket,
				**kwargs
			)
			self.documents = self.loader.load( )
			return self.documents
		except Exception as e:
			exception = Error( e )
			exception.module = 'loaders'
			exception.cause = 'AmazonBucketLoader'
			exception.method = (
					'load( self, bucket: str, prefix: Optional[ str ]=None, '
					'aws_access_key_id: Optional[ str ]=None, '
					'aws_secret_access_key: Optional[ str ]=None, '
					'aws_session_token: Optional[ str ]=None, '
					'region_name: Optional[ str ]=None, '
					'endpoint_url: Optional[ str ]=None ) -> List[ Document ] | None'
			)
			raise exception
	
	def split( self, chunk: int = 1000, overlap: int = 200 ) -> List[ Document ] | None:
		'''

			Purpose:
			--------
			Split loaded AWS S3 bucket documents into smaller chunks for
			downstream processing.

			Parameters:
			-----------
			chunk (int): Maximum number of characters per chunk.
			overlap (int): Number of overlapping characters between chunks.

			Returns:
			--------
			List[Document] | None: Chunked Document objects.

		'''
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
			exception.cause = 'AmazonBucketLoader'
			exception.method = (
					'split( self, chunk: int=1000, overlap: int=200 ) '
					'-> List[ Document ] | None'
			)
			raise exception
