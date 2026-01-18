import sys
import os

# Ensure absolute imports work by adding root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from src.roast_ai.gui.app import RoastApp

def main():
    try:
        app = RoastApp()
        app.mainloop()
    except Exception as e:
        print(f"CRITICAL_STARTUP_ERROR: {e}")

if __name__ == "__main__":
    main()