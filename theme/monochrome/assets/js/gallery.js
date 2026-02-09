/**
 * Monochrome — Gallery Scroll Animations
 *
 * Uses IntersectionObserver to fade in gallery cards as they enter the viewport.
 * Cards are staggered by 80ms per item for a cascading effect.
 */
( function () {
	'use strict';

	function initGalleryAnimations() {
		var cards = document.querySelectorAll( '.image-card' );

		if ( ! cards.length ) {
			return;
		}

		// If IntersectionObserver is not supported, show all cards immediately.
		if ( ! ( 'IntersectionObserver' in window ) ) {
			for ( var i = 0; i < cards.length; i++ ) {
				cards[ i ].classList.add( 'is-visible' );
			}
			return;
		}

		var visibleCount = 0;

		var observer = new IntersectionObserver( function ( entries ) {
			for ( var i = 0; i < entries.length; i++ ) {
				var entry = entries[ i ];
				if ( entry.isIntersecting ) {
					var card = entry.target;
					var delay = visibleCount * 80;
					visibleCount++;

					// Use closure to capture the card reference.
					( function ( c, d ) {
						setTimeout( function () {
							c.classList.add( 'is-visible' );
						}, d );
					} )( card, delay );

					observer.unobserve( card );
				}
			}
		}, {
			threshold: 0.1
		} );

		for ( var j = 0; j < cards.length; j++ ) {
			observer.observe( cards[ j ] );
		}
	}

	document.addEventListener( 'DOMContentLoaded', initGalleryAnimations );
} )();
