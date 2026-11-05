# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- CHANGELOG.md; a check workflow (`tools/check_site.py`: local links resolve; plus the Jekyll build) on pushes to
  master and every PR; and a release workflow that publishes a GitHub release for each `vX.Y.Z` tag, with that
  version's CHANGELOG section as the notes ([#4](https://github.com/lukasgolino/lukasgolino.github.io/issues/4)).
