# FileJanitor

[![CI/CD](https://github.com/UBC-MDS/DSCI_524_FileJanitor/actions/workflows/deploy.yml/badge.svg)](https://github.com/UBC-MDS/DSCI_524_FileJanitor/actions/workflows/deploy.yml)
[![Docs](https://github.com/UBC-MDS/DSCI_524_FileJanitor/actions/workflows/publish.yml/badge.svg)](https://ubc-mds.github.io/DSCI_524_FileJanitor/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/FileJanitor?pypiBaseUrl=https%3A%2F%2Ftest.pypi.org)](https://test.pypi.org/project/FileJanitor/)
[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)
[![codecov](https://codecov.io/gh/UBC-MDS/DSCI_524_FileJanitor/branch/main/graph/badge.svg)](https://codecov.io/gh/UBC-MDS/DSCI_524_FileJanitor)

## Summary

FileJanitor is a package that cleans, standardizes, and organizes file names and folder structures.

## Overview usage

FileJanitor provides a set of utility functions to automate common-file system housekeeping tasks, such as renaming files, standardizing name conventions, ordering files, and restructuring directories. All functions operate on all files in a specialized folder unless specified.

Check deployment at: https://test.pypi.org/project/FileJanitor/

## Installation

### From PyPI (recommended)
Run in your terminal to install FileJanitor package:
```bash
pip install -i https://test.pypi.org/simple/ travelpy
```

## Functions and Examples

### Function 1: replace_pattern(pattern, replacement, dir)
Replaces the input pattern in file names with a new pattern or character. This function will:
- Support replacing characters or strings (_ -> &)
- Capitalize the first word of the file name.
- Apply changes to all files in the folder.

| Parameter | Type | Description |
|-----------|------|-------------|
| `pattern` | str |  The substring or character pattern to search for in filenames. |
| `replacement` | str | The string or character to replace the pattern with in filenames. |
| `dir` | str, optional | Path to the directory containing files to be modified. |

```python
from FileJanitor import replace_pattern

replace_pattern("_", " & ", "docs/") # Renames files like: "file_janitors.txt" -> "file & janitors.txt"
replace_pattern("_", " ")  # Uses current directory, renames files like: "my_file.txt" -> "my file.txt"
```

### Function 2: standardize_filename(dir, case, sep)
This function standardizes file names according to consistent formatting rules. This can be helpful when dealing with large collections of inconsistently named files.
- Replaces spaces and invalid characters with underscores (_).
- Converts dashes (-)  and spaces to underscores (_).
- Removes duplicate punctuation (..)
- Preserves file extensions

| Parameter | Type | Description |
|-----------|------|-------------|
| `dir` | str |  Path to the directory containing files to be standardized |
| `case` | str, optional | Desired casing for filenames (default is 'lower') |
| `sep` | str, optional | Character to use as the separator between words in filenames (default is '_') |

```python
from FileJanitor import standardize_filename

standardize_filename("data/", case="title", sep="-") # Renames files in data/ like: "my file NAME.txt" -> "My-File-Name.txt"
```
### Function 3. index_files(dir, order, unlisted) 
This function orders the files in each folder according to a defined order.

| Parameter | Type | Description |
|-----------|------|-------------|
| `dir` | str |  Path to the target directory containing the files that need to be indexed |
| `order` | list | List of filenames defining the desired order. |
| `unlisted ` | str, optional |  How to handle files not in `order`, accepts "hide" to move files to subdirectory named "_unlisted, or "keep" to leave at end with sequential numbering |

```python
from FileJanitor import index_files

index_files("my_thesis", order = ["intro.pdf", "analysis.pdf", "discussion.pdf", "conclusions.pdf"])
```

**Before:**
```bash
my_thesis/
├── discussion.pdf
├── intro.pdf
├── conclusions.pdf
└── analysis.pdf
```
**After:**
```bash
my_thesis/
├── 01_intro.pdf
├── 02_analysis.pdf
├── 03_discussion.pdf
└── 04_conclusions.pdf
```

### Function 4. flatten(nested_directory, output_directory, recursive) 
This function will move all files from nested subfolders into a single target directory. 
- By default, only files directly inside 'nested_directory' are moved.
- If 'recursive' is True, files from all nested subdirectories are also moved.

| Parameter | Type | Description |
|-----------|------|-------------|
| `nested_directory` | str |  Root directory containing files and nested subdirectories to flatten. |
| `output_directory` | str, optional |  Directory where flattened files will be moved. |
| `recursive` | bool, optional | Whether to move files from nested subdirectories recursively (default is False) |

```python
from FileJanitor import flatten

flatten("data/", recursive=True)
```

**Before:**
```bash
cwd/
├── data/
│   ├── raw/
│   │   └── file1.csv
│   └── processed/
│       └── file2.csv
```
**After:**
```bash
cwd/
├── file1.csv
├── file2
```

## Testing

To run the test suite, first install the package with test dependencies:

```bash
pip install -e .[tests]
pytest
```

To run tests for a specific file:

```bash
pytest tests/unit/test_replace_pattern.py
```

## Documentation

**Full documentation is available at:** https://ubc-mds.github.io/DSCI_524_FileJanitor/

The documentation includes:
- [Getting Started Guide](https://ubc-mds.github.io/DSCI_524_FileJanitor/getting-started.html)
- [Usage Examples](https://ubc-mds.github.io/DSCI_524_FileJanitor/examples.html)
- [Function Reference](https://ubc-mds.github.io/DSCI_524_FileJanitor/reference/) 

## Development Setup

### Installation for Development
```bash
# Clone the repository
git clone https://github.com/UBC-MDS/DSCI_524_FileJanitor.git
cd DSCI_524_FileJanitor

# Install in editable mode with all dependencies
pip install -e ".[dev,docs,tests]"
```

### Building Documentation Locally
```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build the reference documentation
quartodoc build

# Preview documentation in your browser
quarto preview
```

### Deploying Documentation

Documentation is **automatically deployed** to GitHub Pages when changes are merged to the `main` branch.

**Deployment workflow:**
1. The team member creates a pull request (PR) with documentation changes
2. The PR gets reviewed and approved by a team member
3. The PR is merged to `main`
4. GitHub Actions runs `.github/workflows/publish.yml`
5. The documentation is built and deployed to the `gh-pages` branch
6. The changes are at https://ubc-mds.github.io/DSCI_524_FileJanitor/

## Similar Packages

FileJanitor is a high-level package built on top of libraries such as ```os```, ```pathlib```, and ```shutil```. While many Python libraries provide low-level tools for working with files, they do not offer built in functions for tasks such as standardizing file names, reordering files, and flattening directory structures. FileJanitor abstracts these low level capabilities into a simple Python Package that allows users to perform common cleanup tasks with ease.

## Contributors

* **Sean Brown** ([@SeanBrown12345](https://github.com/SeanBrown12345))
* **Sam Lokanc** ([@SamLokanc](https://github.com/SamLokanc))
* **Rabin Duran** ([@rabin0208](https://github.com/rabin0208))
* **Luis Alonso Alvarez** ([@luisalonso8](https://github.com/luisalonso8))

## Copyright

- Copyright © 2026 Sean Brown, Sam Lokanc, Rabin Duran, Luis Alonso Alvarez.
- Free software distributed under the [MIT License](./LICENSE).
