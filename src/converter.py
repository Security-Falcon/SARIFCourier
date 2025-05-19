import os
from collections import defaultdict
from typing import List, Dict

def extract_findings(sarif: Dict) -> List[Dict]:
    findings = []
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
    driver_name = "Unknown Tool"
    if sarif_data:
        try:
            driver_name = sarif_data["runs"][0]["tool"]["driver"]["name"]
        except Exception:
            pass
    total_findings = len(findings)
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
    banner = f"---\n\n>🛡️ **_SARIFCourier_** by [Abdullah Schahin](https://github.com/Security-Falcon) — Delivering security insights to your developers."
    return header + table_header + "\n".join(rows) + "\n\n" + banner

def convert(sarif_content):
    findings = extract_findings(sarif_content)
    return format_summary_comment(findings, sarif_content)