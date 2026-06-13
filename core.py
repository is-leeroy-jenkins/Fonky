'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                core.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="core.py" company="Terry D. Eppler">

	     core.py
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
    Provides shared core utilities and response containers for Fonky.

    Purpose:
        Defines lightweight primitives used by Fonky fetchers, scrapers, loaders, and
        downstream adapters. The module provides a common argument guard and a canonical
        Result container for normalizing HTTP response metadata into a stable object that
        can be inspected, serialized, and passed between service-layer components.
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations
from typing import Dict, Optional, Any
from requests import Response

def throw_if( name: str, value: object ) -> None:
	"""Validate a required value.

	Purpose:
		Provides a lightweight guard for required arguments used by core and service-layer
		components. The function raises a clear ``ValueError`` when a required value is
		``None`` so callers fail early before attempting provider calls, response handling,
		or serialization work.

	Args:
		name (str): Human-readable argument name included in the raised error message.
		value (object): Value to validate.

	Raises:
		ValueError: Raised when ``value`` is ``None``.
	"""
	if value is None:
		raise ValueError( f'Argument "{name}" cannot be None' )

class Result( ):
	"""Represent the result of an HTTP response.

	Purpose:
		Stores the key fields from a ``requests.Response`` object in a small, stable
		container used by Fonky fetchers and scrapers. The class preserves the original
		response while exposing commonly inspected values such as URL, status code, text,
		encoding, and headers for serialization and downstream processing.

	Attributes:
		url (str | None): Final URL associated with the response.
		status_code (int | None): HTTP status code returned by the request.
		text (str | None): Response body text.
		encoding (str | None): Response encoding reported by ``requests``.
		headers (str | None): Response headers captured from the response object.
		response (Response | None): Original ``requests.Response`` object.
	"""
	url: Optional[ str ]
	status_code: Optional[ int ]
	text: Optional[ str ]
	encoding: Optional[ str ]
	headers: Optional[ str ]
	response: Optional[ Response ]
	
	def __init__( self, response: Response ) -> None:
		"""Initialize the response result.

		Purpose:
			Captures the important response fields from a ``requests.Response`` instance and
			retains the original response for callers that need access to provider-specific
			metadata or raw response behavior.

		Args:
			response (Response): Response object returned by the ``requests`` library.
		"""
		self.response = response
		self.url = response.url
		self.status_code = response.status_code
		self.text = response.text
		self.encoding = response.encoding
		self.headers = response.headers
	
	def __dir__( self ) -> list[ str ]:
		"""Return inspectable member names.

		Purpose:
			Provides a stable ordering of public attributes and helper members used by
			interactive sessions, documentation tools, user-interface inspectors, and tests.

		Returns:
			Ordered member names exposed by the result container.
		"""
		return [ 'url',
		         'status_code',
		         'text',
		         'encoding',
		         'headers',
		         'has_html',
		         'to_dict',
		         'from_response' ]
	
	def to_dict( self ) -> Dict[ str, Any ]:
		"""Convert the result to a dictionary.

		Purpose:
			Produces a plain dictionary representation of the response result for JSON-style
			serialization, testing, logging, or adapter output. Header values are copied into a
			new dictionary so downstream callers do not mutate the original response headers.

		Returns:
			Dictionary containing the URL, status code, text, encoding, and copied headers.
		"""
		return \
			{
					'url': self.url,
					'status_code': self.status_code,
					'text': self.text,
					'encoding': self.encoding,
					'headers': dict( self.headers ),
			}
	
	@property
	def has_html( self ) -> bool:
		"""Indicate whether response text is available.

		Purpose:
			Reports whether the stored response text is represented as a string. This property
			provides a small compatibility flag for callers that need to decide whether text
			extraction or HTML-oriented processing can proceed.

		Returns:
			``True`` when ``text`` is a string; otherwise ``False``.
		"""
		return isinstance( self.text, str )