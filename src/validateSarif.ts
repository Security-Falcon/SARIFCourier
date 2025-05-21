// src/validateSarif.ts
import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import { loadSchema } from './utils';

export function validateSarif(sarifContent: any): void {
  const schema = loadSchema();
  const ajv = new Ajv({ allErrors: true });
  addFormats(ajv);
  const validate = ajv.compile(schema);
  if (!validate(sarifContent)) {
    throw new Error('Invalid SARIF file: ' + (validate.errors?.[0]?.message || 'Unknown error'));
  }
  console.log('✅: Successfully Validated Input against OASIS Schema.');

  const runs = (sarifContent as any).runs;

  if (!Array.isArray(runs)) {
    throw new Error('Invalid SARIF file: The "runs" property must be an array.');
  }
  if (runs.length === 0) {
    console.log('ℹ️: SARIF file contains no runs. Exiting successfully.');
    process.exit(0);
  }

  // Check for empty or null results in any run and exit successfully if all are empty or null
  const allResultsEmptyOrNull = runs.every((run: any, idx: number) => {
    if (!('results' in run)) {
      console.warn(`⚠️: Run at index ${idx} is missing the 'results' property. Treating as empty.`);
      return true;
    }
    if (run.results == null) return true;
    if (Array.isArray(run.results) && run.results.length === 0) return true;
    return false;
  });

  if (allResultsEmptyOrNull) {
    console.log('ℹ️: SARIF file contains no results (all results are null, empty, or missing). Exiting successfully.');
    process.exit(0);
  }

  // Optionally, warn if any run has results that are not an array
  runs.forEach((run: any, idx: number) => {
    if ('results' in run && run.results != null && !Array.isArray(run.results)) {
      console.warn(`⚠️: Run at index ${idx} has a 'results' property that is not an array.`);
    }
  });
}
