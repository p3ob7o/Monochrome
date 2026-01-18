# Repository Guidelines

## Project Structure & Module Organization
- `drafts/` holds the only files we edit: long-form Markdown drafts for Monochrome.blog.
- `scripts/` contains Python agents that review drafts and open GitHub issues (e.g., `teacher.py`, `zinsser.py`).
- `assets/` stores reusable visual assets (logos, QR SVGs/PNGs).
- `prints/` contains production-ready print assets (PDF/EPS/TIFF/Keynote).

## Build, Test, and Development Commands
- We do not run build, test, or development commands in this repository.
- The only work here is editing `drafts/*.md` to improve the writing and subsequent review outcomes.

## Coding Style & Naming Conventions
- We only modify draft files in `drafts/`. Do not edit `scripts/`, `assets/`, or `prints/`.
- Draft filenames are lowercase with hyphens (e.g., `a-black-white-renaissance.md`).
- Keep edits focused on clarity and flow; preserve the author’s voice.

## Testing Guidelines
- No automated test suite is present.
- Review scripts are run by GitHub Actions, so no local validation is needed.

## Commit & Pull Request Guidelines
- Commit messages are short, imperative, and sentence-cased (e.g., “Tighten lead for clarity”).
- Keep commits scoped to a single draft or a single editing pass.
- PRs (if used) should include a brief summary and the before/after grade change.

## Security & Configuration Tips
- Reviews are driven by GitHub issues that include grades, reasons, and feedback for drafts.
- Our workflow is to read those issues and revise the matching draft to improve the next grade.
- Scripts rely on Anthropic credentials via environment variables (e.g., `ANTHROPIC_API_KEY`).
- GitHub issue creation requires `gh` CLI authentication (`gh auth login`).
