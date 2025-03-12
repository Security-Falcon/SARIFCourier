import markdown
from datetime import datetime

def convert(sarif_content):
    """Converts SARIF content into Markdown table format with descriptive emojis."""
    runs = sarif_content.get("runs", [])
    md_output = []
    severity_emojis = {
        "none": "NONE ⚪",
        "note": "INFO",
        "warning": "WARNING",
        "error": "ERROR",
    }

    md_output.append("# General SARIF Report 🛡️\n")
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md_output.append(f"This report was generated on: `{current_date}` \nIn case of combined SARIF reports are provided, each tool with have its own Table.\n")

    for run in runs:
        tool = run.get("tool", {}).get("driver", {}).get("name", "Unknown Tool")
        results = run.get("results", [])

        md_output.append(f"### Origin Tool: {tool}\n")

        if not results:
            md_output.append("No issues found - Keep it up ✅ 🎉.\n")
            continue

        # Add Markdown table header
        md_output.append("| Rule-ID | Severity | Message | Location | Line |")
        md_output.append("|:---------|:---------|:---------|:---------|:--:|")

        for result in results:
            rule_id = result.get("ruleId", "Unknown Rule")
            message = result.get("message", {}).get("text", "No message provided.")
            level = result.get("level", "none").lower()
            severity = severity_emojis.get(level, f"⚪ {level.capitalize()}")  # Default emoji for unknown levels

            # Process location details
            location_info = ""
            locations = result.get("locations", [])
            if locations:
                for loc in locations:
                    physical_location = loc.get("physicalLocation", {})
                    file_uri = physical_location.get("artifactLocation", {}).get("uri", "Unknown File")
                    region = physical_location.get("region", {})
                    start_line = region.get("startLine", "Unknown Line")
                    location_info += f"[`{file_uri}`]({file_uri})"

            md_output.append(f"| {rule_id} | {severity} | {message} | {location_info} | {start_line} |")


    md_output.append(">Markdown generated using SARIF-2-MD 🚀\n")
    return "\n".join(md_output)