# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- CI checks are cheap, so they run on every push (and on demand).

## [0.1.0] - 2026-11-05

### Added

- Cloudflare Web Analytics beacon on every page (cookieless); each page's CSP allows it. `check_site.py` checks
  every page loads it exactly once and isn't blocked by its CSP
  ([#3](https://github.com/lukasgolino/lukasgolino.github.io/issues/3)).
- Page titles, meta descriptions, canonical links and Open Graph tags on every page. `writings-book.html` sets its
  canonical and description per book; the bare `travel-gallery.html` template is dropped from the sitemap.
  `check_site.py` checks all of it ([#2](https://github.com/lukasgolino/lukasgolino.github.io/issues/2)).
- `sitemap.xml` (every page, plus one `writings-book.html?book=` entry per book, and the
  /kiln-website/ and /loose-website/ project sites) and `robots.txt`; `check_site.py`
  checks the sitemap lists exactly the pages ([#1](https://github.com/lukasgolino/lukasgolino.github.io/issues/1)).
- CHANGELOG.md; an on-demand check workflow, run once per PR before merge (`tools/check_site.py`: local links and
  JS-fetched data resolve to published files; plus the Jekyll build); deploys skip changelog/CI-only pushes; and a
  release workflow that publishes a GitHub release for each `vX.Y.Z` tag, with that
  version's CHANGELOG section as the notes ([#4](https://github.com/lukasgolino/lukasgolino.github.io/issues/4)).

[Unreleased]: https://github.com/lukasgolino/lukasgolino.github.io/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/lukasgolino/lukasgolino.github.io/releases/tag/v0.1.0
