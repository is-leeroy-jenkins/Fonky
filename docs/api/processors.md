# API Reference: `processors.py`

`processors.py` provides text-processing and parser classes. These are outside the current `fonky.py` wrapper scope.

## Module Inventory

- **Classes:** 3
- **Top-level functions:** 1

## Module-Level Functions

| Function | Signature | Purpose |
|---|---|---|
| `throw_if()` | `throw_if( name: str, value: object ) -> None` | Throw if. |

## Classes

| Class | Constructor | Public Methods | Functional Wrappers |
|---|---|---:|---:|
| [`Processor`](#processor) | `Processor( self: Any ) -> Any` | 0 | 0 |
| [`TextParser`](#textparser) | `TextParser( self: Any ) -> Any` | 32 | 0 |
| [`NltkParser`](#nltkparser) | `NltkParser( self: Any ) -> None` | 9 | 0 |

## `Processor`

Provide shared processor state.

```python
Processor( self: Any ) -> Any
```

**Source:** `processors.py`, line 183

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

## `TextParser`

Process and normalize text.

```python
TextParser( self: Any ) -> Any
```

**Source:** `processors.py`, line 281

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `load_text()` | `load_text( self: Any, filepath: str ) -> str \| None` | Read UTF-8 text from a local file and return the raw string. |
| `collapse_whitespace()` | `collapse_whitespace( self: Any, text: str ) -> str \| None` | Normalize spacing by lowercasing text and collapsing repeated whitespace. |
| `remove_punctuation()` | `remove_punctuation( self: Any, text: str ) -> str` | Strip punctuation from tokenized text while preserving word and spacing content. |
| `normalize_text()` | `normalize_text( self: Any, text: str ) -> str \| None` | Convert text to lowercase for stable downstream comparison and tokenization. |
| `remove_errors()` | `remove_errors( self: Any, text: str ) -> str` | Filter tokens against the NLTK English words corpus. |
| `remove_fragments()` | `remove_fragments( self: Any, text: str ) -> str \| None` | Remove very short token fragments from normalized text. |
| `remove_symbols()` | `remove_symbols( self: Any, text: str ) -> str \| None` | Remove configured symbol characters from normalized text. |
| `remove_html()` | `remove_html( self: Any, text: str ) -> str \| None` | Extract visible text from HTML markup. |
| `remove_xml()` | `remove_xml( self: Any, text: str ) -> str` | Extract inner text from XML-like markup while recovering malformed fragments when possible. |
| `remove_markdown()` | `remove_markdown( self: Any, text: str ) -> str \| None` | Remove common Markdown links, image syntax, and formatting markers. |
| `remove_stopwords()` | `remove_stopwords( self: Any, text: str ) -> str \| None` | Remove English stop words from tokenized text. |
| `remove_encodings()` | `remove_encodings( self: Any, text: str ) -> str \| None` | Resolve HTML entities, normalize Unicode characters, and remove control characters. |
| `remove_headers()` | `remove_headers( self: Any, filepath: str, lines: int = 50, headers: int = 3, footers: int = 3 ) -> str \| None` | Detect and remove repeated page headers and footers from a text file. |
| `remove_numbers()` | `remove_numbers( self: Any, text: str ) -> str \| None` | Remove decimal digits from text. |
| `remove_numerals()` | `remove_numerals( self: Any, text: str ) -> str \| None` | Remove Roman-numeral patterns from text. |
| `remove_images()` | `remove_images( self: Any, text: str ) -> str` | Remove Markdown image references, HTML image elements, and direct image URLs. |
| `tiktokenize()` | `tiktokenize( self: Any, text: str, encoding: str = 'cl100k_base' ) -> DataFrame \| None` | Encode text with a tiktoken tokenizer and return token identifiers as tabular data. |
| `split_sentences()` | `split_sentences( self: Any, text: str ) -> List[str] \| None` | Split text into sentence strings using NLTK sentence tokenization. |
| `split_pages()` | `split_pages( self: Any, filepath: str, num: int = 50 ) -> List[str] \| None` | Split a text file into page-sized text blocks. |
| `split_paragraphs()` | `split_paragraphs( self: Any, filepath: str ) -> DataFrame \| None` | Read a text file and return paragraph-like text blocks as tabular data. |
| `create_frequency_distribution()` | `create_frequency_distribution( self: Any, tokens: List[str] ) -> DataFrame \| None` | Build a word-frequency table from a token sequence. |
| `create_vocabulary()` | `create_vocabulary( self: Any, tokens: List[str] ) -> Series \| None` | Extract the vocabulary column from a token-frequency table. |
| `create_wordbag()` | `create_wordbag( self: Any, tokens: List[str] ) -> DataFrame \| None` | Build a bag-of-words table from a token sequence. |
| `create_vectors()` | `create_vectors( self: Any, tokens: List[str] ) -> DataFrame \| None` | Create TF-IDF vectors for token values. |
| `clean_file()` | `clean_file( self: Any, filepath: str ) -> str \| None` | Apply the standard Fonky text-cleaning pipeline to a single file. |
| `clean_files()` | `clean_files( self: Any, source: str, destination: str ) -> None` | Apply the standard Fonky text-cleaning pipeline to every file in a directory. |
| `chunk_files()` | `chunk_files( self: Any, source: str, destination: str ) -> None` | Split text files into sentence chunks and write chunked output files. |
| `chunk_data()` | `chunk_data( self: Any, filepath: str, size: int = 10 ) -> DataFrame \| None` | Chunk a single text file into fixed-size word groups represented as tabular data. |
| `chunk_datasets()` | `chunk_datasets( self: Any, source: str, destination: str, size: int = 10 ) -> DataFrame` | Clean and chunk a directory of text files into spreadsheet datasets. |
| `convert_jsonl()` | `convert_jsonl( self: Any, source: str, destination: str, size: int = 10 ) -> None` | Convert text files into line-oriented JSON-like chunk output. |
| `encode_sentences()` | `encode_sentences( self: Any, tokens: List[str], model: str = 'all-MiniLM-L6-v2' ) -> Tuple[List[str], np.ndarray]` | Generate sentence-transformer embeddings for normalized token values. |
| `semantic_search()` | `semantic_search( self: Any, query: str, tokens: List[str], embeddings: np.ndarray, model: SentenceTransformer, top: int = 5 ) -> List[tuple[str, float]]` | Rank embedded tokens by semantic similarity to a query. |

## `NltkParser`

Run NLTK parsing operations.

```python
NltkParser( self: Any ) -> None
```

**Source:** `processors.py`, line 1584

**Functional wrappers:** None. This class is infrastructure/base functionality or is not surfaced independently by the current functional API.

### Public Methods

| Method | Signature | Purpose |
|---|---|---|
| `initialize_resources()` | `initialize_resources( self: Any ) -> None` | Ensure the NLTK corpora, tokenizers, taggers, and chunkers required by the parser are available. |
| `word_tokenizer()` | `word_tokenizer( self: Any, text: str ) -> List[str] \| None` | Tokenize text into lowercased word tokens. |
| `sentence_tokenizer()` | `sentence_tokenizer( self: Any, text: str ) -> List[str] \| None` | Tokenize text into lowercased sentence strings. |
| `word_stemmer()` | `word_stemmer( self: Any, text: str ) -> List[str] \| None` | Stem lowercased word tokens with the configured Porter stemmer. |
| `word_lemmatizer()` | `word_lemmatizer( self: Any, text: str ) -> List[str] \| None` | Lemmatize lowercased word tokens with the configured WordNet lemmatizer. |
| `pos_tagger()` | `pos_tagger( self: Any, text: str ) -> List[Tuple[str, str]] \| None` | Assign part-of-speech tags to lowercased word tokens. |
| `named_entity_recognition()` | `named_entity_recognition( self: Any, text: str ) -> List[Tuple[str, str]] \| None` | Extract named-entity text and entity labels from tagged tokens. |
| `chunk_words()` | `chunk_words( self: Any, text: str, size: int = 5 ) -> DataFrame \| None` | Group word tokens into fixed-size chunks and return them as tabular data. |
| `chunk_sentences()` | `chunk_sentences( self: Any, text: str, size: int = 15 ) -> DataFrame \| None` | Group sentence tokens into fixed-size chunks and return them as tabular data. |
