# ──────────────────────────────────────────────────────────────
#  Subliminal Master - Main Application Window
#  Tabbed UI with Dashboard, Messages, Effects, and Settings.
#  Cross-platform: Windows + macOS + Linux.
# ──────────────────────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
import os
import time
import datetime
import hashlib
import math

from constants import (
    BG_DARK, BG_CARD, BG_ACCENT, BG_INPUT, BG_HOVER,
    FG_PRIMARY, FG_DIM, FG_BRIGHT,
    GREEN, GREEN_HOVER, RED, RED_HOVER, GOLD, PURPLE, PURPLE_HOVER,
    CYAN, PINK, ORANGE,
    FLASH_EFFECTS, FOCUS_ZONES, BREATHING_PATTERNS, MESSAGE_PRESETS,
    COLOR_THEMES, ACHIEVEMENTS, DAILY_QUOTES,
)
from messages import AWESOME_MESSAGES
from flasher import SubliminalFlasher, HAS_PIL
from ui_helpers import make_section, make_labeled_slider, make_toggle
from platform_utils import (
    FONT_FAMILY, FONT_MONO, MOD_KEY, MOD_DISPLAY, IS_MAC,
    is_registered_at_startup, register_at_startup, unregister_at_startup,
)

try:
    from PIL import Image, ImageTk
except ImportError:
    pass


class App(tk.Tk):
    """Main application window with tabbed interface."""

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.flasher = SubliminalFlasher(self, self.settings)
        self._preview_photos = []

        self.title("MindFlash")
        self.geometry("540x780")
        self.minsize(500, 700)
        self.configure(bg=BG_DARK)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.bind("<<AutoStopped>>", lambda e: self._on_auto_stopped())

        self._setup_styles()
        self._build_ui()
        self._update_status_loop()
        self._animate_title()
        self._update_breathing_indicator()
        self._bind_hotkeys()

        # Pre-create window pool and auto-start after UI is ready
        self.after(200, self._on_ready)

    # ════════════════════════════════════════════════════════
    #   STYLES
    # ════════════════════════════════════════════════════════

    def _setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=BG_ACCENT,
                             foreground=FG_DIM, font=(FONT_FAMILY, 10, "bold"),
                             padding=[14, 6])
        self.style.map("TNotebook.Tab",
                       background=[("selected", BG_CARD)],
                       foreground=[("selected", GOLD)])

        self.style.configure("TFrame", background=BG_DARK)
        self.style.configure("Card.TFrame", background=BG_CARD)
        self.style.configure("TLabel", background=BG_DARK, foreground=FG_PRIMARY,
                             font=(FONT_FAMILY, 10))

        self.style.configure("TButton", font=(FONT_FAMILY, 10, "bold"),
                             borderwidth=0, padding=6)
        self.style.map("TButton",
                       background=[("active", BG_HOVER), ("!active", BG_ACCENT)],
                       foreground=[("active", FG_PRIMARY), ("!active", FG_PRIMARY)])

        self.style.configure("Start.TButton", background=GREEN,
                             foreground="#000000", font=(FONT_FAMILY, 15, "bold"),
                             padding=14)
        self.style.map("Start.TButton",
                       background=[("active", GREEN_HOVER), ("!active", GREEN)],
                       foreground=[("active", "#000000"), ("!active", "#000000")])

        self.style.configure("Stop.TButton", background=RED,
                             foreground="#FFFFFF", font=(FONT_FAMILY, 15, "bold"),
                             padding=14)
        self.style.map("Stop.TButton",
                       background=[("active", RED_HOVER), ("!active", RED)],
                       foreground=[("active", "#FFFFFF"), ("!active", "#FFFFFF")])

        self.style.configure("Accent.TButton", background=PURPLE,
                             foreground="#FFFFFF", font=(FONT_FAMILY, 10, "bold"))
        self.style.map("Accent.TButton",
                       background=[("active", PURPLE_HOVER), ("!active", PURPLE)],
                       foreground=[("active", "#FFFFFF"), ("!active", "#FFFFFF")])

        self.style.configure("Danger.TButton", background="#FF1744",
                             foreground="#FFFFFF", font=(FONT_FAMILY, 9, "bold"))
        self.style.map("Danger.TButton",
                       background=[("active", "#FF5252"), ("!active", "#FF1744")],
                       foreground=[("active", "#FFFFFF"), ("!active", "#FFFFFF")])

        self.style.configure("TScale", background=BG_CARD, troughcolor=BG_DARK)
        self.style.configure("TCombobox", fieldbackground=BG_INPUT,
                             background=BG_ACCENT, foreground=FG_PRIMARY,
                             font=(FONT_FAMILY, 10))

    # ════════════════════════════════════════════════════════
    #   LAYOUT
    # ════════════════════════════════════════════════════════

    def _build_ui(self):
        # ── Header (always visible) ──
        header = tk.Frame(self, bg=BG_DARK, padx=20, pady=8)
        header.pack(fill=tk.X)

        self.title_label = tk.Label(header, text="MINDFLASH",
                                    bg=BG_DARK, fg=GOLD,
                                    font=(FONT_FAMILY, 22, "bold"))
        self.title_label.pack()
        self._tagline = tk.Label(header, text="Flash your mind. Shape your future.",
                                 bg=BG_DARK, fg=FG_DIM,
                                 font=(FONT_FAMILY, 9, "italic"))
        self._tagline.pack(pady=(0, 4))

        # ── Big Start / Stop button ──
        self.start_stop_button = ttk.Button(
            header, text="START FLASHING", command=self.toggle_flasher,
            width=24, style="Start.TButton")
        self.start_stop_button.pack(pady=(2, 4))

        # ── Live status bar with pulsing indicator ──
        status_bar = tk.Frame(header, bg=BG_DARK)
        status_bar.pack(fill=tk.X)

        status_row = tk.Frame(status_bar, bg=BG_DARK)
        status_row.pack()
        self._pulse_dot = tk.Label(status_row, text="  ", bg=BG_DARK, fg=BG_DARK,
                                    font=(FONT_FAMILY, 8))
        self._pulse_dot.pack(side=tk.LEFT, padx=(0, 4))
        self.status_label = tk.Label(status_row, text="Ready to go", bg=BG_DARK,
                                     fg=FG_DIM, font=(FONT_FAMILY, 9))
        self.status_label.pack(side=tk.LEFT)

        self.timer_label = tk.Label(status_bar, text="", bg=BG_DARK,
                                    fg=FG_DIM, font=(FONT_FAMILY, 9))
        self.timer_label.pack()

        # ── Tabbed notebook ──
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))

        self._build_dashboard_tab()
        self._build_messages_tab()
        self._build_effects_tab()
        self._build_settings_tab()

    def _make_scrollable_tab(self, tab_title):
        """Return (outer_frame, inner_frame) for a scrollable notebook tab."""
        outer = tk.Frame(self.notebook, bg=BG_DARK)
        canvas = tk.Canvas(outer, bg=BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner = tk.Frame(canvas, bg=BG_DARK, padx=14, pady=10)
        cw = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(cw, width=e.width))

        def _scroll(ev):
            if IS_MAC:
                canvas.yview_scroll(int(-1 * ev.delta), "units")
            else:
                canvas.yview_scroll(int(-1 * (ev.delta / 120)), "units")

        def _on_enter(e):
            canvas.bind_all("<MouseWheel>", _scroll)
            if IS_MAC:
                canvas.bind_all("<Button-4>", lambda ev: canvas.yview_scroll(-3, "units"))
                canvas.bind_all("<Button-5>", lambda ev: canvas.yview_scroll(3, "units"))

        def _on_leave(e):
            canvas.unbind_all("<MouseWheel>")
            if IS_MAC:
                canvas.unbind_all("<Button-4>")
                canvas.unbind_all("<Button-5>")

        canvas.bind("<Enter>", _on_enter)
        canvas.bind("<Leave>", _on_leave)

        self.notebook.add(outer, text=f"  {tab_title}  ")
        return outer, inner

    # ════════════════════════════════════════════════════════
    #   TAB 1 : DASHBOARD
    # ════════════════════════════════════════════════════════

    def _build_dashboard_tab(self):
        _, tab = self._make_scrollable_tab("Dashboard")

        # ── Daily Motivational Quote ──
        quote_section = tk.Frame(tab, bg=BG_CARD, highlightbackground=PURPLE,
                                 highlightthickness=1, padx=16, pady=10)
        quote_section.pack(fill=tk.X, pady=(0, 10))

        # Pick a deterministic daily quote based on date
        day_hash = int(hashlib.md5(
            datetime.date.today().isoformat().encode()).hexdigest(), 16)
        quote_text, quote_author = DAILY_QUOTES[day_hash % len(DAILY_QUOTES)]
        tk.Label(quote_section, text=f'"{quote_text}"', bg=BG_CARD, fg=FG_BRIGHT,
                 font=(FONT_FAMILY, 10, "italic"), wraplength=440,
                 justify=tk.CENTER).pack()
        tk.Label(quote_section, text=f"-- {quote_author}", bg=BG_CARD, fg=PURPLE,
                 font=(FONT_FAMILY, 9)).pack(pady=(2, 0))

        # ── Stats cards ──
        stats_section = make_section(tab, "Your Journey",
                                     "Track your consistency and total subliminal exposure.")

        cards = tk.Frame(stats_section, bg=BG_CARD)
        cards.pack(fill=tk.X, pady=4)
        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)
        cards.columnconfigure(2, weight=1)

        def stat_card(parent, col, title, var_name, color):
            f = tk.Frame(parent, bg=BG_ACCENT, padx=10, pady=8,
                         highlightbackground=BG_DARK, highlightthickness=1)
            f.grid(row=0, column=col, padx=4, sticky="nsew")
            tk.Label(f, text=title, bg=BG_ACCENT, fg=FG_DIM,
                     font=(FONT_FAMILY, 8)).pack()
            lbl = tk.Label(f, text="0", bg=BG_ACCENT, fg=color,
                           font=(FONT_FAMILY, 16, "bold"))
            lbl.pack()
            setattr(self, var_name, lbl)

        stat_card(cards, 0, "STREAK", "_streak_val", GOLD)
        stat_card(cards, 1, "TOTAL FLASHES", "_total_val", CYAN)
        stat_card(cards, 2, "SESSIONS", "_sessions_val", GREEN)
        self._update_stats_display()

        # ── Daily Goal ──
        goal_section = make_section(tab, "Daily Goal",
                                    "Set a daily flash target and track your progress.")

        goal_row = tk.Frame(goal_section, bg=BG_CARD)
        goal_row.pack(fill=tk.X, pady=2)
        tk.Label(goal_row, text="Goal:", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 10)).pack(side=tk.LEFT)

        self.goal_var = tk.IntVar(value=self.settings.get("daily_goal"))
        goal_options = [100, 250, 500, 1000, 2500, 5000, 10000]
        goal_combo = ttk.Combobox(goal_row, textvariable=self.goal_var,
                                  values=goal_options, width=8, state="readonly")
        goal_combo.pack(side=tk.LEFT, padx=(8, 0))
        goal_combo.bind("<<ComboboxSelected>>",
                         lambda e: self.settings.set("daily_goal", self.goal_var.get()))
        tk.Label(goal_row, text="flashes/day", bg=BG_CARD, fg=FG_DIM,
                 font=(FONT_FAMILY, 9)).pack(side=tk.LEFT, padx=(6, 0))

        # Progress bar (text-based for Tkinter)
        self._goal_progress_label = tk.Label(goal_section, text="", bg=BG_CARD,
                                             fg=GREEN, font=(FONT_MONO, 10, "bold"))
        self._goal_progress_label.pack(fill=tk.X, pady=(6, 2))
        self._goal_percent_label = tk.Label(goal_section, text="", bg=BG_CARD,
                                            fg=FG_DIM, font=(FONT_FAMILY, 9))
        self._goal_percent_label.pack(fill=tk.X)
        self._update_daily_goal_display()

        # ── Achievements ──
        ach_section = make_section(tab, "Achievements",
                                   "Unlock milestones as you build your practice.")
        self._achievements_frame = tk.Frame(ach_section, bg=BG_CARD)
        self._achievements_frame.pack(fill=tk.X)
        self._refresh_achievements_display()

        # ── Session History ──
        history_section = make_section(tab, "Recent Sessions",
                                       "Your last sessions at a glance.")
        self._history_frame = tk.Frame(history_section, bg=BG_CARD)
        self._history_frame.pack(fill=tk.X)
        self._refresh_history_display()

        # ── Quick actions ──
        quick_section = make_section(tab, "Quick Actions",
                                     "Common actions at your fingertips.")

        self.power_hour_var = tk.BooleanVar(value=self.settings.get("power_hour"))
        self.night_mode_var = tk.BooleanVar(value=self.settings.get("night_mode"))
        self.stealth_var = tk.BooleanVar(value=False)

        make_toggle(quick_section, "POWER HOUR  --  Rapid-fire intensity, faster flashing",
                    self.power_hour_var,
                    lambda: self.settings.set("power_hour", self.power_hour_var.get()),
                    RED, bold=True)
        make_toggle(quick_section, "Night Mode  --  Warm amber colors, easy on eyes while sleeping",
                    self.night_mode_var,
                    lambda: self.settings.set("night_mode", self.night_mode_var.get()),
                    GOLD)
        make_toggle(quick_section, "Stealth Mode  --  Hide this window, keep subliminals running",
                    self.stealth_var, self._toggle_stealth, PURPLE)

        # ── Breathing guide ──
        breath_section = make_section(tab, "Breathing Sync",
                                      "Sync flashes to your breath. Messages appear during exhale "
                                      "when your mind is most receptive.")

        combo_row = tk.Frame(breath_section, bg=BG_CARD)
        combo_row.pack(fill=tk.X, pady=4)
        tk.Label(combo_row, text="Pattern:", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 10)).pack(side=tk.LEFT)

        self.breathing_var = tk.StringVar(value=self.settings.get("breathing_pattern"))
        breath_combo = ttk.Combobox(combo_row, textvariable=self.breathing_var,
                                    values=list(BREATHING_PATTERNS.keys()),
                                    state="readonly", width=22)
        breath_combo.pack(side=tk.LEFT, padx=(8, 0))
        breath_combo.bind("<<ComboboxSelected>>",
                          lambda e: self.settings.set("breathing_pattern", self.breathing_var.get()))

        self.breath_indicator = tk.Label(breath_section, text="", bg=BG_CARD,
                                        fg=CYAN, font=(FONT_FAMILY, 11, "bold"))
        self.breath_indicator.pack(pady=4)

        # ── Hotkeys reference ──
        hotkey_section = make_section(tab, "Keyboard Shortcuts")
        shortcuts = [
            (f"{MOD_DISPLAY} + S", "Start / Stop flashing"),
            (f"{MOD_DISPLAY} + H", "Toggle Stealth Mode"),
            (f"{MOD_DISPLAY} + P", "Toggle Power Hour"),
        ]
        for key, desc in shortcuts:
            row = tk.Frame(hotkey_section, bg=BG_CARD)
            row.pack(fill=tk.X, pady=1)
            tk.Label(row, text=key, bg=BG_ACCENT, fg=GOLD,
                     font=(FONT_MONO, 9, "bold"), padx=8, pady=2).pack(side=tk.LEFT)
            tk.Label(row, text=desc, bg=BG_CARD, fg=FG_PRIMARY,
                     font=(FONT_FAMILY, 9), padx=8).pack(side=tk.LEFT)

    # ════════════════════════════════════════════════════════
    #   TAB 2 : MESSAGES
    # ════════════════════════════════════════════════════════

    def _build_messages_tab(self):
        _, tab = self._make_scrollable_tab("Messages")

        # ── Message Editor ──
        editor_section = make_section(tab, "Message Editor",
                                      "Add, edit, or remove affirmations. These are the "
                                      "messages that flash on your screen.")

        # Quick-add bar
        add_bar = tk.Frame(editor_section, bg=BG_CARD)
        add_bar.pack(fill=tk.X, pady=(0, 6))
        self.new_msg_entry = tk.Entry(
            add_bar, bg=BG_INPUT, fg=FG_BRIGHT, insertbackground=FG_BRIGHT,
            font=(FONT_FAMILY, 10), relief="flat", bd=6)
        self.new_msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        self.new_msg_entry.insert(0, "Type your affirmation here...")
        self.new_msg_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.new_msg_entry.bind("<FocusOut>", self._on_entry_focus_out)
        self.new_msg_entry.bind("<Return>", lambda e: self._add_message())
        ttk.Button(add_bar, text="+ Add", command=self._add_message,
                   style="Accent.TButton").pack(side=tk.RIGHT)

        # Search bar
        search_bar = tk.Frame(editor_section, bg=BG_CARD)
        search_bar.pack(fill=tk.X, pady=(0, 4))
        tk.Label(search_bar, text="Search:", bg=BG_CARD, fg=FG_DIM,
                 font=(FONT_FAMILY, 9)).pack(side=tk.LEFT)
        self._search_var = tk.StringVar()
        search_entry = tk.Entry(search_bar, textvariable=self._search_var,
                                bg=BG_INPUT, fg=FG_BRIGHT, insertbackground=FG_BRIGHT,
                                font=(FONT_FAMILY, 9), relief="flat", bd=4)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 4))
        self._search_var.trace_add("write", lambda *_: self._refresh_msg_listbox())
        tk.Label(search_bar, text="", bg=BG_CARD, fg=FG_DIM,
                 font=(FONT_FAMILY, 8)).pack(side=tk.RIGHT)

        # Listbox
        list_container = tk.Frame(editor_section, bg=BG_DARK)
        list_container.pack(fill=tk.BOTH, expand=True, pady=4)
        list_scroll = tk.Scrollbar(list_container)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_listbox = tk.Listbox(
            list_container, bg=BG_DARK, fg=FG_PRIMARY, selectbackground=PURPLE,
            selectforeground=FG_BRIGHT, font=(FONT_FAMILY, 9), height=10,
            relief="flat", bd=2, highlightthickness=1, highlightcolor=PURPLE,
            yscrollcommand=list_scroll.set, activestyle="none")
        self.msg_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scroll.config(command=self.msg_listbox.yview)

        self.msg_count_label = tk.Label(editor_section, bg=BG_CARD, fg=FG_DIM,
                                        font=(FONT_FAMILY, 9), text="0 messages",
                                        anchor="w")
        self.msg_count_label.pack(fill=tk.X, pady=(2, 4))

        # Action buttons row 1
        btn_row1 = tk.Frame(editor_section, bg=BG_CARD)
        btn_row1.pack(fill=tk.X, pady=2)
        ttk.Button(btn_row1, text="Edit Selected",
                   command=self._edit_message).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(btn_row1, text="Delete Selected",
                   command=self._delete_message,
                   style="Danger.TButton").pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(btn_row1, text="Clear All",
                   command=self._clear_all_messages,
                   style="Danger.TButton").pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        # Action buttons row 2
        btn_row2 = tk.Frame(editor_section, bg=BG_CARD)
        btn_row2.pack(fill=tk.X, pady=2)
        ttk.Button(btn_row2, text="Save to File",
                   command=self._save_messages_to_file,
                   style="Accent.TButton").pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(btn_row2, text="Import .txt",
                   command=self._import_messages).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(btn_row2, text="Load Defaults",
                   command=self._load_default_messages).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(btn_row2, text="Apply to Flasher",
                   command=self._apply_messages,
                   style="Start.TButton").pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        self._refresh_msg_listbox()

        # ── Category Toggles ──
        cat_section = make_section(tab, "Message Categories",
                                   "Enable or disable entire categories. "
                                   "Reload after changing to update the message pool.")
        self.cat_vars = {}
        cats = self.settings.get("categories_enabled") or {}
        for cat_key, enabled in cats.items():
            var = tk.BooleanVar(value=enabled)
            self.cat_vars[cat_key] = var
            make_toggle(cat_section, cat_key.capitalize(), var,
                        lambda: self._save_categories(), CYAN)

        ttk.Button(cat_section, text="Reload Messages",
                   command=self._reload_messages,
                   style="Accent.TButton").pack(pady=(6, 0))

        # ── Preset Packs ──
        preset_section = make_section(tab, "Quick-Load Preset Packs",
                                      "Instantly add themed affirmation bundles to your message pool.")
        preset_grid = tk.Frame(preset_section, bg=BG_CARD)
        preset_grid.pack(fill=tk.X)
        preset_grid.columnconfigure(0, weight=1)
        preset_grid.columnconfigure(1, weight=1)
        for i, pack_name in enumerate(MESSAGE_PRESETS.keys()):
            btn = ttk.Button(preset_grid, text=pack_name,
                             command=lambda n=pack_name: self._load_preset(n))
            btn.grid(row=i // 2, column=i % 2, padx=3, pady=3, sticky="ew")

    # ════════════════════════════════════════════════════════
    #   TAB 3 : EFFECTS & IMAGES
    # ════════════════════════════════════════════════════════

    def _build_effects_tab(self):
        _, tab = self._make_scrollable_tab("Effects")

        # ── Flash Effect ──
        fx_section = make_section(tab, "Flash Effect",
                                  "How the message appears on screen.")

        combo_row = tk.Frame(fx_section, bg=BG_CARD)
        combo_row.pack(fill=tk.X, pady=4)
        tk.Label(combo_row, text="Animation:", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 10)).pack(side=tk.LEFT)
        self.effect_var = tk.StringVar(value=self.settings.get("flash_effect"))
        effect_combo = ttk.Combobox(combo_row, textvariable=self.effect_var,
                                    values=FLASH_EFFECTS, state="readonly", width=18)
        effect_combo.pack(side=tk.LEFT, padx=(8, 0))
        effect_combo.bind("<<ComboboxSelected>>",
                          lambda e: self.settings.set("flash_effect", self.effect_var.get()))

        effect_hints = {
            "Instant": "Message appears and disappears instantly (most subliminal).",
            "Fade In": "Message fades in smoothly, then fades out.",
            "Glow Pulse": "Message pulses with a glowing sine-wave effect.",
            "Typewriter": "Letters appear one by one like typing.",
            "Slide In": "Message slides in from the edge of the screen.",
            "Matrix Rain": "Characters scramble and decode like the Matrix.",
            "Spiral Emerge": "Message spirals in from a circular orbit.",
            "Random": "Surprise! A different effect every flash for variety.",
        }
        self.effect_hint_label = tk.Label(fx_section, text="", bg=BG_CARD,
                                          fg=FG_DIM, font=(FONT_FAMILY, 8),
                                          wraplength=400, anchor="w")
        self.effect_hint_label.pack(fill=tk.X, pady=(0, 4))

        def update_hint(*_):
            self.effect_hint_label.config(
                text=effect_hints.get(self.effect_var.get(), ""))
        self.effect_var.trace_add("write", update_hint)
        update_hint()

        # ── Focus Zone ──
        zone_row = tk.Frame(fx_section, bg=BG_CARD)
        zone_row.pack(fill=tk.X, pady=4)
        tk.Label(zone_row, text="Focus Zone:", bg=BG_CARD, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 10)).pack(side=tk.LEFT)
        self.zone_var = tk.StringVar(value=self.settings.get("focus_zone"))
        zone_combo = ttk.Combobox(zone_row, textvariable=self.zone_var,
                                  values=FOCUS_ZONES, state="readonly", width=18)
        zone_combo.pack(side=tk.LEFT, padx=(8, 0))
        zone_combo.bind("<<ComboboxSelected>>",
                        lambda e: self.settings.set("focus_zone", self.zone_var.get()))

        tk.Label(fx_section, text="Where on screen messages will appear. "
                 "'Full Screen' = random positions everywhere.",
                 bg=BG_CARD, fg=FG_DIM, font=(FONT_FAMILY, 8),
                 wraplength=400, anchor="w").pack(fill=tk.X, pady=(0, 4))

        # ── Color modes ──
        self.rainbow_var = tk.BooleanVar(value=self.settings.get("rainbow_mode"))
        make_toggle(fx_section, "Rainbow Neon Mode  --  Random vibrant colors each flash",
                    self.rainbow_var,
                    lambda: self.settings.set("rainbow_mode", self.rainbow_var.get()),
                    PINK, bold=True)

        self.mirror_var = tk.BooleanVar(value=self.settings.get("mirror_mode"))
        make_toggle(fx_section, "Mirror Mode  --  Reversed text (subconscious reads both ways)",
                    self.mirror_var,
                    lambda: self.settings.set("mirror_mode", self.mirror_var.get()),
                    CYAN)

        # ── Color Theme ──
        theme_section = make_section(tab, "Ambient Color Theme",
                                     "Choose a color palette for your flash messages. "
                                     "Enable Rainbow Mode above to see themed colors.")

        self.theme_var = tk.StringVar(value=self.settings.get("color_theme"))
        theme_grid = tk.Frame(theme_section, bg=BG_CARD)
        theme_grid.pack(fill=tk.X, pady=4)

        self._theme_buttons = {}
        for i, theme_name in enumerate(COLOR_THEMES.keys()):
            theme_data = COLOR_THEMES[theme_name]
            preview_colors = theme_data["colors"][:5]
            btn_frame = tk.Frame(theme_grid, bg=BG_CARD)
            btn_frame.grid(row=i // 2, column=i % 2, padx=4, pady=3, sticky="ew")
            theme_grid.columnconfigure(i % 2, weight=1)

            # Color preview strip
            strip = tk.Frame(btn_frame, bg=BG_CARD, height=4)
            strip.pack(fill=tk.X)
            for j, c in enumerate(preview_colors):
                swatch = tk.Frame(strip, bg=c, width=20, height=4)
                swatch.pack(side=tk.LEFT, expand=True, fill=tk.X)

            btn = tk.Label(btn_frame, text=theme_name, bg=BG_ACCENT, fg=FG_PRIMARY,
                           font=(FONT_FAMILY, 9, "bold"), padx=8, pady=4,
                           cursor="hand2", anchor="center")
            btn.pack(fill=tk.X)
            btn.bind("<Button-1>", lambda e, n=theme_name: self._select_theme(n))
            self._theme_buttons[theme_name] = btn

        self._highlight_active_theme()

        # ── Appearance ──
        appearance_section = make_section(tab, "Text Appearance",
                                          "Control how the flashed text looks on screen.")
        make_labeled_slider(appearance_section, "Font Size",
                            "Bigger = more visible, smaller = more subliminal.",
                            "font_size", 10, 100, True, self.settings)

        ttk.Button(appearance_section, text="Choose Text Color",
                   command=self._change_text_color,
                   style="Accent.TButton").pack(fill=tk.X, pady=4)

        # ── Image Gallery ──
        image_section = make_section(tab, "Vision Board Images",
                                     "Add images to flash alongside text. Great for "
                                     "goals, vision boards, or loved ones.")

        img_btn_row = tk.Frame(image_section, bg=BG_CARD)
        img_btn_row.pack(fill=tk.X, pady=4)
        ttk.Button(img_btn_row, text="+ Add Image(s)", command=self._add_images,
                   style="Accent.TButton").pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(img_btn_row, text="Clear All Images", command=self._clear_all_images,
                   style="Danger.TButton").pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        self.gallery_count_label = tk.Label(image_section, text="No images",
                                            bg=BG_CARD, fg=FG_DIM,
                                            font=(FONT_FAMILY, 9))
        self.gallery_count_label.pack(pady=(4, 2))

        # Scrollable gallery with individual delete buttons per image
        gallery_outer = tk.Frame(image_section, bg=BG_DARK)
        gallery_outer.pack(fill=tk.X, pady=4)
        self.gallery_canvas = tk.Canvas(gallery_outer, bg=BG_DARK,
                                        highlightthickness=0, height=90)
        gallery_xscroll = ttk.Scrollbar(gallery_outer, orient="horizontal",
                                        command=self.gallery_canvas.xview)
        self.gallery_canvas.configure(xscrollcommand=gallery_xscroll.set)
        self.gallery_canvas.pack(fill=tk.X)
        gallery_xscroll.pack(fill=tk.X)
        self.gallery_frame = tk.Frame(self.gallery_canvas, bg=BG_DARK)
        self._gallery_cw = self.gallery_canvas.create_window(
            (0, 0), window=self.gallery_frame, anchor="nw")
        self.gallery_frame.bind("<Configure>",
            lambda e: self.gallery_canvas.configure(
                scrollregion=self.gallery_canvas.bbox("all")))

        make_labeled_slider(image_section, "Image Size", "Thumbnail size in pixels.",
                            "image_size", 40, 300, True, self.settings)

        self.flash_image_only_var = tk.BooleanVar(value=self.settings.get("flash_image_only"))
        make_toggle(image_section, "Flash images only (hide text)",
                    self.flash_image_only_var,
                    lambda: self.settings.set("flash_image_only", self.flash_image_only_var.get()),
                    FG_PRIMARY)

        self._update_gallery()

    # ════════════════════════════════════════════════════════
    #   TAB 4 : SETTINGS
    # ════════════════════════════════════════════════════════

    def _build_settings_tab(self):
        _, tab = self._make_scrollable_tab("Settings")

        # ── Timing & Behavior ──
        timing_section = make_section(tab, "Timing & Behavior",
                                      "Control how fast and how many messages flash at once.")

        make_labeled_slider(timing_section, "Batch Size",
                            "How many messages flash at the same time (1-5).",
                            "batch_size", 1, 5, True, self.settings)

        make_labeled_slider(timing_section, "Flash Duration (ms)",
                            "How long each message stays visible. 100-200ms = readable, 5-50ms = subliminal.",
                            "flash_duration_ms", 5, 500, True, self.settings)

        make_labeled_slider(timing_section, "Interval (seconds)",
                            "Time between flash batches. Lower = more frequent (0.1-5s).",
                            "interval_seconds", 0.1, 5, False, self.settings)

        make_labeled_slider(timing_section, "Edge Margin (px)",
                            "Keep messages this far from screen edges (0-50px).",
                            "margin_px", 0, 50, True, self.settings)

        # ── Auto-Stop Timer ──
        timer_section = make_section(tab, "Auto-Stop Timer",
                                     "Automatically stop flashing after a set time. "
                                     "Great for sleep sessions. Set to 0 to disable.")

        make_labeled_slider(timer_section, "Stop After (minutes)",
                            "0 = run indefinitely until you press Stop.",
                            "auto_stop_minutes", 0, 120, True, self.settings)

        # ── Test Mode ──
        test_section = make_section(tab, "Test Mode",
                                    "Make messages clearly visible so you can verify "
                                    "everything works. Turn this OFF for actual subliminal use.")

        self.test_mode_var = tk.BooleanVar(value=self.settings.get("test_mode"))
        make_toggle(test_section, "Enable Test Mode (messages stay visible longer)",
                    self.test_mode_var, self._toggle_test_mode, ORANGE, bold=True)

        make_labeled_slider(test_section, "Display Time (seconds)",
                            "How long test messages stay visible (0.2-10s).",
                            "test_display_seconds", 0.2, 10, False, self.settings)

        # ── Auto-Start ──
        auto_section = make_section(tab, "Auto-Start",
                                    "Start flashing automatically when the app opens. "
                                    "Combine with 'Run on Startup' to flash every time you turn on your computer.")

        self.auto_start_var = tk.BooleanVar(value=self.settings.get("auto_start"))
        make_toggle(auto_section, "Auto-start flashing when app opens",
                    self.auto_start_var,
                    lambda: self.settings.set("auto_start", self.auto_start_var.get()),
                    GREEN, bold=True)

        self.run_on_startup_var = tk.BooleanVar(value=is_registered_at_startup())
        make_toggle(auto_section, "Run Subliminal Master when I log in to my computer",
                    self.run_on_startup_var,
                    self._toggle_run_on_startup, GOLD)

        # ── About ──
        about_section = make_section(tab, "About")
        tk.Label(about_section, text="MindFlash v5.0",
                 bg=BG_CARD, fg=GOLD, font=(FONT_FAMILY, 12, "bold")).pack()
        tk.Label(about_section, text="by Emmanuel Hagan  |  Free & Open Source",
                 bg=BG_CARD, fg=FG_DIM, font=(FONT_FAMILY, 9)).pack()
        tk.Label(about_section,
                 text="Flash affirmations on your screen below conscious perception.\n"
                      "Your subconscious absorbs the messages while you work, study, or sleep.\n"
                      "Works on Windows and macOS.",
                 bg=BG_CARD, fg=FG_DIM, font=(FONT_FAMILY, 9),
                 wraplength=400, justify=tk.CENTER).pack(pady=(6, 0))

        # LinkedIn link
        linkedin_label = tk.Label(
            about_section,
            text="linkedin.com/in/emmanuel-hagan",
            bg=BG_CARD, fg=CYAN, font=(FONT_FAMILY, 9, "underline"),
            cursor="hand2")
        linkedin_label.pack(pady=(6, 0))
        linkedin_label.bind("<Button-1>", lambda e: __import__("webbrowser").open(
            "https://www.linkedin.com/in/emmanuel-hagan/"))

    # ════════════════════════════════════════════════════════
    #   LIVE UPDATES
    # ════════════════════════════════════════════════════════

    def _animate_title(self):
        colors = [GOLD, "#FFF176", "#FFEE58", "#FFD740", "#FFC107", "#FFB300",
                  CYAN, "#64FFDA", PURPLE, "#EA80FC", "#FF80AB", GOLD]
        self._title_step = 0

        def cycle():
            if hasattr(self, "title_label"):
                c = colors[self._title_step % len(colors)]
                self.title_label.configure(fg=c)
                self._title_step += 1
            self.after(350, cycle)
        cycle()

    def _update_status_loop(self):
        if self.flasher.is_running:
            count = self.flasher.flash_count
            pool = len(self.flasher.message_pool)
            imgs = len(self.flasher.image_paths)
            parts = [f"{count} flashed", f"{pool} msgs"]
            if imgs:
                parts.append(f"{imgs} imgs")
            self.status_label.config(
                text="RUNNING  |  " + "  |  ".join(parts), fg=GREEN)
            # Pulse the dot
            pulse_alpha = int(127 + 128 * math.sin(time.time() * 4))
            pulse_hex = f"#{pulse_alpha:02x}ff{pulse_alpha:02x}"
            try:
                self._pulse_dot.config(fg=pulse_hex, text=" * ")
            except tk.TclError:
                pass
            if self.flasher.session_start:
                elapsed = int(time.time() - self.flasher.session_start)
                h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
                auto_stop = self.settings.get("auto_stop_minutes")
                timer_text = f"Session: {h:02d}:{m:02d}:{s:02d}"
                if auto_stop and auto_stop > 0:
                    remaining = max(0, int(auto_stop * 60) - elapsed)
                    rm, rs = (remaining % 3600) // 60, remaining % 60
                    timer_text += f"  |  Auto-stop in {rm:02d}:{rs:02d}"
                self.timer_label.config(text=timer_text, fg=CYAN)
        else:
            pool = len(self.flasher.message_pool)
            self.status_label.config(text=f"Stopped  |  {pool} messages ready",
                                     fg=FG_DIM)
            self.timer_label.config(text="", fg=FG_DIM)
            self._pulse_dot.config(fg=BG_DARK, text="  ")
        self.after(500, self._update_status_loop)

    def _update_stats_display(self):
        streak = self.settings.get("streak_days")
        total = self.settings.get("total_flashes")
        sessions = self.settings.get("session_count")

        streak_text = str(streak)
        if streak >= 7:
            streak_text += " ON FIRE!"

        if hasattr(self, "_streak_val"):
            self._streak_val.config(text=streak_text)
            self._total_val.config(text=f"{total:,}")
            self._sessions_val.config(text=str(sessions))

    def _update_daily_goal_display(self):
        if not hasattr(self, "_goal_progress_label"):
            return
        daily = self._get_daily_flashes()
        goal = self.settings.get("daily_goal") or 500
        percent = min(daily / max(goal, 1) * 100, 100)
        bar_len = 30
        filled = int(percent / 100 * bar_len)
        bar = "=" * filled + "-" * (bar_len - filled)

        if percent >= 100:
            color = GOLD
            status = "GOAL REACHED!"
        elif percent >= 50:
            color = GREEN
            status = f"{daily:,} / {goal:,} flashes"
        else:
            color = CYAN
            status = f"{daily:,} / {goal:,} flashes"

        self._goal_progress_label.config(text=f"[{bar}]", fg=color)
        self._goal_percent_label.config(text=f"{percent:.0f}%  --  {status}")

    def _refresh_achievements_display(self):
        for w in self._achievements_frame.winfo_children():
            w.destroy()
        unlocked = set(self.settings.get("achievements_unlocked") or [])

        icons = {"ZAP": "//", "STAR": "**", "FIRE": "^^", "CROWN": "##",
                 "FLAME": "~~", "TROPHY": "@@", "CHECK": "++",
                 "DIAMOND": "<>", "ROCKET": ">>"}

        grid = self._achievements_frame
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)

        for i, (key, ach) in enumerate(ACHIEVEMENTS.items()):
            is_unlocked = key in unlocked
            fg = GOLD if is_unlocked else FG_DIM
            bg_c = BG_ACCENT if is_unlocked else BG_DARK
            icon = icons.get(ach["icon"], "--")

            cell = tk.Frame(grid, bg=bg_c, padx=6, pady=4,
                            highlightbackground=GOLD if is_unlocked else BG_ACCENT,
                            highlightthickness=1)
            cell.grid(row=i // 3, column=i % 3, padx=3, pady=3, sticky="nsew")

            tk.Label(cell, text=f"[{icon}]", bg=bg_c, fg=fg,
                     font=(FONT_MONO, 9, "bold")).pack()
            tk.Label(cell, text=ach["title"], bg=bg_c, fg=fg,
                     font=(FONT_FAMILY, 8, "bold")).pack()
            if is_unlocked:
                tk.Label(cell, text=ach["desc"], bg=bg_c, fg=FG_DIM,
                         font=(FONT_FAMILY, 7), wraplength=120).pack()

    def _refresh_history_display(self):
        for w in self._history_frame.winfo_children():
            w.destroy()
        history = list(self.settings.get("session_history") or [])
        if not history:
            tk.Label(self._history_frame, text="No sessions yet. Hit START!",
                     bg=BG_CARD, fg=FG_DIM, font=(FONT_FAMILY, 9)).pack()
            return

        # Show last 7 sessions, newest first
        for entry in reversed(history[-7:]):
            row = tk.Frame(self._history_frame, bg=BG_CARD)
            row.pack(fill=tk.X, pady=1)

            date_str = entry.get("date", "")
            flashes = entry.get("flashes", 0)
            duration = entry.get("duration", 0)
            mins = duration // 60
            secs = duration % 60

            tk.Label(row, text=date_str, bg=BG_CARD, fg=FG_DIM,
                     font=(FONT_MONO, 8), width=16, anchor="w").pack(side=tk.LEFT)
            tk.Label(row, text=f"{flashes:,} flashes", bg=BG_CARD, fg=CYAN,
                     font=(FONT_FAMILY, 9, "bold"), anchor="w").pack(side=tk.LEFT, padx=(8, 0))
            tk.Label(row, text=f"{mins}m {secs}s", bg=BG_CARD, fg=FG_DIM,
                     font=(FONT_FAMILY, 8), anchor="e").pack(side=tk.RIGHT)

    def _update_breathing_indicator(self):
        if not hasattr(self, "breath_indicator"):
            self.after(500, self._update_breathing_indicator)
            return
        pattern_name = self.settings.get("breathing_pattern")
        pattern = BREATHING_PATTERNS.get(pattern_name)
        if not pattern or not self.flasher.is_running or not self.flasher.session_start:
            self.breath_indicator.config(text="")
            self.after(300, self._update_breathing_indicator)
            return
        inhale, hold, exhale = pattern
        cycle_len = inhale + hold + exhale
        elapsed = (time.time() - self.flasher.session_start) % cycle_len
        if elapsed < inhale:
            phase, progress, color = "BREATHE IN...", elapsed / inhale, "#00E676"
        elif elapsed < inhale + hold:
            phase, progress, color = "HOLD...", (elapsed - inhale) / hold, GOLD
        else:
            phase = "BREATHE OUT... (flashing)"
            progress = (elapsed - inhale - hold) / exhale
            color = CYAN
        bar_len = 20
        filled = int(progress * bar_len)
        bar = "=" * filled + "-" * (bar_len - filled)
        self.breath_indicator.config(text=f"{phase}  [{bar}]", fg=color)
        self.after(100, self._update_breathing_indicator)

    # ════════════════════════════════════════════════════════
    #   IMAGE GALLERY
    # ════════════════════════════════════════════════════════

    def _update_gallery(self):
        for widget in self.gallery_frame.winfo_children():
            widget.destroy()
        self._preview_photos = []

        paths = self.flasher.image_paths
        if not paths:
            self.gallery_count_label.config(text="No images -- add your vision board!")
            self.gallery_canvas.config(height=30)
            return

        self.gallery_count_label.config(
            text=f"{len(paths)} image{'s' if len(paths) != 1 else ''} in rotation")
        self.gallery_canvas.config(height=90)

        for i, path in enumerate(paths):
            # Card for each image: thumbnail + filename + delete button
            card = tk.Frame(self.gallery_frame, bg=BG_ACCENT, padx=4, pady=4)
            card.grid(row=0, column=i, padx=3, pady=3)

            try:
                if HAS_PIL:
                    img = Image.open(path)
                    img.thumbnail((55, 55), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self._preview_photos.append(photo)
                    tk.Label(card, image=photo, bg=BG_ACCENT).pack()
                else:
                    fname = os.path.basename(path)
                    tk.Label(card, text=fname[:12], bg=BG_ACCENT, fg=FG_PRIMARY,
                             font=(FONT_FAMILY, 7)).pack()
            except Exception:
                fname = os.path.basename(path)
                tk.Label(card, text=fname[:12], bg=BG_ACCENT, fg=FG_DIM,
                         font=(FONT_FAMILY, 7)).pack()

            # Per-image delete button
            del_btn = tk.Label(card, text="X", bg=RED, fg="#FFFFFF",
                               font=(FONT_FAMILY, 7, "bold"), cursor="hand2",
                               padx=4, pady=0)
            del_btn.pack(pady=(2, 0))
            del_btn.bind("<Button-1>", lambda e, p=path: self._remove_image(p))

    def _remove_image(self, path):
        self.flasher.remove_image(path)
        self._update_gallery()

    # ════════════════════════════════════════════════════════
    #   MESSAGE EDITOR
    # ════════════════════════════════════════════════════════

    def _on_entry_focus_in(self, event):
        if self.new_msg_entry.get() == "Type your affirmation here...":
            self.new_msg_entry.delete(0, tk.END)
            self.new_msg_entry.config(fg=FG_BRIGHT)

    def _on_entry_focus_out(self, event):
        if not self.new_msg_entry.get().strip():
            self.new_msg_entry.delete(0, tk.END)
            self.new_msg_entry.insert(0, "Type your affirmation here...")
            self.new_msg_entry.config(fg=FG_DIM)

    def _refresh_msg_listbox(self):
        self.msg_listbox.delete(0, tk.END)
        seen = set()
        unique = []
        for m in self.flasher.message_pool:
            if m not in seen:
                seen.add(m)
                unique.append(m)

        # Apply search filter
        search_term = ""
        if hasattr(self, "_search_var"):
            search_term = self._search_var.get().strip().lower()

        filtered = [m for m in unique if search_term in m.lower()] if search_term else unique
        for msg in filtered:
            self.msg_listbox.insert(tk.END, msg)

        if search_term:
            self.msg_count_label.config(
                text=f"{len(filtered)} of {len(unique)} messages match '{search_term}'")
        else:
            self.msg_count_label.config(
                text=f"{len(unique)} unique messages ({len(self.flasher.message_pool)} weighted)")

    def _add_message(self):
        text = self.new_msg_entry.get().strip()
        if not text or text == "Type your affirmation here...":
            return
        # Sanitize: limit length
        msg = self.flasher._sanitize_message(text)
        if not msg:
            return
        self.flasher.message_pool.append(msg)
        self.flasher.current_messages.append(msg)
        self.new_msg_entry.delete(0, tk.END)
        self._refresh_msg_listbox()
        self.msg_listbox.see(tk.END)

    def _edit_message(self):
        sel = self.msg_listbox.curselection()
        if not sel:
            return
        old_text = self.msg_listbox.get(sel[0])

        dialog = tk.Toplevel(self)
        dialog.title("Edit Message")
        dialog.geometry("500x150")
        dialog.configure(bg=BG_DARK)
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(dialog, text="Edit your affirmation:", bg=BG_DARK, fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 11)).pack(pady=(15, 5))

        entry = tk.Entry(dialog, bg=BG_INPUT, fg=FG_BRIGHT,
                         insertbackground=FG_BRIGHT,
                         font=(FONT_FAMILY, 11), relief="flat", bd=6, width=60)
        entry.pack(padx=20, fill=tk.X)
        entry.insert(0, old_text)
        entry.select_range(0, tk.END)
        entry.focus_set()

        def save_edit():
            new_text = entry.get().strip()
            if new_text and new_text != old_text:
                self.flasher.message_pool = [
                    new_text if m == old_text else m
                    for m in self.flasher.message_pool]
                self.flasher.current_messages = [
                    new_text if m == old_text else m
                    for m in self.flasher.current_messages]
                self._refresh_msg_listbox()
            dialog.destroy()

        entry.bind("<Return>", lambda e: save_edit())

        btn_frame = tk.Frame(dialog, bg=BG_DARK)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Save", command=save_edit,
                   style="Start.TButton").pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text="Cancel",
                   command=dialog.destroy).pack(side=tk.LEFT, padx=6)

    def _delete_message(self):
        sel = self.msg_listbox.curselection()
        if not sel:
            return
        text = self.msg_listbox.get(sel[0])
        self.flasher.message_pool = [m for m in self.flasher.message_pool if m != text]
        self.flasher.current_messages = [m for m in self.flasher.current_messages if m != text]
        self._refresh_msg_listbox()

    def _clear_all_messages(self):
        if messagebox.askyesno("Clear All",
                               "Remove all messages? You can reload defaults after."):
            self.flasher.message_pool.clear()
            self.flasher.current_messages.clear()
            self._refresh_msg_listbox()

    def _save_messages_to_file(self):
        filepath = filedialog.asksaveasfilename(
            title="Save Messages", defaultextension=".txt",
            initialfile="messages_custom.txt",
            filetypes=(("Text files", "*.txt"),))
        if filepath:
            seen = set()
            unique = []
            for m in self.flasher.message_pool:
                if m not in seen:
                    seen.add(m)
                    unique.append(m)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(unique))
            messagebox.showinfo("Saved",
                                f"Saved {len(unique)} messages to:\n{os.path.basename(filepath)}")

    def _load_default_messages(self):
        self.flasher.message_pool = AWESOME_MESSAGES.copy()
        self.flasher._shuffle_pool()
        self._refresh_msg_listbox()

    def _apply_messages(self):
        if not self.flasher.message_pool:
            messagebox.showwarning("No Messages", "Add some messages first!")
            return
        self.flasher._shuffle_pool()
        self._refresh_msg_listbox()
        messagebox.showinfo("Applied",
                            f"{len(self.flasher.message_pool)} messages ready to flash!")

    def _load_preset(self, pack_name):
        messages = MESSAGE_PRESETS.get(pack_name, [])
        if messages:
            self.flasher.message_pool.extend(messages)
            self.flasher._shuffle_pool()
            self._refresh_msg_listbox()
            messagebox.showinfo("Loaded",
                                f"Added '{pack_name}' pack ({len(messages)} affirmations)!")

    def _save_categories(self):
        cats = {k: v.get() for k, v in self.cat_vars.items()}
        self.settings.set("categories_enabled", cats)

    def _reload_messages(self):
        self._save_categories()
        self.flasher._load_messages()
        self.flasher._shuffle_pool()
        self._refresh_msg_listbox()

    # ════════════════════════════════════════════════════════
    #   ACTIONS
    # ════════════════════════════════════════════════════════

    def toggle_flasher(self):
        if self.flasher.is_running:
            # Record session before stopping
            flash_count = self.flasher.flash_count
            duration = time.time() - self.flasher.session_start if self.flasher.session_start else 0
            self.flasher.stop()
            self._add_daily_flashes(flash_count)
            self._record_session(flash_count, duration)
            self.start_stop_button.config(text="START FLASHING",
                                          style="Start.TButton")
            self.title("MindFlash")
            self._update_stats_display()
            self._update_daily_goal_display()
            self._check_achievements()
            if hasattr(self, "_history_frame"):
                self._refresh_history_display()
        else:
            self.flasher.start()
            self.start_stop_button.config(text="STOP", style="Stop.TButton")
            mode = " - TEST MODE" if self.settings.get("test_mode") else ""
            self.title(f"MindFlash{mode}")

    def _on_auto_stopped(self):
        self._add_daily_flashes(self.flasher.flash_count)
        duration = time.time() - self.flasher.session_start if self.flasher.session_start else 0
        self._record_session(self.flasher.flash_count, duration)
        self.start_stop_button.config(text="START FLASHING",
                                       style="Start.TButton")
        self.title("MindFlash")
        self._update_stats_display()
        self._update_daily_goal_display()
        self._check_achievements()
        self.timer_label.config(text="Auto-stopped! Great session.", fg=GOLD)

    def _toggle_test_mode(self):
        test_mode = self.test_mode_var.get()
        self.settings.set("test_mode", test_mode)
        if test_mode:
            self.title("MindFlash - TEST MODE")
        else:
            self.title("MindFlash")

    def _toggle_run_on_startup(self):
        if self.run_on_startup_var.get():
            ok = register_at_startup()
            if ok:
                self.settings.set("run_on_startup", True)
                messagebox.showinfo("Startup Enabled",
                                    "MindFlash will now start automatically "
                                    "when you log in to your computer.")
            else:
                self.run_on_startup_var.set(False)
                messagebox.showerror("Error", "Could not register startup. Try running as administrator.")
        else:
            unregister_at_startup()
            self.settings.set("run_on_startup", False)

    def _toggle_stealth(self):
        if self.stealth_var.get():
            self.withdraw()
            if not self.flasher.is_running:
                self.flasher.start()
        else:
            self.deiconify()
            self.lift()

    def _add_images(self):
        filepaths = filedialog.askopenfilenames(
            title="Select Images for Subliminal Flashing",
            filetypes=(
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),))
        for fp in filepaths:
            self.flasher.add_image(fp)
        if filepaths:
            self._update_gallery()

    def _clear_all_images(self):
        self.flasher.clear_all_images()
        self._update_gallery()

    def _import_messages(self):
        filepath = filedialog.askopenfilename(
            title="Import Message File",
            filetypes=(("Text files", "*.txt"),))
        if filepath:
            try:
                # Validate file size (5 MB limit)
                file_size = os.path.getsize(filepath)
                if file_size > 5_242_880:
                    messagebox.showerror("Error", "File is too large (max 5 MB).")
                    return
                msgs = self.flasher._safe_read_message_file(filepath)
                if msgs:
                    self.flasher.message_pool.extend(msgs)
                    self.flasher._shuffle_pool()
                    self._refresh_msg_listbox()
                    messagebox.showinfo(
                        "Imported",
                        f"Added {len(msgs)} messages from:\n"
                        f"{os.path.basename(filepath)}")
                else:
                    messagebox.showwarning("Empty", "No valid messages found in file.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not import file:\n{e}")

    def _select_theme(self, theme_name):
        self.theme_var.set(theme_name)
        self.settings.set("color_theme", theme_name)
        self._highlight_active_theme()

    def _highlight_active_theme(self):
        active = self.theme_var.get()
        for name, btn in self._theme_buttons.items():
            if name == active:
                theme = COLOR_THEMES[name]
                btn.config(bg=theme["colors"][0], fg="#000000")
            else:
                btn.config(bg=BG_ACCENT, fg=FG_PRIMARY)

    def _change_text_color(self):
        color_code = colorchooser.askcolor(title="Choose text color")
        if color_code and color_code[1]:
            self.settings.set("font_color", color_code[1])

    # ════════════════════════════════════════════════════════
    #   HOTKEYS
    # ════════════════════════════════════════════════════════

    def _bind_hotkeys(self):
        self.bind_all(f"<{MOD_KEY}-s>", lambda e: self.toggle_flasher())
        self.bind_all(f"<{MOD_KEY}-h>", lambda e: self._hotkey_stealth())
        self.bind_all(f"<{MOD_KEY}-p>", lambda e: self._hotkey_power_hour())

    def _hotkey_stealth(self):
        self.stealth_var.set(not self.stealth_var.get())
        self._toggle_stealth()

    def _hotkey_power_hour(self):
        new_val = not self.power_hour_var.get()
        self.power_hour_var.set(new_val)
        self.settings.set("power_hour", new_val)

    def _on_ready(self):
        """Called ~200ms after launch. Pre-pool windows and auto-start if enabled."""
        self.flasher.prepool_windows()
        if self.settings.get("auto_start"):
            self.toggle_flasher()

    # ════════════════════════════════════════════════════════
    #   ACHIEVEMENTS & TOAST NOTIFICATIONS
    # ════════════════════════════════════════════════════════

    def _check_achievements(self):
        """Check if any new achievements have been unlocked."""
        unlocked = set(self.settings.get("achievements_unlocked") or [])
        stats = {
            "session_count": self.settings.get("session_count"),
            "total_flashes": self.settings.get("total_flashes"),
            "streak_days": self.settings.get("streak_days"),
        }
        new_achievements = []
        for key, ach in ACHIEVEMENTS.items():
            if key not in unlocked and ach["condition"](stats):
                new_achievements.append(ach)
                unlocked.add(key)
        if new_achievements:
            self.settings.set("achievements_unlocked", list(unlocked))
            for ach in new_achievements:
                self._show_toast(
                    f"Achievement Unlocked!",
                    f"{ach['title']}\n{ach['desc']}",
                    GOLD)
        # Update dashboard achievements display
        if hasattr(self, "_achievements_frame"):
            self._refresh_achievements_display()

    def _show_toast(self, title, message, color=GOLD):
        """Show a floating toast notification that fades away."""
        toast = tk.Toplevel(self)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)
        toast.configure(bg="#1A1A2E")

        # Position at top-right of screen
        toast.update_idletasks()
        sw = self.winfo_screenwidth()
        toast.geometry(f"320x90+{sw - 340}+20")

        inner = tk.Frame(toast, bg="#1A1A2E", padx=16, pady=12,
                         highlightbackground=color, highlightthickness=2)
        inner.pack(fill=tk.BOTH, expand=True)

        tk.Label(inner, text=title, bg="#1A1A2E", fg=color,
                 font=(FONT_FAMILY, 11, "bold"), anchor="w").pack(fill=tk.X)
        tk.Label(inner, text=message, bg="#1A1A2E", fg=FG_PRIMARY,
                 font=(FONT_FAMILY, 9), anchor="w", justify=tk.LEFT).pack(fill=tk.X, pady=(4, 0))

        def fade_out(alpha=1.0):
            if alpha > 0:
                try:
                    toast.attributes("-alpha", alpha)
                    self.after(50, lambda: fade_out(alpha - 0.05))
                except tk.TclError:
                    pass
            else:
                try:
                    toast.destroy()
                except tk.TclError:
                    pass

        self.after(3000, fade_out)

    # ════════════════════════════════════════════════════════
    #   DAILY GOAL TRACKING
    # ════════════════════════════════════════════════════════

    def _get_daily_flashes(self):
        """Get today's flash count, resetting if it's a new day."""
        today = datetime.date.today().isoformat()
        if self.settings.get("daily_flashes_date") != today:
            self.settings.set("daily_flashes_date", today)
            self.settings.set("daily_flashes_today", 0)
        return self.settings.get("daily_flashes_today")

    def _add_daily_flashes(self, count):
        """Add to today's flash count."""
        today = datetime.date.today().isoformat()
        if self.settings.get("daily_flashes_date") != today:
            self.settings.set("daily_flashes_date", today)
            self.settings.set("daily_flashes_today", 0)
        current = self.settings.get("daily_flashes_today") or 0
        self.settings.set("daily_flashes_today", current + count)

    def _record_session(self, flash_count, duration_seconds):
        """Record a session to history."""
        history = list(self.settings.get("session_history") or [])
        history.append({
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "flashes": flash_count,
            "duration": int(duration_seconds),
        })
        # Keep last 30
        self.settings.set("session_history", history[-30:])

    def _on_closing(self):
        self.flasher.stop()
        self.destroy()
