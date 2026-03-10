# ──────────────────────────────────────────────────────────────
#  Subliminal Master - Flash Engine
#  Creates transparent overlay windows that display messages
#  with various animation effects across all monitors.
#  Works on Windows, macOS, and Linux.
# ──────────────────────────────────────────────────────────────

import tkinter as tk
from tkinter import font
import random
import glob
import os
import time
import math
import datetime
from screeninfo import get_monitors

from constants import NEON_COLORS, BREATHING_PATTERNS
from messages import AWESOME_MESSAGES
from platform_utils import (
    make_window_transparent, get_transparent_bg, play_ping,
    HAS_SOUND, FONT_FAMILY,
)

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Security limits
_MAX_MESSAGE_LENGTH = 500       # Max characters per message
_MAX_MESSAGES_TOTAL = 10_000    # Max messages in pool
_MAX_FILE_SIZE = 5_242_880      # 5 MB max for message files
_MAX_IMAGE_SIZE = 52_428_800    # 50 MB max for image files
_ALLOWED_IMAGE_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}

# Pre-compute transparent bg once
_TRANS_BG = get_transparent_bg()

# Window pool size to pre-create at startup for smoother first flashes
_PREPOOL_SIZE = 5


class SubliminalFlasher:
    """Core engine that flashes subliminal messages on screen."""

    def __init__(self, root, settings):
        self.root = root
        self.settings = settings
        self.is_running = False
        self.flash_count = 0
        self.message_pool = []
        self.current_messages = []
        self.job_id = None
        self.fade_jobs = []
        self.active_windows = []
        self.window_pool = []
        self.cached_font = None
        self.cached_font_size = -1
        self.monitors = get_monitors()
        self.image_paths = list(self.settings.get("image_paths") or [])
        self.image_index = 0
        self.cached_photos = {}
        self.session_start = None
        self.auto_stop_job = None
        self._load_messages()
        self._shuffle_pool()

    def prepool_windows(self):
        """Pre-create window pool for smoother first flashes. Call after mainloop starts."""
        for _ in range(_PREPOOL_SIZE):
            w, lbl, img_lbl = self._make_flash_window()
            w.withdraw()
            self.window_pool.append((w, lbl, img_lbl))

    # ── Message Loading ─────────────────────────────────────

    @staticmethod
    def _sanitize_message(msg):
        """Sanitize a single message string."""
        if not isinstance(msg, str):
            return None
        msg = msg.strip()
        if not msg:
            return None
        # Truncate overly long messages
        if len(msg) > _MAX_MESSAGE_LENGTH:
            msg = msg[:_MAX_MESSAGE_LENGTH]
        return msg

    def _safe_read_message_file(self, filepath):
        """Read a message file with size and content validation."""
        try:
            file_size = os.path.getsize(filepath)
            if file_size > _MAX_FILE_SIZE:
                print(f"Skipping {filepath}: file too large ({file_size} bytes)")
                return []
            with open(filepath, "r", encoding="utf-8") as f:
                msgs = []
                for line in f:
                    msg = self._sanitize_message(line)
                    if msg:
                        msgs.append(msg)
                    if len(msgs) >= _MAX_MESSAGES_TOTAL:
                        break
                return msgs
        except (OSError, UnicodeDecodeError) as e:
            print(f"Error reading {filepath}: {e}")
            return []

    def _load_messages(self):
        self.message_pool = []
        # Only load message files from the current working directory
        message_files = glob.glob("messages_*.txt")
        cats = self.settings.get("categories_enabled") or {}

        category_weights = {
            "career": 4,
            "awesome": 1,
        }

        if not message_files:
            msgs = self._safe_read_message_file("messages.txt")
            if msgs:
                self.message_pool = msgs
        else:
            for filepath in message_files:
                try:
                    # Ensure file is in current directory (no path traversal)
                    real_path = os.path.realpath(filepath)
                    real_cwd = os.path.realpath(".")
                    if not real_path.startswith(real_cwd):
                        print(f"Skipping {filepath}: outside working directory")
                        continue

                    filename_lower = os.path.basename(filepath).lower()
                    skip = False
                    for cat_key in cats:
                        if cat_key in filename_lower and not cats.get(cat_key, True):
                            skip = True
                            break
                    if skip:
                        continue

                    msgs = self._safe_read_message_file(filepath)
                    if msgs:
                        weight = 1
                        for category, cat_weight in category_weights.items():
                            if category in filename_lower:
                                weight = cat_weight
                                break
                        for _ in range(weight):
                            self.message_pool.extend(msgs)
                        # Enforce total pool limit
                        if len(self.message_pool) >= _MAX_MESSAGES_TOTAL:
                            self.message_pool = self.message_pool[:_MAX_MESSAGES_TOTAL]
                            break
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")

        if not self.message_pool:
            self.message_pool = AWESOME_MESSAGES.copy()

    def _shuffle_pool(self):
        random.shuffle(self.message_pool)
        self.current_messages = self.message_pool.copy()

    # ── Positioning ─────────────────────────────────────────

    def _get_zone_position(self, width, height):
        monitor = random.choice(self.monitors)
        margin = self.settings.get("margin_px")
        zone = self.settings.get("focus_zone")

        mx = monitor.x + margin
        my = monitor.y + margin
        mw = max(monitor.width - 2 * margin - width, 0)
        mh = max(monitor.height - 2 * margin - height, 0)

        if zone == "Top Half":
            return mx + random.randint(0, mw), my + random.randint(0, max(mh // 2, 0))
        elif zone == "Bottom Half":
            return mx + random.randint(0, mw), my + max(mh // 2, 0) + random.randint(0, max(mh // 2, 0))
        elif zone == "Center Band":
            cy = my + mh // 4
            return mx + random.randint(0, mw), cy + random.randint(0, max(mh // 2, 0))
        elif zone == "Corners Only":
            corners = [(mx, my), (mx + mw, my), (mx, my + mh), (mx + mw, my + mh)]
            return random.choice(corners)
        else:  # Full Screen
            return mx + random.randint(0, mw), my + random.randint(0, mh)

    # ── Image Handling ──────────────────────────────────────

    @staticmethod
    def _validate_image_path(path):
        """Validate that an image path is safe to load."""
        if not isinstance(path, str) or len(path) > 1024:
            return False
        ext = os.path.splitext(path)[1].lower()
        if ext not in _ALLOWED_IMAGE_EXT:
            return False
        if not os.path.isfile(path):
            return False
        try:
            file_size = os.path.getsize(path)
            if file_size > _MAX_IMAGE_SIZE:
                print(f"Skipping image {path}: too large ({file_size} bytes)")
                return False
        except OSError:
            return False
        return True

    def _get_next_photo(self):
        if not self.image_paths or not HAS_PIL:
            return None
        img_size = self.settings.get("image_size")
        path = self.image_paths[self.image_index % len(self.image_paths)]
        self.image_index = (self.image_index + 1) % len(self.image_paths)
        cache_key = (path, img_size)
        if cache_key in self.cached_photos:
            return self.cached_photos[cache_key]
        if not self._validate_image_path(path):
            return None
        try:
            img = Image.open(path)
            # Verify image integrity before processing
            img.verify()
            # Re-open after verify (verify closes the file)
            img = Image.open(path)
            img.thumbnail((img_size, img_size), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.cached_photos[cache_key] = photo
            return photo
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None

    def add_image(self, path):
        if not self._validate_image_path(path):
            print(f"Rejected image: {path}")
            return
        if path not in self.image_paths:
            self.image_paths.append(path)
            self.settings.set("image_paths", self.image_paths)

    def remove_image(self, path):
        if path in self.image_paths:
            self.image_paths.remove(path)
            self.cached_photos = {k: v for k, v in self.cached_photos.items() if k[0] != path}
            self.settings.set("image_paths", self.image_paths)

    def clear_all_images(self):
        self.image_paths.clear()
        self.cached_photos.clear()
        self.image_index = 0
        self.settings.set("image_paths", [])

    # ── Color & Transform ───────────────────────────────────

    def _get_flash_color(self):
        if self.settings.get("night_mode"):
            return random.choice(["#FF8F00", "#FFA726", "#FFB74D", "#FFCC02", "#E65100"])
        if self.settings.get("rainbow_mode"):
            return random.choice(NEON_COLORS)
        return self.settings.get("font_color")

    def _transform_message(self, message):
        if self.settings.get("mirror_mode"):
            message = message[::-1]
        return message

    # ── Breathing Sync ──────────────────────────────────────

    def _get_breathing_phase(self):
        pattern_name = self.settings.get("breathing_pattern")
        pattern = BREATHING_PATTERNS.get(pattern_name)
        if not pattern or not self.session_start:
            return None
        inhale, hold, exhale = pattern
        cycle_len = inhale + hold + exhale
        elapsed = (time.time() - self.session_start) % cycle_len
        if elapsed < inhale:
            return "INHALE"
        elif elapsed < inhale + hold:
            return "HOLD"
        return "EXHALE"

    # ── Flash Execution ─────────────────────────────────────

    def _flash_batch(self):
        if not self.is_running:
            return

        if self.settings.get("power_hour"):
            batch_size = min(self.settings.get("batch_size") + 3, 10)
        else:
            batch_size = self.settings.get("batch_size")

        # Only flash during EXHALE (most receptive phase)
        breath_phase = self._get_breathing_phase()
        if breath_phase and breath_phase != "EXHALE":
            self.job_id = self.root.after(200, self._flash_batch)
            return

        for _ in range(batch_size):
            if not self.current_messages:
                self._shuffle_pool()
            message = self.current_messages.pop()
            message = self._transform_message(message)
            self._create_flash_window(message)
            self.flash_count += 1

        # Sound removed — silent operation
        pass  # ambient sound disabled

        if self.settings.get("power_hour"):
            delay_ms = max(int(self.settings.get("interval_seconds") * 800), 200)
        else:
            delay_ms = int(self.settings.get("interval_seconds") * 2000)
        self.job_id = self.root.after(delay_ms, self._flash_batch)

    def _make_flash_window(self):
        """Create a new flash overlay window (platform-safe)."""
        window = tk.Toplevel(self.root)
        make_window_transparent(window)
        img_label = tk.Label(window, bg=_TRANS_BG)
        img_label.pack(padx=10, pady=5)
        label = tk.Label(window, bg=_TRANS_BG, justify=tk.CENTER)
        label.pack(padx=20, pady=10)
        return window, label, img_label

    def _create_flash_window(self, message):
        if self.window_pool:
            window, label, img_label = self.window_pool.pop()
        else:
            window, label, img_label = self._make_flash_window()

        font_size = min(self.settings.get("font_size"), 32)
        if self.settings.get("test_mode"):
            font_size = max(font_size, 24)
        if font_size != self.cached_font_size:
            self.cached_font_size = font_size
            self.cached_font = font.Font(family=FONT_FAMILY, size=font_size, weight="bold")

        flash_image_only = self.settings.get("flash_image_only")
        photo = self._get_next_photo()
        color = self._get_flash_color()

        if photo:
            img_label.config(image=photo)
            img_label.image = photo
        else:
            img_label.config(image="")
            img_label.image = None

        if flash_image_only and photo:
            label.config(text="", font=self.cached_font)
        else:
            label.config(text=message, font=self.cached_font, fg=color,
                         wraplength=self.monitors[0].width * 0.7)

        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x, y = self._get_zone_position(width, height)
        window.geometry(f"{width}x{height}+{x}+{y}")

        effect = self.settings.get("flash_effect")
        if self.settings.get("test_mode"):
            display_time = self.settings.get("test_display_seconds") * 1000
        else:
            display_time = self.settings.get("flash_duration_ms")

        if effect == "Fade In":
            self._effect_fade_in(window, label, img_label, display_time)
        elif effect == "Glow Pulse":
            self._effect_glow_pulse(window, label, img_label, display_time)
        elif effect == "Typewriter" and not (flash_image_only and photo):
            self._effect_typewriter(window, label, img_label, message, color, display_time)
        else:  # Instant
            window.attributes("-alpha", 1.0)
            window.deiconify()
            window.lift()
            self.active_windows.append((window, label, img_label))
            self.root.after(display_time, lambda w=window, l=label, il=img_label: self._hide_window(w, l, il))

    # ── Animation Effects ───────────────────────────────────

    def _effect_fade_in(self, window, label, img_label, display_time):
        window.attributes("-alpha", 0.0)
        window.deiconify()
        window.lift()
        self.active_windows.append((window, label, img_label))

        def fade(step=0):
            if step <= 10:
                try:
                    window.attributes("-alpha", step / 10.0)
                except tk.TclError:
                    return
                job = self.root.after(15, lambda: fade(step + 1))
                self.fade_jobs.append(job)
            else:
                self.root.after(display_time, lambda: self._fade_out(window, label, img_label))
        fade()

    def _fade_out(self, window, label, img_label, step=10):
        if step >= 0:
            try:
                window.attributes("-alpha", step / 10.0)
            except tk.TclError:
                return
            job = self.root.after(20, lambda: self._fade_out(window, label, img_label, step - 1))
            self.fade_jobs.append(job)
        else:
            self._hide_window(window, label, img_label)

    def _effect_glow_pulse(self, window, label, img_label, display_time):
        window.attributes("-alpha", 1.0)
        window.deiconify()
        window.lift()
        self.active_windows.append((window, label, img_label))
        start = time.time()
        total_ms = max(display_time, 150)

        def pulse():
            elapsed = (time.time() - start) * 1000
            if elapsed > total_ms:
                self._hide_window(window, label, img_label)
                return
            alpha = 0.65 + 0.35 * math.sin(elapsed / 50.0)
            try:
                window.attributes("-alpha", alpha)
            except tk.TclError:
                return
            job = self.root.after(16, pulse)
            self.fade_jobs.append(job)
        pulse()

    def _effect_typewriter(self, window, label, img_label, full_text, color, display_time):
        window.attributes("-alpha", 1.0)
        window.deiconify()
        window.lift()
        self.active_windows.append((window, label, img_label))
        chars = list(full_text)
        delay_per_char = max(1, min(display_time // max(len(chars), 1), 30))

        def type_char(i=0):
            if i <= len(chars):
                label.config(text="".join(chars[:i]), fg=color)
                window.update_idletasks()
                job = self.root.after(delay_per_char, lambda: type_char(i + 1))
                self.fade_jobs.append(job)
            else:
                self.root.after(display_time, lambda w=window, l=label, il=img_label: self._hide_window(w, l, il))
        type_char()

    def _hide_window(self, window, label, img_label):
        try:
            window.withdraw()
        except tk.TclError:
            pass
        self.window_pool.append((window, label, img_label))
        if (window, label, img_label) in self.active_windows:
            self.active_windows.remove((window, label, img_label))

    # ── Lifecycle ───────────────────────────────────────────

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.flash_count = 0
        self.session_start = time.time()

        # Update streak
        today = datetime.date.today().isoformat()
        last = self.settings.get("last_session_date")
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        if last == yesterday:
            self.settings.set("streak_days", self.settings.get("streak_days") + 1)
        elif last != today:
            self.settings.set("streak_days", 1)
        self.settings.set("last_session_date", today)
        self.settings.set("session_count", self.settings.get("session_count") + 1)

        # Auto-stop timer
        auto_stop = self.settings.get("auto_stop_minutes")
        if auto_stop and auto_stop > 0:
            self.auto_stop_job = self.root.after(int(auto_stop * 60000), self._auto_stop)

        self._flash_batch()

    def _auto_stop(self):
        if self.is_running:
            self.stop()
            self.root.event_generate("<<AutoStopped>>")

    def stop(self):
        if not self.is_running:
            return
        self.is_running = False

        if self.job_id:
            self.root.after_cancel(self.job_id)
            self.job_id = None
        if self.auto_stop_job:
            self.root.after_cancel(self.auto_stop_job)
            self.auto_stop_job = None

        for job in self.fade_jobs:
            try:
                self.root.after_cancel(job)
            except Exception:
                pass
        self.fade_jobs.clear()

        for window, label, img_label in self.active_windows[:]:
            try:
                window.withdraw()
            except tk.TclError:
                pass
        self.active_windows.clear()

        self.settings.set("total_flashes", self.settings.get("total_flashes") + self.flash_count)
