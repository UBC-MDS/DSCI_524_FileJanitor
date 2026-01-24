# FileJanitor

|        |        |
|--------|--------|
| CI/CD | [![Deploy to Test PyPI](https://github.com/UBC-MDS/DSCI_524_FileJanitor/actions/workflows/deploy.yml/badge.svg)](https://github.com/UBC-MDS/DSCI_524_FileJanitor/actions/workflows/deploy.yml) |
| Meta   | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) |


## Summary

FileJanitor is a package that cleans, standardizes, and organizes file names and folder structures.

## Contributors

* **Sean Brown** ([@SeanBrown12345](https://github.com/SeanBrown12345))
* **Sam Lokanc** ([@SamLokanc](https://github.com/SamLokanc))
* **Rabin Duran** ([@rabin0208](https://github.com/rabin0208))
* **Luis Alonso Alvarez** ([@luisalonso8](https://github.com/luisalonso8))

## Overview usage

FileJanitor provides a set of utility functions to automate common-file system housekeeping tasks, such as renaming files, standardizing name conventions, ordering files, and restructuring directories. All functions operate on all files in a specialized folder unless specified.

## Features

### Function 1: Pattern Replacement in File Names
Replaces the input pattern in file names with a new pattern or character. This function will:
•	Support replacing characters or strings (_ -> &)
•	Capitalize the first word of the file name.
•	Apply changes to all files in the folder.

```bash
file_janitors.txt → File & janitors.txt
```
### Function 2: File name standardization
This function standardizes file names according to consistent formatting rules. This can be helpful when dealing with large collections of inconsistently named files.
•	Replaces spaces and invalid characters with underscores (_).
•	Converts dashes (-)  and spaces to underscores (_).
•	Removes duplicate punctuation (..)
•	Preserves file extensions

```bash
___Final-csv.csv → FINAL_CSV.csv
other 03-file.csv → OTHER_03_FILE.csv
```
### Function 3. Indexing files
This function orders the files in each folder according to a defined order.

Consider the following folder:

```bash
my_thesis_folder/
├── discussion.pdf
├── intro.pdf
├── conclusions.pdf
└── analysis.pdf
```
Then, the desired order should be like this:

```bash
order = [
    "intro.pdf",
    "analysis.pdf",
    "discussion.pdf",
    "conclusions.pdf"
]
```
Output:
```bash
my_thesis_folder/
├── intro.pdf
├── analysis.pdf
├── discussion.pdf
└── conclusions.pdf
```

### Function 4. Flattening Directories


This function will move all files from nested subfolders into a single target directory. This is useful in case someone wants all files at the same directory level. The folder structure is ignored during flattening.

```bash
project_root/
├── data/
│   ├── raw/
│   │   └── file1.csv
│   └── processed/
│       └── file2.csv
```

```bash
project_root/
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

## Copyright

- Copyright © 2026 Sean Brown, Sam Lokanc, Rabin Duran, Luis Alonso Alvarez.
- Free software distributed under the [MIT License](./LICENSE).
