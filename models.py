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
    Defines Pydantic data models and provider-neutral tool-definition helpers for Fonky.

    Purpose:
        Provides serializable model objects for prompts, files, messages, locations,
        forecasts, directions, search tools, computer-use tools, and callable tool
        definitions. The module also converts Python callables and type annotations into
        provider-ready schema objects for OpenAI, Grok, Gemini, and other tool-calling
        workflows while preserving a neutral internal representation.
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
	"""Validate required argument.
	
	Purpose:
	    Validates a required argument before downstream schema generation or tool execution uses it.
	    The function rejects missing values and empty strings so callers fail early with a clear
	    argument-specific error message.
	
	Args:
	    name (str): Human-readable argument name used in validation error messages.
	    value (Any): Runtime value converted into a JSON-safe representation.
	
	Raises:
	    Error: Raised after the underlying exception is wrapped with module, cause, and method metadata."""
	if value is None:
		raise ValueError( f'Argument "{name}" cannot be None.' )
	
	if isinstance( value, str ) and not value.strip( ):
		raise ValueError( f'Argument "{name}" cannot be empty.' )

def clean_docstring( value: Optional[ str ] ) -> str:
	"""Clean callable documentation.
	
	Purpose:
	    Normalizes optional callable documentation into a compact description string for generated
	    tool schemas. The function removes indentation artifacts and returns an empty string when no
	    documentation text is available.
	
	Args:
	    value (Optional[str]): Runtime value converted into a JSON-safe representation.
	
	Returns:
	    Cleaned docstring text suitable for reuse as a provider-facing tool description.
	
	Raises:
	    Error: Raised after the underlying exception is wrapped with module, cause, and method metadata."""
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
	"""Convert Python annotation to JSON Schema.
	
	Purpose:
	    Maps Python type annotations to the JSON Schema fragments used by provider tool
	    declarations. The function handles primitive types, containers, optional unions, and unknown
	    annotations with conservative schema defaults.
	
	Args:
	    annotation (Any): Python type annotation converted into a JSON Schema fragment.
	
	Returns:
	    JSON Schema fragment that represents the supplied Python type annotation.
	
	Raises:
	    Error: Raised after the underlying exception is wrapped with module, cause, and method metadata."""
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
	"""Build callable parameter schema.
	
	Purpose:
	    Inspects a Python callable signature and builds a provider-neutral JSON Schema parameters
	    object. The function excludes instance parameters, detects required arguments, preserves
	    default values, and uses type hints when available.
	
	Args:
	    function (Callable[..., Any]): Callable inspected, wrapped, or converted into a provider-neutral tool schema.
	
	Returns:
	    Provider-neutral JSON Schema object describing the callable parameters.
	
	Raises:
	    Error: Raised after the underlying exception is wrapped with module, cause, and method metadata."""
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
	"""Serialize runtime value.
	
	Purpose:
	    Converts common runtime objects into JSON-safe values for tool execution responses. The
	    function preserves primitive values, recursively serializes mappings and sequences, and
	    normalizes document, model, and dataframe-like objects when possible.
	
	Args:
	    value (Any): Runtime value converted into a JSON-safe representation.
	
	Returns:
	    JSON-safe representation of the supplied value.
	
	Raises:
	    Error: Raised after the underlying exception is wrapped with module, cause, and method metadata."""
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
	"""Prompt model.
	
	Purpose:
	    Represents a structured prompt bundle used to pass instructions, versioning details, output
	    format hints, and a user question through Fonky workflows. The model provides a typed
	    container for prompt metadata that can be serialized by Pydantic.
	
	Attributes:
	    instructions (Optional[str]): Instructions value stored by the model.
	    id (Optional[str]): Id value stored by the model.
	    version (Optional[str]): Version value stored by the model.
	    format (Optional[str]): Format value stored by the model.
	    question (Optional[str]): Question value stored by the model."""
	instructions: Optional[ str ]
	id: Optional[ str ]
	version: Optional[ str ]
	format: Optional[ str ]
	question: Optional[ str ]

class File( BaseModel ):
	"""File model.
	
	Purpose:
	    Represents file metadata returned by provider APIs or managed by Fonky workflows. The model
	    stores identity, lifecycle, size, object type, purpose, and filename fields in a consistent
	    Pydantic structure.
	
	Attributes:
	    filename (Optional[str]): Filename value stored by the model.
	    bytes (Optional[int]): Bytes value stored by the model.
	    created_at (Optional[int]): Created at value stored by the model.
	    expires_at (Optional[int]): Expires at value stored by the model.
	    id (Optional[str]): Id value stored by the model.
	    object (Optional[str]): Object value stored by the model.
	    purpose (Optional[str]): Purpose value stored by the model."""
	filename: Optional[ str ]
	bytes: Optional[ int ]
	created_at: Optional[ int ]
	expires_at: Optional[ int ]
	id: Optional[ str ]
	object: Optional[ str ]
	purpose: Optional[ str ]

class Document( BaseModel ):
	"""Document model.
	
	Purpose:
	    Represents a compact document-style payload containing summary and description text. The
	    model is useful for normalized outputs where only high-level document metadata is required.
	
	Attributes:
	    summary (Optional[str]): Summary value stored by the model.
	    description (Optional[str]): Description value stored by the model."""
	summary: Optional[ str ]
	description: Optional[ str ]

class Message( BaseModel ):
	"""Message model.
	
	Purpose:
	    Represents a normalized chat or tool message payload. The model stores role, content,
	    message type, and optional structured data for conversational and provider-facing workflows.
	
	Attributes:
	    content (Optional[str]): Content value stored by the model.
	    role (Optional[str]): Role value stored by the model.
	    type (Optional[str]): Type value stored by the model.
	    data (Optional[Dict]): Data value stored by the model."""
	content: Optional[ str ]
	role: Optional[ str ]
	type: Optional[ str ]
	data: Optional[ Dict ]

class Location( BaseModel ):
	"""Location model.
	
	Purpose:
	    Represents a high-level location descriptor for tools that need city, region, country,
	    timezone, or location type information. The model keeps user-location context in a provider-
	    neutral shape.
	
	Attributes:
	    type (Optional[str]): Type value stored by the model.
	    city (Optional[str]): City value stored by the model.
	    country (Optional[str]): Country value stored by the model.
	    region (Optional[str]): Region value stored by the model.
	    timezone (Optional[str]): Timezone value stored by the model."""
	type: Optional[ str ]
	city: Optional[ str ]
	country: Optional[ str ]
	region: Optional[ str ]
	timezone: Optional[ str ]

class GeoCoordinates( BaseModel ):
	"""GeoCoordinates model.
	
	Purpose:
	    Represents geographic coordinates and optional timezone metadata for geospatial tools. The
	    model stores latitude, longitude, coordinate type, and timezone in a serializable Pydantic
	    container.
	
	Attributes:
	    type (Optional[str]): Type value stored by the model.
	    latitude (Optional[float]): Latitude value stored by the model.
	    longitude (Optional[float]): Longitude value stored by the model.
	    timezone (Optional[str]): Timezone value stored by the model."""
	type: Optional[ str ]
	latitude: Optional[ float ]
	longitude: Optional[ float ]
	timezone: Optional[ str ]

class Forecast( BaseModel ):
	"""Forecast model.
	
	Purpose:
	    Represents a simplified weather forecast response. The model stores forecast type,
	    temperature, precipitation, and sky-condition values for tool outputs or normalized provider
	    responses.
	
	Attributes:
	    type (Optional[str]): Type value stored by the model.
	    temperature (Optional[int]): Temperature value stored by the model.
	    precipitation (Optional[int]): Precipitation value stored by the model.
	    sky_conditions (Optional[str]): Sky conditions value stored by the model."""
	type: Optional[ str ]
	temperature: Optional[ int ]
	precipitation: Optional[ int ]
	sky_conditions: Optional[ str ]

class Directions( BaseModel ):
	"""Directions model.
	
	Purpose:
	    Represents a simplified route or directions payload. The model stores route data and type
	    metadata for mapping, navigation, or location-aware tool responses.
	
	Attributes:
	    type (Optional[str]): Type value stored by the model.
	    route (Optional[Any]): Route value stored by the model."""
	type: Optional[ str ]
	route: Optional[ Any ]

class SkyCoordinates( BaseModel ):
	"""SkyCoordinates model.
	
	Purpose:
	    Represents astronomical coordinate values used by sky, catalog, and observatory workflows.
	    The model stores declination and right ascension in a typed, serializable structure.
	
	Attributes:
	    type (Optional[str]): Type value stored by the model.
	    declination (Optional[float]): Declination value stored by the model.
	    right_ascension (Optional[float]): Right ascension value stored by the model."""
	type: Optional[ str ]
	declination: Optional[ float ]
	right_ascension: Optional[ float ]

class Tool( BaseModel ):
	"""Tool model.
	
	Purpose:
	    Represents the shared base descriptor for callable tools. The model stores a tool name,
	    provider-facing type, and short description used by function-calling workflows.
	
	Attributes:
	    name (Optional[str]): Name value stored by the model.
	    type (Optional[str]): Type value stored by the model.
	    description (Optional[str]): Description value stored by the model."""
	name: Optional[ str ]
	type: Optional[ str ]
	description: Optional[ str ]

class Function( Tool ):
	"""Function model.
	
	Purpose:
	    Extends the base tool descriptor with callable parameter schema and strictness metadata. The
	    model represents a function-style tool declaration independent of any single provider.
	
	Attributes:
	    parameters (Optional[Dict[str, Any]]): Parameters value stored by the model.
	    strict (Optional[bool]): Strict value stored by the model."""
	parameters: Optional[ Dict[ str, Any ] ]
	strict: Optional[ bool ]

class FileSearch( Tool ):
	"""FileSearch model.
	
	Purpose:
	    Represents configuration for a file-search tool. The model stores vector store identifiers,
	    result limits, and optional filters for retrieval workflows.
	
	Attributes:
	    vector_store_ids (Optional[List[str]]): Vector store ids value stored by the model.
	    max_num_results (Optional[int]): Max num results value stored by the model.
	    filters (Optional[Dict[str, Any]]): Filters value stored by the model."""
	vector_store_ids: Optional[ List[ str ] ]
	max_num_results: Optional[ int ]
	filters: Optional[ Dict[ str, Any ] ]

class WebSearch( Tool ):
	"""WebSearch model.
	
	Purpose:
	    Represents configuration for a web-search tool. The model stores search context size and
	    optional user-location metadata used by search-capable provider workflows.
	
	Attributes:
	    type (Optional[str]): Type value stored by the model.
	    search_context_size (Optional[str]): Search context size value stored by the model.
	    user_location (Optional[Any]): User location value stored by the model."""
	type: Optional[ str ]
	search_context_size: Optional[ str ]
	user_location: Optional[ Any ]

class ComputerUse( Tool ):
	"""ComputerUse model.
	
	Purpose:
	    Represents configuration for a computer-use or UI-automation tool. The model stores display
	    dimensions and execution environment metadata for provider tool declarations.
	
	Attributes:
	    type (Optional[str]): Type value stored by the model.
	    display_height (Optional[int]): Display height value stored by the model.
	    display_width (Optional[int]): Display width value stored by the model.
	    environment (Optional[str]): Environment value stored by the model."""
	type: Optional[ str ]
	display_height: Optional[ int ]
	display_width: Optional[ int ]
	environment: Optional[ str ]

class ToolDef( Function ):
	"""ToolDef model.
	
	Purpose:
	    Represents a provider-neutral tool definition bound to a Python callable or object method.
	    The model stores callable metadata, generated parameter schema, provider conversion helpers,
	    and execution behavior for unified tool dispatch.
	
	Attributes:
	    name (Optional[str]): Name value stored by the model.
	    type (Optional[str]): Type value stored by the model.
	    description (Optional[str]): Description value stored by the model.
	    parameters (Optional[Dict[str, Any]]): Parameters value stored by the model.
	    strict (Optional[bool]): Strict value stored by the model.
	    target (Optional[Any]): Target value stored by the model.
	    method (Optional[str]): Method value stored by the model.
	    handler (Optional[Callable[..., Any]]): Handler value stored by the model.
	    category (Optional[str]): Category value stored by the model.
	    source_module (Optional[str]): Source module value stored by the model.
	    source_class (Optional[str]): Source class value stored by the model.
	    callable_name (Optional[str]): Callable name value stored by the model."""
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
		"""Create tool definition from callable.
		
		Purpose:
		    Creates a provider-neutral tool definition from a standalone Python callable. The method
		    derives the callable name, source module, description, parameter schema, strictness flag,
		    and execution handler needed for later tool dispatch.
		
		Args:
		    function (Callable[..., Any]): Callable inspected, wrapped, or converted into a provider-neutral tool schema.
		    name (Optional[str]): Human-readable argument name used in validation error messages.
		    description (Optional[str]): Optional provider-facing description used instead of the callable docstring.
		    category (Optional[str]): Optional grouping value retained in tool metadata.
		    strict (bool): Flag indicating whether provider schema validation should be strict.
		
		Returns:
		    Tool definition that wraps the supplied callable for provider-neutral use.
		
		Raises:
		    Error: Raised after the underlying exception is wrapped with module, cause, and method metadata."""
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
		"""Create tool definition from object method.
		
		Purpose:
		    Creates a provider-neutral tool definition from a method on an existing object instance. The
		    method validates that the target member exists and is callable, then stores the target,
		    method name, source class, source module, and generated parameter schema.
		
		Args:
		    target (Any): Object instance that owns the method being exposed as a tool.
		    method (str): Name of the target method exposed through the tool definition.
		    name (Optional[str]): Human-readable argument name used in validation error messages.
		    description (Optional[str]): Optional provider-facing description used instead of the callable docstring.
		    category (Optional[str]): Optional grouping value retained in tool metadata.
		    strict (bool): Flag indicating whether provider schema validation should be strict.
		
		Returns:
		    Tool definition that resolves and wraps a named method on the supplied object instance.
		
		Raises:
		    Error: Raised after the underlying exception is wrapped with module, cause, and method metadata."""
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
		"""Resolve bound callable.
		
		Purpose:
		    Resolves the executable Python callable represented by the tool definition. The method
		    returns a direct handler when one is stored or retrieves the named method from the stored
		    target object after validating the binding.
		
		Returns:
		    Python callable bound to this tool definition.
		
		Raises:
		    Error: Raised after the underlying exception is wrapped with module, cause, and method metadata."""
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
		"""Execute bound tool callable.
		
		Purpose:
		    Executes the bound tool callable with keyword arguments and returns a neutral response
		    envelope. The method serializes successful results and converts failures into structured
		    error metadata without exposing provider-specific response objects.
		
		Args:
		    arguments (Optional[Dict[str, Any]]): Keyword arguments passed to the resolved callable during tool execution.
		
		Returns:
		    Dictionary containing execution status, serialized data, error information, and tool
		    metadata."""
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
		"""Export neutral tool dictionary.
		
		Purpose:
		    Exports the tool definition as a provider-neutral dictionary for inspection, persistence, or
		    application-level routing. The method includes schema fields, source metadata, method
		    binding details, and category information.
		
		Returns:
		    Provider-neutral dictionary representation of this tool definition.
		
		Raises:
		    Error: Raised after the underlying exception is wrapped with module, cause, and method metadata."""
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
		"""Export OpenAI tool schema.
		
		Purpose:
		    Builds an OpenAI-compatible function tool declaration from the neutral tool definition. The
		    method supplies a function name, description, parameters object, and strictness flag using
		    safe defaults when optional schema fields are absent.
		
		Returns:
		    OpenAI-compatible function-tool schema for this tool definition.
		
		Raises:
		    Error: Raised after the underlying exception is wrapped with module, cause, and method metadata."""
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
		"""Export Grok tool schema.
		
		Purpose:
		    Builds a Grok-compatible function tool declaration using the same schema shape used for
		    OpenAI function tools. The method preserves the neutral tool definition while reusing the
		    shared provider conversion path.
		
		Returns:
		    Grok-compatible function-tool schema for this tool definition.
		
		Raises:
		    Error: Raised after the underlying exception is wrapped with module, cause, and method metadata."""
		try:
			return self.to_openai( )
		except Exception as e:
			exception = Error( e )
			exception.module = 'models'
			exception.cause = 'ToolDef'
			exception.method = 'to_grok( self ) -> Dict[ str, Any ]'
			raise exception
	
	def to_gemini( self ) -> Dict[ str, Any ]:
		"""Export Gemini tool schema.
		
		Purpose:
		    Builds a Gemini-compatible function declaration from the neutral tool definition. The method
		    returns the function name, description, and parameters object in the schema shape expected
		    by Gemini tool configuration.
		
		Returns:
		    Gemini-compatible function declaration for this tool definition.
		
		Raises:
		    Error: Raised after the underlying exception is wrapped with module, cause, and method metadata."""
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

