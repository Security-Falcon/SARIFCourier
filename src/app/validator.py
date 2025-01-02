
from jsonschema import validate, ValidationError
from termcolor import colored


def validate_sarif(schema, sarif_content):
    """Validates SARIF content against the schema."""
    try:
        validate(instance=sarif_content, schema=schema)
        print(colored("SARIF file is valid. ✅", "green"))
    except ValidationError as e:
        raise ValueError(f"Invalid SARIF file: {e.message}")