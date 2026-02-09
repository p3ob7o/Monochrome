/**
 * Monochrome — Lightbox
 *
 * Full-screen image viewer for the photo detail page.
 * Opens when clicking the featured image. Supports keyboard
 * navigation (Escape to close, arrows for prev/next post).
 */
( function () {
	'use strict';

	var lightbox = null;
	var lightboxImage = null;
	var prevBtn = null;
	var nextBtn = null;
	var prevUrl = null;
	var nextUrl = null;

	/**
	 * Create the lightbox DOM elements.
	 */
	function createLightbox() {
		lightbox = document.createElement( 'div' );
		lightbox.className = 'lightbox';
		lightbox.setAttribute( 'role', 'dialog' );
		lightbox.setAttribute( 'aria-label', 'Image lightbox' );

		lightbox.innerHTML =
			'<button class="lightbox__close" type="button" aria-label="Close lightbox">&times;</button>' +
			'<button class="lightbox__nav lightbox__nav--prev" type="button" aria-label="Previous photo">&#8592;</button>' +
			'<img class="lightbox__image" src="" alt="" />' +
			'<button class="lightbox__nav lightbox__nav--next" type="button" aria-label="Next photo">&#8594;</button>';

		document.body.appendChild( lightbox );

		lightboxImage = lightbox.querySelector( '.lightbox__image' );
		prevBtn = lightbox.querySelector( '.lightbox__nav--prev' );
		nextBtn = lightbox.querySelector( '.lightbox__nav--next' );
		var closeBtn = lightbox.querySelector( '.lightbox__close' );

		// Close on X button click.
		closeBtn.addEventListener( 'click', closeLightbox );

		// Close on backdrop click (not on the image itself).
		lightbox.addEventListener( 'click', function ( e ) {
			if ( e.target === lightbox ) {
				closeLightbox();
			}
		} );

		// Keyboard navigation.
		document.addEventListener( 'keydown', function ( e ) {
			if ( ! lightbox.classList.contains( 'is-open' ) ) {
				return;
			}

			if ( e.key === 'Escape' ) {
				closeLightbox();
			} else if ( e.key === 'ArrowLeft' && prevUrl ) {
				window.location.href = prevUrl;
			} else if ( e.key === 'ArrowRight' && nextUrl ) {
				window.location.href = nextUrl;
			}
		} );

		// Arrow button clicks navigate to prev/next post.
		prevBtn.addEventListener( 'click', function ( e ) {
			e.stopPropagation();
			if ( prevUrl ) {
				window.location.href = prevUrl;
			}
		} );

		nextBtn.addEventListener( 'click', function ( e ) {
			e.stopPropagation();
			if ( nextUrl ) {
				window.location.href = nextUrl;
			}
		} );
	}

	/**
	 * Open the lightbox with the given image src.
	 */
	function openLightbox( src, alt ) {
		if ( ! lightbox ) {
			createLightbox();
		}

		lightboxImage.src = src;
		lightboxImage.alt = alt || '';

		// Show/hide prev/next based on available links.
		if ( prevUrl ) {
			prevBtn.removeAttribute( 'hidden' );
		} else {
			prevBtn.setAttribute( 'hidden', '' );
		}

		if ( nextUrl ) {
			nextBtn.removeAttribute( 'hidden' );
		} else {
			nextBtn.setAttribute( 'hidden', '' );
		}

		// Force reflow before adding class for transition.
		lightbox.offsetHeight;
		lightbox.classList.add( 'is-open' );
		document.body.style.overflow = 'hidden';
	}

	/**
	 * Close the lightbox.
	 */
	function closeLightbox() {
		if ( ! lightbox ) {
			return;
		}

		lightbox.classList.remove( 'is-open' );
		document.body.style.overflow = '';

		lightbox.addEventListener( 'transitionend', function handler() {
			lightboxImage.src = '';
			lightbox.removeEventListener( 'transitionend', handler );
		} );
	}

	/**
	 * Initialize lightbox on single photo pages.
	 */
	function init() {
		var imageWrap = document.querySelector( '.single-photo__image' );
		if ( ! imageWrap ) {
			return;
		}

		var img = imageWrap.querySelector( 'img' );
		if ( ! img ) {
			return;
		}

		// Find prev/next post URLs from navigation links.
		var prevLink = document.querySelector( '.single-photo__prev a' );
		var nextLink = document.querySelector( '.single-photo__next a' );
		prevUrl = prevLink ? prevLink.href : null;
		nextUrl = nextLink ? nextLink.href : null;

		// Make the featured image clickable.
		img.style.cursor = 'zoom-in';
		img.addEventListener( 'click', function ( e ) {
			e.preventDefault();
			// Use the full-size image if available, otherwise the displayed src.
			var fullSrc = img.getAttribute( 'data-full-src' ) || img.src;
			openLightbox( fullSrc, img.alt );
		} );
	}

	document.addEventListener( 'DOMContentLoaded', init );
} )();
