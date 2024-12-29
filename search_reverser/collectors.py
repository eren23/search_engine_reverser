from typing import Dict, List
import requests
from time import sleep


class DataCollector:
    def __init__(self):
        self.session = requests.Session()

    def generate_test_cases(self) -> List[Dict]:
        """Generate a comprehensive set of test cases"""
        return [
            {"query": "exact term", "type": "exact"},
            {"query": "partial ter", "type": "partial"},
            {"query": "misspeled term", "type": "fuzzy"},
            {"query": "term exact", "type": "word_order"},
            {"query": "UPPER CASE", "type": "case_sensitivity"},
            {"query": "special!@#$", "type": "special_chars"},
        ]

    def perform_search(self, target_url: str, query: str) -> List[Dict]:
        """Perform a search request and return results"""
        try:
            response = self.session.get(target_url, params={"q": query}, headers={"User-Agent": "SearchReverseEngineer/1.0", "Accept": "application/json"})
            response.raise_for_status()
            sleep(1)  # Respect rate limits
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error performing search: {e}")
            return []
