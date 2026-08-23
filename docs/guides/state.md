# Stateful vs Functional Usage

Functional wrappers create fresh implementation instances. This is ideal for one-shot calls.

Use direct classes when:

- a later method depends on documents loaded earlier;
- you need to inspect response or provider state;
- you need class helper methods not exposed by `fonky.py`;
- you are debugging or extending an integration.
