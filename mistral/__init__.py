'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                __init__.py
      Author:                  Terry D. Eppler
      Created:                 09-03-2026

      Last Modified By:        Terry D. Eppler
      Last Modified On:        09-03-2026
  ******************************************************************************************
  <summary>
    Initializes the Mistral AI tool integration namespace.

    Purpose:
        Exposes Fonky's Mistral AI-tool integration through the local ``tools`` module while
        keeping provider-specific dependencies isolated from the root Fonky package.
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

from . import tools

__all__: list[ str ] = [
    'tools',
]
