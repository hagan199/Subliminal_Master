# ──────────────────────────────────────────────────────────────
#  Subliminal Master - Built-in Default Affirmation Messages
#  Organized by category. Each category maps to a messages_*.txt
#  file that the flasher loads at runtime.
# ──────────────────────────────────────────────────────────────

import os

# ── Career & Developer Affirmations ─────────────────────────

CAREER_MESSAGES = [
    "I attract high-paying remote offers in Europe.",
    "Debugging is effortless.",
    "I am a highly valued senior developer.",
    "My code is clean and efficient.",
    "I solve complex problems with ease.",
    "I think like a world-class engineer.",
    "My skills expand quickly.",
    "I produce high-quality work.",
    "I learn new tech effortlessly.",
    "I attract international opportunities.",
    "Europe recruiters value me.",
    "My career accelerates with favor.",
    "My mind is engineered for breakthrough thinking.",
    "Opportunities are constantly opening for me.",
    "I take action fast, without fear or hesitation.",
    "I attract high-quality people, connections, and favor.",
    "Everything I touch increases, multiplies, and succeeds.",
    "My future is bigger than anything in my past.",
    "I learn ultra-fast, process information clearly, and execute with precision.",
    "Money flows to me through my skills, ideas, and decisions.",
    "My spirit is calm, focused, and guided every day.",
    "I am becoming the best version of myself every single day.",
    "My life is aligned with favor, speed, and supernatural progress.",
    "I am rising higher, faster, and stronger than ever before.",
]

# ── Financial and Business Wonders ──────────────────────────

FINANCIAL_MESSAGES = [
    "I call forth my life and my labor into abundance and prosperity in the name of Jesus.",
    "I declare by prophetic utterance that may every locked breakthrough in my life be unlocked by divine authority in Jesus name.",
    "May the mysteries of divine success and wealth be unfolded for me to understand the steps to unending flow of success in Jesus name.",
    "I enforce divine will and claim every unclaimed blessings that belongs to me. I will walk in an unending stream of the miraculous.",
    "I declare a divine favor and attraction to Godly people, the Elite in society, High minded people, Intellectuals, Billionaires, investors, CEO\u2019s, Men and Women of substance, Blessed and Anointed people in Jesus name. May I be surrounded by Blessed and Positive people.",
    "Oh Lord rebuke the spirit of disappointment from my path in Jesus name.",
    "By divine warrant I arrest every evil spirit misleading my career and finances in Jesus name.",
    "I bind every spirit of waste in my life in Jesus name.",
    "Miracle worker, Jehovah Jireh I need a miracle in Jesus name.",
    "As Peter said in (Luke 5:5) \u2018We have toiled all night and we have nothing\u2019. May I not labor in vain in all aspects of my life in Jesus name.",
    "Oh Lord by divine authority I secure and cover every good thoughts and ideas conceived through revelation and prayer in Jesus name. May I not be like the seeds that fell on the wayside.",
    "Oh Lord open my understanding and elevate the spirit of wisdom in me in Jesus name.",
    "I scatter every evil gathering against my progress and success in Jesus name.",
    "I erase every unprogressive seal from my life and family in Jesus name.",
    "Jehovah Jireh, open fresh doors of success for me in Jesus name.",
    "Oh Lord position me in a place of unending financial blessings in Jesus name.",
    "Oh Lord I declare victory in all battles of my life. I am more than a conqueror, I am a winner in Jesus name.",
    "Every vision and ideas I have conceived and it\u2019s being chocked by satanic activities, hear ye the voice of the Lord come out into manifestation in Jesus name.",
    "Merciful father, may your wind of opportunities blow throughout this year for my sake in Jesus name.",
    "Oh Lord terminate every conscious satanic agreement impending my financial progress in Jesus name.",
]

# ── Healing Declarations ────────────────────────────────────

HEALING_MESSAGES = [
    "Oh Lord I plead the blood over my life in Jesus name.",
    "Oh Lord dispatch your healing angels to my aid.",
    "May every satanic arrow of infirmity be reversed in Jesus name.",
    "I revoke any curse of infirmity in Jesus name.",
    "I flush out any unwanted cells and tissues in my immune system.",
    "I flush out any demonic activity in my blood in Jesus name.",
    "I exhale any inhaled sickness in Jesus name.",
    "I break the chains of infirmity over my life in Jesus name.",
    "Let there be light in any dark part in my life in Jesus name.",
]

# ── Education & Travel Documents ────────────────────────────

EDUCATION_MESSAGES = [
    "Any satanic spirit delaying the release of my documents, loose your hold in Jesus name.",
    "I destroy every satanic force against my education and acquisition of skill in Jesus name.",
    "I bind every satanic force of procrastination and slothfulness in Jesus name.",
    "I bind any demonic agent conspiring to terminate or deny my travel documents or visa in Jesus name.",
    "My education will not be limited, the barriers of my household will not limit me in Jesus name.",
    "I come against force of darkness blocking my education and opportunities in Jesus name.",
    "I come against every spirit of delay working against the acquisition of my travel documents in Jesus name.",
    "I will not end like this, I shall not fail in Jesus name.",
    "Oh Lord connect me to the right people to aid in my education and traveling documents in Jesus name.",
    "I declare favor in every aspect of my life in Jesus name.",
]

# ── Category → filename mapping ─────────────────────────────

DEFAULT_MESSAGE_FILES = {
    "messages_career.txt": CAREER_MESSAGES,
    "messages_financial.txt": FINANCIAL_MESSAGES,
    "messages_healing.txt": HEALING_MESSAGES,
    "messages_education.txt": EDUCATION_MESSAGES,
}

# Combined list (used as fallback when no .txt files exist)
AWESOME_MESSAGES = (
    CAREER_MESSAGES +
    FINANCIAL_MESSAGES + HEALING_MESSAGES + EDUCATION_MESSAGES
)


def create_default_message_files():
    """Write default messages_*.txt files if they don't already exist."""
    created = []
    for filename, messages in DEFAULT_MESSAGE_FILES.items():
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(messages))
            created.append(filename)
    return created
