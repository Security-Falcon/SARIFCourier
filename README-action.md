# SARIF Courier

A GitHub Action to validate, convert, and comment on SARIF files.

## Usage

Add the following step to your GitHub Actions workflow to use SARIF Courier:

```yaml
- name: Run SARIF Courier
  uses: your-username/SARIFCourier@v1
  with:
    sarif_file: 'path/to/your.sarif'
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    GITHUB_REPOSITORY: ${{ github.repository }}
    GITHUB_PR_NUMBER: ${{ github.event.pull_request.number }}
    # GITHUB_REF is optional, used if PR number is not set
    # GITHUB_REF: ${{ github.ref }}
```

- `sarif_file`: Path to the SARIF file to process (required).
- The required environment variables are passed via the `env:` block. Most are set automatically by GitHub Actions, but you must explicitly pass them if your workflow or action logic requires it.

## Required Environment Variables

To enable posting comments to pull requests, the following environment variables must be provided to the action:

- `GITHUB_TOKEN`: A GitHub token with `repo` scope (automatically provided in GitHub Actions as `secrets.GITHUB_TOKEN`).
- `GITHUB_REPOSITORY`: The repository in the format `owner/repo` (set as `${{ github.repository }}`).
- `GITHUB_PR_NUMBER`: The pull request number to comment on (set as `${{ github.event.pull_request.number }}` for PR workflows).
- `GITHUB_REF`: (Optional) The Git reference, e.g., `refs/pull/123/merge`. Used to infer the PR number if `GITHUB_PR_NUMBER` is not set.

These are required for the action to successfully post comments to pull requests.

## Example Workflow

```yaml
...
      - name: Run SARIF Courier
        uses: your-username/SARIFCourier@v1
        with:
          sarif_file: 'results.sarif'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
          GITHUB_PR_NUMBER: ${{ github.event.pull_request.number }}
```

## Branding
![SARIF Courier](https://img.shields.io/badge/SARIF-green?logo=shield)
