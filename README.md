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
   pip install requests curl_cffi privatebinapi
   ```
3. **Run the application**:
   ```bash
   python main.py
   ```
4. Open [http://localhost:8000](http://localhost:8000) in your browser.

## Customization

Currently configured for Call of Duty: Modern Warfare (2019), but designed to be refactored into a universal repack downloader.
