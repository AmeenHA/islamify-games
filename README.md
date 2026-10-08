# Islamify Games website

Landing page for Kalima Clash by Islamify Games, hosted on Netlify.

- `artifact/index.html` is the source of truth. It is the same page as the Claude artifact "Islamify Games Website".
- `build.py` turns it into the production site in `site/` (full HTML document, images and video split out into `/assets`).
- Netlify runs `python3 build.py` on every push to `main` and publishes `site/` (settings in `netlify.toml`).

To update the site: replace `artifact/index.html` and commit to `main`. Netlify redeploys automatically.

## Auto-sync from Claude

A Claude Code Routine checks the artifact (https://claude.ai/artifact/CkSU8vjFANq7Lj9sQ8PKWu) every hour. If it changed, it downloads the page, runs `python3 sync_artifact.py <downloaded file>` (which strips the wrapper claude.ai adds when publishing), checks that `build.py` still succeeds, and commits `artifact/index.html` to `main`. Netlify then redeploys.
