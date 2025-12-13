import urllib.request
import json
import time
from typing import List, Dict, Any

# --- Schema Definition ---
# Nodes will represent Entities (Countries, Regions) or MetricSnapshots.
# Edges are implicit in the structure or can be extracted.

class StandardizedDemographicEntity:
    def __init__(self, entity_type: str, entity_id: str, name: str, parent_id: str = None):
        self.id = entity_id
        self.type = entity_type
        self.name = name
        self.parent_id = parent_id
        self.data_points = []

    def add_data_point(self, key: str, value: Any, year: int, source: str):
        self.data_points.append({
            "metric": key,
            "value": value,
            "year": year,
            "source": source,
            "timestamp": time.time()
        })

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "parent_id": self.parent_id,
            "attributes": self.data_points
        }

# --- Data Fetchers ---

class WorldBankFetcher:
    BASE_URL = "https://api.worldbank.org/v2"

    def fetch_indicator(self, indicator_code: str, country_code: str = "all", year: str = "2022") -> List[Dict]:
        """
        Generic fetcher for any World Bank indicator.
        """
        url = f"{self.BASE_URL}/country/{country_code}/indicator/{indicator_code}?date={year}&format=json&per_page=500"
        
        print(f"Fetching {indicator_code} from: {url}")
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
            
            if not isinstance(data, list) or len(data) < 2:
                print(f"No data found for {indicator_code}.")
                return []
                
            return data[1]
        except Exception as e:
            print(f"Error fetching {indicator_code}: {e}")
            return []

# --- Ingestion Orchestrator ---

def run_ingestion():
    wb_fetcher = WorldBankFetcher()
    
    # Define indicators to fetch
    indicators = {
        "population_total": "SP.POP.TOTL",
        "gdp_per_capita": "NY.GDP.PCAP.CD",
        "internet_usage_percent": "IT.NET.USER.ZS",
        "literacy_rate_adult_total": "SE.ADT.LITR.ZS",
        "life_expectancy_total": "SP.DYN.LE00.IN",
        "unemployment_total": "SL.UEM.TOTL.ZS"
    }

    # Dictionary to aggregate data by country ID
    # Format: { "wb:USA": StandardizedDemographicEntity object }
    entities_map = {}
    
    for metric_name, indicator_code in indicators.items():
        raw_data = wb_fetcher.fetch_indicator(indicator_code, year="2022")
        print(f"Processing {len(raw_data)} records for {metric_name}...")
        
        for record in raw_data:
            if not record.get('country') or record.get('value') is None:
                continue
                
            country_info = record['country']
            entity_id = f"wb:{country_info['id']}"
            
            # Initialize entity if not exists
            if entity_id not in entities_map:
                entities_map[entity_id] = StandardizedDemographicEntity(
                    entity_type="GeographicRegion",
                    entity_id=entity_id,
                    name=country_info['value']
                )
            
            # Add data point
            entities_map[entity_id].add_data_point(
                key=metric_name,
                value=record['value'],
                year=int(record['date']),
                source=f"World Bank ({indicator_code})"
            )

    normalized_entities = [e.to_dict() for e in entities_map.values()]

    # Outut details
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "data")
    os.makedirs(output_dir, exist_ok=True)
    
    output_filename = os.path.join(output_dir, "demographic_knowledge_graph_data.json")
    with open(output_filename, "w") as f:
        json.dump(normalized_entities, f, indent=2)
    
    print(f"Successfully exported {len(normalized_entities)} standardized entities to {output_filename}")

if __name__ == "__main__":
    run_ingestion()
