# MCP setup (continue work from another PC)

This repo ships a **project-scoped** Grok MCP config:

```
.grok/config.toml
```

Grok loads it automatically when you open this folder (after the project is trusted).

## 1. Prerequisites

| Tool | Why |
|------|-----|
| [Grok / Grok Build CLI](https://x.ai) | Agent + MCP host |
| **Node.js 18+** | Playwright MCP via `npx` |
| **Python 3.11+** | App server (`main.py`) |
| Git | Clone / push |

Optional global Grok config lives in `~/.grok/config.toml` (Windows: `%USERPROFILE%\.grok\config.toml`).

## 2. Playwright MCP (required for UI QA)

Configured in `.grok/config.toml` as `playwright`:

- headless Chromium only (does **not** open Zen / visible Chrome)
- package: `@playwright/mcp@latest`

### First-time install on a new PC

```bash
# Node must be on PATH
node -v
npm -v

# Warm npx cache + install browser binaries
npx -y @playwright/mcp@latest --help
npx playwright install chromium
```

Then open this repo in Grok and confirm:

```bash
grok mcp list
grok mcp doctor playwright
```

You should see `playwright` with status OK / connected.

### What we use it for

- Open `http://127.0.0.1:8000/`
- Click catalog cards, open details
- Screenshots of haze / layout / download dock
- Multi-viewport adaptive catalog checks

## 3. Optional MCPs used on the original machine

These are **not** enabled in the repo (absolute paths differ per PC).

### Bebranoid Telegram session

```toml
# Put in ~/.grok/config.toml (user scope), not committed

[mcp_servers.bebranoid-telegram]
command = "node"
args = ["C:/YOUR/PATH/Bebranoid/mcp-telegram-session/server.js"]
enabled = true
startup_timeout_sec = 15

[mcp_servers.bebranoid-verify]
command = "node"
args = ["C:/YOUR/PATH/Bebranoid/mcp-bebranoid-verify/server.js"]
enabled = true
startup_timeout_sec = 20
tool_timeout_sec = 180
```

Only needed if you work on Harmonoid/Telegram integration alongside this downloader.

## 4. Run the app

```bash
cd fitgirl-downloader
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt   # if present; else: pip install requests curl_cffi beautifulsoup4
python main.py
```

Open: [http://localhost:8000](http://localhost:8000)

Helpers:

- `Run_Downloader.bat` — launch
- `kill_old_servers.ps1` — free port 8000 without killing the new process tree

## 5. Suggested `~/.grok/config.toml` baseline (any PC)

```toml
[cli]
installer = "internal"

[ui]
permission_mode = "always-approve"   # or leave default and approve prompts

[models]
default = "grok-4.5"
default_reasoning_effort = "high"

# Playwright can live only in project .grok/config.toml (already shipped).
# Duplicate here only if you want it in every project:
#
# [mcp_servers.playwright]
# command = "npx"
# args = ["-y", "@playwright/mcp@latest", "--headless", "--browser", "chromium"]
# enabled = true
# startup_timeout_sec = 120
# tool_timeout_sec = 180
```

## 6. GitHub remote

```bash
git clone https://github.com/GitGayHub/fitgirl-downloader.git
cd fitgirl-downloader
```

Use your own auth (SSH key or `gh auth login`). Do **not** commit PATs into remote URLs.

## 7. QA scripts (optional)

Local headless checks (Playwright Python):

```bash
pip install playwright
playwright install chromium
python _qa_adapt.py    # catalog density + download dock
python _qa_ui6.py      # layout / haze smoke
```

Screenshot dumps (`_qa_*.png`, `_mcp_*.png`) are gitignored.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `playwright` missing in Grok | Trust project folder; check `.grok/config.toml` exists |
| MCP startup timeout | Raise `startup_timeout_sec`; run `npx playwright install chromium` once |
| `ERR_CONNECTION_REFUSED` in browser MCP | Start `python main.py` first (port 8000) |
| Black haze / old UI | Hard refresh `Ctrl+Shift+R` (cache-busted assets on `/`) |
| Port already in use | `.\kill_old_servers.ps1` then restart |
