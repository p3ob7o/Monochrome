<?php
/**
 * Monochrome theme functions.
 *
 * @package Monochrome
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'MONOCHROME_VERSION', '1.0.0' );

/**
 * Enqueue theme styles and scripts.
 */
function monochrome_enqueue_assets() {
	// Base design tokens and global styles.
	wp_enqueue_style(
		'monochrome-base',
		get_theme_file_uri( 'assets/css/base.css' ),
		array(),
		MONOCHROME_VERSION
	);

	// Header and navigation styles.
	wp_enqueue_style(
		'monochrome-header',
		get_theme_file_uri( 'assets/css/header.css' ),
		array( 'monochrome-base' ),
		MONOCHROME_VERSION
	);

	// Hero styles.
	wp_enqueue_style(
		'monochrome-hero',
		get_theme_file_uri( 'assets/css/hero.css' ),
		array( 'monochrome-base' ),
		MONOCHROME_VERSION
	);

	// Gallery grid styles.
	wp_enqueue_style(
		'monochrome-gallery',
		get_theme_file_uri( 'assets/css/gallery.css' ),
		array( 'monochrome-base' ),
		MONOCHROME_VERSION
	);

	// Single photo detail page styles.
	wp_enqueue_style(
		'monochrome-single-photo',
		get_theme_file_uri( 'assets/css/single-photo.css' ),
		array( 'monochrome-base' ),
		MONOCHROME_VERSION
	);

	// Dark/light mode toggle script.
	wp_enqueue_script(
		'monochrome-color-mode',
		get_theme_file_uri( 'assets/js/color-mode.js' ),
		array(),
		MONOCHROME_VERSION,
		false // Load in head so it runs before paint to prevent flash.
	);

	// Navigation script (mobile menu, active link detection).
	wp_enqueue_script(
		'monochrome-navigation',
		get_theme_file_uri( 'assets/js/navigation.js' ),
		array(),
		MONOCHROME_VERSION,
		true
	);

	// Gallery scroll animations.
	wp_enqueue_script(
		'monochrome-gallery',
		get_theme_file_uri( 'assets/js/gallery.js' ),
		array(),
		MONOCHROME_VERSION,
		true
	);
}
add_action( 'wp_enqueue_scripts', 'monochrome_enqueue_assets' );

/**
 * Enqueue editor styles.
 */
function monochrome_editor_assets() {
	wp_enqueue_style(
		'monochrome-editor',
		get_theme_file_uri( 'assets/css/base.css' ),
		array(),
		MONOCHROME_VERSION
	);
}
add_action( 'enqueue_block_editor_assets', 'monochrome_editor_assets' );

/**
 * Register block patterns and pattern categories.
 */
function monochrome_register_block_patterns() {
	register_block_pattern_category( 'monochrome', array(
		'label' => __( 'Monochrome', 'monochrome' ),
	) );
}
add_action( 'init', 'monochrome_register_block_patterns' );

/**
 * Add theme support features.
 */
function monochrome_setup() {
	add_theme_support( 'wp-block-styles' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'post-thumbnails' );

	// Image sizes for the gallery and detail pages.
	add_image_size( 'monochrome-gallery', 800, 0, false );
	add_image_size( 'monochrome-hero', 1600, 0, false );
	add_image_size( 'monochrome-detail', 1400, 0, false );
	add_image_size( 'monochrome-thumbnail', 80, 80, true );
	add_image_size( 'monochrome-placeholder', 32, 0, false );
}
add_action( 'after_setup_theme', 'monochrome_setup' );

/**
 * Preload Google Fonts for performance.
 */
function monochrome_preload_fonts() {
	?>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
	<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Source+Serif+4:wght@400;600&display=swap" />
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Source+Serif+4:wght@400;600&display=swap" media="print" onload="this.media='all'" />
	<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Source+Serif+4:wght@400;600&display=swap" /></noscript>
	<?php
}
add_action( 'wp_head', 'monochrome_preload_fonts', 1 );
