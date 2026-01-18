# --- Standard Library Imports ---
import math
import os
import sys
import threading
import gc

# --- Third-Party Library Imports ---
from PIL import Image
import customtkinter as ctk

# Safe Pygame-ce Import
try:
    import pygame
    PYGAME_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    PYGAME_AVAILABLE = False

# --- Project Imports ---
from src.roast_ai.gui.status_widget import StatusRing
from src.roast_ai.api_handler import RiotAPI
from src.roast_ai.roast_engine import RoastEngine

def resource_path(relative_path):
    """ Get absolute path to resource for local and compiled runs """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class RoastApp(ctk.CTk):
    def __init__(self):
        # 1. INITIALIZE CTk CLASS FIRST (Fixes startup error)
        super().__init__()
        
        # 2. AUDIO ENGINE SETUP
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
            except Exception as e:
                print(f"Audio Driver Error: {e}")
        
        # 3. CORE ATTRIBUTES
        self.api = RiotAPI()
        self.roaster = RoastEngine()
        self.volume = 0.5
        self.is_muted = False
        
        # 4. WINDOW CONFIG
        self.title("GG Ai: THE_HUNT")
        self.geometry("1200x800")
        ctk.set_appearance_mode("dark")
        
        # 5. BACKGROUND LAYER
        bg_p = resource_path("assets/bg.png")
        if os.path.exists(bg_p):
            img = ctk.CTkImage(Image.open(bg_p), size=(1200, 800))
            self.bg_label = ctk.CTkLabel(self, image=img, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.rings = []
        self._setup_ui()
        
        # 6. KEY BINDING
        self.bind('<Return>', lambda e: self.on_hunt_click())

    def _setup_ui(self):
        """Builds the UI using relative coordinates to match project layout"""
        
        # --- Search Bar (Top-Middle) ---
        self.entry = ctk.CTkEntry(self, width=500, height=50, 
                                  placeholder_text="SUMMONER#TAG", 
                                  border_color="#00FFFF", fg_color="#0D0D0D")
        self.entry.place(relx=0.5, rely=0.1, anchor="n")

        # --- Audio Cluster (Top-Right) ---
        self.mute_btn = ctk.CTkButton(self, text="🔊", width=40, height=40,
                                      fg_color="transparent", border_color="#00FFFF", 
                                      border_width=1, command=self.toggle_mute)
        self.mute_btn.place(relx=0.97, rely=0.03, anchor="ne")
        
        self.vol_slider = ctk.CTkSlider(self, from_=0, to=1, width=120, command=self.set_volume)
        self.vol_slider.set(self.volume)
        self.vol_slider.place(relx=0.92, rely=0.045, anchor="ne")

        # --- Terminal (Pinned Right) ---
        self.terminal = ctk.CTkTextbox(self, width=380, height=550, 
                                       fg_color="#080808", border_color="#00FFFF", 
                                       border_width=1, font=("Courier New", 13))
        self.terminal.place(relx=0.97, rely=0.5, anchor="e")

        # --- Central Button & Rings ---
        self.hunt_btn = ctk.CTkButton(self, text="INITIATE\nHUNT", 
                                      width=200, height=200, corner_radius=100, 
                                      border_color="#00FFFF", border_width=2, 
                                      fg_color="transparent", font=("Impact", 24), 
                                      command=self.on_hunt_click)
        self.hunt_btn.place(relx=0.4, rely=0.55, anchor="center")

        self._create_rings()

    def _create_rings(self):
        """Positions pulsing rings around the central button"""
        radius = 170
        for i in range(5):
            angle = math.radians(i * 72 - 90)
            x, y = radius * math.cos(angle), radius * math.sin(angle)
            ring = StatusRing(self)
            # Use same relx/rely as button to center the orbit
            ring.place(relx=0.4, rely=0.55, x=x, y=y, anchor="center")
            self.rings.append(ring)

    def toggle_mute(self):
        """Switches audio state and updates button visuals"""
        self.is_muted = not self.is_muted
        self.mute_btn.configure(text="🔇" if self.is_muted else "🔊", 
                                border_color="#FF4444" if self.is_muted else "#00FFFF")

    def set_volume(self, v): 
        self.volume = float(v)

    def write_to_terminal(self, msg):
        self.terminal.insert("end", f"> {msg}\n")
        self.terminal.see("end")

    def on_hunt_click(self):
        """Triggers the search and roasting logic"""
        target = self.entry.get()
        if "#" not in target:
            self.write_to_terminal("ERR: INVALID_FORMAT. USE NAME#TAG")
            return
        
        # UI Status Update
        for r in self.rings: r.set_status("hunting")
        
        # Audio feedback on initiate
        self._play_feedback()
        
        threading.Thread(target=self._run_hunt, args=(target,), daemon=True).start()

    def _play_feedback(self):
        """Handles audio playback via pygame mixer"""
        if PYGAME_AVAILABLE and not self.is_muted and self.volume > 0:
            sound_p = resource_path("assets/sounds/finish.wav")
            if os.path.exists(sound_p):
                try:
                    if not pygame.mixer.get_init(): pygame.mixer.init()
                    s = pygame.mixer.Sound(sound_p)
                    s.set_volume(self.volume)
                    s.play()
                except: pass

    def _run_hunt(self, target):
        """Processes target data and retrieves the AI roast"""
        try:
            self.after(0, lambda: self.write_to_terminal(f"HUNT_START: {target}"))
            data = self.api.get_summoner_data(target)
            matches = self.api.get_recent_matches(data.get("puuid"))
            
            self.after(0, lambda: [r.set_status("thinking") for r in self.rings])
            roast = self.roaster.generate_roast(target, matches)
            
            self.after(0, lambda: self.write_to_terminal(f"RESULT: {roast}"))
            self.after(0, lambda: [r.set_status("complete") for r in self.rings])
            
            # Memory Cleanup
            gc.collect() 
        except Exception as e:
            self.after(0, lambda: self.write_to_terminal(f"CRASH: {e}"))