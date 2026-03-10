# Subliminal Master v4.0

**Flash affirmations on your screen below conscious perception.**
Your subconscious absorbs the messages while you work, study, or sleep.

By [Emmanuel Hagan](https://www.linkedin.com/in/emmanuel-hagan/) | Free & Open Source

---

## Features

- **Subliminal Flashing** — Messages appear and disappear in milliseconds across all monitors
- **4 Flash Effects** — Instant, Fade In, Glow Pulse, Typewriter
- **5 Focus Zones** — Full Screen, Top Half, Bottom Half, Center Band, Corners Only
- **Vision Board** — Flash images alongside text (PNG, JPG, GIF, BMP, WebP)
- **Breathing Sync** — Messages flash during exhale phase for maximum receptivity
- **Power Hour** — Rapid-fire intensity mode with faster flashing
- **Night Mode** — Warm amber colors, easy on eyes while sleeping
- **Stealth Mode** — Hide the app window, keep subliminals running
- **Rainbow Neon Mode** — Random vibrant colors each flash
- **Mirror Mode** — Reversed text for subconscious reading
- **Message Categories** — Career, Financial, Healing, Education (toggleable)
- **Preset Packs** — Wealth, Confidence, Health, Love, Career affirmation bundles
- **Custom Messages** — Add, edit, import, and export your own affirmations
- **Auto-Stop Timer** — Set a timer (up to 2 hours) for sleep sessions
- **Auto-Start** — Start flashing when the app opens
- **Run on Startup** — Launch automatically when you log in (Windows & macOS)
- **Stats Dashboard** — Track streak days, total flashes, and session count
- **Keyboard Shortcuts** — Ctrl+S (Start/Stop), Ctrl+H (Stealth), Ctrl+P (Power Hour)
- **Cross-Platform** — Windows + macOS + Linux
- **Security Hardened** — Input validation, path sanitization, file integrity checks

## Requirements

- Python 3.11+ (tested on 3.13)
- Windows 10/11, macOS, or Linux

## Quick Start

### Run from Source

```bash
# Install dependencies
pip install screeninfo Pillow

# Run the app
python subliminal_master.py
```

### Build as Executable (.exe)

```bash
pip install pyinstaller
pyinstaller SubliminalMaster.spec --clean --noconfirm
```

The `.exe` will be in the `dist/` folder. Double-click `SubliminalMaster.exe` to launch.

## Project Structure

```
subliminal_master.py   — Entry point
app.py                 — Main UI (tabbed interface with Dashboard, Messages, Effects, Settings)
flasher.py             — Flash engine (overlay windows, animations, effects)
settings.py            — Settings persistence with validation & sanitization
messages.py            — Built-in default affirmation messages
constants.py           — Theme colors, effects, zones, presets
ui_helpers.py          — Reusable UI components (sections, sliders, toggles)
platform_utils.py      — Cross-platform utilities (fonts, sound, transparency, startup)
SubliminalMaster.spec  — PyInstaller build spec
settings.json          — User settings (auto-saved)
messages_*.txt         — Message files by category (one message per line)
```

## Message Files

Place `.txt` files in the project root named `messages_<category>.txt`:

- `messages_career.txt` — weighted 4x (priority)
- `messages_financial.txt` — weighted 1x
- `messages_healing.txt` — weighted 1x
- `messages_education.txt` — weighted 1x

Format: one message per line. Empty lines are ignored. If no files exist, built-in defaults are used.

## Settings

All settings are saved in `settings.json` and validated on load:

| Setting | Type | Range | Default |
|---------|------|-------|---------|
| batch_size | int | 1-10 | 5 |
| flash_duration_ms | int | 1-500 | 35 |
| interval_seconds | float | 0.1-30 | 3.0 |
| margin_px | int | 0-200 | 20 |
| font_size | int | 8-200 | 38 |
| font_color | hex | #RRGGBB | #00E676 |
| auto_stop_minutes | int | 0-1440 | 0 |
| test_mode | bool | — | false |

## Security

The app includes multiple layers of protection:

- **Input validation** — All settings type-checked, range-clamped, and whitelist-validated
- **File size limits** — Settings (1 MB), messages (5 MB), images (50 MB)
- **Path traversal protection** — Message files restricted to working directory
- **Image integrity verification** — PIL verify() before processing
- **Atomic file writes** — Settings saved via temp file + rename (prevents corruption)
- **XML injection protection** — macOS plist paths are escaped
- **Startup path validation** — Blocks shell metacharacters in registry/plist paths
- **Extension whitelisting** — Only allowed file types for images and imports
- **Unknown key stripping** — Prevents data injection via settings.json

## Troubleshooting

- **Messages not visible** — Enable Test Mode in Settings tab, increase Display Time
- **Build error "Access is denied"** — Close the running .exe first, then rebuild
- **No messages loaded** — Ensure at least one `messages_*.txt` file exists in the project root
- **App won't start** — Run `pip install screeninfo Pillow` and try again

## License

Personal use project. Built with Python, Tkinter, and Pillow.
