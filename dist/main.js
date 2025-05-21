"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
// src/main.ts
require("dotenv/config");
const yargs_1 = __importDefault(require("yargs"));
const helpers_1 = require("yargs/helpers");
const chalk_1 = __importDefault(require("chalk"));
const path_1 = __importDefault(require("path"));
const fs_1 = __importDefault(require("fs"));
const banner_1 = require("./banner");
const utils_1 = require("./utils");
const validateSarif_1 = require("./validateSarif");
const convert_1 = require("./convert");
const githubPRCommenter_1 = require("./githubPRCommenter");
async function main() {
    (0, banner_1.printBanner)();
    const argv = (0, yargs_1.default)((0, helpers_1.hideBin)(process.argv))
        .option('sarif', { type: 'string', demandOption: true, describe: 'Path to SARIF report' })
        .option('local', { type: 'boolean', default: false, describe: 'Output markdown summary locally instead of posting to GitHub' })
        .option('output-file-name', { alias: 'ofn', type: 'string', describe: 'Name of output Markdown file. Default: sarif-2-md-output.md' })
        .help()
        .parseSync();
    try {
        const sarifPath = path_1.default.resolve(argv.sarif);
        const sarifData = (0, utils_1.loadJsonFile)(sarifPath);
        (0, validateSarif_1.validateSarif)(sarifData);
        const mdContent = (0, convert_1.convert)(sarifData);
        if (argv.local) {
            const outputMdName = argv["output-file-name"] ? `${argv["output-file-name"]}.md` : 'sarif-2-md-output.md';
            const outputMdPath = path_1.default.join(path_1.default.dirname(sarifPath), outputMdName);
            fs_1.default.writeFileSync(outputMdPath, mdContent, 'utf-8');
            console.log(chalk_1.default.green(`✅: Markdown content was written to ${outputMdPath}`));
        }
        else {
            await new githubPRCommenter_1.GitHubPRCommenter().postComment(mdContent);
            console.log(chalk_1.default.green('✅: SARIF Report was posted as a PR comment on GitHub.'));
        }
    }
    catch (e) {
        console.error(chalk_1.default.red(`❌ Error: ${e.message}`));
        console.error(chalk_1.default.yellow('\n--- Stack Trace ---'));
        console.error(e.stack);
        process.exit(1);
    }
}
main();
