import json
import os
from pathlib import Path
from app.utils.utils import load_schema, load_file
from app.validator import validate_sarif
from app.utils.banner import print_banner

def main():
    # File paths
    input_sarif_path = "input.sarif"
    output_md_path = "output.md"

    # Initialize components
    schema = load_schema("OASIS_SCHEMA")
    content = load_file("input.sarif")
    print(content)
    #validator = validate_sarif(schema, )
    #md_generator = MarkdownGenerator()

    # Tool execution
    #tool = SarifToMarkdownTool(validator, md_generator)
    #tool.process_sarif(input_sarif_path, output_md_path)

if __name__ == '__main__':
    main()
    