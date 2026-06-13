'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                models.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="models.py" company="Terry D. Eppler">

	     models.py
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
    models.py
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

import inspect
import types
from boogr import Error
from typing import Any, Dict, List, Optional, Union, get_args, get_origin, get_type_hints, Callable

from pydantic import BaseModel, ConfigDict

def throw_if( name: str, value: Any ) -> None:
	"""Validate a required argument and raise a ValueError when the supplied value is None.
	
	Purpose:
	    Provides the `throw_if` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
	
	Args:
	    name (str): Input value passed to the callable.
	    value (object): Input value passed to the callable.
	
	Raises:
	    Error: Raised when the wrapped operation fails and the exception is logged."""
	if value is None:
		raise ValueError( f'Argument "{name}" cannot be None.' )
	
	if isinstance( value, str ) and not value.strip( ):
		raise ValueError( f'Argument "{name}" cannot be empty.' )

def clean_docstring( value: Optional[ str ] ) -> str:
	"""Clean a callable docstring for use as a tool description.
	
	Purpose:
	    Provides the `clean_docstring` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
	
	Args:
	    value (str): Input value passed to the callable.
	
	Returns:
	    str: Returned value produced by the callable.
	
	Raises:
	    Error: Raised when the wrapped operation fails and the exception is logged."""
	try:
		if not value:
			return ''
		
		return inspect.cleandoc( value ).strip( )
	except Exception as e:
		exception = Error( e )
		exception.module = 'models'
		exception.cause = 'ToolDef'
		exception.method = 'clean_docstring( value: Optional[ str ] ) -> str'
		raise exception

def python_type_to_json_schema( annotation: Any ) -> Dict[ str, Any ]:
	"""Convert a Python type annotation into a JSON Schema fragment suitable for.
	
	Purpose:
	    Provides the `python_type_to_json_schema` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
	
	Args:
	    annotation (object): Input value passed to the callable.
	
	Returns:
	    Dict[str, object]: Returned value produced by the callable.
	
	Raises:
	    Error: Raised when the wrapped operation fails and the exception is logged."""
	try:
		if annotation is inspect.Signature.empty:
			return { 'type': 'string' }
		
		if annotation is Any:
			return { 'type': 'object' }
		
		origin = get_origin( annotation )
		args = get_args( annotation )
		
		if origin in (Union, types.UnionType):
			non_null = [ arg for arg in args if arg is not type( None ) ]
			
			if len( non_null ) == 1:
				return python_type_to_json_schema( non_null[ 0 ] )
			
			return { 'type': 'object' }
		
		if origin in (list, List):
			item_type = args[ 0 ] if args else Any
			
			return {
					'type': 'array',
					'items': python_type_to_json_schema( item_type )
			}
		
		if origin in (dict, Dict):
			return { 'type': 'object' }
		
		if annotation is str:
			return { 'type': 'string' }
		
		if annotation is int:
			return { 'type': 'integer' }
		
		if annotation is float:
			return { 'type': 'number' }
		
		if annotation is bool:
			return { 'type': 'boolean' }
		
		if annotation in (list, tuple, set):
			return { 'type': 'array' }
		
		if annotation is dict:
			return { 'type': 'object' }
		
		return { 'type': 'object' }
	except Exception as e:
		exception = Error( e )
		exception.module = 'models'
		exception.cause = 'ToolDef'
		exception.method = 'python_type_to_json_schema( annotation: Any ) -> Dict[ str, Any ]'
		raise exception

def build_parameter_schema( function: Callable[ ..., Any ] ) -> Dict[ str, Any ]:
	"""Build a provider-neutral JSON Schema parameters object from a Python callable.
	
	Purpose:
	    Provides the `build_parameter_schema` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
	
	Args:
	    function (Callable[..., object]): Input value passed to the callable.
	
	Returns:
	    Dict[str, object]: Returned value produced by the callable.
	
	Raises:
	    Error: Raised when the wrapped operation fails and the exception is logged."""
	try:
		throw_if( 'function', function )
		
		if not callable( function ):
			raise TypeError( 'Argument "function" must be callable.' )
		
		signature = inspect.signature( function )
		
		try:
			type_hints = get_type_hints( function )
		except Exception:
			type_hints = { }
		
		properties: Dict[ str, Any ] = { }
		required: List[ str ] = [ ]
		
		for name, parameter in signature.parameters.items( ):
			if name in ('self', 'cls'):
				continue
			
			if parameter.kind in (
						inspect.Parameter.VAR_POSITIONAL,
						inspect.Parameter.VAR_KEYWORD
			):
				continue
			
			annotation = type_hints.get( name, parameter.annotation )
			schema = python_type_to_json_schema( annotation )
			
			if parameter.default is not inspect.Signature.empty:
				schema[ 'default' ] = parameter.default
			else:
				required.append( name )
			
			properties[ name ] = schema
		
		return {
				'type': 'object',
				'properties': properties,
				'required': required
		}
	except Exception as e:
		exception = Error( e )
		exception.module = 'models'
		exception.cause = 'ToolDef'
		exception.method = 'build_parameter_schema( function: Callable[ ..., Any ] ) -> Dict[ str, Any ]'
		raise exception

def serialize_value( value: Any ) -> Any:
	"""Convert common Fonky, LangChain, Pydantic, pandas, and Python values into a.
	
	Purpose:
	    Provides the `serialize_value` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
	
	Args:
	    value (object): Input value passed to the callable.
	
	Returns:
	    object: Returned value produced by the callable.
	
	Raises:
	    Error: Raised when the wrapped operation fails and the exception is logged."""
	try:
		if value is None:
			return None
		
		if isinstance( value, (str, int, float, bool) ):
			return value
		
		if hasattr( value, 'page_content' ) and hasattr( value, 'metadata' ):
			return {
					'page_content': serialize_value( value.page_content ),
					'metadata': serialize_value( value.metadata )
			}
		
		if hasattr( value, 'model_dump' ) and callable( value.model_dump ):
			return serialize_value( value.model_dump( ) )
		
		if hasattr( value, 'to_dict' ) and callable( value.to_dict ):
			return serialize_value( value.to_dict( ) )
		
		if hasattr( value, 'to_json' ) and callable( value.to_json ):
			return value.to_json( )
		
		if isinstance( value, dict ):
			return {
					str( key ): serialize_value( item )
					for key, item in value.items( )
			}
		
		if isinstance( value, (list, tuple, set) ):
			return [ serialize_value( item ) for item in value ]
		
		return str( value )
	except Exception as e:
		exception = Error( e )
		exception.module = 'models'
		exception.cause = 'ToolDef'
		exception.method = 'serialize_value( value: Any ) -> Any'
		raise exception

class Prompt( BaseModel ):
	"""Represents a structured “system prompt” or instruction bundle used to steer an LLM call.
	
	Purpose:
	    Documents the `Prompt` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	instructions: Optional[ str ]
	id: Optional[ str ]
	version: Optional[ str ]
	format: Optional[ str ]
	question: Optional[ str ]

class File( BaseModel ):
	"""Represents a file-like object returned by an API (uploaded artifacts, generated files,.
	
	Purpose:
	    Documents the `File` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	filename: Optional[ str ]
	bytes: Optional[ int ]
	created_at: Optional[ int ]
	expires_at: Optional[ int ]
	id: Optional[ str ]
	object: Optional[ str ]
	purpose: Optional[ str ]

class Document( BaseModel ):
	"""Represents a generic “document-like” structured output. Boo uses this for demos and.
	
	Purpose:
	    Documents the `Document` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	summary: Optional[ str ]
	description: Optional[ str ]

class Message( BaseModel ):
	"""Represents a chat message-like object used by Boo to normalize conversational state.
	
	Purpose:
	    Documents the `Message` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	content: Optional[ str ]
	role: Optional[ str ]
	type: Optional[ str ]
	data: Optional[ Dict ]

class Location( BaseModel ):
	"""Represents a high-level user location descriptor used by web search or other tools.
	
	Purpose:
	    Documents the `Location` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	type: Optional[ str ]
	city: Optional[ str ]
	country: Optional[ str ]
	region: Optional[ str ]
	timezone: Optional[ str ]

class GeoCoordinates( BaseModel ):
	"""Represents a latitude/longitude coordinate pair, optionally with a timezone. This is.
	
	Purpose:
	    Documents the `GeoCoordinates` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	type: Optional[ str ]
	latitude: Optional[ float ]
	longitude: Optional[ float ]
	timezone: Optional[ str ]

class Forecast( BaseModel ):
	"""Represents a simplified weather forecast payload returned by a tool or model.
	
	Purpose:
	    Documents the `Forecast` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	type: Optional[ str ]
	temperature: Optional[ int ]
	precipitation: Optional[ int ]
	sky_conditions: Optional[ str ]

class Directions( BaseModel ):
	"""Represents a simplified directions/route payload returned by a mapping tool.
	
	Purpose:
	    Documents the `Directions` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	type: Optional[ str ]
	route: Optional[ Any ]

class SkyCoordinates( BaseModel ):
	"""Represents right ascension / declination coordinate pairs used in astronomy-oriented.
	
	Purpose:
	    Documents the `SkyCoordinates` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	type: Optional[ str ]
	declination: Optional[ float ]
	right_ascension: Optional[ float ]

class Tool( BaseModel ):
	"""Represents a tool/function descriptor for tool-calling. Boo uses this to keep “tool.
	
	Purpose:
	    Documents the `Tool` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	name: Optional[ str ]
	type: Optional[ str ]
	description: Optional[ str ]

class Function( Tool ):
	"""Represents a tool/function descriptor for tool-calling. Boo uses this to keep “tool.
	
	Purpose:
	    Documents the `Function` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	parameters: Optional[ Dict[ str, Any ] ]
	strict: Optional[ bool ]

class FileSearch( Tool ):
	"""Represents configuration for a file-search tool invocation. Boo uses this to keep tool.
	
	Purpose:
	    Documents the `FileSearch` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	vector_store_ids: Optional[ List[ str ] ]
	max_num_results: Optional[ int ]
	filters: Optional[ Dict[ str, Any ] ]

class WebSearch( Tool ):
	"""Represents configuration for a web-search tool invocation.
	
	Purpose:
	    Documents the `WebSearch` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	type: Optional[ str ]
	search_context_size: Optional[ str ]
	user_location: Optional[ Any ]

class ComputerUse( Tool ):
	"""Represents configuration for a computer-use tool invocation (UI automation / virtual.
	
	Purpose:
	    Documents the `ComputerUse` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	type: Optional[ str ]
	display_height: Optional[ int ]
	display_width: Optional[ int ]
	environment: Optional[ str ]

class ToolDef( Function ):
	"""Represents a provider-neutral AI tool definition bound to an existing Fonky callable.
	
	Purpose:
	    Documents the `ToolDef` class and its role in the Fonky runtime. The class docstring uses Google style so MkDocs and mkdocstrings can render it without Griffe section warnings."""
	model_config = ConfigDict( arbitrary_types_allowed=True )
	
	name: Optional[ str ] = None
	type: Optional[ str ] = None
	description: Optional[ str ] = None
	parameters: Optional[ Dict[ str, Any ] ] = None
	strict: Optional[ bool ] = None
	target: Optional[ Any ] = None
	method: Optional[ str ] = None
	handler: Optional[ Callable[ ..., Any ] ] = None
	category: Optional[ str ] = None
	source_module: Optional[ str ] = None
	source_class: Optional[ str ] = None
	callable_name: Optional[ str ] = None
	
	@classmethod
	def from_callable( cls, function: Callable[ ..., Any ], name: Optional[ str ] = None,
			description: Optional[ str ] = None, category: Optional[ str ] = None,
			strict: bool = True ) -> 'ToolDef':
		"""Create a provider-neutral tool definition from a plain Python callable.
		
		Purpose:
		    Provides the `from_callable` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    function (Callable[..., object]): Input value passed to the callable.
		    name (str): Input value passed to the callable.
		    description (str): Input value passed to the callable.
		    category (str): Input value passed to the callable.
		    strict (bool): Input value passed to the callable.
		
		Returns:
		    'ToolDef': Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'function', function )
			
			if not callable( function ):
				raise TypeError( 'Argument "function" must be callable.' )
			
			callable_name = getattr( function, '__name__', function.__class__.__name__ )
			source_module = getattr( function, '__module__', None )
			
			return cls( name=name or callable_name, type='function',
				description=description or clean_docstring( getattr( function, '__doc__', '' ) ),
				parameters=build_parameter_schema( function ), strict=strict, target=None,
				method=None, handler=function, category=category, source_module=source_module,
				source_class=None, callable_name=callable_name )
		except Exception as e:
			exception = Error( e )
			exception.module = 'models'
			exception.cause = 'ToolDef'
			exception.method = (
					'from_callable( cls, function: Callable[ ..., Any ], '
					'name: Optional[ str ]=None, description: Optional[ str ]=None, '
					'category: Optional[ str ]=None, strict: bool=True ) -> ToolDef'
			)
			raise exception
	
	@classmethod
	def from_method( cls, target: Any, method: str, name: Optional[ str ] = None,
			description: Optional[ str ] = None, category: Optional[ str ] = None,
			strict: bool = True ) -> 'ToolDef':
		"""Create a provider-neutral tool definition from an existing object instance and.
		
		Purpose:
		    Provides the `from_method` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    target (object): Input value passed to the callable.
		    method (str): Input value passed to the callable.
		    name (str): Input value passed to the callable.
		    description (str): Input value passed to the callable.
		    category (str): Input value passed to the callable.
		    strict (bool): Input value passed to the callable.
		
		Returns:
		    'ToolDef': Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			throw_if( 'target', target )
			throw_if( 'method', method )
			
			if not hasattr( target, method ):
				target_name = type( target ).__name__
				raise AttributeError( f'Target "{target_name}" has no method "{method}".' )
			
			handler = getattr( target, method )
			
			if not callable( handler ):
				target_name = type( target ).__name__
				raise TypeError( f'Target "{target_name}.{method}" is not callable.' )
			
			source_class = type( target ).__name__
			source_module = type( target ).__module__
			
			return cls(
				name=name or f'{source_class}_{method}',
				type='function',
				description=description or clean_docstring( getattr( handler, '__doc__', '' ) ),
				parameters=build_parameter_schema( handler ),
				strict=strict,
				target=target,
				method=method,
				handler=None,
				category=category,
				source_module=source_module,
				source_class=source_class,
				callable_name=method
			)
		except Exception as e:
			exception = Error( e )
			exception.module = 'models'
			exception.cause = 'ToolDef'
			exception.method = (
					'from_method( cls, target: Any, method: str, name: Optional[ str ]=None, '
					'description: Optional[ str ]=None, category: Optional[ str ]=None, '
					'strict: bool=True ) -> ToolDef'
			)
			raise exception
	
	def resolve_callable( self ) -> Callable[ ..., Any ]:
		"""Resolve and return the Python callable bound to this tool definition.
		
		Purpose:
		    Provides the `resolve_callable` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    Callable[..., object]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			if self.handler is not None:
				return self.handler
			
			if self.target is None:
				raise ValueError( 'ToolDef target cannot be None when handler is not supplied.' )
			
			throw_if( 'method', self.method )
			
			if not hasattr( self.target, self.method ):
				target_name = type( self.target ).__name__
				raise AttributeError( f'Target "{target_name}" has no method "{self.method}".' )
			
			handler = getattr( self.target, self.method )
			
			if not callable( handler ):
				target_name = type( self.target ).__name__
				raise TypeError( f'Target "{target_name}.{self.method}" is not callable.' )
			
			return handler
		except Exception as e:
			exception = Error( e )
			exception.module = 'models'
			exception.cause = 'ToolDef'
			exception.method = 'resolve_callable( self ) -> Callable[ ..., Any ]'
			raise exception
	
	def call( self, arguments: Optional[ Dict[ str, Any ] ] = None ) -> Dict[ str, Any ]:
		"""Execute the bound callable with keyword arguments and return a neutral,.
		
		Purpose:
		    Provides the `call` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Args:
		    arguments (Dict[str, object]): Input value passed to the callable.
		
		Returns:
		    Dict[str, object]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			handler = self.resolve_callable( )
			payload = arguments or { }
			result = handler( **payload )
			
			return {
					'ok': True,
					'name': self.name,
					'data': serialize_value( result ),
					'error': None,
					'metadata': {
							'category': self.category,
							'source_module': self.source_module,
							'source_class': self.source_class,
							'method': self.method,
							'callable_name': self.callable_name
					}
			}
		except Exception as e:
			exception = Error( e )
			exception.module = 'models'
			exception.cause = 'ToolDef'
			exception.method = 'call( self, arguments: Optional[ Dict[ str, Any ] ]=None ) -> Dict[ str, Any ]'
			
			return {
					'ok': False,
					'name': self.name,
					'data': None,
					'error': {
							'type': type( exception ).__name__,
							'message': str( exception )
					},
					'metadata': {
							'category': self.category,
							'source_module': self.source_module,
							'source_class': self.source_class,
							'method': self.method,
							'callable_name': self.callable_name
					}
			}
	
	def to_dict( self ) -> Dict[ str, Any ]:
		"""Return a JSON-safe provider-neutral schema dictionary for this tool definition.
		
		Purpose:
		    Provides the `to_dict` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    Dict[str, object]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			return { 'name': self.name,
			         'type': self.type,
			         'description': self.description,
			         'parameters': self.parameters,
			         'strict': self.strict,
			         'category': self.category,
			         'source_module': self.source_module,
			         'source_class': self.source_class,
			         'method': self.method,
			         'callable_name': self.callable_name }
		except Exception as e:
			exception = Error( e )
			exception.module = 'models'
			exception.cause = 'ToolDef'
			exception.method = 'to_dict( self ) -> Dict[ str, Any ]'
			raise exception
	
	def to_openai( self ) -> Dict[ str, Any ]:
		"""Return an OpenAI-compatible function tool schema generated from the neutral.
		
		Purpose:
		    Provides the `to_openai` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    Dict[str, object]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			return {
					'type': 'function',
					'function': {
							'name': self.name,
							'description': self.description or '',
							'parameters': self.parameters or {
									'type': 'object',
									'properties': { },
									'required': [ ]
							},
							'strict': bool( self.strict )
					}
			}
		except Exception as e:
			exception = Error( e )
			exception.module = 'models'
			exception.cause = 'ToolDef'
			exception.method = 'to_openai( self ) -> Dict[ str, Any ]'
			raise exception
	
	def to_grok( self ) -> Dict[ str, Any ]:
		"""Return a Grok-compatible function tool schema generated from the neutral.
		
		Purpose:
		    Provides the `to_grok` callable documented in Google style for MkDocs and mkdocstrings output. The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    Dict[str, object]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			return self.to_openai( )
		except Exception as e:
			exception = Error( e )
			exception.module = 'models'
			exception.cause = 'ToolDef'
			exception.method = 'to_grok( self ) -> Dict[ str, Any ]'
			raise exception
	
	def to_gemini( self ) -> Dict[ str, Any ]:
		"""Return a Gemini-compatible function declaration generated from the neutral.
		
		Purpose:
		    Provides the `to_gemini` callable documented in Google style for MkDocs and mkdocstrings output.
		    The documented signature and return contract are aligned with the source implementation.
		
		Returns:
		    Dict[str, object]: Returned value produced by the callable.
		
		Raises:
		    Error: Raised when the wrapped operation fails and the exception is logged."""
		try:
			return {
					'name': self.name,
					'description': self.description or '',
					'parameters': self.parameters or {
							'type': 'object',
							'properties': { },
							'required': [ ]
					}
			}
		except Exception as e:
			exception = Error( e )
			exception.module = 'models'
			exception.cause = 'ToolDef'
			exception.method = 'to_gemini( self ) -> Dict[ str, Any ]'
			raise exception

