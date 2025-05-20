import argparse
import json
import os
from pathlib import Path
from jsonschema import validate, ValidationError
from collections import defaultdict
from typing import List, Dict
import requests
from colorama import Fore, Style, init
import logging
import sys
import traceback

# --- Banner ---
def print_banner():
    banner = """
███████╗ █████╗ ██████╗ ██╗███████╗     ██████╗ ██████╗ ██╗   ██╗██████╗ ██╗███████╗██████╗ 
██╔════╝██╔══██╗██╔══██╗██║██╔════╝    ██╔════╝██╔═══██╗██║   ██║██╔══██╗██║██╔════╝██╔══██╗
███████╗███████║██████╔╝██║█████╗      ██║     ██║   ██║██║   ██║██████╔╝██║█████╗  ██████╔╝
╚════██║██╔══██║██╔══██╗██║██╔══╝      ██║     ██║   ██║██║   ██║██╔══██╗██║╚═╝  ██╔══██╗
███████║██║  ██║██║  ██║██║██║         ╚██████╗╚██████╔╝╚██████╔╝██║  ██║██║███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝          ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝                                                 
    """
    print(Fore.BLUE + banner + "\n" + Fore.RED + "SARIFCourier 🛡️  By Abdullah Schahin" + "\n\n" + Fore.WHITE)

# --- Utility Functions ---
def load_json_file(file_path: str):
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"File not found at {file_path}")
    with open(file, 'r') as f:
        return json.load(f)

def load_schema():
    return load_json_file("sarif-schema-2.1.0.json")

# --- SARIF Validation ---
def validate_sarif(sarif_content):
    try:
        schema = load_schema()
        validate(instance=sarif_content, schema=schema)
        print("✅: Successfully Validated Input against OASIS Schema.")
    except ValidationError as e:
        raise ValueError(f"Invalid SARIF file: {e.message}")

# --- SARIF to Markdown Conversion ---
def extract_findings(sarif: dict) -> list:
    icon_host = "https://raw.githubusercontent.com/Abdullah-Schahin/icons/refs/heads/main"
    icon_map = {
        "error": f'<img src="{icon_host}/critical.svg" alt="error" width="24" />',
        "warning": f'<img src="{icon_host}/medium.svg" alt="warning" width="24" />',
        "note": f'<img src="{icon_host}/low.svg" alt="note" width="24" />'
    }
    rule_desc, remediation_map, findings = {}, {}, []
    for run in sarif.get("runs", []):
        for rule in run.get("tool", {}).get("driver", {}).get("rules", []):
            rule_id = rule.get("id", "")
            rule_desc[rule_id] = rule.get("fullDescription", {}).get("text", "")
            remediation = rule.get("help", {}).get("text") or rule.get("help", {}).get("markdown", "")
            remediation_map[rule_id] = remediation
        for result in run.get("results", []):
            msg, level, rule_id = result.get("message", {}).get("text", ""), result.get("level", "warning"), result.get("ruleId", "")
            for loc in result.get("locations", []):
                phys = loc.get("physicalLocation", {})
                findings.append({
                    "file": phys.get("artifactLocation", {}).get("uri", ""),
                    "line": phys.get("region", {}).get("startLine", 0),
                    "severity": icon_map.get(level.lower(), level.upper()),
                    "rule_id": rule_id,
                    "message_text": msg,
                    "rule_description": rule_desc.get(rule_id, ""),
                    "remediation": remediation_map.get(rule_id, ""),
                    "level": level.lower()
                })
    return findings

def format_summary_comment(findings: list, sarif_data: dict = None) -> str:
    grouped = defaultdict(list)
    for f in findings:
        grouped[f['level']].append(f)
    branch = os.getenv("HEAD_REF", "main")
    driver = sarif_data.get("runs", [{}])[0].get("tool", {}).get("driver", {}).get("name", "Unknown Tool") if sarif_data else "Unknown Tool"
    legend = """
<details>

<summary><strong>Legend: Severity Levels</strong></summary>

| Icon | Severity |
|:------:|----------|
| <img src=\"https://raw.githubusercontent.com/Abdullah-Schahin/icons/main/critical.svg\" alt=\"error\" width=\"18\" /> | CRITICAL / HIGH   |
| <img src=\"https://raw.githubusercontent.com/Abdullah-Schahin/icons/main/medium.svg\" alt=\"warning\" width=\"18\" /> | MEDIUM |
| <img src=\"https://raw.githubusercontent.com/Abdullah-Schahin/icons/main/low.svg\" alt=\"note\" width=\"18\" /> | LOW    |

</details>
"""
    header = (
        "# 🛡️ Security Findings Summary 🛡️\n"
        "<details>\n"
        "<summary><strong>Details</strong></summary>\n\n"
        f"- Scanner: `{driver}`\n"
        f"- Total Findings: `{len(findings)}`\n"
        "- Source: SARIF\n"
        "</details>\n\n"
        f"{legend}\n"
    )
    table_header = "| Severity | Location | Rule ID | Message |\n|:--:|---------|---------|---------|\n"
    rows = [
        f"| {f['severity']} | [{os.path.basename(f['file'])}#L{f['line']}](../blob/{branch}/{f['file']}#L{f['line']}) | {f['rule_id']} | {f['message_text']} |"
        for level in ["error", "warning", "note"] for f in grouped.get(level, [])
    ]
    banner = "---\n\n>🛡️ **_SARIFCourier_** by [Abdullah Schahin](https://github.com/Security-Falcon) — Delivering security insights to your developers."
    return header + table_header + "\n".join(rows) + "\n\n" + banner

def convert(sarif_content):
    return format_summary_comment(extract_findings(sarif_content), sarif_content)

# --- GitHub PR Commenter ---
class GitHubPRCommenter:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.host = os.getenv("GITHUB_HOST", "https://api.github.com")
        self.repo = os.getenv("GITHUB_REPOSITORY")
        self.ref = os.getenv("GITHUB_REF", "")
        self.pr_number = os.getenv("GITHUB_PR_NUMBER")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required.")
        if not self.repo:
            raise ValueError("GITHUB_REPOSITORY environment variable is required.")
        if not self.pr_number:
            if self.ref.startswith("refs/pull/"):
                self.pr_number = self.ref.split("/")[2]
            else:
                raise ValueError("GITHUB_PR_NUMBER or a valid GITHUB_REF is required.")
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def post_comment(self, body: str):
        url = f"{self.host}/repos/{self.repo}/issues/{self.pr_number}/comments"
        response = requests.post(url, headers=self.headers, json={"body": body})
        if response.status_code != 201:
            raise Exception(f"Failed to post comment: {response.status_code} {response.text}")
        return response.json()

# --- Main Entrypoint ---
def main():
    init(autoreset=True)
    print_banner()
    parser = argparse.ArgumentParser(description='Makes your SARIF reports more readable')
    parser.add_argument('--sarif', required=True, help='Path to SARIF report')
    parser.add_argument('--local', action='store_true', help='Output markdown summary locally instead of posting to GitHub')
    parser.add_argument('--output-file-name', '-ofn', required=False, help='Name of output Markdown file. Default: sarif-2-md-output.md')
    args = parser.parse_args()

    try:
        sarif_path = os.path.abspath(args.sarif)
        sarif_data = load_json_file(sarif_path)
        validate_sarif(sarif_data)
        md_content = convert(sarif_data)

        if args.local:
            output_md_name = f"{args.output_file_name}.md" if args.output_file_name else 'sarif-2-md-output.md'
            output_md_path = os.path.join(os.path.dirname(sarif_path), output_md_name)
            with open(output_md_path, 'w', encoding='utf-8') as output_file:
                output_file.write(md_content)
            print(f"✅: Markdown content was written to {output_md_path}")
        else:
            GitHubPRCommenter().post_comment(md_content)
            print("✅: SARIF Report was posted as a PR comment on GitHub.")
    except Exception as e:
        logging.error(Fore.RED + f"❌ Error: {e}")
        print(Fore.RED + f"❌ Error: {e}")
        print(Fore.YELLOW + "\n--- Stack Trace ---")
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)

if __name__ == '__main__':
    main()
