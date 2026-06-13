( function()
{
	"use strict";
	
	function addExternalLinkBehavior()
	{
		const links = document.querySelectorAll( "a[href^='http']" );
		links.forEach( function( link )
		{
			const href = link.getAttribute( "href" );
			if( !href )
			{
				return;
			}
			if( href.indexOf( window.location.hostname ) === -1 )
			{
				link.setAttribute( "target", "_blank" );
				link.setAttribute( "rel", "noopener noreferrer" );
			}
		} );
	}
	
	function addCodeBlockLabels()
	{
		const blocks = document.querySelectorAll( "div.highlight" );
		blocks.forEach( function( block )
		{
			const code = block.querySelector( "code" );
			if( !code )
			{
				return;
			}
			const classList = Array.from( code.classList );
			const languageClass = classList.find( function( item )
			{
				return item.indexOf( "language-" ) === 0;
			} );
			if( !languageClass )
			{
				return;
			}
			const language = languageClass.replace( "language-", "" );
			if( !language || block.querySelector( ".fonky-code-label" ) )
			{
				return;
			}
			const label = document.createElement( "div" );
			label.className = "fonky-code-label";
			label.textContent = language;
			block.insertBefore( label, block.firstChild );
		} );
	}
	
	function addTableWrappers()
	{
		const tables = document.querySelectorAll( ".md-typeset table:not([data-fonky-wrapped])" );
		tables.forEach( function( table )
		{
			const parent = table.parentElement;
			if( !parent || parent.classList.contains( "fonky-table-wrapper" ) )
			{
				return;
			}
			const wrapper = document.createElement( "div" );
			wrapper.className = "fonky-table-wrapper";
			table.setAttribute( "data-fonky-wrapped", "true" );
			parent.insertBefore( wrapper, table );
			wrapper.appendChild( table );
		} );
	}
	
	function markActiveApiPage()
	{
		const path = window.location.pathname.toLowerCase();
		if( path.indexOf( "/api/" ) === -1 )
		{
			return;
		}
		document.documentElement.classList.add( "fonky-api-page" );
	}
	
	function enhancePage()
	{
		addExternalLinkBehavior();
		addCodeBlockLabels();
		addTableWrappers();
		markActiveApiPage();
	}
	
	document.addEventListener( "DOMContentLoaded", enhancePage );
	if( typeof document$ !== "undefined" )
	{
		document$.subscribe( enhancePage );
	}
} )();