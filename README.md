# Subliminal Master — Installation & Usage Guide

## Overview
- Desktop app that flashes short, weighted messages on your screen.
- Supports message files per category with priority weighting: `prophetic` (3×), `spiritual` (2×), `career` (1×).
- Includes a Test Mode that shows messages clearly (for eye‑visible testing) with adjustable display time.

## Requirements
- Windows 10/11
- Python `3.11+` (tested on `3.13`)
- Tcl/Tk (bundled with standard Python on Windows)
- `pip` (bundled with Python)

## Project Layout
- `subliminal_master.py` — main application (classic UI)
- `subliminal_master_fixed.spec` — PyInstaller spec to build the `.exe`
- `messages_spiritual.txt`, `messages_prophetic.txt`, `messages_career.txt` — message sources (one message per line)
- `settings.json` — app settings saved automatically
- `dist/` — created after building the executable (contains the `.exe` and runtime files)

## Quick Start (Run from Source)
1. Open a terminal in the project folder: `c:\Users\hagan\OneDrive\Desktop\new_me`
2. (Optional) Create a virtual environment:
   - `python -m venv .venv`
   - `.\.venv\Scripts\activate`
3. Install dependencies:
   - `pip install screeninfo`
4. Run the app:
   - `python subliminal_master.py`

## Build the Executable (.exe)
1. Install PyInstaller:
   - `pip install pyinstaller`
2. Build with the provided spec (includes message files and settings):
   - `pyinstaller subliminal_master_fixed.spec --clean --noconfirm`
3. Copy message files to `dist` (if not already present):
   - Git Bash: `cp messages_*.txt dist/`
   - PowerShell: `Copy-Item messages_*.txt dist/`
4. Launch the app:
   - Double‑click `dist\SubliminalMaster_Fixed.exe`
   - Optional: use `dist\Run_SubliminalMaster.bat` if present

## Using the App
- Start/Stop:
  - Click `Start` to begin flashing batches; `Stop` to halt.
- Behavior panel:
  - `Batch Size (1-5)`: number of messages per batch.
  - `Flash Duration (ms, 5-50)`: subliminal visibility time per window.
  - `Interval (s, 0.1-5)`: delay between batches.
  - `Edge Margin (px, 0-50)`: keeps windows inside screen edges.
- Appearance & Content:
  - `Font Size (10-100)`: text size (capped internally for window sizing).
  - `Change Text Color`: pick a hex color (e.g. `#213821`).
  - `Import Messages`: load a custom `.txt` (one message per line).
- Test Mode:
  - Enable `Test Mode (Messages Visible)` to see messages clearly (full opacity).
  - Adjust `Display Time (s, 1-10)` to control how long messages stay visible.
  - Window title shows `TEST MODE` when enabled.

## Message Files
- Place files in the project root with names that include the category:
  - `messages_prophetic.txt` → weight `3×`
  - `messages_spiritual.txt` → weight `2×`
  - `messages_career.txt` → weight `1×`
- Format: one message per line; empty lines are ignored.
- If no `messages_*.txt` are found, the app falls back to built‑in messages.

## Settings (`settings.json`)
- Keys used by the app:
  - `batch_size` — integer 1–5
  - `flash_duration_ms` — integer 5–50
  - `interval_seconds` — float 0.1–5
  - `margin_px` — integer 0–50
  - `font_size` — integer 10–100 (internally capped for window sizing)
  - `font_color` — hex color (e.g. `#213821`)
  - `test_mode` — boolean (true/false)
  - `test_display_seconds` — integer 1–10
- Notes:
  - Sliders update `settings.json` in real time.
  - Clicking `Start` applies current slider values before flashing.

## Troubleshooting
- Start button “not working”:
  - Ensure Python/Tkinter installed: `python --version`.
  - Verify `screeninfo` is installed: `pip show screeninfo`.
  - Check console output (if running `.exe` built with `console=True`).
  - The windows may open on a different monitor; try enabling Test Mode.
- Build error `PermissionError: Access is denied`:
  - Close any running `.exe` from a previous build.
  - Delete `build/` and `dist/` (or use `--clean`) and rebuild.
- Messages not visible:
  - Enable Test Mode and increase `Display Time`.
  - Pick a contrasting `font_color`.
- No messages loaded:
  - Ensure at least one `messages_*.txt` file exists.
  - Use `Import Messages` to verify a custom file.

## Advanced
- Change executable name:
  - Edit `name='SubliminalMaster_Fixed'` in `subliminal_master_fixed.spec`.
- Hide console in production:
  - Set `console=False` in the spec and rebuild.
- Rebuild commands reference:
  - `pyinstaller subliminal_master_fixed.spec --clean --noconfirm`

## License & Credits
- Personal use project created for affirmations and subliminal testing.
- Uses `tkinter` (GUI), `screeninfo` (monitor detection), and `PyInstaller` for packaging.

