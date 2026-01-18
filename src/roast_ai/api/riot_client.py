import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

class RiotClient:
    def __init__(self):
        self.api_key = os.getenv("RIOT_API_KEY")
        self.headers = {"X-Riot-Token": self.api_key}
        self.region_url = "https://europe.api.riotgames.com"

    def get_match_ids(self, puuid: str, count: int = 5):
        """Just gets the 'Index Cards' for the matches."""
        url = f"{self.region_url}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else []

    def get_match_detail(self, match_id: str):
        """Opens the 'Book' to see the full scoreboard."""
        url = f"{self.region_url}/lol/match/v5/matches/{match_id}"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None