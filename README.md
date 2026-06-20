# Lukas Golino Personal Website

Personal website and portfolio hosted on GitHub Pages.

- Domain: www.lukasgolino.com
- Repo: lukasgolino.github.io
- Site config: [_config.yml](_config.yml)

## Current Pages

- [index.html](index.html): homepage and section navigation
- [aboutme.html](aboutme.html): bio and timeline
- [writings.html](writings.html): writings landing page
- [writings-book.html](writings-book.html): embedded book page
- [travels.html](travels.html): travel cards and trip links
- [travel-gallery.html](travel-gallery.html): generic travel gallery page
- [research.html](research.html): publications list
- [contact.html](contact.html): contact form and social links

## Travel Gallery System

Travel content is now managed by one generic gallery page instead of one full page per country/year.

### Add a new trip

1. Add a trip entry in [travels.html](travels.html) inside the trips array.
2. Use folder structure for photos:

   assets/images/travels/YEAR/country-slug/

3. Add a flag file (optional but recommended) in:

   assets/images/flags/Flag_of_Country_Name.svg

Example:

- Country: New Zealand
- Year: 2027
- Photos folder: assets/images/travels/2027/new-zealand/
- Flag file: assets/images/flags/Flag_of_New_Zealand.svg

### Refresh image index

The gallery uses a generated manifest file at [assets/images/travels/index.json](assets/images/travels/index.json).

After adding/removing travel photos, run:

./script/update-travel-index

Script location: [script/update-travel-index](script/update-travel-index)

## Key Asset Folders

- [assets/images/travels](assets/images/travels): travel photos and index.json
- [assets/images/flags](assets/images/flags): country flag images used by travel cards

## Local Preview

If you just need a quick static preview:

python3 -m http.server 4000

Then open:

http://localhost:4000

## Deployment

- Hosted via GitHub Pages from this repository.
- Custom domain configured in [CNAME](CNAME).
