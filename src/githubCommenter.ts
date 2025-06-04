import axios from 'axios';

export class GitHubPRCommenter {
  private token: string;
  private host: string;
  private repo: string;
  private ref: string;
  private headers: Record<string, string>;

  constructor() {
    this.token = process.env.GITHUB_TOKEN || '';
    this.host = process.env.GITHUB_HOST || 'https://api.github.com';
    this.repo = process.env.GITHUB_REPOSITORY || '';
    this.ref = process.env.GITHUB_REF || '';
    if (!this.token) throw new Error('GITHUB_TOKEN environment variable is required.');
    if (!this.repo) throw new Error('GITHUB_REPOSITORY environment variable is required.');
    this.headers = {
      Authorization: `token ${this.token}`,
      Accept: 'application/vnd.github.v3+json',
    };
  }

  async postComment(body: string, driverName?: string, postTarget?: string): Promise<any> {
    // Decide whether to post to PR or issue
    let issueNumber: string | undefined = undefined;
    if (postTarget === 'pr') {
      // Extract PR number only when needed
      let prNumber = process.env.GITHUB_PR_NUMBER || (this.ref.startsWith('refs/pull/') ? this.ref.split('/')[2] : undefined);
      if (!prNumber) {
        throw new Error('GITHUB_PR_NUMBER or a valid GITHUB_REF is required when posting to a PR.');
      }
      issueNumber = prNumber;
    } else if (postTarget === 'issue') {
      // Try to find an open issue with a SARIF-Courier label or title, else create one
      const issuesUrl = `${this.host}/repos/${this.repo}/issues?state=open&labels=sarif-courier`;
      let issueId: string | undefined = undefined;
      try {
        const issuesResp = await axios.get(issuesUrl, { headers: this.headers });
        if (issuesResp.status === 200 && Array.isArray(issuesResp.data)) {
          // Match the actual title used for the issue
          const found = issuesResp.data.find((i: any) => i.title && i.title === 'SAST Security Results 🚨');
          if (found) issueId = found.number;
        }
      } catch {}
      if (!issueId) {
        // Create a new issue and return immediately (do not post a comment)
        const createResp = await axios.post(`${this.host}/repos/${this.repo}/issues`, {
          title: 'SAST Security Results 🚨',
          body,
          labels: ['sarif-courier']
        }, { headers: this.headers });
        if (createResp.status !== 201) {
          throw new Error(`Failed to create issue: ${createResp.status} ${createResp.statusText}`);
        }
        return createResp.data; // Do not post a comment if issue was just created
      } else {
        // Add a comment to the found issue
        const commentsUrl = `${this.host}/repos/${this.repo}/issues/${issueId}/comments`;
        const createResp = await axios.post(commentsUrl, { body }, { headers: this.headers });
        if (createResp.status !== 201) {
          throw new Error(`Failed to post comment: ${createResp.status} ${createResp.statusText}`);
        }
        return createResp.data;
      }
      issueNumber = issueId;
    } else {
      // Default: PR
      let prNumber = process.env.GITHUB_PR_NUMBER || (this.ref.startsWith('refs/pull/') ? this.ref.split('/')[2] : undefined);
      if (!prNumber) {
        throw new Error('GITHUB_PR_NUMBER or a valid GITHUB_REF is required when posting to a PR.');
      }
      issueNumber = prNumber;
    }
    const commentsUrl = `${this.host}/repos/${this.repo}/issues/${issueNumber}/comments`;
    if (driverName) {
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
    const response = await axios.post(commentsUrl, { body }, { headers: this.headers });
    if (response.status !== 201) {
      throw new Error(`Failed to post comment: ${response.status} ${response.statusText}`);
    }
    return response.data;
  }
}
