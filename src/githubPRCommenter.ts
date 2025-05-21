// src/githubPRCommenter.ts
import axios from 'axios';

export class GitHubPRCommenter {
  private token: string;
  private host: string;
  private repo: string;
  private ref: string;
  private prNumber: string;
  private headers: Record<string, string>;

  constructor() {
    this.token = process.env.GITHUB_TOKEN || '';
    this.host = process.env.GITHUB_HOST || 'https://api.github.com';
    this.repo = process.env.GITHUB_REPOSITORY || '';
    this.ref = process.env.GITHUB_REF || '';
    this.prNumber = process.env.GITHUB_PR_NUMBER || '';
    if (!this.token) throw new Error('GITHUB_TOKEN environment variable is required.');
    if (!this.repo) throw new Error('GITHUB_REPOSITORY environment variable is required.');
    if (!this.prNumber) {
      if (this.ref.startsWith('refs/pull/')) {
        this.prNumber = this.ref.split('/')[2];
      } else {
        throw new Error('GITHUB_PR_NUMBER or a valid GITHUB_REF is required.');
      }
    }
    this.headers = {
      Authorization: `token ${this.token}`,
      Accept: 'application/vnd.github.v3+json',
    };
  }

  async postComment(body: string): Promise<any> {
    const url = `${this.host}/repos/${this.repo}/issues/${this.prNumber}/comments`;
    const response = await axios.post(url, { body }, { headers: this.headers });
    if (response.status !== 201) {
      throw new Error(`Failed to post comment: ${response.status} ${response.statusText}`);
    }
    return response.data;
  }
}
