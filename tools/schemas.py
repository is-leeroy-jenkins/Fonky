'''
  ******************************************************************************************
      Assembly:                fonky
      Filename:                schemas.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="schemas.py" company="Terry D. Eppler">

	     schemas.py
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
    schemas.py
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

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
# PARAMETER SCHEMA
# ==========================================================================================

class ToolParameter( BaseModel ):
	'''

		Purpose:
		--------
		Represents one provider-neutral JSON-schema parameter used by a callable Fonky
		tool. The object deliberately avoids OpenAI, Gemini, Grok, or LangChain-specific
		fields so it can be translated later by provider adapters.

		Attributes:
		-----------
		name: str
			The parameter name exposed to callers.

		type: str
			The JSON-schema type, such as string, integer, number, boolean, array, or object.

		description: str
			Human-readable description of the parameter.

		required: bool
			Whether the parameter is included in the parent schema required list.

		enum: Optional[List[Any]]
			Optional list of accepted literal values.

		default: Optional[Any]
			Optional default value for UI construction or adapter-side defaults.

		items: Optional[Dict[str, Any]]
			Optional JSON schema for array item definitions.

		properties: Optional[Dict[str, Any]]
			Optional JSON schema for nested object properties.

		additional_properties: Optional[bool]
			Optional JSON-schema additionalProperties flag for nested object parameters.

		minimum: Optional[float]
			Optional numeric minimum constraint.

		maximum: Optional[float]
			Optional numeric maximum constraint.

		min_length: Optional[int]
			Optional string minimum length constraint.

		max_length: Optional[int]
			Optional string maximum length constraint.

		pattern: Optional[str]
			Optional regular expression constraint for string values.

	'''
	name: str
	type: str
	description: str
	required: bool = True
	enum: Optional[ List[ Any ] ] = None
	default: Optional[ Any ] = None
	items: Optional[ Dict[ str, Any ] ] = None
	properties: Optional[ Dict[ str, Any ] ] = None
	additional_properties: Optional[ bool ] = None
	minimum: Optional[ float ] = None
	maximum: Optional[ float ] = None
	min_length: Optional[ int ] = None
	max_length: Optional[ int ] = None
	pattern: Optional[ str ] = None
	
	def to_property_schema( self ) -> Dict[ str, Any ]:
		'''

			Purpose:
			--------
			Convert the parameter object into a provider-neutral JSON-schema property
			dictionary.

			Parameters:
			-----------
			None

			Returns:
			--------
			Dict[str, Any]: JSON-schema-compatible property dictionary.

		'''
		schema = {
				'type': self.type,
				'description': self.description,
		}
		
		if self.enum is not None:
			schema[ 'enum' ] = self.enum
		
		if self.default is not None:
			schema[ 'default' ] = self.default
		
		if self.items is not None:
			schema[ 'items' ] = self.items
		
		if self.properties is not None:
			schema[ 'properties' ] = self.properties
		
		if self.additional_properties is not None:
			schema[ 'additionalProperties' ] = self.additional_properties
		
		if self.minimum is not None:
			schema[ 'minimum' ] = self.minimum
		
		if self.maximum is not None:
			schema[ 'maximum' ] = self.maximum
		
		if self.min_length is not None:
			schema[ 'minLength' ] = self.min_length
		
		if self.max_length is not None:
			schema[ 'maxLength' ] = self.max_length
		
		if self.pattern is not None:
			schema[ 'pattern' ] = self.pattern
		
		return schema
	
	def to_dict( self ) -> Dict[ str, Any ]:
		'''

			Purpose:
			--------
			Convert the parameter object into a JSON-safe dictionary preserving Fonky's
			neutral parameter metadata.

			Parameters:
			-----------
			None

			Returns:
			--------
			Dict[str, Any]: JSON-safe parameter dictionary.

		'''
		return {
				'name': self.name,
				'type': self.type,
				'description': self.description,
				'required': self.required,
				'schema': self.to_property_schema( ),
		}

# ==========================================================================================
# TOOL SCHEMA
# ==========================================================================================

class ToolSchema( BaseModel ):
	'''

		Purpose:
		--------
		Represents the canonical provider-neutral schema for one callable Fonky tool.
		Provider-specific adapters should translate this schema into OpenAI, Gemini, Grok,
		LangChain, or local model formats.

		Attributes:
		-----------
		name: str
			Callable tool name.

		description: str
			Tool description shown to the model, UI, or caller.

		parameters: List[ToolParameter]
			Parameter definitions used to build the JSON schema.

		category: Optional[str]
			Optional logical category such as fetcher, loader, scraper, processor, or utility.

		tags: List[str]
			Optional searchable labels for filtering and UI grouping.

		metadata: Dict[str, Any]
			Optional provider-neutral metadata used by registries or Streamlit controls.

	'''
	name: str
	description: str
	parameters: List[ ToolParameter ] = Field( default_factory=list )
	category: Optional[ str ] = None
	tags: List[ str ] = Field( default_factory=list )
	metadata: Dict[ str, Any ] = Field( default_factory=dict )
	
	def to_json_schema( self ) -> Dict[ str, Any ]:
		'''

			Purpose:
			--------
			Build the provider-neutral JSON-schema object describing this tool's arguments.

			Parameters:
			-----------
			None

			Returns:
			--------
			Dict[str, Any]: JSON-schema-compatible argument schema.

		'''
		properties = { parameter.name: parameter.to_property_schema( ) for parameter in
		               self.parameters }
		required = [ parameter.name for parameter in self.parameters if parameter.required ]
		
		return {
				'type': 'object',
				'properties': properties,
				'required': required,
				'additionalProperties': False,
		}
	
	def to_schema( self ) -> Dict[ str, Any ]:
		'''

			Purpose:
			--------
			Build Fonky's canonical provider-neutral tool schema.

			Parameters:
			-----------
			None

			Returns:
			--------
			Dict[str, Any]: Provider-neutral Fonky tool schema.

		'''
		return {
				'name': self.name,
				'description': self.description,
				'category': self.category,
				'tags': list( self.tags ),
				'metadata': dict( self.metadata ),
				'parameters': self.to_json_schema( ),
		}
	
	def to_function_schema( self ) -> Dict[ str, Any ]:
		'''

			Purpose:
			--------
			Build a neutral function schema without a provider-specific tool envelope.

			Parameters:
			-----------
			None

			Returns:
			--------
			Dict[str, Any]: Provider-neutral function schema.

		'''
		return {
				'name': self.name,
				'description': self.description,
				'parameters': self.to_json_schema( ),
		}
	
	def to_parameter_map( self ) -> Dict[ str, ToolParameter ]:
		'''

			Purpose:
			--------
			Return the schema parameters keyed by parameter name for validation, lookup,
			adapter construction, or Streamlit control generation.

			Parameters:
			-----------
			None

			Returns:
			--------
			Dict[str, ToolParameter]: Parameter map keyed by parameter name.

		'''
		return { parameter.name: parameter for parameter in self.parameters }

# ==========================================================================================
# SCHEMA FACTORY
# ==========================================================================================

class SchemaFactory:
	'''

		Purpose:
		--------
		Factory for constructing common provider-neutral Fonky tool parameters and tool
		schemas using one consistent internal contract.

		Attributes:
		-----------
		None

		Methods:
		--------
		string(...): Create a string parameter.
		integer(...): Create an integer parameter.
		number(...): Create a number parameter.
		boolean(...): Create a boolean parameter.
		array(...): Create an array parameter.
		object(...): Create an object parameter.
		function(...): Create a ToolSchema object.

	'''
	
	@staticmethod
	def string( name: str, description: str, required: bool = True,
			enum: Optional[ List[ Any ] ] = None,
			default: Optional[ Any ] = None, min_length: Optional[ int ] = None,
			max_length: Optional[ int ] = None, pattern: Optional[ str ] = None ) -> ToolParameter:
		'''

			Purpose:
			--------
			Create a JSON-schema string parameter.

			Parameters:
			-----------
			name (str): Parameter name.
			description (str): Parameter description.
			required (bool): Whether the parameter is required.
			enum (Optional[List[Any]]): Optional accepted literal values.
			default (Optional[Any]): Optional default value.
			min_length (Optional[int]): Optional minimum string length.
			max_length (Optional[int]): Optional maximum string length.
			pattern (Optional[str]): Optional regular expression constraint.

			Returns:
			--------
			ToolParameter: Configured string parameter.

		'''
		throw_if( 'name', name )
		throw_if( 'description', description )
		return ToolParameter( name=name, type='string', description=description, required=required,
			enum=enum, default=default, min_length=min_length, max_length=max_length,
			pattern=pattern )
	
	@staticmethod
	def integer( name: str, description: str, required: bool = True,
			default: Optional[ int ] = None,
			minimum: Optional[ int ] = None, maximum: Optional[ int ] = None ) -> ToolParameter:
		'''

			Purpose:
			--------
			Create a JSON-schema integer parameter.

			Parameters:
			-----------
			name (str): Parameter name.
			description (str): Parameter description.
			required (bool): Whether the parameter is required.
			default (Optional[int]): Optional default integer value.
			minimum (Optional[int]): Optional minimum value.
			maximum (Optional[int]): Optional maximum value.

			Returns:
			--------
			ToolParameter: Configured integer parameter.

		'''
		throw_if( 'name', name )
		throw_if( 'description', description )
		return ToolParameter( name=name, type='integer', description=description, required=required,
			default=default, minimum=minimum, maximum=maximum )
	
	@staticmethod
	def number( name: str, description: str, required: bool = True,
			default: Optional[ float ] = None,
			minimum: Optional[ float ] = None, maximum: Optional[ float ] = None ) -> ToolParameter:
		'''

			Purpose:
			--------
			Create a JSON-schema number parameter.

			Parameters:
			-----------
			name (str): Parameter name.
			description (str): Parameter description.
			required (bool): Whether the parameter is required.
			default (Optional[float]): Optional default numeric value.
			minimum (Optional[float]): Optional minimum value.
			maximum (Optional[float]): Optional maximum value.

			Returns:
			--------
			ToolParameter: Configured number parameter.

		'''
		throw_if( 'name', name )
		throw_if( 'description', description )
		return ToolParameter( name=name, type='number', description=description, required=required,
			default=default, minimum=minimum, maximum=maximum )
	
	@staticmethod
	def boolean( name: str, description: str, required: bool = True,
			default: Optional[ bool ] = None ) -> ToolParameter:
		'''

			Purpose:
			--------
			Create a JSON-schema boolean parameter.

			Parameters:
			-----------
			name (str): Parameter name.
			description (str): Parameter description.
			required (bool): Whether the parameter is required.
			default (Optional[bool]): Optional default boolean value.

			Returns:
			--------
			ToolParameter: Configured boolean parameter.

		'''
		throw_if( 'name', name )
		throw_if( 'description', description )
		return ToolParameter( name=name, type='boolean', description=description, required=required,
			default=default )
	
	@staticmethod
	def array( name: str, description: str, items: Optional[ Dict[ str, Any ] ] = None,
			required: bool = True, default: Optional[ Any ] = None ) -> ToolParameter:
		'''

			Purpose:
			--------
			Create a JSON-schema array parameter.

			Parameters:
			-----------
			name (str): Parameter name.
			description (str): Parameter description.
			items (Optional[Dict[str, Any]]): JSON schema describing array items.
			required (bool): Whether the parameter is required.
			default (Optional[Any]): Optional default array value.

			Returns:
			--------
			ToolParameter: Configured array parameter.

		'''
		throw_if( 'name', name )
		throw_if( 'description', description )
		item_schema = items if items is not None else { 'type': 'string' }
		return ToolParameter( name=name, type='array', description=description, required=required,
			items=item_schema, default=default )
	
	@staticmethod
	def object( name: str, description: str, properties: Optional[ Dict[ str, Any ] ] = None,
			required: bool = True, additional_properties: bool = False,
			default: Optional[ Any ] = None ) -> ToolParameter:
		'''

			Purpose:
			--------
			Create a JSON-schema object parameter.

			Parameters:
			-----------
			name (str): Parameter name.
			description (str): Parameter description.
			properties (Optional[Dict[str, Any]]): Nested object properties.
			required (bool): Whether the parameter is required.
			additional_properties (bool): Whether undeclared nested properties are allowed.
			default (Optional[Any]): Optional default object value.

			Returns:
			--------
			ToolParameter: Configured object parameter.

		'''
		throw_if( 'name', name )
		throw_if( 'description', description )
		return ToolParameter( name=name, type='object', description=description, required=required,
			properties=properties or { }, additional_properties=additional_properties,
			default=default )
	
	@staticmethod
	def function( name: str, description: str, parameters: Optional[ List[ ToolParameter ] ] = None,
			category: Optional[ str ] = None, tags: Optional[ List[ str ] ] = None,
			metadata: Optional[ Dict[ str, Any ] ] = None ) -> ToolSchema:
		'''

			Purpose:
			--------
			Create a complete provider-neutral Fonky tool schema.

			Parameters:
			-----------
			name (str): Tool name.
			description (str): Tool description.
			parameters (Optional[List[ToolParameter]]): Parameter definitions.
			category (Optional[str]): Optional logical category.
			tags (Optional[List[str]]): Optional searchable labels.
			metadata (Optional[Dict[str, Any]]): Optional provider-neutral metadata.

			Returns:
			--------
			ToolSchema: Configured provider-neutral tool schema.

		'''
		throw_if( 'name', name )
		throw_if( 'description', description )
		return ToolSchema( name=name, description=description, parameters=parameters or [ ],
			category=category, tags=tags or [ ], metadata=metadata or { } )

# ==========================================================================================
# MODULE-LEVEL BUILDERS
# ==========================================================================================

def build_tool_schema( name: str, description: str,
		parameters: Optional[ List[ ToolParameter ] ] = None,
		category: Optional[ str ] = None, tags: Optional[ List[ str ] ] = None,
		metadata: Optional[ Dict[ str, Any ] ] = None ) -> Dict[ str, Any ]:
	'''

		Purpose:
		--------
		Build Fonky's canonical provider-neutral tool schema.

		Parameters:
		-----------
		name (str): Tool name.
		description (str): Tool description.
		parameters (Optional[List[ToolParameter]]): Optional parameter definitions.
		category (Optional[str]): Optional logical category.
		tags (Optional[List[str]]): Optional searchable labels.
		metadata (Optional[Dict[str, Any]]): Optional provider-neutral metadata.

		Returns:
		--------
		Dict[str, Any]: Provider-neutral Fonky tool schema.

	'''
	schema = SchemaFactory.function( name=name, description=description, parameters=parameters,
		category=category, tags=tags, metadata=metadata )
	
	return schema.to_schema( )

def build_function_schema( name: str, description: str,
		parameters: Optional[ List[ ToolParameter ] ] = None,
		category: Optional[ str ] = None, tags: Optional[ List[ str ] ] = None,
		metadata: Optional[ Dict[ str, Any ] ] = None ) -> Dict[ str, Any ]:
	'''

		Purpose:
		--------
		Build a provider-neutral function schema without a provider-specific tool envelope.

		Parameters:
		-----------
		name (str): Function name.
		description (str): Function description.
		parameters (Optional[List[ToolParameter]]): Optional parameter definitions.
		category (Optional[str]): Optional logical category retained in metadata.
		tags (Optional[List[str]]): Optional searchable labels retained in metadata.
		metadata (Optional[Dict[str, Any]]): Optional provider-neutral metadata.

		Returns:
		--------
		Dict[str, Any]: Provider-neutral function schema.

	'''
	schema = SchemaFactory.function( name=name, description=description, parameters=parameters,
		category=category, tags=tags, metadata=metadata )
	
	return schema.to_function_schema( )

def build_argument_schema( parameters: Optional[ List[ ToolParameter ] ] = None ) -> Dict[
	str, Any ]:
	'''

		Purpose:
		--------
		Build a provider-neutral JSON-schema object from a parameter list.

		Parameters:
		-----------
		parameters (Optional[List[ToolParameter]]): Optional parameter definitions.

		Returns:
		--------
		Dict[str, Any]: JSON-schema-compatible argument schema.

	'''
	schema = ToolSchema( name='arguments', description='Argument schema.',
		parameters=parameters or [ ] )
	return schema.to_json_schema( )