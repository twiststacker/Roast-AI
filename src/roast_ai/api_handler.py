import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()

class RiotAPI:
    def __init__(self):
        self.api_key = os.getenv("RIOT_API_KEY")
        # Automatically enter Demo Mode if key is missing
        self.is_demo = not self.api_key or "RGAPI" not in self.api_key
        self.region = os.getenv("REGION", "na1")
        self.route = "americas" if self.region in ["na1", "br1", "la1", "la2"] else "europe"

    def get_summoner_data(self, name_with_tag):
        if self.is_demo:
            return {"puuid": "MOCK_ID_999", "gameName": name_with_tag.split("#")[0]}
        
        try:
            name, tag = name_with_tag.split("#")
            url = f"https://{self.route}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
            headers = {"X-Riot-Token": self.api_key}
            response = requests.get(url, headers=headers)
            return response.json() if response.status_code == 200 else {"error": f"CODE_{response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def get_recent_matches(self, puuid, count=5):
        if self.is_demo:
            return [f"SIM_MATCH_{random.randint(1000, 9999)}" for _ in range(count)]
        
        url = f"https://{self.route}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
        headers = {"X-Riot-Token": self.api_key}
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else []