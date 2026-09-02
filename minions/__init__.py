'''
  ******************************************************************************************
      Assembly:                Name
      Filename:                name.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="guro.py" company="Terry D. Eppler">

	     name.py
	     Copyright ©  2022  Terry Eppler

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
    init.py
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, List, Dict
import config as cfg


def throw_if( name: str, value: object ) -> None:
    """
    Input guard.

    Purpose:
        Validates that a required argument contains a usable value before the surrounding
        workflow continues.

    Args:
        name (str): Name of the argument being validated.
        value (object): Value supplied to the argument.

    Returns:
        None: This function performs validation and does not return a value.
    """
    if not value:
        raise ValueError( f'Argument "{name}" cannot be empty!' )


class Minion( ABC ):
    """
    Provider-neutral AI agent abstraction.

    Purpose:
        Defines the common contract required to configure and execute an AI agent across
        supported providers such as OpenAI, Gemini, xAI, and Anthropic. Provider-specific
        subclasses translate this common state into the native SDK objects required by
        each provider.

        The base class owns configuration and lifecycle behavior that is conceptually
        common across providers while leaving provider-specific agent construction,
        invocation, and streaming behavior to subclasses.

    Args:
        name (str): Human-readable name assigned to the agent.
        model (str): Provider model identifier used by the agent.
        instructions (str): System-level instructions controlling agent behavior.
        tools (list[Callable[..., Any]]): Functions or provider-compatible tools exposed
            to the agent.
        description (str): Human-readable description of the agent's purpose.
        max_turns (int): Maximum number of model/tool iterations allowed for one run.

    Returns:
        None: Initialization creates the configured agent abstraction.
    """
    name: str
    model: str
    instructions: str
    description: str
    max_turns: int
    tools: List[ Callable[ ..., Any ] ]
    context: Dict[ str, Any ]
    provider: Any
    result: Any
    
    def __init__( self, name: str, model: str, instructions: str,
		    tools: list[ Callable[ ..., Any ] ], description: str='', max_turns: int=10 ) -> None:
	    """
		Initialize the provider-neutral agent.

		Purpose:
			Validates and stores the configuration shared by all supported agent
			providers.

		Args:
			name (str): Human-readable agent name.
			model (str): Model identifier used by the provider.
			instructions (str): System-level agent instructions.
			tools (list[Callable[..., Any]]): Tools available to the agent.
			description (str): Optional description of the agent's purpose.
			max_turns (int): Maximum number of agent execution turns.

		Returns:
			None: Initialization stores validated agent configuration.
		"""
	    throw_if( 'name', name )
	    throw_if( 'model', model )
	    throw_if( 'instructions', instructions )
	    throw_if( 'tools', tools )
	    
	    if max_turns <= 0:
		    raise ValueError( 'Argument "max_turns" must be greater than zero!' )
	    
	    self.name = name
	    self.model = model
	    self.instructions = instructions
	    self.tools = tools
	    self.description = description
	    self.max_turns = max_turns
	    self.context = { }
	    self.provider = None
	    self.result = None


    def add_tool( self, tool: Callable[ ..., Any ] ) -> None:
        """
        Add a tool to the agent.

        Purpose:
            Adds a callable tool to the collection exposed to the agent.

        Args:
            tool (Callable[..., Any]): Function or callable to register as an agent tool.

        Returns:
            None: The tool collection is modified in place.
        """
        throw_if( 'tool', tool )
        if tool not in self.tools:
            self.tools.append( tool )


    def remove_tool( self, tool: Callable[ ..., Any ] ) -> None:
        """
        Remove a tool from the agent.

        Purpose:
            Removes a previously registered callable from the agent tool collection.

        Args:
            tool (Callable[..., Any]): Tool to remove from the agent.

        Returns:
            None: The tool collection is modified in place.
        """
        throw_if( 'tool', tool )
        if tool in self.tools:
            self.tools.remove( tool )


    def set_context( self, key: str, value: Any ) -> None:
        """
        Set an agent context value.

        Purpose:
            Stores provider-neutral runtime state that may be consumed by tools,
            provider adapters, sessions, or orchestration logic.

        Args:
            key (str): Context key.
            value (Any): Context value associated with the key.

        Returns:
            None: The context collection is modified in place.
        """
        throw_if( 'key', key )
        self.context[ key ] = value


    def get_context( self, key: str ) -> Any:
        """
        Get an agent context value.

        Purpose:
            Retrieves a runtime value previously assigned to the agent context.

        Args:
            key (str): Context key to retrieve.

        Returns:
            Any: Stored context value, or None when the key does not exist.
        """
        throw_if( 'key', key )

        return self.context.get( key )


    def clear_context( self ) -> None:
        """
        Clear agent runtime context.

        Purpose:
            Removes all provider-neutral runtime state associated with the agent.

        Args:
            None.

        Returns:
            None: The context collection is cleared in place.
        """
        self.context.clear( )


    @abstractmethod
    def create( self ) -> Any:
        """
        Create the provider-specific agent.

        Purpose:
            Converts the provider-neutral configuration stored by this class into the
            native agent, client, chat, or runtime object required by the provider SDK.

        Args:
            None.

        Returns:
            Any: Provider-specific agent or execution object.
        """
        raise NotImplementedError


    @abstractmethod
    def run( self, prompt: str ) -> Any:
        """
        Execute the agent.

        Purpose:
            Executes the provider-specific agent using the supplied user prompt and
            returns the provider result.

        Args:
            prompt (str): User input supplied to the agent.

        Returns:
            Any: Provider execution result.
        """
        raise NotImplementedError


    @abstractmethod
    async def run_async( self, prompt: str ) -> Any:
        """
        Execute the agent asynchronously.

        Purpose:
            Executes the provider-specific agent asynchronously using the supplied
            user prompt.

        Args:
            prompt (str): User input supplied to the agent.

        Returns:
            Any: Provider execution result.
        """
        raise NotImplementedError


    @abstractmethod
    def stream( self, prompt: str ) -> Any:
        """
        Stream an agent execution.

        Purpose:
            Starts provider-specific streaming execution and returns the provider's
            streaming iterator or event stream.

        Args:
            prompt (str): User input supplied to the agent.

        Returns:
            Any: Provider-specific streaming result.
        """
        raise NotImplementedError


    def reset( self ) -> None:
        """
        Reset transient agent state.

        Purpose:
            Clears runtime context and execution results while preserving the permanent
            agent configuration and registered tools.

        Args:
            None.

        Returns:
            None: Transient state is reset in place.
        """
        self.context.clear( )
        self.result = None


    def to_dict( self ) -> dict[ str, Any ]:
        """
        Export agent configuration.

        Purpose:
            Returns a provider-neutral representation of the current agent configuration
            suitable for inspection, logging, serialization, or documentation.

        Args:
            None.

        Returns:
            dict[str, Any]: Provider-neutral agent configuration.
        """
        return { 'name': self.name, 'model': self.model, 'instructions': self.instructions,
		        'description': self.description, 'max_turns': self.max_turns, 'tools': self.tools,
		        'context': self.context, }
