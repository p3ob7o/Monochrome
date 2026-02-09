# Monochrome Design System

> Design system for monochrome.photo — a B&W photography and writing project by Paolo Belcastro.
> This document is the single source of truth for building the site. Feed it to Claude Code before any implementation work.

---

## 1. Brand Identity

**Project:** Monochrome is an art project combining black & white photography with writing. Photos are the centerpiece; writing is a companion, not a competitor.

**Philosophy:** The design must disappear so the photographs can speak. Every element exists to serve the images. If something doesn't support the viewing experience, remove it.

**Tone:** Quiet confidence. Gallery-like restraint. The feeling of walking into a well-lit exhibition space — your eye goes to the work, not the walls.

**Multi-domain architecture:**
- `monochrome.photo` — Primary site. Photo gallery + individual photo posts with writing.
- `monochrome.blog` — Long-form writing about photography, cameras, process.
- `monochrome.store` — Future print store (hidden from nav until ready).
- `monochrome.art` — External art profile (hidden from nav until ready).

Navigation shows only active domains: **PHOTO** and **BLOG**. The wordmark "MONOCHROME" links to monochrome.photo. A dark/light mode toggle sits in the header.

---

## 2. Color System

### 2.1 Accent Color

**Darkroom Amber:** `#D4855A`
Evokes the analog darkroom safelight. Used sparingly — only for interactive elements, CTAs, and focus states. Never competes with photographs.

Accent hover: `#E09570` (lighter, for hover states)
Accent muted: `#D4855A33` (20% opacity, for subtle backgrounds/borders)

### 2.2 Dark Mode (Default)

```
--color-bg:              #0A0A0A     /* near-black, not pure #000 */
--color-surface:         #141414     /* cards, elevated surfaces */
--color-surface-hover:   #1E1E1E     /* hover state for surfaces */
--color-border:          #2A2A2A     /* subtle dividers */
--color-text-primary:    #E8E8E8     /* main body text */
--color-text-secondary:  #999999     /* captions, dates, metadata */
--color-text-muted:      #666666     /* tertiary text, disabled states */
--color-accent:          #D4855A     /* Darkroom Amber */
--color-accent-hover:    #E09570     /* accent hover */
--color-accent-muted:    #D4855A33   /* accent at 20% opacity */
--color-overlay:         #0A0A0ACC   /* image overlay for text legibility */
```

### 2.3 Light Mode

```
--color-bg:              #F5F0EB     /* warm off-white, not sterile */
--color-surface:         #FFFFFF     /* cards, elevated surfaces */
--color-surface-hover:   #EDE8E3     /* hover state */
--color-border:          #D9D2CB     /* warm gray dividers */
--color-text-primary:    #1A1A1A     /* main body text */
--color-text-secondary:  #6B6560     /* captions, dates */
--color-text-muted:      #A39E98     /* tertiary text */
--color-accent:          #C07040     /* slightly deeper amber for light bg */
--color-accent-hover:    #D4855A     /* accent hover */
--color-accent-muted:    #C0704020   /* accent at 12% opacity */
--color-overlay:         #F5F0EBCC   /* light overlay */
```

### 2.4 Usage Rules

- Accent color appears ONLY on: links, CTA buttons, hover states, focus rings, the active nav indicator, and the subscribe button.
- Photographs are never tinted, filtered, or overlaid with color. The accent must never touch the images themselves.
- The dark/light mode transition should be a smooth 300ms ease on `background-color` and `color` properties.

---

## 3. Typography

### 3.1 Font Stack

**Display & Headings:** `"Space Grotesk", system-ui, sans-serif`
Geometric, modernist, clean. Reflects the precision of B&W photography. Used for the wordmark, section headings, and photo titles.

**Body (Writing):** `"Source Serif 4", "Georgia", serif`
Warm and readable for longer-form text. Gives the writing an editorial quality — like a photography journal or exhibition catalog essay.

**UI & Captions:** `"Space Grotesk", system-ui, sans-serif`
Same as display, but at lighter weights. Used for navigation, dates, metadata, photo captions, and form elements.

### 3.2 Type Scale

```
--font-display:    Space Grotesk, 700 weight
--font-heading:    Space Grotesk, 500 weight
--font-body:       Source Serif 4, 400 weight
--font-body-bold:  Source Serif 4, 600 weight
--font-ui:         Space Grotesk, 400 weight
--font-ui-medium:  Space Grotesk, 500 weight

--text-xs:    0.75rem / 1.5    /* 12px - metadata, fine print */
--text-sm:    0.875rem / 1.5   /* 14px - captions, dates */
--text-base:  1rem / 1.7       /* 16px - body text */
--text-lg:    1.125rem / 1.6   /* 18px - lead paragraphs */
--text-xl:    1.25rem / 1.4    /* 20px - subheadings */
--text-2xl:   1.75rem / 1.3    /* 28px - section headings */
--text-3xl:   2.5rem / 1.15    /* 40px - page titles */
--text-4xl:   3.5rem / 1.05    /* 56px - hero display text */
```

### 3.3 Typography Rules

- The wordmark "MONOCHROME" is always set in Space Grotesk Bold, uppercase, letter-spacing `0.08em`.
- Section headings ("MORE PHOTOS", "THE BLOG") use Space Grotesk Medium, uppercase, letter-spacing `0.05em`.
- Photo titles on detail pages use Space Grotesk Medium, title case (not all-caps), at `--text-3xl`.
- Blog post body text uses Source Serif 4 at `--text-base` or `--text-lg`, max-width `65ch` for comfortable reading.
- Photo captions (location, date) use Space Grotesk Regular at `--text-sm`, in `--color-text-secondary`.
- Navigation links use Space Grotesk Medium at `--text-sm`, uppercase, letter-spacing `0.06em`. The active page is indicated by the accent color, not bold weight.

---

## 4. Spacing System

```
--space-1:   0.25rem    /* 4px */
--space-2:   0.5rem     /* 8px */
--space-3:   0.75rem    /* 12px */
--space-4:   1rem       /* 16px */
--space-6:   1.5rem     /* 24px */
--space-8:   2rem       /* 32px */
--space-12:  3rem       /* 48px */
--space-16:  4rem       /* 64px */
--space-24:  6rem       /* 96px */
--space-32:  8rem       /* 128px */
```

**Content max-width:** `1200px` for the gallery grid, `800px` for text content, `1400px` for full-bleed hero images.

**Section spacing:** Each major section (hero, gallery, blog list, footer) is separated by `--space-24` vertically.

---

## 5. Layout Patterns

### 5.1 Header / Navigation

```
┌──────────────────────────────────────────────────────┐
│  MONOCHROME                        BLOG  PHOTO  ◐   │
│  texts & photos by @p3ob7o                           │
└──────────────────────────────────────────────────────┘
```

- Fixed/sticky header with a subtle backdrop blur on scroll.
- Left: Wordmark + tagline (tagline hidden on mobile).
- Right: Nav links + dark/light toggle.
- Active nav item underlined with accent color, 2px, offset 4px below text.
- Height: `--space-16` (64px). Background: `--color-bg` at 90% opacity with `backdrop-filter: blur(12px)`.
- Tagline: Rephrase from "texts & photos by @p3ob7o" to simply "by Paolo Belcastro" — more authoritative, less social-media.

### 5.2 Hero (Homepage)

Full-bleed featured photo. The image takes the entire viewport width and ~70vh height, with a subtle gradient overlay at bottom for the title.

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│              [FULL-BLEED FEATURED PHOTO]              │
│                                                      │
│         ░░░░░░░░░░░ gradient overlay ░░░░░░░░░░░░░░  │
│         Photo Title                                  │
│         Vienna, 2021-08-08                            │
└──────────────────────────────────────────────────────┘
```

- Image: `object-fit: cover`, full width, `max-height: 75vh`.
- Title overlay: positioned at bottom-left over a gradient (`transparent` to `--color-overlay`).
- Title: `--text-4xl`, Space Grotesk Bold, white (always white, regardless of mode, since it's over the image).
- Caption: `--text-sm`, white at 80% opacity.
- On click: navigates to the photo's detail page.

### 5.3 About Section

Moved below the hero. A single centered block, max-width `800px`.

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   Monochrome is an art project combining             │
│   writing and photography.                           │
│                                                      │
│   It's also an experiment in running a digital       │
│   project across multiple meaningful domain names... │
│                                                      │
└──────────────────────────────────────────────────────┘
```

- Heading: `--text-2xl`, Space Grotesk Medium.
- Body: `--text-base`, Source Serif 4, `--color-text-secondary`.
- This section is optional — can be collapsed or moved to a dedicated /about page for a cleaner homepage.

### 5.4 Photo Gallery Grid

Masonry-style responsive grid with hover interactions.

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│             │ │             │ │             │
│   [photo]   │ │   [photo]   │ │   [photo]   │
│             │ │             │ │             │
│  ░ Title ░  │ │             │ │             │
│  ░ Date  ░  │ │             │ │             │
└─────────────┘ └─────────────┘ └─────────────┘
   (hovered)       (default)       (default)
```

- Grid: CSS columns or masonry, 2 columns on mobile, 3 on desktop.
- Gap: `--space-3` (12px) — tight gaps make the grid feel like a contact sheet.
- Default state: image only, no text visible.
- Hover state (desktop): subtle dark gradient overlay fades in from bottom (200ms ease), revealing photo title and date in white. Image scales up by 2% (`transform: scale(1.02)`) with `overflow: hidden` on the container.
- Each image links to its detail page.
- Images load with a subtle fade-in (`opacity: 0` to `1`, 400ms) as they enter the viewport (intersection observer).
- Lazy loading with a low-res blurred placeholder (`filter: blur(20px)`, scaled-up tiny thumbnail).

### 5.5 Photo Detail Page

The single most important page — where a photograph is experienced.

```
┌──────────────────────────────────────────────────────┐
│  [HEADER]                                            │
├──────────────────────────────────────────────────────┤
│                                                      │
│              [LARGE PHOTO - max 1400px]               │
│              click to open lightbox                   │
│                                                      │
├──────────────────────────────────────────────────────┤
│  Photo Title                          Vienna         │
│  2021-08-08                           Leica Q2M      │
│──────────────────────────────────────────────────────│
│                                                      │
│  It's strangely fascinating to remember how much     │
│  the world changed over those two years...           │
│                                       (max 65ch)     │
│                                                      │
├──────────────────────────────────────────────────────┤
│  ← [thumbnail] Previous    Next [thumbnail] →        │
├──────────────────────────────────────────────────────┤
│  [SUBSCRIBE FORM]                                    │
│  [FOOTER]                                            │
└──────────────────────────────────────────────────────┘
```

- Photo: max-width `1400px`, centered. Click opens lightbox (see 6.2).
- Metadata row: title left, location/camera right. `--text-sm`, `--color-text-secondary`. Separated by a thin `--color-border` line below.
- Writing: Source Serif 4, `--text-lg`, max-width `65ch`, generous `--space-8` above.
- Prev/Next: thumbnail (small, ~80px) + title, using `--color-text-secondary`. On hover, thumbnail subtly brightens, text becomes `--color-accent`.

### 5.6 Blog List Page (monochrome.blog)

```
┌──────────────────────────────────────────────────────┐
│  [HEADER]                                            │
├──────────────────────────────────────────────────────┤
│                                                      │
│  [FEATURED POST - same pattern as photo hero]        │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────┐  Post Title                            │
│  │  [thumb] │  2026-01-17 · 5 min read               │
│  │          │  First two lines of excerpt...          │
│  └──────────┘                                        │
│                                                      │
│  ┌──────────┐  Post Title                            │
│  │  [thumb] │  2026-01-01 · 3 min read               │
│  │          │  First two lines of excerpt...          │
│  └──────────┘                                        │
│                                                      │
└──────────────────────────────────────────────────────┘
```

- Featured post: full-width hero image with title overlay (same as photo hero pattern).
- Post list: horizontal cards — thumbnail left (fixed width ~200px), title + date + excerpt right.
- On hover: thumbnail slightly scales, title color shifts to `--color-accent`.

### 5.7 Footer

```
┌──────────────────────────────────────────────────────┐
│  The WEELO Factory     From Vienna with ♥     ▦ 🐦 𝕏 │
└──────────────────────────────────────────────────────┘
```

- Single row, three columns: credit left, tagline center, social icons right.
- Social icons: monochrome by default, `--color-accent` on hover.
- Top border: `1px solid --color-border`.
- Padding: `--space-8` vertical.
- Dark/light toggle also appears in footer for convenience.

---

## 6. Interactions & Micro-animations

### 6.1 Scroll Animations

- Gallery images fade in as they enter the viewport: `opacity: 0, translateY(16px)` to `opacity: 1, translateY(0)` over 400ms ease-out, staggered 80ms per item.
- Use `IntersectionObserver` with `threshold: 0.1`.
- Animations run once only (no re-triggering on scroll up).

### 6.2 Lightbox

- Clicking a photo (on detail page or in gallery) opens a full-screen lightbox.
- Black background (`#000000`), image centered and scaled to fit viewport with padding.
- Close: click outside image, press Escape, or click X button (top-right, white).
- Navigate: left/right arrow keys, swipe on mobile.
- Transition: image scales up from its grid position to lightbox (300ms ease).

### 6.3 Hover States

- Gallery images: `scale(1.02)` + gradient overlay with title. Transition: 200ms ease.
- Text links: color transitions to `--color-accent`. No underline by default, underline on hover.
- Nav items: 2px bottom-border in accent color slides in from center on hover.
- Social icons: color transitions to `--color-accent`, 150ms.
- Buttons (subscribe, CTA): background shifts to `--color-accent`, text to white. Border-radius: `2px` (barely rounded — stays sharp and editorial).

### 6.4 Dark/Light Mode Toggle

- Icon: sun (☀) for "switch to light" / moon (◐) for "switch to dark".
- Transition: all color properties animate over 300ms ease.
- Preference saved to `localStorage`. Respects `prefers-color-scheme` on first visit.

### 6.5 Page Transitions

- On navigation between pages: content fades out (150ms) then fades in (250ms).
- Keep header visible and stable during transitions.

---

## 7. Component Specifications

### 7.1 Image Card (Gallery)

```html
<article class="image-card">
  <a href="/photo-slug/">
    <div class="image-card__frame">
      <img src="photo.jpg" alt="Description" loading="lazy" />
      <div class="image-card__overlay">
        <h3 class="image-card__title">Photo Title</h3>
        <span class="image-card__date">Vienna, 2021-08-08</span>
      </div>
    </div>
  </a>
</article>
```

- Frame: `overflow: hidden`, `border-radius: 0` (sharp edges).
- Overlay: `position: absolute`, bottom `0`, full width, gradient from transparent to `rgba(0,0,0,0.7)`, padding `--space-4`.
- Overlay hidden by default (`opacity: 0`), appears on hover (`opacity: 1`, 200ms).

### 7.2 Subscribe Form

```
┌──────────────────────────────────────────────────────┐
│  Subscribe to Monochrome                             │
│  ┌─────────────────────────────┐ ┌──────────────┐    │
│  │  Email address              │ │  Subscribe   │    │
│  └─────────────────────────────┘ └──────────────┘    │
│  We respect your privacy.                            │
└──────────────────────────────────────────────────────┘
```

- Input: transparent background, bottom-border only (`1px solid --color-border`), focus state adds accent color border.
- Button: `--color-accent` background, white text, `--text-sm`, uppercase, letter-spacing `0.05em`.
- Privacy note: `--text-xs`, `--color-text-muted`.
- Max-width: `500px`, centered.

### 7.3 Navigation Link

```css
.nav-link {
  font: var(--font-ui-medium);
  font-size: var(--text-sm);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-text-secondary);
  text-decoration: none;
  position: relative;
}

.nav-link:hover,
.nav-link--active {
  color: var(--color-text-primary);
}

.nav-link--active::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--color-accent);
}
```

---

## 8. Responsive Breakpoints

```
--bp-sm:   640px    /* mobile landscape */
--bp-md:   768px    /* tablet */
--bp-lg:   1024px   /* desktop */
--bp-xl:   1280px   /* wide desktop */
```

**Mobile (< 768px):**
- Gallery grid: 1 column (single column, images stack).
- Hero image: `min-height: 50vh`.
- Nav: hamburger menu with full-screen overlay.
- Tagline hidden.
- Font sizes scale down one step.

**Tablet (768px - 1024px):**
- Gallery grid: 2 columns.
- Hero image: `min-height: 60vh`.

**Desktop (> 1024px):**
- Gallery grid: 3 columns.
- Hero image: `min-height: 70vh`.
- All hover interactions active.

---

## 9. Performance & Technical Notes

- **Image optimization:** Serve WebP with JPEG fallback. Use `srcset` for responsive sizes (400w, 800w, 1200w, 1600w). Lazy load all images below the fold.
- **Blur-up placeholders:** Generate a tiny (32px wide) base64 thumbnail for each image, displayed blurred while the full image loads.
- **Font loading:** Preload Space Grotesk 400/500/700 and Source Serif 4 400/600. Use `font-display: swap` to prevent invisible text.
- **Core Web Vitals:** Target LCP < 2s (hero image preloaded), CLS < 0.05 (explicit image dimensions), INP < 100ms.
- **Accessibility:** All images must have descriptive alt text. Lightbox is keyboard-navigable. Color contrast ratios meet WCAG AA (accent on dark bg = 4.6:1, passes).

---

## 10. What NOT to Do

- Never use gradients, shadows, or glows that feel "web 2.0."
- Never auto-play video or audio.
- Never add loading spinners — use skeleton states or blur-up placeholders.
- Never add a sidebar. Content is always single-column or grid.
- Never use stock UI patterns (carousels with dots, cookie banners, floating chat widgets).
- Never round image corners. Photos are always sharp-edged.
- Never put text over the middle of a photograph — only at edges, over gradient overlays.
- Never use more than one accent color. Darkroom Amber is it.
