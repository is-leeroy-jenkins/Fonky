'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                __init__.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        08-31-2026
  ******************************************************************************************
  <summary>
    Initializes the Fonky package namespace.

    Purpose:
        Defines package metadata for the consolidated Fonky package. Implementation classes remain
        available from their owning modules, while OpenAI Agents SDK function tools are exposed
        explicitly through ``fonky.tools`` to avoid eager initialization of the tool layer.
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

__author__: str = 'Terry D. Eppler'
__copyright__: str = 'Copyright © 2026 Terry Eppler'
__description__: str = 'Data fetching, loading, scraping, preprocessing, and agent-tool framework.'
__email__: str = 'terryeppler@gmail.com'
__license__: str = 'MIT'
__package_name__: str = 'fonky'
__version__: str = '0.1.0'

__all__: list[ str ] = [ ]
