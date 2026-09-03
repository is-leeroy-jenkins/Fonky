# Processing

## Normalize text

```python
from fonky.gemini.tools import preprocess_normalize_text

value = preprocess_normalize_text(
    text='  MULTIPLE    SPACES  ' )

print( value )
```

## Remove stopwords

```python
from fonky.gemini.tools import preprocess_remove_stopwords

value = preprocess_remove_stopwords(
    text='The analyst reviewed the report and the supporting data.' )

print( value )
```

## Split sentences

```python
from fonky.gemini.tools import preprocess_split_sentences

sentences = preprocess_split_sentences(
    text='Fonky loads documents. Fonky processes text.' )

print( sentences )
```

## Semantic search

```python
from fonky.gemini.tools import preprocess_semantic_search

matches = preprocess_semantic_search(
    query='federal spending',
    tokens=[
        'budget execution',
        'weather observations',
        'appropriations and obligations',
        'astronomy catalog',
        'outlay analysis',
    ],
    model='all-MiniLM-L6-v2',
    top=3 )

print( matches )
```

## NLTK

```python
from fonky.gemini.tools import nltk_named_entity_recognition
from fonky.gemini.tools import nltk_pos_tagger
from fonky.gemini.tools import nltk_word_lemmatizer
from fonky.gemini.tools import nltk_word_tokenizer

tokens = nltk_word_tokenizer(
    text='NASA operates the Goddard Space Flight Center.' )

lemmas = nltk_word_lemmatizer(
    text='cars studies running analyzed' )

tags = nltk_pos_tagger(
    text='The analyst reviewed the financial report.' )

entities = nltk_named_entity_recognition(
    text='NASA operates the Goddard Space Flight Center in Maryland.' )
```
