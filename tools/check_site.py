#!/usr/bin/env python3
"""Sanity checks on the site's pages (plain HTML, no layouts): every local href/src resolves to a file in the
repo. Links into the project sites served under this domain (/kiln-website/, /loose-website/) live in other repos
and are skipped."""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE = Path(__file__).resolve().parent.parent
ORIGIN = "https://lukasgolino.com/"
PROJECT_SITES = ("kiln-website/", "loose-website/")  # other repos' GitHub Pages, served under this domain
PAGES = sorted(SITE.glob("*.html"))
errors = []


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
        if target.is_dir():
            target = target / "index.html"
        if not target.resolve().is_relative_to(SITE):
            errors.append(f"{page.name}: {ref} points outside the site")
        elif not target.exists():
            errors.append(f"{page.name}: broken link {ref}")

for e in errors:
    print(f"check_site: {e}", file=sys.stderr)
if errors:
    sys.exit(1)
print(f"check_site: {len(PAGES)} pages, all local links resolve")
