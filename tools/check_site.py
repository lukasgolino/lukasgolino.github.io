#!/usr/bin/env python3
"""Sanity checks on the site's pages (plain HTML, no layouts): every local href/src resolves to a file that Jekyll
publishes, and so do the files the JS-driven pages fetch (travel photo index, world atlas, writings metadata and
the front/back/preview files it names). Each page loads the analytics beacon and the Umami tag exactly once and
its CSP allows both. Each page has one title, description, og:type/site_name/title/description and twitter:card,
and (unless it's a JS template) a canonical and og:url equal to its own URL. sitemap.xml must list exactly the pages, and robots.txt must
point to it."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE = Path(__file__).resolve().parent.parent
ORIGIN = "https://lukasgolino.com/"
TOKEN = "8157ab8d746f4868a67445fdd46c03b8"  # Cloudflare Web Analytics site token
UMAMI_ID = "6c3ba9da-9af9-49a9-a575-90c9cace445c"  # one Umami website for all our sites
PAGES = sorted(SITE.glob("*.html"))
# Pages rendered per query string by JS (writings-book.html?book=, travel-gallery.html?country=&year=): no static
# canonical, not in the sitemap as bare URLs.
TEMPLATES = ("writings-book.html", "travel-gallery.html")
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
        self.head = {"canonical": [], "og:url": [], "title": [], "description": [], "og:title": [],
                     "og:description": [], "og:type": [], "og:site_name": [], "twitter:card": []}
        self._in_title = False
        self.beacons = []
        self.umami = []
        self.csp = []

    def handle_data(self, data):
        if self._in_title:
            self.head["title"][-1] += data

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
            self.head["title"].append("")
        if tag == "link" and "canonical" in (a.get("rel") or "").lower().split():
            self.head["canonical"].append(a.get("href"))
        src = urlsplit(a.get("src") or "")
        if tag == "script" and src.netloc == "static.cloudflareinsights.com" and "beacon" in src.path:
            try:
                self.beacons.append(json.loads(a.get("data-cf-beacon") or "").get("token"))
            except (ValueError, AttributeError):
                self.beacons.append(None)
        if tag == "script" and a.get("src") == "https://cloud.umami.is/script.js":
            self.umami.append(a.get("data-website-id"))
        if tag == "meta" and (a.get("http-equiv") or "").lower() == "content-security-policy":
            self.csp.append(a.get("content") or "")
        if tag == "meta":
            key = a.get("property") or a.get("name")
            if key in self.head:
                self.head[key].append(a.get("content"))
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.refs.append(v)


for page in PAGES:
    parser = Refs()
    parser.feed(page.read_text(encoding="utf-8"))
    url = ORIGIN + ("" if page.name == "index.html" else page.name)
    want = {"canonical": [] if page.name in TEMPLATES else [url], "og:url": [] if page.name in TEMPLATES else [url]}
    for key, got in parser.head.items():
        if key in want:
            if got != want[key]:
                errors.append(f"{page.name}: {key} is {got}, expected {want[key]}")
        elif len(got) != 1 or not (got[0] or "").strip():
            errors.append(f"{page.name}: expected exactly one non-empty {key}, got {got}")
    if parser.beacons != [TOKEN]:
        errors.append(f"{page.name}: analytics beacons {parser.beacons}, expected exactly [{TOKEN!r}]")
    if parser.umami != [UMAMI_ID]:
        errors.append(f"{page.name}: Umami tags {parser.umami}, expected exactly [{UMAMI_ID!r}]")
    for policy in parser.csp:  # the page's CSP must let the beacon load and report
        directives = {}
        for d in policy.split(";"):
            if d.split():
                directives.setdefault(d.split()[0].lower(), d.split()[1:])  # browsers use the first copy

        def effective(*names):  # most specific directive present wins, falling back to default-src
            return next((directives[n] for n in names if n in directives), directives.get("default-src", []))

        if "https://static.cloudflareinsights.com" not in effective("script-src-elem", "script-src"):
            errors.append(f"{page.name}: CSP blocks the analytics beacon script")
        if "https://cloudflareinsights.com" not in effective("connect-src"):
            errors.append(f"{page.name}: CSP blocks analytics reporting")
        if "https://cloud.umami.is" not in effective("script-src-elem", "script-src"):
            errors.append(f"{page.name}: CSP blocks the Umami script")
        if "https://gateway.umami.is" not in effective("connect-src"):
            errors.append(f"{page.name}: CSP blocks Umami reporting")
    for ref in parser.refs:
        if "${" in ref:  # built in JS template literals at runtime
            continue
        u = urlsplit(ref)
        own = ref.startswith(ORIGIN)  # absolute links to this site are checked like relative ones
        if (u.scheme or u.netloc or ref.startswith(("#", "mailto:", "data:"))) and not own:
            continue
        path = unquote(u.path)
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

# sitemap.xml lists every page once (writings-book.html once per book, as ?book=<slug>,
# plus the project sites' roots); robots.txt points to it.
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
try:
    root = ET.parse(SITE / "sitemap.xml").getroot()
except ET.ParseError as e:
    errors.append(f"sitemap.xml: {e}")
    root = ET.Element(NS + "urlset")
if root.tag != NS + "urlset":
    errors.append(f"sitemap.xml: root is {root.tag}, not a sitemaps.org <urlset>")
listed = []
for url in root.findall(NS + "url"):
    locs = url.findall(NS + "loc")
    if len(locs) != 1:
        errors.append(f"sitemap.xml: a <url> has {len(locs)} <loc> elements")
    listed += [(loc.text or "").strip() for loc in locs]
expected = {ORIGIN + ("" if p.name == "index.html" else p.name) for p in PAGES if p.name not in TEMPLATES}
expected |= {f"{ORIGIN}writings-book.html?book={slug}" for slug in slugs}
for name in ("sitemap.xml", "robots.txt"):
    check_target("site root", name, SITE / name)
errors += [f"sitemap.xml: {u} listed twice" for u in sorted({u for u in listed if listed.count(u) > 1})]
errors += [f"sitemap.xml: {u} is not a page" for u in listed if u not in expected]
errors += [f"sitemap.xml: missing {u}" for u in sorted(expected - set(listed))]
if f"Sitemap: {ORIGIN}sitemap.xml" not in (SITE / "robots.txt").read_text(encoding="utf-8").splitlines():
    errors.append("robots.txt: no Sitemap line for sitemap.xml")

for e in errors:
    print(f"check_site: {e}", file=sys.stderr)
if errors:
    sys.exit(1)
print(f"check_site: {len(PAGES)} pages and their fetched data, all local links resolve")
