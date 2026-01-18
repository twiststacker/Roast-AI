import requests

class RoastEngine:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate" 

    def generate_roast(self, target_name, match_data):
        prompt = f"Target: {target_name}. Match History: {match_data}. Task: Write a savage 2-sentence League of Legends roast."
        data = {"model": "llama3", "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.api_url, json=data, timeout=30)
            return response.json().get('response', "AI_SILENT")
        except:
            return "ERROR: Is Ollama running with Llama3?"