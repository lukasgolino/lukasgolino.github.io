#!/usr/bin/env python3
"""Sanity checks on the site's pages (plain HTML, no layouts): every local href/src resolves to a file that Jekyll
publishes, and so do the files the JS-driven pages fetch (travel photo index, world atlas, writings metadata and
the front/back/preview files it names). Links into the project sites served under this domain (/kiln-website/,
/loose-website/) live in other repos and are skipped."""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE = Path(__file__).resolve().parent.parent
ORIGIN = "https://lukasgolino.com/"
PROJECT_SITES = ("kiln-website/", "loose-website/")  # other repos' GitHub Pages, served under this domain
PAGES = sorted(SITE.glob("*.html"))
errors = []

# Jekyll's exclude list plus its built-in rule (names starting with _ or . aren't published).
EXCLUDED = re.findall(r"^  - (\S+)$", (SITE / "_config.yml").read_text(encoding="utf-8"), re.M)


def check_target(where, ref, target):
    if target.is_dir():
        target = target / "index.html"
    target = target.resolve()
    if not target.is_relative_to(SITE):
        errors.append(f"{where}: {ref} points outside the site")
        return
    parts = target.relative_to(SITE).parts
    if parts[0] in EXCLUDED or any(p.startswith(("_", ".")) for p in parts):
        errors.append(f"{where}: {ref} is excluded from the published site")
    elif not target.exists():
        errors.append(f"{where}: broken link {ref}")


class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.refs.append(v)


for page in PAGES:
    parser = Refs()
    parser.feed(page.read_text(encoding="utf-8"))
    for ref in parser.refs:
        if "${" in ref:  # built in JS template literals at runtime
            continue
        u = urlsplit(ref)
        own = ref.startswith(ORIGIN)  # absolute links to this site are checked like relative ones
        if (u.scheme or u.netloc or ref.startswith(("#", "mailto:", "data:"))) and not own:
            continue
        path = unquote(u.path)
        if path.lstrip("/").startswith(PROJECT_SITES):
            continue
        target = (SITE / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
        check_target(page.name, ref, target)

# Files the JS-driven pages fetch at runtime.
travel_index = SITE / "assets/images/travels/index.json"
check_target("travel-gallery.html", "/assets/images/travels/index.json", travel_index)
if travel_index.exists():
    for img in json.loads(travel_index.read_text(encoding="utf-8")):
        check_target("travels/index.json", img["src"], SITE / img["src"].lstrip("/"))
check_target("travels.html", "/assets/data/world-atlas/countries-50m.json", SITE / "assets/data/world-atlas/countries-50m.json")
slugs = re.findall(r'"([\w-]+)"', re.search(r"bookSlugs = \[([^\]]*)\]", (SITE / "writings.html").read_text(encoding="utf-8")).group(1))
for slug in slugs:
    meta = SITE / "writings" / slug / "metadata.json"
    check_target("writings.html", f"/writings/{slug}/metadata.json", meta)
    if meta.exists():
        m = json.loads(meta.read_text(encoding="utf-8"))
        for key in ("front", "back", "preview"):
            if m.get(key):
                check_target(f"writings/{slug}/metadata.json", m[key], meta.parent / m[key])

for e in errors:
    print(f"check_site: {e}", file=sys.stderr)
if errors:
    sys.exit(1)
print(f"check_site: {len(PAGES)} pages and their fetched data, all local links resolve")
