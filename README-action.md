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
