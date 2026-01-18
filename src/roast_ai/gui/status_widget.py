import customtkinter as ctk

class StatusRing(ctk.CTkCanvas):
    """
    A custom Hextech-themed status indicator ring that changes color 
    based on the current phase of the 'Hunt'.
    """
    def __init__(self, master, **kwargs):
        # highlightthickness=0 removes the default border around the canvas
        # bg matches the dark theme background to avoid the 'black box' effect
        super().__init__(
            master, 
            width=40, 
            height=40, 
            bg="#1A1A1A", 
            highlightthickness=0, 
            **kwargs
        )
        
        # Create the initial cyan ring (Hextech Idle/Hunting state)
        self.ring = self.create_oval(
            5, 5, 35, 35, 
            outline="#00FFFF", 
            width=3
        )

    def set_status(self, status):
        """
        Updates the ring's color to provide visual feedback to the user.
        
        Args:
            status (str): The current state ('idle', 'hunting', 'thinking', 'complete')
        """
        # Hextech Color Palette:
        # - Cyan (#00FFFF): Active Hunt / Idle
        # - Purple (#BF00FF): AI Processing (Thinking)
        # - Green (#00FF00): Success (Roast Complete)
        colors = {
            "idle": "#00FFFF", 
            "hunting": "#00FFFF", 
            "thinking": "#BF00FF", 
            "complete": "#00FF00"
        }
        
        new_color = colors.get(status, "#00FFFF")
        self.itemconfig(self.ring, outline=new_color)