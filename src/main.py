import json
import os
from pathlib import Path
from utils import SchemaLoader
from validator import SarifValidator
from Converter import MarkdownGenerator

class SarifToMarkdownTool:
    def __init__(self, validator, md_generator):
        self.validator = validator
        self.md_generator = md_generator

    def process_sarif(self, sarif_file_path, output_md_path):
        """Processes the SARIF file and outputs Markdown."""
        if not os.path.exists(sarif_file_path):
            raise FileNotFoundError(f"SARIF file not found: {sarif_file_path}")

        with open(sarif_file_path, 'r') as sarif_file:
            sarif_content = json.load(sarif_file)

        # Validate SARIF
        self.validator.validate_sarif(sarif_content)

        # Generate Markdown
        md_content = self.md_generator.generate(sarif_content)

        # Save Markdown to file
        with open(output_md_path, 'w') as md_file:
            md_file.write(md_content)

        print(f"Markdown report successfully generated at: {output_md_path}")

if __name__ == "__main__":
    # File paths
    input_sarif_path = "input.sarif"
    output_md_path = "output.md"

    # Initialize components
    schema_loader = SchemaLoader()
    schema = schema_loader.load_schema()
    validator = SarifValidator(schema)
    md_generator = MarkdownGenerator()

    # Tool execution
    tool = SarifToMarkdownTool(validator, md_generator)
    tool.process_sarif(input_sarif_path, output_md_path)