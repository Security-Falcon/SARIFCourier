from jsonschema import validate, ValidationError
from termcolor import colored
from utils import load_schema
import os
import json


def validate_sarif(sarif_content):
    """Validates SARIF content against the schema."""
    try:
        OASIS_SCHEMA = load_schema("OASIS_SCHEMA")

        validate(instance=sarif_content, schema=OASIS_SCHEMA)
        print(colored("Successfully Validated Input against OASIS Schema ✅", "green"))
    except ValidationError as e:
        raise ValueError(f"Invalid SARIF file: {e.message}")