'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                documents.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="documents.py" company="Terry D. Eppler">

	     documents.py
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
    documents.py
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

from fonky.loaders import CsvLoader
from fonky.loaders import EmailLoader
from fonky.loaders import ExcelLoader
from fonky.loaders import HtmlLoader
from fonky.loaders import JsonLoader
from fonky.loaders import JupyterNotebookLoader
from fonky.loaders import Loader
from fonky.loaders import MarkdownLoader
from fonky.loaders import OutlookLoader
from fonky.loaders import PdfLoader
from fonky.loaders import PdfReader
from fonky.loaders import PowerPointLoader
from fonky.loaders import SpfxLoader
from fonky.loaders import TextLoader
from fonky.loaders import WordLoader
from fonky.loaders import XmlLoader

# ==========================================================================================
# PUBLIC EXPORTS
# ==========================================================================================

__all__: list[ str ] = [
		'CsvLoader',
		'EmailLoader',
		'ExcelLoader',
		'HtmlLoader',
		'JsonLoader',
		'JupyterNotebookLoader',
		'Loader',
		'MarkdownLoader',
		'OutlookLoader',
		'PdfLoader',
		'PdfReader',
		'PowerPointLoader',
		'SpfxLoader',
		'TextLoader',
		'WordLoader',
		'XmlLoader',
]