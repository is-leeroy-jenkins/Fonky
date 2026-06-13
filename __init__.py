'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                __init__.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="__init__.py" company="Terry D. Eppler">

	     __init__.py
	     Copyright ©  2026  Terry Eppler

     Permission is hereby granted, free of charge, to any person obtaining a copy
     of this software and associated documentation files (the “Software”),
     to deal in the Software without restriction,
     including without limitation the rights to use,
     copy, modify, merge, publish, distribute, sublicense,
     and/or sell copies of the Software,
     and to permit persons to whom the Software is furnished to do so,
     subject to the following conditions:

     The above copyright notice and this permission notice shall be included in all
     copies or substantial portions of the Software.

     THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
     INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT.
     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
     DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
     ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
     DEALINGS IN THE SOFTWARE.

     You can contact me at:  terryeppler@gmail.com or eppler.terry@epa.gov

  </copyright>
  <summary>
    Initializes the public Fonky package namespace.

    Purpose:
        Defines package metadata and lazily exposes Fonky category modules for archive,
        astronomy, cloud, demographic, document, environmental, geospatial, health, and web
        workflows. The lazy import mechanism keeps package import lightweight while preserving
        stable top-level access to public module groups.

    Notes:
        The former ``collections`` public module has been renamed to ``archives`` to avoid a
        naming conflict with Python's standard-library ``collections`` module.
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

import importlib
from types import ModuleType
from typing import List

# ==========================================================================================
# PACKAGE METADATA
# ==========================================================================================

__author__: str = 'Terry D. Eppler'
__copyright__: str = 'Copyright © 2026 Terry Eppler'
__description__: str = 'Data fetching, loading, scraping, and processing framework.'
__email__: str = 'terryeppler@gmail.com'
__license__: str = 'MIT'
__package_name__: str = 'fonky'
__version__: str = '0.1.0'

# ==========================================================================================
# LAZY MODULE EXPORTS
# ==========================================================================================

_MODULES: List[ str ] = [
		'archives',
		'astronomical',
		'cloud',
		'demographic',
		'documents',
		'environmental',
		'geospatial',
		'health',
		'web',
]

def __getattr__( name: str ) -> ModuleType:
	"""Lazily import a public Fonky category module.

	Purpose:
		Imports an approved public module only when it is first accessed from the package
		namespace. This keeps the initial ``import fonky`` operation lightweight while still
		supporting stable top-level access such as ``fonky.web`` and ``fonky.archives``.

	Args:
		name (str): Requested package attribute name.

	Returns:
		Imported public Fonky category module.

	Raises:
		AttributeError: Raised when ``name`` is not an approved public module.
	"""
	if name in _MODULES:
		return importlib.import_module( f'fonky.{name}' )
	
	raise AttributeError( f'module "fonky" has no attribute "{name}"' )

def __dir__( ) -> List[ str ]:
	"""Return package-level names for inspection.

	Purpose:
		Combines the package globals with lazily exposed category modules so interactive
		inspection, auto-complete, documentation tools, and debuggers can discover the public
		Fonky namespace consistently.

	Returns:
		Sorted package-level names available for inspection.
	"""
	return sorted( list( globals( ).keys( ) ) + _MODULES )

# ==========================================================================================
# PUBLIC EXPORTS
# ==========================================================================================

__all__: List[ str ] = [
		'archives',
		'astronomical',
		'cloud',
		'demographic',
		'documents',
		'environmental',
		'geospatial',
		'health',
		'web', ]