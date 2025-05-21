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

  async postComment(body: string, driverName?: string): Promise<any> {
    // If driverName is provided, try to find and update an existing comment for that driver
    if (driverName) {
      const commentsUrl = `${this.host}/repos/${this.repo}/issues/${this.prNumber}/comments`;
      const commentsResp = await axios.get(commentsUrl, { headers: this.headers });
      if (commentsResp.status === 200 && Array.isArray(commentsResp.data)) {
        const marker = `<!-- SARIFCourier:${driverName} -->`;
        const existing = commentsResp.data.find((c: any) => typeof c.body === 'string' && c.body.includes(marker));
        const commentBody = `${marker}\n${body}`;
        if (existing) {
          // Update existing comment
          const updateUrl = `${this.host}/repos/${this.repo}/issues/comments/${existing.id}`;
          const updateResp = await axios.patch(updateUrl, { body: commentBody }, { headers: this.headers });
          if (updateResp.status !== 200) {
            throw new Error(`Failed to update comment: ${updateResp.status} ${updateResp.statusText}`);
          }
          return updateResp.data;
        } else {
          // Post new comment
          const createResp = await axios.post(commentsUrl, { body: commentBody }, { headers: this.headers });
          if (createResp.status !== 201) {
            throw new Error(`Failed to post comment: ${createResp.status} ${createResp.statusText}`);
          }
          return createResp.data;
        }
      }
    }
    // Fallback: just post a new comment
    const url = `${this.host}/repos/${this.repo}/issues/${this.prNumber}/comments`;
    const response = await axios.post(url, { body }, { headers: this.headers });
    if (response.status !== 201) {
      throw new Error(`Failed to post comment: ${response.status} ${response.statusText}`);
    }
    return response.data;
  }
}
