# Islamify Games website

Landing page for Kalima Clash by Islamify Games, hosted on Netlify.

- `artifact/index.html` is the source of truth. It is the same page as the Claude artifact "Islamify Games Website".
- `build.py` turns it into the production site in `site/` (full HTML document, images and video split out into `/assets`).
- Netlify runs `python3 build.py` on every push to `main` and publishes `site/` (settings in `netlify.toml`).

To update the site: replace `artifact/index.html` and commit to `main`. Netlify redeploys automatically.
