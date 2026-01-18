import os
import requests
from dotenv import load_dotenv

load_dotenv()

class RoastEngine:
    def __init__(self):
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        self.ollama_url = "http://localhost:11434/api/generate"

    def _call_ollama(self, prompt: str):
        """Attempts local generation via Ollama (Free/Private)."""
        try:
            payload = {"model": "llama3", "prompt": prompt, "stream": False}
            response = requests.post(self.ollama_url, json=payload, timeout=5)
            return response.json().get("response")
        except Exception:
            return None

    def _call_deepseek(self, prompt: str):
        """Cloud fallback using DeepSeek API."""
        # Logic for DeepSeek API request would go here
        return "DeepSeek Fallback: You played like a bot."

    def generate_roast(self, match_truth):
        """Processes the Truth Package into Gamer Language."""
        # Formulate the 'Brutal' prompt
        prompt = (f"Analyze this League match: {match_truth}. "
                  "Focus on the 3-minute weakest link and map awareness. "
                  "Use direct gamer language. Be brutally honest.")
        
        # 1. Try Local
        roast = self._call_ollama(prompt)
        
        # 2. Fallback to Cloud
        if not roast:
            roast = self._call_deepseek(prompt)
            
        return roast