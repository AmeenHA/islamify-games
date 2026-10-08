#!/usr/bin/env python3
"""Copy a downloaded copy of the Claude artifact "Islamify Games Website" into artifact/index.html.
claude.ai wraps the published page in a document skeleton (doctype, base styles, <body>);
this strips that wrapper so artifact/index.html stays the bare artifact source build.py expects.
Run: python3 sync_artifact.py <downloaded index.html>   (prints "changed" or "unchanged")
"""
import pathlib, re, sys
DEST = pathlib.Path(__file__).parent / "artifact" / "index.html"

html = pathlib.Path(sys.argv[1]).read_text()
m = re.match(r"<!doctype html><html><head>.*?</head><body>\n?", html, re.S | re.I)
if m and html.rstrip().endswith("</body></html>"):
    html = html[m.end():].rstrip()[: -len("</body></html>")].rstrip("\n") + "\n"
if "<title>" not in html:
    sys.exit("refusing to sync: page has no <title> (build.py needs one)")

if DEST.read_text() == html:
    print("unchanged")
else:
    DEST.write_text(html)
    print("changed")
