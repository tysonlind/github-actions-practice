# File Encoder

A Python package for encoding files with various character encodings.

## Features

- CLI tool for encoding files with different character encodings
- Support for multiple encodings: UTF-8, UTF-16, UTF-32, ASCII, Latin-1, CP1252, and more
- Automatic encoding detection for input files
- Configurable output file paths
- Comprehensive test suite with pytest

## Installation

Install the package in development mode:

```bash
pip install -e .
```

For development with test dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

The package provides an `encode` command that can be used to encode files:

```bash
# Basic usage with default UTF-8 encoding
encode input.txt

# Specify a custom encoding
encode input.txt --encoding ascii

# Specify custom output file
encode input.txt --output encoded_file.txt --encoding utf-16

# Verbose output
encode input.txt --encoding latin-1 --verbose
```

### Python API

You can also use the FileEncoder class directly in your Python code:

```python
from file_encoder import FileEncoder

encoder = FileEncoder()

# Encode a file with default UTF-8 encoding
output_path = encoder.encode_file('input.txt')

# Encode with custom encoding and output path
output_path = encoder.encode_file(
    input_path='input.txt',
    output_path='encoded.txt',
    encoding='utf-16'
)

# Detect file encoding
encoding = encoder.get_file_encoding('somefile.txt')
```

## Supported Encodings

- utf-8 (default)
- utf-16
- utf-32
- ascii
- latin-1
- cp1252
- iso-8859-1
- windows-1252
- big5
- gb2312
- shift_jis

## Testing

Run the test suite with pytest:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=file_encoder
```

## Development

This project uses:
- `pyproject.toml` for project configuration
- `click` for the CLI interface
- `pytest` for testing
- Modern Python packaging standards

## GitHub Actions

https://docs.github.com/en/actions/get-started/quickstart
https://docs.github.com/en/billing/concepts/product-billing/github-actions
https://docs.aws.amazon.com/codebuild/latest/userguide/action-runner.html