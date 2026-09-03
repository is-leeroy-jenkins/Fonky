# Processing & NLP

**Tools:** 40

Examples use the Google ADK callable wrapper surface so each example is directly executable as ordinary Python.

## Tool Index

| Tool |
|---|
| [`nltk_chunk_sentences`](#nltk_chunk_sentences) |
| [`nltk_chunk_words`](#nltk_chunk_words) |
| [`nltk_named_entity_recognition`](#nltk_named_entity_recognition) |
| [`nltk_pos_tagger`](#nltk_pos_tagger) |
| [`nltk_sentence_tokenizer`](#nltk_sentence_tokenizer) |
| [`nltk_word_lemmatizer`](#nltk_word_lemmatizer) |
| [`nltk_word_stemmer`](#nltk_word_stemmer) |
| [`nltk_word_tokenizer`](#nltk_word_tokenizer) |
| [`preprocess_chunk_data`](#preprocess_chunk_data) |
| [`preprocess_chunk_datasets`](#preprocess_chunk_datasets) |
| [`preprocess_chunk_files`](#preprocess_chunk_files) |
| [`preprocess_clean_file`](#preprocess_clean_file) |
| [`preprocess_clean_files`](#preprocess_clean_files) |
| [`preprocess_collapse_whitespace`](#preprocess_collapse_whitespace) |
| [`preprocess_convert_jsonl`](#preprocess_convert_jsonl) |
| [`preprocess_create_frequency_distribution`](#preprocess_create_frequency_distribution) |
| [`preprocess_create_vectors`](#preprocess_create_vectors) |
| [`preprocess_create_vocabulary`](#preprocess_create_vocabulary) |
| [`preprocess_create_wordbag`](#preprocess_create_wordbag) |
| [`preprocess_encode_sentences`](#preprocess_encode_sentences) |
| [`preprocess_load_text`](#preprocess_load_text) |
| [`preprocess_normalize_text`](#preprocess_normalize_text) |
| [`preprocess_remove_encodings`](#preprocess_remove_encodings) |
| [`preprocess_remove_errors`](#preprocess_remove_errors) |
| [`preprocess_remove_fragments`](#preprocess_remove_fragments) |
| [`preprocess_remove_headers`](#preprocess_remove_headers) |
| [`preprocess_remove_html`](#preprocess_remove_html) |
| [`preprocess_remove_images`](#preprocess_remove_images) |
| [`preprocess_remove_markdown`](#preprocess_remove_markdown) |
| [`preprocess_remove_numbers`](#preprocess_remove_numbers) |
| [`preprocess_remove_numerals`](#preprocess_remove_numerals) |
| [`preprocess_remove_punctuation`](#preprocess_remove_punctuation) |
| [`preprocess_remove_stopwords`](#preprocess_remove_stopwords) |
| [`preprocess_remove_symbols`](#preprocess_remove_symbols) |
| [`preprocess_remove_xml`](#preprocess_remove_xml) |
| [`preprocess_semantic_search`](#preprocess_semantic_search) |
| [`preprocess_split_pages`](#preprocess_split_pages) |
| [`preprocess_split_paragraphs`](#preprocess_split_paragraphs) |
| [`preprocess_split_sentences`](#preprocess_split_sentences) |
| [`preprocess_tiktokenize`](#preprocess_tiktokenize) |

---

## `nltk_chunk_sentences`

Group sentence tokens into fixed-size chunks and return them as tabular data.

### Signature

```python
def nltk_chunk_sentences( text: str, size: int=15 ) -> DataFrame | None
```

### Purpose

Group sentence tokens into fixed-size chunks and return them as tabular data through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import nltk_chunk_sentences

result = nltk_chunk_sentences(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |
| `size` | `int` | Maximum size or group size used by the operation. |

### Returns

DataFrame | None: Value produced by the delegated Fonky implementation.

---

## `nltk_chunk_words`

Group word tokens into fixed-size chunks and return them as tabular data.

### Signature

```python
def nltk_chunk_words( text: str, size: int=5 ) -> DataFrame | None
```

### Purpose

Group word tokens into fixed-size chunks and return them as tabular data through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import nltk_chunk_words

result = nltk_chunk_words(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |
| `size` | `int` | Maximum size or group size used by the operation. |

### Returns

DataFrame | None: Value produced by the delegated Fonky implementation.

---

## `nltk_named_entity_recognition`

Extract named-entity text and entity labels from tagged tokens.

### Signature

```python
def nltk_named_entity_recognition( text: str ) -> List[Tuple[str, str]] | None
```

### Purpose

Extract named-entity text and entity labels from tagged tokens through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import nltk_named_entity_recognition

result = nltk_named_entity_recognition(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

List[Tuple[str, str]] | None: Value produced by the delegated Fonky implementation.

---

## `nltk_pos_tagger`

Assign part-of-speech tags to lowercased word tokens.

### Signature

```python
def nltk_pos_tagger( text: str ) -> List[Tuple[str, str]] | None
```

### Purpose

Assign part-of-speech tags to lowercased word tokens through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import nltk_pos_tagger

result = nltk_pos_tagger(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

List[Tuple[str, str]] | None: Value produced by the delegated Fonky implementation.

---

## `nltk_sentence_tokenizer`

Tokenize text into lowercased sentence strings.

### Signature

```python
def nltk_sentence_tokenizer( text: str ) -> List[str] | None
```

### Purpose

Tokenize text into lowercased sentence strings through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import nltk_sentence_tokenizer

result = nltk_sentence_tokenizer(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

List[str] | None: Value produced by the delegated Fonky implementation.

---

## `nltk_word_lemmatizer`

Lemmatize lowercased word tokens with the configured WordNet lemmatizer.

### Signature

```python
def nltk_word_lemmatizer( text: str ) -> List[str] | None
```

### Purpose

Lemmatize lowercased word tokens with the configured WordNet lemmatizer through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import nltk_word_lemmatizer

result = nltk_word_lemmatizer(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

List[str] | None: Value produced by the delegated Fonky implementation.

---

## `nltk_word_stemmer`

Stem lowercased word tokens with the configured Porter stemmer.

### Signature

```python
def nltk_word_stemmer( text: str ) -> List[str] | None
```

### Purpose

Stem lowercased word tokens with the configured Porter stemmer through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import nltk_word_stemmer

result = nltk_word_stemmer(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

List[str] | None: Value produced by the delegated Fonky implementation.

---

## `nltk_word_tokenizer`

Tokenize text into lowercased word tokens.

### Signature

```python
def nltk_word_tokenizer( text: str ) -> List[str] | None
```

### Purpose

Tokenize text into lowercased word tokens through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import nltk_word_tokenizer

result = nltk_word_tokenizer(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

List[str] | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_chunk_data`

Chunk a text file into fixed-size word groups represented as tabular data.

### Signature

```python
def preprocess_chunk_data( filepath: str, size: int=10 ) -> DataFrame | None
```

### Purpose

Chunk a text file into fixed-size word groups represented as tabular data through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_chunk_data

result = preprocess_chunk_data(
    filepath='data/input.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `filepath` | `str` | Local filesystem path used by the operation. |
| `size` | `int` | Maximum size or group size used by the operation. |

### Returns

DataFrame | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_chunk_datasets`

Clean and chunk a directory of text files into spreadsheet datasets.

### Signature

```python
def preprocess_chunk_datasets( source: str, destination: str, size: int=10 ) -> DataFrame
```

### Purpose

Clean and chunk a directory of text files into spreadsheet datasets through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_chunk_datasets

result = preprocess_chunk_datasets(
    source='data/input/',
    destination='output/' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `source` | `str` | Source value used to scope or identify the backing operation. |
| `destination` | `str` | Destination used to receive generated or processed output. |
| `size` | `int` | Maximum size or group size used by the operation. |

### Returns

DataFrame: Value produced by the delegated Fonky implementation.

---

## `preprocess_chunk_files`

Split text files into sentence chunks and write chunked output files.

### Signature

```python
def preprocess_chunk_files( source: str, destination: str ) -> None
```

### Purpose

Split text files into sentence chunks and write chunked output files through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_chunk_files

result = preprocess_chunk_files(
    source='data/input/',
    destination='output/' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `source` | `str` | Source value used to scope or identify the backing operation. |
| `destination` | `str` | Destination used to receive generated or processed output. |

### Returns

None: This function performs its work through the delegated implementation and does not return a value.

---

## `preprocess_clean_file`

Apply the standard Fonky text-cleaning pipeline to a single file.

### Signature

```python
def preprocess_clean_file( filepath: str ) -> str | None
```

### Purpose

Apply the standard Fonky text-cleaning pipeline to a single file through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_clean_file

result = preprocess_clean_file(
    filepath='data/input.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `filepath` | `str` | Local filesystem path used by the operation. |

### Returns

str | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_clean_files`

Apply the standard Fonky text-cleaning pipeline to every file in a directory.

### Signature

```python
def preprocess_clean_files( source: str, destination: str ) -> None
```

### Purpose

Apply the standard Fonky text-cleaning pipeline to every file in a directory through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_clean_files

result = preprocess_clean_files(
    source='data/input/',
    destination='output/' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `source` | `str` | Source value used to scope or identify the backing operation. |
| `destination` | `str` | Destination used to receive generated or processed output. |

### Returns

None: This function performs its work through the delegated implementation and does not return a value.

---

## `preprocess_collapse_whitespace`

Normalize spacing by lowercasing text and collapsing repeated whitespace.

### Signature

```python
def preprocess_collapse_whitespace( text: str ) -> str | None
```

### Purpose

Normalize spacing by lowercasing text and collapsing repeated whitespace through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_collapse_whitespace

result = preprocess_collapse_whitespace(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_convert_jsonl`

Convert text files into line-oriented JSON-like chunk output.

### Signature

```python
def preprocess_convert_jsonl( source: str, destination: str, size: int=10 ) -> None
```

### Purpose

Convert text files into line-oriented JSON-like chunk output through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_convert_jsonl

result = preprocess_convert_jsonl(
    source='data/input/',
    destination='output/' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `source` | `str` | Source value used to scope or identify the backing operation. |
| `destination` | `str` | Destination used to receive generated or processed output. |
| `size` | `int` | Maximum size or group size used by the operation. |

### Returns

None: This function performs its work through the delegated implementation and does not return a value.

---

## `preprocess_create_frequency_distribution`

Build a word-frequency table from a token sequence.

### Signature

```python
def preprocess_create_frequency_distribution( tokens: List[str] ) -> DataFrame | None
```

### Purpose

Build a word-frequency table from a token sequence through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_create_frequency_distribution

result = preprocess_create_frequency_distribution(
    tokens=['budget', 'obligations', 'outlays'] )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `tokens` | `List[str]` | Token values processed by the operation. |

### Returns

DataFrame | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_create_vectors`

Create TF-IDF vectors for token values.

### Signature

```python
def preprocess_create_vectors( tokens: List[str] ) -> DataFrame | None
```

### Purpose

Create TF-IDF vectors for token values through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_create_vectors

result = preprocess_create_vectors(
    tokens=['budget', 'obligations', 'outlays'] )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `tokens` | `List[str]` | Token values processed by the operation. |

### Returns

DataFrame | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_create_vocabulary`

Extract the vocabulary column from a token-frequency table.

### Signature

```python
def preprocess_create_vocabulary( tokens: List[str] ) -> Series | None
```

### Purpose

Extract the vocabulary column from a token-frequency table through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_create_vocabulary

result = preprocess_create_vocabulary(
    tokens=['budget', 'obligations', 'outlays'] )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `tokens` | `List[str]` | Token values processed by the operation. |

### Returns

Series | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_create_wordbag`

Build a bag-of-words table from a token sequence.

### Signature

```python
def preprocess_create_wordbag( tokens: List[str] ) -> DataFrame | None
```

### Purpose

Build a bag-of-words table from a token sequence through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_create_wordbag

result = preprocess_create_wordbag(
    tokens=['budget', 'obligations', 'outlays'] )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `tokens` | `List[str]` | Token values processed by the operation. |

### Returns

DataFrame | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_encode_sentences`

Generate sentence-transformer embeddings for normalized token values.

### Signature

```python
def preprocess_encode_sentences( tokens: List[str], model: str='all-MiniLM-L6-v2' ) -> Tuple[List[str], np.ndarray]
```

### Purpose

Generate sentence-transformer embeddings for normalized token values through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_encode_sentences

result = preprocess_encode_sentences(
    tokens=['budget', 'obligations', 'outlays'] )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `tokens` | `List[str]` | Token values processed by the operation. |
| `model` | `str` | Model identifier used by the operation. |

### Returns

Tuple[List[str], np.ndarray]: Value produced by the delegated Fonky implementation.

---

## `preprocess_load_text`

Read UTF-8 text from a local file and return the raw string.

### Signature

```python
def preprocess_load_text( filepath: str ) -> str | None
```

### Purpose

Read UTF-8 text from a local file and return the raw string through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_load_text

result = preprocess_load_text(
    filepath='data/input.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `filepath` | `str` | Local filesystem path used by the operation. |

### Returns

str | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_normalize_text`

Convert text to lowercase for stable comparison and tokenization.

### Signature

```python
def preprocess_normalize_text( text: str ) -> str | None
```

### Purpose

Convert text to lowercase for stable comparison and tokenization through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_normalize_text

result = preprocess_normalize_text(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_remove_encodings`

Resolve HTML entities, normalize Unicode characters, and remove control characters.

### Signature

```python
def preprocess_remove_encodings( text: str ) -> str | None
```

### Purpose

Resolve HTML entities, normalize Unicode characters, and remove control characters through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_remove_encodings

result = preprocess_remove_encodings(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_remove_errors`

Filter tokens against the NLTK English words corpus.

### Signature

```python
def preprocess_remove_errors( text: str ) -> str
```

### Purpose

Filter tokens against the NLTK English words corpus through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_remove_errors

result = preprocess_remove_errors(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str: Value produced by the delegated Fonky implementation.

---

## `preprocess_remove_fragments`

Remove very short token fragments from normalized text.

### Signature

```python
def preprocess_remove_fragments( text: str ) -> str | None
```

### Purpose

Remove very short token fragments from normalized text through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_remove_fragments

result = preprocess_remove_fragments(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_remove_headers`

Detect and remove repeated page headers and footers from a text file.

### Signature

```python
def preprocess_remove_headers( filepath: str, lines: int=50, headers: int=3, footers: int=3 ) -> str | None
```

### Purpose

Detect and remove repeated page headers and footers from a text file through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_remove_headers

result = preprocess_remove_headers(
    filepath='data/input.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `filepath` | `str` | Local filesystem path used by the operation. |
| `lines` | `int` | Lines value used by the operation. |
| `headers` | `int` | Headers value used by the operation. |
| `footers` | `int` | Footers value used by the operation. |

### Returns

str | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_remove_html`

Extract visible text from HTML markup.

### Signature

```python
def preprocess_remove_html( text: str ) -> str | None
```

### Purpose

Extract visible text from HTML markup through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_remove_html

result = preprocess_remove_html(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_remove_images`

Remove Markdown image references, HTML image elements, and direct image URLs.

### Signature

```python
def preprocess_remove_images( text: str ) -> str
```

### Purpose

Remove Markdown image references, HTML image elements, and direct image URLs through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_remove_images

result = preprocess_remove_images(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str: Value produced by the delegated Fonky implementation.

---

## `preprocess_remove_markdown`

Remove common Markdown links, image syntax, and formatting markers.

### Signature

```python
def preprocess_remove_markdown( text: str ) -> str | None
```

### Purpose

Remove common Markdown links, image syntax, and formatting markers through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_remove_markdown

result = preprocess_remove_markdown(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_remove_numbers`

Remove decimal digits from text.

### Signature

```python
def preprocess_remove_numbers( text: str ) -> str | None
```

### Purpose

Remove decimal digits from text through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_remove_numbers

result = preprocess_remove_numbers(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_remove_numerals`

Remove Roman-numeral patterns from text.

### Signature

```python
def preprocess_remove_numerals( text: str ) -> str | None
```

### Purpose

Remove Roman-numeral patterns from text through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_remove_numerals

result = preprocess_remove_numerals(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_remove_punctuation`

Strip punctuation from tokenized text.

### Signature

```python
def preprocess_remove_punctuation( text: str ) -> str
```

### Purpose

Strip punctuation from tokenized text through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_remove_punctuation

result = preprocess_remove_punctuation(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str: Value produced by the delegated Fonky implementation.

---

## `preprocess_remove_stopwords`

Remove English stop words from tokenized text.

### Signature

```python
def preprocess_remove_stopwords( text: str ) -> str | None
```

### Purpose

Remove English stop words from tokenized text through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_remove_stopwords

result = preprocess_remove_stopwords(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_remove_symbols`

Remove configured symbol characters from normalized text.

### Signature

```python
def preprocess_remove_symbols( text: str ) -> str | None
```

### Purpose

Remove configured symbol characters from normalized text through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_remove_symbols

result = preprocess_remove_symbols(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_remove_xml`

Extract inner text from XML-like markup.

### Signature

```python
def preprocess_remove_xml( text: str ) -> str
```

### Purpose

Extract inner text from XML-like markup through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_remove_xml

result = preprocess_remove_xml(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

str: Value produced by the delegated Fonky implementation.

---

## `preprocess_semantic_search`

Search token content by semantic similarity.

### Signature

```python
def preprocess_semantic_search( query: str, tokens: List[str], model: str='all-MiniLM-L6-v2', top: int=5 ) -> List[Tuple[str, float]]
```

### Purpose

Search token content by semantic similarity through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_semantic_search

result = preprocess_semantic_search(
    query='federal spending',
    tokens=['budget', 'obligations', 'outlays'] )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `query` | `str` | Search query or natural-language request submitted to the backing operation. |
| `tokens` | `List[str]` | Token values processed by the operation. |
| `model` | `str` | Model identifier used by the operation. |
| `top` | `int` | Top value used by the operation. |

### Returns

List[Tuple[str, float]]: Value produced by the delegated Fonky implementation.

---

## `preprocess_split_pages`

Split a text file into page-sized text blocks.

### Signature

```python
def preprocess_split_pages( filepath: str, num: int=50 ) -> List[str] | None
```

### Purpose

Split a text file into page-sized text blocks through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_split_pages

result = preprocess_split_pages(
    filepath='data/input.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `filepath` | `str` | Local filesystem path used by the operation. |
| `num` | `int` | Num value used by the operation. |

### Returns

List[str] | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_split_paragraphs`

Read a text file and return paragraph-like text blocks as tabular data.

### Signature

```python
def preprocess_split_paragraphs( filepath: str ) -> DataFrame | None
```

### Purpose

Read a text file and return paragraph-like text blocks as tabular data through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_split_paragraphs

result = preprocess_split_paragraphs(
    filepath='data/input.txt' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `filepath` | `str` | Local filesystem path used by the operation. |

### Returns

DataFrame | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_split_sentences`

Split text into sentence strings using NLTK sentence tokenization.

### Signature

```python
def preprocess_split_sentences( text: str ) -> List[str] | None
```

### Purpose

Split text into sentence strings using NLTK sentence tokenization through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_split_sentences

result = preprocess_split_sentences(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |

### Returns

List[str] | None: Value produced by the delegated Fonky implementation.

---

## `preprocess_tiktokenize`

Encode text with a tiktoken tokenizer and return token identifiers as tabular data.

### Signature

```python
def preprocess_tiktokenize( text: str, encoding: str='cl100k_base' ) -> DataFrame | None
```

### Purpose

Encode text with a tiktoken tokenizer and return token identifiers as tabular data through Fonky's canonical implementation so the callable can be registered directly with a Google ADK Agent through its ``tools`` collection.

### Example

```python
from fonky.gemini.tools import preprocess_tiktokenize

result = preprocess_tiktokenize(
    text='Fonky provides reusable AI tools.' )

print( result )
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `text` | `str` | Text value processed by the operation. |
| `encoding` | `str` | Text encoding or tokenizer encoding used by the operation. |

### Returns

DataFrame | None: Value produced by the delegated Fonky implementation.

---
