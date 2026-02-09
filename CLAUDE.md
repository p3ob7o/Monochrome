# Monochrome

B&W photography and writing project by Paolo Belcastro. Built on WordPress.

## Multi-Domain Architecture

- `monochrome.photo` — Primary site. Photo gallery + individual photo posts with writing.
- `monochrome.blog` — Long-form writing about photography, cameras, process.
- `monochrome.store` — Future print store (not yet active).
- `monochrome.art` — External art profile on iDART (not yet active).

All domains share the same WordPress theme and visual identity. Nav only shows active domains (PHOTO, BLOG).

## Key Files

- `DESIGN_SYSTEM.md` — Complete design system: colors (Darkroom Amber `#D4855A` accent), typography (Space Grotesk + Source Serif 4), layout patterns, components, interactions. Single source of truth for all design decisions.
- `CLAUDE_CODE_PROMPT.md` — Ready-to-paste prompt for Claude Code to rebuild the site as a custom WordPress block theme implementing the design system.
- `drafts/` — Blog post drafts (markdown).
- `prints/` — Print-ready files for physical products.
- `assets/` — Logo and QR code assets.

## Notes

- This repo uses git-lfs for large files (TIFFs). If git commands hang, bypass with `git -c filter.lfs.process=false`.
- The branch `editorial/revise-black-white-renaissance` handles editorial feedback on blog drafts via the `editor-feedback-resolver` agent (see `AGENTS.md`).
