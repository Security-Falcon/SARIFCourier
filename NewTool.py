# CLI Tool: SARIFCourier
# Purpose: Parses SARIF reports and posts security findings as PR comments on GitHub, pinned to specific lines or outputs them locally as markdown

import argparse
import json
import os
import requests
from typing import List, Dict
from jsonschema import validate, ValidationError
from collections import defaultdict

# Banner
BANNER = r'''
 _______  _______  _______ _________ _______    _______  _______           _______ _________ _______  _______ 
(  ____ \(  ___  )(  ____ )\__   __/(  ____ \  (  ____ \(  ___  )|\     /|(  ____ )\__   __/(  ____ \(  ____ )
| (    \/| (   ) || (    )|   ) (   | (    \/  | (    \/| (   ) || )   ( || (    )|   ) (   | (    \/| (    )|
| (_____ | (___) || (____)|   | |   | (__      | |      | |   | || |   | || (____)|   | |   | (__    | (____)|
(_____  )|  ___  ||     __)   | |   |  __)     | |      | |   | || |   | ||     __)   | |   |  __)   |     __)
      ) || (   ) || (\ (      | |   | (        | |      | |   | || |   | || (\ (      | |   | (      | (\ (   
/\____) || )   ( || ) \ \_____) (___| )        | (____/\| (___) || (___) || ) \ \_____) (___| (____/\| ) \ \__
\_______)|/     \||/   \__/\_______/|/         (_______/(_______)(_______)|/   \__/\_______/(_______/|/   \__/
                                                                                                                                                                                  
        SARIFCourier - Delivering SARIF Findings to GitHub Pull Requests
        By Abdullah Schahin      
------------------------------------------------------------------------------
Features:
- Parses SARIF v2.1.0 reports
- Validates SARIF input against schema
- Extracts security findings
- Comments inline on GitHub PR diffs at specific file & line
- Posts summary comment with all findings
- Outputs local markdown reports when --local flag is used
- Saves local markdown to _md_report.md file
- Uses environment variables for GitHub token and API URL
'''

# GitHub API endpoint for posting comments
GITHUB_API = os.getenv("GITHUB_API", "https://api.github.com")

def parse_args():
    parser = argparse.ArgumentParser(description="Post SARIF security findings as GitHub PR comments or output locally.")
    parser.add_argument("--sarif", required=True, help="Path to SARIF report")
    parser.add_argument("--repo", required=False, help="GitHub repository in the format owner/repo")
    parser.add_argument("--pr", required=False, type=int, help="Pull request number")
    parser.add_argument("--token", required=False, help="GitHub token (use GITHUB_TOKEN env variable instead)")
    parser.add_argument("--schema", required=False, default="src/schema/sarif-schema-2.1.0.json", help="Path to SARIF JSON Schema")
    parser.add_argument("--local", action="store_true", help="Output markdown summary locally instead of posting to GitHub")
    return parser.parse_args()

def load_sarif(sarif_path: str) -> Dict:
    with open(sarif_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_sarif(data: Dict, schema_path: str):
    if not os.path.exists(schema_path):
        print("Schema file not found:", schema_path)
        exit(1)
    with open(schema_path, "r", encoding="utf-8") as schema_file:
        schema = json.load(schema_file)
    try:
        validate(instance=data, schema=schema)
        print("SARIF file is valid")
    except ValidationError as ve:
        print(f"Invalid SARIF file: {ve.message}")
        exit(1)

def extract_findings(sarif: Dict) -> List[Dict]:
    findings = []
    # Use SVG icons from src/app/assets for each level
    icon_content_host = "https://raw.githubusercontent.com/Abdullah-Schahin/icons/refs/heads/main"
    icon_map = {
        "error": f'<img src="{icon_content_host}/critical.svg" alt="error" width="24" />',
        "warning": f'<img src="{icon_content_host}/medium.svg" alt="warning" width="24" />',
        "note": f'<img src="{icon_content_host}/low.svg" alt="note" width="24" />'
    }

    rule_descriptions = {}
    for run in sarif.get("runs", []):
        rules = run.get("tool", {}).get("driver", {}).get("rules", [])
        for rule in rules:
            rule_id = rule.get("id", "")
            description = rule.get("fullDescription", {}).get("text", "")
            rule_descriptions[rule_id] = description

        for result in run.get("results", []):
            message = result.get("message", {}).get("text", "")
            level = result.get("level", "warning")
            rule_id = result.get("ruleId", "")
            rule_description = rule_descriptions.get(rule_id, "")
            for loc in result.get("locations", []):
                phys_loc = loc.get("physicalLocation", {})
                artifact_loc = phys_loc.get("artifactLocation", {}).get("uri", "")
                region = phys_loc.get("region", {})
                start_line = region.get("startLine", 0)
                findings.append({
                    "file": artifact_loc,
                    "line": start_line,
                    "severity": icon_map.get(level.lower(), level.upper()),
                    "rule_id": rule_id,
                    "message_text": message,
                    "rule_description": rule_description,
                    "level": level.lower()
                })
    return findings

def format_summary_comment(findings: List[Dict], sarif_data: Dict = None) -> str:
    grouped = defaultdict(list)
    for f in findings:
        grouped[f['level']].append(f)

    branch_name = os.getenv("HEAD_REF", "main")

    # Get driver name from SARIF if provided
    driver_name = "Unknown Tool"
    if sarif_data:
        try:
            driver_name = sarif_data["runs"][0]["tool"]["driver"]["name"]
        except Exception:
            pass

    total_findings = len(findings)

    # Legend for severity icons in an expandable section
    legend = """
<details>
<summary><strong>Legend: Severity Levels</strong></summary>

| Icon | Severity |
|:------:|----------|
| <img src="https://raw.githubusercontent.com/Abdullah-Schahin/icons/main/critical.svg" alt="error" width="18" /> | CRITICAL / HIGH   |
| <img src="https://raw.githubusercontent.com/Abdullah-Schahin/icons/main/medium.svg" alt="warning" width="18" /> | MEDIUM |
| <img src="https://raw.githubusercontent.com/Abdullah-Schahin/icons/main/low.svg" alt="note" width="18" /> | LOW    |

</details>
"""

    header = (
        "# 🛡️ Security Findings Summary 🛡️\n"
        "<details>\n"
        "<summary><strong>Details</strong></summary>\n\n"
        f"- Scanner: `{driver_name}`\n"
        f"- Total Findings: `{total_findings}`\n"
        "- Source: SARIF\n"
        "</details>\n\n"
        f"{legend}\n"
    )
    table_header = "| Severity | Location | Rule ID | Message |\n|:--:|---------|---------|---------|\n"
    rows = []
    for level in ["error", "warning", "note"]:
        for f in grouped.get(level, []):
            filename = os.path.basename(f['file'])
            location_label = f"{filename}#L{f['line']}"
            location_link = f"[{location_label}](../blob/{branch_name}/{f['file']}#L{f['line']})"
            severity_cell = f['severity']
            rows.append(f"| {severity_cell} | {location_link} | {f['rule_id']} | {f['message_text']} |")

    banner = f"---\n\n>**_SARIFCourier_** by [Abdullah Schahin](https://github.com/Security-Falcon) — Delivering security insights to your developers."
    return header + table_header + "\n".join(rows) + "\n\n" + banner

def post_summary_comment(repo: str, pr_number: int, token: str, body: str):
    url = f"{GITHUB_API}/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"body": body}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 201:
        print(f"Failed to post summary comment - {response.status_code} - {response.text}")
    else:
        print("✅ Summary comment posted successfully.")

def save_local_report(sarif_path: str, markdown: str):
    base_name = os.path.splitext(sarif_path)[0]
    output_path = f"{base_name}_md_report.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"✅ Markdown report saved to: {output_path}")

def main():
    print(BANNER)
    args = parse_args()
    sarif_data = load_sarif(args.sarif)
    validate_sarif(sarif_data, args.schema)
    findings = extract_findings(sarif_data)

    if not findings:
        print("No findings to process.")
        return

    comment_body = format_summary_comment(findings, sarif_data)

    if args.local:
        print("\n--- LOCAL MARKDOWN REPORT ---\n")
        print(comment_body)
        save_local_report(args.sarif, comment_body)
    else:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("GitHub token is required. Set `GITHUB_TOKEN` environment variable.")
            return
        if not args.repo or not args.pr:
            print("Both --repo and --pr must be specified for posting to GitHub.")
            return
        post_summary_comment(args.repo, args.pr, token, comment_body)

if __name__ == "__main__":
    main()
