# Loading

## Text

```python
from fonky.gemini.tools import load_text

documents = load_text(
    path='data/sample.txt',
    encoding='utf-8' )

print( documents )
```

## PDF

```python
from fonky.gemini.tools import load_pdf

documents = load_pdf(
    path='data/report.pdf',
    mode='single',
    extract='plain',
    include=False,
    format='markdown-img' )

print( documents )
```

## Word

```python
from fonky.gemini.tools import load_word

documents = load_word(
    path='data/report.docx' )

print( documents )
```

## CSV

```python
from fonky.gemini.tools import load_csv

documents = load_csv(
    path='data/sample.csv' )

print( documents )
```

## Excel

```python
from fonky.gemini.tools import load_excel

documents = load_excel(
    path='data/sample.xlsx' )

print( documents )
```

## JSON

```python
from fonky.gemini.tools import load_json

documents = load_json(
    path='data/sample.json' )

print( documents )
```
