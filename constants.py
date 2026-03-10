# ──────────────────────────────────────────────────────────────
#  Subliminal Master - Theme, Colors & Configuration Constants
# ──────────────────────────────────────────────────────────────

# Color palette
BG_DARK = "#0D0D1A"
BG_CARD = "#141428"
BG_ACCENT = "#1E1E3F"
BG_INPUT = "#1A1A35"
BG_HOVER = "#252550"
FG_PRIMARY = "#E8E8F0"
FG_DIM = "#6B6B8D"
FG_BRIGHT = "#FFFFFF"
GREEN = "#00E676"
GREEN_HOVER = "#69F0AE"
GREEN_DIM = "#00E67640"
RED = "#FF1744"
RED_HOVER = "#FF5252"
GOLD = "#FFD740"
PURPLE = "#B388FF"
PURPLE_HOVER = "#D1B3FF"
CYAN = "#18FFFF"
PINK = "#FF80AB"
ORANGE = "#FF9100"

# Neon glow colors for rainbow mode
NEON_COLORS = [
    "#FF006E", "#FF4DA6", "#FB5607", "#FFBE0B", "#FFD700",
    "#00F5D4", "#00BBF9", "#9B5DE5", "#F15BB5", "#FEE440",
    "#00E676", "#18FFFF", "#FF1744", "#D500F9", "#651FFF",
]

# Flash animation styles
FLASH_EFFECTS = ["Instant", "Fade In", "Glow Pulse", "Typewriter"]

# Screen zones where messages can appear
FOCUS_ZONES = ["Full Screen", "Top Half", "Center Band", "Bottom Half", "Corners Only"]

# Breathing patterns: (inhale_sec, hold_sec, exhale_sec)
BREATHING_PATTERNS = {
    "Off": None,
    "4-7-8 Calm": (4, 7, 8),
    "Box Breathing 4-4-4-4": (4, 4, 4),
    "Power Breath 3-3-3": (3, 3, 3),
    "Deep Focus 5-5-5": (5, 5, 5),
}

# Preset affirmation packs for quick loading
MESSAGE_PRESETS = {
    "Wealth & Abundance": [
        "Money flows to me easily and abundantly.",
        "I am a magnet for financial prosperity.",
        "Wealth is my birthright. I claim it now.",
        "Every day my income increases.",
        "I attract lucrative opportunities effortlessly.",
        "My bank account grows while I sleep.",
        "I am worthy of massive financial success.",
        "Abundance surrounds me in every area of life.",
    ],
    "Confidence & Power": [
        "I am unstoppable.",
        "I radiate confidence in every room I enter.",
        "My presence commands respect.",
        "I believe in myself completely.",
        "I am powerful beyond measure.",
        "Fear has no authority over me.",
        "I speak with authority and clarity.",
        "I am the architect of my destiny.",
    ],
    "Health & Healing": [
        "My body heals itself rapidly.",
        "Every cell in my body vibrates with health.",
        "I am full of energy and vitality.",
        "My immune system is strong and powerful.",
        "I choose health in every decision I make.",
        "My mind and body are in perfect harmony.",
        "I release all tension and stress now.",
        "I sleep deeply and wake refreshed.",
    ],
    "Love & Relationships": [
        "I attract loving, genuine people.",
        "I am worthy of deep, meaningful love.",
        "My relationships are healthy and fulfilling.",
        "I give and receive love effortlessly.",
        "I am surrounded by people who uplift me.",
        "My heart is open to receiving blessings.",
        "I attract my divine connections now.",
        "Love flows through everything I do.",
    ],
    "Career & Success": [
        "I am a high-value professional.",
        "Promotions and raises seek me out.",
        "I deliver excellence in everything I do.",
        "My skills are in massive demand.",
        "I attract dream job opportunities.",
        "Leaders recognize my talent instantly.",
        "I negotiate with power and confidence.",
        "Success is inevitable for me.",
    ],
}
