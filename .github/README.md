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

## Branding
![SARIF Courier](https://img.shields.io/badge/SARIF-green?logo=shield)
