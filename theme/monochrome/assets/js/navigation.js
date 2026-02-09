/**
 * Monochrome — Navigation
 *
 * Handles mobile menu toggle and active nav link detection based on domain.
 */
( function () {
	'use strict';

	/**
	 * Set the active nav link based on the current hostname.
	 */
	function setActiveNavLink() {
		var hostname = window.location.hostname;
		var links = document.querySelectorAll( '.nav-link[data-domain]' );

		for ( var i = 0; i < links.length; i++ ) {
			var link = links[ i ];
			if ( hostname === link.getAttribute( 'data-domain' ) ) {
				link.classList.add( 'nav-link--active' );
			} else {
				link.classList.remove( 'nav-link--active' );
			}
		}
	}

	/**
	 * Set up the mobile menu toggle.
	 */
	function initMobileMenu() {
		var toggle = document.querySelector( '.mobile-menu-toggle' );
		var menu = document.querySelector( '.mobile-menu' );

		if ( ! toggle || ! menu ) {
			return;
		}

		toggle.addEventListener( 'click', function () {
			var isOpen = toggle.getAttribute( 'aria-expanded' ) === 'true';

			if ( isOpen ) {
				closeMenu( toggle, menu );
			} else {
				openMenu( toggle, menu );
			}
		} );

		// Close on Escape key.
		document.addEventListener( 'keydown', function ( e ) {
			if ( e.key === 'Escape' && menu.classList.contains( 'is-open' ) ) {
				closeMenu( toggle, menu );
				toggle.focus();
			}
		} );

		// Close when clicking a nav link inside the menu.
		var menuLinks = menu.querySelectorAll( '.mobile-menu__link' );
		for ( var i = 0; i < menuLinks.length; i++ ) {
			menuLinks[ i ].addEventListener( 'click', function () {
				closeMenu( toggle, menu );
			} );
		}
	}

	function openMenu( toggle, menu ) {
		toggle.setAttribute( 'aria-expanded', 'true' );
		toggle.setAttribute( 'aria-label', 'Close menu' );
		menu.removeAttribute( 'hidden' );
		// Force reflow before adding class for transition.
		menu.offsetHeight;
		menu.classList.add( 'is-open' );
		document.body.style.overflow = 'hidden';
	}

	function closeMenu( toggle, menu ) {
		toggle.setAttribute( 'aria-expanded', 'false' );
		toggle.setAttribute( 'aria-label', 'Open menu' );
		menu.classList.remove( 'is-open' );
		document.body.style.overflow = '';
		// Re-hide after transition completes.
		menu.addEventListener( 'transitionend', function handler() {
			if ( ! menu.classList.contains( 'is-open' ) ) {
				menu.setAttribute( 'hidden', '' );
			}
			menu.removeEventListener( 'transitionend', handler );
		} );
	}

	document.addEventListener( 'DOMContentLoaded', function () {
		setActiveNavLink();
		initMobileMenu();
	} );
} )();
