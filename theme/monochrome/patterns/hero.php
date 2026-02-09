<?php
/**
 * Title: Hero
 * Slug: monochrome/hero
 * Categories: monochrome
 * Description: Full-bleed featured photo hero for the homepage.
 * Inserter: false
 */

// Get sticky posts first, fall back to most recent post.
$sticky = get_option( 'sticky_posts' );
$hero_args = array(
	'posts_per_page'      => 1,
	'post_status'         => 'publish',
	'ignore_sticky_posts' => true,
);

if ( ! empty( $sticky ) ) {
	$hero_args['post__in'] = $sticky;
} else {
	$hero_args['orderby'] = 'date';
	$hero_args['order']   = 'DESC';
}

$hero_query = new WP_Query( $hero_args );

if ( $hero_query->have_posts() ) :
	$hero_query->the_post();
	$post_id       = get_the_ID();
	$permalink     = get_permalink();
	$title         = get_the_title();
	$thumbnail_url = get_the_post_thumbnail_url( $post_id, 'monochrome-hero' );

	// Extract location and date from post meta or content.
	$date_display = get_the_date( 'Y-m-d' );

	// Try to get location from a custom field, fall back to empty.
	$location = get_post_meta( $post_id, 'monochrome_location', true );
	$caption  = $location ? $location . ', ' . $date_display : $date_display;

	if ( $thumbnail_url ) :
?>
<section class="hero">
	<a href="<?php echo esc_url( $permalink ); ?>" class="hero__link" aria-label="<?php echo esc_attr( $title ); ?>">
		<div class="hero__image-wrapper">
			<img
				class="hero__image"
				src="<?php echo esc_url( $thumbnail_url ); ?>"
				alt="<?php echo esc_attr( $title ); ?>"
				fetchpriority="high"
			/>
		</div>
		<div class="hero__overlay">
			<h2 class="hero__title"><?php echo esc_html( $title ); ?></h2>
			<span class="hero__caption"><?php echo esc_html( $caption ); ?></span>
		</div>
	</a>
</section>
<?php
	endif;
	wp_reset_postdata();
endif;
