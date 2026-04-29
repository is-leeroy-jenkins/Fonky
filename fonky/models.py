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
from fonky.boogr import Error
from collections.abc import Callable
from typing import Any, Dict, List, Optional, Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel, ConfigDict

class Prompt( BaseModel ):
	'''

		Purpose:
		--------
		Represents a structured “system prompt” or instruction bundle used to steer an LLM call.
		This model is intended to capture the canonical components you pass into Boo when you
		want to track prompts as first-class objects (versioning, variables, and provenance).

		Attributes:
		----------
		instructions: Optional[ str ]
			The primary instruction block (typically the system message content).

		context: Optional[ str ]
			Optional background context provided to the model (policies, references, etc.).

		output_indicator: Optional[ str ]
			A short indicator describing the desired output style/format (e.g., "json", "table").

		input_data: Optional[ str ]
			Optional data payload embedded into the prompt (small inputs, examples, etc.).

		id: Optional[ str ]
			Optional identifier for tracking prompts (e.g., GUID, hash, or friendly name).

		version: Optional[ str ]
			Optional version string for prompt management and experimentation.

		format: Optional[ str ]
			Optional format label describing the prompt template type (e.g., "chat", "completion").

		variables: Optional[ List[ str ] ]
			Optional list of placeholder variables referenced by the prompt template.

		question: Optional[ str ]
			Optional question or user query associated with the prompt.

	'''
	instructions: Optional[ str ]
	id: Optional[ str ]
	version: Optional[ str ]
	format: Optional[ str ]
	question: Optional[ str ]

class File( BaseModel ):
	'''

		Purpose:
		--------
		Represents a file-like object returned by an API (uploaded artifacts, generated files,
		or tool outputs). This is intentionally permissive: Boo only needs the common metadata.

		Attributes:
		----------
		filename: Optional[ str ]
			The original or assigned filename.

		bytes: Optional[ int ]
			The size of the file in bytes, if provided.

		created_at: Optional[ int ]
			Unix timestamp of creation (seconds), if provided.

		expires_at: Optional[ int ]
			Unix timestamp when the file expires, if the upstream supports expiring artifacts.

		id: Optional[ str ]
			Unique file identifier in the upstream system.

		object: Optional[ str ]
			Object discriminator from the upstream API (e.g., "file").

		purpose: Optional[ str ]
			Intended purpose for the file in the upstream system (e.g., "assistants", "fine-tune").

	'''
	filename: Optional[ str ]
	bytes: Optional[ int ]
	created_at: Optional[ int ]
	expires_at: Optional[ int ]
	id: Optional[ str ]
	object: Optional[ str ]
	purpose: Optional[ str ]

class Document( BaseModel ):
	'''

		Purpose:
		--------
		Represents a generic “document-like” structured output. Boo uses this for demos and
		for workflows where the model produces a multi-field narrative artifact with concepts.

		Attributes:
		----------
		invented_year: Optional[ int ]
			Example field used in some structured-output prompts; can be repurposed.

		summary: Optional[ str ]
			High-level summary of the document.

		inventors: Optional[ List[ str ] ]
			Example list field used in structured-output prompts.

		description: Optional[ str ]
			Long-form description.

		concepts: Optional[ List[ Concept ] ]
			List of extracted or described concepts.

	'''
	summary: Optional[ str ]
	description: Optional[ str ]

class Message( BaseModel ):
	'''

		Purpose:
		--------
		Represents a chat message-like object used by Boo to normalize conversational state.
		This is intentionally general to support both “input messages” and “output messages”.

		Attributes:
		----------
		content: str
			Message content payload. Boo treats this as required for operational messages.

		role: str
			Message role (e.g., "system", "user", "assistant", "tool").

		type: Optional[ str ]
			Optional discriminator if an upstream system emits typed message objects.

		instructions: Optional[ str ]
			Optional per-message instruction string (used in some orchestration patterns).

		data: Optional[ Dict ]
			Optional message metadata or additional structured payload.

	'''
	content: Optional[ str ]
	role: Optional[ str ]
	type: Optional[ str ]
	data: Optional[ Dict ]

class Location( BaseModel ):
	'''

		Purpose:
		--------
		Represents a high-level user location descriptor used by web search or other tools.

		Attributes:
		----------
		type: Optional[ str ]
			Type discriminator for location objects.

		city: Optional[ str ]
			City name.

		country: Optional[ str ]
			Country name or code.

		region: Optional[ str ]
			State/province/region.

		timezone: Optional[ str ]
		IANA timezone string when known.

	'''
	type: Optional[ str ]
	city: Optional[ str ]
	country: Optional[ str ]
	region: Optional[ str ]
	timezone: Optional[ str ]

class GeoCoordinates( BaseModel ):
	'''

		Purpose:
		--------
		Represents a latitude/longitude coordinate pair, optionally with a timezone. This is
		useful for tools like web search, maps, or proximity-based retrieval.

		Attributes:
		----------
		type: Optional[ str ]
			Type discriminator for geocoordinate objects.

		latitude: Optional[ float ]
			Latitude in decimal degrees.

		longitude: Optional[ float ]
			Longitude in decimal degrees.

		timezone: Optional[ str ]
			IANA timezone string when known.

	'''
	type: Optional[ str ]
	latitude: Optional[ float ]
	longitude: Optional[ float ]
	timezone: Optional[ str ]

class Forecast( BaseModel ):
	'''

		Purpose:
		--------
		Represents a simplified weather forecast payload returned by a tool or model.

		Attributes:
		----------
		type: Optional[ str ]
			Type discriminator for the object.

		temperature: Optional[ int ]
			Temperature value (units depend on the tool/provider).

		precipitation: Optional[ int ]
			Precipitation percentage or amount (provider-specific).

		sky_conditions: Optional[ str ]
			Text description such as "clear", "cloudy", "rain".

	'''
	type: Optional[ str ]
	temperature: Optional[ int ]
	precipitation: Optional[ int ]
	sky_conditions: Optional[ str ]

class Directions( BaseModel ):
	'''

		Purpose:
		--------
		Represents a simplified directions/route payload returned by a mapping tool.

		Attributes:
		----------
		type: Optional[ str ]
			Type discriminator for the object.

		route: Optional[ Any ]
			Route representation (provider-specific). Frequently this is a string/polyline or
			a structured list of steps.

	'''
	type: Optional[ str ]
	route: Optional[ Any ]

class SkyCoordinates( BaseModel ):
	'''

		Purpose:
		--------
		Represents right ascension / declination coordinate pairs used in astronomy-oriented
		structured outputs.

		Attributes:
		----------
		type: Optional[ str ]
			Type discriminator for the object.

		declination: Optional[ float ]
			Declination in decimal degrees.

		right_ascension: Optional[ float ]
			Right ascension in decimal degrees or hours (provider-specific).

	'''
	type: Optional[ str ]
	declination: Optional[ float ]
	right_ascension: Optional[ float ]

class Tool( BaseModel ):
	'''

		Purpose:
		--------
		Represents a tool/function descriptor for tool-calling. Boo uses this to keep “tool
		specification” structured (name, description, JSON schema parameters, strictness).

		Attributes:
		----------
		name: Optional[ str ]
			Function name as exposed to the model.

		type: Optional[ str ]
			Type discriminator (commonly "function") when used in tool lists.

		description: Optional[ str ]
			Human-readable description of the tool/function.

		parameters: Optional[ Dict[ str, Any ] ]
			JSON Schema-like parameters object describing accepted inputs.

		strict: Optional[ bool ]
			Whether the upstream should strictly validate arguments against the schema.

	'''
	name: Optional[ str ]
	type: Optional[ str ]
	description: Optional[ str ]

class Function( Tool ):
	'''

		Purpose:
		--------
		Represents a tool/function descriptor for tool-calling. Boo uses this to keep “tool
		specification” structured (name, description, JSON schema parameters, strictness).

		Attributes:
		----------
		name: Optional[ str ]
			Function name as exposed to the model.

		type: Optional[ str ]
			Type discriminator (commonly "function") when used in tool lists.

		description: Optional[ str ]
			Human-readable description of the tool/function.

		parameters: Optional[ Dict[ str, Any ] ]
			JSON Schema-like parameters object describing accepted inputs.

		strict: Optional[ bool ]
			Whether the upstream should strictly validate arguments against the schema.

	'''
	parameters: Optional[ Dict[ str, Any ] ]
	strict: Optional[ bool ]

# ==========================================================================================
# TOOL DEFINITION HELPERS
# ==========================================================================================

def throw_if( name: str, value: Any ) -> None:
	'''

		Purpose:
		--------
		Validate a required argument and raise a ValueError when the supplied value is None
		or an empty string.

		Parameters:
		-----------
		name (str): Name of the argument being validated.
		value (Any): Value being validated.

		Returns:
		--------
		None

	'''
	if value is None:
		raise ValueError( f'Argument "{name}" cannot be None.' )
	
	if isinstance( value, str ) and not value.strip( ):
		raise ValueError( f'Argument "{name}" cannot be empty.' )

def clean_docstring( value: Optional[ str ] ) -> str:
	'''

		Purpose:
		--------
		Clean a callable docstring for use as a tool description.

		Parameters:
		-----------
		value (Optional[str]): Raw docstring value.

		Returns:
		--------
		str: Cleaned docstring text.

	'''
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
	'''

		Purpose:
		--------
		Convert a Python type annotation into a JSON Schema fragment suitable for
		provider-neutral tool definitions.

		Parameters:
		-----------
		annotation (Any): Python type annotation.

		Returns:
		--------
		Dict[str, Any]: JSON Schema fragment.

	'''
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
	'''

		Purpose:
		--------
		Build a provider-neutral JSON Schema parameters object from a Python callable
		signature and resolved type hints.

		Parameters:
		-----------
		function (Callable[..., Any]): Callable used to generate the schema.

		Returns:
		--------
		Dict[str, Any]: JSON Schema object with properties and required fields.

	'''
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
	'''

		Purpose:
		--------
		Convert common Fonky, LangChain, Pydantic, pandas, and Python values into a
		JSON-safe representation suitable for tool-call results.

		Parameters:
		-----------
		value (Any): Value to serialize.

		Returns:
		--------
		Any: JSON-safe value.

	'''
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

# ==========================================================================================
# TOOL DEFINITION
# ==========================================================================================

class ToolDef( Function ):
	'''

		Purpose:
		--------
		Represents a provider-neutral AI tool definition bound to an existing Fonky callable.
		ToolDef does not duplicate behavior from fetchers, loaders, or scrapers. It stores
		callable metadata, generates a JSON-schema parameter contract from the callable
		signature, executes the callable, and serializes the result.

		Attributes:
		-----------
		target: Optional[Any]
			Object instance that owns the callable method, when method-backed.

		method: Optional[str]
			Method name on the target object, when method-backed.

		handler: Optional[Callable[..., Any]]
			Callable used for direct function-backed tool execution.

		category: Optional[str]
			Fonky category such as collections, documents, web, environmental, or cloud.

		source_module: Optional[str]
			Module where the callable originates.

		source_class: Optional[str]
			Class name for method-backed tools.

		callable_name: Optional[str]
			Underlying callable name.

		Methods:
		--------
		from_callable(...): Create a ToolDef from a function or callable.
		from_method(...): Create a ToolDef from an object instance and method name.
		resolve_callable(...): Resolve the executable callable.
		call(...): Execute the callable and return a neutral result envelope.
		to_dict(...): Return a JSON-safe schema dictionary.
		to_openai(...): Return an OpenAI-compatible tool schema.
		to_gemini(...): Return a Gemini-compatible function declaration.
		to_grok(...): Return a Grok-compatible tool schema.

	'''
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
		'''

			Purpose:
			--------
			Create a provider-neutral tool definition from a plain Python callable.

			Parameters:
			-----------
			function (Callable[..., Any]): Function or callable object to expose.
			name (Optional[str]): Optional tool name override.
			description (Optional[str]): Optional description override.
			category (Optional[str]): Optional Fonky category.
			strict (bool): Whether provider-side strict validation should be requested.

			Returns:
			--------
			ToolDef: Callable-backed tool definition.

		'''
		try:
			throw_if( 'function', function )
			
			if not callable( function ):
				raise TypeError( 'Argument "function" must be callable.' )
			
			callable_name = getattr( function, '__name__', function.__class__.__name__ )
			source_module = getattr( function, '__module__', None )
			
			return cls(
				name=name or callable_name,
				type='function',
				description=description or clean_docstring( getattr( function, '__doc__', '' ) ),
				parameters=build_parameter_schema( function ),
				strict=strict,
				target=None,
				method=None,
				handler=function,
				category=category,
				source_module=source_module,
				source_class=None,
				callable_name=callable_name
			)
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
		'''

			Purpose:
			--------
			Create a provider-neutral tool definition from an existing object instance and
			one of its methods.

			Parameters:
			-----------
			target (Any): Object instance that owns the method.
			method (str): Method name to expose.
			name (Optional[str]): Optional tool name override.
			description (Optional[str]): Optional description override.
			category (Optional[str]): Optional Fonky category.
			strict (bool): Whether provider-side strict validation should be requested.

			Returns:
			--------
			ToolDef: Method-backed tool definition.

		'''
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
		'''

			Purpose:
			--------
			Resolve and return the Python callable bound to this tool definition.

			Parameters:
			-----------
			None

			Returns:
			--------
			Callable[..., Any]: Resolved callable.

		'''
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
		'''

			Purpose:
			--------
			Execute the bound callable with keyword arguments and return a neutral,
			JSON-safe tool result envelope.

			Parameters:
			-----------
			arguments (Optional[Dict[str, Any]]): Keyword arguments passed to the callable.

			Returns:
			--------
			Dict[str, Any]: Tool result envelope.

		'''
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
		'''

			Purpose:
			--------
			Return a JSON-safe provider-neutral schema dictionary for this tool definition.
			Runtime-only fields such as target and handler are excluded.

			Parameters:
			-----------
			None

			Returns:
			--------
			Dict[str, Any]: Provider-neutral tool definition.

		'''
		try:
			return {
					'name': self.name,
					'type': self.type,
					'description': self.description,
					'parameters': self.parameters,
					'strict': self.strict,
					'category': self.category,
					'source_module': self.source_module,
					'source_class': self.source_class,
					'method': self.method,
					'callable_name': self.callable_name
			}
		except Exception as e:
			exception = Error( e )
			exception.module = 'models'
			exception.cause = 'ToolDef'
			exception.method = 'to_dict( self ) -> Dict[ str, Any ]'
			raise exception
	
	def to_openai( self ) -> Dict[ str, Any ]:
		'''

			Purpose:
			--------
			Return an OpenAI-compatible function tool schema generated from the neutral
			ToolDef contract.

			Parameters:
			-----------
			None

			Returns:
			--------
			Dict[str, Any]: OpenAI-compatible tool schema.

		'''
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
		'''

			Purpose:
			--------
			Return a Grok-compatible function tool schema generated from the neutral
			ToolDef contract.

			Parameters:
			-----------
			None

			Returns:
			--------
			Dict[str, Any]: Grok-compatible tool schema.

		'''
		try:
			return self.to_openai( )
		except Exception as e:
			exception = Error( e )
			exception.module = 'models'
			exception.cause = 'ToolDef'
			exception.method = 'to_grok( self ) -> Dict[ str, Any ]'
			raise exception
	
	def to_gemini( self ) -> Dict[ str, Any ]:
		'''

			Purpose:
			--------
			Return a Gemini-compatible function declaration generated from the neutral
			ToolDef contract.

			Parameters:
			-----------
			None

			Returns:
			--------
			Dict[str, Any]: Gemini-compatible function declaration.

		'''
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
		
class FileSearch( Tool ):
	'''

		Purpose:
		--------
		Represents configuration for a file-search tool invocation. Boo uses this to keep tool
		config structured and to support serialization/rehydration of tool configurations.

		Attributes:
		----------
		type: Optional[ str ]
			Type discriminator for the tool (commonly "file_search").

		vector_store_ids: Optional[ List[ str ] ]
			Vector store identifiers available to the search tool.

		max_num_results: Optional[ int ]
			Maximum number of results to return.

		filters: Optional[ Dict[ str, Any ] ]
			Optional filter object (metadata filters, namespace filters, etc.).

	'''
	vector_store_ids: Optional[ List[ str ] ]
	max_num_results: Optional[ int ]
	filters: Optional[ Dict[ str, Any ] ]

class WebSearch( Tool ):
	'''

		Purpose:
		--------
		Represents configuration for a web-search tool invocation.

		Attributes:
		----------
		type: Optional[ str ]
			Type discriminator for the tool (commonly "web_search").

		search_context_size: Optional[ str ]
			Desired context size (vendor-specific; common values are "low", "medium", "high").

		user_location: Optional[ Any ]
			Optional location descriptor to bias search results. This may be a Location,
			GeoCoordinates, or a vendor-specific object.

	'''
	type: Optional[ str ]
	search_context_size: Optional[ str ]
	user_location: Optional[ Any ]

class ComputerUse( Tool ):
	'''

		Purpose:
		--------
		Represents configuration for a computer-use tool invocation (UI automation / virtual
		display sessions).

		Attributes:
		----------
		type: Optional[ str ]
			Type discriminator for the tool (commonly "computer_use").

		display_height: Optional[ int ]
			Height (pixels) of the virtual display.

		display_width: Optional[ int ]
			Width (pixels) of the virtual display.

		environment: Optional[ str ]
			Environment label (e.g., "browser", "desktop") when supported by the tool provider.

	'''
	type: Optional[ str ]
	display_height: Optional[ int ]
	display_width: Optional[ int ]
	environment: Optional[ str ]
