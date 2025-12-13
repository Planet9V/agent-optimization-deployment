import csv
import json
import time
import sys

# Standard Schema Structure
def create_entity(entity_id, entity_type, name, data_points):
    return {
        "id": entity_id,
        "type": entity_type,
        "name": name,
        "parent_id": None,
        "attributes": data_points
    }

def ingest_csv(file_path, id_col, name_col, mapping_config):
    """
    Ingests a CSV file and maps columns to the standard schema using a config.
    mapping_config: dict { "csv_col_name": "metric_key" }
    """
    entities = []
    
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                entity_id = row.get(id_col)
                name = row.get(name_col, "Unknown")
                
                if not entity_id:
                    continue
                
                data_points = []
                for csv_col, metric_key in mapping_config.items():
                    if csv_col in row and row[csv_col]:
                        try:
                            val = float(row[csv_col])
                        except ValueError:
                            val = row[csv_col]

                        data_points.append({
                            "metric": metric_key,
                            "value": val,
                            "year": 2022, # Defaulting for static datasets
                            "source": f"Kaggle CSV: {file_path}",
                            "timestamp": time.time()
                        })
                
                entities.append(create_entity(
                    entity_id=f"kaggle:{entity_id}",
                    entity_type="PsychometricProfile",
                    name=name,
                    data_points=data_points
                ))
                
        return entities
        
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

if __name__ == "__main__":
    # Example Usage for Big Five Dataset (Hypothetical columns)
    # python parse_csv_data.py data/big_five.csv
    
    if len(sys.argv) < 2:
        print("Usage: python parse_csv_data.py <path_to_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]
    
    # Configuration for a hypothetical Big Five dataset
    # You would adjust this map based on the specific CSV header
    config = {
        "O_score": "openness",
        "C_score": "conscientiousness",
        "E_score": "extraversion",
        "A_score": "agreeableness",
        "N_score": "neuroticism",
        "age": "demographic_age",
        "country": "demographic_country"
    }

    # Assuming 'case_id' is the unique identifier column in the CSV
    result = ingest_csv(input_csv, id_col="case_id", name_col="case_id", mapping_config=config)
    
    if result:
        output_file = "kaggle_psychometric_data.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Converted {len(result)} rows to {output_file}")
    else:
        print("No data converted.")
