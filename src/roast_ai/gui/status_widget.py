import customtkinter as ctk

class StatusRing(ctk.CTkCanvas):
    """Circular status indicator for the Hextech Dashboard"""
    def __init__(self, master, **kwargs):
        super().__init__(master, width=40, height=40, bg="#1A1A1A", 
                         highlightthickness=0, **kwargs)
        
        # Initial State: Dim Gray ring
        self.ring = self.create_oval(5, 5, 35, 35, outline="#333333", width=3)
        self.status = "idle"

    def set_status(self, status):
        """Updates the visual state of the ring based on app progress"""
        self.status = status
        
        if status == "hunting":
            self.itemconfig(self.ring, outline="#00FFFF") # Cyan for scanning
        
        elif status == "thinking":
            self.itemconfig(self.ring, outline="#FF00FF") # Neon Purple for AI processing
            self._pulse()
            
        elif status == "complete":
            self.itemconfig(self.ring, outline="#00FF00") # Green for success
            
    def _pulse(self):
        """Internal animation loop to show the AI is working"""
        if self.status == "thinking":
            current_color = self.itemcget(self.ring, "outline")
            # Alternate between bright and dim purple
            new_color = "#550055" if current_color == "#FF00FF" else "#FF00FF"
            self.itemconfig(self.ring, outline=new_color)
            self.after(500, self._pulse)