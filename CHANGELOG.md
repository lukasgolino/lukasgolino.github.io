# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- CHANGELOG.md; an on-demand check workflow, run once per PR before merge (`tools/check_site.py`: local links and
  JS-fetched data resolve to published files; plus the Jekyll build); deploys skip changelog/CI-only pushes; and a
  release workflow that publishes a GitHub release for each `vX.Y.Z` tag, with that
  version's CHANGELOG section as the notes ([#4](https://github.com/lukasgolino/lukasgolino.github.io/issues/4)).
