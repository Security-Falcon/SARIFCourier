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
    .option('post-target', { type: 'string', describe: 'Where to post the results: "pr" for Pull Request comment, "issue" for Issue comment. If not set, auto-detect.' })
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
      let postTarget = argv['post-target'];
      if (!postTarget) {
        // Auto-detect: PR if PR context, else issue
        const eventName = process.env.GITHUB_EVENT_NAME;
        const prNumber = process.env.GITHUB_PR_NUMBER || (process.env.GITHUB_REF && process.env.GITHUB_REF.startsWith('refs/pull/') ? process.env.GITHUB_REF.split('/')[2] : undefined);
        if (eventName === 'pull_request' || prNumber) {
          postTarget = 'pr';
        } else {
          postTarget = 'issue';
        }
      }
      // Try to extract driver name for unique comment marker
      let driverName = undefined;
      if (sarifData && Array.isArray(sarifData.runs) && sarifData.runs[0]?.tool?.driver?.name) {
        driverName = sarifData.runs[0].tool.driver.name;
      }
      // Only extract PR number if posting to PR
      let prNumber = undefined;
      if (postTarget === 'pr') {
        prNumber = process.env.GITHUB_PR_NUMBER || (process.env.GITHUB_REF && process.env.GITHUB_REF.startsWith('refs/pull/') ? process.env.GITHUB_REF.split('/')[2] : undefined);
        if (!prNumber) {
          throw new Error('GITHUB_PR_NUMBER or a valid GITHUB_REF is required when posting to a PR.');
        }
      }
      await new GitHubPRCommenter().postComment(mdContent, driverName, postTarget);
      console.log(chalk.green(`✅: SARIF Report was posted as a ${postTarget === 'pr' ? 'PR' : 'Issue'} comment on GitHub.`));
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
  const postTarget = process.env['INPUT_POST_TARGET'] || '';
  // Simulate CLI args for yargs
  process.argv.push('--sarif', sarifFile);
  if (postTarget) {
    process.argv.push('--post-target', postTarget);
  }
  await main();
}

runAction();
