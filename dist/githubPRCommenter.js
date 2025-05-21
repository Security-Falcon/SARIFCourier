"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.GitHubPRCommenter = void 0;
// src/githubPRCommenter.ts
const axios_1 = __importDefault(require("axios"));
class GitHubPRCommenter {
    constructor() {
        this.token = process.env.GITHUB_TOKEN || '';
        this.host = process.env.GITHUB_HOST || 'https://api.github.com';
        this.repo = process.env.GITHUB_REPOSITORY || '';
        this.ref = process.env.GITHUB_REF || '';
        this.prNumber = process.env.GITHUB_PR_NUMBER || '';
        if (!this.token)
            throw new Error('GITHUB_TOKEN environment variable is required.');
        if (!this.repo)
            throw new Error('GITHUB_REPOSITORY environment variable is required.');
        if (!this.prNumber) {
            if (this.ref.startsWith('refs/pull/')) {
                this.prNumber = this.ref.split('/')[2];
            }
            else {
                throw new Error('GITHUB_PR_NUMBER or a valid GITHUB_REF is required.');
            }
        }
        this.headers = {
            Authorization: `token ${this.token}`,
            Accept: 'application/vnd.github.v3+json',
        };
    }
    async postComment(body) {
        const url = `${this.host}/repos/${this.repo}/issues/${this.prNumber}/comments`;
        const response = await axios_1.default.post(url, { body }, { headers: this.headers });
        if (response.status !== 201) {
            throw new Error(`Failed to post comment: ${response.status} ${response.statusText}`);
        }
        return response.data;
    }
}
exports.GitHubPRCommenter = GitHubPRCommenter;
