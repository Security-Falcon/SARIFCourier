
from jsonschema import validate, ValidationError
from termcolor import colored
from app.utils.utils import load_schema


def validate_sarif(sarif_content):
    """Validates SARIF content against the schema."""
    try:
        OASIS_SCHEMA = load_schema("OASIS_SCHEMA")
        #SARD_SCHEMA = load_schema("SARD_SCHEMA")

        validate(instance=sarif_content, schema=OASIS_SCHEMA)
        print(colored("Successfully Validated Input against OASIS Schema ✅", "green"))
        
        # TODO: Enable Validation against SARD Schema
        #validate(instance=sarif_content, schema=SARD_SCHEMA)
        #print(colored("Successfully Validated Input against SARD Schema ✅", "green"))
    except ValidationError as e:
        raise ValueError(f"Invalid SARIF file: {e.message}")