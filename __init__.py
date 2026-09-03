'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                __init__.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        09-01-2026
  ******************************************************************************************
  <summary>
    Initializes the Fonky package namespace.

    Purpose:
        Defines package metadata for Fonky. Core fetching, loading, scraping, processing, and
        model functionality remains available from its owning modules. AI tool integrations are
        exposed explicitly through the ``gpt``, ``gemini``, ``grok``, and ``langchain``
        subpackages so importing the core package does not eagerly initialize provider tool SDKs.
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

__author__: str = 'Terry D. Eppler'
__copyright__: str = 'Copyright © 2026 Terry Eppler'
__description__: str = 'Data fetching, loading, scraping, processing, and AI-tool framework.'
__email__: str = 'terryeppler@gmail.com'
__license__: str = 'MIT'
__package_name__: str = 'fonky'
__version__: str = '0.1.0'

__all__: list[ str ] = [ ]
