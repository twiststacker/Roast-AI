import os
import sys

def resource_path(relative_path):
    """
    Finds the absolute path to resources for both 
    development and PyInstaller 'frozen' states.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)