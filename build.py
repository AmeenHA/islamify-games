#!/usr/bin/env python3
"""Turn the Claude artifact page (artifact/index.html) into a production static site in site/.
- wraps it in a full HTML document (doctype, meta, social tags, favicon)
- pulls embedded data: URIs out into real files under site/assets/ (cacheable, smaller HTML)
Run: python3 build.py
"""
import base64, hashlib, re, pathlib, shutil
ROOT = pathlib.Path(__file__).parent
SRC, OUT = ROOT / "artifact" / "index.html", ROOT / "site"
EXT = {"image/webp": "webp", "image/png": "png", "image/jpeg": "jpg", "video/mp4": "mp4"}

html = SRC.read_text()
if OUT.exists(): shutil.rmtree(OUT)
(OUT / "assets").mkdir(parents=True)

names = {}
def extract(m):
    mime, data = m.group(1), m.group(2)
    raw = base64.b64decode(data)
    name = f"{hashlib.sha1(raw).hexdigest()[:12]}.{EXT[mime]}"
    (OUT / "assets" / name).write_bytes(raw)
    names[name] = len(raw)
    return f"/assets/{name}"
html = re.sub(r"data:(image/webp|image/png|image/jpeg|video/mp4);base64,([A-Za-z0-9+/=]+)", extract, html)

title = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
html = re.sub(r"<title>.*?</title>\n?", "", html, count=1, flags=re.S)
logo = next((n for n in names if n.endswith(".png")), "")
og = next((n for n in names if n.endswith(".jpg")), "")

head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Kalima Clash! | Islamify Games</title>
<meta name="description" content="Kalima Clash is the word-guessing game for Muslims that your group chat will argue about for a week. 100 cards, 400 words, 2+ players, ages 6+.">
<meta name="theme-color" content="#071226">
<meta property="og:type" content="website">
<meta property="og:title" content="Kalima Clash! by Islamify Games">
<meta property="og:description" content="The word-guessing game for Muslims that your group chat will argue about for a week.">
{f'<meta property="og:image" content="/assets/{og}">' if og else ''}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
</head>
<body>
"""
(OUT / "index.html").write_text(head + html + "\n</body>\n</html>\n")
(OUT / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="9" fill="#071226"/><g fill="none" stroke="#f3c46b" stroke-width="1.8"><rect x="11" y="11" width="18" height="18"/><rect x="11" y="11" width="18" height="18" transform="rotate(45 20 20)"/><circle cx="20" cy="20" r="5"/></g></svg>')
print(f"built site/index.html ({(OUT/'index.html').stat().st_size//1024} KB) + {len(names)} assets")
