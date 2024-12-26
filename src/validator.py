from jsonschema import validate, ValidationError

class SarifValidator:
    def __init__(self, schema):
        self.schema = schema

    def validate_sarif(self, sarif_content):
        """Validates SARIF content against the schema."""
        try:
            validate(instance=sarif_content, schema=self.schema)
        except ValidationError as e:
            raise ValueError(f"Invalid SARIF file: {e.message}")