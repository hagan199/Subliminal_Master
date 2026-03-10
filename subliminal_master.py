# ──────────────────────────────────────────────────────────────
#  Subliminal Master - Entry Point
#  Flash affirmations on your screen below conscious perception.
# ──────────────────────────────────────────────────────────────

from messages import create_default_message_files
from settings import Settings
from app import App

if __name__ == "__main__":
    create_default_message_files()
    app_settings = Settings()
    app = App(app_settings)
    app.mainloop()
