import os
import requests
import json
import time

class CensusFetcher:
    BASE_URL = "https://api.census.gov/data/2022/acs/acs5/profile"
    
    def __init__(self):
        self.api_key = os.environ.get("CENSUS_API_KEY")
        if not self.api_key:
            print("WARNING: CENSUS_API_KEY environment variable not set. Fetching will likely fail.")

    def fetch_acs_profile(self, state_code="*"):
        """
        Fetches American Community Survey (ACS) 5-Year Data Profile.
        Variable Groups:
        - DP02: Selected Social Characteristics
        - DP03: Selected Economic Characteristics
        - DP04: Selected Housing Characteristics
        - DP05: Demographic and Housing Estimates
        """
        if not self.api_key:
            return []

        # Example: Fetch Total Population (DP05_0001E) for all states
        params = {
            "get": "NAME,DP05_0001E",
            "for": f"state:{state_code}",
            "key": self.api_key
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching Census data: {e}")
            return []

if __name__ == "__main__":
    print("--- US Census Data Fetcher ---")
    fetcher = CensusFetcher()
    data = fetcher.fetch_acs_profile()
    if data:
        print(f"Successfully fetched {len(data)} records (including header).")
        # Print first few rows
        for row in data[:5]:
            print(row)
    else:
        print("No data fetched. Check API key.")
