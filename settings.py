# ──────────────────────────────────────────────────────────────
#  Subliminal Master - Settings Persistence
# ──────────────────────────────────────────────────────────────

import json
import os
import re
import stat
import tempfile


# Maximum settings file size (1 MB) to prevent loading malicious files
_MAX_SETTINGS_SIZE = 1_048_576

# Validation rules: key -> (type, min, max) or (type,) for non-numeric
_VALIDATION_RULES = {
    "batch_size":            (int, 1, 10),
    "flash_duration_ms":     (int, 1, 500),
    "interval_seconds":      ((int, float), 0.1, 30),
    "margin_px":             (int, 0, 200),
    "font_size":             (int, 8, 200),
    "font_color":            (str,),
    "image_size":            (int, 10, 1000),
    "flash_image_only":      (bool,),
    "test_mode":             (bool,),
    "test_display_seconds":  (int, 0, 60),
    "flash_effect":          (str,),
    "focus_zone":            (str,),
    "rainbow_mode":          (bool,),
    "ambient_sound":         (bool,),
    "auto_stop_minutes":     (int, 0, 1440),
    "session_count":         (int, 0, 999_999_999),
    "total_flashes":         (int, 0, 999_999_999),
    "streak_days":           (int, 0, 999_999),
    "last_session_date":     (str,),
    "image_paths":           (list,),
    "categories_enabled":    (dict,),
    "stealth_mode":          (bool,),
    "breathing_pattern":     (str,),
    "power_hour":            (bool,),
    "mirror_mode":           (bool,),
    "night_mode":            (bool,),
    "auto_start":            (bool,),
    "run_on_startup":        (bool,),
}

# Allowed flash effects and focus zones (whitelist)
_ALLOWED_EFFECTS = {"Instant", "Fade In", "Glow Pulse", "Typewriter"}
_ALLOWED_ZONES = {"Full Screen", "Top Half", "Center Band", "Bottom Half", "Corners Only"}
_ALLOWED_BREATHING = {"Off", "4-7-8 Calm", "Box Breathing 4-4-4-4", "Power Breath 3-3-3", "Deep Focus 5-5-5"}

# Regex for valid hex color
_HEX_COLOR_RE = re.compile(r'^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$')

# Allowed image extensions
_ALLOWED_IMAGE_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}


class Settings:
    """Load, store, and persist user settings as JSON."""

    DEFAULTS = {
        "batch_size": 5,
        "flash_duration_ms": 35,
        "interval_seconds": 3,
        "margin_px": 20,
        "font_size": 38,
        "font_color": "#00E676",
        "image_size": 120,
        "flash_image_only": False,
        "test_mode": False,
        "test_display_seconds": 2,
        "flash_effect": "Instant",
        "focus_zone": "Full Screen",
        "rainbow_mode": False,
        "ambient_sound": False,
        "auto_stop_minutes": 0,
        "session_count": 0,
        "total_flashes": 0,
        "streak_days": 0,
        "last_session_date": "",
        "image_paths": [],
        "categories_enabled": {
            "career": True,
            "financial": True,
            "healing": True,
            "education": True,
        },
        "stealth_mode": False,
        "breathing_pattern": "Off",
        "power_hour": False,
        "mirror_mode": False,
        "night_mode": False,
        "auto_start": False,
        "run_on_startup": False,
    }

    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.data = self._load()

    def _load(self):
        try:
            # Check file size before reading to prevent memory exhaustion
            file_size = os.path.getsize(self.filename)
            if file_size > _MAX_SETTINGS_SIZE:
                print(f"Settings file too large ({file_size} bytes), using defaults.")
                return self.DEFAULTS.copy()

            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)

                if not isinstance(data, dict):
                    return self.DEFAULTS.copy()

                # Fill in missing keys with defaults
                for key, value in self.DEFAULTS.items():
                    if key not in data:
                        data[key] = value

                # Validate and sanitize all loaded values
                data = self._sanitize(data)
                return data
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return self.DEFAULTS.copy()

    def _sanitize(self, data):
        """Validate and clamp all settings to safe values."""
        for key, rule in _VALIDATION_RULES.items():
            if key not in data:
                continue
            value = data[key]
            expected_type = rule[0]

            # Type check
            if isinstance(expected_type, tuple):
                if not isinstance(value, expected_type):
                    data[key] = self.DEFAULTS[key]
                    continue
            else:
                # Allow int where float is expected
                if expected_type in (int, float) and isinstance(value, (int, float)):
                    value = expected_type(value)
                    data[key] = value
                elif not isinstance(value, expected_type):
                    data[key] = self.DEFAULTS[key]
                    continue

            # Range clamp for numeric types
            if len(rule) == 3 and isinstance(value, (int, float)):
                _, min_val, max_val = rule
                data[key] = max(min_val, min(max_val, value))

        # Whitelist validation for enum-like strings
        if data.get("flash_effect") not in _ALLOWED_EFFECTS:
            data["flash_effect"] = self.DEFAULTS["flash_effect"]
        if data.get("focus_zone") not in _ALLOWED_ZONES:
            data["focus_zone"] = self.DEFAULTS["focus_zone"]
        if data.get("breathing_pattern") not in _ALLOWED_BREATHING:
            data["breathing_pattern"] = self.DEFAULTS["breathing_pattern"]

        # Validate hex color
        if not _HEX_COLOR_RE.match(data.get("font_color", "")):
            data["font_color"] = self.DEFAULTS["font_color"]

        # Validate date format (YYYY-MM-DD or empty)
        date_str = data.get("last_session_date", "")
        if date_str and not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            data["last_session_date"] = ""

        # Validate image paths: must exist, have allowed extension, be real files
        data["image_paths"] = self._sanitize_image_paths(
            data.get("image_paths", []))

        # Validate categories_enabled: only allow known keys with bool values
        cats = data.get("categories_enabled", {})
        if not isinstance(cats, dict):
            cats = self.DEFAULTS["categories_enabled"].copy()
        safe_cats = {}
        for cat_key in self.DEFAULTS["categories_enabled"]:
            val = cats.get(cat_key, True)
            safe_cats[cat_key] = bool(val)
        data["categories_enabled"] = safe_cats

        # Strip any unknown keys to prevent data injection
        known_keys = set(self.DEFAULTS.keys())
        for key in list(data.keys()):
            if key not in known_keys:
                del data[key]

        return data

    @staticmethod
    def _sanitize_image_paths(paths):
        """Filter image paths to only existing files with allowed extensions."""
        if not isinstance(paths, list):
            return []
        safe_paths = []
        for p in paths:
            if not isinstance(p, str) or len(p) > 1024:
                continue
            ext = os.path.splitext(p)[1].lower()
            if ext not in _ALLOWED_IMAGE_EXT:
                continue
            if os.path.isfile(p):
                safe_paths.append(p)
        return safe_paths

    def save(self):
        try:
            # Atomic write: write to temp file first, then rename
            # This prevents corruption if the app crashes mid-write
            dir_name = os.path.dirname(os.path.abspath(self.filename))
            fd, tmp_path = tempfile.mkstemp(
                suffix=".tmp", prefix="settings_", dir=dir_name)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=4)
                # Replace the original file atomically
                # On Windows, need to remove target first
                if os.path.exists(self.filename):
                    os.replace(tmp_path, self.filename)
                else:
                    os.rename(tmp_path, self.filename)
            except Exception:
                # Clean up temp file on failure
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
                raise
        except OSError as e:
            print(f"Could not save settings: {e}")

    def get(self, key):
        return self.data.get(key, self.DEFAULTS.get(key))

    def set(self, key, value):
        # Only allow known keys
        if key not in self.DEFAULTS:
            return
        # Validate the single value before storing
        temp = {key: value}
        rule = _VALIDATION_RULES.get(key)
        if rule:
            temp_full = dict(self.data)
            temp_full[key] = value
            temp_full = self._sanitize(temp_full)
            value = temp_full[key]
        self.data[key] = value
        self.save()
