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
      await new GitHubPRCommenter().postComment(mdContent);
      console.log(chalk.green('✅: SARIF Report was posted as a PR comment on GitHub.'));
    }
  } catch (e: any) {
    console.error(chalk.red(`❌ Error: ${e.message}`));
    console.error(chalk.yellow('\n--- Stack Trace ---'));
    console.error(e.stack);
    process.exit(1);
  }
}

main();
