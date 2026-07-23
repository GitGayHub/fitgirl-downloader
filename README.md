# FitGirl Repack Automated Downloader

A premium, high-performance web dashboard and automated downloader designed to simplify downloading and installing large repack files from FitGirl Repacks. 

It handles PrivateBin link decryption, Cloudflare bypasses, parallel multi-threaded downloading, and automatic archive extraction.

## Features

- 💜 **Stunning Dashboard UI**: Modern violet dark theme with glassmorphism effects, progress circles, and smooth animations.
- ⚡ **Multi-threaded Parallel Downloader**: Configurable download threads (defaults to 4) to saturate your bandwidth.
- 🔄 **IP & VPN Reconnection Protection**: Automatically pauses, renews links, and resumes download if your VPN drops or IP changes.
- 📦 **Automated Unpacking (WinRAR/unrar)**: Seamless extraction of split RAR archives with real-time progress parsing directly inside the dashboard.
- 🛠️ **Failsafe System Logs**: Streams extraction and downloading stdout/stderr messages safely without terminal encoding crashes.

## Tech Stack

- **Backend**: Python (HTTPServer, requests, curl_cffi, privatebinapi)
- **Frontend**: Vanilla HTML5, CSS3, ES6 JavaScript (EMA-filtered speed tracking, dynamic UI updates)

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GitGayHub/fitgirl-downloader.git
   cd fitgirl-downloader
   ```
2. **Install Python dependencies**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   pip install requests curl_cffi privatebinapi beautifulsoup4
   ```
3. **Run the application** (silent, no CMD pile):
   - Double-click **FitGirl Downloader** shortcut (Desktop / Start Menu), or `Launch_Downloader.vbs`
   - Install/refresh shortcuts: `powershell -ExecutionPolicy Bypass -File .\install_shortcuts.ps1`
   - Dev console mode: `python main.py` or `Run_Downloader.bat`
4. Browser opens [http://127.0.0.1:8000](http://127.0.0.1:8000) automatically. Re-launch only focuses the UI if the server is already running.

## Continue with Grok on another PC

Project MCP config is committed at **`.grok/config.toml`** (Playwright headless).

See full instructions: **[docs/MCP_SETUP.md](docs/MCP_SETUP.md)**

Quick check:

```bash
npx playwright install chromium
grok mcp list
grok mcp doctor playwright
```

Agent notes: **[AGENTS.md](AGENTS.md)**
