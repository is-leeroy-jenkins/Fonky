'''
  ******************************************************************************************
      Assembly:                fonky
      Filename:                serializers.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="serializers.py" company="Terry D. Eppler">

	     serializers.py
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
    serializers.py
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence
from uuid import UUID

import numpy as np
import pandas as pd
from pydantic import BaseModel
from requests import Response

from fonky.core import Result

# ==========================================================================================
# GUARDS
# ==========================================================================================

def throw_if( name: str, value: object ) -> None:
	'''

		Purpose:
		--------
		Validate a required argument and raise a ValueError when the supplied value is None
		or an empty string.

		Parameters:
		-----------
		name (str): Name of the argument being validated.
		value (object): Value being validated.

		Returns:
		--------
		None

	'''
	if value is None:
		raise ValueError( f'Argument "{name}" cannot be None.' )
	
	if isinstance( value, str ) and not value.strip( ):
		raise ValueError( f'Argument "{name}" cannot be empty.' )

# ==========================================================================================
# SERIALIZATION HELPERS
# ==========================================================================================

def serialize_datetime( value: date | datetime ) -> str:
	'''

		Purpose:
		--------
		Convert a date or datetime object into an ISO-8601 string.

		Parameters:
		-----------
		value (date | datetime): Date-like value to serialize.

		Returns:
		--------
		str: ISO-8601 formatted string.

	'''
	throw_if( 'value', value )
	return value.isoformat( )

def serialize_path( value: Path ) -> str:
	'''

		Purpose:
		--------
		Convert a pathlib.Path instance into a string path.

		Parameters:
		-----------
		value (Path): Path object to serialize.

		Returns:
		--------
		str: String representation of the path.

	'''
	throw_if( 'value', value )
	return str( value )

def serialize_enum( value: Enum ) -> Any:
	'''

		Purpose:
		--------
		Convert an Enum instance into its JSON-safe value.

		Parameters:
		-----------
		value (Enum): Enum value to serialize.

		Returns:
		--------
		Any: Enum value.

	'''
	throw_if( 'value', value )
	return value.value

def serialize_decimal( value: Decimal ) -> float:
	'''

		Purpose:
		--------
		Convert a Decimal instance into a JSON-safe floating-point value.

		Parameters:
		-----------
		value (Decimal): Decimal value to serialize.

		Returns:
		--------
		float: Floating-point representation.

	'''
	throw_if( 'value', value )
	return float( value )

def serialize_uuid( value: UUID ) -> str:
	'''

		Purpose:
		--------
		Convert a UUID instance into a string.

		Parameters:
		-----------
		value (UUID): UUID value to serialize.

		Returns:
		--------
		str: String UUID.

	'''
	throw_if( 'value', value )
	return str( value )

def serialize_numpy_value( value: Any ) -> Any:
	'''

		Purpose:
		--------
		Convert NumPy scalar and array values into JSON-safe Python values.

		Parameters:
		-----------
		value (Any): NumPy value, scalar, array, or non-NumPy fallback value.

		Returns:
		--------
		Any: JSON-safe Python value.

	'''
	if isinstance( value, np.ndarray ):
		return value.tolist( )
	
	if isinstance( value, np.generic ):
		return value.item( )
	
	return value

def serialize_dataframe( df_data: pd.DataFrame ) -> Dict[ str, Any ]:
	'''

		Purpose:
		--------
		Convert a pandas DataFrame into a JSON-safe dictionary while preserving columns,
		row count, and record-oriented data.

		Parameters:
		-----------
		df_data (pd.DataFrame): DataFrame to serialize.

		Returns:
		--------
		Dict[str, Any]: JSON-safe DataFrame payload.

	'''
	throw_if( 'df_data', df_data )
	
	df_clean = df_data.replace( { np.nan: None } )
	return {
			'type': 'dataframe',
			'columns': list( df_clean.columns ),
			'rows': int( len( df_clean ) ),
			'data': df_clean.to_dict( orient='records' ),
	}

def serialize_series( series: pd.Series ) -> Dict[ str, Any ]:
	'''

		Purpose:
		--------
		Convert a pandas Series into a JSON-safe dictionary.

		Parameters:
		-----------
		series (pd.Series): Series to serialize.

		Returns:
		--------
		Dict[str, Any]: JSON-safe Series payload.

	'''
	throw_if( 'series', series )
	
	clean = series.replace( { np.nan: None } )
	return {
			'type': 'series',
			'name': clean.name,
			'length': int( len( clean ) ),
			'data': clean.tolist( ),
	}

def serialize_pydantic_model( model: BaseModel ) -> Dict[ str, Any ]:
	'''

		Purpose:
		--------
		Convert a Pydantic model into a JSON-safe dictionary.

		Parameters:
		-----------
		model (BaseModel): Pydantic model instance to serialize.

		Returns:
		--------
		Dict[str, Any]: JSON-safe model payload.

	'''
	throw_if( 'model', model )
	return serialize_value( model.model_dump( mode='json' ) )

def serialize_response( response: Response ) -> Dict[ str, Any ]:
	'''

		Purpose:
		--------
		Convert a requests.Response object into a JSON-safe dictionary.

		Parameters:
		-----------
		response (Response): HTTP response to serialize.

		Returns:
		--------
		Dict[str, Any]: JSON-safe response payload.

	'''
	throw_if( 'response', response )
	
	return {
			'type': 'response',
			'url': response.url,
			'status_code': response.status_code,
			'encoding': response.encoding,
			'headers': dict( response.headers ),
			'text': response.text,
			'ok': response.ok,
			'reason': response.reason,
	}

def serialize_result( result: Result ) -> Dict[ str, Any ]:
	'''

		Purpose:
		--------
		Convert a Fonky Result object into a JSON-safe dictionary.

		Parameters:
		-----------
		result (Result): Fonky Result instance to serialize.

		Returns:
		--------
		Dict[str, Any]: JSON-safe Result payload.

	'''
	throw_if( 'result', result )
	
	return {
			'type': 'result',
			'url': result.url,
			'status_code': result.status_code,
			'encoding': result.encoding,
			'headers': dict( result.headers ) if result.headers is not None else { },
			'text': result.text,
	}

def serialize_document( document: Any ) -> Dict[ str, Any ]:
	'''

		Purpose:
		--------
		Convert a LangChain-style Document object into a JSON-safe dictionary. The function
		uses duck typing so it can serialize compatible document objects without importing
		LangChain at module load time.

		Parameters:
		-----------
		document (Any): Document-like object with page_content and metadata attributes.

		Returns:
		--------
		Dict[str, Any]: JSON-safe document payload.

	'''
	throw_if( 'document', document )
	
	page_content = getattr( document, 'page_content', None )
	metadata = getattr( document, 'metadata', None )
	
	return {
			'type': 'document',
			'page_content': page_content,
			'metadata': serialize_value( metadata or { } ),
	}

def serialize_documents( documents: Sequence[ Any ] ) -> List[ Dict[ str, Any ] ]:
	'''

		Purpose:
		--------
		Convert a sequence of LangChain-style Document objects into JSON-safe dictionaries.

		Parameters:
		-----------
		documents (Sequence[Any]): Sequence of document-like objects.

		Returns:
		--------
		List[Dict[str, Any]]: JSON-safe document payloads.

	'''
	throw_if( 'documents', documents )
	return [ serialize_document( document ) for document in documents ]

def serialize_mapping( value: Mapping[ Any, Any ] ) -> Dict[ str, Any ]:
	'''

		Purpose:
		--------
		Convert a mapping into a JSON-safe dictionary with string keys.

		Parameters:
		-----------
		value (Mapping[Any, Any]): Mapping to serialize.

		Returns:
		--------
		Dict[str, Any]: JSON-safe dictionary.

	'''
	throw_if( 'value', value )
	
	return {
			str( key ): serialize_value( item )
			for key, item in value.items( )
	}

def serialize_sequence( value: Sequence[ Any ] ) -> List[ Any ]:
	'''

		Purpose:
		--------
		Convert a sequence into a JSON-safe list.

		Parameters:
		-----------
		value (Sequence[Any]): Sequence to serialize.

		Returns:
		--------
		List[Any]: JSON-safe list.

	'''
	throw_if( 'value', value )
	return [ serialize_value( item ) for item in value ]

def is_document_like( value: Any ) -> bool:
	'''

		Purpose:
		--------
		Determine whether a value appears to be a LangChain-style Document object.

		Parameters:
		-----------
		value (Any): Value to inspect.

		Returns:
		--------
		bool: True when the value has page_content and metadata attributes.

	'''
	return hasattr( value, 'page_content' ) and hasattr( value, 'metadata' )

def is_scalar( value: Any ) -> bool:
	'''

		Purpose:
		--------
		Determine whether a value is already JSON-safe as a scalar value.

		Parameters:
		-----------
		value (Any): Value to inspect.

		Returns:
		--------
		bool: True when the value is a JSON-safe scalar.

	'''
	return value is None or isinstance( value, (str, int, float, bool) )

def serialize_value( value: Any ) -> Any:
	'''

		Purpose:
		--------
		Convert an arbitrary Python object into a JSON-safe value. This is the central
		provider-neutral serializer used by registries, adapters, fetcher tools, loader tools,
		and future provider-specific wrappers.

		Parameters:
		-----------
		value (Any): Value to serialize.

		Returns:
		--------
		Any: JSON-safe scalar, list, or dictionary.

	'''
	value = serialize_numpy_value( value )
	
	if is_scalar( value ):
		return value
	
	if isinstance( value, Result ):
		return serialize_result( value )
	
	if isinstance( value, Response ):
		return serialize_response( value )
	
	if isinstance( value, BaseModel ):
		return serialize_pydantic_model( value )
	
	if isinstance( value, pd.DataFrame ):
		return serialize_dataframe( value )
	
	if isinstance( value, pd.Series ):
		return serialize_series( value )
	
	if isinstance( value, (datetime, date) ):
		return serialize_datetime( value )
	
	if isinstance( value, Decimal ):
		return serialize_decimal( value )
	
	if isinstance( value, UUID ):
		return serialize_uuid( value )
	
	if isinstance( value, Enum ):
		return serialize_enum( value )
	
	if isinstance( value, Path ):
		return serialize_path( value )
	
	if is_document_like( value ):
		return serialize_document( value )
	
	if isinstance( value, Mapping ):
		return serialize_mapping( value )
	
	if isinstance( value, tuple ):
		return [ serialize_value( item ) for item in value ]
	
	if isinstance( value, list ):
		return [ serialize_value( item ) for item in value ]
	
	if isinstance( value, set ):
		return [ serialize_value( item ) for item in sorted( value, key=lambda item: str( item ) ) ]
	
	if hasattr( value, 'to_dict' ) and callable( value.to_dict ):
		return serialize_value( value.to_dict( ) )
	
	if hasattr( value, '__dict__' ):
		return serialize_mapping( vars( value ) )
	
	return str( value )

# ==========================================================================================
# TOOL RESULT PAYLOADS
# ==========================================================================================

class ToolResultSerializer:
	'''

		Purpose:
		--------
		Build provider-neutral tool-result payloads. These results are intended to be passed
		into provider-specific adapters that translate them into OpenAI, Gemini, Grok, or
		local-model response formats.

		Attributes:
		-----------
		None

		Methods:
		--------
		success(...): Build a successful tool-result payload.
		failure(...): Build a failed tool-result payload.
		result(...): Build a generic tool-result payload.

	'''
	
	@staticmethod
	def result( name: str, success: bool, data: Any = None, error: Optional[ str ] = None,
			metadata: Optional[ Dict[ str, Any ] ] = None ) -> Dict[ str, Any ]:
		'''

			Purpose:
			--------
			Build a provider-neutral tool-result payload.

			Parameters:
			-----------
			name (str): Tool name.
			success (bool): Whether the tool execution succeeded.
			data (Any): Optional result data.
			error (Optional[str]): Optional error message.
			metadata (Optional[Dict[str, Any]]): Optional result metadata.

			Returns:
			--------
			Dict[str, Any]: Provider-neutral tool-result payload.

		'''
		throw_if( 'name', name )
		
		return {
				'name': name,
				'success': success,
				'data': serialize_value( data ),
				'error': error,
				'metadata': serialize_value( metadata or { } ),
		}
	
	@staticmethod
	def success( name: str, data: Any = None,
			metadata: Optional[ Dict[ str, Any ] ] = None ) -> Dict[ str, Any ]:
		'''

			Purpose:
			--------
			Build a successful provider-neutral tool-result payload.

			Parameters:
			-----------
			name (str): Tool name.
			data (Any): Optional result data.
			metadata (Optional[Dict[str, Any]]): Optional result metadata.

			Returns:
			--------
			Dict[str, Any]: Provider-neutral successful result payload.

		'''
		return ToolResultSerializer.result( name=name, success=True, data=data, error=None,
			metadata=metadata )
	
	@staticmethod
	def failure( name: str, error: Exception | str,
			metadata: Optional[ Dict[ str, Any ] ] = None ) -> Dict[ str, Any ]:
		'''

			Purpose:
			--------
			Build a failed provider-neutral tool-result payload.

			Parameters:
			-----------
			name (str): Tool name.
			error (Exception | str): Exception or error message.
			metadata (Optional[Dict[str, Any]]): Optional result metadata.

			Returns:
			--------
			Dict[str, Any]: Provider-neutral failed result payload.

		'''
		throw_if( 'error', error )
		
		error_text = str( error )
		return ToolResultSerializer.result( name=name, success=False, data=None, error=error_text,
			metadata=metadata )

# ==========================================================================================
# MODULE-LEVEL RESULT BUILDERS
# ==========================================================================================

def build_success_result( name: str, data: Any = None,
		metadata: Optional[ Dict[ str, Any ] ] = None ) -> Dict[ str, Any ]:
	'''

		Purpose:
		--------
		Build a successful provider-neutral tool-result payload.

		Parameters:
		-----------
		name (str): Tool name.
		data (Any): Optional result data.
		metadata (Optional[Dict[str, Any]]): Optional result metadata.

		Returns:
		--------
		Dict[str, Any]: Provider-neutral successful result payload.

	'''
	return ToolResultSerializer.success( name=name, data=data, metadata=metadata )

def build_failure_result( name: str, error: Exception | str,
		metadata: Optional[ Dict[ str, Any ] ] = None ) -> Dict[ str, Any ]:
	'''

		Purpose:
		--------
		Build a failed provider-neutral tool-result payload.

		Parameters:
		-----------
		name (str): Tool name.
		error (Exception | str): Exception or error message.
		metadata (Optional[Dict[str, Any]]): Optional result metadata.

		Returns:
		--------
		Dict[str, Any]: Provider-neutral failed result payload.

	'''
	return ToolResultSerializer.failure( name=name, error=error, metadata=metadata )