# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-11-09

### Added

- Umami analytics alongside Cloudflare Web Analytics: cookieless, so still no consent banner, and it adds
  per-visit page journeys (entry page, pages in order, exit), which Cloudflare's aggregate counts can't show.
  All our sites share one Umami website; the Host filter separates them.

## [0.2.0] - 2026-11-06

### Added

- A standard icon set: `favicon.ico` (16/32/48 px), a 96 px icon, a 180 px apple-touch icon and `site.webmanifest`
  with 192/512 px and maskable icons, so search results, tabs, bookmarks and home-screen shortcuts all show the
  icon ([#12](https://github.com/lukasgolino/lukasgolino.github.io/issues/12)).
- schema.org structured data (JSON-LD) on the home page, an `llms.txt` summary for AI assistants, and robots.txt
  content signals allowing search and AI use; the home page title names what the site is for
  ([#13](https://github.com/lukasgolino/lukasgolino.github.io/issues/13)).

## [0.1.1] - 2026-11-06

### Changed

- CI checks are cheap, so they run on every push (and on demand).
- KILN and LOOSE! links point at their own domains, https://kiln3d.dev/ and https://loosegame.com/; the sitemap no
  longer lists the old /kiln-website/ and /loose-website/ paths ([#10](https://github.com/lukasgolino/lukasgolino.github.io/issues/10)).

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

[Unreleased]: https://github.com/lukasgolino/lukasgolino.github.io/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/lukasgolino/lukasgolino.github.io/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/lukasgolino/lukasgolino.github.io/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/lukasgolino/lukasgolino.github.io/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/lukasgolino/lukasgolino.github.io/releases/tag/v0.1.0
