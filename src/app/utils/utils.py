import json
from pathlib import Path

def load_schema(schema_provider: str):
    """Loads the SARIF schema from a local file (Input options: OASIS_SCHEMA or SARD_SCHEMA)."""
    
    OASIS_SCHEMA_LOCAL_PATH = Path("src/schema/sarif-schema-2.1.0.json")
    SARD_SCHEMA_LOCAL_PATH = Path("src/schema/sard-schema.json")
    
    try:
        if schema_provider == "OASIS_SCHEMA":
            return load_file(OASIS_SCHEMA_LOCAL_PATH)
        elif schema_provider == "SARD_SCHEMA":
            return load_file(SARD_SCHEMA_LOCAL_PATH)
        else:
            raise ValueError("Invalid schema provider. Use 'OASIS_SCHEMA' or 'SARD_SCHEMA'.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    
def load_file(file_path: str):
    """Loads the content of a file."""
    file = Path(file_path)
    if file.exists():
        with open(file, 'r') as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"File not found at {file_path}")