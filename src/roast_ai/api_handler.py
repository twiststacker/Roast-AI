import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()

class RiotAPI:
    def __init__(self):
        # 🔑 Privacy Layer: If no key is found, we use Demo Mode
        self.api_key = os.getenv("RIOT_API_KEY")
        self.region = os.getenv("REGION", "na1")
        
        # Detection logic
        self.is_demo = not self.api_key or "RGAPI" not in self.api_key
        
        # Americas routing for real NA1/BR/LAN calls
        self.route = "americas" if self.region in ["na1", "br1", "la1", "la2"] else "europe"

    def get_summoner_data(self, name_with_tag):
        """Fetches profile. Uses Mock data if in Demo Mode."""
        if self.is_demo:
            return {
                "puuid": f"MOCK_USER_{random.randint(100,999)}", 
                "gameName": name_with_tag.split("#")[0]
            }
        
        try:
            name, tag = name_with_tag.split("#")
            url = f"https://{self.route}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
            headers = {"X-Riot-Token": self.api_key}
            response = requests.get(url, headers=headers)
            return response.json() if response.status_code == 200 else {"error": f"RIOT_ERR_{response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def get_recent_matches(self, puuid, count=5):
        """Fetches match IDs. Uses fake IDs if in Demo Mode."""
        if self.is_demo:
            # Fake IDs give the AI something to 'look at'
            return [f"SIM_MATCH_{random.randint(1000, 9999)}" for _ in range(count)]
            
        url = f"https://{self.route}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
        headers = {"X-Riot-Token": self.api_key}
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else []