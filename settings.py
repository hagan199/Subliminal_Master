# ──────────────────────────────────────────────────────────────
#  Subliminal Master - Settings Persistence
# ──────────────────────────────────────────────────────────────

import json


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
            with open(self.filename, "r") as f:
                data = json.load(f)
                for key, value in self.DEFAULTS.items():
                    if key not in data:
                        data[key] = value
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return self.DEFAULTS.copy()

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key):
        return self.data.get(key, self.DEFAULTS.get(key))

    def set(self, key, value):
        self.data[key] = value
        self.save()
