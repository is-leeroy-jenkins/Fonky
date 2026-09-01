( function()
{
    "use strict";

    function createElement( tag, className, text )
    {
        const element = document.createElement( tag );
        element.className = className || "";
        element.textContent = text || "";
        return element;
    }

    function isApiPage()
    {
        return Boolean( document.querySelector( ".doc-object, .doc-heading" ) );
    }

    function addBackToTop()
    {
        if( document.querySelector( ".fonky-back-to-top" ) )
        {
            return;
        }

        const button = createElement( "button", "fonky-back-to-top", "↑ Top" );
        button.type = "button";

        button.addEventListener( "click", function()
        {
            window.scrollTo( { top: 0, behavior: "smooth" } );
        } );

        window.addEventListener( "scroll", function()
        {
            button.classList.toggle(
                "fonky-back-to-top--visible",
                window.scrollY > 500 );
        } );

        document.body.appendChild( button );
    }

    function addCodeBadges()
    {
        document.querySelectorAll( "pre > code[class*='language-']" ).forEach( function( code )
        {
            const pre = code.parentElement;

            if( !pre || pre.querySelector( ".fonky-code-badge" ) )
            {
                return;
            }

            const languageClass = Array.from( code.classList ).find( function( value )
            {
                return value.startsWith( "language-" );
            } );

            if( !languageClass )
            {
                return;
            }

            pre.classList.add( "fonky-code-block" );
            pre.appendChild(
                createElement(
                    "span",
                    "fonky-code-badge",
                    languageClass.replace( "language-", "" ) ) );
        } );
    }

    function addApiTools()
    {
        if( !isApiPage() )
        {
            return;
        }

        const main = document.querySelector( ".md-content__inner" );

        if( !main || main.querySelector( ".fonky-api-tools" ) )
        {
            return;
        }

        const tools = createElement( "section", "fonky-api-tools", "" );
        const title = createElement( "div", "fonky-api-tools__title", "API Tools" );
        const filter = createElement( "input", "fonky-api-filter", "" );
        const status = createElement( "div", "fonky-api-filter-status", "" );
        const row = createElement( "div", "fonky-api-toggle-row", "" );
        const expand = createElement( "button", "fonky-api-button", "Expand all" );
        const collapse = createElement( "button", "fonky-api-button", "Collapse all" );

        filter.type = "search";
        filter.placeholder = "Filter classes, methods, functions, or text...";
        expand.type = "button";
        collapse.type = "button";

        tools.appendChild( title );
        tools.appendChild( filter );
        tools.appendChild( status );
        row.appendChild( expand );
        row.appendChild( collapse );
        tools.appendChild( row );

        const h1 = main.querySelector( "h1" );

        if( h1 && h1.nextSibling )
        {
            h1.parentNode.insertBefore( tools, h1.nextSibling );
        }
        else
        {
            main.insertBefore( tools, main.firstChild );
        }

        filter.addEventListener( "input", function()
        {
            const query = filter.value.trim().toLowerCase();
            const objects = Array.from( document.querySelectorAll( ".doc-object" ) );
            let visible = 0;

            objects.forEach( function( object )
            {
                const matches = !query ||
                    ( object.textContent || "" ).toLowerCase().includes( query );

                object.classList.toggle( "fonky-api-object-hidden", !matches );

                if( matches )
                {
                    visible += 1;
                }
            } );

            status.textContent = query
                ? `${ visible } matching API section${ visible === 1 ? "" : "s" }`
                : "";
        } );

        expand.addEventListener( "click", function()
        {
            document.querySelectorAll( "details" ).forEach( function( details )
            {
                details.open = true;
            } );
        } );

        collapse.addEventListener( "click", function()
        {
            document.querySelectorAll( "details" ).forEach( function( details )
            {
                details.open = false;
            } );
        } );
    }

    function initialize()
    {
        addBackToTop();
        addCodeBadges();
        addApiTools();
    }

    if( document.readyState === "loading" )
    {
        document.addEventListener( "DOMContentLoaded", initialize );
    }
    else
    {
        initialize();
    }

    if( window.document$ && typeof window.document$.subscribe === "function" )
    {
        window.document$.subscribe( initialize );
    }
} )();
