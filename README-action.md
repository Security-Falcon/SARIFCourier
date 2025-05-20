# SARIF Courier

A GitHub Action to validate, convert, and comment on SARIF files.

## Usage

```yaml
- name: Run SARIF Courier
  uses: your-username/SARIFCourier@v1
  with:
    sarif_file: 'path/to/your.sarif'
```

## Inputs
- `sarif_file`: Path to the SARIF file to process. (required)

## Outputs
- `result`: Result of the SARIF processing.

## Required Environment Variables

To enable posting comments to pull requests, the following environment variables must be provided to the action:

- `GITHUB_TOKEN`: A GitHub token with `repo` scope (automatically provided in GitHub Actions as `secrets.GITHUB_TOKEN`).
- `GITHUB_REPOSITORY`: The repository in the format `owner/repo` (automatically set in GitHub Actions).
- `GITHUB_PR_NUMBER`: The pull request number to comment on. If not set, the action will attempt to extract it from `GITHUB_REF`.
- `GITHUB_REF`: (Optional) The Git reference, e.g., `refs/pull/123/merge`. Used to infer the PR number if `GITHUB_PR_NUMBER` is not set.

These are required for the action to successfully post comments to pull requests.

## Branding
![SARIF Courier](https://img.shields.io/badge/SARIF-green?logo=shield)
