# SARIF2MD
Convert a SARIF Report to Markdown so it can be posted to Pull Request or Issues.

**SARIF2MD** is a lightweight, Python-based tool designed to convert SARIF (Static Analysis Results Interchange Format) security reports into clean, readable Markdown documents. With SARIF2MD, you can seamlessly transform complex SARIF reports into Markdown files suitable for GitHub Issues or Pull Request comments, making it easier to collaborate and address security concerns.

---

## Features

### Core Features:
- **SARIF Validation**: Ensures that the provided SARIF file adheres to the SARIF v2.1.0 schema.
- **Markdown Conversion**: Translates SARIF data into a well-structured Markdown format, highlighting tools, issues, severities, and locations.

### Additional Features:
- **Modular Architecture**: Cleanly separates validation, conversion, and utility functionalities for better maintainability.
- **Companion GitHub Action**: Automates the process of generating and posting Markdown reports directly within your CI/CD pipeline.

---

## Installation

### Prerequisites:
- Python 3.7 or later
- `pip` (Python package manager)

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/SARIF2MD.git
   cd SARIF2MD
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install the tool as a package:
   ```bash
   pip install .
   ```

---

## Usage

### Command-Line Usage:
Run the tool with the following command:

```bash
python main.py --input <path-to-sarif-file> --output <path-to-output-md>
```

- **`--input`**: Path to the SARIF file to be converted.
- **`--output`**: Path where the generated Markdown file will be saved.

Example:
```bash
python main.py --input example.sarif --output report.md
```

### Companion GitHub Action:
SARIF2MD comes with a GitHub Action to automate Markdown report generation. Add the following step to your `.github/workflows` YAML configuration:

```yaml
steps:
  - name: Checkout repository
    uses: actions/checkout@v3

  - name: Generate Markdown Report
    uses: your-repo/SARIF2MD-action@v1
    with:
      sarif_file: path/to/input.sarif
      output_md: path/to/output.md

  - name: Post Markdown as a comment
    uses: github-script@v6
    with:
      script: |
        github.rest.issues.createComment({
          owner: context.repo.owner,
          repo: context.repo.repo,
          issue_number: context.issue.number,
          body: fs.readFileSync('path/to/output.md', 'utf8'),
        });
```

---

## Project Structure

- `Converter.py`: Contains the logic for converting SARIF data into Markdown.
- `validator.py`: Validates the SARIF file against the schema.
- `utils.py`: Provides utility functions like loading the SARIF schema.
- `main.py`: Entry point for the application.

---

## Example Output

### Sample Markdown Report:

```
# SARIF Report

## Tool: CodeScanner

### Rule: CA1001
**Severity**: Error
**Message**: Class without a finalizer.
**Location**:
File: src/main.cpp, Line: 42

### Rule: CA2000
**Severity**: Warning
**Message**: Dispose objects correctly.
**Location**:
File: src/utils.cpp, Line: 87
```

---

## Contributing

We welcome contributions to SARIF2MD! Please open an issue or submit a pull request to help improve the tool.

---

## License

SARIF2MD is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- [SARIF Specification](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)
- [SARIF Python Library](https://github.com/microsoft/sarif-python-om)