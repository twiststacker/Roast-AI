import math
import os
import sys
import threading
from PIL import Image
import customtkinter as ctk

# Absolute imports for stability
from src.roast_ai.gui.status_widget import StatusRing
from src.roast_ai.api_handler import RiotAPI
from src.roast_ai.roast_engine import RoastEngine

def resource_path(relative_path):
    """ PyInstaller helper for assets """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class RoastApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.api = RiotAPI()
        self.roaster = RoastEngine()
        
        # Window Configuration
        self.title("GG Ai: THE_HUNT")
        self.geometry("1200x800")
        ctk.set_appearance_mode("dark")
        
        # 🖼️ Layer 0: Background Image (Bottom Layer)
        bg_path = resource_path("assets/bg.png")
        if os.path.exists(bg_path):
            img = Image.open(bg_path)
            self.bg_image = ctk.CTkImage(light_image=img, dark_image=img, size=(1200, 800))
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.rings = []
        self._setup_ui()
        
        # ⌨️ Key Binding: Hit 'Enter' to start the hunt
        self.bind('<Return>', lambda event: self.on_hunt_click())

    def _setup_ui(self):
        # 🕹️ Layer 1: Top-Middle Search Bar
        # We use relx=0.5 and rely=0.1 to keep it centered at the top
        self.summoner_entry = ctk.CTkEntry(self, 
                                            placeholder_text="Enter Riot ID (Name#Tag)", 
                                            width=500, height=50,
                                            border_color="#00FFFF", 
                                            fg_color="#1A1A1A",
                                            font=("Helvetica", 18, "bold"))
        self.summoner_entry.place(relx=0.5, rely=0.1, anchor="n")

        # 📟 Layer 1: Terminal (Pinned to the Right)
        # We use relx=0.95 to keep it on the far right edge
        self.terminal = ctk.CTkTextbox(self, width=380, height=550, 
                                        font=("Courier New", 13),
                                        fg_color=("#1A1A1A", "#080808"),
                                        border_color="#00FFFF", border_width=1,
                                        activate_scrollbars=True)
        self.terminal.place(relx=0.97, rely=0.5, anchor="e")
        self.write_to_terminal("SYSTEM_ONLINE: READY_FOR_HUNT")

        # ⭕ Layer 1: Central Hextech Button & Rings
        self.center_container = ctk.CTkFrame(self, fg_color="transparent")
        self.center_container.place(relx=0.4, rely=0.55, anchor="center")
        
        self.hunt_button = ctk.CTkButton(self.center_container, text="INITIATE\nHUNT", 
                                        width=200, height=200, corner_radius=100,
                                        fg_color="transparent", border_color="#00FFFF", 
                                        border_width=2, hover_color="#003333",
                                        font=("Impact", 26),
                                        command=self.on_hunt_click)
        self.hunt_button.pack()
        
        self._create_circular_status_rings()

    def _create_circular_status_rings(self):
        """Positions rings around the central button without overlapping"""
        radius = 170
        for i in range(5):
            angle = math.radians(i * 72 - 90)
            x_offset = radius * math.cos(angle)
            y_offset = radius * math.sin(angle)
            ring = StatusRing(self.center_container)
            ring.place(relx=0.5, rely=0.5, x=x_offset, y=y_offset, anchor="center")
            self.rings.append(ring)

    def write_to_terminal(self, msg):
        self.terminal.insert("end", f"> {msg}\n")
        self.terminal.see("end")

    def on_hunt_click(self):
        target = self.summoner_entry.get()
        if "#" not in target:
            self.write_to_terminal("ERROR: INVALID_FORMAT. USE NAME#TAG")
            return
            
        self.write_to_terminal(f"HUNT_START: {target}")
        for r in self.rings: r.set_status("hunting")
        threading.Thread(target=self._run_hunt_logic, args=(target,), daemon=True).start()

    def _run_hunt_logic(self, target):
        try:
            self.after(0, lambda: self.write_to_terminal("STEP_1: SCANNING_RIOT_DATA..."))
            player = self.api.get_summoner_data(target)
            if "error" in player:
                self.after(0, lambda: self.write_to_terminal(f"FAIL: {player['error']}"))
                return
            
            self.after(0, lambda: self.write_to_terminal("STEP_2: ANALYZING_MATCHES..."))
            matches = self.api.get_recent_matches(player.get("puuid"))
            
            self.after(0, lambda: [r.set_status("thinking") for r in self.rings])
            self.after(0, lambda: self.write_to_terminal("STEP_3: GENERATING_AI_ROAST..."))
            roast = self.roaster.generate_roast(target, matches)
            
            self.after(0, lambda: self.write_to_terminal(f"\nRESULT:\n{roast}\n"))
            self.after(0, lambda: [r.set_status("complete") for r in self.rings])
        except Exception as e:
            self.after(0, lambda: self.write_to_terminal(f"CRASH: {e}"))