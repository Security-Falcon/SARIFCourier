import markdown

def convert(sarif_content):
    """Converts SARIF content into Markdown table format with descriptive emojis."""
    runs = sarif_content.get("runs", [])
    md_output = []

    md_output.append("# General SARIF Report 🛡️\n")
    
    md_output.append(">[!NOTE]")
    md_output.append(">In case of combined SARIF reports are provided, each tool with have it's own Table.\n")

    severity_emojis = {
        "none": "None ⚪",
        "note": "Note ℹ️",
        "warning": "Warning ⚠️",
        "error": "Error 🔥",
    }

    for run in runs:
        tool = run.get("tool", {}).get("driver", {}).get("name", "Unknown Tool")
        results = run.get("results", [])

        md_output.append(f"### Origin: {tool}\n")

        if not results:
            md_output.append("No issues found ✅🎉.\n")
            continue

        # Add Markdown table header
        md_output.append("| Rule-ID | Severity | Message | Location |")
        md_output.append("|---------|----------|---------|----------|")

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
                    location_info += f"[`{file_uri}, Line {start_line}`]({file_uri})"

            md_output.append(f"| {rule_id} | {severity} | {message} | {location_info} |")

    md_output.append("------\n")
    md_output.append("Markdown generated using SARIF-2-MD 🚀\n")
    return "\n".join(md_output)