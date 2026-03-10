# ──────────────────────────────────────────────────────────────
#  Subliminal Master - Cross-Platform Utilities
#  Detects OS and provides platform-safe helpers for fonts,
#  sounds, hotkeys, startup registration, and transparency.
# ──────────────────────────────────────────────────────────────

import sys
import os
import subprocess
import hashlib
import stat
from xml.sax.saxutils import escape as xml_escape

PLATFORM = sys.platform  # "win32", "darwin", "linux"
IS_WINDOWS = PLATFORM == "win32"
IS_MAC = PLATFORM == "darwin"
IS_LINUX = PLATFORM.startswith("linux")

# ── Cross-platform font ────────────────────────────────────

if IS_MAC:
    FONT_FAMILY = "Helvetica Neue"
    FONT_MONO = "Menlo"
elif IS_WINDOWS:
    FONT_FAMILY = "Segoe UI"
    FONT_MONO = "Consolas"
else:
    FONT_FAMILY = "DejaVu Sans"
    FONT_MONO = "DejaVu Sans Mono"

# ── Hotkey modifier (Cmd on Mac, Ctrl on Windows/Linux) ────

MOD_KEY = "Command" if IS_MAC else "Control"
MOD_DISPLAY = "Cmd" if IS_MAC else "Ctrl"

# ── Sound ──────────────────────────────────────────────────

HAS_SOUND = False
if IS_WINDOWS:
    try:
        import winsound
        HAS_SOUND = True
    except ImportError:
        pass


_MAC_SOUND_FILE = "/System/Library/Sounds/Tink.aiff"


def play_ping():
    """Play a short ambient ping sound, cross-platform."""
    if IS_WINDOWS and HAS_SOUND:
        try:
            winsound.Beep(800, 30)
        except Exception:
            pass
    elif IS_MAC:
        try:
            # Only play the sound if the file actually exists (prevents path manipulation)
            if os.path.isfile(_MAC_SOUND_FILE):
                subprocess.Popen(
                    ["/usr/bin/afplay", _MAC_SOUND_FILE],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    # Prevent shell injection: no shell=True, use full path
                )
        except Exception:
            pass


# ── Transparent window ─────────────────────────────────────

def make_window_transparent(window):
    """Apply transparency to a Toplevel flash window, platform-safe."""
    window.overrideredirect(True)
    window.attributes("-topmost", True)

    if IS_WINDOWS:
        window.configure(bg="black")
        window.attributes("-transparentcolor", "black")
    elif IS_MAC:
        window.configure(bg="systemTransparent")
        try:
            window.attributes("-transparent", True)
        except Exception:
            window.configure(bg="black")
            window.wait_visibility(window)
            try:
                window.attributes("-alpha", 0.95)
            except Exception:
                pass
    else:
        window.configure(bg="black")
        try:
            window.attributes("-transparentcolor", "black")
        except Exception:
            window.attributes("-alpha", 0.95)


def get_transparent_bg():
    """Return the bg color string used for transparent flash windows."""
    if IS_MAC:
        return "systemTransparent"
    return "black"


# ── Startup registration ──────────────────────────────────

def _get_script_path():
    """Get the full path to subliminal_master.py or the exe."""
    if getattr(sys, "frozen", False):
        return os.path.realpath(sys.executable)
    return os.path.realpath(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "subliminal_master.py"))
    )


def is_registered_at_startup():
    """Check if the app is registered to run on OS startup."""
    if IS_WINDOWS:
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, "SubliminalMaster")
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False
    elif IS_MAC:
        plist = os.path.expanduser(
            "~/Library/LaunchAgents/com.subliminalmaster.plist")
        return os.path.exists(plist)
    return False


def _validate_startup_path(path):
    """Validate that the startup path is safe and points to our app."""
    if not path or not isinstance(path, str):
        return False
    # Must be an absolute path
    if not os.path.isabs(path):
        return False
    # Must actually exist
    if not os.path.isfile(path):
        return False
    # Must not contain shell metacharacters that could enable injection
    dangerous_chars = set(';&|`$(){}[]!#~')
    if any(c in path for c in dangerous_chars):
        return False
    # Path length limit
    if len(path) > 512:
        return False
    return True


def register_at_startup():
    """Register the app to auto-run when the user logs in."""
    script = _get_script_path()

    # Validate the path before registering
    if not _validate_startup_path(script):
        print(f"Startup registration blocked: invalid path '{script}'")
        return False

    if IS_WINDOWS:
        try:
            import winreg
            if getattr(sys, "frozen", False):
                cmd = f'"{script}"'
            else:
                python_path = sys.executable
                if not _validate_startup_path(python_path):
                    print("Startup registration blocked: invalid Python path")
                    return False
                cmd = f'"{python_path}" "{script}"'
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SubliminalMaster", 0, winreg.REG_SZ, cmd)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Startup registration failed: {e}")
            return False

    elif IS_MAC:
        plist_path = os.path.expanduser(
            "~/Library/LaunchAgents/com.subliminalmaster.plist")
        # XML-escape paths to prevent XML injection attacks
        if getattr(sys, "frozen", False):
            program_args = f"    <string>{xml_escape(script)}</string>"
        else:
            python_path = sys.executable
            if not _validate_startup_path(python_path):
                print("Startup registration blocked: invalid Python path")
                return False
            program_args = (f"    <string>{xml_escape(python_path)}</string>\n"
                            f"    <string>{xml_escape(script)}</string>")
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.subliminalmaster</string>
  <key>ProgramArguments</key>
  <array>
{program_args}
  </array>
  <key>RunAtLoad</key>
  <true/>
</dict>
</plist>"""
        try:
            os.makedirs(os.path.dirname(plist_path), exist_ok=True)
            with open(plist_path, "w", encoding="utf-8") as f:
                f.write(plist_content)
            # Restrict plist file permissions (owner read/write only)
            os.chmod(plist_path, stat.S_IRUSR | stat.S_IWUSR)
            return True
        except Exception as e:
            print(f"Startup registration failed: {e}")
            return False
    return False


def unregister_at_startup():
    """Remove the app from auto-run on login."""
    if IS_WINDOWS:
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE)
            try:
                winreg.DeleteValue(key, "SubliminalMaster")
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
            return True
        except Exception:
            return False
    elif IS_MAC:
        plist = os.path.expanduser(
            "~/Library/LaunchAgents/com.subliminalmaster.plist")
        try:
            if os.path.exists(plist):
                os.remove(plist)
            return True
        except Exception:
            return False
    return False
