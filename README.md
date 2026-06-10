> [!WARNING]
> Usage of this tool is entirely at your own risk. The author assumes no responsibility for any adverse consequences that may arise from its use.

# ExitLag Auto Signup Lite

A lightweight CLI version of [exitlag-auto-signup-revamp](https://github.com/TDoomX/exitlag-auto-signup-revamp) — no graphical interface, runs directly in the terminal.

## Features

- Automatic account creation for 3-day and 7-day plans
- Supports any Chromium-based browser (Chrome, Brave, Opera GX)
- Password complexity checker with random password generation
- Proxy support
- Fill speed control (slow, fast, superfast)
- Silent mode (headless) with Ghost Mode — hides the browser window by process ID
- Automatic system language detection (11 languages)
- Configuration saving for reuse
- Automatic update checker
- No webdriver required

## Requirements

> [!NOTE]
> For full Unicode support (Japanese, Chinese, Russian, Arabic), [Windows Terminal](https://aka.ms/terminal) is recommended. Without it the script will fall back to English automatically.

## Installation

### Option A — Executable (no Python required)

Download the latest release zip from the [Releases](https://github.com/TDoomX/exitlag-auto-signup-revamp-lite/releases) page, extract everything and run `mainrev-lite.exe` directly. No dependencies needed.

### Option B — Run from source

**1. Clone the repository:**
```shell
git clone https://github.com/TDoomX/exitlag-auto-signup-revamp-lite
```

**2. Install dependencies:**
```shell
pip install -r requirements.txt
```

**3. Run:**
```shell
python main_lite.py
```

## Usage

On startup the script will prompt for:
- Browser path (Chrome, Brave or Opera GX)
- Password (or generates one randomly)
- Proxy (optional)
- Number of accounts to create
- Desired plan (3-day trial or 7-day OMEN)
- Fill speed
- Silent mode
- Close after

Generated credentials are automatically saved to `accounts.txt`.

## Supported Languages

Portuguese, English, Spanish, French, German, Italian, Russian, Japanese, Chinese, Vietnamese, Arabic

## Full Version

Looking for a graphical interface with more controls? Check out [exitlag-auto-signup-revamp](https://github.com/TDoomX/exitlag-auto-signup-revamp).

## Author

Doom — [![Discord](https://img.shields.io/discord/1452848560910368933?label=Discord&logo=discord&color=5865F2)](https://discord.gg/WT5MNusUDX)
