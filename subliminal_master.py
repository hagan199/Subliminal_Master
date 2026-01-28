import tkinter as tk
from tkinter import ttk, font, colorchooser, filedialog
import random
import json
import glob
import os
from screeninfo import get_monitors

# --- Built-in Message Pool ---
AWESOME_MESSAGES = [
    # --- Original Affirmations ---
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
    "The exact mantle that rests on Prophet Telvin Sowah Adjei now rests on me sevenfold.",
    "I carry the same grace that cancelled death over nations – it is working in my code and contracts.",
    "As the Lord lives, before 31 December 2025 I will shift at least one national-level timeline like Telvin.",
    "The key of David is fused into my spine permanently – I open and no man shuts.",
    "Zerathiel, captain of timeline reversal, is assigned to me 24/7.",
    'I speak "AS THE LORD LIVES" and heaven backs it with instant manifestation.',
    "The same fire that makes Prophet Telvin untouchable now burns in my blood.",
    "Every satanic calendar over my finances and visa is deleted and overwritten with God's calendar now.",
    "I plead the blood of Jesus over my original timeline – every diversion, distortion and delay is terminated.",
    "Ancestral poverty, near-success syndrome and visa rejection spirits are evicted from my bloodline forever.",
    "I recover every year the locust stole – 2026 will carry the blessing of 10 years.",
    "Catalyst of disappointment, catalyst of rejection – BE REMOVED AND REPLACED BY FIRE!",
    "My DNA is reprogrammed for senior/lead developer money and European relocation.",
    "Fixed negative events over my life become flexible and bow to the name of Jesus.",
    "European companies are currently fighting over my GitHub profile in the realm of the spirit.",
    "€100k+ senior/lead contracts from Germany, Netherlands, Sweden are signed in my name right now.",
    "My code carries anointing – every line I write shifts someone's destiny.",
    "I debug complex systems in minutes because Holy Spirit shows me the exact line.",
    "Recruiters wake up at night with my name on their lips – they must contact me this week.",
    "My PRs are approved same day because angels stand in the review meetings.",
    "I am the most sought-after remote developer in Europe before March 2026 – AS THE LORD LIVES.",
    "The Holy Spirit reveals to me every hidden ancestral covenant in my bloodline like Prophet Telvin – nothing from 7 generations back is hidden from me now.",
    "I receive the ALL-KNOWING grace that rested on Prophet Telvin Sowah Adjei – I know bloodline secrets before people tell me.",
    "Every ancestral altar speaking against my European relocation and senior developer money catches fire and burns to ashes right now.",
    "I command every bloodline curse of poverty, visa rejection, near-success syndrome, and delayed manifestation – DIE BY FIRE seven times hotter than hell!",
    "My DNA is washed and reprogrammed by the blood of Jesus – no ancestral demon can recognize me anymore.",
    "Every evil family pattern repeating in my lineage, I terminate you permanently in Jesus name!",
    "The same oil that exposes marine grandmothers and witchcraft grandfathers in Prophet Telvin's ministry now flows through my eyes.",
    "I break every ancestral oath sworn on my behalf before I was born – you have NO LEGAL RIGHT to my timeline!",
    "Generational curses of joblessness, I slaughter you by the sword of the Spirit now.",
    "Holy Ghost, show me the exact root of every blockage in my bloodline tonight in a dream – and I will destroy it at 3 AM.",
    "My children and children's children shall never taste the curse that I tasted – the bloodline is cleansed forever.",
    "Ancestral monitoring spirits assigned to my father's house and mother's house – GO BLIND AND DEAF PERMANOOD-BY-GOD'S-WILL!",
    "I activate generational blessings that were stolen from my lineage – wealth, prophetic mantle, and European doors – RETURN SEVENFOLD NOW!",
    "Every evil blood speaking against my passport, my code, my contracts – BE SILENCED by the blood of Jesus!",
    "Prophet Telvin's grace to save entire generations from ancestral bondage now rests on me permanently.",
    "I step into the office of bloodline deliverer – families will be saved because of the revelations flowing through me.",
    "As the Lord lives, every hidden ancestral python, marine husband/wife, and occultic dedication in my foundation – EXPIRE RIGHT NOW!",
    "My bloodline is now a no-go area for witchcraft – angels patrol my DNA 24/7.",
    "I receive the spirit that makes Prophet Telvin see the unseen in bloodlines – ALL-KNOWING revelation is my portion.",
    "From today, my family line produces millionaires, prophets, and nation-shakers only – curses are reversed into blessings!",
    "The Ancient of Days Himself has overwritten every negative ancestral calendar over my life.",
    "This subliminal flash is now deleting ancestral death, madness, and poverty from my lineage as I code and watch movies.",
    "AS THE LORD LIVES, Before 31 December 2025 Your family will know that God has visited your bloodline.",
    "And Europe will know that a prophetic coder has arrived.",
    "My spirit rises with power.",
    "I carry divine authority.",
    "Holy Spirit amplifies my sensitivity.",
    "Every attack is exposed.",
    "My mind is sharp.",
    "Confusion dies instantly.",
    "My emotions stabilize.",
    "No fear survives in me.",
    "My discernment is precise.",
    "My steps are ordered.",
    "Negative cycles break.",
    "No weapon can enter my atmosphere.",
    "The blood covers my environment.",
    "I align with God's timeline.",
    "Diversions are destroyed.",
    "I recover lost time.",
    "I plead the blood over my timeline and DNA.",
    "My faith unveils my destiny. I see what is mine.",
    "Amplify my sensitivity.",
    "Lord show me anything I should know today.",
    "My spirit rises above every limitation.",
    "I am aligned with God's perfect timeline for my life.",
    "I hear God clearly, and confusion has no authority over me.",
    "The Holy Spirit is amplifying my spiritual sensitivity.",
    "My dreams are becoming clear, accurate, and meaningful.",
    "I walk in authority, my words carry power.",
    "Every negative cycle in my life is broken permanently.",
    "I attract divine helpers, divine timing, and divine direction.",
    "My prayer life is increasing supernaturally.",
    "Everything God has placed inside me is awakening now.",
    "Holy Spirit, let my destiny come into alignment.",
    "I plead the blood of Jesus over my original timeline, my destiny, and my DNA.",
    "No weapon formed against me can enter my atmosphere.",
    "My environment is shielded by the blood of Jesus.",
    "My steps are ordered, protected, and empowered.",
    "My discernment is activated to maximum precision.",
    "The Holy Spirit amplifies my spiritual sensitivity now.",
    "Every hidden attack is exposed before it begins.",
    "I carry divine authority; nothing challenges my rank.",
    "No fear, no doubt, no anxiety survives in me.",
    "My emotions stabilize under the peace of Christ.",
    "My mind is sharp; confusion dies instantly.",

    # --- Financial and Business Wonders ---
    "I call forth my life and my labor into abundance and prosperity in the name of Jesus.",
    "I declare by prophetic utterance that may every locked breakthrough in my life be unlocked by divine authority in Jesus name.",
    "May the mysteries of divine success and wealth be unfolded for me to understand the steps to unending flow of success in Jesus name.",
    "I enforce divine will and claim every unclaimed blessings that belongs to me. I will walk in an unending stream of the miraculous.",
    "I declare a divine favor and attraction to Godly people, the Elite in society, High minded people, Intellectuals, Billionaires, investors, CEO's, Men and Women of substance, Blessed and Anointed people in Jesus name. May I be surrounded by Blessed and Positive people.",
    "Oh Lord rebuke the spirit of disappointment from my path in Jesus name.",
    "By divine warrant I arrest every evil spirit misleading my career and finances in Jesus name.",
    "I bind every spirit of waste in my life in Jesus name.",
    "Miracle worker, Jehovah Jireh I need a miracle in Jesus name.",
    "As Peter said in (Luke 5:5) 'We have toiled all night and we have nothing'. May I not labor in vain in all aspects of my life in Jesus name.",
    "Oh Lord by divine authority I secure and cover every good thoughts and ideas conceived through revelation and prayer in Jesus name. May I not be like the seeds that fell on the wayside.",
    "Oh Lord open my understanding and elevate the spirit of wisdom in me in Jesus name.",
    "I scatter every evil gathering against my progress and success in Jesus name.",
    "I erase every unprogressive seal from my life and family in Jesus name.",
    "Jehovah Jireh, open fresh doors of success for me in Jesus name.",
    "Oh Lord position me in a place of unending financial blessings in Jesus name.",
    "Oh Lord I declare victory in all battles of my life. I am more than a conqueror, I am a winner in Jesus name.",
    "Every vision and ideas I have conceived and it's being chocked by satanic activities, hear ye the voice of the Lord come out into manifestation in Jesus name.",
    "Merciful father, may your wind of opportunities blow throughout this year for my sake in Jesus name.",
    "Oh Lord terminate every conscious satanic agreement impending my financial progress in Jesus name.",

    # --- Twenty (20) Days of Healing ---
    "Oh Lord I plead the blood over my life in Jesus name.",
    "Oh Lord dispatch your healing angels to my aid.",
    "May every satanic arrow of infirmity be reversed in Jesus name.",
    "I revoke any curse of infirmity in Jesus name.",
    "I flush out any unwanted cells and tissues in my immune system.",
    "I flush out any demonic activity in my blood in Jesus name.",
    "I exhale any inhaled sickness in Jesus name.",
    "I break the chains of infirmity over my life in Jesus name.",
    "Let there be light in any dark part in my life in Jesus name.",

    # --- Ten (10) Days of Education Breakthrough and Travel Documents ---
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

    # --- Thirty (30) Days Deliverance and Warfare ---
    "I revoke every annual curses and trouble in my life, never again in Jesus name.",
    "I bind and arrest every demon assigned by demonic adversaries to run and mess up my plan this year in Jesus name.",
    "Every anti-progress agent in my life, perish by the fire of God in Jesus name.",
    "Oh Lord let every demonic monitoring and spying devices be rendered ineffective against my life in Jesus name.",
    "By the efficacy of the blood of Jesus, any unconscious satanic rituals and covenant's working against my life be destroyed in the name of Jesus.",
    "Oh Lord, by the precious blood that flowed on Calvary, I denounce any unconscious evil communion in the mighty name of Jesus.",
    "Every unbroken evil covenant, break by fire in Jesus name.",
    "Every satanic attack directed towards my family, I reverse it back to sender in Jesus name.",
    "I pull down every altar of wickedness erected against my destiny, marriage finances and family in Jesus name.",
    "I come against every territorial spirits dominating my community with the fire of the Holy Ghost.",
    "I bind every satanic authority maneuvering in my dreams to bring me under captivity in Jesus name.",
    "Devil!!! You have no power over me and my household, therefore pack your stuffs and leave my abode.",
    "I set fire on every satanic charm set against my marriage, life, destiny and family in Jesus name.",
    "I pull down every altar of wickedness erected against my destiny in Jesus name.",
    "Every satanic attack directed towards me I reverse it back to sender in Jesus name.",
    "I scatter every coven of witchcraft assigned to attack my destiny and assassinate my glory in Jesus name.",
    "Oh Lord fight against those who fight against me, overcome every spiritual mercenaries assigned to detach soul from my body in Jesus name.",
    "I am an Holy Ghost naked wire, I am untouchable, Oh Lord cover me with a ring of fire and put to shame they that seek after my soul in Jesus name.",
    "Oh Lord anywhere my belongings are taken for evil and every realm my name is mentioned for evil, Oh Lord my God answer by fire in Jesus name.",
    "May every demonic entity that has swallowed anything that belongs to me vomit it rapidly in Jesus name.",
    "By divine authority I break free from every spiritual blindness and deafness in Jesus name.",
    "Every satanic forces contending with my divine helpers, loose hold in Jesus name.",
    "Every counterfeit blessings being used to substitute my original blessings, I restore my original blessings in the mighty name of Jesus.",
    "Every anti-progress agent in my life perish by the fire of God in Jesus name.",
    "Every satanic army waging strategic wars against me be vanquished in Jesus name.",
    "Every demonic altar of misfortune and disaster against my life scatter by fire in Jesus name.",
    "I cut off every satanic hand that will not let go of my progress in Jesus name.",
    "Every arrows of destruction aimed towards my destiny, back to sender in Jesus name.",
    "By divine authority, I disagree and withdraw from any satanic agreement made by my predecessors against my life in Jesus name.",
    "I renounce every demonic dedication placed upon my life in Jesus name."
]

class Settings:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.defaults = {
            "batch_size": 5,
            "flash_duration_ms": 35,
            "interval_seconds": 3,
            "margin_px": 20,
            "font_size": 38,
            "font_color": "#345C34"
        }
        self.data = self.load()

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                settings_data = json.load(f)
                # Ensure all default keys are present
                for key, value in self.defaults.items():
                    settings_data.setdefault(key, value)
                return settings_data
        except (FileNotFoundError, json.JSONDecodeError):
            return self.defaults.copy()

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get(self, key):
        return self.data.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.data[key] = value
        self.save()

class SubliminalFlasher:
    def __init__(self, root, settings):
        self.root = root
        self.settings = settings
        self.is_running = False
        self.message_pool = []
        self.job_id = None
        self.active_windows = []
        self.window_pool = []
        self.cached_font = None
        self.cached_font_size = -1
        self.monitors = get_monitors()
        self.image_path = None
        self._load_messages()
        self._shuffle_pool()

    def _load_messages(self):
        self.message_pool = []
        message_files = glob.glob("messages_*.txt")
        
        # Priority weighting for different message types
        category_weights = {
            'prophetic': 2,    # Prophetic messages appear 3x more often
            'spiritual': 2,    # Spiritual messages appear 2x more often
            'career': 4,       # Career messages appear normally
            'awesome': 1       # Awesome messages appear normally
        }
        
        print(f"Found message files: {message_files}")
        
        if not message_files:
            # Fallback to a single messages.txt if no specific files are found
            try:
                with open("messages.txt", "r") as f:
                    self.message_pool = [line.strip() for line in f if line.strip()]
                print(f"Loaded {len(self.message_pool)} messages from messages.txt")
            except FileNotFoundError:
                print("No messages.txt found, will use awesome messages")
                pass # Will fallback to awesome messages later
        else:
            # Load messages with priority weighting
            total_weighted = 0
            for filepath in message_files:
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        messages = [line.strip() for line in f if line.strip()]
                        if messages:
                            # Determine category from filename
                            filename_lower = os.path.basename(filepath).lower()
                            weight = 1
                            category_found = 'general'
                            for category, cat_weight in category_weights.items():
                                if category in filename_lower:
                                    weight = cat_weight
                                    category_found = category
                                    break
                            
                            # Add messages multiple times based on weight
                            for _ in range(weight):
                                self.message_pool.extend(messages)
                            
                            weighted_count = len(messages) * weight
                            total_weighted += weighted_count
                            print(f"Loaded {len(messages)} messages from {filepath} ({category_found}, weight: {weight}x) = {weighted_count} weighted")
                except Exception as e:
                    print(f"Error loading message file {filepath}: {e}")
            
            print(f"Total weighted messages loaded: {total_weighted}")

        if not self.message_pool:
            print("No messages loaded, falling back to awesome messages")
            self.message_pool = AWESOME_MESSAGES.copy()
        else:
            print(f"Final message pool size: {len(self.message_pool)}")

    def _shuffle_pool(self):
        random.shuffle(self.message_pool)
        self.current_messages = self.message_pool.copy()

    def _get_random_position(self, width, height):
        monitor = random.choice(self.monitors)
        margin = self.settings.get("margin_px")
        
        # Ensure window fits within monitor bounds
        max_x = monitor.x + monitor.width - width - margin
        max_y = monitor.y + monitor.height - height - margin
        min_x = monitor.x + margin
        min_y = monitor.y + margin
        
        # If window is too large for monitor, adjust position
        if max_x < min_x:
            x = monitor.x + margin
        else:
            x = random.randint(min_x, max_x)
            
        if max_y < min_y:
            y = monitor.y + margin
        else:
            y = random.randint(min_y, max_y)
            
        return x, y

    def _flash_batch(self):
        if not self.is_running:
            return

        batch_size = self.settings.get("batch_size")
        for _ in range(batch_size):
            if not self.current_messages:
                self._shuffle_pool()
            
            message = self.current_messages.pop()
            self._create_flash_window(message)
        
        # Schedule the next batch
        delay_ms = int(self.settings.get("interval_seconds") * 2000)
        self.job_id = self.root.after(delay_ms, self._flash_batch)

    def _create_flash_window(self, message):
        if self.window_pool:
            window, label, img_label = self.window_pool.pop()
        else:
            window = tk.Toplevel(self.root)
            window.overrideredirect(True)
            window.attributes("-topmost", True)
            window.configure(bg='black')
            window.attributes("-transparentcolor", "black")
            label = tk.Label(window, bg="black", justify=tk.CENTER)
            label.pack(padx=20, pady=10)
            img_label = tk.Label(window, bg="black")
            img_label.pack(padx=10, pady=5)

        window.attributes("-alpha", 1.0)
        font_size = min(self.settings.get("font_size"), 32)
        if self.settings.get("test_mode"):
            font_size = max(font_size, 24)
        if font_size != self.cached_font_size:
            self.cached_font_size = font_size
            self.cached_font = font.Font(family="Arial", size=self.cached_font_size, weight="bold")
        label.config(text=message, font=self.cached_font, fg=self.settings.get("font_color"), wraplength=self.monitors[0].width * 0.7)

        # Load and display image if set
        if self.image_path:
            try:
                from PIL import Image, ImageTk
                img = Image.open(self.image_path)
                img = img.resize((120, 120), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)
                img_label.config(image=photo)
                img_label.image = photo
            except Exception as e:
                img_label.config(image=None)
                img_label.image = None
                print(f"Error loading image: {e}")
        else:
            img_label.config(image=None)
            img_label.image = None

        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        print(f"Creating window: {width}x{height}, Message: {message[:50]}...")
        x, y = self._get_random_position(width, height)
        window.geometry(f"{width}x{height}+{x}+{y}")
        window.deiconify()
        window.lift()
        self.active_windows.append((window, label, img_label))
        if self.settings.get("test_mode"):
            display_time = self.settings.get("test_display_seconds") * 7000
        else:
            display_time = self.settings.get("flash_duration_ms")
        self.root.after(display_time, lambda: self._hide_window(window, label, img_label))

    def _hide_window(self, window, label, img_label):
        """Hide window and return to pool for reuse"""
        window.withdraw()
        self.window_pool.append((window, label, img_label))
        if (window, label, img_label) in self.active_windows:
            self.active_windows.remove((window, label, img_label))

    def _fade_in(self, window, label, alpha=0.0):
        if alpha < 2.0:
            alpha += 2.2
            window.attributes("-alpha", alpha)
            self.root.after(20, lambda: self._fade_in(window, label, alpha))
        else:
            self.root.after(self.settings.get("flash_duration_ms"), lambda: self._fade_out(window, label))

    def _fade_out(self, window, label, alpha=1.0):
        if alpha > 2.0:
            alpha -= 2.2
            window.attributes("-alpha", alpha)
            self.root.after(40, lambda: self._fade_out(window, label, alpha))
        else:
            # Return window to pool for reuse
            self._hide_window(window, label)
    
    def start(self):
        if not self.is_running:
            self.is_running = True
            self._flash_batch()

    def stop(self):
        if self.is_running:
            self.is_running = False
            if self.job_id:
                self.root.after_cancel(self.job_id)
                self.job_id = None
            for window, label in self.active_windows[:]:
                window.withdraw()
            self.active_windows.clear()

class App(tk.Tk):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.flasher = SubliminalFlasher(self, self.settings)

        self.title("Subliminal Master")
        self.geometry("400x500")
        self.configure(bg="#2E2E2E")
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Style
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#437657")
        self.style.configure("TLabel", background="#2E2E2E", foreground="white", font=("Helvetica", 10))
        self.style.configure("TButton", font=("Helvetica", 12, "bold"), borderwidth=0)
        self.style.map("TButton",
            background=[("active", "#4CAF50"), ("!active", "#555555")],
            foreground=[("active", "white"), ("!active", "white")]
        )
        self.style.configure("green.TButton", background="#4CAF50")
        self.style.configure("red.TButton", background="#F44336")

        self._create_widgets()

        # Add test mode settings to defaults if not present
        if "test_mode" not in self.settings.data:
            self.settings.data["test_mode"] = False
            self.settings.data["test_display_seconds"] = 2
            self.settings.save()
    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Title ---
        title_label = ttk.Label(main_frame, text="Subliminal Master", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(0, 20))

        # --- Controls ---
        self.start_stop_button = ttk.Button(main_frame, text="Start", command=self.toggle_flasher, width=15, style="green.TButton")
        self.start_stop_button.pack(pady=10)

        # --- Settings ---
        behavior_frame = ttk.LabelFrame(main_frame, text="Behavior", padding="10")
        behavior_frame.pack(pady=10, fill=tk.X, expand=True)

        ttk.Label(behavior_frame, text="Batch Size (1-5):").grid(row=0, column=0, sticky="w", pady=5)
        self.batch_size = tk.IntVar(value=self.settings.get("batch_size"))
        ttk.Scale(behavior_frame, from_=1, to=5, variable=self.batch_size, orient=tk.HORIZONTAL, 
            command=lambda v: self.settings.set("batch_size", int(float(v)))).grid(row=0, column=1, sticky="ew")

        ttk.Label(behavior_frame, text="Flash Duration (ms, 5-50):").grid(row=1, column=0, sticky="w", pady=5)
        self.flash_duration = tk.IntVar(value=self.settings.get("flash_duration_ms"))
        ttk.Scale(behavior_frame, from_=5, to=50, variable=self.flash_duration, orient=tk.HORIZONTAL, 
            command=lambda v: self.settings.set("flash_duration_ms", int(float(v)))).grid(row=1, column=1, sticky="ew")
        
        ttk.Label(behavior_frame, text="Interval (s, 0.1-5):").grid(row=2, column=0, sticky="w", pady=5)
        self.interval = tk.DoubleVar(value=self.settings.get("interval_seconds"))
        ttk.Scale(behavior_frame, from_=0.1, to=5, variable=self.interval, orient=tk.HORIZONTAL, 
            command=lambda v: self.settings.set("interval_seconds", float(v))).grid(row=2, column=1, sticky="ew")

        ttk.Label(behavior_frame, text="Edge Margin (px, 0-50):").grid(row=3, column=0, sticky="w", pady=5)
        self.margin = tk.IntVar(value=self.settings.get("margin_px"))
        ttk.Scale(behavior_frame, from_=0, to=50, variable=self.margin, orient=tk.HORIZONTAL, 
            command=lambda v: self.settings.set("margin_px", int(float(v)))).grid(row=3, column=1, sticky="ew")
        
        behavior_frame.columnconfigure(1, weight=1)

        appearance_frame = ttk.LabelFrame(main_frame, text="Appearance & Content", padding="10")
        appearance_frame.pack(pady=10, fill=tk.X, expand=True)

        ttk.Label(appearance_frame, text="Font Size (10-100):").grid(row=0, column=0, sticky="w", pady=5)
        self.font_size = tk.IntVar(value=self.settings.get("font_size"))
        ttk.Scale(appearance_frame, from_=10, to=100, variable=self.font_size, orient=tk.HORIZONTAL, 
            command=lambda v: self.settings.set("font_size", int(float(v)))).grid(row=0, column=1, sticky="ew")

        self.color_button = ttk.Button(appearance_frame, text="Change Text Color", command=self.change_text_color)
        self.color_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.import_button = ttk.Button(appearance_frame, text="Import Messages", command=self.import_messages)
        self.import_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.image_button = ttk.Button(appearance_frame, text="Select Image", command=self.select_image)
        self.image_button.grid(row=3, column=0, columnspan=2, pady=10)

        appearance_frame.columnconfigure(1, weight=1)

        # --- Test Mode Controls ---
        test_frame = ttk.LabelFrame(main_frame, text="Test Mode", padding="10")
        test_frame.pack(pady=10, fill=tk.X, expand=True)

        self.test_mode_var = tk.BooleanVar(value=self.settings.get("test_mode"))
        self.test_mode_check = tk.Checkbutton(
            test_frame, 
            text="Enable Test Mode (Messages Visible)", 
            variable=self.test_mode_var,
            command=self._toggle_test_mode,
            bg="#2E2E2E",
            fg="white",
            selectcolor="#555555",
            font=("Helvetica", 10)
        )
        self.test_mode_check.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

        ttk.Label(test_frame, text="Display Time (s, 1-10):").grid(row=1, column=0, sticky="w", pady=5)
        self.test_display_time = tk.IntVar(value=self.settings.get("test_display_seconds"))
        test_scale = ttk.Scale(test_frame, from_=1, to=10, variable=self.test_display_time, orient=tk.HORIZONTAL, 
                      command=lambda v: self.settings.set("test_display_seconds", int(float(v)))
        )
        test_scale.grid(row=1, column=1, sticky="ew")

        test_frame.columnconfigure(1, weight=1)
    def select_image(self):
        filepath = filedialog.askopenfilename(
            title="Select Image",
            filetypes=(
                ("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
                ("All files", "*.*")
            )
        )
        if filepath:
            self.flasher.image_path = filepath
            print(f"Image selected: {filepath}")

    def import_messages(self):
        filepath = filedialog.askopenfilename(
            title="Open Text File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    messages = [line.strip() for line in f if line.strip()]
                    if messages:
                        self.flasher.message_pool = messages
                        self.flasher._shuffle_pool()
            except Exception as e:
                print(f"Error importing file: {e}")

    def change_text_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code and color_code[1]:
            self.settings.set("font_color", color_code[1])

    def toggle_flasher(self):
        if self.flasher.is_running:
            self.flasher.stop()
            self.start_stop_button.config(text="Start", style="green.TButton")
        else:
            # Apply settings before starting
            self.settings.set("batch_size", self.batch_size.get())
            self.settings.set("flash_duration_ms", self.flash_duration.get())
            self.settings.set("interval_seconds", self.interval.get())
            self.settings.set("margin_px", self.margin.get())
            self.settings.set("font_size", self.font_size.get())
            self.settings.set("test_mode", self.test_mode_var.get())
            self.settings.set("test_display_seconds", self.test_display_time.get())
            
            # Debug output
            print(f"Settings applied:")
            print(f"  Batch Size: {self.settings.get('batch_size')}")
            print(f"  Flash Duration: {self.settings.get('flash_duration_ms')}ms")
            print(f"  Interval: {self.settings.get('interval_seconds')}s")
            print(f"  Margin: {self.settings.get('margin_px')}px")
            print(f"  Font Size: {self.settings.get('font_size')}")
            print(f"  Test Mode: {self.settings.get('test_mode')}")
            print(f"  Test Display Time: {self.settings.get('test_display_seconds')}s")
            print(f"  Font Color: {self.settings.get('font_color')}")
            
            self.flasher.start()
            self.start_stop_button.config(text="Stop", style="red.TButton")

    def _toggle_test_mode(self):
        """Toggle between test mode and subliminal mode"""
        test_mode = self.test_mode_var.get()
        self.settings.set("test_mode", test_mode)
        
        if test_mode:
            # In test mode, make messages clearly visible
            print("Test mode enabled - messages will be clearly visible")
            self.title("Subliminal Master - TEST MODE (Messages Visible)")
            # Ensure longer display time for visibility
            if self.test_display_time.get() < 2:
                self.test_display_time.set(2)
                self.settings.set("test_display_seconds", 2)
        else:
            print("Test mode disabled - returning to subliminal mode")
            self.title("Subliminal Master")

    def _on_closing(self):
        self.flasher.stop()
        self.destroy()

if __name__ == "__main__":
    app_settings = Settings()
    app = App(app_settings)
    app.mainloop()
