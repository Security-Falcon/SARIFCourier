// src/extractFindings.ts
const iconHost = "https://raw.githubusercontent.com/Abdullah-Schahin/icons/refs/heads/main";
const iconMap: Record<string, string> = {
  error: `<img src="${iconHost}/critical.svg" alt="error" width="24" />`,
  warning: `<img src="${iconHost}/medium.svg" alt="warning" width="24" />`,
  note: `<img src="${iconHost}/low.svg" alt="note" width="24" />`
};

export interface Finding {
  file: string;
  line: number;
  severity: string;
  rule_id: string;
  message_text: string;
  rule_description: string;
  remediation: string;
  level: string;
}

export function extractFindings(sarif: any): Finding[] {
  const ruleDesc: Record<string, string> = {};
  const remediationMap: Record<string, string> = {};
  const findings: Finding[] = [];
  for (const run of sarif.runs || []) {
    for (const rule of run.tool?.driver?.rules || []) {
      const ruleId = rule.id || '';
      ruleDesc[ruleId] = rule.fullDescription?.text || '';
      const remediation = rule.help?.text || rule.help?.markdown || '';
      remediationMap[ruleId] = remediation;
    }
    for (const result of run.results || []) {
      const msg = result.message?.text || '';
      const level = result.level || 'warning';
      const ruleId = result.ruleId || '';
      for (const loc of result.locations || []) {
        const phys = loc.physicalLocation || {};
        findings.push({
          file: phys.artifactLocation?.uri || '',
          line: phys.region?.startLine || 0,
          severity: iconMap[level.toLowerCase()] || level.toUpperCase(),
          rule_id: ruleId,
          message_text: msg,
          rule_description: ruleDesc[ruleId] || '',
          remediation: remediationMap[ruleId] || '',
          level: level.toLowerCase(),
        });
      }
    }
  }
  return findings;
}
