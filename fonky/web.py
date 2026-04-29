'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                web.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="web.py" company="Terry D. Eppler">

	     web.py
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
    web.py
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

from fonky.fetchers import Fetcher
from fonky.fetchers import WebCrawler
from fonky.fetchers import WebFetcher
from fonky.fetchers import encode_image
from fonky.loaders import ArXivLoader
from fonky.loaders import GithubLoader
from fonky.loaders import OpenCityLoader
from fonky.loaders import PubMedSearchLoader
from fonky.loaders import WebLoader
from fonky.loaders import WikiLoader
from fonky.scrapers import Extractor
from fonky.scrapers import WebExtractor

# ==========================================================================================
# PUBLIC EXPORTS
# ==========================================================================================

__all__: list[ str ] = [
		'ArXivLoader',
		'Extractor',
		'Fetcher',
		'GithubLoader',
		'OpenCityLoader',
		'PubMedSearchLoader',
		'WebCrawler',
		'WebExtractor',
		'WebFetcher',
		'WebLoader',
		'WikiLoader',
		'encode_image',
]