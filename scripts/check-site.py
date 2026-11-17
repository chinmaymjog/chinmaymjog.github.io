#!/usr/bin/env python3
"""Check a built Hugo site (default: ./public): key pages exist and every
internal link/asset reference resolves to a file. External links are not
followed (they would make the check flaky). Usage: check-site.py [public-dir] [base-url]
base-url (e.g. http://localhost/): absolute links under it count as internal.
"""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

public = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
base = sys.argv[2].rstrip("/") if len(sys.argv) > 2 else None
# Known gaps, referenced by the PaperMod theme but not shipped in static/.
# Remove an entry once the file is added.
KNOWN_MISSING = {
    "/apple-touch-icon.png",
    "/favicon-16x16.png",
    "/favicon-32x32.png",
    "/favicon.ico",
    "/safari-pinned-tab.svg",
}
errors = []

for required in ("index.html", "sitemap.xml", "robots.txt", "404.html"):
    if not (public / required).is_file():
        errors.append(f"missing expected file: {required}")


class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append(a[key])


def resolves(page: Path, ref: str) -> bool:
    if base and ref.startswith(base + "/"):
        ref = ref[len(base):]
    u = urlparse(ref)
    if u.scheme or u.netloc or ref.startswith(("mailto:", "tel:", "data:", "javascript:")):
        return True  # external or non-file reference
    path = unquote(u.path)
    if path in KNOWN_MISSING:
        return True
    if not path:
        return True  # same-page anchor
    target = public / path.lstrip("/") if path.startswith("/") else (page.parent / path)
    target = Path(target).resolve()
    return target.is_file() or (target / "index.html").is_file()


pages = sorted(public.rglob("*.html"))
if not pages:
    errors.append("no HTML pages were built")
checked = 0
for page in pages:
    p = Refs()
    p.feed(page.read_text(encoding="utf-8", errors="replace"))
    for ref in p.refs:
        checked += 1
        if not resolves(page, ref):
            errors.append(f"{page.relative_to(public)}: broken reference {ref}")

print(f"checked {len(pages)} pages, {checked} references")
if errors:
    print("\n".join(sorted(set(errors))[:50]))
    print(f"FAIL: {len(set(errors))} problem(s)")
    sys.exit(1)
print("OK: site checks passed")
