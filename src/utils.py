import json
from pathlib import Path

SARIF_SCHEMA_URL = "https://docs.oasis-open.org/sarif/sarif/v2.1.0/cs01/schemas/sarif-schema-2.1.0.json"
SCHEMA_LOCAL_PATH = Path("sarif-schema-2.1.0.json")

class SchemaLoader:
    @staticmethod
    def load_schema():
        """Loads the SARIF schema from a local file or URL."""
        if SCHEMA_LOCAL_PATH.exists():
            with open(SCHEMA_LOCAL_PATH, 'r') as file:
                return json.load(file)
        else:
            raise FileNotFoundError(f"SARIF schema file not found at {SCHEMA_LOCAL_PATH}")