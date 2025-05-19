import argparse
import json
import os
from utils import load_file
from validator import validate_sarif
from converter import convert
from banner import print_banner
from github_commenter import GitHubPRCommenter


def main():
    parser = argparse.ArgumentParser(description='Makes your SARIF reports more readable')
    parser.add_argument('--sarif', required=True, help='Path to SARIF report')
    parser.add_argument('--local', action='store_true', help='Output markdown summary locally instead of posting to GitHub')
    parser.add_argument('--output-file-name', '-ofn', required=False, help='Name of output Markdown file. Default: sarif-2-md-output.md')
    args = parser.parse_args()

    sarif_path = os.path.abspath(args.sarif)
    if not os.path.exists(sarif_path):
        raise ValueError(f"SARIF file not found: {sarif_path}")
    
    sarif_data = load_file(sarif_path)
    validate_sarif(sarif_data)
    md_content = convert(sarif_data)

    if args.local:
        output_md_name = f"{args.output_file_name}.md" if args.output_file_name else 'sarif-2-md-output.md'
        output_md_path = os.path.join(os.path.dirname(sarif_path), output_md_name)
        with open(output_md_path, 'w', encoding='utf-8') as output_file:
            output_file.write(md_content)
        print(f"✅ Markdown content was written to {output_md_path}")
    else:
        commenter = GitHubPRCommenter()
        commenter.post_comment(md_content)
        print("✅ SARIF Report   was posted as a PR comment on GitHub.")

if __name__ == '__main__':
    main()
