'''
  ******************************************************************************************
      Assembly:                Fonky
      Filename:                tools.py
      Author:                  Terry D. Eppler
      Created:                 09-02-2026

      Last Modified By:        Terry D. Eppler
      Last Modified On:        09-02-2026
  ******************************************************************************************
  <summary>
    Provides the Anthropic Claude function-tool interface for Fonky.

    Purpose:
        Exposes the complete Fonky tool surface as Anthropic ``beta_tool`` objects without
        duplicating the provider wrappers already maintained by the GPT integration. Each OpenAI
        ``FunctionTool`` is unwrapped to its original typed Fonky callable and registered with
        Anthropic so Claude receives the same function name, signature, documentation, and
        delegated implementation.
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

from typing import Any

from agents import FunctionTool
from anthropic import beta_tool

from ..config import throw_if
from ..gpt import tools as _gpt_tools


# ==========================================================================================
# CLAUDE TOOL REGISTRATION
# ==========================================================================================

def _create_claude_tool( name: str, source_tool: FunctionTool ) -> Any:
    """Create an Anthropic tool from an existing Fonky function tool.

    Purpose:
        Restores the original typed Python callable stored by the OpenAI Agents SDK wrapper and
        registers that callable with Anthropic's ``beta_tool`` decorator. This preserves Fonky's
        existing signatures, docstrings, provider delegation, validation, defaults, and return
        behavior while avoiding a duplicated Claude-specific implementation for every tool.

    Args:
        name (str): Public Fonky tool name used by the provider integration.
        source_tool (FunctionTool): Existing OpenAI Agents SDK tool that retains the original
            Fonky callable through ``__wrapped__``.

    Returns:
        Any: Anthropic beta function-tool object generated from the original Fonky callable.

    Raises:
        ValueError: If the tool name is empty or the source tool does not expose its wrapped
            callable.
    """
    throw_if( 'name', name )
    throw_if( 'source_tool', source_tool )

    _callable = getattr( source_tool, '__wrapped__', None )
    if _callable is None or not callable( _callable ):
        raise ValueError( f'Fonky tool "{name}" does not expose a wrapped callable!' )

    return beta_tool( _callable )


def _register_tools( ) -> tuple[ list[ Any ], list[ str ] ]:
    """Register all current Fonky GPT tools for Claude.

    Purpose:
        Discovers the OpenAI ``FunctionTool`` objects exported by ``fonky.gpt.tools``, unwraps
        each one to the original Fonky callable, converts it to an Anthropic beta tool, and binds
        the converted object into this module under the same public name. The generated collection
        keeps Claude coverage synchronized automatically whenever the GPT tool surface changes.

    Args:
        None.

    Returns:
        tuple[list[Any], list[str]]: Ordered Anthropic tool collection and corresponding exported
            public names.
    """
    _registered: list[ Any ] = [ ]
    _names: list[ str ] = [ ]

    for _name, _value in vars( _gpt_tools ).items( ):
        if _name.startswith( '_' ):
            continue

        if not isinstance( _value, FunctionTool ):
            continue

        _tool = _create_claude_tool( _name, _value )
        globals( )[ _name ] = _tool
        _registered.append( _tool )
        _names.append( _name )

    return _registered, _names


TOOLS, _TOOL_NAMES = _register_tools( )
TOOL_COUNT: int = len( TOOLS )

__all__: list[ str ] = [
    *_TOOL_NAMES,
    'TOOLS',
    'TOOL_COUNT',
]
