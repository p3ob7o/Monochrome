# Prompt: Redesign Monochrome Photography Site

Paste the following into Claude Code as your opening prompt. It references the DESIGN_SYSTEM.md file in this same directory.

---

## The Prompt

```
I'm redesigning monochrome.photo, a black & white photography and writing site built on WordPress. Read the design system first:

@DESIGN_SYSTEM.md

This is the complete design system — colors, typography, layout patterns, components, interactions, and rules. Follow it exactly. Every design decision has already been made in that document.

## What exists today

The site runs on WordPress (hosted on WordPress.com). It currently spans multiple domains:
- monochrome.photo — photo gallery homepage + individual photo posts
- monochrome.blog — blog/writing (separate WordPress site, same theme)
- monochrome.store — placeholder (hide from nav)
- monochrome.art — external platform (hide from nav)

The current theme is a dark WordPress block theme with basic layouts. The homepage has a featured post (split: image left, about text right), then a "MORE PHOTOS" 2-column grid, then footer. Photo posts have a title, image, caption, short text, and prev/next links.

## What I want you to build

A custom WordPress block theme called "Monochrome" that implements the design system. Build it section by section — I'll review each section before we move to the next.

### Build order:

**Section 1: Theme setup + design tokens**
- Create the theme structure (theme.json, style.css, functions.php, templates/, parts/)
- Define all CSS custom properties from the design system (colors, typography, spacing) in theme.json and a base stylesheet
- Set up font loading for Space Grotesk (400/500/700) and Source Serif 4 (400/600) from Google Fonts
- Implement dark/light mode toggle with localStorage persistence and prefers-color-scheme detection
- Set up the 300ms smooth transition between modes

**Section 2: Header + Navigation**
- Sticky header with backdrop blur on scroll
- Wordmark "MONOCHROME" left, nav links right (BLOG, PHOTO only), dark/light toggle
- Tagline "by Paolo Belcastro" below wordmark (hidden on mobile)
- Active page indicated by accent color underline
- Mobile: hamburger menu with full-screen overlay
- The BLOG link goes to monochrome.blog, PHOTO link goes to monochrome.photo

**Section 3: Homepage hero**
- Full-bleed featured image, 70vh height on desktop
- Title overlaid at bottom-left over gradient (transparent to dark overlay)
- Caption (location, date) below title in lighter opacity
- Pulls from the latest/sticky post
- Clickable — links to the photo's detail page

**Section 4: Gallery grid**
- Masonry layout, 3 columns desktop / 2 tablet / 1 mobile
- Tight 12px gaps (contact sheet feel)
- No visible text by default
- Hover: gradient overlay fades in from bottom with title + date, image scales 1.02
- Intersection observer: images fade in with translateY(16px) on scroll, staggered 80ms
- Lazy loading with blur-up placeholders
- Each image links to its detail page
- Pulls from photo posts, excluding the featured/sticky one

**Section 5: About section**
- Below the gallery grid
- Centered text block, max-width 800px
- Heading in Space Grotesk, body in Source Serif 4
- Keep it short — the current about text is fine, just restyle it

**Section 6: Photo detail page (single post)**
- Large photo centered, max-width 1400px, clickable to open lightbox
- Below photo: title left, location/camera right, separated by border
- Writing below in Source Serif 4, max-width 65ch
- Prev/next navigation with thumbnails
- Subscribe form at bottom

**Section 7: Lightbox**
- Full-screen black overlay
- Image centered and scaled to fit viewport
- Close on click outside, Escape key, or X button
- Left/right arrow key navigation
- Smooth scale-up transition from source position

**Section 8: Footer**
- Three columns: "The WEELO Factory" left, "From Vienna with ♥" center, social icons right
- Social icons: monochrome default, accent on hover
- Dark/light toggle repeated here
- Top border in --color-border

**Section 9: Subscribe form component**
- Transparent input with bottom-border only
- Accent-colored subscribe button
- Privacy note in muted text
- Centered, max-width 500px
- Works with WordPress subscription/Jetpack subscriptions

**Section 10: Blog page template (for monochrome.blog)**
- Same theme, but configured for the blog domain
- Featured post as full-bleed hero (same pattern as photo homepage)
- Post list below: horizontal cards with thumbnail left, title + date + excerpt right
- Post detail: same layout as photo detail but optimized for longer text

## Technical requirements

- WordPress block theme (uses theme.json, block templates, template parts)
- No page builder plugins — pure blocks and custom CSS
- Semantic HTML, accessible (WCAG AA)
- All images with descriptive alt text
- Performance: preload hero image, lazy load everything else, font-display: swap
- CSS custom properties for all design tokens (no hardcoded values)
- Smooth dark/light mode that respects system preference

## How to work

- Build one section at a time
- Show me the code for each section before moving on
- Ask me questions if anything in the design system is ambiguous
- Don't add anything not in the design system — no extra features, no "improvements"
- If a WordPress limitation prevents something, tell me and suggest the closest alternative
```

---

## Usage Notes

- Paste the entire prompt above (between the ``` markers) into Claude Code
- Make sure DESIGN_SYSTEM.md is in the same directory so the `@DESIGN_SYSTEM.md` reference works
- Claude Code will work through the 10 sections sequentially, showing you code for each
- Review and approve each section before it moves to the next
- If you want to skip ahead or reorder, just tell it which section to do next
- The prompt explicitly tells Claude Code not to add unrequested features — this prevents scope creep
