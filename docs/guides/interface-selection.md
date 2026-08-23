# Choosing Functional vs Class Usage

## Use `fonky.py` When

- one call completes the operation;
- you want the simplest typed interface;
- shared instance state is unnecessary;
- you are integrating Fonky into an application, notebook, API, or future Tool layer.

## Use the Implementation Class When

- multiple operations must share state;
- you need helper/validation methods not exposed as wrappers;
- you are debugging or extending the provider;
- you need to inspect internal documents or provider state.

## Example — One-Shot Functional Call

```python
from fonky import fonky

documents = fonky.load_text(
    path='notes.txt',
    encoding='utf-8'
)
```

## Example — Stateful Loader

```python
from fonky.loaders import TextLoader

loader = TextLoader()
documents = loader.load(
    path='notes.txt',
    encoding='utf-8'
)

# Continue with loader-specific stateful operations on the same object when required.
```
