# ──────────────────────────────────────────────────────────────
#  Subliminal Master - Reusable UI Components
#  Factory functions for styled sections, sliders, and toggles.
# ──────────────────────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk

from constants import BG_CARD, BG_ACCENT, BG_DARK, FG_PRIMARY, FG_DIM, CYAN
from platform_utils import FONT_FAMILY


def make_section(parent, title, description=None):
    """Create a styled card-like section with a title and optional description."""
    frame = tk.Frame(parent, bg=BG_CARD, highlightbackground=BG_ACCENT,
                     highlightthickness=1, padx=16, pady=12)
    frame.pack(fill=tk.X, pady=(0, 10))

    tk.Label(frame, text=title, bg=BG_CARD, fg="#B388FF",
             font=(FONT_FAMILY, 11, "bold"), anchor="w").pack(fill=tk.X)
    if description:
        tk.Label(frame, text=description, bg=BG_CARD, fg=FG_DIM,
                 font=(FONT_FAMILY, 8), anchor="w", wraplength=420).pack(fill=tk.X, pady=(0, 6))
    return frame


def make_labeled_slider(parent, label_text, hint, setting_key, from_, to,
                        is_int, settings_obj):
    """Slider with a label, hint text, and live value readout."""
    container = tk.Frame(parent, bg=BG_CARD)
    container.pack(fill=tk.X, pady=3)

    top_row = tk.Frame(container, bg=BG_CARD)
    top_row.pack(fill=tk.X)

    tk.Label(top_row, text=label_text, bg=BG_CARD, fg=FG_PRIMARY,
             font=(FONT_FAMILY, 10), anchor="w").pack(side=tk.LEFT)

    val_label = tk.Label(top_row, text="", bg=BG_CARD, fg=CYAN,
                         font=(FONT_FAMILY, 10, "bold"), anchor="e")
    val_label.pack(side=tk.RIGHT)

    if hint:
        tk.Label(container, text=hint, bg=BG_CARD, fg=FG_DIM,
                 font=(FONT_FAMILY, 8), anchor="w").pack(fill=tk.X)

    var = tk.IntVar(value=settings_obj.get(setting_key)) if is_int \
        else tk.DoubleVar(value=settings_obj.get(setting_key))

    def on_change(v):
        if is_int:
            val = int(float(v))
            val_label.config(text=str(val))
        else:
            val = round(float(v), 2)
            val_label.config(text=f"{val:.2f}")
        settings_obj.set(setting_key, val)

    if is_int:
        val_label.config(text=str(int(var.get())))
    else:
        val_label.config(text=f"{var.get():.2f}")

    slider = ttk.Scale(container, from_=from_, to=to, variable=var,
                       orient=tk.HORIZONTAL, command=on_change)
    slider.pack(fill=tk.X, pady=(2, 0))

    return var


def make_toggle(parent, text, variable, command=None, color=FG_PRIMARY,
                bold=False):
    """Styled checkbox toggle."""
    f = (FONT_FAMILY, 10, "bold") if bold else (FONT_FAMILY, 10)
    cb = tk.Checkbutton(
        parent, text=text, variable=variable, command=command,
        bg=BG_CARD, fg=color, selectcolor=BG_DARK,
        activebackground=BG_CARD, activeforeground=color, font=f,
        anchor="w", padx=4
    )
    cb.pack(fill=tk.X, pady=2)
    return cb
