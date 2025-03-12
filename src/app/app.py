import json
import os
from pathlib import Path
from app.utils.utils import load_schema, load_file
from app.validator import validate_sarif
from app.utils.banner import print_banner
from app.converter import convert
import argparse
from termcolor import colored

def main():
    parser = argparse.ArgumentParser(description='Convert SARIF to Markdown.')
    parser.add_argument('--sarif-input', '-si', required=True, help='Path to the input SARIF file')
    parser.add_argument('--output-file-name', '-ofn', required=False, help='Name of output Markdown file. Default: sarif-2-md-output.md')
    args = parser.parse_args()

    input_sarif_path = os.path.abspath(args.sarif_input)
    if not input_sarif_path.startswith(os.getcwd()):
        raise ValueError("Invalid input file path")
    output_md_name = f"{args.output_file_name}.md" if args.output_file_name else 'sarif-2-md-output.md'
   
    content = load_file(input_sarif_path)
    validate_sarif(content)
    md_content = convert(content)
    print(colored(f"Successfully Converted SARIF to MD ✅", "green"))
    
    output_md_path = os.path.join(os.path.dirname(input_sarif_path), output_md_name)
    with open(output_md_path, 'w') as output_file:
        output_file.write(md_content)
    print(colored(f"Markdown content was written to {output_md_path} ✅", "green"))

if __name__ == '__main__':
    main()
    