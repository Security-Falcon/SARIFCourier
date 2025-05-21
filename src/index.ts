import 'dotenv/config';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import chalk from 'chalk';
import path from 'path';
import fs from 'fs';
import { printBanner } from './banner';
import { loadJsonFile } from './utils';
import { validateSarif } from './validateSarif';
import { convert } from './convert';
import { GitHubPRCommenter } from './githubPRCommenter';

async function main() {
  printBanner();
  const argv = yargs(hideBin(process.argv))
    .option('sarif', { type: 'string', demandOption: true, describe: 'Path to SARIF report' })
    .option('local', { type: 'boolean', default: false, describe: 'Output markdown summary locally instead of posting to GitHub' })
    .option('output-file-name', { alias: 'ofn', type: 'string', describe: 'Name of output Markdown file. Default: sarif-2-md-output.md' })
    .help()
    .parseSync();

  try {
    const sarifPath = path.resolve(argv.sarif);
    const sarifData = loadJsonFile(sarifPath);
    validateSarif(sarifData);
    const mdContent = convert(sarifData);

    if (argv.local) {
      const outputMdName = argv["output-file-name"] ? `${argv["output-file-name"]}.md` : 'sarif-2-md-output.md';
      const outputMdPath = path.join(path.dirname(sarifPath), outputMdName);
      fs.writeFileSync(outputMdPath, mdContent, 'utf-8');
      console.log(chalk.green(`✅: Markdown content was written to ${outputMdPath}`));
    } else {
      // Try to extract driver name for unique comment marker
      let driverName = undefined;
      if (sarifData && Array.isArray(sarifData.runs) && sarifData.runs[0]?.tool?.driver?.name) {
        driverName = sarifData.runs[0].tool.driver.name;
      }
      await new GitHubPRCommenter().postComment(mdContent, driverName);
      console.log(chalk.green('✅: SARIF Report was posted as a PR comment on GitHub.'));
    }
  } catch (e: any) {
    console.error(chalk.red(`❌ Error: ${e.message}`));
    console.error(chalk.yellow('\n--- Stack Trace ---'));
    console.error(e.stack);
    process.exit(1);
  }
}

async function runAction() {
  // GitHub Actions passes inputs as environment variables: INPUT_<input_name>
  const sarifFile = process.env['INPUT_SARIF_FILE'] || '';
  if (!sarifFile) {
    console.error('❌ Error: Missing required input: sarif_file');
    process.exit(1);
  }
  // Simulate CLI args for yargs
  process.argv.push('--sarif', sarifFile);
  await main();
}

runAction();
