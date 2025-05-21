# 🛡️ SARIF Courier 🛡️

![alt text](banner.png)

**Render SARIF Security Reports directly in your Pull Requests – no GitHub Advanced Security (GHAS) required!**

---

## ✨ What is SARIF Courier?

SARIF Courier is a GitHub Action that takes a SARIF (Static Analysis Results Interchange Format) report and posts a beautifully formatted summary as a comment on your Pull Requests. This enables you to surface security and static analysis findings in your PR workflow, even if you do not have access to GitHub Advanced Security (GHAS).

- **No GHAS required:** Works for all repositories, public or private.
- **Instant feedback:** See security and code analysis results right in your PRs.
- **Easy integration:** Just drop the action in your workflow and point it to your SARIF file.

---

## 🚦 Usage

Add the following step to your workflow after generating a SARIF report:

```yaml
- name: Render SARIF in PR
  uses: Abdullah-Schahin/SARIFCourier@v1
  with:
    sarif_file: path/to/your-report.sarif
```

#### Output on PR
![image](https://github.com/user-attachments/assets/395920ca-f6e8-4ff1-9ccf-bb4dfda51ce1)



- `sarif_file` (**required**): Path to the SARIF file to process (relative to the workspace).

### Example Workflow

```yaml
name: Static Analysis
on:
  pull_request:
    branches: [main]
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
        uses: Abdullah-Schahin/SARIFCourier@v1
        with:
          sarif_file: results.sarif
```

---

## 🔑 Required Environment Variables & Permissions

- **GITHUB_TOKEN**: Provided automatically by GitHub Actions. Used to post comments on PRs.
  - **Permissions required:**
    - `contents: write` (to create/update comments)
    - `pull-requests: write` (recommended for private repos)

No additional secrets or configuration are needed.

---

> [!NOTE]
> SARIF Courier automatically uses environment variables provided by GitHub Actions for repository, pull request number, and other context. You do not need to set these manually—only `GITHUB_TOKEN` is required for posting comments. See the [GitHub Actions documentation](https://docs.github.com/en/actions/learn-github-actions/environment-variables) for more details.

---

## 📝 Inputs

| Name        | Description                        | Required | Default         |
|-------------|------------------------------------|----------|-----------------|
| sarif_file  | Path to the SARIF file to process. |   Yes    | results.sarif   |

---

## 💡 Why SARIF Courier?

- **Universal:** Works with any SARIF-compliant tool (CodeQL, Semgrep, ESLint, etc).
- **No vendor lock-in:** No need for GHAS or paid features.
- **Fast feedback:** Developers see issues before merging.

---

## 🛠️ License

MIT License. See [LICENSE](./LICENSE).

---

## 🙋‍♂️ Author

Abdullah Schahin
