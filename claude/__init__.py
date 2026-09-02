'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                __init__.py
      Author:                  Terry D. Eppler
      Created:                 09-02-2026

      Last Modified By:        Terry D. Eppler
      Last Modified On:        09-02-2026
  ******************************************************************************************
  <summary>
    Initializes the Claude/Anthropic tool integration namespace.

    Purpose:
        Exposes Fonky's Claude/Anthropic AI-tool integration through the local ``tools`` module
        while keeping Anthropic-specific dependencies isolated from the root Fonky package.
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

from . import tools

__all__: list[ str ] = [
    'tools',
]
