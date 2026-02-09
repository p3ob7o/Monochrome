/**
 * Monochrome — Dark/Light Mode Toggle
 *
 * Runs before paint to prevent flash of wrong color scheme.
 * Reads preference from localStorage, falls back to prefers-color-scheme.
 */
( function () {
	'use strict';

	var STORAGE_KEY = 'monochrome-color-mode';
	var root = document.documentElement;

	/**
	 * Get the user's preferred color mode.
	 * Priority: localStorage > system preference > dark (default).
	 */
	function getPreferredMode() {
		var stored = localStorage.getItem( STORAGE_KEY );
		if ( stored === 'light' || stored === 'dark' ) {
			return stored;
		}
		if ( window.matchMedia && window.matchMedia( '(prefers-color-scheme: light)' ).matches ) {
			return 'light';
		}
		return 'dark';
	}

	/**
	 * Apply color mode to the document.
	 */
	function applyMode( mode ) {
		root.setAttribute( 'data-color-mode', mode );
	}

	/**
	 * Toggle between dark and light mode.
	 */
	function toggleMode() {
		var current = root.getAttribute( 'data-color-mode' ) || 'dark';
		var next = current === 'dark' ? 'light' : 'dark';
		applyMode( next );
		localStorage.setItem( STORAGE_KEY, next );
		updateToggleButtons( next );
	}

	/**
	 * Update all toggle button labels/icons.
	 */
	function updateToggleButtons( mode ) {
		var buttons = document.querySelectorAll( '.color-mode-toggle' );
		for ( var i = 0; i < buttons.length; i++ ) {
			var btn = buttons[ i ];
			var icon = btn.querySelector( '.color-mode-toggle__icon' );
			var label = btn.querySelector( '.color-mode-toggle__label' );
			if ( icon ) {
				// Sun icon when in dark mode (click to switch to light).
				// Moon icon when in light mode (click to switch to dark).
				icon.textContent = mode === 'dark' ? '\u2600' : '\u25D0';
			}
			if ( label ) {
				label.textContent = mode === 'dark' ? 'Light mode' : 'Dark mode';
			}
			btn.setAttribute( 'aria-label',
				mode === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
			);
		}
	}

	// Apply mode immediately (before paint) to prevent flash.
	// Disable transitions during initial application.
	root.classList.add( 'no-transition' );
	var initialMode = getPreferredMode();
	applyMode( initialMode );

	// Remove no-transition class after a tick so transitions work normally.
	requestAnimationFrame( function () {
		requestAnimationFrame( function () {
			root.classList.remove( 'no-transition' );
		} );
	} );

	// Once DOM is ready, set up toggle buttons and system preference listener.
	document.addEventListener( 'DOMContentLoaded', function () {
		updateToggleButtons( initialMode );

		// Bind click handlers to all toggle buttons.
		var buttons = document.querySelectorAll( '.color-mode-toggle' );
		for ( var i = 0; i < buttons.length; i++ ) {
			buttons[ i ].addEventListener( 'click', toggleMode );
		}

		// Listen for system preference changes (only if no stored preference).
		if ( window.matchMedia ) {
			window.matchMedia( '(prefers-color-scheme: light)' ).addEventListener( 'change', function ( e ) {
				if ( ! localStorage.getItem( STORAGE_KEY ) ) {
					var mode = e.matches ? 'light' : 'dark';
					applyMode( mode );
					updateToggleButtons( mode );
				}
			} );
		}
	} );

	// Expose toggle function globally for use in templates.
	window.monochromeToggleColorMode = toggleMode;
} )();
