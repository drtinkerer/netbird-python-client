---
layout: page
title: Installation Guide
description: How to install and set up the NetBird Python client
---

# Installation Guide

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Install from PyPI

The easiest way to install the NetBird Python client is using pip:

```bash
pip install netbird-client
```

### Development Installation

If you want to install the latest development version:

```bash
pip install git+https://github.com/bhushanrane/netbird-python-client.git
```

## Verify Installation

After installation, verify that the client is working correctly:

```python
import netbird
print(f"NetBird Python Client version: {netbird.__version__}")
```

## Dependencies

The NetBird Python client has minimal dependencies:

- **httpx** - Modern HTTP client for API requests
- **pydantic** - Data validation and serialization

These will be automatically installed when you install the client.

## Development Setup

If you want to contribute to the project or run tests:

### 1. Clone the Repository

```bash
git clone https://github.com/bhushanrane/netbird-python-client.git
cd netbird-python-client
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/netbird --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
```

## Troubleshooting

### Import Errors

If you encounter import errors:

```python
ImportError: No module named 'netbird'
```

Make sure you've:
1. Activated your virtual environment (if using one)
2. Installed the package correctly: `pip install netbird-client`
3. Are using the correct Python interpreter

### Version Conflicts

If you have dependency conflicts:

```bash
# Upgrade pip first
pip install --upgrade pip

# Install with force reinstall
pip install --force-reinstall netbird-client
```

### Python Version Issues

The NetBird client requires Python 3.8+. Check your Python version:

```bash
python --version
```

If you need to use multiple Python versions, consider using [pyenv](https://github.com/pyenv/pyenv).

## Next Steps

Once installation is complete, head to the [Quick Start Guide](quickstart.md) to begin using the NetBird Python client.

## Getting Help

If you encounter installation issues:

1. Check the [GitHub Issues](https://github.com/bhushanrane/netbird-python-client/issues)
2. Search for existing solutions
3. Create a new issue with:
   - Your Python version
   - Operating system
   - Full error message
   - Steps to reproduce