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
    Provides text-processing, tokenization, normalization, cleaning, chunking,
    vectorization, and natural-language processing utilities used by Fonky ingestion
    and retrieval workflows.

    Purpose:
        Centralizes reusable processing routines for plain text, HTML, XML, Markdown,
        document files, token streams, frequency distributions, vector encodings, and
        semantic search inputs. The module prepares raw content for downstream loaders,
        embeddings, analysis, persistence, and model-facing workflows while preserving
        a consistent project error-wrapping pattern.
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
	"""Validate a required argument before processing continues.
	
	Purpose:
	    Prevents later processing stages from operating on missing inputs by raising an
	    exception as soon as a required value is absent. This guard keeps validation behavior
	    consistent across parser and processor methods.
	
	Args:
	    name (str): Argument name used in validation messages.
	    value (object): Value that must be present before processing continues.
	
	Raises:
	    Exception: Raised when the required value is missing."""
	if value is None:
		raise Exception( f'Argument "{name}" cannot be empty!' )

class Processor( ):
	"""Provide shared processor state.
	
	Purpose:
	    Initializes shared state and reusable NLP helpers used by text-processing subclasses.
	    The class centralizes tokenizer, lemmatizer, stemmer, corpus, chunking, and intermediate
	    text containers that derived processors reuse across cleaning, tokenization, and
	    vectorization workflows.
	
	Attributes:
	    lemmatizer (Optional[ WordNetLemmatizer ]): WordNet lemmatizer used by lexical normalization routines.
	    stemmer (Optional[ PorterStemmer ]): Porter stemmer used by stemming routines.
	    file_path (Optional[ str ]): Active local file path being processed.
	    normalized (Optional[ str ]): Most recent normalized text value.
	    lemmatized (Optional[ str ]): Most recent lemmatized text value.
	    tokenized (Optional[ str ]): Most recent tokenized text value.
	    encoding (Optional[ Encoding ]): Active tiktoken encoding instance.
	    nlp (Optional[ Language ]): Optional spaCy language pipeline.
	    parts_of_speech (Optional[ List[ Tuple[ str, str ] ] ]): Part-of-speech tuples generated by parser operations.
	    embedddings (Optional[ List[ np.ndarray ] ]): Embedding vectors generated during vectorization workflows.
	    chunk_size (Optional[ int ]): Current chunk size used by chunking routines.
	    corrected (Optional[ str ]): Corrected text retained by spelling or cleanup workflows.
	    raw_input (Optional[ str ]): Raw text input retained for the active operation.
	    raw_html (Optional[ str ]): Raw HTML input retained before markup removal.
	    raw_pages (Optional[ List[ str ] ]): Raw page strings extracted from a document.
	    lines (Optional[ List[ str ] ]): Line strings read from an input file.
	    tokens (Optional[ List[ str ] ]): Token strings generated from text.
	    files (Optional[ List[ str ] ]): File names or paths collected for batch processing.
	    pages (Optional[ List[ str ] ]): Page-level text blocks generated from file content.
	    paragraphs (Optional[ List[ str ] ]): Paragraph-level text blocks generated from file content.
	    ids (Optional[ List[ int ] ]): Identifier values associated with processed records.
	    stop_words (Optional[ set ]): Stop-word set used by filtering routines.
	    vocabulary (Optional[ set ]): Vocabulary generated from tokens or frequency distributions.
	    corpus (Optional[ DataFrame ]): Tabular corpus representation used by analysis routines.
	    removed (Optional[ List[ str ] ]): Values removed by filtering or cleaning routines.
	    frequency_distribution (Optional[ DataFrame ]): Frequency information generated from token counts."""
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
		"""  init  .
		
		Purpose:
		    Initializes Processor state used by later processing operations. The constructor
		    prepares reusable containers, helper objects, and default runtime values without
		    performing external document processing."""
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
	"""Process and normalize text.
	
	Purpose:
	    Provides text-cleaning, markup-removal, tokenization, chunking, vocabulary, frequency,
	    vectorization, and semantic-search utilities for Fonky processing workflows. The class
	    transforms raw file and string inputs into normalized text, tabular artifacts, token
	    lists, embeddings, and dataset-ready chunks.
	
	Attributes:
	    lowercase (Optional[ str ]): Lowercase text retained by normalization workflows.
	    cleaned_text (Optional[ str ]): Most recent cleaned text output.
	    cleaned_lines (Optional[ List[ str ] ]): Cleaned line strings.
	    cleaned_tokens (Optional[ List[ str ] ]): Cleaned token strings.
	    cleaned_pages (Optional[ List[ str ] ]): Cleaned page strings.
	    cleaned_html (Optional[ str ]): HTML-derived text after tag removal.
	    conditional_distribution (Optional[ DataFrame ]): Conditional frequency-distribution data.
	    PUNCTUATION (Optional[ Set[ str ] ]): Punctuation characters used by filtering routines.
	    CONTROL_CHARACTERS (Optional[ Set[ str ] ]): Control characters removed during cleanup.
	    DELIMITERS (Optional[ Set[ str ] ]): Delimiter strings used by splitting routines.
	    DIGITS (Optional[ Set[ str ] ]): Digit characters used by number filtering routines.
	    SYMBOLS (Optional[ Set[ str ] ]): Symbol characters removed by symbol filtering routines.
	    NUMERALS (Optional[ str ]): Roman-numeral regular expression used by numeral filtering."""
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
		"""  init  .
		
		Purpose:
		    Initializes TextParser state used by later processing operations. The constructor
		    prepares reusable containers, helper objects, and default runtime values without
		    performing external document processing."""
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
		"""Return the public attribute and method names exposed by the object.
		
		Purpose:
		    Returns a stable list of public attributes and methods for interactive inspection,
		    documentation, and UI discovery. The ordering groups state fields and callable
		    processing operations in a predictable way.
		
		Returns:
		    List[ str ] | None: List of processed text values when the operation succeeds."""
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
		"""Read UTF-8 text from a local file and return the raw string.
		
		Purpose:
		    Loads a local text file using UTF-8 with ignored decode errors so downstream cleaning
		    routines can operate on a plain string. The method records the active file path and
		    raises a project Error when the file cannot be read.
		
		Args:
		    filepath (str): Path to the local source file.
		
		Returns:
		    str | None: Processed text value when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Normalize spacing by lowercasing text and collapsing repeated whitespace.
		
		Purpose:
		    Creates a compact lowercase representation of text by splitting on whitespace and
		    joining tokens with single spaces. This prepares raw text for deterministic comparison,
		    cleaning, and tokenization steps.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str | None: Processed text value when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Strip punctuation from tokenized text while preserving word and spacing content.
		
		Purpose:
		    Tokenizes lowercase text and removes punctuation marks from each token. The method
		    preserves alphanumeric token content while returning a whitespace-joined string for
		    later cleaning stages.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str: Processed text value produced by the operation.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Convert text to lowercase for stable downstream comparison and tokenization.
		
		Purpose:
		    Converts text to lowercase without otherwise changing content. This provides a simple
		    normalization stage for workflows that need case-insensitive matching or tokenization.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str | None: Processed text value when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Filter tokens against the NLTK English words corpus.
		
		Purpose:
		    Uses the NLTK English words corpus as a vocabulary filter and keeps only tokens
		    recognized by that corpus. This reduces obvious OCR, spelling, and parsing artifacts
		    before later analysis.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str: Processed text value produced by the operation.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Remove very short token fragments from normalized text.
		
		Purpose:
		    Removes short text fragments that are unlikely to be useful lexical units. This helps
		    reduce noise produced by OCR, markup stripping, punctuation removal, and aggressive
		    token cleanup.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str | None: Processed text value when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Remove configured symbol characters from normalized text.
		
		Purpose:
		    Removes characters listed in the parser symbol set from lowercase text. This produces
		    cleaner text for tokenization, word-frequency generation, and embedding workflows.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str | None: Processed text value when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Extract visible text from HTML markup.
		
		Purpose:
		    Parses HTML input with BeautifulSoup and extracts visible text content. This allows raw
		    HTML fragments or pages to enter the same cleaning pipeline used for plain text.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str | None: Processed text value when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Extract inner text from XML-like markup while recovering malformed fragments when possible.
		
		Purpose:
		    Wraps XML-like text in a temporary root node, parses it with recovery enabled, and
		    concatenates element text and tail content. This retains readable content while
		    discarding markup structure.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str: Processed text value produced by the operation.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Remove common Markdown links, image syntax, and formatting markers.
		
		Purpose:
		    Removes common Markdown link, image, and inline-formatting syntax from lowercase text.
		    This converts README-style or documentation-style content into cleaner text for
		    downstream analysis.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str | None: Processed text value when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Remove English stop words from tokenized text.
		
		Purpose:
		    Tokenizes lowercase text and removes standard English stop words. This leaves a reduced
		    token stream better suited for frequency analysis, vocabulary extraction, and embedding
		    preparation.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str | None: Processed text value when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Resolve HTML entities, normalize Unicode characters, and remove control characters.
		
		Purpose:
		    Decodes common escaped sequences when possible, resolves HTML entities, normalizes
		    Unicode to compatibility form, and strips control characters. This reduces text
		    artifacts from scraped, copied, or encoded sources.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str | None: Processed text value when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Detect and remove repeated page headers and footers from a text file.
		
		Purpose:
		    Splits a text file into page-sized blocks and identifies repeated leading and trailing
		    line groups. Matching header and footer blocks are removed to produce cleaner body text
		    for analysis.
		
		Args:
		    filepath (str): Path to the local source file.
		    lines (int): Number of lines treated as one page during header and footer detection.
		    headers (int): Number of leading lines considered as a repeated page header.
		    footers (int): Number of trailing lines considered as a repeated page footer.
		
		Returns:
		    str | None: Processed text value when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Remove decimal digits from text.
		
		Purpose:
		    Removes digit sequences from lowercase text. This supports workflows that need lexical
		    content without numeric values.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str | None: Processed text value when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Remove Roman-numeral patterns from text.
		
		Purpose:
		    Applies the configured Roman-numeral expression to lowercase text and replaces matching
		    numeral tokens with spaces. This reduces numbering artifacts in outlines, headings, and
		    document sections.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str | None: Processed text value when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Remove Markdown image references, HTML image elements, and direct image URLs.
		
		Purpose:
		    Removes Markdown image syntax, HTML image tags, and direct image URLs from text. This
		    keeps descriptive text while excluding image-only references that do not support text
		    processing.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    str: Processed text value produced by the operation.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Encode text with a tiktoken tokenizer and return token identifiers as tabular data.
		
		Purpose:
		    Encodes lowercase text using the requested tiktoken encoding and returns token
		    identifiers in a pandas DataFrame. This supports token inspection and model-facing
		    preprocessing workflows.
		
		Args:
		    text (str): Text value to process.
		    encoding (str): Tiktoken encoding name used for tokenization.
		
		Returns:
		    DataFrame | None: Pandas DataFrame containing the processed output when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Split text into sentence strings using NLTK sentence tokenization.
		
		Purpose:
		    Applies NLTK sentence tokenization to lowercase text and returns the resulting sentence
		    list. This provides sentence boundaries for chunking, cleaning, and dataset generation
		    workflows.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    List[ str ] | None: List of processed text values when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Split a text file into page-sized text blocks.
		
		Purpose:
		    Reads a plain-text file and splits it into page-sized blocks using form-feed characters
		    when available or fixed line counts otherwise. The resulting list can be used for page-
		    level cleaning and analysis.
		
		Args:
		    filepath (str): Path to the local source file.
		    num (int): Number of lines used as the fallback page boundary.
		
		Returns:
		    List[ str ] | None: List of processed text values when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Read a text file and return paragraph-like text blocks as tabular data.
		
		Purpose:
		    Reads a text file and converts separated text blocks into a pandas DataFrame. The
		    fallback Latin-1 branch preserves the ability to process files that fail UTF-8 decoding.
		
		Args:
		    filepath (str): Path to the local source file.
		
		Returns:
		    DataFrame | None: Pandas DataFrame containing the processed output when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Build a word-frequency table from a token sequence.
		
		Purpose:
		    Counts token occurrences with NLTK frequency distribution support and returns a labeled
		    pandas DataFrame. The output provides a simple word-frequency table for analysis and
		    reporting.
		
		Args:
		    tokens (List[ str ]): Token sequence used by the processing operation.
		
		Returns:
		    DataFrame | None: Pandas DataFrame containing the processed output when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Extract the vocabulary column from a token-frequency table.
		
		Purpose:
		    Counts token occurrences and returns the unique token column as a pandas Series. This
		    gives downstream routines a vocabulary list derived from the active token stream.
		
		Args:
		    tokens (List[ str ]): Token sequence used by the processing operation.
		
		Returns:
		    Series | None: Pandas Series containing the processed output when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Build a bag-of-words table from a token sequence.
		
		Purpose:
		    Builds a bag-of-words representation by extracting unique terms from the token frequency
		    distribution. The returned DataFrame supports simple vocabulary inspection and feature
		    preparation.
		
		Args:
		    tokens (List[ str ]): Token sequence used by the processing operation.
		
		Returns:
		    DataFrame | None: Pandas DataFrame containing the processed output when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Create TF-IDF vectors for token values.
		
		Purpose:
		    Builds one-token documents, fits a TF-IDF vectorizer, and maps each token to its vector
		    representation. This supplies lightweight vector features for lexical comparison
		    workflows.
		
		Args:
		    tokens (List[ str ]): Token sequence used by the processing operation.
		
		Returns:
		    DataFrame | None: Pandas DataFrame containing the processed output when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Apply the standard Fonky text-cleaning pipeline to a single file.
		
		Purpose:
		    Runs a single file through the parser cleaning pipeline, including whitespace
		    normalization, encoding cleanup, symbol removal, fragment filtering, lemmatization, and
		    stop-word removal. The method returns the cleaned text instead of writing a file.
		
		Args:
		    filepath (str): Path to the local source file.
		
		Returns:
		    str | None: Processed text value when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Apply the standard Fonky text-cleaning pipeline to every file in a directory.
		
		Purpose:
		    Processes every file in a source directory through the standard cleaning pipeline and
		    writes cleaned text to a destination directory. This supports batch preparation of
		    corpora before chunking or dataset creation.
		
		Args:
		    source (str): Directory containing source text files.
		    destination (str): Directory where generated output files are written.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Split text files into sentence chunks and write chunked output files.
		
		Purpose:
		    Reads each file in a source directory, splits text into sentences, and writes the
		    resulting sentence sequence to matching output files. This prepares cleaned corpora for
		    chunk-based downstream workflows.
		
		Args:
		    source (str): Directory containing source text files.
		    destination (str): Directory where generated output files are written.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Chunk a single text file into fixed-size word groups represented as tabular data.
		
		Purpose:
		    Reads a single text file, filters recognized English alphabetic tokens, groups them into
		    fixed-size chunks, and returns the chunk rows as a DataFrame. This provides a compact
		    dataset-ready representation of token groups.
		
		Args:
		    filepath (str): Path to the local source file.
		    size (int): Maximum number of tokens or sentences grouped into each chunk.
		
		Returns:
		    DataFrame | None: Pandas DataFrame containing the processed output when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Clean and chunk a directory of text files into spreadsheet datasets.
		
		Purpose:
		    Processes all text files in a directory through cleaning, tokenization, fixed-size
		    chunking, and Excel export. This creates spreadsheet datasets suitable for review,
		    labeling, or later ingestion.
		
		Args:
		    source (str): Directory containing source text files.
		    destination (str): Directory where generated output files are written.
		    size (int): Maximum number of tokens or sentences grouped into each chunk.
		
		Returns:
		    DataFrame: Pandas DataFrame containing the processed output.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Convert text files into line-oriented JSON-like chunk output.
		
		Purpose:
		    Splits text files into fixed-size token groups and writes each group using a JSON-like
		    line-oriented representation. This supports quick conversion of raw text corpora into
		    chunked training or testing artifacts.
		
		Args:
		    source (str): Directory containing source text files.
		    destination (str): Directory where generated output files are written.
		    size (int): Maximum number of tokens or sentences grouped into each chunk.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Generate sentence-transformer embeddings for normalized token values.
		
		Purpose:
		    Lemmatizes token values and encodes them with a SentenceTransformer model. The returned
		    tuple pairs token text with a NumPy embedding matrix for semantic-search workflows.
		
		Args:
		    tokens (List[ str ]): Token sequence used by the processing operation.
		    model (str): Sentence-transformer model used to encode the query or token sequence.
		
		Returns:
		    Tuple[ List[ str ], np.ndarray ]: Token values paired with the generated embedding matrix.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Rank embedded tokens by semantic similarity to a query.
		
		Purpose:
		    Encodes the query with the supplied model, compares it with the embedding matrix using
		    cosine similarity, and returns the highest-scoring token matches. This supports
		    lightweight semantic retrieval over prepared token embeddings.
		
		Args:
		    query (str): Search text or semantic query submitted to the operation.
		    tokens (List[ str ]): Token sequence used by the processing operation.
		    embeddings (np.ndarray): Precomputed embedding matrix compared against the query vector.
		    model (SentenceTransformer): Sentence-transformer model used to encode the query or token sequence.
		    top (int): Maximum number of ranked semantic-search matches to return.
		
		Returns:
		    List[ tuple[ str, float ] ]: Ranked token and similarity-score pairs.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
	"""Run NLTK parsing operations.
	
	Purpose:
	    Wraps NLTK tokenization, stemming, lemmatization, part-of-speech tagging, named-entity
	    recognition, and token chunking routines. The class ensures required NLTK resources are
	    available and exposes parser methods that return structured token, sentence, tag, and
	    entity outputs.
	
	Attributes:
	    word_tokens (Optional[ List[ str ] ]): Word tokens produced by NLTK tokenization.
	    sentence_tokens (Optional[ List[ str ] ]): Sentence tokens produced by NLTK tokenization.
	    stemmed_tokens (Optional[ List[ str ] ]): Tokens produced by stemming.
	    lemmatized_tokens (Optional[ List[ str ] ]): Tokens produced by lemmatization.
	    tagged_tokens (Optional[ List[ Tuple[ str, str ] ] ]): Part-of-speech tagged token tuples.
	    named_entities (Optional[ List[ Tuple[ str, str ] ] ]): Named-entity text and label tuples."""
	word_tokens: Optional[ List[ str ] ]
	sentence_tokens: Optional[ List[ str ] ]
	stemmed_tokens: Optional[ List[ str ] ]
	lemmatized_tokens: Optional[ List[ str ] ]
	tagged_tokens: Optional[ List[ Tuple[ str, str ] ] ]
	named_entities: Optional[ List[ Tuple[ str, str ] ] ]
	
	def __init__( self ) -> None:
		"""  init  .
		
		Purpose:
		    Initializes NltkParser state used by later processing operations. The constructor
		    prepares reusable containers, helper objects, and default runtime values without
		    performing external document processing."""
		super( ).__init__( )
		self.initialize_resources( )
		self.word_tokens = [ ]
		self.sentence_tokens = [ ]
		self.stemmed_tokens = [ ]
		self.lemmatized_tokens = [ ]
		self.tagged_tokens = [ ]
		self.named_entities = [ ]
	
	def __dir__( self ) -> List[ str ] | None:
		"""Return the public attribute and method names exposed by the object.
		
		Purpose:
		    Returns a stable list of public attributes and methods for interactive inspection,
		    documentation, and UI discovery. The ordering groups state fields and callable
		    processing operations in a predictable way.
		
		Returns:
		    List[ str ] | None: List of processed text values when the operation succeeds."""
		return [ 'initialize_resources', 'word_tokenizer', 'sentence_tokenizer', 'word_stemmer',
		         'word_lemmatizer', 'pos_tagger', 'named_entity_recognition', 'word_tokens',
		         'sentence_tokens', 'stemmed_tokens', 'lemmatized_tokens', 'tagged_tokens',
		         'named_entities' ]
	
	def initialize_resources( self ) -> None:
		"""Ensure the NLTK corpora, tokenizers, taggers, and chunkers required by the parser are available.
		
		Purpose:
		    Checks for required NLTK resources and downloads missing packages. This prepares
		    tokenization, lemmatization, tagging, and named-entity recognition routines for use by
		    parser methods.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Tokenize text into lowercased word tokens.
		
		Purpose:
		    Lowercases text and tokenizes it into word tokens with NLTK. The resulting list is also
		    stored on the parser instance for reuse by later NLTK operations.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    List[ str ] | None: List of processed text values when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Tokenize text into lowercased sentence strings.
		
		Purpose:
		    Lowercases text and tokenizes it into sentence strings with NLTK. The resulting
		    sentences are stored on the parser instance and returned to the caller.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    List[ str ] | None: List of processed text values when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Stem lowercased word tokens with the configured Porter stemmer.
		
		Purpose:
		    Lowercases text, tokenizes it, and applies Porter stemming to each non-empty token. This
		    produces stemmed tokens for lexical normalization workflows.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    List[ str ] | None: List of processed text values when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Lemmatize lowercased word tokens with the configured WordNet lemmatizer.
		
		Purpose:
		    Lowercases text, tokenizes it, and applies WordNet lemmatization to each non-empty
		    token. This produces normalized lexical forms suitable for downstream analysis.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    List[ str ] | None: List of processed text values when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Assign part-of-speech tags to lowercased word tokens.
		
		Purpose:
		    Lowercases and tokenizes text, then assigns NLTK part-of-speech tags to each token. The
		    tagged sequence is stored on the instance and returned for syntactic analysis.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    List[ Tuple[ str, str ] ] | None: List of text and label tuples when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Extract named-entity text and entity labels from tagged tokens.
		
		Purpose:
		    Lowercases text, tokenizes and tags it, then applies NLTK named-entity chunking. Entity
		    text and labels are collected into tuples for downstream review or extraction workflows.
		
		Args:
		    text (str): Text value to process.
		
		Returns:
		    List[ Tuple[ str, str ] ] | None: List of text and label tuples when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Group word tokens into fixed-size chunks and return them as tabular data.
		
		Purpose:
		    Tokenizes lowercase text into words, groups the tokens into fixed-size chunks, and
		    returns a DataFrame of chunk strings. This provides a simple word-level chunking utility
		    for downstream vector or dataset generation.
		
		Args:
		    text (str): Text value to process.
		    size (int): Maximum number of tokens or sentences grouped into each chunk.
		
		Returns:
		    DataFrame | None: Pandas DataFrame containing the processed output when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
		"""Group sentence tokens into fixed-size chunks and return them as tabular data.
		
		Purpose:
		    Tokenizes lowercase text into sentences, groups the sentences into fixed-size chunks,
		    and returns a DataFrame of chunk strings. This provides a sentence-level chunking
		    utility for review or dataset preparation.
		
		Args:
		    text (str): Text value to process.
		    size (int): Maximum number of tokens or sentences grouped into each chunk.
		
		Returns:
		    DataFrame | None: Pandas DataFrame containing the processed output when the operation succeeds.
		
		Raises:
		    Error: Re-raised after the underlying exception is wrapped in the project error type."""
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
