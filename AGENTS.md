# FitGirl Downloader — agent notes

## App

- Python `ThreadingHTTPServer` on **port 8000** (`main.py`)
- UI: `web/index.html`, `web/app.js`, `web/style.css`, `web/details-fix.css` (loaded last)
- Session: open `http://127.0.0.1:8000/`

## Important UI systems

1. **Harmonoid haze** — WebGL `AnimatedMeshGradient` port of `mesh_gradient` in `app.js` (`createMeshRenderer`, dual canvases `#haze-mesh-a/b`). Palette from cover, luminance &lt; 0.5, crossfade layers.
2. **Catalog** — adaptive page size (`computeCatalogLayout`), flex wrap + centered incomplete last row, CSS vars `--catalog-cols`, `--catalog-card-w`.
3. **Details Download dock** — `#details-bottom-bar` lives on `<body>`, `position: fixed`, not inside scroll/transform ancestors.
4. **Description** — under media in right column (not after tall left meta).

## MCP

Project config: `.grok/config.toml` (Playwright headless). Setup: `docs/MCP_SETUP.md`.

When verifying UI, use Playwright MCP headless; do not open the user’s Zen browser.

## Do not commit

- QA screenshots (`_qa_*`, `_mcp_*`, `qa-*.png`)
- `.venv/`, caches, `gdrive_accounts.json`, session secrets
- Absolute machine paths in committed MCP configs
