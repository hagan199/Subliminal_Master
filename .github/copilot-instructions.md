# Subliminal Master — AI Coding Agent Guidelines

## Project Overview
**Subliminal Master** flashes rapid affirmational messages across Windows desktop screens. Uses Tkinter GUI, `screeninfo` for multi-monitor detection, and PyInstaller for packaging. Supports weighted message categories (prophetic 2×, spiritual 2×, career 4×) and Test Mode for visibility debugging.

## Architecture Essentials

### 1. Message Loading & Weighting (`SubliminalFlasher._load_messages()`)
Messages loaded from `messages_*.txt` files via `glob.glob()` with category-based weights duplicated in a pool before random draw.

**Weight mapping** (from filename prefix):
- `prophetic` → weight 2 (doubled in pool)
- `spiritual` → weight 2 (doubled in pool)  
- `career` → weight 4 (quadrupled in pool)
- Default fallback: `AWESOME_MESSAGES` constant (~260 built-in messages)

**Load logic:** Extract category from filename → read lines → add to pool N times (weight×) → shuffle. Empty lines ignored.

### 2. Settings Class (Two-Phase Load Pattern)
`Settings` class with lazy JSON persistence:
- `load()`: Returns loaded dict or defaults if file missing
- `set(key, value)`: Updates dict AND immediately writes `settings.json`
- `get(key)`: Returns from dict or default value

**Active settings keys:**
- Behavior: `batch_size` (1-5), `flash_duration_ms` (5-50), `interval_seconds` (0.1-5), `margin_px` (0-50)
- Appearance: `font_size` (10-100), `font_color` (hex string)
- Test: `test_mode` (bool), `test_display_seconds` (1-10)

Unused but present: `font_family`, `font_weight`, `window_theme`, `auto_start`, `fade_effect`, `random_position`, `priority_mode`, `scientific_mode`, `use_message_files`, `enhanced_mode`, `test_flash_duration_ms`, `test_font_size`

### 3. Window Creation & Display Loop
**`_flash_batch()` → `_create_flash_window()`:**
1. Pop message from `current_messages` pool, reshuffle when empty
2. Create or reuse `Toplevel` window with black background
3. Position randomly via `_get_random_position()` respecting `margin_px` bounds
4. Schedule hide via `_hide_window()` after `flash_duration_ms` (or `test_display_seconds×7000` in test mode)
5. Window returned to `window_pool` for reuse

**Multi-monitor:** `screeninfo.get_monitors()` called once in `__init__`, random monitor chosen per window.

### 4. Tkinter GUI (App Class)
Single main window with:
- **Behavior frame:** Four sliders (batch size, flash duration, interval, margin) → real-time `settings.set()`
- **Appearance frame:** Font size slider + color picker + import messages button
- **Test Mode frame:** Checkbox to toggle `test_mode`, slider for display seconds
- **Start/Stop button:** Calls `toggle_flasher()` to manage `SubliminalFlasher.start()`/`.stop()`

Style: Dark theme (#2E2E2E bg), green/red button states, `ttk.Scale` for all sliders.

## Development Workflows

### Run from Source
```bash
pip install screeninfo
python subliminal_master.py
```

### Build Executable
```bash
pip install pyinstaller
pyinstaller subliminal_master_fixed.spec --clean --noconfirm
```
Spec includes message files and settings.json as bundled data; sets `console=False`.

### Test Visibility Changes
Enable `test_mode=True` in GUI or settings.json:
- Full opacity (1.0 alpha)
- Extended display time (test_display_seconds × 7000 ms)
- Window title changes to include "TEST MODE"

## Common Tasks

**Add a new setting:** Create slider in appearance/behavior frame → callback calls `settings.set()` → reference key in flashing logic.

**Add message category:** Create `messages_newcategory.txt` → add weight mapping in `_load_messages()` → glob pattern auto-detects.

**Debug window positioning:** Verify `_get_random_position()` respects monitor bounds. Check `max_x < min_x` and `max_y < min_y` safety checks.

## Key Files
- [subliminal_master.py](subliminal_master.py) — `Settings`, `SubliminalFlasher`, `App` classes
- [messages_*.txt](messages_career.txt) — One message per line (one per category file)
- [settings.json](settings.json) — Persisted user config
- [subliminal_master_fixed.spec](subliminal_master_fixed.spec) — PyInstaller config

## External Deps
- **screeninfo** (runtime) — Monitor bounds detection
- **tkinter** (bundled with Python)
- **PyInstaller** (dev-only, packaging)
