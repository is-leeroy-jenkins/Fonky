'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                environmental.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="environmental.py" company="Terry D. Eppler">

	     environmental.py
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
    environmental.py
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

from fonky.fetchers import AirNow
from fonky.fetchers import ClimateData
from fonky.fetchers import EarthObservatory
from fonky.fetchers import EnviroFacts
from fonky.fetchers import EoNet
from fonky.fetchers import Firms
from fonky.fetchers import GoogleWeather
from fonky.fetchers import HistoricalWeather
from fonky.fetchers import OpenAQ
from fonky.fetchers import OpenWeather
from fonky.fetchers import PurpleAir
from fonky.fetchers import TidesAndCurrents
from fonky.fetchers import USGSEarthquakes
from fonky.fetchers import USGSWaterData
from fonky.fetchers import UvIndex

# ==========================================================================================
# PUBLIC EXPORTS
# ==========================================================================================

__all__: list[ str ] = [
		'AirNow',
		'ClimateData',
		'EarthObservatory',
		'EnviroFacts',
		'EoNet',
		'Firms',
		'GoogleWeather',
		'HistoricalWeather',
		'OpenAQ',
		'OpenWeather',
		'PurpleAir',
		'TidesAndCurrents',
		'USGSEarthquakes',
		'USGSWaterData',
		'UvIndex',
]