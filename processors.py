'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                processors.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="guro.py" company="Terry D. Eppler">

	     name.py
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
    name.py
  </summary>
  ******************************************************************************************
  '''
from __future__ import annotations
import string

import docx
from pymupdf import Page, Document
from sklearn.feature_extraction.text import TfidfVectorizer
from boogr import Error
from bs4 import BeautifulSoup
import chromadb
from chromadb.config import Settings
from collections import Counter
import html
import glob
from gensim.models import Word2Vec
import json
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk import FreqDist, ConditionalFreqDist
from nltk.corpus import stopwords, wordnet, words
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import os
import pandas as pd
from pandas import DataFrame, Series
from pathlib import Path
from pinecone import Pinecone, ServerlessSpec
import re
import spacy
from spacy import Language
import sqlite3
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
from typing import List, Optional, Dict, Tuple, Any, Set
import tiktoken
from tiktoken.core import Encoding
import unicodedata
from lxml import etree

try:
	import fitz
except Exception:
	fitz = None

DELIMITERS: Set[ str ] = { '. ', '; ', '? ', '! ', ', ' }

SYMBOLS: Set[ str ] = {
		"@",
		"#",
		"$",
		"^",
		"*",
		"<",
		">",
		"+",
		"=",
		"|",
		"\\",
		"<",
		">",
		":",
		"[",
		"]",
		"{",
		"}",
		"(",
		")",
		"`",
		"~",
		"-",
		"_",
		'"',
		"'",
		".",
}

ASCII_LETTERS: Set[ str ] = set( string.ascii_letters )

DIGITS: Set[ str ] = set( string.digits )

PUNCTUATION: Set[ str ] = set( string.punctuation )

WHITESPACE: Set[ str ] = {
		" ", "\t", "\n", "\r", "\v", "\f"
}

CONTROL_CHARACTERS: Set[ str ] = {
		chr( i ) for i in range( 0x00, 0x20 )
}.union( { chr( 0x7F ) } )

NUMERALS = (r"\bM{0,4}(CM|CD|D?C{0,3})"
            r"(XC|XL|L?X{0,3})"
            r"(IX|IV|V?I{0,3})\b")

try:
	nltk.data.find( 'tokenizers/punkt' )
except LookupError:
	nltk.download( 'punkt' )
	nltk.download( 'punkt_tab' )
	nltk.download( 'stopwords' )
	nltk.download( 'wordnet' )
	nltk.download( 'omw-1.4' )
	nltk.download( 'words' )

def throw_if( name: str, value: object ):
	if value is None:
		raise Exception( f'Argument "{name}" cannot be empty!' )

class Processor( ):
	"""Base class for processing classes.
	
	Purpose:
	    Documents the `Processor` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	lemmatizer: Optional[ WordNetLemmatizer ]
	stemmer: Optional[ PorterStemmer ]
	file_path: Optional[ str ]
	normalized: Optional[ str ]
	lemmatized: Optional[ str ]
	tokenized: Optional[ str ]
	encoding: Optional[ Encoding ]
	nlp: Optional[ Language ]
	parts_of_speech: Optional[ List[ Tuple[ str, str ] ] ]
	embedddings: Optional[ List[ np.ndarray ] ]
	chunk_size: Optional[ int ]
	corrected: Optional[ str ]
	raw_input: Optional[ str ]
	raw_html: Optional[ str ]
	raw_pages: Optional[ List[ str ] ]
	lines: Optional[ List[ str ] ]
	tokens: Optional[ List[ str ] ]
	lines: Optional[ List[ str ] ]
	files: Optional[ List[ str ] ]
	pages: Optional[ List[ str ] ]
	paragraphs: Optional[ List[ str ] ]
	ids: Optional[ List[ int ] ]
	stop_words: Optional[ set ]
	vocabulary: Optional[ set ]
	corpus: Optional[ DataFrame ]
	removed: Optional[ List[ str ] ]
	frequency_distribution: Optional[ DataFrame ]
	
	def __init__( self ):
		self.lemmatizer = WordNetLemmatizer( )
		self.stemmer = PorterStemmer( )
		self.files = [ ]
		self.lines = [ ]
		self.tokens = [ ]
		self.lines = [ ]
		self.pages = [ ]
		self.ids = [ ]
		self.chunks = [ ]
		self.chunk_size = 0
		self.paragraphs = [ ]
		self.embedddings = [ ]
		self.stop_words = set( )
		self.vocabulary = set( )
		self.frequency_distribution = { }
		self.encoding = None
		self.corrected = None
		self.lowercase = None
		self.raw_html = None
		self.corpus = None
		self.file_path = ''
		self.raw_input = ''
		self.normalized = ''
		self.lemmatized = ''
		self.tokenized = ''
		self.cleaned_text = ''

class TextParser( Processor ):
	"""Class providing path preprocessing functionality.
	
	Purpose:
	    Documents the `TextParser` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	lowercase: Optional[ str ]
	cleaned_text: Optional[ str ]
	cleaned_lines: Optional[ List[ str ] ]
	cleaned_tokens: Optional[ List[ str ] ]
	cleaned_pages: Optional[ List[ str ] ]
	cleaned_html: Optional[ str ]
	conditional_distribution: Optional[ DataFrame ]
	PUNCTUATION: Optional[ Set[ str ] ]
	CONTROL_CHARACTERS: Optional[ Set[ str ] ]
	DELIMITERS: Optional[ Set[ str ] ]
	DIGITS: Optional[ Set[ str ] ]
	SYMBOLS: Optional[ Set[ str ] ]
	NUMERALS: Optional[ str ]
	
	def __init__( self ):
		"""Constructor for 'Text' objects.
		
		Purpose:
		    Initializes `TextParser` instance state while preserving the constructor contract used by the application."""
		super( ).__init__( )
		self.PUNCTUATION = PUNCTUATION
		self.CONTROL_CHARACTERS = ({ chr( i ) for i in range( 0x00, 0x20 ) } | { chr( 0x7F ) })
		self.DELIMITERS = DELIMITERS
		self.DIGITS = DIGITS
		self.SYMBOLS = SYMBOLS
		self.NUMERALS = NUMERALS
		self.lemmatizer = WordNetLemmatizer( )
		self.stemmer = PorterStemmer( )
		self.encoding = tiktoken.get_encoding( 'cl100k_base' )
		self.lines = [ ]
		self.tokens = [ ]
		self.pages = [ ]
		self.ids = [ ]
		self.paragraphs = [ ]
		self.chunks = [ ]
		self.chunk_size = 10
		self.raw_pages = [ ]
		self.stop_words = set( )
		self.frequency_distribution = { }
		self.file_path = ''
		self.raw_input = ''
		self.normalized = ''
		self.lemmatized = ''
		self.tokenized = ''
		self.cleaned_text = ''
		self.vocabulary = None
		self.corrected = None
		self.lowercase = None
		self.raw_html = None
		self.translator = None
		self.tokenizer = None
		self.vectorizer = None
	
	def __dir__( self ) -> List[ str ] | None:
		"""Provides a list of strings representing class members.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
		return [  # Attributes
				'file_path',
				'raw_input',
				'raw_pages',
				'normalized',
				'lemmatized',
				'tokenized',
				'corrected',
				'cleaned_text',
				'words',
				'paragraphs',
				'words',
				'pages',
				'chunks',
				'chunk_size',
				'stop_words',
				'removed',
				'lowercase',
				'encoding',
				'vocabulary',
				'translator',
				'lemmatizer',
				'stemmer',
				'tokenizer',
				'vectorizer',
				'conditional_distribution',
				# Methods
				'split_sentences',
				'split_pages',
				'collapse_whitespace',
				'compress_whitespace',
				'remove_punctuation',
				'remove_numbers',
				'remove_special',
				'remove_html',
				'remove_markdown',
				'remove_stopwords',
				'remove_formatting',
				'remove_headers',
				'remove_encodings',
				'tiktokenize',
				'lemmatize_text',
				'normalize_text',
				'chunk_text',
				'chunk_sentences',
				'chunk_files',
				'chunk_data',
				'chunk_datasets',
				'create_wordbag',
				'clean_file',
				'clean_files',
				'convert_jsonl',
				'speech_tagging',
				'split_paragraphs',
				'calculate_frequency_distribution',
				'create_vocabulary',
				'create_wordbag',
				'create_vectors',
				'encode_sentences',
				'semantic_search' ]
	
	def load_text( self, filepath: str ) -> str | None:
		"""Loads raw text from a file.
		
		Purpose:
		    Provides the `load_text` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    filepath (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'filepath', filepath )
			if not os.path.exists( filepath ):
				raise FileNotFoundError( f'File not found: {filepath}' )
			else:
				self.file_path = filepath
			raw_text = open( self.file_path, mode='r', encoding='utf-8', errors='ignore' ).read( )
			return raw_text
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'load_text( self, file_path: str ) -> str'
			raise exception
	
	def collapse_whitespace( self, text: str ) -> str | None:
		"""Removes extra lines from the string 'text'.
		
		Purpose:
		    Provides the `collapse_whitespace` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			return ' '.join( _text.split( ) )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'collapse_whitespace( self, path: str ) -> str:'
			raise exception
	
	def remove_punctuation( self, text: str ) -> str:
		"""Removes all punctuation characters from the input text using NLTK's tokenizer.
		
		Purpose:
		    Provides the `remove_punctuation` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			_tokens = word_tokenize( _text )
			cleaned_tokens = [ re.sub( r'[^\w\s]', '', t ) for t in _tokens if
			                   re.sub( r'[^\w\s]', '', t ) ]
			return ' '.join( cleaned_tokens )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'remove_punctuation( self, text: str ) -> str:'
			raise exception
	
	def normalize_text( self, text: str ) -> str | None:
		"""Converts the input 'text' to lower case.
		
		Purpose:
		    Provides the `normalize_text` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			return text.lower( )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'normalize_text( self, text: str ) -> str:'
			raise exception
	
	def remove_errors( self, text: str ) -> str:
		"""Removes tokens that are not recognized as valid English words.
		
		Purpose:
		    Provides the `remove_errors` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_vocab = words.words( 'en' )
			_text = text.lower( )
			_tokens = _text.split( )
			_words = [ w for w in _tokens if w in _vocab ]
			_data = ' '.join( _words )
			return _data
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'remove_errors( self, text: str  ) -> str'
			raise exception
	
	def remove_fragments( self, text: str ) -> str | None:
		"""Removes strings less that 4 chars in length.
		
		Purpose:
		    Provides the `remove_fragments` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			_cleaned = [ ]
			_fragments = _text.split( )
			for char in _fragments:
				if len( char ) > 2:
					_cleaned.append( char )
			return ' '.join( _cleaned )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'remove_fragments( self, text: str ) -> str:'
			raise exception
	
	def remove_symbols( self, text: str ) -> str | None:
		"""Removes special characters from the path path path.
		
		Purpose:
		    Provides the `remove_symbols` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			return ''.join( c for c in _text if c not in self.SYMBOLS )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'remove_symbols( self, text: str ) -> str:'
			raise exception
	
	def remove_html( self, text: str ) -> str | None:
		"""Removes HTML tags from the path.
		
		Purpose:
		    Provides the `remove_html` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			self.raw_html = text
			cleaned_html = BeautifulSoup( self.raw_html, 'html.parser' ).get_text( )
			return cleaned_html
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'remove_html( self, text: str ) -> str'
			raise exception
	
	def remove_xml( self, text: str ) -> str:
		"""Remove XML tags from a string while preserving inner text content using.
		
		Purpose:
		    Provides the `remove_xml` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		throw_if( 'text', text )
		try:
			_text = text.lower( )
			wrapped_text = f"<root>{_text}</root>"
			parser = etree.XMLParser( recover=True, remove_comments=True,
				remove_blank_text=False )
			
			root = etree.fromstring( wrapped_text.encode( "utf-8" ), parser )
			text_parts = [ ]
			for element in root.iter( ):
				if element.text:
					text_parts.append( element.text )
				if element.tail:
					text_parts.append( element.tail )
			
			return "".join( text_parts )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'remove_xml( self, text: str ) -> str'
			raise exception
	
	def remove_markdown( self, text: str ) -> str | None:
		"""Removes Markdown syntax (e.g., *, #, [], etc.).
		
		Purpose:
		    Provides the `remove_markdown` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			self.raw_input = text.lower( )
			_text = re.sub( r'\[.*?]\(.*?\)', ' ', self.raw_input )
			_unmarked = re.sub( r'[`_*#~><-]', ' ', _text )
			self.cleaned_text = re.sub( r'!\[.*?]\(.*?\)', ' ', _unmarked )
			return self.cleaned_text
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'remove_markdown( self, path: str ) -> str'
			raise exception
	
	def remove_stopwords( self, text: str ) -> str | None:
		"""This function:.
		
		Purpose:
		    Provides the `remove_stopwords` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_stop_words = set( stopwords.words( 'english' ) )
			_text = text.lower( )
			_tokens = word_tokenize( _text )
			_filtered = [ token for token in _tokens if
			              token.isalnum( ) and token not in _stop_words ]
			return ' '.join( _filtered )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'remove_stopwords( self, text: str ) -> str'
			raise exception
	
	def remove_encodings( self, text: str ) -> str | None:
		"""Cleans text of encoding artifacts by resolving HTML entities,.
		
		Purpose:
		    Provides the `remove_encodings` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			try:
				_text = text.lower( )
				text = bytes( _text, 'utf-8' ).decode( 'unicode_escape' )
			except UnicodeDecodeError:
				pass
			
			self.raw_input = text
			_html = html.unescape( self.raw_input )
			_norm = unicodedata.normalize( 'NFKC', _html )
			_chars = re.sub( r'[\x00-\x1F\x7F]', '', _norm )
			cleaned_text = _chars.strip( )
			return cleaned_text
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'remove_encodings( self, text: str ) -> str'
			raise exception
	
	def remove_headers( self, filepath: str, lines: int = 50, headers: int = 3,
			footers: int = 3 ) -> str | None:
		"""Remove repetitive headers and footers from a text document by identifying recurring.
		
		Purpose:
		    Provides the `remove_headers` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    filepath (str): Input value passed to the callable.
		    lines (int): Input value passed to the callable.
		    headers (int): Input value passed to the callable.
		    footers (int): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'filepath', filepath )
			if not os.path.exists( filepath ):
				raise FileNotFoundError( f'File not found: {filepath}' )
			else:
				self.file_path = filepath
			if lines < 6:
				raise ValueError( 'Argument \"lines_per_page\" should be at least 6.' )
			if headers < 0 or footers < 0:
				msg = 'Arguments \"header_lines\" and \"footer_lines\" must be non-negative.'
				raise ValueError( msg )
			
			with open( self.file_path, 'r', encoding='utf-8', errors='ignore' ) as fh:
				self.lines = fh.readlines( )
			
			self.pages = [ self.lines[ i: i + lines ] for i in
			               range( 0, len( self.lines ), lines ) ]
			
			header_counts = { }
			footer_counts = { }
			for page in self.pages:
				n = len( page )
				if n == 0:
					continue
				
				if headers > 0 and n >= headers:
					hdr = tuple( page[ :headers ] )
					if hdr in header_counts:
						header_counts[ hdr ] += 1
					else:
						header_counts[ hdr ] = 1
				
				if footers > 0 and n >= footers:
					ftr = tuple( page[ -footers: ] )
					if ftr in footer_counts:
						footer_counts[ ftr ] += 1
					else:
						footer_counts[ ftr ] = 1
			
			common_header = ( )
			if header_counts:
				common_header = max( header_counts.items( ), key=lambda kv: kv[ 1 ] )[ 0 ]
			
			common_footer = ( )
			if footer_counts:
				common_footer = max( footer_counts.items( ), key=lambda kv: kv[ 1 ] )[ 0 ]
			
			cleaned_pages = [ ]
			for page in self.pages:
				lines = list( page )
				
				if common_header and len( lines ) >= len( common_header ):
					if tuple( lines[ : len( common_header ) ] ) == common_header:
						lines = lines[ len( common_header ): ]
				
				if common_footer and len( lines ) >= len( common_footer ):
					if tuple( lines[ -len( common_footer ): ] ) == common_footer:
						lines = lines[ : -len( common_footer ) ]
				
				cleaned_pages.append( ''.join( lines ) )
			return '\n'.join( cleaned_pages )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'remove_headers( self, filepath: str ) -> str'
			raise exception
	
	def remove_numbers( self, text: str ) -> str | None:
		"""Removes the numbers 0 through 9 from the input text.
		
		Purpose:
		    Provides the `remove_numbers` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			return re.sub( r'\d+', '', _text )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'remove_encodings( self, text: str ) -> str'
			raise exception
	
	def remove_numerals( self, text: str ) -> str | None:
		"""Removes the numbers 0 through 9 from the input text.
		
		Purpose:
		    Provides the `remove_numerals` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			self.raw_input = text.lower( )
			self.cleaned_text = re.sub( self.NUMERALS, ' ', self.raw_input, flags=re.IGNORECASE, )
			return self.cleaned_text
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'remove_numerals( self, text: str ) -> str'
			raise exception
	
	def remove_images( self, text: str ) -> str:
		"""Remove image references from text, including Markdown images, HTML <img> tags,.
		
		Purpose:
		    Provides the `remove_images` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		throw_if( "text", text )
		
		try:
			self.raw_input = text
			
			# Remove Markdown images: ![alt](path)
			without_markdown_images = re.sub(
				r"!\[[^\]]*]\([^)]*\)",
				" ",
				self.raw_input
			)
			
			# Remove HTML <img> tags
			without_html_images = re.sub(
				r"<img\b[^>]*>",
				" ",
				without_markdown_images,
				flags=re.IGNORECASE
			)
			
			# Remove standalone image URLs
			self.parsed_text = re.sub(
				r"https?://\S+\.(png|jpg|jpeg|gif|bmp|svg|webp)",
				" ",
				without_html_images,
				flags=re.IGNORECASE
			)
			
			return self.parsed_text
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = ('remove_formatting( self, text: str ) -> str')
			raise exception
	
	def tiktokenize( self, text: str, encoding: str = 'cl100k_base' ) -> DataFrame | None:
		"""Tokenizes text text into subword words using OpenAI's tiktoken tokenizer.
		
		Purpose:
		    Provides the `tiktokenize` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		    encoding (str): Input value passed to the callable.
		
		Returns:
		    DataFrame: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			self.encoding = tiktoken.get_encoding( encoding )
			token_ids = self.encoding.encode( _text )
			_data = pd.DataFrame( token_ids )
			return _data
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = ('tiktokenize( self, text, encoding) -> List[ int ]')
			raise exception
	
	def split_sentences( self, text: str ) -> List[ str ] | None:
		"""Splits the text string into a list of strings using NLTK's Punkt sentence tokenizer.
		
		Purpose:
		    Provides the `split_sentences` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    List[str]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			_sentences = sent_tokenize( _text )
			return _sentences
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'split_sentences( self, text: str ) -> DataFrame'
			raise exception
	
	def split_pages( self, filepath: str, num: int = 50 ) -> List[ str ] | None:
		"""Splits a plain-text document into a list of pages using either form-feed characters.
		
		Purpose:
		    Provides the `split_pages` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    filepath (str): Input value passed to the callable.
		    num (int): Input value passed to the callable.
		
		Returns:
		    List[str]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'filepath', filepath )
			if not os.path.exists( filepath ):
				raise FileNotFoundError( f'File not found: {filepath}' )
			else:
				self.file_path = filepath
			with open( self.file_path, 'r', encoding='utf-8', errors='ignore' ) as file:
				content = file.read( )
			if '\f' in content:
				return [ page.strip( ) for page in content.split( '\f' ) if page.strip( ) ]
			self.lines = content.splitlines( )
			i = 0
			n = len( self.lines )
			while i < n:
				page_lines = self.lines[ i: i + num ]
				page_text = '\n'.join( page_lines ).strip( )
				if page_text:
					self.pages.append( page_text )
				i += num
			return self.pages
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'split_pages( file_path )'
			raise exception
	
	def split_paragraphs( self, filepath: str ) -> DataFrame | None:
		"""Reads  a file and splits it into paragraphs. A paragraph is defined as a block.
		
		Purpose:
		    Provides the `split_paragraphs` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    filepath (str): Input value passed to the callable.
		
		Returns:
		    DataFrame: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'filepath', filepath )
			if not os.path.exists( filepath ):
				raise FileNotFoundError( f'File not found: {filepath}' )
			else:
				self.file_path = filepath
			with open( self.file_path, 'r', encoding='utf-8', errors='ignore' ) as file:
				_input = file.read( )
				_paragraphs = [ pg.strip( ) for pg in _input.split( ' ' ) if pg.strip( ) ]
				_data = pd.DataFrame( _paragraphs )
				return _data
		except UnicodeDecodeError:
			with open( self.file_path, 'r', encoding='latin1', errors='ignore' ) as file:
				_input = file.read( )
				_paragraphs = [ pg.strip( ) for pg in _input.split( ' ' ) if pg.strip( ) ]
				_data = pd.DataFrame( _paragraphs )
				return _data
	
	def create_frequency_distribution( self, tokens: List[ str ] ) -> DataFrame | None:
		"""Creates a word frequency freq_dist from a list of tokens.
		
		Purpose:
		    Provides the `create_frequency_distribution` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    tokens (List[str]): Input value passed to the callable.
		
		Returns:
		    DataFrame: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'tokens', tokens )
			self.tokens = tokens
			_freqdist = FreqDist( dict( Counter( self.tokens ) ) )
			_words = _freqdist.items( )
			_data = pd.DataFrame( _words, columns=[ 'Word', 'Frequency' ] )
			_data.index.name = 'ID'
			return _data
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'create_frequency_distribution(self, tokens: List[ str ])->DataFrame'
			raise exception
	
	def create_vocabulary( self, tokens: List[ str ] ) -> Series | None:
		"""Builds a vocabulary list from a frequency.
		
		Purpose:
		    Provides the `create_vocabulary` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    tokens (List[str]): Input value passed to the callable.
		
		Returns:
		    Series: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'tokens', tokens )
			self.tokens = tokens
			_freqdist = FreqDist( dict( Counter( self.tokens ) ) )
			_vocab = _freqdist.items( )
			_vocabulary = pd.DataFrame( _vocab, columns=[ 'Word', 'Frequency' ] )
			_words = _vocabulary.iloc[ :, 0 ]
			return _words
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = ('create_vocabulary(self, freq_dist: dict, min: int=1)->List[str]')
			raise exception
	
	def create_wordbag( self, tokens: List[ str ] ) -> DataFrame | None:
		"""Construct a Bag-of-Words (BoW) frequency dictionary from a list of strings.
		
		Purpose:
		    Provides the `create_wordbag` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    tokens (List[str]): Input value passed to the callable.
		
		Returns:
		    DataFrame: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'tokens', tokens )
			self.tokens = tokens
			_freqdist = FreqDist( dict( Counter( self.tokens ) ) )
			_words = _freqdist.keys( )
			_data = pd.DataFrame( _words )
			return _data
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'create_wordbag( self, words: List[ str ] ) -> dict'
			raise exception
	
	def create_vectors( self, tokens: List[ str ] ) -> DataFrame | None:
		"""Generates word embeddings using TF-IDF vectors from a list of tokens.
		
		Purpose:
		    Provides the `create_vectors` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    tokens (List[str]): Input value passed to the callable.
		
		Returns:
		    DataFrame: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			fake_docs = [ [ word ] for word in tokens ]
			joined_docs = [ ' '.join( doc ) for doc in fake_docs ]
			vectorizer = TfidfVectorizer( )
			X = vectorizer.fit_transform( joined_docs )
			feature_names = vectorizer.get_feature_names_out( )
			embeddings = { }
			for idx, word in enumerate( tokens ):
				vector = X[ idx ].toarray( ).flatten( )
				embeddings[ word ] = vector
			
			_data = pd.DataFrame( data=embeddings, columns=feature_names )
			return embeddings
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'create_vectors( self, tokens: List[str]) -> Dict[str, np.ndarray]'
			raise exception
	
	def clean_file( self, filepath: str ) -> str | None:
		"""Cleans text files given a source directory (src) and destination directory (dest).
		
		Purpose:
		    Provides the `clean_file` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    filepath (str): Input value passed to the callable.
		
		Returns:
		    str: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'filepath', filepath )
			if not os.path.exists( filepath ):
				raise FileNotFoundError( f'File not found: {filepath}' )
			else:
				_sourcepath = filepath
				_text = open( _sourcepath, 'r', encoding='utf-8', errors='ignore' ).read( )
				_collapsed = self.collapse_whitespace( _text )
				_compressed = self.compress_whitespace( _collapsed )
				_normalized = self.normalize_text( _compressed )
				_encoded = self.remove_encodings( _normalized )
				_special = self.remove_symbols( _encoded )
				_cleaned = self.remove_fragments( _special )
				_recompress = self.compress_whitespace( _cleaned )
				_lemmatized = self.lemmatize_text( _recompress )
				_stops = self.remove_stopwords( _lemmatized )
				return _stops
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'clean_file( self, src: str ) -> str'
			raise exception
	
	def clean_files( self, source: str, destination: str ) -> None:
		"""Cleans text files given a source directory (src) and destination directory (dest).
		
		Purpose:
		    Provides the `clean_files` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    source (str): Input value passed to the callable.
		    destination (str): Input value passed to the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'src', source )
			throw_if( 'dest', destination )
			if not os.path.exists( source ):
				raise FileNotFoundError( f'File not found: {source}' )
			elif not os.path.exists( destination ):
				raise FileNotFoundError( f'File not found: {destination}' )
			else:
				_source = source
				_destpath = destination
				_files = os.listdir( _source )
				for f in _files:
					_processed = [ ]
					_filename = os.path.basename( f )
					_sourcepath = _source + '\\' + _filename
					_text = open( _sourcepath, 'r', encoding='utf-8', errors='ignore' ).read( )
					_collapsed = self.collapse_whitespace( _text )
					_compressed = self.compress_whitespace( _collapsed )
					_normalized = self.normalize_text( _compressed )
					_encoded = self.remove_encodings( _normalized )
					_special = self.remove_symbols( _encoded )
					_cleaned = self.remove_fragments( _special )
					_recompress = self.compress_whitespace( _cleaned )
					_lemmatized = self.lemmatize_text( _recompress )
					_stops = self.remove_stopwords( _lemmatized )
					_sentences = self.split_sentences( _stops )
					_destination = _destpath + '\\' + _filename
					_clean = open( _destination, 'wt', encoding='utf-8', errors='ignore' )
					_lines = ' '.join( _sentences )
					_clean.write( _lines )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'clean_files( self, src: str, dest: str )'
			raise exception
	
	def chunk_files( self, source: str, destination: str ) -> None:
		"""Chunks cleaned text files given a _source directory and destination directory.
		
		Purpose:
		    Provides the `chunk_files` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    source (str): Input value passed to the callable.
		    destination (str): Input value passed to the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'src', source )
			throw_if( 'dest', destination )
			if not os.path.exists( source ):
				raise FileNotFoundError( f'File not found: {source}' )
			elif not os.path.exists( destination ):
				raise FileNotFoundError( f'File not found: {destination}' )
			else:
				_source = source
				_destination = destination
				_files = os.listdir( _source )
				_words = [ ]
				for f in _files:
					_processed = [ ]
					_filename = os.path.basename( f )
					_sourcepath = _source + '\\' + _filename
					_text = open( _sourcepath, 'r', encoding='utf-8', errors='ignore' ).read( )
					_sentences = self.split_sentences( _text )
					_datamap = [ ]
					for v in _sentences:
						_datamap.append( v )
					
					for s in _datamap:
						_processed.append( s )
					
					_final = _destination + '\\' + _filename
					_clean = open( _final, 'wt', encoding='utf-8', errors='ignore' )
					for p in _processed:
						_clean.write( p )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'chunk_files( self, src: str, dest: str )'
			raise exception
	
	def chunk_data( self, filepath: str, size: int = 10 ) -> DataFrame | None:
		"""Chunks cleaned text files given a source directory and destination directory.
		
		Purpose:
		    Provides the `chunk_data` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    filepath (str): Input value passed to the callable.
		    size (int): Input value passed to the callable.
		
		Returns:
		    DataFrame: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'filepath', filepath )
			if not os.path.exists( filepath ):
				raise FileNotFoundError( f'File not found: {filepath}' )
			else:
				_source = filepath
				_processed = [ ]
				_wordlist = [ ]
				_vocab = words.words( 'en' )
				_text = open( _source, 'r', encoding='utf-8', errors='ignore' ).read( )
				_lower = _text.lower( )
				_tokens = _lower.split( )
				for s in _tokens:
					if s.isalpha( ) and s in _vocab:
						_wordlist.append( s )
				self.chunks = [ _wordlist[ i: i + size ] for i in
				                range( 0, len( _wordlist ), size ) ]
				for i, c in enumerate( self.chunks ):
					_item = '[' + ' '.join( c ) + '],'
					_processed.append( _item )
				_data = pd.DataFrame( _processed )
				return _data
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'chunk_data( self, filepath: str, size: int=512  ) -> DataFrame'
			raise exception
	
	def chunk_datasets( self, source: str, destination: str, size: int = 10 ) -> DataFrame:
		"""Chunks cleaned text files given a source directory and destination directory.
		
		Purpose:
		    Provides the `chunk_datasets` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    source (str): Input value passed to the callable.
		    destination (str): Input value passed to the callable.
		    size (int): Input value passed to the callable.
		
		Returns:
		    DataFrame: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'filepath', source )
			throw_if( 'destination', destination )
			if not os.path.exists( source ):
				raise FileNotFoundError( f'File not found: {source}' )
			elif not os.path.exists( destination ):
				raise FileNotFoundError( f'File not found: {destination}' )
			else:
				_src = source
				_destination = destination
				_files = os.listdir( _src )
				_words = [ ]
				for f in _files:
					_processed = [ ]
					_filename = os.path.basename( f )
					_sourcepath = _src + '\\' + _filename
					_text = open( _sourcepath, 'r', encoding='utf-8', errors='ignore' ).read( )
					_collapsed = self.collapse_whitespace( _text )
					_compressed = self.compress_whitespace( _collapsed )
					_normalized = self.normalize_text( _compressed )
					_encoded = self.remove_encodings( _normalized )
					_special = self.remove_symbols( _encoded )
					_cleaned = self.remove_fragments( _special )
					_recompress = self.compress_whitespace( _cleaned )
					_lemmatized = self.lemmatize_text( _recompress )
					_stops = self.remove_stopwords( _lemmatized )
					_tokens = _stops.split( None )
					_chunks = [ _tokens[ i: i + size ] for i in range( 0, len( _tokens ), size ) ]
					_datamap = [ ]
					for i, c in enumerate( _chunks ):
						_row = ' '.join( c )
						_datamap.append( _row )
					
					for s in _datamap:
						_processed.append( s )
					
					_name = _filename.replace( '.txt', '.xlsx' )
					_savepath = (_destination + f'\\' + _name)
					_data = pd.DataFrame( _processed, columns=[ 'Data', ] )
					_data.to_excel( _savepath, sheet_name='Dataset', index=False,
						columns=[ 'Data', ] )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'chunk_data( self, filepath: str, size: int=15  ) -> DataFrame'
			raise exception
	
	def convert_jsonl( self, source: str, destination: str, size: int = 10 ) -> None:
		"""Coverts text files to JSONL format given a source directory (Source).
		
		Purpose:
		    Provides the `convert_jsonl` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    source (str): Input value passed to the callable.
		    destination (str): Input value passed to the callable.
		    size (int): Input value passed to the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'source', source )
			throw_if( 'destination', destination )
			if not os.path.exists( source ):
				raise FileNotFoundError( f'File not found: {source}' )
			elif not os.path.exists( destination ):
				raise FileNotFoundError( f'File not found: {destination}' )
			else:
				_source = source
				_destpath = destination
				_files = os.listdir( _source )
				_wordlist = [ ]
				for f in _files:
					_processed = [ ]
					_filename = os.path.basename( f )
					_sourcepath = _source + '\\' + _filename
					_text = open( _sourcepath, 'r', encoding='utf-8', errors='ignore' ).read( )
					_tokens = _text.split( ' ' )
					_chunks = [ _tokens[ i: i + size ] for i in range( 0, len( _tokens ), size ) ]
					_datamap = [ ]
					for i, c in enumerate( _chunks ):
						_value = '{ ' + f' {i} : [ ' + ' '.join( c ) + ' ] }, ' + "\n"
						_datamap.append( _value )
					
					for s in _datamap:
						_processed.append( s )
					
					_destination = _destpath + '\\' + _filename.replace( '.txt', '.jsonl' )
					_clean = open( _destination, 'wt', encoding='utf-8', errors='ignore' )
					for p in _processed:
						_clean.write( p )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'convert_jsonl( self, source: str, desination: str )'
			raise exception
	
	def encode_sentences( self, tokens: List[ str ], model: str = 'all-MiniLM-L6-v2' ) -> \
			Tuple[ List[ str ], np.ndarray ]:
		"""Generate contextual sentence embeddings using SentenceTransformer.
		
		Purpose:
		    Provides the `encode_sentences` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    tokens (List[str]): Input value passed to the callable.
		    model (str): Input value passed to the callable.
		
		Returns:
		    Tuple[List[str], np.ndarray]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'tokens', tokens )
			throw_if( 'model', model )
			_transformer = SentenceTransformer( model )
			_tokens = [ self.lemmatizer.lemmatize( t ) for t in tokens ]
			_encoding = _transformer.encode( _tokens, show_progress_bar=True )
			return (self.cleaned_tokens, np.array( _encoding ))
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'encode_sentences( self, sentences: List[ str ], model_name ) -> ( )'
			raise exception
	
	def semantic_search( self, query: str, tokens: List[ str ], embeddings: np.ndarray,
			model: SentenceTransformer, top: int = 5 ) -> List[ tuple[ str, float ] ]:
		"""Perform semantic search over embedded corpus using query.
		
		Purpose:
		    Provides the `semantic_search` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    query (str): Input value passed to the callable.
		    tokens (List[str]): Input value passed to the callable.
		    embeddings (np.ndarray): Input value passed to the callable.
		    model (SentenceTransformer): Input value passed to the callable.
		    top (int): Input value passed to the callable.
		
		Returns:
		    List[tuple[str, float]]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'query', query )
			throw_if( 'tokens', tokens )
			throw_if( 'embedding', embeddings )
			throw_if( 'model', model )
			query_vec = model.encode( [ query ] )
			sims = cosine_similarity( query_vec, embeddings )[ 0 ]
			top_indices = sims.argsort( )[ ::-1 ][ : top ]
			return [ (tokens[ i ], sims[ i ]) for i in top_indices ]
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = ('semantic_search( self, query: str, tokens: List[ str ], '
			                    'embeddings: np.ndarray, model: SentenceTransformer,  '
			                    'top_k: int=5 ) -> List[ tuple[ str, float ] ]')
			raise exception

class NltkParser( Processor ):
	"""Class providing NLTK-based natural language processing functionality for text that.
	
	Purpose:
	    Documents the `NltkParser` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	word_tokens: Optional[ List[ str ] ]
	sentence_tokens: Optional[ List[ str ] ]
	stemmed_tokens: Optional[ List[ str ] ]
	lemmatized_tokens: Optional[ List[ str ] ]
	tagged_tokens: Optional[ List[ Tuple[ str, str ] ] ]
	named_entities: Optional[ List[ Tuple[ str, str ] ] ]
	
	def __init__( self ) -> None:
		"""Initializes the NltkParser and prepares internal containers used by the.
		
		Purpose:
		    Initializes `NltkParser` instance state while preserving the constructor contract used by the application."""
		super( ).__init__( )
		self.initialize_resources( )
		self.word_tokens = [ ]
		self.sentence_tokens = [ ]
		self.stemmed_tokens = [ ]
		self.lemmatized_tokens = [ ]
		self.tagged_tokens = [ ]
		self.named_entities = [ ]
	
	def __dir__( self ) -> List[ str ] | None:
		"""Provides a list of strings representing class members.
		
		Purpose:
		    Provides the `__dir__` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    List[str]: Returned value produced by the callable."""
		return [ 'initialize_resources', 'word_tokenizer', 'sentence_tokenizer', 'word_stemmer',
		         'word_lemmatizer', 'pos_tagger', 'named_entity_recognition', 'word_tokens',
		         'sentence_tokens', 'stemmed_tokens', 'lemmatized_tokens', 'tagged_tokens',
		         'named_entities' ]
	
	def initialize_resources( self ) -> None:
		"""Ensures the NLTK tokenizers, taggers, and corpora required by this class.
		
		Purpose:
		    Provides the `initialize_resources` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			required_resources: List[ Tuple[ str, str ] ] = [
					('tokenizers/punkt', 'punkt'),
					('tokenizers/punkt_tab', 'punkt_tab'),
					('corpora/wordnet', 'wordnet'),
					('corpora/omw-1.4', 'omw-1.4'),
					('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
					('taggers/averaged_perceptron_tagger_eng', 'averaged_perceptron_tagger_eng'),
					('chunkers/maxent_ne_chunker', 'maxent_ne_chunker'),
					('chunkers/maxent_ne_chunker_tab', 'maxent_ne_chunker_tab'),
					('corpora/words', 'words'), ]
			
			for resource_path, resource_name in required_resources:
				try:
					nltk.data.find( resource_path )
				except LookupError:
					nltk.download( resource_name )
		except Exception as e:
			exception = Error( e )
			exception.module = 'processing'
			exception.cause = 'NltkParser'
			exception.method = 'NltkParser._ensure_nltk_resources( self ) -> None'
			raise exception
	
	def word_tokenizer( self, text: str ) -> List[ str ] | None:
		"""Tokenizes the input text into word tokens and returns a display-ready.
		
		Purpose:
		    Provides the `word_tokenizer` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    List[str]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			self.word_tokens = word_tokenize( _text )
			words = [ token for token in self.word_tokens ]
			return words
		except Exception as e:
			exception = Error( e )
			exception.module = 'processing'
			exception.cause = 'NltkParser'
			exception.method = 'word_tokenizer( self, text: str ) -> List[ str ]'
			raise exception
	
	def sentence_tokenizer( self, text: str ) -> List[ str ] | None:
		"""Tokenizes the input text into sentences and returns a display-ready.
		
		Purpose:
		    Provides the `sentence_tokenizer` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    List[str]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			self.sentence_tokens = sent_tokenize( _text )
			return self.sentence_tokens
		except Exception as e:
			exception = Error( e )
			exception.module = 'processing'
			exception.cause = 'NltkParser'
			exception.method = 'tokenize_sentences( self, text: str ) -> str'
			raise exception
	
	def word_stemmer( self, text: str ) -> List[ str ] | None:
		"""Applies stemming to the input text and returns a whitespace-joined.
		
		Purpose:
		    Provides the `word_stemmer` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    List[str]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			self.word_tokens = word_tokenize( _text )
			self.stemmed_tokens = [ self.stemmer.stem( t ) for t in self.word_tokens
			                        if isinstance( t, str ) and t.strip( ) ]
			
			return self.stemmed_tokens
		except Exception as e:
			exception = Error( e )
			exception.module = 'processing'
			exception.cause = 'NltkParser'
			exception.method = 'stemmer( self, text: str ) -> str'
			raise exception
	
	def word_lemmatizer( self, text: str ) -> List[ str ] | None:
		"""Applies WordNet lemmatization to the input text and returns a.
		
		Purpose:
		    Provides the `word_lemmatizer` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    List[str]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			self.word_tokens = word_tokenize( _text )
			self.lemmatized_tokens = [ self.lemmatizer.lemmatize( t ) for t in self.word_tokens
			                           if isinstance( t, str ) and t.strip( ) ]
			
			return self.lemmatized_tokens
		except Exception as e:
			exception = Error( e )
			exception.module = 'processing'
			exception.cause = 'NltkParser'
			exception.method = 'lemmatizer( self, text: str ) -> str'
			raise exception
	
	def pos_tagger( self, text: str ) -> List[ Tuple[ str, str ] ] | None:
		"""Applies part-of-speech tagging to the input text and returns a.
		
		Purpose:
		    Provides the `pos_tagger` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    List[Tuple[str, str]]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			self.word_tokens = word_tokenize( _text )
			self.tagged_tokens = nltk.pos_tag( self.word_tokens )
			return self.tagged_tokens
		except Exception as e:
			exception = Error( e )
			exception.module = 'processing'
			exception.cause = 'NltkParser'
			exception.method = 'pos_tagger( self, text: str ) -> str'
			raise exception
	
	def named_entity_recognition( self, text: str ) -> List[ Tuple[ str, str ] ] | None:
		"""Applies named entity recognition to the input text and returns a.
		
		Purpose:
		    Provides the `named_entity_recognition` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		
		Returns:
		    List[Tuple[str, str]]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			self.word_tokens = word_tokenize( _text )
			self.tagged_tokens = nltk.pos_tag( self.word_tokens )
			tree = nltk.ne_chunk( self.tagged_tokens )
			self.named_entities = [ ]
			for node in tree:
				if hasattr( node, 'label' ):
					label = node.label( )
					entity_text = ' '.join( token for token, _ in node.leaves( )
					                        if isinstance( token, str ) and token.strip( ) )
					
					if entity_text:
						self.named_entities.append( (entity_text, label) )
			
			return self.named_entities
		except Exception as e:
			exception = Error( e )
			exception.module = 'processing'
			exception.cause = 'NltkParser'
			exception.method = 'named_entity_recogniztion( self, text: str ) -> str'
			raise exception
	
	def chunk_words( self, text: str, size: int = 5 ) -> DataFrame | None:
		"""Tokenizes cleaned_lines pages and breaks it into chunks for downstream vectors.
		
		Purpose:
		    Provides the `chunk_words` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		    size (int): Input value passed to the callable.
		
		Returns:
		    DataFrame: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			_tokens = nltk.word_tokenize( _text )
			_sentences = [ _tokens[ i: i + size ] for i in range( 0, len( _tokens ), size ) ]
			_datamap = [ ]
			for index, chunk in enumerate( _sentences ):
				_item = ' '.join( chunk )
				_datamap.append( _item )
			
			_data = pd.DataFrame( _datamap )
			return _data
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'TextParser'
			exception.method = 'chunk_sentences( self, text: str, max: int=10 ) -> DataFrame'
			raise exception
	
	def chunk_sentences( self, text: str, size: int = 15 ) -> DataFrame | None:
		"""Tokenizes cleaned_lines pages and breaks it into chunks for downstream vectors.
		
		Purpose:
		    Provides the `chunk_sentences` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    text (str): Input value passed to the callable.
		    size (int): Input value passed to the callable.
		
		Returns:
		    DataFrame: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'text', text )
			_text = text.lower( )
			_tokens = sent_tokenize( _text )
			_sentences = [ _tokens[ i: i + size ] for i in range( 0, len( _tokens ), size ) ]
			_datamap = [ ]
			for i, c in enumerate( _sentences ):
				_item = ' '.join( c )
				_datamap.append( _item )
			
			_data = pd.DataFrame( _datamap )
			return _data
		except Exception as e:
			exception = Error( e )
			exception.module = 'processors'
			exception.cause = 'NltkParser'
			exception.method = 'chunk_sentences( self, text: str, max: int=512 ) -> DataFrame'
			raise exception
