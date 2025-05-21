import path from 'path';
import { Finding } from './extractFindings';

export function formatSummaryComment(findings: Finding[], sarifData?: any): string {
  const grouped: Record<string, Finding[]> = { error: [], warning: [], note: [] };
  for (const f of findings) {
    if (grouped[f.level]) grouped[f.level].push(f);
  }
  const branch = process.env.HEAD_REF || 'main';
  const driver = sarifData?.runs?.[0]?.tool?.driver?.name || 'Unknown Tool';
  const legend = `
<details>

<summary><strong>Legend: Severity Levels</strong></summary>

| Icon | Severity |
|:------:|----------|
| <img src=\"https://raw.githubusercontent.com/Abdullah-Schahin/icons/main/critical.svg\" alt=\"error\" width=\"18\" /> | CRITICAL / HIGH   |
| <img src=\"https://raw.githubusercontent.com/Abdullah-Schahin/icons/main/medium.svg\" alt=\"warning\" width=\"18\" /> | MEDIUM |
| <img src=\"https://raw.githubusercontent.com/Abdullah-Schahin/icons/main/low.svg\" alt=\"note\" width=\"18\" /> | LOW    |

</details>
`;
  const header =
    `# 🛡️ Security Findings Summary 🛡️\n` +
    `<details>\n<summary><strong>Details</strong></summary>\n\n` +
    `- Scanner: \`${driver}\`\n` +
    `- Total Findings: \`${findings.length}\`\n` +
    `- Source: SARIF\n` +
    `</details>\n\n` +
    legend + '\n';
  const tableHeader = '| Severity | Location | Rule ID | Message |\n|:--:|---------|---------|---------|\n';
  const rows = [
    ...(['error', 'warning', 'note'] as const).flatMap(level =>
      grouped[level].map(f =>
        `| ${f.severity} | [${path.basename(f.file)}#L${f.line}](../blob/${branch}/${f.file}#L${f.line}) | ${f.rule_id} | ${f.message_text} |`
      )
    )
  ];
  const banner = '---\n\n>🛡️ **_SARIFCourier_** by [Abdullah Schahin](https://github.com/Security-Falcon) — Delivering security insights to your developers.';
  return header + tableHeader + rows.join('\n') + '\n\n' + banner;
}
