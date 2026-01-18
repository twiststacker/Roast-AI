import requests

class RoastEngine:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate" 

    def generate_roast(self, target_name, match_data):
        """Generates the savage roast seen in your screenshot"""
        prompt = f"Target: {target_name}. Data: {match_data}. Task: Write a savage 3-sentence League of Legends roast."
        data = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.api_url, json=data, timeout=60)
            return response.json().get('response', "AI_SILENT") if response.status_code == 200 else "AI_OFFLINE"
        except Exception:
            return "CONNECTION_FAILURE: IS_OLLAMA_RUNNING?"