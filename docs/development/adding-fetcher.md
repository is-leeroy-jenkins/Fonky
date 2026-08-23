# Adding a Fetcher

A fetcher owns endpoint construction, authentication inputs, validation, HTTP behavior, provider parsing, response shaping, and provider-specific failure handling. Do not move those responsibilities into `fonky.py`.
