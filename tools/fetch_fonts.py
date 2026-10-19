#!/usr/bin/env python3
"""Copy the Google Fonts the site uses into assets/fonts/google, so pages load them from this site.

For every stylesheet URL tools/web_fonts.py would request (each script's own
families and the small subset for language names), this downloads the CSS
Google serves to current browsers (WOFF2, split by Unicode range), saves each
font file under assets/fonts/google/files/ and writes the CSS with local URLs
to assets/fonts/google/<id>.css, where <id> comes from the Google URL. Run it
after changing a family, an axis or the name characters in web_fonts.py;
--check (no network) verifies every stylesheet the pages need is present.
All families are under the SIL Open Font License 1.1; each family's license is
saved to assets/fonts/google/licenses/<family>.txt from github.com/google/fonts.
"""
import argparse
import hashlib
import re
import sys
import urllib.request
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "assets" / "fonts" / "google"
# Google serves WOFF2 split by unicode-range to current browsers.
AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


_spec = spec_from_file_location("kumihan_web_fonts", Path(__file__).with_name("web_fonts.py"))
WEB_FONTS = module_from_spec(_spec)
_spec.loader.exec_module(WEB_FONTS)


def css_path(url):
    return DIR / f"{WEB_FONTS.local_id(url)}.css"


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": AGENT}), timeout=60) as r:
        return r.read()


def fetch(url):
    css = get(url).decode("utf-8")

    def local(m):
        data = get(m.group(1))
        name = hashlib.sha256(data).hexdigest()[:16] + ".woff2"
        (DIR / "files").mkdir(parents=True, exist_ok=True)
        (DIR / "files" / name).write_bytes(data)
        return f"url(files/{name})"

    css = re.sub(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", local, css)
    css_path(url).write_text(f"/* {url} — copied by tools/fetch_fonts.py; do not edit. */\n" + css, encoding="utf-8")


def families():
    names = {n for local_sans, local_serif, sans, serif in WEB_FONTS.SCRIPTS.values() for n in (sans, serif)}
    return sorted(names | set(WEB_FONTS.SUBSET))


def license_path(family):
    return DIR / "licenses" / (family.lower().replace(" ", "") + ".txt")


def fetch_license(family):
    url = f"https://raw.githubusercontent.com/google/fonts/main/ofl/{license_path(family).stem}/OFL.txt"
    license_path(family).parent.mkdir(parents=True, exist_ok=True)
    license_path(family).write_bytes(get(url))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    urls = WEB_FONTS.google_urls()
    missing = [u for u in urls if not css_path(u).exists()] + [f for f in families() if not license_path(f).exists()]
    if args.check:
        if missing:
            sys.exit("Fonts not copied (run tools/fetch_fonts.py): " + ", ".join(missing))
        print(f"Fonts: {len(urls)} stylesheets present")
        return
    for url in urls:
        fetch(url)
    for family in families():
        fetch_license(family)
    used = {n for u in urls for n in re.findall(r"files/([0-9a-f]+\.woff2)", css_path(u).read_text(encoding="utf-8"))}
    for path in (DIR / "files").glob("*.woff2"):
        if path.name not in used:
            path.unlink()
    for path in DIR.glob("*.css"):
        if path.name not in {css_path(u).name for u in urls}:
            path.unlink()
    print(f"Fonts: {len(urls)} stylesheets, {len(used)} files copied")


if __name__ == "__main__":
    main()
