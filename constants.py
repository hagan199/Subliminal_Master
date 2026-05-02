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
FLASH_EFFECTS = ["Instant", "Fade In", "Glow Pulse", "Typewriter", "Slide In", "Matrix Rain", "Spiral Emerge", "Random"]

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

# ── Ambient Color Themes ───────────────────────────────────
# Each theme: (name, [list of flash colors], night_colors)
COLOR_THEMES = {
    "Default": {
        "colors": NEON_COLORS,
        "night": ["#FF8F00", "#FFA726", "#FFB74D", "#FFCC02", "#E65100"],
    },
    "Ocean Deep": {
        "colors": ["#00B4D8", "#0077B6", "#48CAE4", "#90E0EF", "#00E5FF",
                    "#26C6DA", "#00ACC1", "#0097A7", "#80DEEA", "#B2EBF2"],
        "night": ["#1A237E", "#283593", "#3949AB", "#5C6BC0", "#7986CB"],
    },
    "Galaxy": {
        "colors": ["#E040FB", "#D500F9", "#AA00FF", "#7C4DFF", "#651FFF",
                    "#536DFE", "#448AFF", "#B388FF", "#EA80FC", "#F50057"],
        "night": ["#4A148C", "#6A1B9A", "#7B1FA2", "#8E24AA", "#9C27B0"],
    },
    "Forest": {
        "colors": ["#00E676", "#69F0AE", "#00C853", "#76FF03", "#B2FF59",
                    "#CCFF90", "#64DD17", "#00BFA5", "#1DE9B6", "#A7FFEB"],
        "night": ["#1B5E20", "#2E7D32", "#388E3C", "#43A047", "#4CAF50"],
    },
    "Sunset": {
        "colors": ["#FF6D00", "#FF9100", "#FFAB00", "#FFD600", "#FF1744",
                    "#FF5252", "#FF8A80", "#FF80AB", "#F50057", "#FF6E40"],
        "night": ["#BF360C", "#D84315", "#E64A19", "#F4511E", "#FF5722"],
    },
    "Neon City": {
        "colors": ["#FF006E", "#FB5607", "#FFBE0B", "#8338EC", "#3A86FF",
                    "#FF0099", "#00FF87", "#FFE600", "#FF3D00", "#00E5FF"],
        "night": ["#880E4F", "#AD1457", "#C2185B", "#D81B60", "#E91E63"],
    },
    "Ice Crystal": {
        "colors": ["#E0F7FA", "#B2EBF2", "#80DEEA", "#4DD0E1", "#26C6DA",
                    "#00BCD4", "#00ACC1", "#0097A7", "#00838F", "#E1F5FE"],
        "night": ["#01579B", "#0277BD", "#0288D1", "#039BE5", "#03A9F4"],
    },
}

# ── Achievement Definitions ────────────────────────────────
ACHIEVEMENTS = {
    "first_flash": {
        "title": "First Flash",
        "desc": "Started your first session!",
        "icon": "ZAP",
        "condition": lambda stats: stats.get("session_count", 0) >= 1,
    },
    "century": {
        "title": "Century Club",
        "desc": "100 total flashes!",
        "icon": "STAR",
        "condition": lambda stats: stats.get("total_flashes", 0) >= 100,
    },
    "thousand": {
        "title": "Thousand Strong",
        "desc": "1,000 total flashes!",
        "icon": "FIRE",
        "condition": lambda stats: stats.get("total_flashes", 0) >= 1000,
    },
    "ten_thousand": {
        "title": "Mind Master",
        "desc": "10,000 total flashes! Legendary!",
        "icon": "CROWN",
        "condition": lambda stats: stats.get("total_flashes", 0) >= 10000,
    },
    "week_streak": {
        "title": "Week Warrior",
        "desc": "7-day streak! Consistency is key.",
        "icon": "FLAME",
        "condition": lambda stats: stats.get("streak_days", 0) >= 7,
    },
    "month_streak": {
        "title": "Unstoppable",
        "desc": "30-day streak! You're on fire!",
        "icon": "TROPHY",
        "condition": lambda stats: stats.get("streak_days", 0) >= 30,
    },
    "ten_sessions": {
        "title": "Regular",
        "desc": "10 sessions completed!",
        "icon": "CHECK",
        "condition": lambda stats: stats.get("session_count", 0) >= 10,
    },
    "fifty_sessions": {
        "title": "Devoted",
        "desc": "50 sessions! True dedication.",
        "icon": "DIAMOND",
        "condition": lambda stats: stats.get("session_count", 0) >= 50,
    },
    "hundred_sessions": {
        "title": "Ascended",
        "desc": "100 sessions! You've transformed.",
        "icon": "ROCKET",
        "condition": lambda stats: stats.get("session_count", 0) >= 100,
    },
}

# ── Daily Motivational Quotes ──────────────────────────────
DAILY_QUOTES = [
    ("Your thoughts create your reality.", "Buddha"),
    ("What you think, you become.", "Mahatma Gandhi"),
    ("The mind is everything. What you think you become.", "Buddha"),
    ("Change your thoughts and you change your world.", "Norman Vincent Peale"),
    ("You are what you believe yourself to be.", "Paulo Coelho"),
    ("The only limit to our realization of tomorrow is our doubts of today.", "Franklin D. Roosevelt"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("Act as if what you do makes a difference. It does.", "William James"),
    ("What lies behind us and what lies before us are tiny matters compared to what lies within us.", "Ralph Waldo Emerson"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("You are never too old to set another goal or to dream a new dream.", "C.S. Lewis"),
    ("Everything you've ever wanted is on the other side of fear.", "George Addair"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Your limitation is only your imagination.", "Unknown"),
    ("Push yourself, because no one else is going to do it for you.", "Unknown"),
    ("Great things never come from comfort zones.", "Unknown"),
    ("Dream it. Wish it. Do it.", "Unknown"),
    ("Success doesn't just find you. You have to go out and get it.", "Unknown"),
    ("Don't stop when you're tired. Stop when you're done.", "Unknown"),
    ("Wake up with determination. Go to bed with satisfaction.", "Unknown"),
    ("The harder you work for something, the greater you'll feel when you achieve it.", "Unknown"),
    ("Dream bigger. Do bigger.", "Unknown"),
    ("Don't wait for opportunity. Create it.", "Unknown"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("What we plant in the soil of contemplation, we shall reap in the harvest of action.", "Meister Eckhart"),
    ("Your subconscious mind is a powerful force. Use it wisely.", "Unknown"),
    ("Repetition is the mother of learning, the father of action.", "Zig Ziglar"),
    ("You become what you think about most of the time.", "Earl Nightingale"),
    ("The mind is a powerful thing. When you fill it with positive thoughts, your life will start to change.", "Unknown"),
    ("Program your mind with success and you will get it.", "Unknown"),
    ("Every thought we think is creating our future.", "Louise L. Hay"),
]
