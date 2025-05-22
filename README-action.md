<h4 align="center">
  <img src="banner-nob.png" alt="SARIF Courier Logo" width="1000" />
</h4>

**Render SARIF Security Reports directly in your Pull Requests – no GitHub Advanced Security (GHAS) required!**

## ✨ What is SARIF Courier?

SARIF Courier is a GitHub Action that takes a SARIF (Static Analysis Results Interchange Format) report and posts a beautifully formatted summary as a comment on your Pull Requests. This enables you to surface security and static analysis findings in your PR workflow, even if you do not have access to GitHub Advanced Security (GHAS).

- **No GHAS required:** Works for all repositories, public or private.
- **Instant feedback:** See security and code analysis results right in your PRs.
- **Easy integration:** Just drop the action in your workflow and point it to your SARIF file.

## 💡 Why SARIF Courier?

- **Universal:** Works with any SARIF-compliant tool (CodeQL, Semgrep, ESLint, etc).
- **No vendor lock-in:** No need for GHAS or paid features.
- **Fast feedback:** Developers see issues before merging.

## 🚦 Usage

### 🔑 Required Environment Variables & Permissions

- **GITHUB_TOKEN**: Provided automatically by GitHub Actions. Used to post comments on PRs.
  - **Permissions required:**
    - `contents: write` (to create/update comments)
    - `pull-requests: write` (recommended for private repos)

No additional secrets or configuration are needed.

> [!NOTE]
> SARIF Courier automatically uses environment variables provided by GitHub Actions for repository name, pull request number, and ref name. You do not need to set these manually—only `GITHUB_TOKEN` is required for posting comments. See the [GitHub Actions documentation](https://docs.github.com/en/actions/learn-github-actions/environment-variables) for more details.

### 📝 Inputs

| Name        | Description                        | Required | Default         |
|-------------|------------------------------------|----------|-----------------|
| sarif_file  | Path to the SARIF file to process. |   Yes    | results.sarif   |


### Integration
Add the following step to your workflow after generating a SARIF report:

```yaml
- name: Render SARIF in PR
  uses: Abdullah-Schahin/SARIFCourier@v1 #Preferred: Pin the action to a given commit sha!
  with:
    sarif_file: path/to/your-report.sarif # Path to the SARIF file to process (relative to the workspace)
```

### Output on PR
![image](https://github.com/user-attachments/assets/395920ca-f6e8-4ff1-9ccf-bb4dfda51ce1)

### Example Workflow

```yaml
name: Static Analysis
on:
  pull_request:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run your static analysis tool
        run: |
          # ...run your tool, output SARIF to results.sarif...
          # ...assuming exit code 1
      - name: Render SARIF in PR
        if: failure()
        uses: Abdullah-Schahin/SARIFCourier@v1 #Preferred: Pin the action to a given commit sha!
        with:
          sarif_file: results.sarif
```

---

## 🛠️ License

MIT License. See [LICENSE](./LICENSE).
