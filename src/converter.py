### Converter.py
import markdown

class MarkdownGenerator:
    def generate(self, sarif_content):
        """Converts SARIF content into Markdown format."""
        runs = sarif_content.get("runs", [])
        md_output = []

        md_output.append("# SARIF Report\n")
        for run in runs:
            tool = run.get("tool", {}).get("driver", {}).get("name", "Unknown Tool")
            md_output.append(f"## Tool: {tool}\n")

            results = run.get("results", [])
            if not results:
                md_output.append("No issues found.\n")
                continue

            for result in results:
                rule_id = result.get("ruleId", "Unknown Rule")
                message = result.get("message", {}).get("text", "No message provided.")
                level = result.get("level", "none").capitalize()
                locations = result.get("locations", [])

                location_info = ""
                if locations:
                    for loc in locations:
                        physical_location = loc.get("physicalLocation", {})
                        file_uri = physical_location.get("artifactLocation", {}).get("uri", "Unknown File")
                        region = physical_location.get("region", {})
                        start_line = region.get("startLine", "Unknown Line")
                        location_info += f"File: {file_uri}, Line: {start_line}\n"

                md_output.append(f"### Rule: {rule_id}\n")
                md_output.append(f"**Severity**: {level}\n")
                md_output.append(f"**Message**: {message}\n")
                if location_info:
                    md_output.append(f"**Location**: \n{location_info}\n")

        return "\n".join(md_output)